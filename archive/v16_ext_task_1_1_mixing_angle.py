import numpy as np
from TRXT_Analysis_Engine import TRXTAnalyzer

def main():
    print("=== TRXT V16 EXTENDED: TASK 1.1 (MIXING ANGLE TENSION) ===")
    engine = TRXTAnalyzer()
    
    # ===== ELECTROWEAK PRECISION DATA =====
    # sin²θ_eff (Effective Weak Mixing Angle)
    # Two most precise measurements disagree by ~3 sigma:
    
    # SLD (Polarized e+e- at Z pole): Left-Right Asymmetry
    sin2_sld = 0.23098
    sin2_sld_err = 0.00026
    
    # LEP (A_FB^b): Forward-Backward Asymmetry in b-quarks
    sin2_lep_afb = 0.23221
    sin2_lep_afb_err = 0.00029
    
    # World Average (PDG)
    sin2_world = 0.23153
    sin2_world_err = 0.00016
    
    print("[EXPERIMENTAL DATA]")
    print(f"  SLD (A_LR): {sin2_sld} ± {sin2_sld_err}")
    print(f"  LEP (A_FB^b): {sin2_lep_afb} ± {sin2_lep_afb_err}")
    print(f"  World Average: {sin2_world} ± {sin2_world_err}")
    
    # Calculate tension
    diff = sin2_lep_afb - sin2_sld
    combined_err = np.sqrt(sin2_sld_err**2 + sin2_lep_afb_err**2)
    tension_sigma = diff / combined_err
    
    print(f"\n[TENSION]")
    print(f"  Difference (LEP - SLD): {diff:.5f}")
    print(f"  Combined Error: {combined_err:.5f}")
    print(f"  Tension: {tension_sigma:.1f} sigma")
    
    # ===== TRXT HYPOTHESIS =====
    # The Vacuum Shear affects Left and Right currents differently due to chirality.
    # Hypothesis: sin²θ_eff = sin²θ_0 * (1 + ε_chiral)
    # where ε_chiral ~ ± Δρ for L vs R polarizations.
    
    # Get TRXT shear from CDF-fit
    delta_rho_cdf = 0.001892  # From V16 Task 1
    
    print(f"\n[TRXT HYPOTHESIS: CHIRAL SHEAR]")
    print(f"  Vacuum Shear Δρ (CDF): {delta_rho_cdf:.6f}")
    
    # Model: SLD (Left-polarized) sees sin²θ_L = sin²θ_0 * (1 - ε)
    #        LEP A_FB (unpolarized but b-quark dependent) sees sin²θ_R = sin²θ_0 * (1 + ε)
    # The difference would be: Δsin²θ ~ 2 * sin²θ_0 * ε
    
    # For TRXT, ε ~ Δρ / (some geometric factor)
    # Let's estimate: if ε ~ Δρ, then expected difference:
    epsilon_trxt = delta_rho_cdf
    sin2_base = sin2_world
    expected_diff = 2 * sin2_base * epsilon_trxt
    
    print(f"  Expected Chiral Splitting: 2 * sin²θ * ε = {expected_diff:.5f}")
    print(f"  Observed Splitting: {diff:.5f}")
    print(f"  Ratio (Observed/Predicted): {diff / expected_diff:.2f}")
    
    # Interpretation
    print(f"\n[INTERPRETATION]")
    if 0.5 < (diff / expected_diff) < 2.0:
        print("  ✓ The TRXT Chiral Shear (~Δρ) can QUALITATIVELY explain the SLD/LEP split!")
        print("  ✓ This is a potential 'Smoking Gun' independent of the W-mass.")
        print("  STATUS: SUPPORTIVE (requires detailed EW fit)")
    elif (diff / expected_diff) > 0.1:
        print("  ~ TRXT predicts the correct ORDER OF MAGNITUDE for the split.")
        print("  STATUS: SUGGESTIVE")
    else:
        print("  ✗ TRXT prediction is too small/large to explain the split.")
        print("  STATUS: NO SUPPORT")

if __name__ == "__main__":
    main()
