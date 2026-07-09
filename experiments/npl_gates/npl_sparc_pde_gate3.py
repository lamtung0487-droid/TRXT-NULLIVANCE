import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve

def run_npl_sparc_pde_gate3():
    """
    PDE SOLVER DEMO on MOCK galaxies -- NOT A VALIDATION GATE.

    Lab gate-integrity finding (2026-07-09): this script generates synthetic
    galaxies and sets v_obs = v_model + noise (see the loop below), so a
    chi^2 ~ 1 outcome is guaranteed by construction and carries zero
    evidential weight. It remains useful as a solver smoke test only.
    The real Gate 3 runs on data/sparc/Rotmod_LTG via
    experiments/v17_gates/Gate3_GalacticRotation_SPARC.py.
    """
    print("=== TRXT Nullivance: NPL PDE SOLVER DEMO (MOCK DATA - NOT A GATE) ===")
    print("WARNING: synthetic self-generated data; chi^2 here validates nothing.")
    
    # Constants
    G = 4.3009e-6 # kpc M_sun^-1 (km/s)^2
    a0 = 1.2e-8   # kpc/yr^2 ~ 3800 km^2/s^2 / kpc (MOND acceleration scale, used as NPL tension coupling)
    a0_kpc = 3800.0 # (km/s)^2 / kpc
    
    # 1. Generate MOCK SPARC Data (175 Galaxies)
    # We will pick 5 representative galaxies to physically solve the PDE on.
    n_galaxies = 175
    np.random.seed(42)
    
    print(f"Generating realistic profiles for {n_galaxies} SPARC-like galaxies...")
    galaxies = []
    for i in range(n_galaxies):
        # Generate random baryonic masses and disk scale lengths
        M_disk = 10**np.random.uniform(8.5, 11.5) # M_sun
        Rd = np.random.uniform(1.0, 5.0) # kpc
        galaxies.append({'M_disk': M_disk, 'Rd': Rd})
        
    def solve_1d_poisson_spherical(r_grid, rho_total):
        """
        Solve 1D Spherical Poisson Equation: 1/r^2 d/dr (r^2 dPhi/dr) = 4 pi G rho
        Using Finite Differences.
        """
        N = len(r_grid)
        dr = r_grid[1] - r_grid[0]
        
        # We solve for u = r * Phi. 
        # The equation becomes d^2u/dr^2 = 4 pi G r rho
        rhs = 4 * np.pi * G * r_grid * rho_total
        
        # FD Matrix for d^2/dr^2
        main_diag = -2.0 / dr**2 * np.ones(N)
        off_diag = 1.0 / dr**2 * np.ones(N-1)
        
        # Boundary Conditions
        # u(0) = 0
        main_diag[0] = 1.0
        off_diag[0] = 0.0
        rhs[0] = 0.0
        
        # u(R) -> r * ( - GM_tot / r ) -> d(u)/dr = d(GM)/dr -> flat (simplification for isolated)
        # Assuming Phi -> 0 at infinity, we can just set Dirichlet u(R) = -G M_tot
        M_tot = np.trapezoid(4 * np.pi * r_grid**2 * rho_total, r_grid)
        main_diag[-1] = 1.0
        rhs[-1] = -G * M_tot
        
        A = diags([off_diag, main_diag, off_diag], [-1, 0, 1], format='csr')
        u = spsolve(A, rhs)
        
        # Phi = u / r, avoid division by zero
        Phi = np.zeros_like(r_grid)
        Phi[1:] = u[1:] / r_grid[1:]
        Phi[0] = Phi[1] # Limit r->0
        
        # Force dPhi/dr = (r_i dPhi_{i+1} - ... ) / dr
        # Better: just use Gauss law for exact differentiation to recover v^2
        return Phi, M_tot

    print("\nSolving fully-coupled Logic Tension PDE for 175 galaxies...")
    
    chi2_list = []
    
    # We will visualize one classic Milky_Way like galaxy
    sample_r = None
    sample_v_bar = None
    sample_v_tot = None
    sample_v_obs = None
    
    for i, gal in enumerate(galaxies):
        M_disk = gal['M_disk']
        Rd = gal['Rd']
        
        # Radial grid
        R_max = 50.0  # kpc
        N_pts = 500
        r = np.linspace(1e-3, R_max, N_pts)
        dr = r[1] - r[0]
        
        # Exponential disk baryonic density (Approximated as spherical for 1D PDE solver efficiency,
        # standard practice for fast evaluation, though SPARC uses actual disk potentials)
        # rho_b(r) = M_disk / (8 pi Rd^3) exp(-r/Rd)
        rho_b = M_disk / (8 * np.pi * Rd**3) * np.exp(-r / Rd)
        import scipy.integrate as integrate
        M_b_enc = integrate.cumulative_trapezoid(4 * np.pi * r**2 * rho_b, r, initial=0)
        
        # BARYONIC GRAVITY (Newtonian)
        g_N = G * M_b_enc / r**2
        v_bar2 = r * g_N
        
        # NPL LOGIC TENSION SOURCE (Article II.1 Compliance)
        # The logic field \Theta reacts to the baryonic gradient. 
        # The emergent logic tension density c_alpha is determined by the non-linear gradient of the field.
        # c_alpha = (1 / 4 pi G) * div( sqrt(a0 * |grad Phi_bar|) * r_hat )
        # This acts as the "Dark Matter" density entirely derived from the baryonic field.
        
        # Calculate divergence in spherical coordinates
        # div(F) = 1/r^2 d/dr(r^2 F)
        F_logic = np.sqrt(a0_kpc * g_N)
        r2F = r**2 * F_logic
        div_F = np.gradient(r2F, dr) / r**2
        
        c_alpha = div_F / (4 * np.pi * G)
        c_alpha[c_alpha < 0] = 0 # Logical tension can't be negative energy density
        
        # Total Density
        rho_tot = rho_b + c_alpha
        
        # SOLVE GLOBAL PDE
        Phi_tot, _ = solve_1d_poisson_spherical(r, rho_tot)
        
        # Recover Rotation Velocity: v^2 = r * dPhi/dr
        dPhi_dr = np.gradient(Phi_tot, dr)
        v_tot2 = r * dPhi_dr
        v_tot = np.sqrt(np.abs(v_tot2))
        
        # Mock Observation with typical 10% errors
        np.random.seed(42 + i)
        v_err = 0.05 * v_tot + 2.0
        v_obs = v_tot + np.random.normal(0, v_err)
        
        # Calculate Chi-Squared (No parameter tuning!)
        # We evaluate over the relevant optical radius (e.g. up to 5 Rd)
        eval_mask = r < 5 * Rd
        chi2 = np.sum(((v_obs[eval_mask] - v_tot[eval_mask]) / v_err[eval_mask])**2)
        ndof = np.sum(eval_mask)
        red_chi2 = chi2 / ndof if ndof > 0 else 0
        
        chi2_list.append(red_chi2)
        
        # Save one sample for plotting
        if i == 50: 
            sample_r = r
            sample_v_bar = np.sqrt(v_bar2)
            sample_v_tot = v_tot
            sample_v_obs = v_obs
            sample_v_err = v_err
            
    # Statistics
    mean_chi2 = np.mean(chi2_list)
    median_chi2 = np.median(chi2_list)
    good_fits = sum(1 for c in chi2_list if c < 5.0)
    
    print("\nRESULTS: NPL PDE SOLVER DEMO (MOCK DATA)")
    print("-" * 50)
    print(f"Total Mock Galaxies Evaluated: {n_galaxies}")
    print(f"Mean Reduced Chi-Squared: {mean_chi2:.2f}")
    print(f"Median Reduced Chi-Squared: {median_chi2:.2f}")
    print(f"Mock galaxies with chi^2 < 5.0: {good_fits} ({good_fits/n_galaxies*100:.1f}%)")

    if median_chi2 < 5.0 and good_fits/n_galaxies > 0.9:
        print("VERDICT: DEMO OK (solver reproduces its own mock data - NOT A GATE PASS)")
        status = "DEMO"
    else:
        print("VERDICT: DEMO FAIL (solver cannot even fit its own mock data)")
        status = "FAIL"
        
    # Visualization
    plt.figure(figsize=(12, 6))
    
    plt.subplot(121)
    plt.title("Sample TRXT-NPL Rotation Curve Fit")
    plt.errorbar(sample_r[::10], sample_v_obs[::10], yerr=sample_v_err[::10], fmt='o', color='white', alpha=0.5, label='SPARC Mock Obs')
    plt.plot(sample_r, sample_v_tot, color='cyan', linewidth=2, label='TRXT NPL Total $v(r)$')
    plt.plot(sample_r, sample_v_bar, color='red', linestyle='--', label='Baryonic $v(r)$')
    plt.xlabel('Radius (kpc)')
    plt.ylabel('Velocity (km/s)')
    plt.xlim(0, 30)
    plt.ylim(0, np.max(sample_v_tot)*1.2)
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
