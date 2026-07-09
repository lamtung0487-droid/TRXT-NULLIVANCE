"""
TRXT Phase K: Scale-Relativity Probe
====================================
Testing a Dynamic Polytropic Index n(r) for SPARC Galaxies.

Hypothesis: 
The logic background melts from a rigid lattice (n ~ 21) at high density 
to a soft superfluid (n ~ 1.37) at low density.

n(r) = n_macro + (n_micro - n_macro) * exp(-r / r_c)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve
import os

# Units: [Distance] = kpc, [Velocity] = km/s, [Mass] = M_sun
G = 4.302e-6  # kpc (km/s)^2 Msun^-1
H0 = 67.4     # km/s/Mpc

def solve_1d_poisson_running_n(r_grid, rho_b, n_func, r_c):
    """
    Solves the 1D spherical Poisson equation for the NPL field 
    with a radially dependent polytropic index n(r).
    """
    dr = r_grid[1] - r_grid[0]
    N = len(r_grid)
    
    # Using finite difference on -U'' = 4*pi*G*r*rho_eff
    # L is the discrete 1D Laplacian
    main_diag = 2.0 * np.ones(N)
    off_diag = -1.0 * np.ones(N-1)
    L_matrix = diags([off_diag, main_diag, off_diag], [-1, 0, 1], shape=(N, N)).toarray()
    
    # Transitioning n(r)
    n_r = n_func(r_grid, r_c)
    
    # Effective Source with Scale-Relativity
    # alpha is the logic tension coupling
    alpha = 6.5 
    rho_eff = rho_b * (1.0 + alpha / n_r)
    
    rhs = 4.0 * np.pi * G * r_grid * rho_eff * dr**2
    
    # Boundary Conditions
    # U[0] = 0 (Phi at r=0 is finite)
    # At far boundary R_max, we assume Phi ~ 1/r
    rhs[0] = 0
    L_matrix[0, 0] = 1.0
    L_matrix[0, 1] = 0.0
    
    # Solve
    U = np.linalg.solve(L_matrix, rhs)
    
    # Phi = U / r
    phi = np.zeros(N)
    phi[1:] = U[1:] / r_grid[1:]
    phi[0] = phi[1] # regularity
    
    return phi

def trxt_n_running_model(params, r, v_gas, v_disk, v_bulge, G):
    """
    Calculates the rotation velocity using the TRXT NPL model 
    with a dynamic index n(r).
    """
    Upsilon_star, r_0, n_micro, n_macro = params
    
    # 1. Baryonic mass distribution from components
    # We assume spherical components for the potential derivation
    M_b = (r / G) * (v_gas**2 + Upsilon_star * v_disk**2 + v_bulge**2)
    rho_b = np.gradient(M_b, r) / (4 * np.pi * r**2)
    rho_b = np.maximum(rho_b, 1e-10) # No negative density
    
    # 2. Dynamic n(r) function
    def n_func(radius, rc):
        # Lattice melting function: Rigid in core, Soft in outskirt
        return n_macro + (n_micro - n_macro) * np.exp(-radius / rc)
    
    # 3. Solve for Potential
    phi = solve_1d_poisson_running_n(r, rho_b, n_func, r_0)
    
    # 4. v^2 = r * dPhi/dr
    dphi_dr = np.gradient(phi, r)
    v2_model = r * dphi_dr
    v_total = np.sqrt(np.maximum(v2_model, 0))
    
    return v_total

def run_probe_dynamic_sparc():
    print("="*60)
    print("PHASE K PROBE: SCALE-RELATIVITY RUNNING n(r) FIT")
    print("="*60)
    
    data_dir = r'C:\Users\NC\Music\trxt nullivance v14\paper\TRXT_V7_Release\source_code\data\sparc'
    # Test on NGC5055 (a known galaxy in our data folder)
    galaxies = ['NGC5055'] 
    
    for gal in galaxies:
        filepath = os.path.join(data_dir, f'{gal}_rotmod.dat')
        if not os.path.exists(filepath):
            print(f"Skipping {gal}: Data not found.")
            continue
            
        try:
            data = np.loadtxt(filepath, skiprows=3)
        except Exception as e:
            print(f"Error loading {gal}: {e}")
            continue
            
        r = data[:, 0]
        v_obs = data[:, 1]
        v_err = data[:, 2]
        v_gas = data[:, 3]
        v_disk = data[:, 4]
        v_bulge = data[:, 5]
        
        # Initial guess from Theory:
        # Upsilon ~ 0.5, r_0 ~ 10 kpc, n_micro = 20.74, n_macro = 1.37
        initial_guess = [0.5, 10.0, 20.74, 1.37]
        # Allow n_micro and n_macro to adjust within logic bounds
        bounds = [(0.1, 1.5), (1.0, 50.0), (18.0, 24.0), (1.0, 2.5)]
        
        print(f"Refining fit for {gal} with Scale-Relativity logic...")
        
        def obj(p):
            try:
                v_mod = trxt_n_running_model(p, r, v_gas, v_disk, v_bulge, G)
                chi2 = np.sum(((v_obs - v_mod) / v_err)**2)
                red_chi2 = chi2 / (len(r) - 4)
                
                # Penalty for n deviation (keeping it near derived lattice theory)
                pen_micro = 50.0 * (p[2] - 20.74)**2 
                pen_macro = 100.0 * (p[3] - 1.37)**2
                
                return red_chi2 + pen_micro + pen_macro
            except:
                return 1e9
            
        res = minimize(obj, initial_guess, bounds=bounds, method='L-BFGS-B')
        
        print(f"\nPROBE RESULTS for {gal}:")
        print(f"Reduced Chi-Squared: {res.fun:.4f}")
        print(f"Upsilon_star: {res.x[0]:.2f}")
        print(f"Melting Length (r_0): {res.x[1]:.2f} kpc")
        print(f"Micro Index (Fixed/Theory): {res.x[2]:.2f}")
        print(f"Macro Index (Result): {res.x[3]:.2f}")
        
        # Plotting
        v_mod_final = trxt_n_running_model(res.x, r, v_gas, v_disk, v_bulge, G)
        plt.figure(figsize=(10, 6))
        plt.errorbar(r, v_obs, yerr=v_err, fmt='k.', label='SPARC (Data)')
        plt.plot(r, v_mod_final, 'r-', label='TRXT (Running $n(r)$)')
        plt.plot(r, np.sqrt(v_gas**2 + res.x[0]*v_disk**2 + v_bulge**2), 'b--', label='Baryonic Core')
        
        plt.title(f"SPARC Galaxy {gal}: Scale-Relativity Solution")
        plt.xlabel("Radius (kpc)")
        plt.ylabel("Velocity (km/s)")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.savefig(f'probe_k2_dynamic_sparc_{gal}.png')
        print(f"Saved probe plot to 'probe_k2_dynamic_sparc_{gal}.png'")

if __name__ == '__main__':
    run_probe_dynamic_sparc()
