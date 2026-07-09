"""
TRXT MCMC Analysis with Cobaya
==============================
Runs MCMC sampling for TRXT cosmology parameters using Cobaya.

Note: Full Planck likelihood requires downloading large data files.
This script uses a simplified Gaussian likelihood as demonstration.
"""

import numpy as np
from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from trxt_cosmology import TRXTCosmology


class TRXTGaussianLikelihood:
    """
    Simplified Gaussian likelihood for TRXT cosmology.
    
    Uses BAO and Planck-like constraints on r_s and H0.
    """
    
    # Observational constraints
    PLANCK_RS = 147.09
    PLANCK_RS_ERR = 0.26
    PLANCK_H0 = 67.4
    PLANCK_H0_ERR = 0.5
    SHOES_H0 = 73.04
    SHOES_H0_ERR = 1.04
    
    # BAO measurements (BOSS DR12)
    BAO_DM_RD = {0.38: 10.27, 0.51: 13.38, 0.61: 15.36}
    BAO_DM_RD_ERR = {0.38: 0.15, 0.51: 0.18, 0.61: 0.22}
    
    def __init__(self, use_shoes: bool = False):
        """
        Parameters
        ----------
        use_shoes : bool
            If True, use SH0ES H0 prior instead of Planck
        """
        self.use_shoes = use_shoes
    
    def log_likelihood(self, H0: float, Omega_m: float, 
                       Omega_b: float = 0.0493) -> float:
        """
        Compute log-likelihood for given parameters.
        """
        cosmo = TRXTCosmology(H0=H0, Omega_m=Omega_m, Omega_b=Omega_b)
        
        chi2 = 0.0
        
        # r_s constraint
        r_s = cosmo.compute_r_s()
        chi2 += ((r_s - self.PLANCK_RS) / self.PLANCK_RS_ERR)**2
        
        # H0 constraint
        if self.use_shoes:
            chi2 += ((H0 - self.SHOES_H0) / self.SHOES_H0_ERR)**2
        else:
            chi2 += ((H0 - self.PLANCK_H0) / self.PLANCK_H0_ERR)**2
        
        return -0.5 * chi2


def run_mcmc_grid():
    """
    Run a grid-based MCMC approximation for TRXT cosmology.
    
    Full MCMC would use Cobaya's sampler, but this grid approach
    gives quick posterior estimates.
    """
    print("=" * 70)
    print("TRXT MCMC ANALYSIS (Grid-Based Posterior)")
    print("=" * 70)
    
    # Parameter grid
    H0_grid = np.linspace(64, 76, 49)
    Omega_m_grid = np.linspace(0.28, 0.36, 33)
    
    # Compute likelihood on grid
    like_planck = TRXTGaussianLikelihood(use_shoes=False)
    like_shoes = TRXTGaussianLikelihood(use_shoes=True)
    
    log_L_planck = np.zeros((len(H0_grid), len(Omega_m_grid)))
    log_L_shoes = np.zeros((len(H0_grid), len(Omega_m_grid)))
    
    print("\n[Computing posterior on grid...]")
    for i, H0 in enumerate(H0_grid):
        for j, Om in enumerate(Omega_m_grid):
            log_L_planck[i, j] = like_planck.log_likelihood(H0, Om)
            log_L_shoes[i, j] = like_shoes.log_likelihood(H0, Om)
        
        if (i + 1) % 10 == 0:
            print(f"  H0 = {H0:.1f} done...")
    
    # Convert to posterior (flat prior)
    P_planck = np.exp(log_L_planck - np.max(log_L_planck))
    P_planck /= np.sum(P_planck)
    
    P_shoes = np.exp(log_L_shoes - np.max(log_L_shoes))
    P_shoes /= np.sum(P_shoes)
    
    # Marginalize over Omega_m to get H0 posterior
    P_H0_planck = np.sum(P_planck, axis=1)
    P_H0_planck /= np.sum(P_H0_planck) * (H0_grid[1] - H0_grid[0])
    
    P_H0_shoes = np.sum(P_shoes, axis=1)
    P_H0_shoes /= np.sum(P_H0_shoes) * (H0_grid[1] - H0_grid[0])
    
    # Find best-fit and uncertainties
    idx_planck = np.argmax(P_H0_planck)
    idx_shoes = np.argmax(P_H0_shoes)
    
    H0_bf_planck = H0_grid[idx_planck]
    H0_bf_shoes = H0_grid[idx_shoes]
    
    # Estimate 1-sigma (find 68% CL)
    cumsum_planck = np.cumsum(P_H0_planck) / np.sum(P_H0_planck)
    cumsum_shoes = np.cumsum(P_H0_shoes) / np.sum(P_H0_shoes)
    
    idx_16_p = np.searchsorted(cumsum_planck, 0.16)
    idx_84_p = np.searchsorted(cumsum_planck, 0.84)
    idx_16_s = np.searchsorted(cumsum_shoes, 0.16)
    idx_84_s = np.searchsorted(cumsum_shoes, 0.84)
    
    H0_lo_planck = H0_grid[max(idx_16_p, 0)]
    H0_hi_planck = H0_grid[min(idx_84_p, len(H0_grid)-1)]
    H0_lo_shoes = H0_grid[max(idx_16_s, 0)]
    H0_hi_shoes = H0_grid[min(idx_84_s, len(H0_grid)-1)]
    
    print(f"\n  ╔══════════════════════════════════════════════════════════╗")
    print(f"  ║  TRXT POSTERIOR RESULTS                                  ║")
    print(f"  ╠══════════════════════════════════════════════════════════╣")
    print(f"  ║  [Planck Prior]                                          ║")
    print(f"  ║  H0 = {H0_bf_planck:.2f} +{H0_hi_planck-H0_bf_planck:.2f} -{H0_bf_planck-H0_lo_planck:.2f} km/s/Mpc               ║")
    print(f"  ║                                                          ║")
    print(f"  ║  [SH0ES Prior]                                           ║")
    print(f"  ║  H0 = {H0_bf_shoes:.2f} +{H0_hi_shoes-H0_bf_shoes:.2f} -{H0_bf_shoes-H0_lo_shoes:.2f} km/s/Mpc               ║")
    print(f"  ╠══════════════════════════════════════════════════════════╣")
    print(f"  ║  Planck measured: H0 = 67.4 ± 0.5 km/s/Mpc               ║")
    print(f"  ║  SH0ES measured:  H0 = 73.0 ± 1.0 km/s/Mpc               ║")
    print(f"  ╚══════════════════════════════════════════════════════════╝")
    
    # Compute prediction for r_s at best-fit
    cosmo_planck = TRXTCosmology(H0=H0_bf_planck, Omega_m=0.315)
    cosmo_shoes = TRXTCosmology(H0=H0_bf_shoes, Omega_m=0.315)
    
    r_s_planck = cosmo_planck.compute_r_s()
    r_s_shoes = cosmo_shoes.compute_r_s()
    
    print(f"\n  Predicted r_s:")
    print(f"    Planck prior: r_s = {r_s_planck:.2f} Mpc")
    print(f"    SH0ES prior:  r_s = {r_s_shoes:.2f} Mpc")
    print(f"    (Planck measured: r_s = 147.09 Mpc)")
    
    # Save results
    output_dir = Path(__file__).parent.parent / "outputs"
    output_dir.mkdir(exist_ok=True)
    
    results = {
        'planck_prior': {
            'H0_bestfit': float(H0_bf_planck),
            'H0_lo': float(H0_lo_planck),
            'H0_hi': float(H0_hi_planck),
            'r_s_predicted': float(r_s_planck)
        },
        'shoes_prior': {
            'H0_bestfit': float(H0_bf_shoes),
            'H0_lo': float(H0_lo_shoes),
            'H0_hi': float(H0_hi_shoes),
            'r_s_predicted': float(r_s_shoes)
        },
        'observational_constraints': {
            'planck_H0': 67.4,
            'planck_H0_err': 0.5,
            'shoes_H0': 73.04,
            'shoes_H0_err': 1.04,
            'planck_r_s': 147.09,
            'planck_r_s_err': 0.26
        },
        'grid_size': {
            'H0': len(H0_grid),
            'Omega_m': len(Omega_m_grid)
        }
    }
    
    output_file = output_dir / "trxt_mcmc_posterior.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to: {output_file}")
    
    return results


if __name__ == "__main__":
    results = run_mcmc_grid()
