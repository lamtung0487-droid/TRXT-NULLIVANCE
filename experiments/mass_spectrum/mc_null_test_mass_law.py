"""
Monte Carlo null test for the harmonic mass law m(p,q) = M*(1/p + 1/q).

Question: given the mode density of the (p,q) lattice, how well does a RANDOM
mass in [50, 200] GeV match some mode, compared to the real W/Z/Higgs masses?
If random masses match as well as real ones, the law has no discriminating power.

Run from repo root: python results/mc_null_test_mass_law.py
"""
import numpy as np

M_STAR = 365.240678  # GeV, value printed by the lab's own robustness report
P_MAX = Q_MAX = 200

# Real masses (PDG 2024)
REAL = {"W": 80.3692, "Z": 91.1876, "Higgs": 125.20}

def all_modes(lo=50.0, hi=200.0):
    modes = set()
    for p in range(1, P_MAX + 1):
        for q in range(p, Q_MAX + 1):
            m = M_STAR * (1.0 / p + 1.0 / q)
            if lo <= m <= hi:
                modes.add(m)
    return np.sort(np.array(list(modes)))

def best_rel_err(mass, modes):
    i = np.searchsorted(modes, mass)
    cands = modes[max(0, i - 1):i + 1]
    return np.min(np.abs(cands - mass) / mass)

def main():
    rng = np.random.default_rng(20260709)
    modes = all_modes()
    print(f"Mode count in [50, 200] GeV (deduplicated): {len(modes)}")
    print(f"Median gap between adjacent modes: {np.median(np.diff(modes)):.4f} GeV")

    n_trials = 100_000
    fake = rng.uniform(50.0, 200.0, n_trials)
    errs = np.array([best_rel_err(m, modes) for m in fake])

    print(f"\nNull distribution of best relative match error (random masses):")
    for pct in (50, 90, 99):
        print(f"  {pct}th percentile: {np.percentile(errs, pct)*100:.4f}%")
    frac_01 = np.mean(errs < 1e-3)
    print(f"  Fraction of RANDOM masses matching some mode within 0.1%: {frac_01*100:.1f}%")

    print(f"\nReal particles:")
    for name, m in REAL.items():
        e = best_rel_err(m, modes)
        p_val = np.mean(errs <= e)  # look-elsewhere-corrected p-value vs null
        print(f"  {name}: best match error {e*100:.4f}%  ->  p-value vs null = {p_val:.3f}")

    print("\nInterpretation: p-value ~ O(1) means the real masses match no better")
    print("than random numbers would, i.e. the lattice is dense enough to fit anything.")

if __name__ == "__main__":
    main()
