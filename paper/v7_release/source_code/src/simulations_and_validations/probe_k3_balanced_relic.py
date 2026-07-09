"""
TRXT Phase K: Scale-Relativity Probe
====================================
Testing "Topological Re-freezing" (Defect Production) for Relic Density.

Hypothesis:
As the logic lattice melts (n drops), the surplus logic tension 
condenses into additional topological defects. This term S(T) 
offsets the Area-Law annihilation.

dY/dx = - (lam/x^2) * sigma_v * (Y^2 - Y_eq^2) + S(x)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Constants
M_PL = 1.22e19 # GeV
T_0 = 2.35e-13 # GeV
rho_c = 3.6e-47 # GeV^4

def Y_eq(x, g_chi):
    if x > 100: return 0.0
    return 0.145 * (g_chi / 106.75) * (x**(1.5)) * np.exp(-x)

def x_sigma_v(x, m_chi):
    # Area Law suppressed cross section (The "Failure" from J1)
    sigma_0 = 100.0 
    suppression = np.exp(-x / 3.0) 
    return sigma_0 * suppression

def boltzmann_balanced_eq(W, x, params):
    g_star, g_chi, m_chi, s_scale = params
    
    Y = np.exp(W)
    Y_e = Y_eq(x, g_chi)
    
    lam = np.sqrt(np.pi / 45.0) * M_PL * m_chi * np.sqrt(g_star)
    sig_v = x_sigma_v(x, m_chi)
    
    # 1. Annihilation term (Standard Riccati)
    annihil = - (lam / x**2) * sig_v * Y * (1.0 - (Y_e/Y)**2)
    
    # 2. Production term S(x) - "Topological Re-freezing"
    # S(x) scales with the rate of lattice melting dn/dx
    # We model it as a Gaussian pulse around the melting temperature T_m
    x_m = 23.0 # Lattice melting point
    S_x = s_scale * np.exp(-(x - x_m)**2 / 4.0) / Y # Normalize by Y for W-space
    
    return annihil + S_x

def run_probe_balanced_relic(m_chi=5.71):
    print("="*60)
    print("PHASE K PROBE: BALANCED RELIC DENSITY (RE-FREEZING)")
    print("="*60)
    
    g_star = 106.75
    g_chi = 2
    
    x_span = np.logspace(0, 3, 5000)
    W_initial = np.log(max(Y_eq(x_span[0], g_chi), 1e-30))
    
    # Scan for S_scale that matches Planck
    s_scales = [0.0, 1e-15, 1e-13, 1e-11] 
    
    plt.figure(figsize=(10, 6))
    
    for s_scale in s_scales:
        print(f"Solving with S_scale = {s_scale:.2e}...")
        sol_W = odeint(boltzmann_balanced_eq, W_initial, x_span, 
                       args=([g_star, g_chi, m_chi, s_scale],), rtol=1e-8, atol=1e-10)
        Y_final = np.exp(sol_W[-1][0])
        omega_h2 = 2.74e8 * m_chi * Y_final
        
        label = f"S={s_scale:.1e}, $\Omega h^2$={omega_h2:.4f}"
        plt.loglog(x_span, np.exp(sol_W[:,0]), label=label)
        print(f"  Final Omega h2: {omega_h2:.4f}")

    # Reference Planck Line
    plt.axhline(4.0e-10, color='k', linestyle='--', label='Planck Target Yield')
    plt.title("Relic Density: Annihilation vs. Topological Re-freezing")
    plt.xlabel("x = m/T")
    plt.ylabel("Yield Y")
    plt.ylim(1e-20, 1e-1)
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.2)
    plt.savefig('probe_k3_balanced_relic.png')
    print("Saved 'probe_k3_balanced_relic.png'")

if __name__ == '__main__':
    run_probe_balanced_relic()
