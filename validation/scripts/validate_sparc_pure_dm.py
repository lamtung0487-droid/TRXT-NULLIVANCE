"""
TRXT Validation - Pure Lane-Emden (DM Only) Test
=================================================
This replicates the V4 manuscript "Pure Lane-Emden" test that 
reports 38% pass rate with median χ²_red = 11.77.

This is DM-ONLY - NO baryonic components (V_gas, V_disk, V_bul).
"""

import numpy as np
from scipy.integrate import odeint
from scipy.optimize import minimize
import json
from pathlib import Path
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')


G_NEWTON = 4.302e-6  # kpc (km/s)^2 / M_sun


def parse_sparc_data(filepath: str) -> dict:
    """Parse SPARC data file."""
    galaxies = defaultdict(lambda: {
        'R': [], 'Vobs': [], 'e_Vobs': [], 
        'Vgas': [], 'Vdisk': [], 'Vbul': [],
        'D': None
    })
    
    lines = None
    for encoding in ['utf-8', 'utf-16', 'utf-16-le', 'latin-1', 'cp1252']:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                lines = f.readlines()
            break
        except (UnicodeDecodeError, UnicodeError):
            continue
    
    if lines is None:
        return {}
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith(('Title:', 'Authors:', 'Table:', '=', '-', 'Byte', 'Note')):
            continue
        if 'Bytes' in line or 'Format' in line or 'Units' in line:
            continue
            
        parts = line.split()
        if len(parts) >= 9:
            try:
                galaxy_id = parts[0]
                D = float(parts[1])
                R = float(parts[2])
                Vobs = float(parts[3])
                e_Vobs = float(parts[4])
                Vgas = float(parts[5])
                Vdisk = float(parts[6])
                Vbul = float(parts[7])
                
                galaxies[galaxy_id]['R'].append(R)
                galaxies[galaxy_id]['Vobs'].append(Vobs)
                galaxies[galaxy_id]['e_Vobs'].append(e_Vobs)
                galaxies[galaxy_id]['Vgas'].append(Vgas)
                galaxies[galaxy_id]['Vdisk'].append(Vdisk)
                galaxies[galaxy_id]['Vbul'].append(Vbul)
                galaxies[galaxy_id]['D'] = D
            except (ValueError, IndexError):
                continue
    
    for gal_id in galaxies:
        for key in ['R', 'Vobs', 'e_Vobs', 'Vgas', 'Vdisk', 'Vbul']:
            galaxies[gal_id][key] = np.array(galaxies[gal_id][key])
    
    return dict(galaxies)


def lane_emden_ode(y, xi, n):
    theta, phi = y
    if xi < 1e-10:
        return [phi, 0.0]
    dtheta = phi
    dphi = -np.power(max(theta, 0), n) - 2 * phi / xi
    return [dtheta, dphi]


def solve_lane_emden(n: float, xi_max: float = 20.0, n_points: int = 500) -> tuple:
    xi = np.linspace(1e-6, xi_max, n_points)
    y0 = [1.0, 0.0]
    solution = odeint(lane_emden_ode, y0, xi, args=(n,))
    theta = solution[:, 0]
    return xi, theta


def compute_dm_velocity(R: np.ndarray, rho_0: float, r_0: float, n: float = 1.37) -> np.ndarray:
    """Compute DM-only rotation curve from Lane-Emden profile."""
    xi_arr, theta_arr = solve_lane_emden(n, xi_max=30.0, n_points=1000)
    
    V_DM = np.zeros_like(R)
    
    for i, r in enumerate(R):
        xi_r = r / r_0
        
        if xi_r >= xi_arr[-1]:
            theta_r = 0.0
        else:
            theta_r = np.interp(xi_r, xi_arr, theta_arr)
        
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


def fit_galaxy_pure_dm(galaxy_data: dict, n: float = 1.37) -> dict:
    """
    Fit PURE Lane-Emden (DM ONLY) to galaxy.
    NO BARYONS - This matches the V4 manuscript methodology.
    """
    R = galaxy_data['R']
    Vobs = galaxy_data['Vobs']
    e_Vobs = galaxy_data['e_Vobs']
    
    if len(R) < 3:
        return {'status': 'SKIP', 'reason': 'Too few points'}
    
    def objective(params):
        log_rho_0, log_r_0 = params
        rho_0 = 10**log_rho_0
        r_0 = 10**log_r_0
        
        if r_0 < 0.1 or r_0 > 100:
            return 1e10
        
        # PURE DM - NO BARYONS
        V_model = compute_dm_velocity(R, rho_0, r_0, n)
        
        sigma = np.sqrt(e_Vobs**2 + 5.0**2)
        chi2 = np.sum(((Vobs - V_model) / sigma)**2)
        return chi2
    
    r_0_init = np.median(R)
    rho_0_init = 1e7
    
    try:
        result = minimize(
            objective,
            x0=[np.log10(rho_0_init), np.log10(r_0_init)],
            method='Nelder-Mead',
            options={'maxiter': 500}
        )
        
        log_rho_0, log_r_0 = result.x
        rho_0 = 10**log_rho_0
        r_0 = 10**log_r_0
        chi2 = result.fun
        chi2_red = chi2 / max(len(R) - 2, 1)
        
        return {
            'status': 'OK',
            'rho_0': rho_0,
            'r_0': r_0,
            'chi2': chi2,
            'chi2_red': chi2_red,
            'n_points': len(R)
        }
        
    except Exception as e:
        return {'status': 'FAIL', 'reason': str(e)}


def main():
    print("=" * 70)
    print("TRXT VALIDATION - PURE LANE-EMDEN (DM ONLY)")
    print("Replicating V4 manuscript methodology (38% pass rate claim)")
    print("=" * 70)
    
    data_file = Path(__file__).parent.parent / "data" / "sparc" / "MassModels_Lelli2016c.txt"
    
    if not data_file.exists():
        print(f"ERROR: Data file not found: {data_file}")
        return None
    
    print(f"\n[Loading SPARC data...]")
    galaxies = parse_sparc_data(str(data_file))
    print(f"  Found {len(galaxies)} galaxies")
    
    n_poly = 1.37
    print(f"\n[Fitting PURE Lane-Emden (n={n_poly}, NO BARYONS)...]")
    
    results = {}
    n_pass = 0
    n_fail = 0
    chi2_reds = []
    
    for i, (gal_id, gal_data) in enumerate(galaxies.items()):
        fit_result = fit_galaxy_pure_dm(gal_data, n=n_poly)
        results[gal_id] = fit_result
        
        if fit_result['status'] == 'OK':
            chi2_reds.append(fit_result['chi2_red'])
            if fit_result['chi2_red'] < 5.0:
                n_pass += 1
            else:
                n_fail += 1
        
        if (i + 1) % 20 == 0:
            print(f"  Processed {i+1}/{len(galaxies)} galaxies...")
    
    chi2_reds = np.array(chi2_reds)
    median_chi2 = np.median(chi2_reds) if len(chi2_reds) > 0 else float('nan')
    mean_chi2 = np.mean(chi2_reds) if len(chi2_reds) > 0 else float('nan')
    pass_rate = n_pass / (n_pass + n_fail) * 100 if (n_pass + n_fail) > 0 else 0
    
    print(f"\n  ╔══════════════════════════════════════════════════════════╗")
    print(f"  ║  PURE LANE-EMDEN (DM ONLY) RESULTS                       ║")
    print(f"  ╠══════════════════════════════════════════════════════════╣")
    print(f"  ║  Total Galaxies     = {len(galaxies):4d}                              ║")
    print(f"  ║  Fitted Successfully= {len(chi2_reds):4d}                              ║")
    print(f"  ║  χ²_red < 5 (PASS)  = {n_pass:4d} ({pass_rate:.1f}%)                   ║")
    print(f"  ║  χ²_red ≥ 5 (FAIL)  = {n_fail:4d}                              ║")
    print(f"  ║  Median χ²_red      = {median_chi2:.2f}                            ║")
    print(f"  ║  Mean χ²_red        = {mean_chi2:.2f}                            ║")
    print(f"  ╠══════════════════════════════════════════════════════════╣")
    print(f"  ║  V4 MANUSCRIPT:     38%, median 11.77                    ║")
    print(f"  ║  THIS RUN:          {pass_rate:.1f}%, median {median_chi2:.2f}                    ║")
    print(f"  ╚══════════════════════════════════════════════════════════╝")
    
    summary = {
        'test_type': 'PURE_DM_ONLY',
        'n_galaxies': len(galaxies),
        'n_fitted': len(chi2_reds),
        'n_pass': n_pass,
        'n_fail': n_fail,
        'pass_rate_pct': pass_rate,
        'median_chi2_red': float(median_chi2),
        'mean_chi2_red': float(mean_chi2),
        'polytropic_n': n_poly,
        'v4_manuscript_pass_rate': 38.0,
        'v4_manuscript_median_chi2': 11.77
    }
    
    output_dir = Path(__file__).parent.parent / "outputs"
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / "sparc_pure_dm_validation.json"
    with open(output_file, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nResults saved to: {output_file}")
    
    return summary


if __name__ == "__main__":
    results = main()
