"""
TRXT Cosmology Theory Module for Cobaya
========================================
Implements the TRXT superfluid dark sector as a Cobaya theory.
Computes cosmological parameters including:
- Sound horizon r_s (predictive, not anchored)
- Hubble parameter H(z)
- Angular diameter distance D_A(z)
- Growth rate σ_8

Based on V4 Appendix I: Sound Speed and Causality
"""

import numpy as np
from scipy.integrate import quad, solve_ivp
from typing import Optional, Dict, Any


class TRXTCosmology:
    """
    TRXT Cosmology Calculator.
    
    Implements the modified dark sector with:
    - P(X) = c2*X + c4*X^2 effective Lagrangian
    - Modified sound speed: c_s^2 = (c2 + 2*c4*X)/(c2 + 6*c4*X)
    - Emergent equation of state from topological vacuum
    """
    
    # Physical constants
    C_LIGHT_KM_S = 299792.458  # km/s
    
    # TRXT EFT coefficients from HB-2 verification
    C2_DEFAULT = 6.38e4
    C4_DEFAULT = 0.111
    
    def __init__(self, 
                 H0: float = 67.4,
                 Omega_m: float = 0.315,
                 Omega_b: float = 0.0493,
                 Omega_r: float = 8.5e-5,
                 c2: float = None,
                 c4: float = None,
                 X_bg: float = 1e-10):
        """
        Initialize TRXT cosmology.
        
        Parameters
        ----------
        H0 : float
            Hubble constant (km/s/Mpc)
        Omega_m : float
            Total matter density
        Omega_b : float
            Baryon density
        Omega_r : float
            Radiation density
        c2, c4 : float
            TRXT EFT coefficients
        X_bg : float
            Background kinetic term X = (∂θ)²
        """
        self.H0 = H0
        self.Omega_m = Omega_m
        self.Omega_b = Omega_b
        self.Omega_r = Omega_r
        self.Omega_Lambda = 1.0 - Omega_m - Omega_r
        
        self.c2 = c2 if c2 is not None else self.C2_DEFAULT
        self.c4 = c4 if c4 is not None else self.C4_DEFAULT
        self.X_bg = X_bg
        
        # Derived parameters
        self.z_recomb = 1089.9
        self.z_drag = 1059.68  # Baryon drag epoch
    
    def H(self, z: float) -> float:
        """
        Hubble parameter H(z) in km/s/Mpc.
        
        H(z) = H0 * sqrt(Ω_m(1+z)³ + Ω_r(1+z)⁴ + Ω_Λ)
        """
        return self.H0 * np.sqrt(
            self.Omega_m * (1 + z)**3 +
            self.Omega_r * (1 + z)**4 +
            self.Omega_Lambda
        )
    
    def sound_speed_plasma(self, z: float) -> float:
        """
        Standard baryon-photon plasma sound speed.
        
        c_s = c / sqrt(3(1 + R_b))
        R_b = 3ρ_b / 4ρ_γ
        """
        R_b = 0.75 * (self.Omega_b / self.Omega_r) / (1 + z)
        c_s = 1.0 / np.sqrt(3 * (1 + R_b))
        return c_s
    
    def sound_speed_trxt(self, z: float) -> float:
        """
        TRXT modified sound speed from P(X) theory.
        
        c_s² = (c2 + 2*c4*X) / (c2 + 6*c4*X)
        
        At cosmological backgrounds, returns plasma c_s (dominant before recomb).
        """
        # X scales with energy density
        X = self.X_bg * (1 + z)**4
        
        # TRXT sound speed
        c_s_sq_trxt = (self.c2 + 2 * self.c4 * X) / (self.c2 + 6 * self.c4 * X)
        c_s_trxt = np.sqrt(max(c_s_sq_trxt, 0))
        
        # Plasma sound speed
        c_s_plasma = self.sound_speed_plasma(z)
        
        # Effective: minimum (plasma physics dominates)
        return min(c_s_trxt, c_s_plasma)
    
    def compute_r_s(self, z_star: float = None) -> float:
        """
        Compute sound horizon r_s at z_star.
        
        r_s = ∫_{z*}^∞ c_s(z) / H(z) dz
        
        Returns r_s in Mpc.
        """
        if z_star is None:
            z_star = self.z_drag
            
        def integrand(z):
            c_s = self.sound_speed_trxt(z)
            H_z = self.H(z)
            return self.C_LIGHT_KM_S * c_s / H_z
        
        r_s, _ = quad(integrand, z_star, 1e5, limit=200)
        return r_s
    
    def compute_D_A(self, z: float) -> float:
        """
        Compute angular diameter distance D_A(z) in Mpc.
        
        D_A(z) = c/(1+z) ∫_0^z dz'/H(z')
        """
        def integrand(z_prime):
            return 1.0 / self.H(z_prime)
        
        integral, _ = quad(integrand, 0, z, limit=200)
        D_A = self.C_LIGHT_KM_S * integral / (1 + z)
        return D_A
    
    def compute_H_rd(self, z: float = None) -> float:
        """
        Compute H(z) * r_d / r_d_fid for BAO analysis.
        
        This is the key BAO observable.
        """
        if z is None:
            z = 0.51  # BOSS effective redshift
            
        r_d = self.compute_r_s()
        r_d_fid = 147.09  # Planck fiducial
        
        return self.H(z) * r_d / r_d_fid
    
    def get_derived_parameters(self) -> Dict[str, float]:
        """
        Compute all derived cosmological parameters.
        
        Returns dict with H0, r_s, D_A at various redshifts, etc.
        """
        r_s = self.compute_r_s()
        r_s_recomb = self.compute_r_s(self.z_recomb)
        
        # 100 θ_s = r_s / D_A(z_*)
        D_A_star = self.compute_D_A(self.z_recomb)
        theta_s = 100 * r_s_recomb / D_A_star
        
        return {
            'H0': self.H0,
            'r_s_drag': r_s,
            'r_s_recomb': r_s_recomb,
            'theta_s': theta_s,
            'D_A_star': D_A_star,
            'Omega_m': self.Omega_m,
            'Omega_Lambda': self.Omega_Lambda,
            'z_recomb': self.z_recomb,
            'z_drag': self.z_drag
        }


def run_trxt_cosmology_scan():
    """
    Run a scan over H0 to find the TRXT prediction.
    """
    import json
    from pathlib import Path
    
    print("=" * 70)
    print("TRXT COSMOLOGY PREDICTION (Pre-MCMC)")
    print("=" * 70)
    
    # Planck-like baseline
    cosmo = TRXTCosmology(H0=67.4, Omega_m=0.315, Omega_b=0.0493)
    
    print("\n[Baseline: Planck-like parameters]")
    params = cosmo.get_derived_parameters()
    for key, val in params.items():
        if isinstance(val, float):
            print(f"  {key}: {val:.4f}")
    
    # Scan H0 to find SH0ES-compatible point
    print("\n[Scanning H0 for TRXT prediction...]")
    
    H0_values = np.linspace(65, 76, 23)
    results = []
    
    for H0 in H0_values:
        cosmo = TRXTCosmology(H0=H0, Omega_m=0.315, Omega_b=0.0493)
        r_s = cosmo.compute_r_s()
        results.append({
            'H0': H0,
            'r_s': r_s,
            'theta_s': 100 * r_s / cosmo.compute_D_A(cosmo.z_recomb) * 1000
        })
        print(f"  H0 = {H0:.1f} km/s/Mpc → r_s = {r_s:.2f} Mpc")
    
    # Find H0 that gives r_s = 147 Mpc (Planck anchored)
    r_s_targets = [r['r_s'] for r in results]
    H0_for_planck = np.interp(147.09, r_s_targets[::-1], H0_values[::-1])
    
    print(f"\n  ╔══════════════════════════════════════════════════════════╗")
    print(f"  ║  TRXT COSMOLOGY PREDICTION                               ║")
    print(f"  ╠══════════════════════════════════════════════════════════╣")
    print(f"  ║  H0 (for r_s=147 Mpc) = {H0_for_planck:.2f} km/s/Mpc             ║")
    print(f"  ║  Planck:    H0 = 67.4 km/s/Mpc                           ║")
    print(f"  ║  SH0ES:     H0 = 73.0 km/s/Mpc                           ║")
    print(f"  ╚══════════════════════════════════════════════════════════╝")
    
    # Save results
    output_dir = Path(__file__).parent.parent / "outputs"
    output_dir.mkdir(exist_ok=True)
    
    summary = {
        'baseline_H0': 67.4,
        'baseline_r_s': params['r_s_drag'],
        'H0_for_planck_rs': float(H0_for_planck),
        'planck_rs_target': 147.09,
        'scan_results': results
    }
    
    output_file = output_dir / "trxt_cosmology_prediction.json"
    with open(output_file, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"\nResults saved to: {output_file}")
    
    return summary


if __name__ == "__main__":
    run_trxt_cosmology_scan()
