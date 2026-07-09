"""
TRXT PROTOCOL: TASK C (DARK TOWER) - SCIENCE GRADE
===================================================
Compliance: Master Protocol V2.0, Article IV

This script loads REAL exclusion limits from data files.
NO HARDCODED DATA.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import json
import sys

from data_loader import TRXTDataLoader, DATA_DIR
from TRXT_Analysis_Engine import TRXTAnalyzer


def calculate_suppressed_coupling(mass, m_star, suppression_power=4):
    """
    Topology Suppression Rule.
    Cross-section scales with (mass/M*)^power.
    
    power=4 corresponds to dimension-6 operators.
    """
    g0 = 1e-39  # Base coupling (Weak scale)
    return g0 * (mass / m_star)**suppression_power


def main():
    print("=== TRXT PROTOCOL: TASK C (DARK TOWER) - SCIENCE GRADE ===")
    print("Compliance: Master Protocol V2.0, Article IV")
    print()
    
    # Initialize
    loader = TRXTDataLoader()
    engine = TRXTAnalyzer()
    
    # Load DM Exclusion Limits
    try:
        dm_data, dm_prov = loader.load_dm_exclusion_limits()
        mass_lim = np.array(dm_data["mass_gev"])
        cs_lim = np.array(dm_data["limit_cm2"])
        experiments = dm_data.get("experiments", ["Unknown"])
        
        print(f"[DATA] DM Limits: {len(mass_lim)} points")
        print(f"[DATA] Experiments: {', '.join(experiments)}")
        
        if "WARNING" in dm_data:
            print(f"[WARNING] {dm_data['WARNING']}")
            
    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)
    
    # Generate TRXT Candidates
    print()
    print("[CANDIDATES] Dark Tower Hierarchy (from predict_mass):")
    candidates = []
    
    # (32,32) = M*/16
    m1 = engine.predict_mass(32, 32)
    candidates.append(("(32,32)", m1))
    
    # (64,64) = M*/32
    m2 = engine.predict_mass(64, 64)
    candidates.append(("(64,64)", m2))
    
    # (128,128) = M*/64
    m3 = engine.predict_mass(128, 128)
    candidates.append(("(128,128)", m3))
    
    # (256,256) = M*/128
    m4 = engine.predict_mass(256, 256)
    candidates.append(("(256,256)", m4))
    
    for label, mass in candidates:
        print(f"  {label}: {mass:.4f} GeV")
    
    # Interpolate limit function
    f_limit = interp1d(mass_lim, cs_lim, kind='linear', fill_value="extrapolate")
    
    # Analysis
    print()
    print("[ANALYSIS] Checking candidates against limits...")
    print()
    print(f"{'Candidate':<12} | {'Mass [GeV]':<12} | {'Pred σ [cm²]':<15} | {'Limit [cm²]':<15} | {'Status'}")
    print("-" * 75)
    
    results = []
    for label, mass in candidates:
        cs_pred = calculate_suppressed_coupling(mass, engine.M_STAR)
        limit_val = float(f_limit(mass))
        status = "SAFE" if cs_pred < limit_val else "EXCLUDED"
        results.append((label, mass, cs_pred, limit_val, status))
        print(f"{label:<12} | {mass:<12.4f} | {cs_pred:<15.2e} | {limit_val:<15.2e} | {status}")
    
    # Provenance Report
    print()
    print("[PROVENANCE REPORT]")
    for prov in loader.get_provenance_report():
        print(f"  - {prov['name']}: {prov['source']} (v{prov['version']})")
    
    # Plot
    plt.figure(figsize=(10, 7))
    
    # Exclusion curve
    x_plot = np.logspace(-1, 3, 200)
    y_plot = f_limit(x_plot)
    plt.plot(x_plot, y_plot, 'k-', linewidth=2, label='Exclusion Limit')
    plt.fill_between(x_plot, y_plot, 1e-30, color='gray', alpha=0.3, label='Excluded Region')
    
    # Plot candidates
    for label, mass, cs_pred, limit_val, status in results:
        color = 'g^' if status == "SAFE" else 'rx'
        plt.plot(mass, cs_pred, color, markersize=12, markeredgecolor='k')
        plt.text(mass * 1.1, cs_pred, f"{label}\n[{status}]", fontsize=9)
    
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel("Dark Matter Mass [GeV]")
    plt.ylabel("Cross Section [cm²]")
    plt.title("Task C (Science Grade): Dark Tower Exclusion Check")
    plt.grid(True, which="both", ls="-", alpha=0.2)
    plt.ylim(1e-48, 1e-35)
    plt.xlim(0.5, 100)
    plt.legend()
    
    output_plot = "trxt_task_c_science_grade.png"
    plt.savefig(output_plot)
    print(f"\n[OUTPUT] Plot saved to: {output_plot}")


if __name__ == "__main__":
    main()
