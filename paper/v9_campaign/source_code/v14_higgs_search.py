#!/usr/bin/env python3
"""
TRXT V14: HIGGS & MASS TERM SEARCH
==================================
Module 4: Mass Mechanism
Goal: Find an algebraic element Phi that couples Left and Right fermions.
Criteria:
1. Interactions: < Psi_L | Phi * Psi_R > != 0 (Yukawa Term)
2. Symmetry: Must be Color Singlet.
3. Symmetry: Must have Electric Charge 0 (after breaking) or correct Q for Higgs.
4. Representation: Identify if Phi transforms as an SU(2) doublet.
"""
import numpy as np
import json
import os

# =============================================================================
# 1. SETUP ALGEBRA & BASIS (Standard V12)
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

# Minimal Left Ideal S
P = 0.5 * (I_64 + iC @ eL[7])
U, S_vals, Vt = np.linalg.svd(P)
rank = np.sum(S_vals > 1e-5)
basis_S = U[:, :rank] # 32 dims

def get_S_op(Op): return basis_S.T @ Op @ basis_S

# =============================================================================
# 2. DEFINE STATES (L/R)
# =============================================================================
# Re-construct L/R projectors
Gammas = []
for k in range(1, 7): Gammas.append(iC @ eL[k])
G_vol = Gammas[0]
for k in range(1, 6): G_vol = G_vol @ Gammas[k]
Gamma7_S = get_S_op(1j * G_vol)
Id_S = np.eye(32)
P_L = 0.5 * (Id_S + Gamma7_S)
P_R = 0.5 * (Id_S - Gamma7_S)

# Identify a specific electron state e_L and e_R for testing
# Q operator for filtering
P_color_8 = np.zeros((8,8)); 
for k in range(1, 7): P_color_8[k,k] = 1.0
P_color_S = get_S_op(kron3(np.eye(2), np.eye(4), P_color_8))
I3_S = get_S_op(0.5 * iH)
I3_R = -1j * I3_S @ P_R # Check def
# My previous definition of I3_Right was -1j * I3_S @ P_R.
# Wait. I3_Left was -1j * I3_S @ P_L.
# Use consistent definition from V12.
I3_L_op = -1j * I3_S @ P_L
I3_R_op = -1j * I3_S @ P_R
B_minus_L = (4.0/3.0) * P_color_S - Id_S
Y_Op = B_minus_L + 2.0 * I3_R_op
Q_Op = I3_L_op + 0.5 * Y_Op

def get_state(name_filter):
    # Find eigenvector of Q_Op with specific properties
    # Just grab first one matching
    # Diagonalize Q, P_L/R etc.
    vals, vecs = np.linalg.eigh(Q_Op + 0.1 * P_L + 0.01 * P_color_S)
    for i in range(32):
        v = vecs[:, i]
        q = np.vdot(v, Q_Op @ v).real
        is_l = np.vdot(v, P_L @ v).real > 0.5
        is_color = np.vdot(v, P_color_S @ v).real > 0.5
        
        if name_filter == "e_L":
            if abs(q + 1.0) < 0.1 and is_l and not is_color: return v
        if name_filter == "e_R":
            # e_R has Q=-1, Right
            if abs(q + 1.0) < 0.1 and not is_l and not is_color: return v
        if name_filter == "nu_L":
            # Q=0, L
            if abs(q) < 0.1 and is_l and not is_color: return v
            
    return None

vec_eL = get_state("e_L")
vec_eR = get_state("e_R")
vec_nuL = get_state("nu_L")

if vec_eL is None or vec_eR is None:
    print("Error: Could not isolate e_L / e_R states.")
    exit()

# =============================================================================
# 3. HIGGS SEARCH
# =============================================================================
# We need an element M in the algebra (64x64 matrix) such that:
# < e_L | M | e_R > != 0.
# And M must "look like" a Higgs.
# Candidate: Elements of the Algebra not in the Gauge Group.
# Specifically, directions in C x H x O.
# Try generic basis elements.

print("Searching for Mass Term Candidates (Yukawa Coupling)...")
print(f"Testing coupling between e_L and e_R...")

candidates = []

# Basis: 1, iC, H-units, O-units?
# Let's iterate over C x H x O basis elements.
# 2 x 4 x 8 = 64 elements.
# basis_64[i]

basis_64_ops = []
basis_names = []

labels_C = ['1', 'i']
labels_H = ['1', 'i', 'j', 'k']
labels_O = ['e0', 'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7']

for ic, c_lab in enumerate(labels_C):
    for ih, h_lab in enumerate(labels_H):
        for io, o_lab in enumerate(labels_O):
            # Construct Op
            op = kron3(rep_C(c_lab if c_lab!='1' else 1), 
                       rep_H(h_lab if h_lab!='1' else 1), 
                       O_mats[io])
            
            # Project onto Ideal S to see effective term
            op_S = get_S_op(op)
            
            # Check Coupling
            # Yukawa ~ v_eL.hm * op_S * v_eR
            coupling = np.vdot(vec_eL, op_S @ vec_eR)
            mag = abs(coupling)
            
            if mag > 1e-5:
                # Found a candidate!
                # Check if it also couples nu_L to something?
                candidates.append({
                    "name": f"C({c_lab})xH({h_lab})xO({o_lab})",
                    "coupling_mag": mag,
                    "op": op_S
                })

print(f"Found {len(candidates)} algebra elements that couple e_L to e_R.")

# Filter for "Scalar-like" properties?
# A Higgs field must transform as a doublet under SU(2).
# Meaning: [T_su2, Phi] != 0.
# If Phi is a singlet (like Real mass), it commutes.
# Let's check commutator with Isospin T3.

T_su2_3 = get_S_op(0.5 * kron3(rep_C(1), rep_H('i'), O_mats[0])) @ P_L # Only acts on L
# Wait. The Higgs field Phi is a field in the Lagrangian.
# The term is Psi_bar Phi Psi.
# Under SU(2): Psi_L -> U Psi_L. Psi_R -> Psi_R.
# Term: (U Psi_L)^dag Ph U_phi? No.
# Psi_L^dag U^dag Phi Psi_R.
# For invariance, we need U^dag Phi = Phi? No.
# Psi_L^dag Phi Psi_R
# Transformed: Psi_L^dag U^dag Phi Psi_R.
# This must equal original. So U^dag Phi = Phi => U Phi = Phi.
# This implies Phi is a singlet under SU(2)?
# NO.
# In SM, the term is (bar L) dot (Phi R). No.
# It's bar{L} Phi R ?? 
# L is doublet. R is singlet. Phi is Doublet.
# The contraction is (bar{L}_a Phi_a) R.
# So Phi must carry an index 'a' to contract with L.
# In our algebra, the "index" is internal direction.
# Does multiplication by an element M "rotate" the Left state into a Right state?
# Yes.
# The candidates we found do exactly that: M |R> -> |L_like>.
# So <L| M |R> is non-zero.

print("\nAnalyzing Candidates for SU(2) Transformation Properties:")
# We want to see if {Phi_real, Phi_imag} form a doublet.
# Or just identify the "Higgs Direction".

# We assume the vacuum Higgs is one specific direction (VEV).
# Does picking a candidate break SU(2)?
# i.e. does [Su2_gen, Candidate] != 0?

su2_gen = 0.5 * kron3(rep_C(1), rep_H('i'), O_mats[0]) # Generic T3
su2_gen_S = get_S_op(su2_gen)

for cand in candidates[:5]: # Show top 5
    op = cand['op']
    comm = su2_gen_S @ op - op @ su2_gen_S # Commutator
    comm_norm = np.linalg.norm(comm)
    print(f"  {cand['name']}: Coupling={cand['coupling_mag']:.2f}, [T3, Phi] Norm={comm_norm:.2f}")

# Search for the "Standard Mass" direction if valid.
# Ideally H(1) is mass?
# Let's check C(1)xH(1)xO(e0) (Identity).
# <L| 1 |R> ?
ortho_check = np.vdot(vec_eL, vec_eR)
print(f"\nOrthogonality Check <eL|eR> = {abs(ortho_check):.2e}")
# If L and R are orthogonal, Identity cannot couple them.
# So Mass requires a non-Identity element.
# This confirms Mass MUST break some symmetry or use specific gamma matrix.
# In Dirac theory, mass term is gamma0.
# In our Chiral basis, L and R are eigenstates of Gamma7.
# We need an operator that ANTICOMMUTES with Gamma7.
# {Gamma7, M} = 0.
# This operator flips Chirality: M |R> ~ |L>.

print("\nChecking Anti-Commutation with Chirality (Gamma7):")
valid_mass_terms = []
for cand in candidates:
    op = cand['op']
    # Check {G7, M}
    anti = Gamma7_S @ op + op @ Gamma7_S
    anti_norm = np.linalg.norm(anti)
    if anti_norm < 1e-4:
        valid_mass_terms.append(cand)

print(f"Found {len(valid_mass_terms)} candidates that flip chirality perfectly (Valid Mass Terms).")
for v in valid_mass_terms[:5]:
    print(f"  Valid Higgs VEV Direction: {v['name']}")

# Export result
with open("results/higgs_candidates.json", "w") as f:
    # Convert numpy types
    out = []
    for c in valid_mass_terms:
        out.append({
            "name": c['name'],
            "coupling": float(c['coupling_mag'])
        })
    json.dump(out, f, indent=2)
    
print("Artifact saved: results/higgs_candidates.json")
