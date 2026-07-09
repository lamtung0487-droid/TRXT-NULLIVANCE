#!/usr/bin/env python3
"""
TRXT V10 Direction C — Phase C1+C2: Division Algebra → SM Gauge Groups
======================================================================
Master Protocol V2.0 — REQUIRED: CANONICAL DERIVATION (No Ad-Hoc Constructions)

Derives:
  C1. Octonion algebra O & G₂ = Der(O) (Computed via derivation constraints)
  C1. SU(3) = Stab_G2(e_1) (Computed via nullspace)
  C2. SU(2) = Stab_G2(H) (Computed via nullspace) - THE CANONICAL WAY
      * Not by constructing pre-defined rotation matrices *
      * But by finding the subalgebra of G2 that kills the H-subalgebra *

Mathematical foundations:
  - G₂ is the automorphism group of the octonions.
  - SU(3) is the subgroup fixing one unit imaginary (e.g. e1).
  - SU(2) is the subgroup fixing a quaternionic subalgebra (e.g. 1, e1, e2, e4).
    (Mathematically this SU(2) acts on the orthogonal complement H_perp).

References:
  - Baez (2002) "The Octonions"
  - Furey (2018)

Author: TRXT-Nullivance V10 Division Algebra Campaign
Date: 2026-02-13
"""
import numpy as np
import json
import os
from datetime import datetime
from itertools import combinations

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer,)): return int(obj)
        if isinstance(obj, (np.floating,)): return float(obj)
        if isinstance(obj, (np.bool_,)): return bool(obj)
        if isinstance(obj, np.ndarray): return obj.tolist()
        return super().default(obj)

# =============================================================================
# ALGEBRA BUILDERS
# =============================================================================

FANO_TRIPLES = [
    (1, 2, 4), (2, 3, 5), (3, 4, 6), (4, 5, 7),
    (5, 6, 1), (6, 7, 2), (7, 1, 3),
]

def build_structure_constants():
    """Build octonion structure constants f_ijk."""
    f = np.zeros((7, 7, 7), dtype=int)
    for (a, b, c) in FANO_TRIPLES:
        i, j, k = a-1, b-1, c-1
        f[i, j, k] = 1
        f[j, k, i] = 1
        f[k, i, j] = 1
        f[j, i, k] = -1
        f[k, j, i] = -1
        f[i, k, j] = -1
    return f

# =============================================================================
# DERIVATION ALGEBRA SOLVER (G2)
# =============================================================================

def compute_g2_generators(f):
    """
    Compute Der(O) by solving linear system D(xy) = D(x)y + xD(y).
    Returns basis of 7x7 matrices.
    """
    # ... (Same robust logic as before) ...
    constraints = []
    
    # Derivation condition constraints
    for i in range(7):
        for j in range(7):
            if i == j: continue
            for c in range(7):
                row = np.zeros(49)
                # LHS: sum_k f[i,j,k] D[c,k]
                for k in range(7):
                    if f[i, j, k] != 0: row[c*7 + k] -= f[i, j, k]
                # RHS term 1: sum_a D[a,i] f[a,j,c]
                for a in range(7):
                    if f[a, j, c] != 0: row[a*7 + i] += f[a, j, c]
                # RHS term 2: sum_b D[b,j] f[i,b,c]
                for b in range(7):
                    if f[i, b, c] != 0: row[b*7 + j] += f[i, b, c]
                constraints.append(row)

    # Antisymmetry constraints D_ab + D_ba = 0
    for a in range(7):
        for b in range(a, 7):
            row = np.zeros(49)
            if a == b:
                row[a*7 + a] = 1
            else:
                row[a*7 + b] = 1
                row[b*7 + a] = 1
            constraints.append(row)

    A = np.array(constraints)
    U, S, Vt = np.linalg.svd(A)
    tol = 1e-10
    null_dim = np.sum(S < tol) + (49 - len(S))
    null_vectors = Vt[len(S)-np.sum(S < tol):] if len(S) == 49 else Vt[np.sum(S > tol):]
    
    generators = []
    for vec in null_vectors:
        D = vec.reshape(7, 7)
        D[np.abs(D) < 1e-12] = 0
        generators.append(D)
        
    return generators

# =============================================================================
# CANONICAL STABILIZER EXTRACTION
# =============================================================================

def get_stabilizer(generators, fixed_indices):
    """
    Find the subalgebra of 'generators' that annihilates all basis vectors 
    in 'fixed_indices'.
    
    This computes Stab_g({e_i}) = { D in g | D(e_i) = 0 for all i in fixed_indices }
    
    Start with raw G2 generators and find the linear combinations that 
    have zeros in the columns corresponding to fixed_indices.
    """
    n = len(generators)
    if n == 0: return []
    
    # We need sum_k c_k * D_k[row, fixed_col] = 0 for all row, all fixed_col
    
    # Build a constraint matrix where columns are the coefficients c_k
    # Rows are the conditions: (row, fixed_col) pairs
    constraints = []
    
    for D_k in generators:
        # Extract the columns corresponding to fixed indices
        # We need these relevant columns to be zero
        relevant_cols = D_k[:, fixed_indices] # shape (7, num_fixed)
        constraints.append(relevant_cols.flatten())
        
    # Matrix A: shape (n_generators, 7*num_fixed)
    # We want to find null space of A.T (linear combos of generators)
    A = np.array(constraints).T 
    
    # Solve A * x = 0
    U, S, Vt = np.linalg.svd(A)
    tol = 1e-10
    null_dim = np.sum(S < tol) + (n - len(S) if len(S) < n else 0)
    
    # Null vectors are in Vt
    stabilizer_coeffs = Vt[len(S)-np.sum(S < tol):] if len(S) < n else Vt[np.sum(S > tol):]
    
    bsub = []
    for coeffs in stabilizer_coeffs:
        D_sub = sum(coeffs[i] * generators[i] for i in range(n))
        D_sub[np.abs(D_sub) < 1e-12] = 0
        bsub.append(D_sub)
        
    return bsub

# =============================================================================
# ALGEBRA VERIFICATION UTILS
# =============================================================================

def verify_algebra(generators, name="Algebra"):
    """
    Check closure, Jacobi identity, antisymmetric. 
    Returns dict with stats.
    """
    res = {"name": name, "dim": len(generators), "valid": True}
    
    # 1. Antisymmetry
    err_anti = max([np.linalg.norm(D + D.T) for D in generators]) if generators else 0
    res['antisym_error'] = float(err_anti)
    if err_anti > 1e-9: res['valid'] = False

    # 2. Closure
    # Commutator should be in span
    basis = np.array([D.flatten() for D in generators]).T # (49, N)
    max_closure_err = 0.0
    
    # Use QR or SVD to check span
    if len(generators) > 0:
        Q, R = np.linalg.qr(basis)
        for i in range(len(generators)):
            for j in range(i+1, len(generators)):
                comm = generators[i]@generators[j] - generators[j]@generators[i]
                comm_vec = comm.flatten()
                
                # Project onto Q
                proj = Q @ (Q.T @ comm_vec)
                resid = np.linalg.norm(comm_vec - proj)
                max_closure_err = max(max_closure_err, resid)
    
    res['closure_error'] = float(max_closure_err)
    if max_closure_err > 1e-9: res['valid'] = False

    # 3. Jacobi
    max_jacobi_err = 0.0
    # Test random triples if too large
    import random
    n_tests = 100
    idxs = list(range(len(generators)))
    
    for _ in range(n_tests):
        if len(idxs) < 3: break
        a,b,c = random.sample(idxs, 3)
        A,B,C = generators[a], generators[b], generators[c]
        J = (A@B - B@A)@C - C@(A@B - B@A) + \
            (B@C - C@B)@A - A@(B@C - C@B) + \
            (C@A - A@C)@B - B@(C@A - A@C)
        max_jacobi_err = max(max_jacobi_err, np.linalg.norm(J))
        
    res['jacobi_error'] = float(max_jacobi_err)
    if max_jacobi_err > 1e-9: res['valid'] = False
    
    return res

# =============================================================================
# MAIN
# =============================================================================

def main():
    print("="*60)
    print("TRXT V10: CANONICAL DERIVATION RUN")
    print("Phase C1/C2: G2 -> SU(3) -> SU(2) via Stabilizers")
    print("="*60)
    
    results = {}
    
    # 1. Build Algebra
    f = build_structure_constants()
    print(f"\n[1] Built Octonion Structure Constants (Fano).")
    
    # 2. Compute G2 (Derivations)
    print(f"\n[2] Computing Der(O) = G2 via derivation constraints...")
    g2_gens = compute_g2_generators(f)
    print(f"    G2 Dimension found: {len(g2_gens)} (Expected 14)")
    
    g2_check = verify_algebra(g2_gens, "G2")
    print(f"    Validation: {g2_check}")
    
    # 3. Extract SU(3) (Stabilizer of e1)
    # Baez: SU(3) is the subgroup of G2 that fixes a specific imaginary unit.
    print(f"\n[3] Extracting SU(3) = Stab_G2(e1)...")
    # e1 corresponds to index 0 in our 0-6 imaginary arrays
    su3_gens = get_stabilizer(g2_gens, [0]) # Fix index 0 (e1)
    print(f"    SU(3) Dimension found: {len(su3_gens)} (Expected 8)")
    
    su3_check = verify_algebra(su3_gens, "SU(3)")
    print(f"    Validation: {su3_check}")
    
    # 4. Extract SU(2) (Stabilizer of Quaternionic Subalgebra H)
    # H = span{1, e1, e2, e4} (First Fano line)
    # The subgroup of G2 that preserves H *pointwise* is SU(2).
    # Why? Aut(O) fixing H pointwise acts on H_perp (4 dim).
    # Actually, fixing a quaternion subalgebra usually leaves an SU(2) freedom?
    # Wait, Aut(H) is SO(3).
    # We want the SU(2) associated with H.
    # The reviewer said: "Extract the stabilizer of that H inside G2. That stabilizer is isomorphic to SO(4) or SU(2)xSU(2)?"
    # Actually, let's look at the math:
    # If we fix the subalgebra H = {1, e1, e2, e4}, 
    # we are looking for D in G2 such that D(H) subset H? No.
    # The reviewer said: "Pick a quaternionic subalgebra... Extract the stabilizer... Then explicitly split."
    
    # Let's try fixing TWO imaginary units in the subalgebra.
    # e1 and e2.
    # e4 = e1*e2 is then automatically fixed by derivation property.
    # So fixing e1, e2 is equivalent to fixing the whole quaternion subalgebra H pointwise.
    # Stab(H pointwise) = Stab(e1) intersect Stab(e2).
    # dim(Stab(e1)) = 8 (SU3).
    # Inside SU(3), fixing another vector e2 reduces it to SU(2).
    # This SU(2) acts on the complement of H.
    
    # Is this the "Weak" SU(2)?
    # In Furey's model, SU(2)_L acts on H?
    # Actually, the SM SU(2) comes from the automorphisms of H itself?
    # No, G2 automorphisms are inner.
    # The "canonical" SU(2) inside G2 is usually the one associated with the H-subalgebra.
    
    print(f"\n[4] Extracting SU(2) = Stab_G2(H_subalgebra)...")
    # Fix e1 (index 0) and e2 (index 1). e4 determined.
    # This finds the automorphisms that leave H pointwise invariant.
    su2_gens = get_stabilizer(g2_gens, [0, 1])
    print(f"    SU(2) generators found (fixing H ptwise): {len(su2_gens)}")
    
    su2_check = verify_algebra(su2_gens, "SU(2)")
    print(f"    Validation: {su2_check}")
    
    # NOW: Verify these generators satisfy [Ti, Tj] = eps Tk?
    # The generators found are a basis. They might not be normalized to eps_ijk.
    # But they must form a 3D Lie algebra. 
    # Is it SU(2) ~ SO(3)?
    # Jacobian check passed means it is a Lie algebra.
    # 3D, simple -> must be SO(3) or SL(2). Since compact (subgroup of SO(7)), it is SO(3)~SU(2).
    
    # Can we find the basis that satisfies standard commutation?
    # We can try to diagonalize the Casimir or just check structure constants.
    
    results = {
        "G2": g2_check,
        "SU3": su3_check,
        "SU2": su2_check,
        "Method": "Canonical Stabilizer Extraction (No Matrices Hardcoded)"
    }
    
    # Save
    outdir = os.path.join(os.path.dirname(__file__), "..", "results")
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "C1C2_canonical_results.json"), "w") as f_out:
        json.dump(results, f_out, indent=2, cls=NumpyEncoder)

if __name__ == "__main__":
    main()
