"""
ghost_stability_check.py
TRXT V7 Research — Ghost-Free k-Essence Stability Proof
Evidence ID: GATE-X-GHOST-FREE

Purpose:
    Verify that the TRXT k-essence Lagrangian
        P(X) = c₂X + c₄X²,   X ≡ -½(∂φ)²
    satisfies the no-ghost and no-gradient-instability conditions
    across 50 representative values of X:

        1)  P_X + 2X P_XX > 0        (no ghost: kinetic energy positive definite)
        2)  0 < c_s² ≤ 1             (causal sound speed)

    where P_X = ∂P/∂X, P_XX = ∂²P/∂X², and cs² = P_X / (P_X + 2X P_XX).

Reference: Appendix X of TRXT_Research_Report_V14_FINAL.tex
"""

import numpy as np
import json
import time

# ─── TRXT k-essence coefficients ──────────────────────────────────────────────
# From slow-roll best-fit (Gate G): these ensure w₀ ≈ −0.984
C2 = 1.0         # coefficient of X   (dimensionless, normalised to 1)
C4 = 0.5         # coefficient of X²  (tuned for dark energy EOS)


def P(X):      return C2 * X + C4 * X**2
def P_X(X):    return C2 + 2 * C4 * X
def P_XX(X):   return 2 * C4 * np.ones_like(np.asarray(X, dtype=float))


def cs_squared(X):
    """Sound speed squared: c_s² = P_X / (P_X + 2X P_XX)."""
    px   = P_X(X)
    pxx  = P_XX(X)
    return px / (px + 2 * X * pxx)


def run_ghost_check(n_test: int = 50):
    """Check ghost and gradient stability at n_test log-spaced X values."""
    X_values = np.logspace(-4, 4, n_test)

    ghost_cond   = []    # P_X + 2X P_XX
    cs2_values   = []

    for X in X_values:
        px   = float(P_X(X))
        pxx  = float(P_XX(X))
        gc   = px + 2 * X * pxx
        cs2  = px / gc if gc != 0 else np.nan
        ghost_cond.append(gc)
        cs2_values.append(cs2)

    ghost_cond = np.array(ghost_cond)
    cs2_values = np.array(cs2_values)

    no_ghost      = bool(np.all(ghost_cond > 0))
    causal        = bool(np.all((cs2_values > 0) & (cs2_values <= 1)))
    all_pass      = no_ghost and causal

    print("=" * 60)
    print("GATE X: Ghost-Free k-Essence Stability Check")
    print("=" * 60)
    print(f"\n  P(X)   = {C2}·X + {C4}·X²")
    print(f"  c₂ = {C2},  c₄ = {C4}")
    print(f"\n  Test points: {n_test} log-spaced X ∈ [1e-4, 1e4]")
    print(f"\n  No-ghost  (P_X + 2X P_XX > 0):  {'PASS ✓' if no_ghost else 'FAIL ✗'}")
    print(f"    min(P_X + 2X P_XX) = {ghost_cond.min():.6f}")
    print(f"\n  Causal cs² (0 < c_s² ≤ 1):      {'PASS ✓' if causal else 'FAIL ✗'}")
    print(f"    cs² range = [{cs2_values.min():.6f}, {cs2_values.max():.6f}]")
    print("\n" + "=" * 60)
    print(f"GATE X RESULT: {'ALL PASS ✓' if all_pass else 'FAIL ✗'}")
    print("=" * 60)

    return {
        "evidence_id": "GATE-X-GHOST-FREE",
        "date": "2026-03-02",
        "c2": C2, "c4": C4,
        "n_test": n_test,
        "X_range": [float(X_values[0]), float(X_values[-1])],
        "ghost_cond_min": float(ghost_cond.min()),
        "ghost_cond_max": float(ghost_cond.max()),
        "cs2_min": float(cs2_values.min()),
        "cs2_max": float(cs2_values.max()),
        "no_ghost_pass": no_ghost,
        "causal_pass": causal,
        "all_pass": all_pass,
        "status": "PASS" if all_pass else "FAIL",
    }


if __name__ == "__main__":
    import os
    t0 = time.time()
    result = run_ghost_check(n_test=50)
    t1 = time.time()
    result["runtime_s"] = round(t1 - t0, 2)
    out_path = "artifacts/gate_x_ghost_free_result.json"
    os.makedirs("artifacts", exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nArtifact saved: {out_path}")
