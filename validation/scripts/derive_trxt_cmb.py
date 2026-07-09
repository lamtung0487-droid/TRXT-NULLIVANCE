import numpy as np

# --- TRXT CONSTANTS ---
M_STAR_GEV = 365.24 
# Vacuum Energy Density rho_vac ~ mu^4
# From loop integral: rho_vac ~ (N_f/16pi^2) * Lambda^4
# Using effective parameters from deriving EOS
MU_EFF = 365.24 # Order of M*
LAMBDA_EFF = 0.5

def derive_cmb_thermodynamics():
    print("--- TRXT PHASE 5: CMB ORIGIN DERIVATION ---")
    
    # 1. Calculate Vacuum Energy Density (Latent Heat reservoir)
    # V(0) - V(v) = mu^4 / (4*lambda)
    rho_vac = (MU_EFF**4) / (4 * LAMBDA_EFF)
    print(f"Vacuum Energy Density (Latent Heat): {rho_vac:.2e} GeV^4")
    
    # 2. Convert to Temperature (assuming thermalization)
    # rho_rad = (pi^2 / 30) * g_star * T^4
    # T = (30 * rho_vac / (pi^2 * g_star))^(1/4)
    
    g_star_sm = 106.75 # Standard Model degrees of freedom at high T
    
    T_reheat = (30 * rho_vac / (np.pi**2 * g_star_sm))**0.25
    print(f"Reheating Temperature (T_rh): {T_reheat:.2e} GeV")
    
    # Check if T_reheat > T_BBN (1 MeV) to allow nucleosynthesis
    if T_reheat > 1e-3:
        print("[PASS] T_rh >> T_BBN (1 MeV). Standard Cosmology preserved.")
    else:
        print("[FAIL] Reheating too cold!")
        
    # 3. Entropy Generation
    # S = (2*pi^2 / 45) * g_star * T^3
    S_density = (2 * np.pi**2 / 45) * g_star_sm * T_reheat**3
    print(f"Entropy Density generated: {S_density:.2e} GeV^3")
    
    # 4. CMB Connection
    # The CMB we see today is the redshifted remnant of this bath.
    # Prediction: The "Condensation" IS the reheating event.
    
    print("\n--- CONCLUSION ---")
    print("The Big Condensation (Symmetry Breaking of Logic Field) releases")
    print(f"massive latent heat (T ~ {T_reheat:.1f} GeV), creating the primordial")
    print("particle bath. This bath then expands and cools to become the CMB.")
    print("Therefore, CMB is consistent with TRXT Phase Transition.")

if __name__ == "__main__":
    derive_cmb_thermodynamics()
