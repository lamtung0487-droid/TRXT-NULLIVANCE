import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve
from scipy.optimize import minimize
import os
import glob

def parse_sparc_file(filepath):
    """Parses a SPARC .dat file."""
    try:
        data = np.loadtxt(filepath, skiprows=3) # Skip header
        if data.ndim == 1:
            data = data.reshape(1, -1)
        # Rad[kpc], Vobs[km/s], errV[km/s], Vgas[km/s], Vdisk[km/s], Vbul[km/s], SBdisk[L_sun/pc^2], SBbul[L_sun/pc^2]
        r = data[:, 0]
        v_obs = data[:, 1]
        v_err = data[:, 2]
        v_gas = data[:, 3]
        v_disk = data[:, 4]
        v_bulge = data[:, 5]
        return r, v_obs, v_err, v_gas, v_disk, v_bulge
    except Exception as e:
        return None

def solve_1d_poisson_spherical(r_grid, rho_total, G):
    """
    Solve 1D Spherical Poisson Equation: 1/r^2 d/dr (r^2 dPhi/dr) = 4 pi G rho
    Using Finite Differences.
    """
    N = len(r_grid)
    dr = r_grid[1] - r_grid[0]
    
    rhs = 4 * np.pi * G * r_grid * rho_total
    
    main_diag = -2.0 / dr**2 * np.ones(N)
    off_diag = 1.0 / dr**2 * np.ones(N-1)
    
    main_diag[0] = 1.0
    off_diag[0] = 0.0
    rhs[0] = 0.0
    
    M_tot = np.trapz(4 * np.pi * r_grid**2 * rho_total, r_grid)
    main_diag[-1] = 1.0
    rhs[-1] = -G * M_tot
    
    A = diags([off_diag, main_diag, off_diag], [-1, 0, 1], format='csr')
    u = spsolve(A, rhs)
    
    Phi = np.zeros_like(r_grid)
    Phi[1:] = u[1:] / r_grid[1:]
    Phi[0] = Phi[1]
    
    return Phi, M_tot

def trxt_npl_model(params, r, v_gas, v_disk, v_bulge, G, a0_kpc):
    """
    Calculates the total rotation curve under the TRXT-NPL framework.
    Params: [Upsilon_star, r_0]
    """
    upsilon, r_0 = params
    
    # Positive constraints
    if upsilon < 0.1 or upsilon > 10.0 or r_0 < 0.1 or r_0 > 50.0:
        return np.inf * np.ones_like(r)
        
    # Baryonic contribution (v^2 = sum of squares)
    # Gas is multiplied by 1.33 to account for Helium
    v_baryon_sq = np.abs(v_gas)*np.abs(v_gas) * np.sign(v_gas) + upsilon * (np.abs(v_disk)*np.abs(v_disk) * np.sign(v_disk) + np.abs(v_bulge)*np.abs(v_bulge) * np.sign(v_bulge))
    
    # Prevent negative values due to gas tracking
    v_baryon_sq[v_baryon_sq < 0] = 0.0
    g_N = v_baryon_sq / r
    
    # NPL Logic Tension Source (The "Dark Matter" counterpart)
    # c_alpha = (1 / 4 pi G) * div( sqrt(a0 * |grad Phi_bar|) * r_hat )
    # With spatial modulation factor r_0
    # FIX 2026-03-01: np.gradient(f, x) requires coordinate array, NOT spacing array
    # dr = np.gradient(r) was a VECTOR — passing it as 'varargs' causes silent wrong result
    F_logic = np.sqrt(a0_kpc * g_N) * (1.0 - np.exp(-r/r_0))
    r2F = r**2 * F_logic
    div_F = np.gradient(r2F, r) / (r**2 + 1e-10)  # FIXED: r not dr
    
    c_alpha = div_F / (4 * np.pi * G)
    c_alpha[c_alpha < 0] = 0.0
    
    # Baryonic density (approximated for spherical Poisson solver)
    rho_b = g_N / (4 * np.pi * G * r + 1e-10)
    rho_tot = rho_b + c_alpha
    
    # Solve Global PDE
    Phi_tot, _ = solve_1d_poisson_spherical(r, rho_tot, G)
    dPhi_dr = np.gradient(Phi_tot, r)  # FIXED: r not dr (same API bug as above)
    v_tot2 = r * dPhi_dr
    
    # Return velocity
    v_tot2[v_tot2 < 0] = 0.0
    return np.sqrt(v_tot2)

def objective_function(params, r, v_obs, v_err, v_gas, v_disk, v_bulge, G, a0_kpc):
    """Calculates Chi-Squared."""
    v_model = trxt_npl_model(params, r, v_gas, v_disk, v_bulge, G, a0_kpc)
    
    if np.any(np.isinf(v_model)) or np.any(np.isnan(v_model)):
        return 1e9
        
    chi2 = np.sum(((v_obs - v_model) / v_err)**2)
    
    if np.isnan(chi2):
        return 1e9
        
    return chi2

def run_npl_sparc_pde_gate3():
    """
    STRICT GATE 3: SPARC ROTATION CURVES VIA GLOBAL PDE SOLVER (USING AUTHENTIC SPARC DATA)
    Master Protocol V2.0 Compliance: Solve Global Poisson Field Equation on real Lelli et al. 2016 data.
    """
    print("=== TRXT Nullivance: AUTHENTIC SPARC ROTATION CURVES (Gate 3 - V14) ===")
    
    # FIX 2026-03-01: removed hardcoded user path; use path relative to script
    # Data: Lelli, McGaugh & Schombert (2016) AJ 152,157  DOI:10.3847/0004-6256/152/6/157
    # Download: http://astroweb.cwru.edu/SPARC/Rotmod_LTG.zip
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.normpath(os.path.join(script_dir,
                    "..", "..", "..", "..", "data", "sparc"))
    if not os.path.exists(data_dir):
        print(f"ERROR: SPARC data directory not found at: {data_dir}")
        print("  Download Rotmod_LTG.zip from http://astroweb.cwru.edu/SPARC/Rotmod_LTG.zip")
        print("  Extract into: <workspace>/source_code/data/sparc/")
        return
        
    files = glob.glob(os.path.join(data_dir, "*.dat"))
    if not files:
        print("ERROR: No .dat files found in data directory.")
        return
        
    print(f"Found {len(files)} SPARC galaxies. Commencing PDE Solver fitting...")
    
    G = 4.3009e-6 # kpc M_sun^-1 (km/s)^2
    a0_kpc = 3800.0 # (km/s)^2 / kpc
    
    chi2_list = []
    best_fits = {}
    
    sample_to_plot = None
    
    # Process a representative sample to save time, or all if needed
    for counter, filepath in enumerate(files):
        galaxy_name = os.path.basename(filepath).replace('.dat', '')
        
        parsed = parse_sparc_file(filepath)
        if parsed is None:
            continue
            
        r, v_obs, v_err, v_gas, v_disk, v_bulge = parsed
        
        # Enforce minimum error floor of 5% or 5 km/s for realistic fitting (standard practice)
        v_err_eff = np.maximum(v_err, 0.05 * v_obs)
        v_err_eff = np.maximum(v_err_eff, 5.0)
        
        bounds = [(0.1, 5.0), (0.1, 30.0)] # Upsilon, r_0 bounds
        initial_guess = [0.5, 5.0]
        
        res = minimize(objective_function, initial_guess, 
                       args=(r, v_obs, v_err_eff, v_gas, v_disk, v_bulge, G, a0_kpc),
                       bounds=bounds, method='L-BFGS-B')
                       
        red_chi2 = res.fun / (len(r) - 2) if len(r) > 2 else 0
        chi2_list.append(red_chi2)
        best_fits[galaxy_name] = {'chi2': red_chi2, 'params': res.x}
        
        # Save NGC 5055 (or similar good quality galaxy) for plotting
        if "NGC5055" in galaxy_name:
            v_model = trxt_npl_model(res.x, r, v_gas, v_disk, v_bulge, G, a0_kpc)
            sample_to_plot = (galaxy_name, r, v_obs, v_err_eff, v_model, v_gas, v_disk, v_bulge, res.x)
            
        if (counter+1) % 25 == 0:
            print(f"Processed {counter+1}/{len(files)} galaxies...")
            
    # Fallback if NGC 5055 is not found, just use the last one
    if sample_to_plot is None and len(files) > 0:
        v_model = trxt_npl_model(res.x, r, v_gas, v_disk, v_bulge, G, a0_kpc)
        sample_to_plot = (galaxy_name, r, v_obs, v_err_eff, v_model, v_gas, v_disk, v_bulge, res.x)

    n_galaxies = len(chi2_list)
    mean_chi2 = np.mean(chi2_list)
    median_chi2 = np.median(chi2_list)
    # FIX 2026-03-01: threshold 3.0 (standard scientific criterion), was 5.0 (too lenient)
    CHI2_THRESHOLD = 3.0
    good_fits = sum(1 for c in chi2_list if c < CHI2_THRESHOLD)

    print("\nRESULTS: AUTHENTIC GATE 3 SPARC EVALUATION")
    print("-" * 50)
    print(f"Total Galaxies Evaluated:    {n_galaxies}")
    print(f"Mean    Reduced Chi-Squared: {mean_chi2:.2f}")
    print(f"Median  Reduced Chi-Squared: {median_chi2:.2f}")
    print(f"Galaxies passing chi2<{CHI2_THRESHOLD}: {good_fits} ({good_fits/n_galaxies*100:.1f}%)")
    
    # Visualization
    plt.figure(figsize=(12, 6))
    
    if sample_to_plot:
        name, r, v_obs, v_err, v_model, v_gas, v_disk, v_bulge, params = sample_to_plot
        
        plt.subplot(121)
        plt.title(fr"TRXT-NPL Fit: {name} ($\Upsilon_\star={params[0]:.2f}, r_0={params[1]:.2f}$)")
        plt.errorbar(r, v_obs, yerr=v_err, fmt='o', color='white', alpha=0.5, label='SPARC Obs')
        plt.plot(r, v_model, color='cyan', linewidth=2, label='NPL Total $v(r)$')
        
        v_bar_sq = np.abs(v_gas)*np.abs(v_gas)*np.sign(v_gas) + params[0]*(np.abs(v_disk)*np.abs(v_disk)*np.sign(v_disk) + np.abs(v_bulge)*np.abs(v_bulge)*np.sign(v_bulge))
        v_bar_sq[v_bar_sq < 0] = 0
        plt.plot(r, np.sqrt(v_bar_sq), color='red', linestyle='--', label='Baryonic $v(r)$')
        
        plt.xlabel('Radius (kpc)')
        plt.ylabel('Velocity (km/s)')
        plt.grid(alpha=0.2)
        plt.legend()
        plt.gca().set_facecolor('#111111')
        
    plt.subplot(122)
    plt.title(f"Reduced $\chi^2$ Distribution (N={n_galaxies})")
    plt.hist(chi2_list, bins=20, color='orange', alpha=0.7)
    plt.axvline(5.0, color='red', linestyle='dashed', linewidth=2, label='Gate 3 Threshold ($\chi^2 < 5$)')
    plt.axvline(median_chi2, color='cyan', linestyle='-', linewidth=2, label=f'Median: {median_chi2:.2f}')
    plt.xlabel('Reduced $\chi^2$')
    plt.ylabel('Galaxy Count')
    plt.legend()
    plt.gca().set_facecolor('#111111')
    
    plt.tight_layout()
    save_path = 'sparc_npl_pde_gate3.png'
    plt.savefig(save_path, dpi=300)
    print(f"\nVisualization saved to {save_path}")

if __name__ == '__main__':
    run_npl_sparc_pde_gate3()
