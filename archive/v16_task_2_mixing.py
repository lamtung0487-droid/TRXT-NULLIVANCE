import numpy as np
from TRXT_Analysis_Engine import TRXTAnalyzer

def main():
    print("=== TRXT PROTOCOL: V16 TASK 2 (STERILE MIXING) - SCIENCE GRADE ===")
    engine = TRXTAnalyzer()
    
    # LEP Data (PDG / CERN)
    N_NU_MEASURED = 2.9840
    N_NU_ERROR = 0.0082
    N_NU_SM = 3.0
    
    print("[LEP DATA (PDG)]")
    print(f"  N_nu Measured: {N_NU_MEASURED} +/- {N_NU_ERROR}")
    print(f"  N_nu SM: {N_NU_SM}")
    print(f"  Deficit: {N_NU_SM - N_NU_MEASURED:.4f} ({(N_NU_SM - N_NU_MEASURED)/N_NU_ERROR:.2f} sigma)")
    
    # Convert to Width Deficit
    # Gamma_inv ~ N_nu * Gamma_nu_single
    # Gamma_nu_single ~ 167 MeV
    gamma_nu_single = 167.2  # MeV
    gamma_inv_sm = N_NU_SM * gamma_nu_single
    gamma_inv_meas = N_NU_MEASURED * gamma_nu_single
    deficit_mev = gamma_inv_meas - gamma_inv_sm
    
    print(f"\n[INVISIBLE WIDTH]")
    print(f"  Gamma_inv (SM): {gamma_inv_sm:.1f} MeV")
    print(f"  Gamma_inv (Measured): {gamma_inv_meas:.1f} MeV")
    print(f"  Deficit: {deficit_mev:.2f} MeV")
    
    # Calculate Mixing
    sin2_theta = engine.calculate_sterile_mixing(deficit_mev)
    theta_rad = np.arcsin(np.sqrt(sin2_theta))
    theta_deg = np.degrees(theta_rad)
    
    print(f"\n[STERILE MIXING CALCULATION]")
    print(f"  Required sin^2(theta): {sin2_theta:.5f}")
    print(f"  Mixing Angle theta: {theta_deg:.3f} degrees")
    
    print(f"\n[CONSTRAINT CHECK]")
    print(f"  - This deficit is only ~2 sigma. Could be systematic/fluctuation.")
    print(f"  - sin^2(theta) ~ 0.005 is at the edge of global 3+1 sterile fits.")
    print(f"  - LSND/MiniBooNE anomalies suggest similar range, but are also controversial.")
    print(f"  - Non-unitarity bounds from EW precision are model-dependent.")
    
    print(f"\n[CONCLUSION]")
    print(f"  STATUS: 'Mechanism plausible. Requires detailed 3+1/3+n global fit.'")
    print(f"  VERDICT: SUGGESTIVE HINT (~2 sigma), NOT VALIDATED.")

if __name__ == "__main__":
    main()
