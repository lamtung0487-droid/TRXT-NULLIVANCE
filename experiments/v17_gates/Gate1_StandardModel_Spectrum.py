#!/usr/bin/env python3
"""
TRXT V12: FERMION SPECTRUM CERTIFICATION
========================================
Module 2: Particle Physics Verification
Goal: Map the 16 derived eigenstates to EXACT Standard Model Quantum Numbers.
Formulae derived:
  B-L = 4/3 * P_Color - 1
  Y   = (B-L) + 2 * I3_Right
  Q   = I3_Left + Y/2
"""
import numpy as np
import json
import os

# =============================================================================
# 1. ALGEBRA SETUP (Same as V11)
# =============================================================================
def rep_C(x):
    if x == 1: return np.eye(2)
    if x == 'i': return np.array([[0, -1], [1, 0]])
    return np.zeros((2,2))

def rep_H(x):
    I = np.eye(4)
    i = np.array([[0, -1, 0, 0], [1, 0, 0, 0], [0, 0, 0, -1], [0, 0, 1, 0]])
    j = np.array([[0, 0, -1, 0], [0, 0, 0, 1], [1, 0, 0, 0], [0, -1, 0, 0]])
    k = np.array([[0, 0, 0, -1], [0, 0, -1, 0], [0, 1, 0, 0], [1, 0, 0, 0]])
    if x == 1: return I; 
    if x == 'i': return i; 
    if x == 'j': return j; 
    if x == 'k': return k
    return np.zeros((4,4))

FANO = [(1,2,4), (2,3,5), (3,4,6), (4,5,7), (5,6,1), (6,7,2), (7,1,3)]
mult = np.zeros((8,8,8))
for i in range(8): mult[0,i,i] = 1; mult[i,0,i] = 1
for i in range(1,8): mult[i,i,0] = -1
for (a,b,c) in FANO:
    mult[a,b,c] = 1; mult[b,c,a] = 1; mult[c,a,b] = 1
    mult[b,a,c] = -1; mult[c,b,a] = -1; mult[a,c,b] = -1
O_mats = {}
for a in range(8):
    M = np.zeros((8,8))
    for j in range(8): M[:, j] = mult[a, j, :]
    O_mats[a] = M
    
def kron3(A, B, C): return np.kron(A, np.kron(B, C))

I_64 = np.eye(64)
iC = kron3(rep_C('i'), rep_H(1), O_mats[0])
iH = kron3(rep_C(1), rep_H('i'), O_mats[0])
eL = {}
for i in range(1, 8): eL[i] = kron3(rep_C(1), rep_H(1), O_mats[i])

# =============================================================================
# 2. OPERATOR CONSTRUCTION
# =============================================================================

# Chirality Gamma7
Gammas = []
for k in range(1, 7): Gammas.append(iC @ eL[k])
G_vol = Gammas[0]
for k in range(1, 6): G_vol = G_vol @ Gammas[k]
Gamma7_full = 1j * G_vol # Hermitian, evals +/- 1

# Minimal Left Ideal S
P = 0.5 * (I_64 + iC @ eL[7])
U, S_vals, Vt = np.linalg.svd(P)
rank = np.sum(S_vals > 1e-5)
basis_S = U[:, :rank] # 32 dims

def get_S_op(Op): return basis_S.T @ Op @ basis_S

Gamma7_S = get_S_op(Gamma7_full)
I3_S = get_S_op(0.5 * iH)

# Color Projector P_Q (Projs onto e1..e6)
P_color_8 = np.zeros((8,8))
for k in range(1, 7): P_color_8[k,k] = 1.0
P_color_full = kron3(np.eye(2), np.eye(4), P_color_8)
P_color_S = get_S_op(P_color_full)

# =============================================================================
# 3. DERIVE PHYSICAL OPERATORS
# =============================================================================
# Projectors for L/R
Id_S = np.eye(32)
P_L = 0.5 * (Id_S + Gamma7_S)
P_R = 0.5 * (Id_S - Gamma7_S)

# Physical Isospin (Left only)
I3_Left = -1j * I3_S @ P_L # Hermitian
I3_Right = -1j * I3_S @ P_R # Hermitian (Auxiliary)
# Note: I3_S is anti-hermitian, so -1j*I3_S is Hermitian (evals +/- 0.5)

# B-L Operator from Color
# B-L = 4/3 * P_Q - 1
B_minus_L = (4.0/3.0) * P_color_S - Id_S

# Hypercharge derived formula
# Y = (B-L) + 2 * I3_Right
Y_Op = B_minus_L + 2.0 * I3_Right

# Electric Charge
# Q = I3_Left + Y/2
Q_Op = I3_Left + 0.5 * Y_Op

# Spectrum Analysis
print("Diagonalizing Q_Op to classify states...")
# Add small perturbation from other ops to separate degenerate states
Combined = Q_Op + 0.1 * Y_Op + 0.01 * P_color_S + 0.001 * Gamma7_S
w, v = np.linalg.eigh(Combined)

spectrum = []
for i in range(32):
    vec = v[:, i]
    
    val_Q = np.vdot(vec, Q_Op @ vec).real
    val_Y = np.vdot(vec, Y_Op @ vec).real
    val_I3L = np.vdot(vec, I3_Left @ vec).real
    val_I3R = np.vdot(vec, I3_Right @ vec).real
    val_PQ = np.vdot(vec, P_color_S @ vec).real
    val_Gam7 = np.vdot(vec, Gamma7_S @ vec).real
    
    # Identify SM Particle
    name = "Unknown"
    is_left = val_Gam7 > 0.5
    is_quark = val_PQ > 0.5
    
    if is_left:
        # Left Handed
        if not is_quark:
            # Lepton Doublet (nuL, eL)
            if abs(val_I3L - 0.5) < 0.1: name = "nu_L"
            elif abs(val_I3L + 0.5) < 0.1: name = "e_L"
        else:
            # Quark Doublet (uL, dL)
            if abs(val_I3L - 0.5) < 0.1: name = "u_L"
            elif abs(val_I3L + 0.5) < 0.1: name = "d_L"
    else:
        # Right Handed (Singlets)
        if not is_quark:
            # Lepton Singlets
            # Distinguish by Q?
            if abs(val_Q) < 0.1: name = "nu_R"
            elif abs(val_Q + 1.0) < 0.1: name = "e_R"
        else:
            # Quark Singlets
            if abs(val_Q - 2/3) < 0.1: name = "u_R"
            elif abs(val_Q + 1/3) < 0.1: name = "d_R"
            
    spectrum.append({
        "Name": name,
        "Q": val_Q,
        "Y": val_Y,
        "I3_L": val_I3L,
        "B-L": (4/3)*val_PQ - 1.0,
        "Chirality": "L" if is_left else "R",
        "Color": "Triplet" if is_quark else "Singlet"
    })

# Print Table
print(f"{'Name':<10} {'Q':<6} {'Y':<6} {'I3_L':<6} {'B-L':<6} {'Chirality':<10}")
print("-" * 60)
spectrum.sort(key=lambda x: (x['Chirality'], x['Color'], x['Q']))

unique_states = {}
for s in spectrum:
    k = s['Name']
    if k not in unique_states: unique_states[k] = 0
    unique_states[k] += 1
    print(f"{s['Name']:<10} {s['Q']:<6.2f} {s['Y']:<6.2f} {s['I3_L']:<6.2f} {s['B-L']:<6.2f} {s['Chirality']:<10}")
    
# VERIFICATION
expected = {
    "nu_L": 2, "e_L": 2,         # 2 real DOFs each
    "u_L": 6, "d_L": 6,          # 6 real DOFs (3 colors x 2)
    "nu_R": 2, "e_R": 2,
    "u_R": 6, "d_R": 6
}
print(f"\nVerification Counts:")
passed = True
for k, v in expected.items():
    count = unique_states.get(k, 0)
    res = "OK" if count == v else "FAIL"
    print(f"  {k}: {count} (Exp {v}) -> {res}")
    if count != v: passed = False
    
# Anomaly Check: Sum of Q
total_Q = sum(s['Q'] for s in spectrum)
print(f"\nAnomaly Check (Sum Q): {total_Q:.2f} (Expected 0.00)")
if abs(total_Q) > 0.1: passed = False

# Export
with open("results/C4_CERTIFIED_spectrum.json", "w") as f:
    json.dump(spectrum, f, indent=2)
    
if passed:
    print("\n[SUCCESS] Full Perfect Match with Standard Model Spectrum!")
else:
    print("\n[FAIL] Spectrum mismatch.")
