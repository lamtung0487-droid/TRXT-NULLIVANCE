"""
TRXT V17: DEFINITIVE DARK TOWER EXPERIMENT
===========================================
Compliance: Master Protocol V2.0
Data: CRESST-III + XENON1T Official Limits

This is the FINAL test to determine if TRXT Dark Matter candidates survive.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from TRXT_Analysis_Engine import TRXTAnalyzer

def load_official_limits():
    """Load official CRESST-III + XENON1T limits from JSON."""
    data_file = Path(__file__).parent / "data" / "dm_exclusion_limits.json"
    
    with open(data_file, 'r') as f:
        data = json.load(f)
    
    # Use combined envelope
    mass = np.array(data["combined_envelope"]["mass_gev"])
    limit = np.array(data["combined_envelope"]["limit_cm2"])
    
    return mass, limit, data


def calculate_trxt_cross_section(mass_gev, m_star, suppression_power=4):
    """
    TRXT Topology Suppression Model.
    σ = g0 * (m / M*)^power
    """
    g0 = 1e-39  # Base weak-scale coupling
    return g0 * (mass_gev / m_star)**suppression_power


def main():
    print("=" * 70)
    print("TRXT V17: DEFINITIVE DARK TOWER EXPERIMENT")
    print("=" * 70)
    print("Data: CRESST-III (arXiv:1905.07335) + XENON1T (arXiv:1805.12562)")
    print()
    
    # Initialize
    engine = TRXTAnalyzer()
    mass_lim, cs_lim, data_info = load_official_limits()
    
    print(f"[DATA] Source: {data_info['source']}")
    print(f"[DATA] Access Date: {data_info['access_date']}")
    print(f"[DATA] Limit Points: {len(mass_lim)}")
    print()
    
    # TRXT Dark Tower Candidates (Full Spectrum)
    print("[CANDIDATES] TRXT Dark Tower Hierarchy")
    print("-" * 70)
    
    candidates = []
    
    # Generate all candidates from (16,16) down to (512,512)
    for k in [16, 32, 64, 128, 256, 512]:
        mass = engine.predict_mass(k, k)
        label = f"({k},{k})"
        candidates.append((label, mass))
        print(f"  {label}: {mass:.4f} GeV")
    
    print()
    
    # Interpolate limit function
    f_limit = interp1d(mass_lim, cs_lim, kind='linear', 
                       bounds_error=False, fill_value=(1e-30, 1e-45))
    
    # Test each candidate
    print("[ANALYSIS] Testing candidates against official limits")
    print("-" * 70)
    print(f"{'Mode':<12} | {'Mass [GeV]':<12} | {'σ_pred [cm²]':<15} | {'σ_limit [cm²]':<15} | {'Verdict'}")
    print("-" * 70)
    
    results = []
    safe_count = 0
    excluded_count = 0
    
    for label, mass in candidates:
        sigma_pred = calculate_trxt_cross_section(mass, engine.M_STAR, 4)
        sigma_limit = float(f_limit(mass))
        
        if sigma_pred < sigma_limit:
            verdict = "✅ SAFE"
            safe_count += 1
        else:
            verdict = "❌ EXCLUDED"
            excluded_count += 1
            
        results.append((label, mass, sigma_pred, sigma_limit, verdict))
        print(f"{label:<12} | {mass:<12.4f} | {sigma_pred:<15.2e} | {sigma_limit:<15.2e} | {verdict}")
    
    print("-" * 70)
    print()
    
    # Summary
    print("[SUMMARY]")
    print(f"  Total Candidates: {len(candidates)}")
    print(f"  SAFE: {safe_count}")
    print(f"  EXCLUDED: {excluded_count}")
    print()
    
    # Verdict
    print("=" * 70)
    print("[FINAL VERDICT ON DARK TOWER]")
    print("=" * 70)
    
    if excluded_count == 0:
        print("  ✅ ALL candidates SAFE. TRXT Dark Tower is VIABLE.")
    elif safe_count == 0:
        print("  ❌ ALL candidates EXCLUDED. TRXT Dark Tower is FALSIFIED.")
    else:
        print(f"  ⚠️  PARTIAL: {safe_count} candidates safe, {excluded_count} excluded.")
        safe_masses = [m for l, m, sp, sl, v in results if "SAFE" in v]
        print(f"  SURVIVING MODES: {[f'{m:.2f} GeV' for m in safe_masses]}")
        
        # Check if surviving modes are below some threshold
        if all(m < 6.0 for m in safe_masses):
            print("  → Only modes < 6 GeV survive. 'Low Mass Sanctuary' confirmed.")
        elif all(m < 12.0 for m in safe_masses):
            print("  → Only modes < 12 GeV survive. Intermediate zone excluded.")
    
    # Plot
    plt.figure(figsize=(12, 8))
    
    # Limit curve
    x_plot = np.logspace(-1, 3.5, 500)
    y_plot = f_limit(x_plot)
    plt.loglog(x_plot, y_plot, 'k-', linewidth=2, label='90% CL Limit (CRESST+XENON)')
    plt.fill_between(x_plot, y_plot, 1e-30, color='gray', alpha=0.3, label='Excluded Region')
    
    # Plot candidates
    for label, mass, sigma_pred, sigma_limit, verdict in results:
        if "SAFE" in verdict:
            plt.plot(mass, sigma_pred, 'g^', markersize=14, markeredgecolor='k', 
                     markeredgewidth=2, zorder=5)
        else:
            plt.plot(mass, sigma_pred, 'rx', markersize=14, markeredgewidth=3, zorder=5)
        plt.text(mass * 1.1, sigma_pred * 1.5, f"{label}\n{mass:.1f} GeV", 
                 fontsize=8, ha='left')
    
    plt.xlabel("Dark Matter Mass [GeV]", fontsize=12)
    plt.ylabel("SI Cross-Section [cm²]", fontsize=12)
    plt.title("TRXT V17: Definitive Dark Tower Test\n(CRESST-III + XENON1T)", fontsize=14)
    plt.xlim(0.1, 1000)
    plt.ylim(1e-50, 1e-32)
    plt.legend(loc='upper right')
    plt.grid(True, which='both', alpha=0.3)
    
    output_file = Path(__file__).parent.parent / "results" / "v17_dark_tower_final.png"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"\n[OUTPUT] Plot saved: {output_file}")


if __name__ == "__main__":
    main()
