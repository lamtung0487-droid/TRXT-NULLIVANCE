import numpy as np
from TRXT_Analysis_Engine import TRXTAnalyzer

def main():
    print("=== TRXT V16 EXTENDED: TASK 1.2 (MUON g-2) ===")
    engine = TRXTAnalyzer()
    
    # ===== EXPERIMENTAL DATA =====
    # Muon Anomalous Magnetic Moment
    # a_mu = (g-2)/2
    
    # Fermilab 2023 + BNL Combined
    a_mu_exp = 116592059e-11  # (116592059 ± 22) × 10^-11
    a_mu_exp_err = 22e-11
    
    # SM Prediction (White Paper 2020 + Lattice updates)
    # Note: Lattice QCD results are closing the gap
    # Using "Data-Driven" HVP: ~251 × 10^-11 discrepancy
    a_mu_sm = 116591810e-11
    a_mu_sm_err = 43e-11
    
    delta_a_mu = a_mu_exp - a_mu_sm
    combined_err = np.sqrt(a_mu_exp_err**2 + a_mu_sm_err**2)
    
    print("[EXPERIMENTAL DATA (Fermilab + BNL)]")
    print(f"  a_mu (Exp): {a_mu_exp:.4e}")
    print(f"  a_mu (SM): {a_mu_sm:.4e}")
    print(f"  Δa_mu: {delta_a_mu:.2e} ({delta_a_mu/combined_err:.1f}σ)")
    
    # ===== TRXT HYPOTHESIS: GHOST Z' LOOP =====
    # New scalar/vector contribution to g-2:
    # Δa_mu ~ (m_mu / M_X)^2 * g_X^2 / (16π²)
    
    m_mu = 0.1057  # GeV
    M_ghost = engine.predict_mass(16, 16)  # 45.66 GeV
    
    # For invisible Ghost: coupling to muons ~ 0 (by hypothesis)
    # BUT: if there's any residual mixing...
    # Let's parametrize: g_X = sin(theta) * g_SM
    # where theta is the sterile mixing angle
    
    sin2_theta = 0.005  # From V16 Task 2
    g_weak = 0.65  # Approximate weak coupling
    g_x = np.sqrt(sin2_theta) * g_weak
    
    # Scalar loop contribution (order of magnitude)
    # Δa ~ (g^2 / 16π²) * (m_mu / M)^2 * F(m_mu/M)
    # For heavy M >> m_mu, F ~ 1/3
    delta_a_ghost = (g_x**2 / (16 * np.pi**2)) * (m_mu / M_ghost)**2 * (1/3)
    
    print(f"\n[TRXT GHOST Z' LOOP CALCULATION]")
    print(f"  Ghost Mass: {M_ghost:.2f} GeV")
    print(f"  Effective Coupling (sin²θ ~ 0.005): g_X = {g_x:.4f}")
    print(f"  Loop Contribution: Δa_mu(Ghost) = {delta_a_ghost:.2e}")
    
    # Compare
    fraction = delta_a_ghost / delta_a_mu
    
    print(f"\n[COMPARISON]")
    print(f"  Experimental Anomaly: {delta_a_mu:.2e}")
    print(f"  Ghost Contribution: {delta_a_ghost:.2e}")
    print(f"  Fraction Explained: {fraction*100:.2f}%")
    
    print(f"\n[INTERPRETATION]")
    if fraction > 0.1:
        print("  ✓ Ghost Z' can explain a significant portion of the g-2 anomaly!")
        print("  STATUS: SUPPORTIVE")
    elif fraction > 0.01:
        print("  ~ Ghost Z' provides a small but non-negligible contribution.")
        print("  STATUS: PARTIAL SUPPORT")
    else:
        print("  ✗ Ghost contribution is negligible compared to the anomaly.")
        print("  STATUS: NO SIGNIFICANT CONTRIBUTION")
    
    # Alternative: Dark Tower Light States
    print(f"\n[ALTERNATIVE: LIGHT DARK TOWER]")
    m_tower = 2.85  # GeV (lightest survivor)
    # Light scalars can give larger contribution
    delta_a_tower = (g_x**2 / (16 * np.pi**2)) * (m_mu / m_tower)**2 * (1/3)
    print(f"  Tower Mass: {m_tower} GeV")
    print(f"  Loop Contribution: Δa_mu(Tower) = {delta_a_tower:.2e}")
    print(f"  Fraction Explained: {delta_a_tower/delta_a_mu*100:.2f}%")

if __name__ == "__main__":
    main()
