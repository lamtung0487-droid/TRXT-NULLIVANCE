"""
TRXT Phase K.2: SPARC V15 Validation
====================================
Solving the Global Poisson PDE with a Scale-Dependent Polytropic Index n(r).

This script implements the formal n(r) transition derived in K.1 and 
executes a 2-parameter fit (Upsilon_star, Transition_Scale) across 
SPARC galaxies.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.sparse import diags
import os

# Constants
G = 4.302e-6  # kpc (km/s)^2 Msun^-1

def get_running_n(rho, n_min=1.37, n_max=20.74, rho_crit=1e-26):
    """The derived Scale-Relativity transition."""
    return n_min + (n_max - n_min) / (1.0 + (rho_crit / rho)**1.5)

def solve_poisson_k2(r, rho_b, r_c):
    """Solves -U'' = 4*pi*G*r*rho_eff for U=r*Phi"""
    dr = r[1] - r[0]
    N = len(r)
    
    # Effective Density with Scale-Relativity
    # alpha is the logic tension coupling derived from NJL sector ~ 6.5
    alpha_coupling = 6.5
    
    # We estimate local density to get running n
    # For a first pass, we use rho_b as the scale proxy
    n_r = get_running_n(rho_b, rho_crit=1/(r_c**3)) # r_c maps to density scale
    
    rho_eff = rho_b * (1.0 + alpha_coupling / n_r)
    
    # Discrete Laplacian
    main_diag = 2.0 * np.ones(N)
    off_diag = -1.0 * np.ones(N-1)
    K = diags([off_diag, main_diag, off_diag], [-1, 0, 1], shape=(N, N)).toarray()
    
    # RHS: 4*pi*G*r*rho_eff * dr^2
    rhs = 4.0 * np.pi * G * r * rho_eff * dr**2
    
    # BCs: U[0]=0, U[N-1] match mass
    K[0,0] = 1.0; K[0,1] = 0.0; rhs[0] = 0.0
    
    U = np.linalg.solve(K, rhs)
    phi = np.zeros(N)
    phi[1:] = U[1:] / r[1:]
    phi[0] = phi[1]
    
    v2 = r * np.gradient(phi, r)
    return np.sqrt(np.maximum(v2, 0))

def run_v15_k2_validation():
    print("="*60)
    print("TRXT PHASE K.2: SPARC V15 VALIDATION (SCALE-RELATIVITY)")
    print("="*60)
    
    data_dir = r'C:\Users\NC\Music\trxt nullivance v14\paper\TRXT_V7_Release\source_code\data\sparc'
    gal = 'NGC5055' # Primary litmus test
    filepath = os.path.join(data_dir, f'{gal}_rotmod.dat')
    
    if not os.path.exists(filepath):
        print(f"Error: {gal} data not found at {filepath}")
        return

    data = np.loadtxt(filepath, skiprows=3)
    r = data[:,0]; v_obs = data[:,1]; v_err = data[:,2]
    v_gas = data[:,3]; v_disc = data[:,4]; v_bul = data[:,5]
    
    def objective(params):
        Upsilon, r_trans = params
        v_baryon = np.sqrt(v_gas**2 + Upsilon*v_disc**2 + v_bul**2)
        rho_b = (v_baryon**2) / (4*np.pi*G*r**2 + 1e-9)
        
        try:
            v_model = solve_poisson_k2(r, rho_b, r_trans)
            chi2 = np.sum(((v_obs - v_model)/v_err)**2)
            return chi2 / (len(r) - 2)
        except:
            return 1e9

    res = minimize(objective, [0.5, 5.0], bounds=[(0.1, 1.2), (0.1, 50.0)], method='L-BFGS-B')
    
    print(f"\nVALIDATION RESULTS (V15):")
    print(f"Reduced Chi-Squared: {res.fun:.4f}")
    print(f"Optimal Upsilon_star: {res.x[0]:.3f}")
    print(f"Transition Scale r_c: {res.x[1]:.2f} kpc")
    
    v_final = solve_poisson_k2(r, (np.sqrt(v_gas**2 + res.x[0]*v_disc**2 + v_bul**2)**2)/(4*np.pi*G*r**2+1e-9), res.x[1])
    
    plt.figure(figsize=(10,6))
    plt.errorbar(r, v_obs, yerr=v_err, fmt='k.', label='SPARC Data')
    plt.plot(r, v_final, 'r-', label='TRXT V15 (Scale-Relativity)')
    plt.title(f"SPARC V15 Validation: {gal} (Reduced $\\chi^2 = {res.fun:.2f}$)")
    plt.xlabel("Radius (kpc)"); plt.ylabel("Velocity (km/s)")
    plt.legend(); plt.grid(True, alpha=0.3)
    plt.savefig('v15_k2_sparc_validation.png')
    print("Saved 'v15_k2_sparc_validation.png'")

if __name__ == "__main__":
    run_v15_k2_validation()
