"""
verify_g2_stab.py
TRXT V7 Research — G₂ Stabiliser Subgroup Verification
Evidence ID: GATE-V-G2-STAB

Purpose:
    Verify that the octonionic exceptional group G₂ = Aut(O) has the correct
    stabiliser subgroups:
        Stab_{G₂}(e₁) ≅ SU(3)  with Lie algebra dim = 8
        Stab_{G₂}(H)  ≅ SO(4)  with Lie algebra dim = 6

    Here e₁ is a unit octonion and H = span{1, e₁, e₂, e₃} is the
    quaternionic imaginary subalgebra.

Algorithm (Appendix S.10):
    1. Build G₂ generators as antisymmetric derivations of O via SVD.
    2. For each generator M, check if [M, e₁] = 0 (stabiliser condition).
    3. Count linearly independent elements in the stabiliser.

Reference: Appendix S.10 of TRXT_Research_Report_V14_FINAL.tex
"""

import numpy as np
import json
import time

# ─── Fano plane octonion multiplication ───────────────────────────────────────
#
# Basis: e0=1, e1..e7 (imaginary units)
# Fano lines: {1,2,4},{2,3,5},{3,4,6},{4,5,7},{5,6,1},{6,7,2},{7,1,3}
# with cyclic rule: eᵢeⱼ = eₖ, eⱼeₖ = eᵢ, eₖeᵢ = eⱼ  (+1 or −1 by orientation)

FANO_LINES = [
    (1, 2, 4),
    (2, 3, 5),
    (3, 4, 6),
    (4, 5, 7),
    (5, 6, 1),
    (6, 7, 2),
    (7, 1, 3),
]


def build_oct_mul():
    """Build 8×8 octonionic structure tensor C[i,j,k]: eᵢ·eⱼ = Σₖ C[i,j,k] eₖ."""
    C = np.zeros((8, 8, 8))
    # e₀ = 1 is the identity
    for i in range(8):
        C[0, i, i] = 1.0
        C[i, 0, i] = 1.0

    for (a, b, c) in FANO_LINES:
        # Cyclic: eₐ·eᵦ = eᵣ  (and all cyclic permutations)
        for (i, j, s) in [(a, b, c), (b, c, a), (c, a, b)]:
            C[i, j, s] += 1.0    # eᵢ·eⱼ = eₛ
            C[j, i, s] -= 1.0    # eⱼ·eᵢ = −eₛ  (anti-commutativity)

    # Imaginary units square to −1: eᵢ² = −e₀
    for i in range(1, 8):
        C[i, i, 0] -= 1.0
    return C


def left_mult_mat(a_vec, C):
    """8×8 matrix for left multiplication by a ∈ O."""
    M = np.zeros((8, 8))
    for j in range(8):
        for k in range(8):
            M[:, j] += a_vec[k] * C[k, j, :]
    return M


def get_g2_gens(C):
    """
    Build G₂ generators by finding derivations D: O → O satisfying
        D(xy) = D(x)y + xD(y)

    Use SVD on the (derivation condition) matrix kernel.
    Returns list of 14 basis derivation matrices (7×7 on imaginary subspace).
    """
    # G₂ acts on the 7-dimensional imaginary part Im(O) = span{e₁,...,e₇}
    # Derivation condition (on imaginary elements): [D, L_a] + [D, R_a] = L_{Da} + R_{Da}
    # Simplified: D must preserve structure constants.
    # We build the 49×49 "derivation constraint" system and find its kernel.

    dim = 7  # imaginary octonions e₁..e₇
    # Structure constants f[i,j,k] for imaginary part (i,j,k ∈ 0..6)
    f = np.zeros((dim, dim, dim))
    for i in range(dim):
        for j in range(dim):
            for k in range(dim):
                f[i, j, k] = C[i+1, j+1, k+1]

    # Derivation condition: D_{ia} f_{ajk} + D_{ja} f_{iak} = f_{ija} D_{ak}
    # Reshape into a linear system: A @ vec(D) = 0
    n2 = dim * dim
    rows = []
    for i in range(dim):
        for j in range(i+1, dim):
            for k in range(dim):
                row = np.zeros(n2)
                # D_{ia} f_{ajk}
                for a in range(dim):
                    row[i*dim + a] += f[a, j, k]
                # D_{ja} f_{iak}
                for a in range(dim):
                    row[j*dim + a] += f[i, a, k]
                # -f_{ija} D_{ak}
                for a in range(dim):
                    row[a*dim + k] -= f[i, j, a]
                rows.append(row)

    # Add antisymmetry constraint: D + D^T = 0  (derivations of compact form)
    for i in range(dim):
        for j in range(i+1, dim):
            row = np.zeros(n2)
            row[i*dim + j] = 1.0
            row[j*dim + i] = 1.0
            rows.append(row)

    A = np.array(rows)
    _, s, Vt = np.linalg.svd(A)
    tol = 1e-8
    null_mask = s < tol if len(s) == n2 else np.zeros(n2, dtype=bool)
    # Pad s to n2 length
    s_full = np.zeros(n2)
    s_full[:len(s)] = s
    null_mask = s_full < tol

    gens = [Vt[i].reshape(dim, dim) for i in range(n2) if null_mask[i]]

    # Fallback: use kernel of A directly
    if len(gens) == 0:
        _, _, Vt2 = np.linalg.svd(A, full_matrices=True)
        rank = np.sum(s_full > tol)
        gens = [Vt2[i].reshape(dim, dim) for i in range(rank, n2)]

    return gens


def get_stab_dim(gens, fixed_vec):
    """
    Return dimension of Lie(Stab(v)) = ker(action on v) inside span(gens).

    Method: build the "action matrix" R with rows R_a = (M_a @ v).
    The stabiliser has dimension dim(gens) - rank(R) because each
    independent image direction removes one stabiliser direction.
    """
    if len(gens) == 0:
        return 0

    # Build action matrix: rows are (M_a @ fixed_vec)
    R = np.array([M @ fixed_vec for M in gens])   # shape (n_gens, dim_v)
    n_gens = R.shape[0]
    rank_R = np.linalg.matrix_rank(R, tol=1e-7)
    return n_gens - rank_R


def get_subalgebra_stab_dim(gens, basis_indices):
    """
    Return dimension of the subgroup of G₂ that preserves the subspace
    V = span{e_i : i in basis_indices} setwise.

    Condition: for each generator M and each basis vector e_i in V,
    M @ e_i must lie in V (all components outside basis_indices are zero).

    We use the action matrix on the "escape directions": rows are the
    out-of-subspace components of M @ e_i for each i in basis_indices,
    concatenated over all basis vectors.
    """
    if len(gens) == 0:
        return 0

    dim = 7
    outside_idx = [j for j in range(dim) if j not in basis_indices]

    # For each generator M_a, collect the "leakage rows":
    # For each basis index i, compute (M_a @ e_i) restricted to outside_idx
    leakage_rows = []
    for M in gens:
        leak = []
        for i in basis_indices:
            e_i = np.zeros(dim)
            e_i[i] = 1.0
            Mei = M @ e_i
            leak.extend([Mei[j] for j in outside_idx])
        leakage_rows.append(leak)

    R = np.array(leakage_rows)   # shape (n_gens, len(basis_indices)*len(outside_idx))
    n_gens = R.shape[0]
    rank_R = np.linalg.matrix_rank(R, tol=1e-7)
    return n_gens - rank_R


def run_g2_stab():
    print("=" * 60)
    print("GATE V: G₂ Stabiliser Subgroup Verification")
    print("=" * 60)

    C = build_oct_mul()

    # Build G₂ generators
    gens = get_g2_gens(C)
    dim_G2 = len(gens)
    print(f"\n  G₂ generator count (should be 14): {dim_G2}")

    # Stabiliser of e₁ (should be SU(3), dim = 8)
    e1_imag = np.zeros(7)
    e1_imag[0] = 1.0   # e₁ is first imaginary unit
    dim_stab_e1 = get_stab_dim(gens, e1_imag)
    print(f"  Dim(Stab(e₁)) [expect 8 = SU(3)]: {dim_stab_e1}")

    # Stabiliser of Im(ℍ) = span{e₁,e₂,e₄} as subspace (should be SO(4), dim = 6)
    # Under this Fano convention, {e₁,e₂,e₄} are the imaginary units of ℍ
    # (e₁e₂=e₄ from line {1,2,4}). Indices 0,1,3 in 0-indexed imaginary space.
    dim_stab_H = get_subalgebra_stab_dim(gens, basis_indices=[0, 1, 3])
    print(f"  Dim(Stab(H))  [expect 6 = SO(4)]:  {dim_stab_H}")

    pass_G2   = (dim_G2 == 14)
    pass_su3  = (dim_stab_e1 == 8)
    pass_so4  = (dim_stab_H == 6)
    all_pass  = pass_G2 and pass_su3 and pass_so4

    print(f"\n  G₂ dim = 14:                  {'PASS ✓' if pass_G2 else 'FAIL ✗'}")
    print(f"  Stab(e₁) = SU(3) (dim=8):    {'PASS ✓' if pass_su3 else 'FAIL ✗'}")
    print(f"  Stab(H) = SO(4) (dim=6):     {'PASS ✓' if pass_so4 else 'FAIL ✗'}")
    print("\n" + "=" * 60)
    print(f"GATE V RESULT: {'ALL PASS ✓' if all_pass else 'PARTIAL/FAIL ✗'}")
    print("=" * 60)

    artifact = {
        "evidence_id": "GATE-V-G2-STAB",
        "date": "2026-03-02",
        "dim_G2": int(dim_G2),
        "dim_stab_e1": int(dim_stab_e1),
        "dim_stab_H": int(dim_stab_H),
        "expected": {"dim_G2": 14, "dim_stab_e1": 8, "dim_stab_H": 6},
        "pass_G2": bool(pass_G2),
        "pass_su3": bool(pass_su3),
        "pass_so4": bool(pass_so4),
        "all_pass": bool(all_pass),
        "status": "PASS" if all_pass else "PARTIAL"
    }
    return artifact


if __name__ == "__main__":
    import os
    t0 = time.time()
    result = run_g2_stab()
    t1 = time.time()
    result["runtime_s"] = round(t1 - t0, 2)
    out_path = "artifacts/gate_v_g2_stab_result.json"
    os.makedirs("artifacts", exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nArtifact saved: {out_path}")
