"""
TRXT Validation - EXACT V4 Methodology Replication
===================================================
Uses the EXACT same methodology as rotation_curves.py and V4 manuscript
to replicate the 38% pass rate claim.

Key differences from my previous scripts:
- v_err floor = 1.0 km/s (not σ_sys = 5 km/s)
- DoF = n_points - 1 (only M_total is free, n is fixed)
- minimize_scalar on log_M in [8, 14]
- Uses fit_galaxy_rotation from rotation_curves.py
"""

import numpy as np
import sys
from pathlib import Path
import json
from collections import defaultdict

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rotation_curves import fit_galaxy_rotation


def parse_sparc_data(filepath: str) -> dict:
    """Parse SPARC data file."""
    galaxies = defaultdict(lambda: {
        'R': [], 'Vobs': [], 'e_Vobs': [], 
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
        if len(parts) >= 5:
            try:
                galaxy_id = parts[0]
                D = float(parts[1])
                R = float(parts[2])
                Vobs = float(parts[3])
                e_Vobs = float(parts[4])
                
                galaxies[galaxy_id]['R'].append(R)
                galaxies[galaxy_id]['Vobs'].append(Vobs)
                galaxies[galaxy_id]['e_Vobs'].append(e_Vobs)
                galaxies[galaxy_id]['D'] = D
            except (ValueError, IndexError):
                continue
    
    for gal_id in galaxies:
        for key in ['R', 'Vobs', 'e_Vobs']:
            galaxies[gal_id][key] = np.array(galaxies[gal_id][key])
    
    return dict(galaxies)


def main():
    print("=" * 70)
    print("TRXT VALIDATION - EXACT V4 METHODOLOGY REPLICATION")
    print("Using rotation_curves.fit_galaxy_rotation (PURE DM, 1 param)")
    print("=" * 70)
    
    data_file = Path(__file__).parent.parent / "data" / "sparc" / "MassModels_Lelli2016c.txt"
    
    if not data_file.exists():
        print(f"ERROR: Data file not found: {data_file}")
        return None
    
    print(f"\n[Loading SPARC data...]")
    galaxies = parse_sparc_data(str(data_file))
    print(f"  Found {len(galaxies)} galaxies")
    
    n_poly = 1.37
    print(f"\n[Fitting with EXACT V4 rotation_curves.py methodology (n={n_poly}, 1 param)...]")
    
    results = {}
    n_pass = 0
    n_fail = 0
    chi2_reds = []
    
    for i, (gal_id, gal_data) in enumerate(galaxies.items()):
        R = gal_data['R']
        Vobs = gal_data['Vobs']
        e_Vobs = gal_data['e_Vobs']
        
        if len(R) < 3:
            continue
            
        try:
            # Use EXACT V4 function (PURE DM, no baryons)
            fit_result = fit_galaxy_rotation(R, Vobs, e_Vobs, n=n_poly)
            
            results[gal_id] = fit_result
            chi2_reds.append(fit_result['chi2_red'])
            
            if fit_result['chi2_red'] < 5.0:
                n_pass += 1
            else:
                n_fail += 1
                
        except Exception as e:
            results[gal_id] = {'status': 'FAIL', 'reason': str(e)}
        
        if (i + 1) % 20 == 0:
            print(f"  Processed {i+1}/{len(galaxies)} galaxies...")
    
    chi2_reds = np.array(chi2_reds)
    median_chi2 = np.median(chi2_reds) if len(chi2_reds) > 0 else float('nan')
    mean_chi2 = np.mean(chi2_reds) if len(chi2_reds) > 0 else float('nan')
    pass_rate = n_pass / (n_pass + n_fail) * 100 if (n_pass + n_fail) > 0 else 0
    
    print(f"\n  ╔══════════════════════════════════════════════════════════╗")
    print(f"  ║  EXACT V4 METHODOLOGY RESULTS                            ║")
    print(f"  ╠══════════════════════════════════════════════════════════╣")
    print(f"  ║  Total Galaxies     = {len(galaxies):4d}                              ║")
    print(f"  ║  Fitted Successfully= {len(chi2_reds):4d}                              ║")
    print(f"  ║  χ²_red < 5 (PASS)  = {n_pass:4d} ({pass_rate:.1f}%)                   ║")
    print(f"  ║  χ²_red ≥ 5 (FAIL)  = {n_fail:4d}                              ║")
    print(f"  ║  Median χ²_red      = {median_chi2:.2f}                            ║")
    print(f"  ║  Mean χ²_red        = {mean_chi2:.2f}                            ║")
    print(f"  ╠══════════════════════════════════════════════════════════╣")
    print(f"  ║  V4 MANUSCRIPT CLAIMS: 38%, median 11.77                 ║")
    print(f"  ║  THIS RUN (exact V4): {pass_rate:.1f}%, median {median_chi2:.2f}                   ║")
    print(f"  ╚══════════════════════════════════════════════════════════╝")
    
    # Calculate discrepancy
    if abs(pass_rate - 38.0) < 5:
        match_status = "MATCH ✓"
    else:
        match_status = "DISCREPANCY"
        
    print(f"\n  Comparison with V4 claim: {match_status}")
    
    summary = {
        'test_type': 'EXACT_V4_METHODOLOGY',
        'n_galaxies': len(galaxies),
        'n_fitted': len(chi2_reds),
        'n_pass': n_pass,
        'n_fail': n_fail,
        'pass_rate_pct': pass_rate,
        'median_chi2_red': float(median_chi2),
        'mean_chi2_red': float(mean_chi2),
        'polytropic_n': n_poly,
        'v4_claim_pass_rate': 38.0,
        'v4_claim_median_chi2': 11.77,
        'match_status': match_status
    }
    
    output_dir = Path(__file__).parent.parent / "outputs"
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / "sparc_exact_v4_methodology.json"
    with open(output_file, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nResults saved to: {output_file}")
    
    return summary


if __name__ == "__main__":
    results = main()
