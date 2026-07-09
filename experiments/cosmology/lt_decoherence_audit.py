import numpy as np
import matplotlib.pyplot as plt

def simulate_lt_decoherence():
    """
    E11.1: Logic Tension Decoherence Simulation
    Models the stability of the phase mismatch field Delta-Theta 
    under environmental scattering in ISM vs Laboratory.
    """
    print("=== Logic Tension Decoherence Audit (Problem D) ===")
    
    # 1. Environmental Parameters
    # ISM (Interstellar Medium)
    n_ism = 1.0e6  # atoms/m^3 (~1 cm^-3)
    T_ism = 1.0e4  # K
    
    # Laboratory Vacuum (High vac)
    n_lab = 1.0e12 # atoms/m^3 (~10^6 cm^-3)
    T_lab = 300.0  # K
    
    # Physical Constants
    k_B = 1.38e-23
    hbar = 1.054e-34
    m_p = 1.67e-27 # mass of scatterer (proton)
    
    # 2. Decoherence Rate Calculation
    # Gamma_dec ~ lambda_dB^2 * n * v * sigma
    # lambda_dB = hbar / sqrt(2 pi m k_B T)
    
    def get_decoherence_rate(n, T, r_system):
        v_th = np.sqrt(k_B * T / m_p)
        lambda_dB = hbar / np.sqrt(2 * np.pi * m_p * k_B * T)
        
        # Effective cross section for phase perturbation
        # In LT framework, phase mismatch is sensitive to collisions that shift the wavepacket
        sigma_scatt = np.pi * r_system**2
        
        # Rate of scattering
        gamma_scatt = n * v_th * sigma_scatt
        
        # Decoherence rate: Gamma_dec = gamma_scatt * (r_system / lambda_dB)^2
        # (Assuming the system is larger than the thermal de Broglie wavelength)
        gamma_dec = gamma_scatt * (r_system / lambda_dB)**2
        return gamma_dec

    r_target = 1e-10 # 1 Angstrom (atomic scale)
    
    g_ism = get_decoherence_rate(n_ism, T_ism, r_target)
    g_lab = get_decoherence_rate(n_lab, T_lab, r_target)
    
    print(f"Decoherence Rate (ISM): {g_ism:.2e} Hz  => Tau: {1/g_ism:.2e} s")
    print(f"Decoherence Rate (Lab): {g_lab:.2e} Hz  => Tau: {1/g_lab:.2e} s")
    
    # 3. Chameleon Protection Mechanism
    # The LT framework suggests that alpha (existence density) stiffens the field.
    # We model a 'Stiffening Factor' S = exp(alpha * rho / rho_crit)
    # Effective decoherence rate: Gamma_eff = Gamma / S
    
    rho_ism = n_ism * m_p
    rho_lab = n_lab * m_p
    rho_crit = 1e-20 # Arbitrary threshold for non-linear stiffening
    
    tau_vals = []
    dens_range = np.logspace(-27, -12, 100) # kg/m^3
    
    for rho in dens_range:
        # Interpolate T from ISM-like to Lab-like
        T = 10**np.interp(np.log10(rho), [np.log10(rho_ism), np.log10(rho_lab)], [4, 2.5])
        n = rho / m_p
        g = get_decoherence_rate(n, T, r_target)
        
        # Apply stiffening (The hypothesis)
        S = np.exp(rho / (100 * rho_crit)) 
        tau_eff = 1.0 / (g / S + 1e-20)
        tau_vals.append(tau_eff)
        
    plt.figure(figsize=(10, 6))
    plt.loglog(dens_range, tau_vals, color='cyan', label='Phase Stability Lifetime (Tau)')
    plt.axhline(1.0, color='red', linestyle='--', label='1 Second Threshold')
    plt.axvline(rho_ism, color='orange', linestyle=':', label='ISM Density')
    plt.axvline(rho_lab, color='green', linestyle=':', label='Lab Density')
    
    plt.title("Logic Tension Phase Stability vs Environmental Density")
    plt.xlabel("Density (kg/m^3)")
    plt.ylabel("Stability Lifetime (s)")
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.2)
    plt.gca().set_facecolor('#111111')
    
    save_path = 'lt_decoherence_audit.png'
    plt.savefig(save_path)
    print(f"Audit plot saved to {save_path}")

if __name__ == "__main__":
    simulate_lt_decoherence()
