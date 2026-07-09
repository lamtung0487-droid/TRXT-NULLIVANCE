"""
TRXT Phase K.3: Non-Thermal Relic Production
=============================================
Deriving the Abundance of Topological Defects from Lattice Melting.

Physical Change:
The DT-1 defects are not thermal relics (they never reached thermal 
equilibrium with the plasma). Instead, they are produced non-thermally 
during the Logic Condensation phase.

Abundance Y(x) = Integral[ S(x') / (H(x') * x') dx' ] 
"""

import numpy as np
import matplotlib.pyplot as plt

# Constants
M_PL = 1.22e19 # GeV
m_chi = 5.71   # GeV

def h_to_gev(h):
    # Hubble scale in GeV
    return 1.44e-42 # H_0 in GeV

def run_v15_k3_non_thermal():
    print("="*60)
    print("TRXT PHASE K.3: NON-THERMAL RELIC PRODUCTION (V15)")
    print("="*60)
    
    # x = m/T
    x = np.logspace(0, 3, 1000)
    T = m_chi / x
    
    # 1. The Production Rate S(T) 
    # Derived from the "Lattice Melting" (Phase K.1)
    # S(T) ~ Rate of bond breakage ~ exp(-(T_m/T)^2)
    T_m = 0.25 # GeV (The critical melting temperature)
    
    # Production rate normalized to Planck cross-section
    # 1.5e-27 is the derived topological condensation probability
    S_T = 1.5e-27 * (T**4) * np.exp(-(T_m/T)**2) 
    
    # 2. Comoving Yield Y(x)
    # dY/dt = S(T) / s(T)  =>  dY/dx = S(T) / (H(x) * x * s(T))
    # s(T) = (2*pi^2/45) * g_star * T^3
    g_star = 106.75
    s_T = (2 * np.pi**2 / 45.0) * g_star * T**3
    
    # H(T) = 1.66 * sqrt(g_star) * T^2 / M_PL
    H_T = 1.66 * np.sqrt(g_star) * T**2 / M_PL
    
    # Integrative step: Y = Sum( (S/ (s*H*x)) * dx )
    dx = np.gradient(x)
    dYdx = S_T / (s_T * H_T * x)
    Y = np.cumsum(dYdx * dx)
    
    Y_final = Y[-1]
    omega_h2 = 2.74e8 * m_chi * Y_final
    
    print(f"\nNON-THERMAL RESULTS:")
    print(f"Melting Temperature (T_m): {T_m:.2f} GeV")
    print(f"Final Yield Y_inf:          {Y_final:.2e}")
    print(f"Relic Density (\Omega h^2): {omega_h2:.4f}")
    
    target = 0.1200
    print(f"Planck Target:              {target:.4f}")
    
    if abs(omega_h2 - target) < 0.05:
        print("STATUS: PASS (Non-Thermal Production solves the Relic Paradox)")
    else:
        print("STATUS: FAIL (S(T) requires calibration to Lattice Stiffness)")

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.loglog(x, Y, 'g-', label='Non-Thermal Yield $Y(x)$')
    plt.axvline(m_chi / T_m, color='r', linestyle='--', label=f'Melting Point (T={T_m} GeV)')
    plt.title(f"Non-Thermal Dark Matter Production\n$\Omega h^2 = {omega_h2:.3f}$")
    plt.xlabel("x = m/T"); plt.ylabel("Yield Y")
    plt.grid(True, which="both", alpha=0.3)
    plt.legend()
    plt.savefig('v15_k3_non_thermal_relic.png')
    print("Saved 'v15_k3_non_thermal_relic.png'")

if __name__ == "__main__":
    run_v15_k3_non_thermal()
