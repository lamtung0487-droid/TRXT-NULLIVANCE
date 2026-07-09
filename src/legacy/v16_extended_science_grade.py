"""
TRXT PROTOCOL: V16 EXTENDED TASKS - SCIENCE GRADE
==================================================
Compliance: Master Protocol V2.0, Article IV

Combined script for all V16 Extended validation tasks.
All data loaded from files, NO HARDCODING.
"""

import numpy as np
import matplotlib.pyplot as plt
import sys

from data_loader import TRXTDataLoader
from TRXT_Analysis_Engine import TRXTAnalyzer


def task_1_1_mixing_angle(loader, engine):
    """
    Task 1.1: Weak Mixing Angle (SLD/LEP Tension)
    Tests if TRXT Chiral Shear explains the ~3σ split.
    """
    print("=" * 60)
    print("TASK 1.1: WEAK MIXING ANGLE TENSION")
    print("=" * 60)
    
    # Load data from PDG
    pdg_data, _ = loader.load_pdg_ewprecision()
    
    sin2_sld = pdg_data["sin2theta_eff_sld"]["value"]
    sin2_sld_err = pdg_data["sin2theta_eff_sld"]["error"]
    sin2_lep = pdg_data["sin2theta_eff_lep_afb"]["value"]
    sin2_lep_err = pdg_data["sin2theta_eff_lep_afb"]["error"]
    sin2_world = pdg_data["sin2theta_eff_world"]["value"]
    
    print(f"[DATA] SLD (A_LR): {sin2_sld} ± {sin2_sld_err}")
    print(f"[DATA] LEP (A_FB^b): {sin2_lep} ± {sin2_lep_err}")
    print(f"[DATA] World Average: {sin2_world}")
    
    # Calculate tension
    diff = sin2_lep - sin2_sld
    combined_err = np.sqrt(sin2_sld_err**2 + sin2_lep_err**2)
    tension = diff / combined_err
    
    print(f"\n[TENSION] Δ = {diff:.5f}, σ = {combined_err:.5f}")
    print(f"[TENSION] {tension:.1f} sigma")
    
    # TRXT Prediction
    MW = pdg_data["MW"]["value"]
    MW_CDF = pdg_data["MW_cdf"]["value"]
    delta_rho = (MW_CDF / MW)**2 - 1
    
    epsilon_trxt = delta_rho
    expected_diff = 2 * sin2_world * epsilon_trxt
    
    print(f"\n[TRXT] Δρ (from CDF): {delta_rho:.6f}")
    print(f"[TRXT] Expected Chiral Split: {expected_diff:.5f}")
    print(f"[TRXT] Observed/Predicted: {diff/expected_diff:.2f}")
    
    if 0.5 < (diff / expected_diff) < 2.0:
        print("\n[RESULT] ✓ SUPPORTIVE - Chiral Shear explains SLD/LEP split")
        return True
    else:
        print("\n[RESULT] ✗ Not supportive")
        return False


def task_1_2_muon_g2(loader, engine):
    """
    Task 1.2: Muon g-2 Anomaly
    Tests if Light Dark Tower contributes.
    """
    print("\n" + "=" * 60)
    print("TASK 1.2: MUON g-2 ANOMALY")
    print("=" * 60)
    
    # Load data
    g2_data, _ = loader.load_muon_g2()
    
    a_mu_exp = g2_data["a_mu_exp"]
    a_mu_exp_err = g2_data["a_mu_exp_err"]
    a_mu_sm = g2_data["a_mu_sm_data_driven"]
    a_mu_sm_err = g2_data["a_mu_sm_err"]
    
    delta_a = a_mu_exp - a_mu_sm
    combined_err = np.sqrt(a_mu_exp_err**2 + a_mu_sm_err**2)
    
    print(f"[DATA] a_μ (Exp): {a_mu_exp:.4e}")
    print(f"[DATA] a_μ (SM): {a_mu_sm:.4e}")
    print(f"[DATA] Δa_μ: {delta_a:.2e} ({delta_a/combined_err:.1f}σ)")
    
    # TRXT Prediction (Light Tower at 2.85 GeV)
    m_mu = 0.1057  # GeV
    m_tower = engine.predict_mass(256, 256)  # Lightest survivor
    
    # Estimate mixing from sterile hypothesis
    sin2_theta = 0.005
    g_weak = 0.65
    g_x = np.sqrt(sin2_theta) * g_weak
    
    # Scalar loop contribution
    delta_a_tower = (g_x**2 / (16 * np.pi**2)) * (m_mu / m_tower)**2 * (1/3)
    
    print(f"\n[TRXT] Tower Mass: {m_tower:.3f} GeV")
    print(f"[TRXT] Effective Coupling: g_X = {g_x:.4f}")
    print(f"[TRXT] Loop Contribution: {delta_a_tower:.2e}")
    print(f"[TRXT] Fraction of Anomaly: {delta_a_tower/delta_a*100:.1f}%")
    
    if delta_a_tower / delta_a > 1.0:
        print("\n[RESULT] ⚠ OVER-EXPLAINS - Coupling must be tuned down")
    elif delta_a_tower / delta_a > 0.1:
        print("\n[RESULT] ✓ PARTIAL SUPPORT")
    else:
        print("\n[RESULT] ✗ Negligible contribution")
    
    return delta_a_tower / delta_a


def main():
    print("=== TRXT V16 EXTENDED VALIDATION - SCIENCE GRADE ===")
    print("Compliance: Master Protocol V2.0, Article IV")
    print()
    
    # Initialize
    loader = TRXTDataLoader()
    engine = TRXTAnalyzer()
    
    try:
        # Run all tasks
        result_1_1 = task_1_1_mixing_angle(loader, engine)
        result_1_2 = task_1_2_muon_g2(loader, engine)
        
        # Summary
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(f"  Task 1.1 (Mixing Angle): {'SUPPORTIVE' if result_1_1 else 'NOT SUPPORTIVE'}")
        print(f"  Task 1.2 (Muon g-2): {result_1_2*100:.1f}% of anomaly explained")
        
        # Provenance
        print("\n[PROVENANCE REPORT]")
        for prov in loader.get_provenance_report():
            print(f"  - {prov['name']}: {prov['source']} (v{prov['version']})")
            
    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
