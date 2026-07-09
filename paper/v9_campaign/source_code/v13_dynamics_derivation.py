#!/usr/bin/env python3
"""
TRXT V13: DYNAMICS & COUPLING CONSTANT DERIVATION
=================================================
Module 3: Dynamics
Goal: 
1. Compute Trace Normalizations of derived SU(3), SU(2), U(1) generators.
2. Predict Weinberg Angle at Unification: sin^2(theta_W) = g1^2 / (g1^2 + g2^2).
3. Investigate Mass Terms (Yukawa potential candidates).
"""
import numpy as np
import json
import os

# =============================================================================
# 1. RECONSTRUCT GENERATORS (From V12 Logic)
# =============================================================================
# We need to rebuild the exact matrices used in V12 to compute their traces.

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
# 2. DEFINING THE GENERATORS (Algebraic Form)
# =============================================================================

# Minimal Left Ideal S Projection
P = 0.5 * (I_64 + iC @ eL[7])
U, S_vals, Vt = np.linalg.svd(P)
rank = np.sum(S_vals > 1e-5)
basis_S = U[:, :rank] 
def get_S_op(Op): return basis_S.T @ Op @ basis_S

# 2.1 SU(2) Generators (Weak Isospin)
# T_L^i correspond to quaternion units i, j, k acting on S.
# Specifically, 0.5 * iH, 0.5 * jH, 0.5 * kH? 
# Wait, chiral projection needed.
# SM SU(2) only acts on Left Handed states.
# So T_a = P_L @ (0.5 * q_a) @ P_L.

# Chirality
Gammas = []
for k in range(1, 7): Gammas.append(iC @ eL[k])
G_vol = Gammas[0]
for k in range(1, 6): G_vol = G_vol @ Gammas[k]
Gamma7_S = get_S_op(1j * G_vol)
Id_S = np.eye(32)
P_L = 0.5 * (Id_S + Gamma7_S)

factor_su2 = 0.5
T_su2_1 = get_S_op(factor_su2 * kron3(rep_C(1), rep_H('i'), O_mats[0])) @ P_L
T_su2_2 = get_S_op(factor_su2 * kron3(rep_C(1), rep_H('j'), O_mats[0])) @ P_L
T_su2_3 = get_S_op(factor_su2 * kron3(rep_C(1), rep_H('k'), O_mats[0])) @ P_L

# 2.2 SU(3) Generators (Color)
# Standard Gell-Mann matrices embedded in Octonions e1..e6.
# We need to construct them explicitly.
# Based on V11/V12, they are linear combos of [ei, ej].
# Let's use the Projector P_color to define the normalization volume?
# Better: Construct one explicit generator, e.g., T3 (Isospin of Color) and T8 (Hypercharge of Color).
# T_color_3 = 0.5 * (eL[1]@eL[2] - eL[2]@eL[1]) # Rotation in 1-2 plane
# This acts on L and R quarks.
T_su3_3_full = 0.5 * (eL[1]@eL[2] - eL[2]@eL[1])
T_su3_3 = get_S_op(T_su3_3_full)

# 2.3 U(1) Generator (Hypercharge Y)
# We derived Y = (4/3 P_Q - 1) + 2 I3_R.
# P_Q is Color Projector.
P_color_8 = np.zeros((8,8))
for k in range(1, 7): P_color_8[k,k] = 1.0
P_color_S = get_S_op(kron3(np.eye(2), np.eye(4), P_color_8))

P_R = 0.5 * (Id_S - Gamma7_S)
I3_R = get_S_op(0.5 * iH) @ P_R # Isospin acting on Right sector only

Y_gen = ( (4.0/3.0)*P_color_S - Id_S ) + 2.0 * I3_R

# =============================================================================
# 3. COMPUTE TRACE NORMALIZATIONS
# =============================================================================
# In unified theories, couplings g_i are related by k_i * g_i^2 = const.
# k_i = Tr(T_i^2) over the full representation (generation).
# For SU(N), standard normalization is Tr(T^2) = 1/2.
# We compute k_i for our derived operators.

print("Computing Trace Normalizations (Sum of squared eigenvalues)...")

# SU(2) trace
# T_su2_3 is 32x32.
# Tr(T3^2). T3 is anti-hermitian? 
# Our T_su2_3 above is anti-hermitian (iH).
# We want Tr( (i*T)^2 ) or -Tr(T^2).
# Let's compute norm squared: Tr(T dagger T).
k2 = np.trace(T_su2_3.conj().T @ T_su2_3).real
print(f"  k2 (SU2) = {k2:.2f}")
# Expected: Left Doublets only.
# 4 Lepton Doublets (e, nu) + 12 Quark Doublets (u, d x3 colors)?
# Wait.
# Standard generation:
# L (doublet): T3 = +/- 1/2. Sum sq = 1/4 + 1/4 = 1/2.
# Q (doublet, 3 colors): 3 * (1/2) = 3/2.
# Total for 1 gen: 1/2 + 3/2 = 2.
# We expect k2 = 2.0 (in standard normalization units).

# SU(3) trace
# T_su3_3 acts on Quarks only (L and R).
# Leptons are singlets (0).
# Quarks: u_L, d_L, u_R, d_R.
# Each is a triplet.
# T3 eigenvalues: 1/2, -1/2, 0 for the triplet components.
# Sum sq = 1/4 + 1/4 = 1/2 per triplet.
# We have 4 triplets (uL, dL, uR, dR).
# Total k3 = 4 * 1/2 = 2.0.
k3 = np.trace(T_su3_3.conj().T @ T_su3_3).real
print(f"  k3 (SU3) = {k3:.2f}")

# U(1) Hypercharge trace
# Y values in SM:
# e_L: -1 -> 1
# nu_L: -1 -> 1
# u_L: 1/3 -> 1/9 * 3 colors = 1/3
# d_L: 1/3 -> 1/9 * 3 colors = 1/3
# e_R: -2 -> 4
# nu_R: 0 -> 0
# u_R: 4/3 -> 16/9 * 3 = 16/3
# d_R: -2/3 -> 4/9 * 3 = 4/3
# Total Y^2 sum:
# 1 + 1 + 1/3 + 1/3 + 4 + 0 + 16/3 + 4/3
# = 6 + 2/3 + 20/3 = 6 + 22/3 = 40/3.
# Wait.
# Standard GUT normalization: g' = sqrt(3/5) g1.
# Here we just compute the raw trace of our Y operator.
k1 = np.trace(Y_gen.conj().T @ Y_gen).real
print(f"  k1 (U1_Y) = {k1:.2f}")
# Expected 40/3 = 13.333?

# =============================================================================
# 4. WEINBERG ANGLE PREDICTION
# =============================================================================
# sin^2 theta_W = g'2 / (g2^2 + g'2)
# Or g1^2 / (g1^2 + g2^2)
# At unification, g_unif is single.
# g_phys * generator = const.
# g1_phys * Y = g_unif * T_unified.
# So g1_phys^2 * Tr(Y^2) = g_unif^2 * Tr(T_unif^2)
# g2_phys^2 * Tr(T2^2) = g_unif^2 * Tr(T_unif^2)
# => g1^2 k1 = g2^2 k2
# => g1/g2 = sqrt(k2/k1).
# sin^2 theta_W = 1 / (1 + (g2/g1)^2) = 1 / (1 + k1/k2)
# Standard SU(5): k1 = 5/3 k2 (with different Y norm).
# Let's calculate sin^2 theta_W directly from traces.

if k2 > 1e-5:
    ratio_sq = k1 / k2  # This is (g2/g1)^2? No.
    # g1^2 k1 = g2^2 k2 => (g2/g1)^2 = k1/k2.
    # sin2 = g1^2 / (g1^2 + g2^2) = 1 / (1 + g2^2/g1^2) = 1 / (1 + k1/k2).
    
    sin2_theta_W = 1.0 / (1.0 + (k1 / k2)) 
    print(f"\nPredicted Weinberg Angle at Unification:")
    print(f"  Theoretical sin^2(theta_W) = {sin2_theta_W:.4f}")
    
    # Standard SU(5) prediction is 3/8 = 0.375.
    # Let's see what Division Algebra predicts.
    # Using SM Y values (sum Y^2 = 40/3) and T3 values (sum T3^2 = 2):
    # k1/k2 = (40/3) / 2 = 20/3.
    # sin2 = 1 / (1 + 20/3) = 1 / (23/3) = 3/23 = 0.13 ?? 
    # This implies our Y scaling is different from SU(5) convention.
    # The SU(5) generator is sqrt(3/5) Y/2.
    # If we use Y/2 (as in Q = T3 + Y/2):
    # Then Y_gen_scaled = Y/2.
    # k1_scaled = k1 / 4 = 10/3.
    # Ratio = (10/3) / 2 = 5/3.
    # sin2 = 1 / (1 + 5/3) = 1 / (8/3) = 3/8 = 0.375.
    
    # We need to check if our derived Y is normalized correctly.
    # Based on Q = T3 + Y/2, the operator is Y_gen.
    # But usually T is generators. Y/2 is the generator corresponding to U(1).
    # Let's check T_hyper = Y_gen * 0.5.
    
    k1_gen = np.trace((0.5 * Y_gen).conj().T @ (0.5 * Y_gen)).real
    sin2_theta_W_gen = 1.0 / (1.0 + (k1_gen / k2))
    print(f"  Adjusted (using T=Y/2) sin^2(theta_W) = {sin2_theta_W_gen:.4f}")
    
else:
    print("  Error: k2 is zero.")

# =============================================================================
# 5. YUKAWA MASS TERMS
# =============================================================================
# Experimental Construction of Mass Term
# Mass ~ Psi_bar * Phi * Psi
# Psi is in S (32 real). Psi_bar is in S_bar (dual).
# We need a Lorentz Scalar.
# Dirac Mass: m (L_bar R + R_bar L).
# In our algebra, does there exist an element H (Higgs) such that
# Psi^dag G0 H Psi is non-zero and invariant under gauge group?

# We test the simplest scalar: H = 1 (Standard Mass).
# In SM, mass term breaks SU(2).
# L is doublet, R is singlet. L_bar R transforms as doublet.
# So H must be a doublet.
# Can we identify a doublet vector in the algebra?
# Quaternion units i, j, k or complex i?
# e1, e2, e3...
# This requires a deeper search. We will just output the prediction for now.

results = {
    "k1_Y": k1,
    "k2_SU2": k2,
    "k3_SU3": k3,
    "sin2_theta_W_raw": sin2_theta_W,
    "sin2_theta_W_adjusted": sin2_theta_W_gen,
    "match_SU5": bool(abs(sin2_theta_W_gen - 0.375) < 0.01)
}

with open("results/coupling_predictions.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"Artifact saved: results/coupling_predictions.json")
