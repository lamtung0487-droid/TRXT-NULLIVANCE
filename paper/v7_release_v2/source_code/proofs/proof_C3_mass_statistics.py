"""
proof_C3_mass_statistics.py — Statistical Analysis of TRXT Mass Predictions
=============================================================================
TRXT V7 — C3 Critical Error Resolution
Evidence ID: C3-STATS-2026-03

QUESTION: Given M(p,q) = M*(1/p + 1/q) with M* = 365.24 GeV,
is matching W, Z, H masses to <0.2% statistically remarkable,
or inevitable given the dense spectrum of modes?

APPROACH:
  1. Look-elsewhere effect: count modes near each target mass
  2. Monte Carlo: random M* → probability of simultaneous 3-particle match
  3. Sector-constrained test: given p is fixed, is q unique?
  4. Combined p-value for the 3-particle simultaneous match

References: Academic Critique (C3), Appendix W, Chapter Z
"""

import numpy as np
from collections import defaultdict
import json, os, time

# ====================================================================
# Physical Constants
# ====================================================================
M_STAR = 365.24  # GeV (TRXT scale)
ALPHA = 1 / 137.036
M_TAU = 1.77686  # GeV

# Observed masses (PDG 2024)
M_W_OBS = 80.3692     # GeV (PDG 2024 average)
M_W_ERR = 0.0133      # GeV
M_Z_OBS = 91.1876     # GeV
M_Z_ERR = 0.0021      # GeV
M_H_OBS = 125.20      # GeV
M_H_ERR = 0.11        # GeV

# TRXT predictions
PREDICTIONS = {
    'W': {'p': 5, 'q': 50, 'mass': M_STAR * (1/5 + 1/50)},
    'Z': {'p': 8, 'q': 8,  'mass': M_STAR * (1/8 + 1/8)},
    'H': {'p': 5, 'q': 7,  'mass': M_STAR * (1/5 + 1/7)},
}

# Sector rules from TRXT (homotopy hypothesis)
SECTOR_RULES = {
    'W': {'p': 5, 'reason': 'EW sector: dim(fund(SU(5))) = 5'},
    'Z': {'p': 8, 'reason': 'Neutral sector: Cl(6) dim = 8'},
    'H': {'p': 5, 'reason': 'EW sector: same as W'},
}


def mass_formula(p, q, m_star=M_STAR):
    """E(p,q) = M* (1/p + 1/q)"""
    return m_star * (1.0/p + 1.0/q)


def find_q_for_mass(p, m_obs, m_star=M_STAR):
    """Given sector p and observed mass, find the unique q."""
    denom = p * m_obs - m_star
    if denom <= 0:
        return None
    q_exact = p * m_star / denom
    q_int = round(q_exact)
    if q_int < 1:
        return None
    return q_int


# ====================================================================
# TEST 1: Mode Counting (Look-Elsewhere Effect)
# ====================================================================
def count_modes_near_mass(m_obs, tolerance_GeV, p_max=200, q_max=1000,
                          m_star=M_STAR):
    """Count how many (p,q) pairs give mass within tolerance of m_obs."""
    matches = []
    for p in range(1, p_max + 1):
        for q in range(p, q_max + 1):  # q >= p by convention
            m = mass_formula(p, q, m_star)
            if abs(m - m_obs) < tolerance_GeV:
                matches.append((p, q, m))
    return matches


def test_mode_counting():
    """Test 1: How many modes match each particle?"""
    print("\n" + "=" * 70)
    print("TEST 1: Mode Counting (Look-Elsewhere Effect)")
    print("=" * 70)
    print(f"  Search space: p <= 200, q <= 1000")
    print(f"  Total modes in search space: ~100,000")
    
    # Use experimental uncertainty as tolerance
    particles = {
        'W': (M_W_OBS, M_W_ERR),
        'Z': (M_Z_OBS, M_Z_ERR),
        'H': (M_H_OBS, M_H_ERR),
    }
    
    results = {}
    for name, (m_obs, m_err) in particles.items():
        # Count at 1-sigma
        matches_1s = count_modes_near_mass(m_obs, m_err)
        # Count at 3-sigma
        matches_3s = count_modes_near_mass(m_obs, 3*m_err)
        # Count at 0.2% (the claimed precision)
        tol_02 = 0.002 * m_obs
        matches_02 = count_modes_near_mass(m_obs, tol_02)
        
        pred = PREDICTIONS[name]
        is_in_list = any(
            (p == pred['p'] and q == pred['q']) or 
            (q == pred['p'] and p == pred['q'])
            for p, q, m in matches_02
        )
        
        print(f"\n  {name} boson (m = {m_obs} +/- {m_err} GeV):")
        print(f"    Within 1-sigma ({m_err:.4f} GeV): {len(matches_1s)} modes")
        print(f"    Within 3-sigma ({3*m_err:.4f} GeV): {len(matches_3s)} modes")
        print(f"    Within 0.2%    ({tol_02:.3f} GeV):  {len(matches_02)} modes")
        print(f"    TRXT prediction ({pred['p']},{pred['q']}) in 0.2% list: {is_in_list}")
        
        if len(matches_1s) <= 20:
            print(f"    1-sigma matches: {[(p,q,f'{m:.3f}') for p,q,m in matches_1s[:10]]}")
        
        results[name] = {
            'n_1sigma': len(matches_1s),
            'n_3sigma': len(matches_3s),
            'n_02pct': len(matches_02),
        }
    
    return results


# ====================================================================
# TEST 2: Sector-Constrained Uniqueness
# ====================================================================
def test_sector_constrained():
    """Test 2: Given fixed sector p, is q uniquely determined?"""
    print("\n" + "=" * 70)
    print("TEST 2: Sector-Constrained Uniqueness")
    print("=" * 70)
    print("  IF the sector p is topologically determined, is q unique?")
    
    results = {}
    for name, rule in SECTOR_RULES.items():
        p = rule['p']
        obs = {'W': (M_W_OBS, M_W_ERR), 'Z': (M_Z_OBS, M_Z_ERR), 
               'H': (M_H_OBS, M_H_ERR)}
        m_obs, m_err = obs[name]
        
        q_unique = find_q_for_mass(p, m_obs)
        m_pred = mass_formula(p, q_unique) if q_unique else None
        dev = abs(m_pred - m_obs) if m_pred else float('inf')
        dev_sigma = dev / m_err if m_err > 0 else float('inf')
        
        # Check if this q is robust: how much can m_obs vary before q changes?
        if q_unique:
            m_for_q_minus = mass_formula(p, q_unique - 1) if q_unique > 1 else float('inf')
            m_for_q_plus = mass_formula(p, q_unique + 1)
            # q changes when m_obs crosses the midpoint between adjacent modes
            boundary_lo = (m_pred + m_for_q_minus) / 2 if q_unique > 1 else 0
            boundary_hi = (m_pred + m_for_q_plus) / 2
            plateau_width = boundary_hi - boundary_lo
            plateau_sigma = plateau_width / m_err
        else:
            plateau_width = 0
            plateau_sigma = 0
        
        print(f"\n  {name} boson: p = {p} ({rule['reason']})")
        print(f"    q(unique) = {q_unique}")
        print(f"    M(p,q) = {m_pred:.4f} GeV vs {m_obs:.4f} +/- {m_err:.4f} GeV")
        print(f"    Deviation = {dev:.4f} GeV = {dev_sigma:.2f} sigma")
        print(f"    Robustness plateau: {plateau_width:.3f} GeV = {plateau_sigma:.1f} sigma")
        
        results[name] = {
            'p': p, 'q': q_unique, 'm_pred': m_pred,
            'dev_GeV': dev, 'dev_sigma': dev_sigma,
            'plateau_GeV': plateau_width, 'plateau_sigma': plateau_sigma,
        }
    
    return results


# ====================================================================
# TEST 3: Monte Carlo — Random M* Test
# ====================================================================
def test_monte_carlo(n_trials=100000, p_max_search=20, q_max_search=200):
    """
    Test 3: If M* were drawn from a uniform range, what fraction of 
    M* values simultaneously match W, Z, H to the observed precision?
    
    This tests whether the TRXT match is "surprising" or expected
    from any random energy scale.
    """
    print("\n" + "=" * 70)
    print(f"TEST 3: Monte Carlo Random M* (n = {n_trials:,})")
    print("=" * 70)
    print(f"  For each random M* in [50, 1000] GeV:")
    print(f"  Find best (p,q) match for each of W, Z, H")
    print(f"  Count how often ALL THREE match within 0.2%")
    
    rng = np.random.default_rng(42)
    m_star_samples = rng.uniform(50, 1000, n_trials)
    
    targets = [
        ('W', M_W_OBS, 0.002 * M_W_OBS),  # 0.2% tolerance
        ('Z', M_Z_OBS, 0.002 * M_Z_OBS),
        ('H', M_H_OBS, 0.002 * M_H_OBS),
    ]
    
    # Also test tighter thresholds
    thresholds = [0.01, 0.005, 0.002, 0.001, 0.0005]
    
    results = {f'{t*100:.2f}%': 0 for t in thresholds}
    best_per_trial = []
    
    for m_star in m_star_samples:
        # For each particle, find the best (p,q) match
        worst_frac = 0
        for name, m_obs, _ in targets:
            best_dev = float('inf')
            for p in range(1, p_max_search + 1):
                q = find_q_for_mass(p, m_obs, m_star)
                if q is None or q < 1 or q > q_max_search:
                    continue
                m_pred = mass_formula(p, q, m_star)
                dev = abs(m_pred - m_obs) / m_obs
                if dev < best_dev:
                    best_dev = dev
            if best_dev == float('inf'):
                worst_frac = float('inf')
                break
            worst_frac = max(worst_frac, best_dev)
        
        # Check all thresholds
        for t in thresholds:
            if worst_frac < t:
                results[f'{t*100:.2f}%'] += 1
        
        best_per_trial.append(worst_frac)
    
    print(f"\n  Results (fraction of trials matching ALL THREE particles):")
    for t_str, count in results.items():
        frac = count / n_trials
        print(f"    Within {t_str}: {count:,}/{n_trials:,} = {frac:.6f} "
              f"({frac*100:.4f}%)")
    
    # p-value for the actual TRXT M*
    actual_worst = 0
    for name, m_obs, _ in targets:
        pred = PREDICTIONS[name]
        m_pred = pred['mass']
        dev = abs(m_pred - m_obs) / m_obs
        actual_worst = max(actual_worst, dev)
    
    n_better = sum(1 for b in best_per_trial if b < actual_worst)
    p_value = n_better / n_trials
    
    print(f"\n  TRXT M* = {M_STAR} GeV: worst deviation = {actual_worst*100:.4f}%")
    print(f"  p-value (fraction of random M* doing better) = {p_value:.6f}")
    print(f"  Equivalent sigma = ", end="")
    from scipy.stats import norm
    if p_value > 0:
        sigma_equiv = norm.ppf(1 - p_value)
        print(f"{sigma_equiv:.2f}")
    else:
        print(f"> {norm.ppf(1-1/n_trials):.1f} (no trial matched)")
    
    return {
        'n_trials': n_trials,
        'thresholds': {k: v/n_trials for k, v in results.items()},
        'actual_worst_dev': actual_worst,
        'p_value': p_value,
    }


# ====================================================================
# TEST 4: Constrained Monte Carlo (Fixed Sector p)
# ====================================================================
def test_constrained_mc(n_trials=100000):
    """
    Test 4: Same as Test 3, but now sectors are FIXED:
    p(W)=5, p(Z)=8, p(H)=5.
    Only q varies. How often does a random M* match all three?
    """
    print("\n" + "=" * 70)
    print(f"TEST 4: Constrained Monte Carlo (fixed sectors, n = {n_trials:,})")
    print("=" * 70)
    print(f"  Sectors fixed: p(W)=5, p(Z)=8, p(H)=5")
    print(f"  For each random M* in [50, 1000] GeV:")
    print(f"  q is uniquely determined for each particle")
    
    rng = np.random.default_rng(42)
    m_star_samples = rng.uniform(50, 1000, n_trials)
    
    targets = [
        ('W', 5, M_W_OBS),
        ('Z', 8, M_Z_OBS),
        ('H', 5, M_H_OBS),
    ]
    
    thresholds = [0.01, 0.005, 0.002, 0.001, 0.0005, 0.0002]
    results = {f'{t*100:.2f}%': 0 for t in thresholds}
    worst_devs = []
    
    for m_star in m_star_samples:
        worst_frac = 0
        valid = True
        for name, p, m_obs in targets:
            q = find_q_for_mass(p, m_obs, m_star)
            if q is None or q < 1:
                valid = False
                break
            m_pred = mass_formula(p, q, m_star)
            dev = abs(m_pred - m_obs) / m_obs
            worst_frac = max(worst_frac, dev)
        
        if not valid:
            worst_frac = float('inf')
        
        for t in thresholds:
            if worst_frac < t:
                results[f'{t*100:.2f}%'] += 1
        
        worst_devs.append(worst_frac)
    
    print(f"\n  Results:")
    for t_str, count in results.items():
        frac = count / n_trials
        print(f"    Within {t_str}: {count:,}/{n_trials:,} = {frac:.6f}")
    
    # p-value for actual TRXT
    actual_worst = 0
    for name, p, m_obs in targets:
        q = PREDICTIONS[name]['q']
        m_pred = mass_formula(p, q)
        dev = abs(m_pred - m_obs) / m_obs
        actual_worst = max(actual_worst, dev)
    
    n_better = sum(1 for d in worst_devs if d < actual_worst)
    p_value = n_better / n_trials
    
    from scipy.stats import norm
    
    print(f"\n  TRXT actual worst deviation = {actual_worst*100:.4f}%")
    print(f"  p-value (sector-constrained) = {p_value:.6f}")
    if p_value > 0:
        sigma_equiv = norm.ppf(1 - p_value)
        print(f"  Equivalent sigma = {sigma_equiv:.2f}")
    else:
        print(f"  Equivalent sigma > {norm.ppf(1-1/n_trials):.1f}")
    
    return {
        'n_trials': n_trials,
        'thresholds': {k: v/n_trials for k, v in results.items()},
        'actual_worst_dev': actual_worst,
        'p_value': p_value,
    }


# ====================================================================
# TEST 5: Simultaneous Sigma Assessment
# ====================================================================
def test_combined_significance():
    """
    Test 5: What is the combined chi-squared significance
    of the 3-particle match with 1 free parameter (M*)?
    """
    print("\n" + "=" * 70)
    print("TEST 5: Combined chi-squared Significance")
    print("=" * 70)
    
    # 3 measurements, 1 free parameter (M*) → 2 d.o.f.
    particles = {
        'W': (M_W_OBS, M_W_ERR, 5, 50),
        'Z': (M_Z_OBS, M_Z_ERR, 8, 8),
        'H': (M_H_OBS, M_H_ERR, 5, 7),
    }
    
    chi2 = 0
    print(f"\n  {'Particle':<10} {'Observed':>12} {'Predicted':>12} {'sigma':>10}")
    print(f"  {'-'*46}")
    for name, (m_obs, m_err, p, q) in particles.items():
        m_pred = mass_formula(p, q)
        dev_sigma = (m_pred - m_obs) / m_err
        chi2 += dev_sigma**2
        print(f"  {name:<10} {m_obs:>12.4f} {m_pred:>12.4f} {dev_sigma:>+10.2f}")
    
    n_dof = 2  # 3 measurements - 1 parameter (M*)
    chi2_per_dof = chi2 / n_dof
    
    from scipy.stats import chi2 as chi2_dist
    p_value = 1 - chi2_dist.cdf(chi2, n_dof)
    
    print(f"\n  chi^2 = {chi2:.2f}, n_dof = {n_dof}")
    print(f"  chi^2/dof = {chi2_per_dof:.2f}")
    print(f"  p-value = {p_value:.4f}")
    print(f"  (p > 0.05 means the fit is acceptable)")
    
    # Caveat: sector assignments double as free parameters!
    print(f"\n  CAVEAT: Sector assignments (p=5,8,5) are treated as fixed.")
    print(f"  If sectors are free parameters, n_dof = 0 (overfitting).")
    print(f"  The chi^2 test is only valid IF sectors are independently derived.")
    
    return {
        'chi2': chi2,
        'n_dof': n_dof,
        'chi2_per_dof': chi2_per_dof,
        'p_value': p_value,
    }


# ====================================================================
# MAIN
# ====================================================================
def main():
    print("=" * 70)
    print("C3 STATISTICAL ANALYSIS: Are TRXT Mass Predictions Remarkable?")
    print("=" * 70)
    print(f"\n  Mass formula: E(p,q) = M*(1/p + 1/q), M* = {M_STAR} GeV")
    print(f"  Predictions: W(5,50)={PREDICTIONS['W']['mass']:.2f}, "
          f"Z(8,8)={PREDICTIONS['Z']['mass']:.2f}, "
          f"H(5,7)={PREDICTIONS['H']['mass']:.2f} GeV")
    
    t1 = test_mode_counting()
    t2 = test_sector_constrained()
    t3 = test_monte_carlo(n_trials=100000)
    t4 = test_constrained_mc(n_trials=100000)
    t5 = test_combined_significance()
    
    # ================================================================
    # OVERALL VERDICT
    # ================================================================
    print("\n" + "=" * 70)
    print("OVERALL VERDICT")
    print("=" * 70)
    
    print(f"""
  TEST 1 (Mode Counting):
    Finding a match for ANY SINGLE particle is not remarkable due to
    mode density. The key question is simultaneous matching.

  TEST 2 (Sector Constrained):
    Given fixed sectors, q is uniquely determined with deviations:
    W: {t2['W']['dev_sigma']:.2f}sigma, Z: {t2['Z']['dev_sigma']:.2f}sigma, H: {t2['H']['dev_sigma']:.2f}sigma
    Robustness plateaus are wide (>{min(t2[n]['plateau_sigma'] for n in ['W','Z','H']):.0f} sigma).

  TEST 3 (MC Random M*):
    p-value for random M* matching all 3: {t3['p_value']:.6f}
    This is {'significant (p<0.05)' if t3['p_value'] < 0.05 else 'NOT significant'}.

  TEST 4 (MC Constrained):
    p-value with fixed sectors: {t4['p_value']:.6f}
    This is {'highly significant' if t4['p_value'] < 0.01 else 'significant' if t4['p_value'] < 0.05 else 'NOT significant'}.

  TEST 5 (chi^2):
    chi^2/dof = {t5['chi2_per_dof']:.2f}, p = {t5['p_value']:.4f}
    {'Good fit' if t5['p_value'] > 0.05 else 'Poor fit'} (if sectors treated as fixed).

  HONEST CONCLUSION:
    - The mass formula with M* = 365.24 GeV produces remarkably good matches.
    - The STATISTICAL significance depends critically on whether sector 
      assignments (p=5,8) are INDEPENDENTLY derived or fit to data.
    - IF sectors are derived: the 3-particle match with 1 parameter is impressive.
    - IF sectors are chosen to fit: the framework is over-parameterized (3 params for 3 data).
    - CURRENT STATUS: Sector rules are MOTIVATED by homotopy hypothesis but
      NOT DERIVED from first principles. This is the key open problem.
""")
    
    # Save artifact
    artifact = {
        "evidence_id": "C3-STATS-2026-03",
        "version": "v1",
        "test1_mode_counting": t1,
        "test2_sector_constrained": {k: {kk: (float(vv) if isinstance(vv, (int,float)) else vv)
                                          for kk, vv in v.items()} 
                                     for k, v in t2.items()},
        "test3_mc_random": t3,
        "test4_mc_constrained": t4,
        "test5_chi2": t5,
    }
    return artifact


if __name__ == "__main__":
    t0 = time.time()
    artifact = main()
    t1 = time.time()
    artifact["runtime_s"] = round(t1 - t0, 2)
    
    artifact_dir = os.path.join(os.path.dirname(__file__), "..", "artifacts")
    os.makedirs(artifact_dir, exist_ok=True)
    out_path = os.path.join(artifact_dir, "C3_mass_statistics_result.json")
    with open(out_path, "w") as f:
        json.dump(artifact, f, indent=2, default=str)
    print(f"\nArtifact saved: {out_path}")
