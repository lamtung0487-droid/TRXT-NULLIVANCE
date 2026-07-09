"""
Run validation on the full SPARC sample dataset.
Uses the 5-galaxy sample to demonstrate the Lane-Emden fit.
For full 175 galaxies, download from http://astroweb.cwru.edu/SPARC/
"""
import sys
sys.path.insert(0, 'src')

import numpy as np
from sparc_data_loader import parse_rotmod_mrt
from rotation_curves import fit_galaxy_rotation
import json

# Load data (prioritize full manual download)
import os
data_dir = 'data/sparc'
mass_models_file = os.path.join(data_dir, 'MassModels_Lelli2016c.mrt')
sample_file = os.path.join(data_dir, 'sample_rotmod.mrt')

if os.path.exists(mass_models_file):
    print(f"Loading FULL dataset from: {mass_models_file}")
    # Use load_sparc_data which handles file detection
    from sparc_data_loader import load_sparc_data
    galaxies = load_sparc_data('data')
    data_file = mass_models_file
else:
    print(f"Full dataset not found at {mass_models_file}")
    print(f"Loading SAMPLE dataset from: {sample_file}")
    galaxies = parse_rotmod_mrt(sample_file)
    data_file = sample_file

print('='*70)
print('LANE-EMDEN VALIDATION ON SPARC ROTATION CURVES')
print('='*70)
print(f'Data file: {data_file}')
print(f'Galaxies loaded: {len(galaxies)}')
print(f'Polytropic index: n = 1.37 (fixed)')
print('-'*70)
print(f'{"Galaxy":<12} {"N_pts":<6} {"chi2_red":<10} {"M_total":<14} {"v_max":<10} {"Status"}')
print('-'*70)

n = 1.37
results = []
chi2_list = []

for name, gal in sorted(galaxies.items()):
    result = fit_galaxy_rotation(
        gal.r_kpc, 
        gal.v_obs, 
        gal.v_err, 
        n=n
    )
    
    chi2_red = result['chi2_red']
    M_total = result['M_total']
    v_max = max(gal.v_obs)
    passed = chi2_red < 5.0
    status = "✓ PASS" if passed else "✗ FAIL"
    
    print(f'{name:<12} {len(gal.r_kpc):<6} {chi2_red:<10.3f} {M_total:<14.2e} {v_max:<10.1f} {status}')
    
    results.append({
        'galaxy': name,
        'n_points': int(len(gal.r_kpc)),
        'chi2_red': float(chi2_red),
        'M_total': float(M_total),
        'v_max': float(v_max),
        'pass': bool(passed)
    })
    chi2_list.append(chi2_red)

print('-'*70)
n_pass = sum(1 for r in results if r['pass'])
median_chi2 = np.median(chi2_list)
mean_chi2 = np.mean(chi2_list)

print(f'\nSUMMARY:')
print(f'  Galaxies tested: {len(results)}')
print(f'  Passed (chi2 < 5): {n_pass}/{len(results)} ({100*n_pass/len(results):.0f}%)')
print(f'  Median chi2_red: {median_chi2:.3f}')
print(f'  Mean chi2_red: {mean_chi2:.3f}')
print('='*70)

if n_pass == len(results):
    print('\n🎉 VALIDATION SUCCESS: All galaxies fit with chi2_red < 5')
    verdict = "FULL_PASS"
elif n_pass / len(results) >= 0.6:
    print('\n✅ VALIDATION PARTIAL SUCCESS: Majority of galaxies fit well')
    verdict = "PARTIAL_PASS"
else:
    print('\n⚠️ VALIDATION NEEDS REVIEW: Many galaxies have poor fits')
    verdict = "NEEDS_REVIEW"

# Save results to JSON
output_file = 'outputs/runs/sparc_validation_results.json'
import os
os.makedirs('outputs/runs', exist_ok=True)

with open(output_file, 'w') as f:
    json.dump({
        'n': n,
        'n_galaxies': len(results),
        'n_pass': n_pass,
        'median_chi2_red': median_chi2,
        'mean_chi2_red': mean_chi2,
        'verdict': verdict,
        'galaxies': results
    }, f, indent=2)

print(f'\nResults saved to: {output_file}')
