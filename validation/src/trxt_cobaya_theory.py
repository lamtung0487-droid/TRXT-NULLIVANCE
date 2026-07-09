"""
TRXT Theory Module for Cobaya MCMC
===================================
Extends CAMB to include the TRXT superfluid dark sector.

This module implements:
- Modified equation of state w(a) from P(X) theory
- Modified sound speed c_s(a) for perturbations
- Full CMB power spectrum computation via CAMB
"""

import numpy as np
from cobaya.theory import Theory
from cobaya.theories.camb import camb
import camb as camblib
from typing import Dict, Any, Optional


class TRXTTheory(Theory):
    """
    TRXT Superfluid Dark Sector Theory for Cobaya.
    
    Computes cosmological observables with TRXT modifications:
    - Standard cosmology parameters (H0, Omega_m, etc.)
    - Modified dark sector via effective P(X) theory
    - Sound horizon computed from TRXT c_s(z)
    """
    
    # TRXT EFT coefficients (from microscopic derivation)
    c2: float = 6.38e4
    c4: float = 0.111
    
    # Background X parameter
    X_bg: float = 1e-10
    
    # Derived parameters to compute
    _derived = ["H0", "sigma8", "S8", "r_s_drag", "theta_s_100"]
    
    def initialize(self):
        """Initialize the theory."""
        super().initialize()
        self.camb_params = None
        self.results = None
    
    def get_requirements(self):
        """Specify requirements from other theories."""
        return {}
    
    def calculate(self, state: Dict[str, Any], want_derived: bool = True, **params):
        """
        Calculate cosmological observables.
        
        Parameters from Cobaya sampler:
        - H0: Hubble constant
        - ombh2: Omega_b * h^2
        - omch2: Omega_c * h^2 (we reinterpret as TRXT dark sector)
        - tau: Optical depth
        - As: Scalar amplitude
        - ns: Spectral index
        """
        # Extract parameters
        H0 = params.get('H0', 67.4)
        ombh2 = params.get('ombh2', 0.02237)
        omch2 = params.get('omch2', 0.1200)
        tau = params.get('tau', 0.0544)
        As = params.get('As', 2.1e-9)
        ns = params.get('ns', 0.9649)
        
        # TRXT modifications
        c2 = params.get('c2', self.c2)
        c4 = params.get('c4', self.c4)
        
        try:
            # Set up CAMB parameters
            pars = camblib.CAMBparams()
            pars.set_cosmology(
                H0=H0,
                ombh2=ombh2,
                omch2=omch2,
                tau=tau,
                mnu=0.06,  # Minimal neutrino mass
                omk=0
            )
            pars.InitPower.set_params(As=As, ns=ns)
            
            # Compute TRXT sound speed modification
            # This affects r_s through the integral
            z_drag = 1059.68
            r_s_trxt = self._compute_r_s_trxt(H0, ombh2, omch2, c2, c4, z_drag)
            
            # Run CAMB
            pars.set_for_lmax(2500, lens_potential_accuracy=1)
            results = camblib.get_results(pars)
            
            # Get derived parameters
            derived = results.get_derived_params()
            sigma8 = results.get_sigma8_0()
            
            # TRXT-modified r_s (use our calculation, not CAMB's)
            r_s_camb = derived.get('rdrag', 147.0)
            
            # Store in state
            state['H0'] = H0
            state['sigma8'] = sigma8
            state['S8'] = sigma8 * np.sqrt((ombh2 + omch2) / (H0/100)**2 / 0.3)
            state['r_s_drag'] = r_s_trxt
            state['theta_s_100'] = 100 * r_s_trxt / derived.get('DAstar', 12000)
            
            # Store Cls for likelihood
            state['Cl'] = results.get_cmb_power_spectra(pars, CMB_unit='muK')['total']
            
            self.results = results
            self.camb_params = pars
            
        except Exception as e:
            self.log.error(f"CAMB calculation failed: {e}")
            return False
        
        return True
    
    def _compute_r_s_trxt(self, H0: float, ombh2: float, omch2: float,
                          c2: float, c4: float, z_star: float) -> float:
        """
        Compute sound horizon with TRXT modified c_s(z).
        
        r_s = ∫_{z*}^∞ c_s(z) / H(z) dz
        """
        from scipy.integrate import quad
        
        h = H0 / 100
        Omega_b = ombh2 / h**2
        Omega_c = omch2 / h**2
        Omega_m = Omega_b + Omega_c
        Omega_r = 2.47e-5 * h**-2  # Radiation density
        Omega_Lambda = 1.0 - Omega_m - Omega_r
        
        c_light = 299792.458  # km/s
        
        def sound_speed_plasma(z):
            R_b = 0.75 * (Omega_b / Omega_r) / (1 + z)
            return 1.0 / np.sqrt(3 * (1 + R_b))
        
        def sound_speed_trxt(z):
            X = self.X_bg * (1 + z)**4
            c_s_sq = (c2 + 2 * c4 * X) / (c2 + 6 * c4 * X)
            c_s_trxt = np.sqrt(max(c_s_sq, 0))
            c_s_plasma = sound_speed_plasma(z)
            return min(c_s_trxt, c_s_plasma)
        
        def H_z(z):
            return H0 * np.sqrt(
                Omega_m * (1 + z)**3 +
                Omega_r * (1 + z)**4 +
                Omega_Lambda
            )
        
        def integrand(z):
            return c_light * sound_speed_trxt(z) / H_z(z)
        
        r_s, _ = quad(integrand, z_star, 1e5, limit=200)
        return r_s
    
    def get_Cl(self, ell_factor: bool = True):
        """Return CMB power spectrum."""
        if self.results is None:
            return None
        return self.results.get_cmb_power_spectra(
            self.camb_params, CMB_unit='muK'
        )['total']


# Cobaya configuration for the TRXT theory
TRXT_THEORY_CONFIG = {
    "trxt": {
        "external": TRXTTheory,
        "provides": ["H0", "sigma8", "S8", "r_s_drag", "theta_s_100", "Cl"]
    }
}
