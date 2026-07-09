"""
TRXT Validation with Real SPARC Data
=====================================
Fits the TRXT Lane-Emden dark matter profile to REAL rotation curve data
from the SPARC database (175 galaxies).

Reference: Lelli, McGaugh, & Schombert (2016), AJ, 152, 157
Data source: http://astroweb.cwru.edu/SPARC/
"""

import numpy as np
from scipy.integrate import odeint
from scipy.optimize import minimize
import json
from pathlib import Path
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')


# =============================================================================
# Physical Constants
# =============================================================================
G_NEWTON = 4.302e-6  # kpc (km/s)^2 / M_sun


def parse_sparc_data(filepath: str) -> dict:
    """
    Parse SPARC MassModels data file.
    
    Returns dict with galaxy_id -> {'R': [], 'Vobs': [], 'e_Vobs': [], 'Vgas': [], 'Vdisk': [], 'Vbul': []}
    """
    galaxies = defaultdict(lambda: {
        'R': [], 'Vobs': [], 'e_Vobs': [], 
        'Vgas': [], 'Vdisk': [], 'Vbul': [],
        'D': None
    })
    
    # Try different encodings
    lines = None
    for encoding in ['utf-8', 'utf-16', 'utf-16-le', 'latin-1', 'cp1252']:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                lines = f.readlines()
            break
        except (UnicodeDecodeError, UnicodeError):
            continue
    
    if lines is None:
        print(f"ERROR: Could not decode file with any encoding")
        return {}
    
    # Skip header lines (starts with data after "---" lines)
    data_started = False
    header_count = 0
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Skip header section
        if line.startswith(('Title:', 'Authors:', 'Table:', '=', '-', 'Byte', 'Note')):
            continue
        if 'Bytes' in line or 'Format' in line or 'Units' in line:
            continue
            
        # Try to parse data line
        parts = line.split()
        if len(parts) >= 9:
            try:
                galaxy_id = parts[0]
                D = float(parts[1])      # Distance (Mpc)
                R = float(parts[2])      # Radius (kpc)
                Vobs = float(parts[3])   # Observed velocity (km/s)
                e_Vobs = float(parts[4]) # Error
                Vgas = float(parts[5])   # Gas contribution
                Vdisk = float(parts[6])  # Disk contribution
                Vbul = float(parts[7])   # Bulge contribution
                
                galaxies[galaxy_id]['R'].append(R)
                galaxies[galaxy_id]['Vobs'].append(Vobs)
                galaxies[galaxy_id]['e_Vobs'].append(e_Vobs)
                galaxies[galaxy_id]['Vgas'].append(Vgas)
                galaxies[galaxy_id]['Vdisk'].append(Vdisk)
                galaxies[galaxy_id]['Vbul'].append(Vbul)
                galaxies[galaxy_id]['D'] = D
            except (ValueError, IndexError):
                continue
    
    # Convert to numpy arrays
    for gal_id in galaxies:
        for key in ['R', 'Vobs', 'e_Vobs', 'Vgas', 'Vdisk', 'Vbul']:
            galaxies[gal_id][key] = np.array(galaxies[gal_id][key])
    
    return dict(galaxies)


def lane_emden_ode(y, xi, n):
    """
    Lane-Emden equation: d²θ/dξ² + (2/ξ)dθ/dξ + θⁿ = 0
    
    Rewritten as system:
    dθ/dξ = φ
    dφ/dξ = -θⁿ - 2φ/ξ
    """
    theta, phi = y
    
    if xi < 1e-10:
        return [phi, 0.0]
    
    dtheta = phi
    dphi = -np.power(max(theta, 0), n) - 2 * phi / xi
    
    return [dtheta, dphi]


def solve_lane_emden(n: float, xi_max: float = 20.0, n_points: int = 500) -> tuple:
    """
    Solve Lane-Emden equation for polytropic index n.
    
    Returns (xi, theta) arrays.
    """
    xi = np.linspace(1e-6, xi_max, n_points)
    
    # Initial conditions: θ(0) = 1, θ'(0) = 0
    y0 = [1.0, 0.0]
    
    solution = odeint(lane_emden_ode, y0, xi, args=(n,))
    theta = solution[:, 0]
    
    return xi, theta


def compute_dm_velocity(R: np.ndarray, rho_0: float, r_0: float, n: float = 1.37) -> np.ndarray:
    """
    Compute dark matter contribution to rotation curve from Lane-Emden profile.
    
    V_DM²(R) = G * M_DM(<R) / R
    
    For polytropic profile: ρ(r) = ρ_0 * θ^n(r/r_0)
    """
    xi_arr, theta_arr = solve_lane_emden(n, xi_max=30.0, n_points=1000)
    
    V_DM = np.zeros_like(R)
    
    for i, r in enumerate(R):
        xi_r = r / r_0
        
        # Find theta at this radius
        if xi_r >= xi_arr[-1]:
            theta_r = 0.0
        else:
            theta_r = np.interp(xi_r, xi_arr, theta_arr)
        
        # Enclosed mass integral: M(<r) ∝ ∫ξ²θⁿ dξ
        mask = xi_arr <= xi_r
        if np.sum(mask) < 2:
            M_enclosed = 0.0
        else:
            xi_int = xi_arr[mask]
            theta_int = np.maximum(theta_arr[mask], 0)
            integrand = xi_int**2 * np.power(theta_int, n)
            M_enclosed = 4 * np.pi * rho_0 * r_0**3 * np.trapz(integrand, xi_int)
        
        if r > 0 and M_enclosed > 0:
            V_DM[i] = np.sqrt(G_NEWTON * M_enclosed / r)
        else:
            V_DM[i] = 0.0
    
    return V_DM


def fit_galaxy(galaxy_data: dict, n: float = 1.37, ML_disk: float = 0.5) -> dict:
    """
    Fit TRXT model to a single galaxy.
    
    Model: V_tot² = V_gas² + (ML_disk * V_disk)² + V_DM²
    
    Free parameters: rho_0, r_0 (and optionally ML_disk)
    
    Returns fit results with chi2.
    """
    R = galaxy_data['R']
    Vobs = galaxy_data['Vobs']
    e_Vobs = galaxy_data['e_Vobs']
    Vgas = galaxy_data['Vgas']
    Vdisk = galaxy_data['Vdisk']
    Vbul = galaxy_data['Vbul']
    
    if len(R) < 3:
        return {'status': 'SKIP', 'reason': 'Too few points'}
    
    # Baryonic contribution with M/L scaling
    def V_bar_squared(ML):
        return Vgas**2 + (ML * Vdisk)**2 + (ML * Vbul)**2
    
    # Objective function
    def objective(params):
        log_rho_0, log_r_0, ML = params
        rho_0 = 10**log_rho_0
        r_0 = 10**log_r_0
        
        if r_0 < 0.1 or r_0 > 100:
            return 1e10
        if ML < 0.1 or ML > 2.0:
            return 1e10
        
        V_DM = compute_dm_velocity(R, rho_0, r_0, n)
        V_bar_sq = V_bar_squared(ML)
        V_model = np.sqrt(V_bar_sq + V_DM**2)
        
        # Add systematic floor
        sigma = np.sqrt(e_Vobs**2 + 5.0**2)  # 5 km/s systematic
        
        chi2 = np.sum(((Vobs - V_model) / sigma)**2)
        return chi2
    
    # Initial guess
    r_0_init = np.median(R)
    rho_0_init = 1e7  # M_sun / kpc^3
    
    try:
        result = minimize(
            objective,
            x0=[np.log10(rho_0_init), np.log10(r_0_init), 0.5],
            method='Nelder-Mead',
            options={'maxiter': 500}
        )
        
        log_rho_0, log_r_0, ML = result.x
        rho_0 = 10**log_rho_0
        r_0 = 10**log_r_0
        chi2 = result.fun
        chi2_red = chi2 / max(len(R) - 3, 1)
        
        # Compute final velocities
        V_DM = compute_dm_velocity(R, rho_0, r_0, n)
        V_bar_sq = Vgas**2 + (ML * Vdisk)**2 + (ML * Vbul)**2
        V_model = np.sqrt(V_bar_sq + V_DM**2)
        
        return {
            'status': 'OK',
            'rho_0': rho_0,
            'r_0': r_0,
            'ML': ML,
            'chi2': chi2,
            'chi2_red': chi2_red,
            'n_points': len(R),
            'V_model': V_model.tolist(),
            'V_obs': Vobs.tolist(),
            'R': R.tolist()
        }
        
    except Exception as e:
        return {'status': 'FAIL', 'reason': str(e)}


def main():
    """
    Main validation routine with REAL SPARC data.
    """
    print("=" * 70)
    print("TRXT VALIDATION WITH REAL SPARC DATA")
    print("=" * 70)
    
    # Load data
    data_file = Path(__file__).parent.parent / "data" / "sparc" / "MassModels_Lelli2016c.txt"
    
    if not data_file.exists():
        print(f"ERROR: Data file not found: {data_file}")
        return None
    
    print(f"\n[Loading SPARC data from: {data_file}]")
    galaxies = parse_sparc_data(str(data_file))
    print(f"  Found {len(galaxies)} galaxies")
    
    # Polytropic index from TRXT theory
    n_poly = 1.37
    print(f"\n[Fitting with Lane-Emden profile, n = {n_poly}]")
    
    # Fit all galaxies
    results = {}
    n_pass = 0
    n_fail = 0
    chi2_reds = []
    
    print("\n[Processing galaxies...]")
    for i, (gal_id, gal_data) in enumerate(galaxies.items()):
        fit_result = fit_galaxy(gal_data, n=n_poly)
        results[gal_id] = fit_result
        
        if fit_result['status'] == 'OK':
            chi2_reds.append(fit_result['chi2_red'])
            if fit_result['chi2_red'] < 5.0:
                n_pass += 1
            else:
                n_fail += 1
        
        if (i + 1) % 20 == 0:
            print(f"  Processed {i+1}/{len(galaxies)} galaxies...")
    
    # Statistics
    chi2_reds = np.array(chi2_reds)
    median_chi2 = np.median(chi2_reds) if len(chi2_reds) > 0 else float('nan')
    mean_chi2 = np.mean(chi2_reds) if len(chi2_reds) > 0 else float('nan')
    pass_rate = n_pass / (n_pass + n_fail) * 100 if (n_pass + n_fail) > 0 else 0
    
    print(f"\n  ╔══════════════════════════════════════════════════════════╗")
    print(f"  ║  REAL DATA VALIDATION RESULTS                            ║")
    print(f"  ╠══════════════════════════════════════════════════════════╣")
    print(f"  ║  Total Galaxies     = {len(galaxies):4d}                              ║")
    print(f"  ║  Fitted Successfully= {len(chi2_reds):4d}                              ║")
    print(f"  ║  χ²_red < 5 (PASS)  = {n_pass:4d} ({pass_rate:.1f}%)                   ║")
    print(f"  ║  χ²_red ≥ 5 (FAIL)  = {n_fail:4d}                              ║")
    print(f"  ║  Median χ²_red      = {median_chi2:.2f}                             ║")
    print(f"  ║  Mean χ²_red        = {mean_chi2:.2f}                             ║")
    print(f"  ╠══════════════════════════════════════════════════════════╣")
    print(f"  ║  OVERALL: {'PASS ✓' if pass_rate > 50 else 'FAIL ✗'}                                        ║")
    print(f"  ╚══════════════════════════════════════════════════════════╝")
    
    # Save results
    output_dir = Path(__file__).parent.parent / "outputs"
    output_dir.mkdir(exist_ok=True)
    
    summary = {
        'n_galaxies': len(galaxies),
        'n_fitted': len(chi2_reds),
        'n_pass': n_pass,
        'n_fail': n_fail,
        'pass_rate_pct': pass_rate,
        'median_chi2_red': float(median_chi2),
        'mean_chi2_red': float(mean_chi2),
        'polytropic_n': n_poly,
        'data_source': 'SPARC (Lelli et al. 2016)',
        'threshold_chi2': 5.0
    }
    
    output_file = output_dir / "sparc_real_data_validation.json"
    with open(output_file, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nSummary saved to: {output_file}")
    
    # Save per-galaxy results
    detailed_file = output_dir / "sparc_per_galaxy_results.json"
    with open(detailed_file, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"Detailed results saved to: {detailed_file}")
    
    return summary


if __name__ == "__main__":
    results = main()
