"""
Gate 0b: Ghost / gradient-instability / causality check for the TRXT
k-essence sector P(X) = c2*X + c4*X^2 -- on BOTH branches of X.

This is the check that MASTER-PROTOCOL Article III G0 actually requires
("no ghosts, c_s <= 1 in ALL environments") and that Appendix X of the
report only performed for X > 0 (cosmological branch). Static screening
configurations have spacelike gradients, i.e. X = -(nabla phi)^2/2 < 0,
so the X < 0 branch is physical and mandatory.

Criteria (pre-declared, from the standard k-essence conditions):
  ghost-free      : P_X > 0
  gradient-stable : P_X + 2*X*P_XX > 0
  causal          : 0 < c_s^2 = P_X / (P_X + 2*X*P_XX) <= 1

PASS iff all three hold on the entire physical X-range sampled.
Run from repo root: python experiments/v17_gates/Gate0b_StabilityCheck.py
"""
import sys
import numpy as np

def check(c2=1.0, c4=1.0):
    # Dimensionless scan: X in units of c2/c4. Physical environments span
    # r = c4*X/c2 from ~0 (vacuum) to ~1e3 (report Table 9), and the static
    # screening branch mirrors this range at negative X.
    r = np.concatenate([-np.logspace(-3, 3, 400), np.logspace(-3, 3, 400)])
    X = r * c2 / c4

    P_X = c2 + 2 * c4 * X
    K = P_X + 2 * X * (2 * c4)          # P_X + 2 X P_XX
    with np.errstate(divide='ignore', invalid='ignore'):
        cs2 = np.where(K != 0, P_X / K, np.inf)

    ghost_ok = P_X > 0
    grad_ok = K > 0
    causal_ok = (cs2 > 0) & (cs2 <= 1.0 + 1e-12)
    ok = ghost_ok & grad_ok & causal_ok

    print("--- GATE 0b: FULL-BRANCH STABILITY CHECK, P(X) = c2 X + c4 X^2 ---")
    print(f"  scan: r = c4 X / c2 in [-1e3, 1e3], {len(r)} points")

    pos = r > 0
    neg = r < 0
    print(f"  X > 0 branch: {ok[pos].sum()}/{pos.sum()} points healthy "
          f"({'ALL OK' if ok[pos].all() else 'VIOLATIONS'})")
    print(f"  X < 0 branch: {ok[neg].sum()}/{neg.sum()} points healthy "
          f"({'ALL OK' if ok[neg].all() else 'VIOLATIONS'})")

    if not ok[neg].all():
        bad = r[neg & ~ok]
        # Analytic boundaries: P_X = 0 at r = -1/2 ; K = 0 at r = -1/6
        first_kind = []
        if (~ghost_ok[neg]).any():
            first_kind.append("GHOST (P_X < 0) for r < -1/2")
        if ((~grad_ok) & ghost_ok)[neg].any():
            first_kind.append("gradient instability / c_s^2 pathology for -1/2 < r < -1/6")
        if ((~causal_ok) & grad_ok & ghost_ok)[neg].any():
            first_kind.append("superluminal c_s^2 > 1 for -1/6 < r < 0")
        print("  X<0 pathologies found:")
        for k in first_kind:
            print(f"    - {k}")
        print(f"  worst r sampled: {bad.min():.3g} .. {bad.max():.3g}")

    if ok.all():
        print(">>> GATE 0b STATUS: PASS (ghost-free, stable, subluminal on both branches) <<<")
        return 0
    else:
        print(">>> GATE 0b STATUS: FAIL <<<")
        print("  The declared G0 criterion ('all environments') is NOT met:")
        print("  static screening configurations (X < 0) hit the instability/superluminal")
        print("  window identified in theory/reviews/audit_core_framework_20260709.md Item 5.")
        print("  Required fix: re-derive the screening branch stability (e.g. constraint")
        print("  mechanism, different P(X) completion) before G0 can pass honestly.")
        return 1

if __name__ == "__main__":
    sys.exit(check())
