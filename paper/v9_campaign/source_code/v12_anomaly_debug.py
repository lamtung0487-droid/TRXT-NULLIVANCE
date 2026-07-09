#!/usr/bin/env python3
"""
V10 A2: ANOMALY SUM Q DIAGNOSTIC
=================================
Goal: Determine if Sum Q = 0.08 is a rounding artifact or a real physics bug.

We re-run the same algebra but:
1. Print UNROUNDED Q values (full precision).
2. Compute Sum Q from unrounded values.
3. Also compute Tr(Q_Op) directly (algebraic trace = exact anomaly check).
"""
import numpy as np

# =============================================================================
# 1. ALGEBRA SETUP (Exact copy from v12_fermion_certification.py)
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
Gammas = []
for k in range(1, 7): Gammas.append(iC @ eL[k])
G_vol = Gammas[0]
for k in range(1, 6): G_vol = G_vol @ Gammas[k]
Gamma7_full = 1j * G_vol

P = 0.5 * (I_64 + iC @ eL[7])
U, S_vals, Vt = np.linalg.svd(P)
rank = np.sum(S_vals > 1e-5)
basis_S = U[:, :rank]

def get_S_op(Op): return basis_S.T @ Op @ basis_S

Gamma7_S = get_S_op(Gamma7_full)
I3_S = get_S_op(0.5 * iH)

P_color_8 = np.zeros((8,8))
for k in range(1, 7): P_color_8[k,k] = 1.0
P_color_full = kron3(np.eye(2), np.eye(4), P_color_8)
P_color_S = get_S_op(P_color_full)

Id_S = np.eye(32)
P_L = 0.5 * (Id_S + Gamma7_S)
P_R = 0.5 * (Id_S - Gamma7_S)

I3_Left = -1j * I3_S @ P_L
I3_Right = -1j * I3_S @ P_R

B_minus_L = (4.0/3.0) * P_color_S - Id_S
Y_Op = B_minus_L + 2.0 * I3_Right
Q_Op = I3_Left + 0.5 * Y_Op

# =============================================================================
# 3. DIAGNOSTIC: Exact Algebraic Trace
# =============================================================================
print("=" * 70)
print("V10 ANOMALY DIAGNOSTIC")
print("=" * 70)

# Method 1: Exact Matrix Trace (No diagonalization needed)
trace_Q = np.trace(Q_Op).real
print(f"\n[METHOD 1] Tr(Q_Op) = {trace_Q:.15f}")
print(f"  This is the EXACT algebraic anomaly.")
print(f"  If Tr(Q) = 0, the anomaly cancels EXACTLY in the algebra.")
print(f"  If Tr(Q) != 0, there is a REAL physics problem.")

# Decompose to understand
trace_I3L = np.trace(I3_Left).real
trace_Y = np.trace(Y_Op).real
trace_BL = np.trace(B_minus_L).real
trace_I3R = np.trace(I3_Right).real
trace_Pcolor = np.trace(P_color_S).real

print(f"\n[DECOMPOSITION]")
print(f"  Tr(Q_Op) = Tr(I3_Left) + 0.5 * Tr(Y_Op)")
print(f"  Tr(I3_Left)  = {trace_I3L:.15f}")
print(f"  Tr(Y_Op)     = {trace_Y:.15f}")
print(f"  Tr(B-L)      = {trace_BL:.15f}")
print(f"  Tr(I3_Right) = {trace_I3R:.15f}")
print(f"  Tr(P_color)  = {trace_Pcolor:.15f}")
print(f"  Check: {trace_I3L:.6f} + 0.5 * {trace_Y:.6f} = {trace_I3L + 0.5*trace_Y:.6f}")

# Method 2: Sum of eigenvalues (unrounded)
print(f"\n[METHOD 2] Diagonalization (Unrounded)")
Combined = Q_Op + 0.1 * Y_Op + 0.01 * P_color_S + 0.001 * Gamma7_S
w, v = np.linalg.eigh(Combined)

sum_Q_unrounded = 0.0
sum_Q_rounded = 0.0
for i in range(32):
    vec = v[:, i]
    val_Q = np.vdot(vec, Q_Op @ vec).real
    val_Q_rounded = round(val_Q, 2)
    sum_Q_unrounded += val_Q
    sum_Q_rounded += val_Q_rounded
    print(f"  State {i:2d}: Q_exact = {val_Q:+.10f}   Q_rounded = {val_Q_rounded:+.2f}")

print(f"\n  Sum Q (unrounded): {sum_Q_unrounded:.15f}")
print(f"  Sum Q (rounded):   {sum_Q_rounded:.2f}")

# Diagnosis
print(f"\n{'='*70}")
print("DIAGNOSIS")
print(f"{'='*70}")
if abs(trace_Q) < 1e-10:
    print("  [OK] Tr(Q_Op) = 0 EXACTLY.")
    print("  The anomaly DOES cancel in the algebra.")
    if abs(sum_Q_rounded) > 0.01:
        print(f"  [WARN] Sum Q (rounded) = {sum_Q_rounded:.2f} is a ROUNDING ARTIFACT.")
        print("  The original code rounds Q to 2 decimals before summing.")
        print("  For quarks: Q = +/-1/3 ~ +/-0.33, Q = +/-2/3 ~ +/-0.67")
        print("  Rounding error per quark: ~0.003")
        print("  With 24 quarks: total error ~24 x 0.003 = 0.07-0.08")
        print("  -> THIS EXPLAINS Sum Q = 0.08!")
        print("")
        print("  FIX: Use exact fractions or round to 4+ decimals.")
    else:
        print("  [OK] Both exact and rounded sums are zero. No issue.")
else:
    print(f"  [FAIL] Tr(Q_Op) = {trace_Q:.10f} != 0")
    print("  This is a REAL PHYSICS PROBLEM in the algebra construction.")
