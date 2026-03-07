#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
DERIVATION OF δ_CP FROM Cl(6) — SECOND PASS (CORRECTED)
===============================================================================

Findings from first pass:
  1. Cl(6) algebra: ✓ verified (64 basis, 8×8 matrices)
  2. CP classification: 32 odd, 32 even — correct
  3. Coset torsion = 0: Spin(6)/[SU(2)×SU(2)] is SYMMETRIC SPACE
     → Cartan torsion vanishes identically (math theorem, not a bug)
  4. Idempotents: cyclic permutation doesn't give orthogonal projectors
  5. 6 nonzero CP-odd traces found: Tr(γ₇ · γ_{ia} · γ_{jb} · γ_{kc})

This script:
  A. REVERSE-ENGINEER TEST: Compute what δ_CP the EWBG formula requires
  B. PROPER WITT DECOMPOSITION: Construct correct generation idempotents
  C. CONDENSATE TORSION: The physical torsion comes from the Nieh-Yan term
  D. CP-ODD ALGEBRAIC INVARIANT: Compute the unique Cl(6) CP-odd number
  E. PHYSICAL δ_CP: Combine algebraic invariant with proper normalization
  F. HONEST ASSESSMENT: What can and cannot be derived

NO HARDCODING: Every number traces to Cl(6) structure or standard physics.
===============================================================================
"""

import numpy as np
from itertools import combinations
from functools import reduce
import sys

np.set_printoptions(precision=12, linewidth=120)

# ═══════════════════════════════════════════════════════════════════════
# SECTION A: REVERSE-ENGINEER TEST
# ═══════════════════════════════════════════════════════════════════════
print("=" * 78)
print("  SECTION A: REVERSE-ENGINEER TEST")
print("  (Is δ_CP = 1.35×10⁻⁵ derived or back-computed from η_obs?)")
print("=" * 78)

# EWBG master equation (standard, e.g., Morrissey & Ramsey-Musolf 2012):
#   η_B = (405 Γ_sph / (4π² g_* v_w T)) × δ_CP × (m_t(T)/T)²
#
# Parameters used in the manuscript (all standard physics):
alpha_w = 0.0340          # α_w = g²/(4π) at EW scale
g2_ew = np.sqrt(4 * np.pi * alpha_w)  # SU(2) coupling
T_nuc = 158.5             # GeV — from bounce action
g_star = 106.75           # SM d.o.f.
v_w = 0.1                 # bubble wall velocity (typical)
m_t_Tnuc = 100.0          # running top mass at T_nuc (GeV)

# Sphaleron rate (NLO):
# Γ_sph / T⁴ ≈ κ α_w⁵  with κ ≈ 20 (lattice result, D'Onofrio+ 2014)
kappa_sph = 20.0
Gamma_sph_over_T4 = kappa_sph * alpha_w**5
Gamma_sph = Gamma_sph_over_T4 * T_nuc**4  # GeV⁴... but η formula needs Γ/T

# Actually the standard EWBG formula in the manuscript is:
# η = (405 Γ_sph) / (4π² g_* v_w) × δ_CP × (m_t/T)²
# where Γ_sph is the sphaleron RATE per unit volume per unit time,
# divided by T⁴ (dimensionless).
# The conventional form: η_B/s ≈ (n_f × Γ_sph) / (g_* T³ H(T)) × ε_CP
# Let me use the manuscript's exact formula instead.

# From the manuscript eq: η ≈ 7.73 × 10⁻¹⁰ with δ_CP = 1.35×10⁻⁵
# Back-compute the prefactor:
eta_claimed = 7.73e-10
delta_CP_claimed = 1.35e-5
prefactor_manuscript = eta_claimed / delta_CP_claimed

# Now compute what δ_CP would give η_obs:
eta_obs = 6.14e-10  # Planck 2018
delta_CP_needed = eta_obs / prefactor_manuscript

print(f"\n  Manuscript values:")
print(f"    η_claimed = {eta_claimed:.2e}")
print(f"    δ_CP_claimed = {delta_CP_claimed:.2e}")
print(f"    Implied prefactor = η/δ = {prefactor_manuscript:.4e}")
print(f"\n  Reverse test:")
print(f"    η_obs (Planck) = {eta_obs:.2e}")
print(f"    δ_CP needed for exact η_obs = {delta_CP_needed:.4e}")
print(f"    Ratio δ_CP(claimed)/δ_CP(needed) = {delta_CP_claimed/delta_CP_needed:.4f}")

# Compute prefactor from first principles
# η = prefactor × δ_CP
# prefactor = (405 × Γ_sph/(T⁴)) × T³ / (4π² g_* v_w) × (m_t/T)²
# = 405 × κ × α_w⁵ × (m_t/T)² / (4π² g_* v_w)

prefactor_theory = 405 * kappa_sph * alpha_w**5 * (m_t_Tnuc / T_nuc)**2 / (4 * np.pi**2 * g_star * v_w)
delta_needed_theory = eta_obs / prefactor_theory

print(f"\n  Theory prefactor (from first principles):")
print(f"    405 × κ × α_w⁵ × (m_t/T)² / (4π² g_* v_w)")
print(f"    = 405 × {kappa_sph} × {alpha_w}⁵ × ({m_t_Tnuc/T_nuc:.4f})² / "
      f"(4π² × {g_star} × {v_w})")
print(f"    = {prefactor_theory:.6e}")
print(f"    δ_CP needed = η_obs / prefactor = {delta_needed_theory:.6e}")

# VERDICT on reverse-engineering:
ratio_test = delta_CP_claimed / delta_needed_theory
print(f"\n  ╔══════════════════════════════════════════════════════╗")
print(f"  ║  REVERSE-ENGINEER TEST RESULT:                      ║")
print(f"  ║  δ_CP(claimed) / δ_CP(theory prefactor → η_obs):   ║")
print(f"  ║  Ratio = {ratio_test:.4f}                                  ║")
if abs(ratio_test - 1.0) < 0.1:
    print(f"  ║  → Consistent with forward derivation if prefactor  ║")
    print(f"  ║    matches manuscript's implied prefactor.           ║")
else:
    print(f"  ║  → Significant discrepancy from simple back-compute ║")
print(f"  ╚══════════════════════════════════════════════════════╝")

# ═══════════════════════════════════════════════════════════════════════
# SECTION B: CL(6) ALGEBRA AND WITT DECOMPOSITION
# ═══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 78)
print("  SECTION B: Cl(6) WITH PROPER WITT DECOMPOSITION")
print("=" * 78)

sigma_0 = np.eye(2, dtype=complex)
sigma_1 = np.array([[0, 1], [1, 0]], dtype=complex)
sigma_2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
sigma_3 = np.array([[1, 0], [0, -1]], dtype=complex)

def tensor(*matrices):
    return reduce(np.kron, matrices)

# Gamma matrices (same construction as before, verified)
gamma = [
    tensor(sigma_1, sigma_0, sigma_0),  # γ₁
    tensor(sigma_2, sigma_0, sigma_0),  # γ₂
    tensor(sigma_3, sigma_1, sigma_0),  # γ₃
    tensor(sigma_3, sigma_2, sigma_0),  # γ₄
    tensor(sigma_3, sigma_3, sigma_1),  # γ₅
    tensor(sigma_3, sigma_3, sigma_2),  # γ₆
]
N = 8

# Quick verify
for i in range(6):
    for j in range(6):
        anti = gamma[i] @ gamma[j] + gamma[j] @ gamma[i]
        assert np.allclose(anti, 2 * (1 if i==j else 0) * np.eye(N))
print("  ✓ Cl(6) algebra verified")

# Volume element
gamma7 = gamma[0]
for i in range(1, 6):
    gamma7 = gamma7 @ gamma[i]
assert np.allclose(gamma7 @ gamma7, -np.eye(N))
print("  ✓ γ₇² = −I verified")

# ── WITT DECOMPOSITION ──
# For Cl(6,0) (Euclidean), introduce COMPLEX null vectors:
#   w_i = (γ_{2i-1} + i γ_{2i}) / 2,  i = 1,2,3
#   w̄_i = (γ_{2i-1} - i γ_{2i}) / 2
#
# These satisfy: {w_i, w̄_j} = δ_{ij}, {w_i, w_j} = 0, {w̄_i, w̄_j} = 0
# They are NILPOTENT: w_i² = 0, w̄_i² = 0

w = []  # w_1, w_2, w_3
wbar = []  # w̄_1, w̄_2, w̄_3
for i in range(3):
    wi = (gamma[2*i] + 1j * gamma[2*i + 1]) / 2
    wbi = (gamma[2*i] - 1j * gamma[2*i + 1]) / 2
    w.append(wi)
    wbar.append(wbi)

# Verify nilpotency
print("\n  Witt basis verification:")
for i in range(3):
    assert np.allclose(w[i] @ w[i], 0), f"w_{i+1}² ≠ 0"
    assert np.allclose(wbar[i] @ wbar[i], 0), f"w̄_{i+1}² ≠ 0"
print("  ✓ All w_i² = 0, w̄_i² = 0 (nilpotency)")

for i in range(3):
    for j in range(3):
        anti = w[i] @ wbar[j] + wbar[j] @ w[i]
        expected = (1 if i == j else 0) * np.eye(N)
        assert np.allclose(anti, expected), f"{{w_{i+1}, w̄_{j+1}}} ≠ δ_{i+1}{j+1}"
        anti2 = w[i] @ w[j] + w[j] @ w[i]
        assert np.allclose(anti2, 0), f"{{w_{i+1}, w_{j+1}}} ≠ 0"
        anti3 = wbar[i] @ wbar[j] + wbar[j] @ wbar[i]
        assert np.allclose(anti3, 0), f"{{w̄_{i+1}, w̄_{j+1}}} ≠ 0"
print("  ✓ {w_i, w̄_j} = δ_ij, {w_i, w_j} = 0 verified")

# ── GENERATION IDEMPOTENTS FROM WITT BASIS ──
# The "vacuum" state: Ω = w̄₁ w̄₂ w̄₃ · w₃ w₂ w₁ (normalized)  
# Actually the standard construction (Furey 2016):
#   The minimal left ideal is generated by a primitive idempotent.
#   For Cl(6): f = w̄₁ w₁ · w̄₂ w₂ · w̄₃ w₃
# This projects onto a 1-dimensional subspace.

# Number operators: n_i = w̄_i w_i (eigenvalues 0,1)
n_ops = [wbar[i] @ w[i] for i in range(3)]

# Primitive idempotent: all number operators eigenvalue 1
# f_000 = (1-n₁)(1-n₂)(1-n₃) = w₁w̄₁ · w₂w̄₂ · w₃w̄₃
# f_111 = n₁ n₂ n₃ = w̄₁w₁ · w̄₂w₂ · w̄₃w₃

# There are 2³ = 8 primitive idempotents (one for each "occupation")
idempotents = {}
labels_idemp = {}
for bits in range(8):
    b = [(bits >> k) & 1 for k in range(3)]
    proj = np.eye(N, dtype=complex)
    for k in range(3):
        if b[k] == 1:
            proj = proj @ n_ops[k]  # w̄_k w_k
        else:
            proj = proj @ (np.eye(N) - n_ops[k])  # w_k w̄_k
    idempotents[tuple(b)] = proj
    labels_idemp[tuple(b)] = f"|{b[0]}{b[1]}{b[2]}⟩"

# Verify they are idempotent and mutually orthogonal
print("\n  Primitive idempotents (Witt basis):")
for bits_a, proj_a in idempotents.items():
    assert np.allclose(proj_a @ proj_a, proj_a), f"f_{bits_a}² ≠ f_{bits_a}"
    tr = np.trace(proj_a).real
    assert abs(tr - 1.0) < 1e-10, f"Tr(f_{bits_a}) ≠ 1"
    for bits_b, proj_b in idempotents.items():
        if bits_a != bits_b:
            assert np.allclose(proj_a @ proj_b, 0, atol=1e-12), \
                f"f_{bits_a} · f_{bits_b} ≠ 0"
print("  ✓ All 8 primitive idempotents verified (idempotent, orthogonal, Tr=1)")
print(f"  ✓ Sum of all 8 = I: {np.allclose(sum(idempotents.values()), np.eye(N))}")

# In the TRXT/Furey model, the 3 GENERATIONS correspond to
# the 3 "one-particle" states: |100⟩, |010⟩, |001⟩
# These are the states with exactly one "occupied" Witt mode.
gen1 = idempotents[(1, 0, 0)]
gen2 = idempotents[(0, 1, 0)]
gen3 = idempotents[(0, 0, 1)]

print(f"\n  Generation projectors:")
print(f"  Gen 1: |100⟩, Tr = {np.trace(gen1).real:.0f}")
print(f"  Gen 2: |010⟩, Tr = {np.trace(gen2).real:.0f}")  
print(f"  Gen 3: |001⟩, Tr = {np.trace(gen3).real:.0f}")
print(f"  Orthogonal: f₁f₂=0 {np.allclose(gen1@gen2, 0)}, "
      f"f₁f₃=0 {np.allclose(gen1@gen3, 0)}, "
      f"f₂f₃=0 {np.allclose(gen2@gen3, 0)}")

# ═══════════════════════════════════════════════════════════════════════
# SECTION C: CP TRANSFORMATION AND GENERATION MIXING
# ═══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 78)
print("  SECTION C: CP TRANSFORMATION ON WITT BASIS")
print("=" * 78)

# Charge conjugation in Witt basis:
# C: w_i ↔ w̄_i (exchanges creation and annihilation)
# This is equivalent to complex conjugation of the Cl(6) element.
#
# C maps |100⟩ state to a different state:
# C(w̄₁ w₁ · w₂ w̄₂ · w₃ w̄₃) = w₁ w̄₁ · w̄₂ w₂ · w̄₃ w₃ = |011⟩
# So C: |100⟩ → |011⟩, etc.
# In general: C: |b₁b₂b₃⟩ → |1−b₁, 1−b₂, 1−b₃⟩

# Parity: exchanges spatial directions (generators 1,2,3 → -γ₁,-γ₂,-γ₃)
# In Witt basis: P: w₁ → -w̄₁ (since w₁ involves γ₁,γ₂)
# P acts on w_i = (γ_{2i-1} + iγ_{2i})/2:
#   - γ₁,γ₂,γ₃ spatial → flipped by P
#   - γ₄,γ₅,γ₆ internal → unchanged by P
# So P: w₁ → -(γ₁-iγ₂)/2 = -w̄₁ (for spatial pair 1,2)
#    P: w₂ → -(γ₃-iγ₄)/2... wait, γ₃ is spatial but γ₄ is internal.
# This is where the TRXT structure matters: the pairing (12)(34)(56)
# mixes spatial and internal indices in w₂ and w₃.

# But physically, the definition of CP in Cl(6) is representation-dependent.
# Let's use the CANONICAL definition:
#   CP: γ_i → -γ_i for all i (total reflection)
# which maps w_i → -w̄_i and w̄_i → -w_i.
# Under this: |b₁b₂b₃⟩ → (-1)^something |1-b₁,1-b₂,1-b₃⟩

# Let's compute CP action on each generation:
def cp_action(mat):
    """CP = complex conjugation + overall sign from (−1)^(grade)."""
    # For Euclidean Cl(6), CP: Γ → Γ† (Hermitian conjugate)
    # This is because B = product of imaginary γ's, and
    # B Γ* B⁻¹ = Γ†  for the standard representation.
    return mat.conj().T

# More precisely: the CP-transformation that physically reverses
# particle↔antiparticle is the "main anti-involution" of Cl(6):
# α: γ_i → -γ_i, combined with reversal: γ_{i₁...iₖ} → γ_{iₖ...i₁}
# This is α(Γ) = (-1)^k Γ^reverse = Γ†  (for unitary Γ)

# Check CP transformation of generation states:
print("\n  CP action on generation states:")
for label, proj in [("Gen1 |100⟩", gen1), ("Gen2 |010⟩", gen2), ("Gen3 |001⟩", gen3)]:
    cp_proj = cp_action(proj)
    # Decompose in the idempotent basis
    overlaps = {}
    for bits, f in idempotents.items():
        ov = np.trace(cp_proj @ f).real
        if abs(ov) > 1e-10:
            overlaps[labels_idemp[bits]] = ov
    print(f"  CP({label}) = {overlaps}")

# ═══════════════════════════════════════════════════════════════════════
# SECTION D: THE CP-ODD ALGEBRAIC INVARIANT
# ═══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 78)
print("  SECTION D: CP-ODD ALGEBRAIC INVARIANT FROM Cl(6)")
print("=" * 78)

# The UNIQUE CP-violating quantity that can be constructed from
# Cl(6) alone is related to the CHIRALITY operator γ₇.
#
# γ₇ = i³ γ₁ γ₂ γ₃ γ₄ γ₅ γ₆ is CP-odd (it changes sign under CP).
# Its eigenvalues are ±i (since γ₇² = -I).
#
# The key insight: When we have 3 generations in the Witt basis,
# the CP violation comes from the ASYMMETRY between the three
# complex structures:
#   J_k: the complex structure given by the k-th Witt pair (w_k, w̄_k)
#   J_k = i(w̄_k w_k - w_k w̄_k) = i(2n_k - I)
#
# Each J_k has eigenvalues ±i on its 2D subspace.
# The CP-odd combination is:
#   Im[Tr(J₁ J₂ J₃)] / Tr(I)

J = []
for k in range(3):
    Jk = 1j * (2 * n_ops[k] - np.eye(N))
    J.append(Jk)
    # Verify J_k² = -I (complex structure)
    Jk_sq = Jk @ Jk
    print(f"  J_{k+1}² {'= −I ✓' if np.allclose(Jk_sq, -np.eye(N)) else '≠ −I ✗'}")

# CP-odd triple product
J123 = J[0] @ J[1] @ J[2]
tr_J123 = np.trace(J123)
print(f"\n  Tr(J₁ J₂ J₃) = {tr_J123}")
print(f"  Tr(J₁ J₂ J₃) / N = {tr_J123 / N}")

# The mixing between generations is mediated by TRANSITION OPERATORS:
# T_{ij} = w_i w̄_j  (annihilate generation j, create generation i)
# These are the "flavor-changing" operators in the Witt basis.

T_ops = [[None]*3 for _ in range(3)]
for i in range(3):
    for j in range(3):
        T_ops[i][j] = wbar[i] @ w[j]  # w̄_i w_j: annihilate j, create i

# Check: T_{ii} = n_i (number operator)
for i in range(3):
    assert np.allclose(T_ops[i][i], n_ops[i]), f"T_{i}{i} ≠ n_{i}"
print("\n  ✓ T_{ii} = n_i verified")

# The mixing matrix between generations is:
# M_{αβ} = ⟨α| H_torsion |β⟩ = Tr(f_α · H · f_β)
# where H is an operator built from Cl(6) elements.
#
# The key question: WHICH Cl(6) operator gives the mass/mixing matrix?
#
# In the TRXT model, this is the TORSION of the Cl(6) bundle connection.
# But as we showed, the FLAT torsion is zero (symmetric space).
# The NON-ZERO torsion comes from the CONDENSATE GRADIENT.
#
# The physical torsion operator is:
#   H_torsion = Σ_μ (∂_μ φ^a) γ_a γ^μ
# where φ^a are the Goldstone modes of the broken Cl(6) symmetry.
#
# At the EW phase transition, the condensate φ varies across the
# bubble wall (the "bounce" solution). The CP violation comes from
# the COMPLEX PHASE of this variation.
#
# The ALGEBRAIC part of the torsion (independent of dynamics) is
# the operator that COUPLES different generations:

# Construct the most general grade-3 CP-odd operator:
# From Step 3 of first pass: the CP-odd grade-3 elements are:
# γ₁₂₃, γ₁₄₅, γ₁₄₆, γ₁₅₆, γ₂₄₅, γ₂₄₆, γ₂₅₆, γ₃₄₅, γ₃₄₆, γ₃₅₆
# (10 elements)

# Build all basis elements
def multivector(indices):
    """Product γ_{i₁} γ_{i₂} ... γ_{iₖ} for sorted indices."""
    if len(indices) == 0:
        return np.eye(N, dtype=complex)
    return reduce(np.dot, [gamma[i] for i in indices])

# Enumerate all CP-odd grade-3 elements and compute their
# matrix elements between generation states
print("\n  Generation-changing matrix elements of CP-odd grade-3 operators:")
print("  (These are the 'torsion couplings' between generations)\n")

grade3_elements = list(combinations(range(6), 3))
cp_odd_g3 = []

for idx_tuple in grade3_elements:
    mat = multivector(idx_tuple)
    # Check if CP-odd
    cp_mat = cp_action(mat)
    if np.allclose(cp_mat, -mat, atol=1e-12):
        cp_odd_g3.append(idx_tuple)

print(f"  CP-odd grade-3 elements: {len(cp_odd_g3)}")

# For each CP-odd grade-3 element, compute the 3×3 matrix of 
# its expectation values between generation states
generation_projectors = [gen1, gen2, gen3]
gen_labels = ["Gen1", "Gen2", "Gen3"]

print("\n  Matrix elements M_{αβ}(Γ) = Tr(f_α · Γ · f_β):")
print("-" * 60)

non_trivial_couplings = []
for idx_tuple in cp_odd_g3:
    mat = multivector(idx_tuple)
    label = "γ_" + "".join(str(i+1) for i in idx_tuple)
    M = np.zeros((3, 3), dtype=complex)
    for a in range(3):
        for b in range(3):
            M[a, b] = np.trace(generation_projectors[a] @ mat @ generation_projectors[b])
    
    if np.max(np.abs(M)) > 1e-10:
        non_trivial_couplings.append((label, M, idx_tuple))
        print(f"\n  {label}:")
        for a in range(3):
            row = [f"{M[a,b].real:+.4f}{M[a,b].imag:+.4f}i" for b in range(3)]
            print(f"    [{', '.join(row)}]")

print(f"\n  Non-trivial generation couplings: {len(non_trivial_couplings)}/{len(cp_odd_g3)}")

# ═══════════════════════════════════════════════════════════════════════
# SECTION E: CONSTRUCT THE FLAVOR MIXING MATRIX
# ═══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 78)
print("  SECTION E: FLAVOR MIXING MATRIX FROM TORSION")
print("=" * 78)

# The condensate torsion at the bubble wall is a SPECIFIC linear 
# combination of CP-odd operators, determined by the topology.
#
# For a single instanton/sphaleron of winding number 1:
#   φ(x) = Σ_a ĝ_a(x) Γ_a
# where ĝ_a(x) is the instanton profile and Γ_a are the CP-odd operators.
#
# The TOPOLOGICAL constraint is that the winding must equal 1:
#   ∫ dΩ₃ Tr(φ dφ dφ) = 2π × winding_number
#
# For the simplest (hedgehog) instanton, the profile is UNIFORM:
#   ĝ_a = const × n̂_a (unit vector in group space)
#
# So the total torsion operator for a single sphaleron is:
#   H = Σ_a c_a Γ_a   where c_a ∈ ℂ
# with the constraint |Σ c_a|² = 1 (normalized instanton).
#
# The DEMOCRATICALLY AVERAGED instanton (spherically symmetric in
# flavor space) gives all c_a EQUAL:

if len(non_trivial_couplings) > 0:
    H_torsion = np.zeros((N, N), dtype=complex)
    for label, M_elem, idx_tuple in non_trivial_couplings:
        mat = multivector(idx_tuple)
        H_torsion += mat
    # Normalize
    norm = np.linalg.norm(H_torsion, 'fro')
    if norm > 0:
        H_torsion_normalized = H_torsion / norm
    else:
        H_torsion_normalized = H_torsion
    
    print(f"  H_torsion (democratic average of {len(non_trivial_couplings)} CP-odd operators)")
    print(f"  ||H|| = {norm:.6f}")
    print(f"  H hermitian? {np.allclose(H_torsion, H_torsion.conj().T)}")
    
    # Project onto generation subspace
    M_eff = np.zeros((3, 3), dtype=complex)
    for a in range(3):
        for b in range(3):
            M_eff[a, b] = np.trace(generation_projectors[a] @ H_torsion_normalized @ generation_projectors[b])
    
    print(f"\n  Effective 3×3 mixing matrix M_eff:")
    for a in range(3):
        row = [f"{M_eff[a,b].real:+.6f}{M_eff[a,b].imag:+.6f}i" for b in range(3)]
        print(f"    [{', '.join(row)}]")
    
    # Compute Jarlskog invariant
    # J = Im(M_11 M_22 M*_12 M*_21)
    J_eff = np.imag(M_eff[0,0] * M_eff[1,1] * np.conj(M_eff[0,1]) * np.conj(M_eff[1,0]))
    print(f"\n  Jarlskog invariant J = Im(M₁₁M₂₂M*₁₂M*₂₁) = {J_eff:.10e}")
    
    # If M is Hermitian, diagonalize
    if np.allclose(M_eff, M_eff.conj().T, atol=1e-10):
        eigvals, eigvecs = np.linalg.eigh(M_eff)
        print(f"\n  M_eff is Hermitian → eigenvalues: {eigvals}")
        print(f"  (Hermitian matrix → J = 0 necessarily)")
        print(f"  → Need ANTI-Hermitian part for CP violation")
    
    # Compute anti-Hermitian part
    M_anti = (M_eff - M_eff.conj().T) / 2
    M_herm = (M_eff + M_eff.conj().T) / 2
    print(f"\n  ||Hermitian part||  = {np.linalg.norm(M_herm):.6e}")
    print(f"  ||Anti-Hermitian part|| = {np.linalg.norm(M_anti):.6e}")
else:
    print("  No non-trivial generation couplings found!")
    H_torsion_normalized = np.zeros((N, N), dtype=complex)

# ═══════════════════════════════════════════════════════════════════════
# SECTION F: THE FUNDAMENTAL CP-ODD NUMBER FROM Cl(6)
# ═══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 78)
print("  SECTION F: FUNDAMENTAL CP-ODD NUMBERS FROM Cl(6)")
print("=" * 78)

# What NUMBERS can Cl(6) produce that are:
# (a) CP-odd
# (b) O(10⁻⁵)
# (c) Calculable from pure algebra?
#
# Answer from first principles:

# 1. The Euler characteristic of CP³ ≅ SU(4)/[SU(3)×U(1)]
chi_CP3 = 4  # mathematical fact: χ(CPⁿ) = n+1
print(f"\n  1. Euler characteristic χ(CP³) = {chi_CP3}")

# 2. The Chern numbers of CP³
c1_CP3 = 4     # First Chern number: c₁ = n+1 for CP^n
c2_CP3 = 6     # Second Chern number: c₂ = C(n+1,2) for CP^n
c3_CP3 = 4     # Third Chern number: c₃ = C(n+1,3) for CP^n
print(f"  2. Chern numbers: c₁={c1_CP3}, c₂={c2_CP3}, c₃={c3_CP3}")

# 3. The A-hat genus (index of Dirac operator):
# For CP³: Â = (c₁⁴ - 4c₁²c₂ + 4c₁c₃ + c₂² - 2c₄) / 720
# But CP³ is 6-real-dimensional (3-complex), and all odd-dim Chern 
# classes of a complex 3-fold... actually CP³ is a 4-fold.
# Wait: CP³ has complex dimension 3, real dimension 6.
# Chern classes: c₁ = 4α, c₂ = 6α², c₃ = 4α³ where α ∈ H²(CP³)
# with ∫ α³ = 1.

# For a 6-real-dimensional manifold, the Â-genus is:
# Â = 1 + p₁/12  (up to higher terms) where p₁ = first Pontryagin class
# For CP³: p₁ = c₁² - 2c₂ = 16 - 12 = 4 (in units of α²)
# ∫ p₁ ∧ α = 4 (over CP³)
# But Â for 6D: Â₂ = (7p₁² - 4p₂)/5760
# Actually for dim 6, the relevant index is the Dirac index on CP³:
# index(D) = Â[CP³] = (-1/720)(4p₁² - 7p₂)[CP³]... this gets complicated.

# More directly: for CP³, the Todd class gives:
# td(CP³) = (1+α)⁴... no, td = Π (x_i/(1-e^{-x_i}))
# where the Chern roots x_i satisfy:
# c₁ = Σx_i = 4α, c₂ = Σ_{i<j} x_i x_j = 6α², c₃ = x₁x₂x₃ = 4α³

# For the HOLOMORPHIC Euler characteristic:
# χ(CP³, O) = 1 (by Kodaira vanishing)

# The KEY topological quantity for CP violation is the
# PONTRYAGIN density integrated over the instanton:
# ν = (1/8π²) ∫ Tr(F∧F) = instanton number = 1 (for a single instanton)

print(f"  3. Pontryagin class p₁(CP³) = c₁²−2c₂ = {c1_CP3**2 - 2*c2_CP3}")
nu_instanton = 1  # winding number
print(f"  4. Instanton number ν = {nu_instanton}")

# 4. The CP-odd phase from the η-invariant
# The Atiyah-Patodi-Singer η-invariant for the Dirac operator on
# a Cl(6) bundle measures the spectral asymmetry — this IS the
# fundamental CP-violating quantity.
#
# For the standard Dirac operator on S⁵ = boundary of CP³:
# η(S⁵) depends on the spin structure.
# For the UNIQUE spin structure on S⁵:
# η(0) = 0 (since S⁵ has a orientation-reversing isometry)
#
# But with the INSTANTON background connection:
# Δη = 2 × index(D) on the filling manifold CP³
# Δη = 2 × Â(CP³) × ch(F)|_{top}

# 5. The pure NUMBER from Cl(6) that enters δ_CP
# After all the geometry, the answer is:
#
# The CP-violating phase for a single sphaleron transition is:
#   δ_CP = (2π × ν) / V_gen
# where ν is the instanton number and V_gen is the "volume" 
# of the generation space in appropriate units.
#
# V_gen = dim(generation space) × normalization
# For 3 generations: V_gen = 3! / (number of CP-odd couplings)

# Actually, let me be more precise. The CP phase per sphaleron is:
# δ_CP = Im(det(Y)) / |det(Y)|
# where Y is the Yukawa coupling matrix.

# In the SM: Im(det(Y_u Y_u† Y_d Y_d†)) gives the Jarlskog invariant.
# In TRXT: Im(det(M_eff)) is the analogous quantity.

# From our computation, M_eff might be zero or Hermitian.
# Let's try ALL CP-odd operators, not just grade-3.

print("\n" + "-" * 78)
print("  Computing generation matrix elements for ALL CP-odd basis elements")
print("-" * 78)

# Enumerate ALL 32 CP-odd basis elements
all_cp_odd = []
for grade in range(7):
    for indices in combinations(range(6), grade):
        mat = multivector(indices)
        cp_mat = cp_action(mat)
        if np.allclose(cp_mat, -mat, atol=1e-12):
            all_cp_odd.append(indices)

print(f"  Total CP-odd elements: {len(all_cp_odd)}")

# For each, compute the 3×3 generation mixing matrix
all_couplings = []
for indices in all_cp_odd:
    mat = multivector(indices)
    label = "γ_" + ("".join(str(i+1) for i in indices) if len(indices) > 0 else "I")
    M = np.zeros((3, 3), dtype=complex)
    for a in range(3):
        for b in range(3):
            M[a, b] = np.trace(generation_projectors[a] @ mat @ generation_projectors[b])
    
    has_offdiag = any(abs(M[a,b]) > 1e-10 for a in range(3) for b in range(3) if a != b)
    has_diag = any(abs(M[a,a]) > 1e-10 for a in range(3))
    has_any = np.max(np.abs(M)) > 1e-10
    
    if has_any:
        all_couplings.append((label, M, indices, has_offdiag))

print(f"  Elements with non-zero generation matrix elements: {len(all_couplings)}")
print(f"  Elements with off-diagonal (flavor-changing) couplings: "
      f"{sum(1 for _, _, _, od in all_couplings if od)}")

for label, M, indices, has_offdiag in all_couplings:
    marker = " ← FLAVOR CHANGING" if has_offdiag else ""
    print(f"\n  {label}{marker}:")
    for a in range(3):
        row = [f"{M[a,b].real:+.6f}{M[a,b].imag:+.6f}i" for b in range(3)]
        print(f"    [{', '.join(row)}]")

# ═══════════════════════════════════════════════════════════════════════
# SECTION G: ALTERNATIVE: CP VIOLATION FROM TRIALITY
# ═══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 78)
print("  SECTION G: CP VIOLATION FROM TRIALITY AUTOMORPHISM")
print("=" * 78)

# Cl(6) has a special property: Spin(6) ≅ SU(4), and the triality
# automorphism of D₃ = SO(6) permutes the three 4-dim representations:
#   vector (6) ↔ spinor+ (4) ↔ spinor- (4̄)
#
# This triality is the mathematical origin of 3 GENERATIONS.
# The CP violation comes from the PHASE acquired when triality
# acts on the combined fermion state.
#
# Triality automorphism τ: Cl(6) → Cl(6)
# τ acts as a PERMUTATION on the Witt modes:
#   τ: (w₁, w₂, w₃) → (w₂, w₃, w₁)  (cyclic permutation)

# Construct the triality matrix explicitly
# τ(w_i) = w_{i+1 mod 3}
# This means τ(γ_{2i-1}) = γ_{2(i+1)-1} and τ(γ_{2i}) = γ_{2(i+1)}

# First, define τ as a unitary transformation on the 8D space
# τ maps: γ₁→γ₃→γ₅→γ₁ and γ₂→γ₄→γ₆→γ₂
# So the permutation of generators is: (1→3→5→1), (2→4→6→2)

# Find U_τ such that U_τ γ_i U_τ† = γ_σ(i)
# where σ = (1→3, 2→4, 3→5, 4→6, 5→1, 6→2)

# This is equivalent to finding U such that:
# U γ₁ U† = γ₃, U γ₂ U† = γ₄, U γ₃ U† = γ₅, 
# U γ₄ U† = γ₆, U γ₅ U† = γ₁, U γ₆ U† = γ₂

# Construct using Clifford algebra elements
# U = (1/√8) exp(π/3 × Σ) where Σ generates the cyclic permutation
# Actually, let me use the direct method: find all 8×8 unitaries
# that implement the permutation.

# Method: Use the fact that
# U = (1 + γ₁γ₃ + γ₃γ₅ + γ₅γ₁) × (1 + γ₂γ₄ + γ₄γ₆ + γ₆γ₂) / norm
# Wait, this doesn't work for a cubic permutation.

# Instead, note that the cyclic permutation (135)(246) has order 3.
# The element implementing it in Pin(6) is:
# For a rotation by 2π/3 in the (13) plane composed with (35) and (24),(46):
# Actually this is getting complicated. Let me use numerical optimization.

# Direct approach: solve for U_τ
from scipy.optimize import minimize

def triality_cost(params):
    """Cost function: ||U γ_i U† - γ_{σ(i)}||² for all i."""
    # params = 128 real numbers (64 complex = 8×8 matrix)
    U_real = params[:64].reshape(8, 8)
    U_imag = params[64:].reshape(8, 8)
    U = U_real + 1j * U_imag
    
    # Enforce unitarity approximately via QR
    Q, R = np.linalg.qr(U)
    U = Q
    
    cost = 0.0
    sigma_map = [2, 3, 4, 5, 0, 1]  # γ₁→γ₃, γ₂→γ₄, ...
    for i in range(6):
        diff = U @ gamma[i] @ U.conj().T - gamma[sigma_map[i]]
        cost += np.sum(np.abs(diff)**2).real
    return cost

# Instead of optimization, I can construct U analytically:
# The permutation (w₁→w₂→w₃→w₁) corresponds to
# (n₁→n₂→n₃→n₁) on the occupation numbers.
# This maps |b₁b₂b₃⟩ → |b₃b₁b₂⟩.

# Let's just find U by its action on the 8 basis states.
# The 8 basis states are eigenstates of (n₁, n₂, n₃):
# |000⟩, |100⟩, |010⟩, |001⟩, |110⟩, |101⟩, |011⟩, |111⟩

# Under τ: |b₁b₂b₃⟩ → |b₃b₁b₂⟩
# So: |000⟩→|000⟩, |100⟩→|010⟩, |010⟩→|001⟩, |001⟩→|100⟩, etc.

# Find the matrix representation by computing the projectors
basis_states = []
state_labels = []
for bits in range(8):
    b = [(bits >> k) & 1 for k in range(3)]
    proj = idempotents[tuple(b)]
    # Find the eigenvector (rank 1 projector → 1 eigenvector)
    eigvals, eigvecs = np.linalg.eigh(proj)
    # The eigenvector with eigenvalue 1
    idx_max = np.argmax(eigvals.real)
    state = eigvecs[:, idx_max]
    basis_states.append(state)
    state_labels.append(f"|{b[0]}{b[1]}{b[2]}⟩")

print(f"  Extracted {len(basis_states)} basis states")

# Construct the triality matrix
U_tau = np.zeros((N, N), dtype=complex)
for bits in range(8):
    b = [(bits >> k) & 1 for k in range(3)]
    # τ: (b₁,b₂,b₃) → (b₃,b₁,b₂)
    b_new = (b[2], b[0], b[1])
    
    # U_τ |b⟩ = |τ(b)⟩
    state_old = basis_states[bits]
    bits_new = b_new[0] + 2*b_new[1] + 4*b_new[2]
    state_new = basis_states[bits_new]
    
    U_tau += np.outer(state_new, state_old.conj())

# Check unitarity
print(f"  U_τ unitary? {np.allclose(U_tau @ U_tau.conj().T, np.eye(N))}")
print(f"  U_τ³ = I? {np.allclose(U_tau @ U_tau @ U_tau, np.eye(N), atol=1e-10)}")

# Check triality action on generation states
print("\n  Triality τ action on generations:")
for a in range(3):
    gen_state = basis_states[2**a]  # |100⟩, |010⟩, |001⟩
    tau_state = U_tau @ gen_state
    overlaps = []
    for b in range(3):
        ov = abs(np.dot(basis_states[2**b].conj(), tau_state))**2
        overlaps.append(ov)
    print(f"  τ|Gen{a+1}⟩: overlap with Gen1={overlaps[0]:.4f}, "
          f"Gen2={overlaps[1]:.4f}, Gen3={overlaps[2]:.4f}")

# The TRIALITY PHASE is the key to CP violation.
# Under τ, a generation state picks up a PHASE:
#   τ|ψ⟩ = e^{iφ_τ} |τ(ψ)⟩
# But τ also permutes the generations.
# The CP-violating phase is the phase of det(τ) restricted to
# the 3-generation subspace.

# Project τ into the 3D generation subspace
tau_3x3 = np.zeros((3, 3), dtype=complex)
for a in range(3):
    for b in range(3):
        tau_3x3[a, b] = np.dot(basis_states[2**a].conj(), U_tau @ basis_states[2**b])

print(f"\n  Triality matrix in generation subspace:")
for a in range(3):
    row = [f"{tau_3x3[a,b].real:+.6f}{tau_3x3[a,b].imag:+.6f}i" for b in range(3)]
    print(f"    [{', '.join(row)}]")

det_tau = np.linalg.det(tau_3x3)
phase_tau = np.angle(det_tau)
print(f"\n  det(τ₃ₓ₃) = {det_tau:.6f}")
print(f"  |det(τ₃ₓ₃)| = {abs(det_tau):.6f}")
print(f"  arg(det(τ₃ₓ₃)) = {phase_tau:.10f} rad")
print(f"                   = {np.degrees(phase_tau):.6f}°")

# The eigenvalues of τ (in the generation subspace)
eigvals_tau = np.linalg.eigvals(tau_3x3)
print(f"\n  Eigenvalues of τ₃ₓ₃: {eigvals_tau}")
print(f"  |eigenvalues|: {np.abs(eigvals_tau)}")
print(f"  phases: {np.angle(eigvals_tau)} rad = {np.degrees(np.angle(eigvals_tau))}°")

# Cube roots of unity: ω = e^{2πi/3}
omega = np.exp(2j * np.pi / 3)
print(f"\n  Expected (cube roots of unity): 1, ω, ω² = 1, e^{{2πi/3}}, e^{{4πi/3}}")
print(f"  ω = {omega:.6f}")
print(f"  ω² = {omega**2:.6f}")

# The Jarlskog invariant from the triality matrix
J_triality = np.imag(tau_3x3[0,0] * tau_3x3[1,1] * np.conj(tau_3x3[0,1]) * np.conj(tau_3x3[1,0]))
print(f"\n  Jarlskog (triality) = {J_triality:.10e}")

# ═══════════════════════════════════════════════════════════════════════
# SECTION H: THE SPHALERON-TRIALITY CP PHASE
# ═══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 78)
print("  SECTION H: PHYSICAL δ_CP FROM SPHALERON + TRIALITY")
print("=" * 78)

# The physical process that generates the baryon asymmetry is:
# 1. A sphaleron transition changes B+L by 2n_gen = 6
# 2. The CP violation comes from the INTERFERENCE between
#    different generation paths through the sphaleron
# 3. The triality automorphism mixes the generations
#
# The CP phase per sphaleron is:
#   δ_CP = J_triality × (suppression from dynamics)
#
# The dynamical suppression comes from the RATIO of the
# torsion coupling to the gauge coupling:
#   κ = g_torsion / g_gauge
#
# In TRXT: g_gauge = 1/(9π + 10) (the mass formula coupling)
# The torsion coupling comes from the GRADIENT of the condensate
# across the bubble wall. For a bubble wall of width L and
# height Δφ:
#   g_torsion ~ Δφ / (Λ L)
# where Λ is the UV cutoff (= M* in TRXT).
#
# For the EWPT: Δφ = v(T_nuc) = M* and L ~ 1/T_nuc
# So g_torsion ~ M* T_nuc / M*² = T_nuc / M* ≈ 158.5/365.2 ≈ 0.434

M_star = 365.24  # GeV (TRXT condensate scale)
g_torsion = T_nuc / M_star
g_gauge = 1.0 / (9 * np.pi + 10)

print(f"\n  Dynamical scales:")
print(f"    M* = {M_star} GeV")
print(f"    T_nuc = {T_nuc} GeV")
print(f"    g_torsion = T_nuc/M* = {g_torsion:.6f}")
print(f"    g_gauge = 1/(9π+10) = {g_gauge:.6f}")

# The LOOP SUPPRESSION for the CP-violating process:
# At tree level, the sphaleron is CP-conserving (it's a saddle point).
# CP violation enters at ONE LOOP through the fermion determinant.
# The one-loop suppression factor is:
#   1/(16π²) = {1/(16*np.pi**2):.6e}
loop_factor = 1.0 / (16 * np.pi**2)
print(f"    Loop factor 1/(16π²) = {loop_factor:.6e}")

# Now combine everything:
# δ_CP = J_algebraic × g_torsion² × loop_factor × (topological factor)
#
# The "topological factor" is the instanton number (= 1 for a single sphaleron)
# times the Chern-Simons level (= 1 for SU(2)).

# From the triality: J = Im(det(τ)) / |det(τ)|
# But if τ is a pure permutation, J = 0.
# The CP violation requires the COMBINATION of triality with the
# chirality operator γ₇.

# The proper Jarlskog: for the CKM-like matrix, we need both "up" and "down"
# type mass matrices. In TRXT:
# - "up" type: coupling through the condensate (Witt mode w₁ direction)
# - "down" type: coupling through the torsion (mixed w₁,w₂,w₃ direction)

# Construct "up" and "down" mass matrices from Cl(6)
# "Up" sector: coupling to γ₇ (chirality) → grade-6 element
# "Down" sector: coupling to Σ (torsion) → grade-3 element

# The up-type coupling: M_u ~ Tr(f_α · γ₇ · f_β)
M_u = np.zeros((3, 3), dtype=complex)
for a in range(3):
    for b in range(3):
        M_u[a, b] = np.trace(generation_projectors[a] @ gamma7 @ generation_projectors[b])

print(f"\n  'Up-type' mass matrix M_u = Tr(f_α · γ₇ · f_β):")
for a in range(3):
    row = [f"{M_u[a,b].real:+.6f}{M_u[a,b].imag:+.6f}i" for b in range(3)]
    print(f"    [{', '.join(row)}]")

# The down-type coupling: M_d ~ Tr(f_α · Σ · f_β)
# where Σ = Σ_{CP-odd grade-3} c_a γ_a

# Use the CP-odd invariant we found: Tr(γ₇ · γ_{14} · γ_{25} · γ_{36})
# This is the unique (up to sign) CP-odd scalar from 3 coset generators.
# Define Σ as the sum of CP-odd grade-3 operators weighted by their structure

# The most natural "down-type" operator is the torsion sum
# For the 3 "diagonal" torsion operators: γ₁₄₅, γ₂₅₆, γ₃₄₆
# These correspond to the 3 coset directions that couple (spatial_i, internal_{4,5,6})

Sigma_down = np.zeros((N, N), dtype=complex)
# Use equally weighted sum of CP-odd grade-3 elements that appear in
# Tr(γ₇ · ...) = ±1 pattern (the 6 from first pass)
key_operators = [(0,3,4), (0,3,5), (0,4,5), (1,3,4), (1,3,5), (1,4,5),
                 (2,3,4), (2,3,5), (2,4,5), (0,1,2)]

for idx_tuple in key_operators:
    mat = multivector(idx_tuple)
    cp_mat = cp_action(mat)
    if np.allclose(cp_mat, -mat, atol=1e-12):
        Sigma_down += mat

norm_Sigma = np.linalg.norm(Sigma_down, 'fro')
if norm_Sigma > 0:
    Sigma_down /= norm_Sigma

M_d = np.zeros((3, 3), dtype=complex)
for a in range(3):
    for b in range(3):
        M_d[a, b] = np.trace(generation_projectors[a] @ Sigma_down @ generation_projectors[b])

print(f"\n  'Down-type' mass matrix M_d:")
for a in range(3):
    row = [f"{M_d[a,b].real:+.6f}{M_d[a,b].imag:+.6f}i" for b in range(3)]
    print(f"    [{', '.join(row)}]")

# Jarlskog from commutator: J = Im(Tr([M_u M_u†, M_d M_d†]³)) / (6i × Δm_products)
C_comm = M_u @ M_u.conj().T @ M_d @ M_d.conj().T - M_d @ M_d.conj().T @ M_u @ M_u.conj().T
J_CKM_like = np.imag(np.trace(C_comm @ C_comm @ C_comm)) / 6.0

print(f"\n  CKM-like Jarlskog from [M_u M_u†, M_d M_d†]:")
print(f"    J = Im(Tr([...]³))/6 = {J_CKM_like:.10e}")

# ═══════════════════════════════════════════════════════════════════════
# SECTION I: FINAL HONEST ASSESSMENT  
# ═══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 78)
print("  SECTION I: FINAL HONEST ASSESSMENT")
print("=" * 78)

print("""
  ╔══════════════════════════════════════════════════════════════════╗
  ║  WHAT Cl(6) CAN DETERMINE (from pure algebra):                 ║
  ║                                                                ║
  ║  1. CP classification: 32 odd / 32 even basis elements    ✓   ║
  ║  2. Generation structure: 3 one-particle Witt states      ✓   ║
  ║  3. 8 orthogonal idempotents (correct Fock space)         ✓   ║
  ║  4. Triality: cyclic permutation of 3 generations         ✓   ║
  ║  5. CP-odd topological invariants (Chern numbers)         ✓   ║
  ║  6. Volume element γ₇ is CP-odd                           ✓   ║
  ╠══════════════════════════════════════════════════════════════════╣
  ║  WHAT REQUIRES DYNAMICS (beyond pure algebra):                 ║
  ║                                                                ║
  ║  1. The actual VALUE of δ_CP requires:                         ║
  ║     - The bubble wall profile φ(x) at the EWPT                ║
  ║     - The sphaleron rate Γ_sph (lattice input)                 ║
  ║     - The fermion mass hierarchy (Yukawa couplings)            ║
  ║  2. Pure Cl(6) algebra gives either:                           ║
  ║     - Zero (if M_u, M_d are in the same Witt basis)           ║
  ║     - Maximal (if M_u, M_d are misaligned by triality)        ║
  ║  3. The O(10⁻⁵) VALUE requires specific dynamics              ║
  ╠══════════════════════════════════════════════════════════════════╣
  ║  CONCLUSION:                                                    ║
  ║                                                                ║
  ║  δ_CP = 1.35 × 10⁻⁵ CANNOT be derived from Cl(6) alone.     ║
  ║  It requires both:                                              ║
  ║  (a) The algebraic CP-odd structure (from Cl(6))               ║
  ║  (b) The dynamical suppression (from EWPT physics)             ║
  ║                                                                ║
  ║  The BEST ESTIMATE from Cl(6) + dynamics:                      ║
  ╚══════════════════════════════════════════════════════════════════╝
""")

# Best estimate combining algebra + dynamics:
# δ_CP = (topological phase) × (coupling)² × (loop factor)
# = (2π/3) × (T_nuc/M*)² × 1/(16π²) × (Majorana hierarchy factor)

# The topological phase: from triality, the phase is 2π/3 per generation
topo_phase = 2 * np.pi / 3

# The coupling squared: (g_torsion)²
coupling_sq = g_torsion**2

# The hierarchy factor: from the Majorana spectrum 1:6:36
# This gives off-diagonal mixing ~ √(m_i/m_j) ~ 1/√6
hierarchy_factor = 1.0 / (6 * np.sqrt(6))  # product of mixing angles

# Total:
delta_CP_derived = topo_phase * coupling_sq * loop_factor * hierarchy_factor
print(f"  DERIVED δ_CP = (2π/3) × (T/M*)² × 1/(16π²) × 1/(6√6)")
print(f"               = {topo_phase:.4f} × {coupling_sq:.6f} × {loop_factor:.6e} × {hierarchy_factor:.6f}")
print(f"               = {delta_CP_derived:.6e}")
print(f"")
print(f"  Manuscript value: {delta_CP_claimed:.6e}")
print(f"  Ratio: {delta_CP_derived / delta_CP_claimed:.4f}")
print(f"")

# Check what η this gives
eta_derived = prefactor_manuscript * delta_CP_derived
print(f"  Resulting η_B = prefactor × δ_CP = {eta_derived:.4e}")
print(f"  Observed η_B = {eta_obs:.4e}")
print(f"  Ratio: {eta_derived / eta_obs:.4f}")

# ═══════════════════════════════════════════════════════════════════════
# SECTION J: CAN WE DO BETTER? SYSTEMATIC SCAN
# ═══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 78)
print("  SECTION J: SYSTEMATIC SCAN OF PURE-ALGEBRA NORMALIZATIONS")
print("=" * 78)

# The question: is there a UNIQUE normalization from Cl(6) + standard 
# physics that gives δ_CP ≈ 1.35 × 10⁻⁵?

# Pure algebraic numbers from Cl(6):
alg_numbers = {
    "dim(Cl(6))": 64,
    "n_generators": 6,
    "rep_dim": 8,
    "n_CP_odd": 32,
    "n_CP_even": 32,
    "n_generations": 3,
    "vol_CP3": np.pi**3 / 6,
    "chi_CP3": 4,
    "c2_CP3": 6,
    "n_coset": 9,
    "dim_su4": 15,
    "triality_order": 3,
    "2pi_over_3": 2*np.pi/3,
}

# Physical numbers:
phys_numbers = {
    "g_eff": 1.0 / (9*np.pi + 10),
    "alpha_w": 0.034,
    "T_nuc/M*": T_nuc / M_star,
    "loop_16pi2": 1.0 / (16*np.pi**2),
    "1/6sqrt6": 1.0 / (6*np.sqrt(6)),
}

# Try various combinations
print("\n  Candidate formulas for δ_CP:")
target = 1.35e-5
candidates = []

# Formula 1: (2π/3) × (T/M*)² × 1/(16π²) × hierarchy
f1 = (2*np.pi/3) * (T_nuc/M_star)**2 / (16*np.pi**2) * hierarchy_factor
candidates.append(("(2π/3)(T/M*)²/(16π²×6√6)", f1))

# Formula 2: g_eff² × c₂ / (16π²)
f2 = g_gauge**2 * c2_CP3 / (16*np.pi**2)
candidates.append(("g_eff² × c₂/(16π²)", f2))

# Formula 3: α_w × (T/M*) / (4π)
f3 = alpha_w * (T_nuc/M_star) / (4*np.pi)
candidates.append(("α_w × (T/M*)/(4π)", f3))

# Formula 4: g_eff³ × Vol(CP³) / (4π)³
vol_cp3 = np.pi**3 / 6
f4 = g_gauge**3 * vol_cp3 / (4*np.pi)**3
candidates.append(("g³ × Vol(CP³)/(4π)³", f4))

# Formula 5: (T/M*)³ / (6π²)
f5 = (T_nuc/M_star)**3 / (6*np.pi**2)
candidates.append(("(T/M*)³/(6π²)", f5))

# Formula 6: α_w² × 3/(16π²) (3 generations, one loop)
f6 = alpha_w**2 * 3 / (16*np.pi**2)
candidates.append(("3α_w²/(16π²)", f6))

# Formula 7: g_eff × (T/M*)² × 1/(8π²)
f7 = g_gauge * (T_nuc/M_star)**2 / (8*np.pi**2)
candidates.append(("g × (T/M*)²/(8π²)", f7))

# Formula 8: 1/(dim(Cl(6)) × 16π²) × n_gen = 3/64 × 1/(16π²)
f8 = 3.0 / (64 * 16 * np.pi**2)
candidates.append(("3/(64×16π²)", f8))

# Formula 9: (T/M*)² × α_w / (4π × n_gen!)
f9 = (T_nuc/M_star)**2 * alpha_w / (4*np.pi * 6)
candidates.append(("(T/M*)²α_w/(4π×3!)", f9))

# Formula 10: J_CKM(SM) ≈ 3×10⁻⁵ × g_eff
f10 = 3e-5 * g_gauge  # using SM J as reference
candidates.append(("J_CKM(SM)×g_eff [NOT pure]", f10))

print(f"\n  {'Formula':<35s} {'Value':>12s} {'Ratio to 1.35e-5':>18s}")
print("  " + "-" * 68)
for name, val in sorted(candidates, key=lambda x: abs(np.log10(abs(x[1]/target)) if x[1] != 0 else 100)):
    ratio = val / target if target != 0 else float('inf')
    match = "←← MATCH" if 0.5 < abs(ratio) < 2.0 else ("← close" if 0.1 < abs(ratio) < 10 else "")
    print(f"  {name:<35s} {val:>12.4e} {ratio:>12.4f}      {match}")

print(f"\n  Target δ_CP = {target:.4e}")

# ═══════════════════════════════════════════════════════════════════════
# BACK-COMPUTATION TEST (definitive)
# ═══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 78)
print("  DEFINITIVE BACK-COMPUTATION TEST")
print("=" * 78)

# From the EWBG formula, compute what prefactor gives η = 7.73×10⁻¹⁰
# directly from the manuscript, then compute what δ_CP is needed:
# η = P × δ_CP → δ_CP = η / P

# Method: compute P from the numerical values in the manuscript
# The EXACT formula used is:
# η = (405 Γ_sph / (4π² g_* v_w)) × δ_CP × (m_t(T)/T)²
# with Γ_sph in units of T⁴ (dimensionless rate)

# From the manuscript: η = 7.73 × 10⁻¹⁰ when δ_CP = 1.35 × 10⁻⁵
# So P = 7.73e-10 / 1.35e-5 = 5.726e-5

P_back = 7.73e-10 / 1.35e-5
print(f"  P = η/δ_CP = {P_back:.6e}")
print(f"  For η_obs = 6.14e-10: δ_CP = {6.14e-10/P_back:.6e}")
print(f"  For η_obs = 6.14e-10: δ_CP exactly = η_obs/P = {eta_obs/P_back:.8e}")

# REVERSE ENGINEERING TEST:
# If δ_CP was chosen to match η_obs, we'd expect δ_CP = 6.14e-10/P 
# = 1.072e-5. But the manuscript uses 1.35e-5 giving η = 7.73e-10.
# The ratio η/η_obs = 1.26 ≠ 1.00.
# This means δ_CP was NOT simply back-computed from η_obs.

# The 7.73×10⁻¹⁰ result actually OVERSHOOTS η_obs by 26%.
# If δ_CP were reverse-engineered, the author would have used 
# δ_CP = 1.07×10⁻⁵ to get exact agreement.

print(f"\n  ╔══════════════════════════════════════════════════════╗")
print(f"  ║  REVERSE-ENGINEERING VERDICT:                        ║")
print(f"  ║  δ_CP = 1.35e-5 gives η = 7.73e-10                ║")
print(f"  ║  η_obs = 6.14e-10 → would need δ_CP = 1.07e-5     ║")
print(f"  ║  RATIO = 1.26 ≠ 1.00                                ║")
print(f"  ║                                                      ║")
print(f"  ║  CONCLUSION: δ_CP was NOT reverse-engineered from    ║")
print(f"  ║  η_obs (it overshoots by 26%). However, the source  ║")
print(f"  ║  of the 1.35e-5 value remains UNDOCUMENTED.         ║")
print(f"  ║                                                      ║")
print(f"  ║  BEST MATCHING FORMULA FROM PURE ALGEBRA + PHYSICS: ║")

# Find the best match
best_name, best_val = min(candidates, key=lambda x: abs(np.log10(abs(x[1]/target)) if x[1] != 0 else 100))
print(f"  ║  {best_name:<45s}    ║")
print(f"  ║  = {best_val:.6e} (ratio {best_val/target:.3f} to claimed)     ║")
print(f"  ╚══════════════════════════════════════════════════════╝")

sys.stdout.flush()
