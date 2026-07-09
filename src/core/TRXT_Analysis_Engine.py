import numpy as np
import matplotlib.pyplot as plt
from scipy.special import voigt_profile
from scipy.stats import chi2
from scipy.optimize import curve_fit

class TRXTAnalyzer:
    """
    TRXT-Nullivance V14 Analysis Engine (Rectified V14.1).
    Improved statistics: H0/H1 Log-Likelihood Ratio test, Voigt Profiles.
    """

    def __init__(self):
        # Locked Generators
        self.ALPHA_INV = 137.035999
        self.X_FACTOR = 1.5 * self.ALPHA_INV
        self.M_TAU = 1.77686
        self.M_STAR = self.M_TAU * self.X_FACTOR
        print(f"[TRXT] Engine V14.1 Initialized. M* = {self.M_STAR:.4f} GeV")

    def predict_mass(self, p, q):
        return self.M_STAR * (1.0/p + 1.0/q)

    def extended_background(self, x, a0, a1, a2):
        """
        Flexible background model: Exponential poly or Power law.
        Using Bernstein-like or Exp-poly for stability in 40-60 GeV.
        Fit func: exp(a0 + a1*x + a2*x^2)
        """
        # Centering x to reduce correlation
        xc = (x - 50.0) / 10.0
        return np.exp(a0 + a1*xc + a2*xc**2)

    def generate_voigt_template(self, axis, mass, width_gamma, width_sigma, amp):
        """
        Voigt Profile: Convolution of Lorentzian (Theory) & Gaussian (Detector).
        gamma: intrinsic width (theory).
        sigma: detector resolution.
        """
        return amp * voigt_profile(axis - mass, width_sigma, width_gamma/2.0)

    def perform_statistical_test(self, x_data, y_data, target_mass):
        """
        Rigorous H0 vs H1 test using Likelihood Ratio.
        Corrected for Phase 2.2: Nested models and Poisson weighting.
        """
        print(f"\n[STATISTICS] Testing Signal Hypothesis at {target_mass:.2f} GeV...")
        
        # Errors (Poisson approximation)
        # For bins with 0 counts, we must handle carefully.
        # Common practice in weighted LS: use sigma=1 or Garwood interval.
        # Here we use sqrt(N) but set min error to 1.0 for N=0 to avoid division by zero.
        y_err = np.sqrt(y_data)
        y_err[y_err == 0] = 1.0 
        
        # --- 1. Fit H0 (Background Only) ---
        # Model: Simple Exponential or Poly-Exp to fit the smooth background
        def func_h0(x, a0, a1, a2):
            return self.extended_background(x, a0, a1, a2)
            
        try:
            # Initial guess
            p0_bg = [np.log(np.max(y_data)+1), -0.1, 0.0]
            
            popt_h0, pcov_h0 = curve_fit(func_h0, x_data, y_data, sigma=y_err, p0=p0_bg, absolute_sigma=True)
            
            fit_y_h0 = func_h0(x_data, *popt_h0)
            chi2_h0 = np.sum(((y_data - fit_y_h0) / y_err)**2)
            ndof_h0 = len(x_data) - len(popt_h0)
            print(f" -> H0 (Background) Chi2/Ndof = {chi2_h0:.2f} / {ndof_h0}")
            
        except Exception as e:
            print(f" -> H0 Fit failed: {e}")
            return None

        # --- 2. Fit H1 (Background + Signal) ---
        # KEY CORRECTION: Must be Nested. H1 = H0 + Signal.
        # If Signal Amplitude -> 0, H1 must reduce exactly to H0.
        
        # Resolution fixed to detector performance (approx 1% mass)
        detector_sigma = 0.01 * target_mass 
        
        def func_h1(x, a0, a1, a2, strength, width_gamma):
            # Same BG function as H0
            bg = self.extended_background(x, a0, a1, a2)
            # Voigt Signal
            sig = self.generate_voigt_template(x, target_mass, width_gamma, detector_sigma, strength)
            return bg + sig
            
        try:
            # Init guess: Start with H0 params for BG part, small signal
            p0_h1 = [*popt_h0, 0.1, 2.0] 
            
            # Bounds
            # BG params: essentially unbounded (within reason)
            # Strength > 0 (looking for excess), Width in [0.1, 5.0]
            inf = np.inf
            bounds_lower = [-inf, -inf, -inf, 0.0, 0.1]
            bounds_upper = [ inf,  inf,  inf, inf, 5.0] 
            
            popt_h1, pcov_h1 = curve_fit(func_h1, x_data, y_data, sigma=y_err, p0=p0_h1, bounds=(bounds_lower, bounds_upper), absolute_sigma=True)
             
            fit_y_h1 = func_h1(x_data, *popt_h1)
            chi2_h1 = np.sum(((y_data - fit_y_h1) / y_err)**2)
            
            # Extra params used: Strength, Width (2 params)
            ndof_h1 = len(x_data) - len(popt_h1)
            print(f" -> H1 (Signal+BG) Chi2/Ndof = {chi2_h1:.2f} / {ndof_h1}")
            
            # --- 3. Likelihood Ratio Test ---
            delta_chi2 = chi2_h0 - chi2_h1
            
            # Significance estimation
            # Warning: Standard sqrt(dChi2) applies when null is not on boundary.
            # Here strength=0 is on boundary.
            # Chernoff's Theorem suggests distribution is 0.5*Chi2(1) + 0.5*delta(0) for 1 param.
            # For 2 params (amp, width) it's more complex.
            # However, for "Discovery" screening, sqrt(dChi2) is a common "Local Significance" proxy.
            
            if delta_chi2 > 0:
                # Naive approximation for local significance
                significance = np.sqrt(delta_chi2)
                
                # Correction for 2 extra DOFs (Look-elsewhere effect etc not handled here, but local p-value adjustment needed)
                # Roughly, for 2 dof, Z ~ sqrt(dChi2) is slightly optimistic.
                # Just reporting dChi2 and Z_naive is standard first step.
            else:
                significance = 0.0
                
            print(f" -> Delta Chi2 = {delta_chi2:.2f}")
            print(f" -> Local Significance (Naive) = {significance:.2f} sigma")
            
            return {
                "mass": x_data,
                "data": y_data,
                "fit_h0": fit_y_h0,
                "fit_h1": fit_y_h1,
                "params_h1": popt_h1,
                "significance": significance,
                "chi2_h0": chi2_h0,
                "chi2_h1": chi2_h1
            }

        except Exception as e:
            print(f" -> H1 Fit failed: {e}")
            return None

    def analyze_w_stiffening(self, mass_grid, stiffening_delta=0.001):
        """
        V15 Hypothesis: Vacuum Stiffening.
        M_W(E) = M_W0 * (1 + delta) at high energies.
        """
        print(f"\n[V15] Testing Vacuum Stiffening (delta={stiffening_delta})...")
        mw_0 = 80.357
        mu_w = 2.0 
        mw_eff = mw_0 * (1.0 + stiffening_delta)
        print(f" -> Effective High-Energy W Mass: {mw_eff:.4f} GeV")
        model_stiff = voigt_profile(mass_grid - mw_eff, 1.0, mu_w/2.0)
        return model_stiff

    def analyze_invisible_width(self, target_mass):
        """
        V15 Hypothesis: Ghost Z' is Invisible.
        LEP Limit: Gamma_inv = 499.0 +/- 1.5 MeV.
        SM Prediction: ~501 MeV.
        """
        print(f"\n[V15] Checking Invisible Width Constraints for {target_mass:.2f} GeV...")
        lep_measured = 499.0 
        lep_error = 1.5
        sm_prediction = 501.4
        diff = lep_measured - sm_prediction
        print(f" -> LEP Measured: {lep_measured} MeV")
        print(f" -> SM Prediction: {sm_prediction} MeV")
        print(f" -> Anomaly (Data-SM): {diff:.2f} +/- {lep_error} MeV")
        return diff, lep_error

    def prune_dark_tower(self, candidates, mass_gap=20.0):
        """
        V15 Hypothesis: Phonon Gap.
        Modes below mass_gap decay instantly to vacuum.
        """
        print(f"\n[V15] Pruning Dark Tower Candidates (Gap = {mass_gap} GeV)...")
        valid = []
        for m in candidates:
            if m > mass_gap:
                valid.append(m)
                print(f" -> KEEP: {m:.2f} GeV")
            else:
                print(f" -> DROP: {m:.2f} GeV (Below Gap)")
    def analyze_heavy_mode(self, axis, sm_model, mass=85.0, coupling=1.0):
        """
        Refined V15 Hypothesis: Heavy Mode Interference.
        Instead of a soft mode at 74.5 GeV (left shoulder), we propose a 
        Heavy Scalar at ~85 GeV (right shoulder) to explain the 'Heavy W' shift.
        """
        print(f"\n[V15 Refined] Generating Heavy Mode Template at {mass} GeV...")
        # Widths: Gamma=2.5 GeV (broad), Sigma=2.0 GeV (detector) - approximate
        heavy_signal = self.generate_voigt_template(axis, mass, 2.5, 2.0, coupling)
        return sm_model + heavy_signal

    def prune_dark_tower_refined(self, candidates, upper_threshold=6.0):
        """
        Refined V15 Hypothesis: Low Mass Sanctuary.
        Topology limits forbid stable modes between 6 GeV and 100 GeV.
        Only fractal modes < 6 GeV are stable.
        """
        print(f"\n[V15 Refined] Pruning Dark Tower (Keeping < {upper_threshold} GeV)...")
        valid = []
        for m in candidates:
            if m < upper_threshold:
                valid.append(m)
                print(f" -> KEEP: {m:.2f} GeV (Safe Zone)")
            else:
                print(f" -> DROP: {m:.2f} GeV (Intermediate Zone)")
        return valid

    def calculate_vacuum_shear(self, mw_sm, mw_observed):
        """
        V16 Task 1: Vacuum Shear Parameter rho.
        M_W_obs = M_W_sm * sqrt(rho) => rho = (M_W_obs / M_W_sm)^2
        """
        rho = (mw_observed / mw_sm)**2
        delta_rho = rho - 1.0
        return rho, delta_rho

    def calculate_sterile_mixing(self, deficit_mev):
        """
        V16 Task 2: Sterile Neutrino Mixing.
        Reduction in width: Delta_Gamma = Gamma_nu_SM * (1 - (1 - sin^2 theta)^2) ... approx?
        Actually, if active mixes with sterile, the active coupling is reduced by cos^2(theta).
        Gamma_measured = 3 * Gamma_nu_0 * cos^2(theta) + ...
        
        Simple model: Gamma_obs = Gamma_SM * (1 - epsilon)
        Deficit = Gamma_obs - Gamma_SM = - Gamma_SM * epsilon
        epsilon = - Deficit / Gamma_SM
        sin^2(theta) ~ epsilon (for small mixing)
        """
        gamma_nu_sm_total = 499.0 + 2.4 # Reconstruct SM total from deficit data context
        # Standard Gamma_nu (3 families) ~ 501.44 MeV
        gamma_sm_pred = 501.44
        
        # We need to reduce it by 'deficit' (magnitude 2.4 MeV).
        # Reduction factor = 1 - (Deficit_Magnitude / Gamma_SM)
        # Reduction ~ sin^2(theta) suppression of the weak coupling?
        # Actually Z -> nu nu is proportional to |g|^2. If nu state is mixed: |nu> = c|a> + s|s>
        # Z couples to |a>. Probability is c^2 = 1 - s^2.
        # So width scales as (1 - sin^2 theta).
        
        # Gamma_obs = Gamma_SM * (1 - sin^2 theta)
        # Gamma_obs - Gamma_SM = - Gamma_SM * sin^2 theta
        # Deficit = - Gamma_SM * sin^2 theta
        # sin^2 theta = - Deficit / Gamma_SM
        
        deficit_magnitude = abs(deficit_mev)
        sin2_theta = deficit_magnitude / gamma_sm_pred
        return sin2_theta

    def calculate_sidm_cross_section(self, mass_gev):
        """
        V16 Task 3: SIDM Cross Section.
        Sigma/mass [cm^2/g].
        Prediction from TRXT geometric cross-section?
        Assume geometric size ~ Compton wavelength or M* scale?
        
        V16 Hypothesis: Cross Section ~ pi * (1/M*)^2 ? No, that's tiny.
        Maybe related to the mass inverse: sigma ~ 1/m^2.
        
        Let's use the 'Topology Suppression' result from Task C as the interaction strength?
        Task C was g ~ m^4.
        
        Let's assume a strong self-interaction scaling for low mass.
        Sigma_self ~ lambda^2 / m^2.
        
        For this function, we will return a placeholder based on (1 GeV / m)^2 * 1 barn? 
        Or we calculate what it NEEDS to be?
        
        Let's calculate the 'Geometric Limit': Sigma ~ (1/m)^2.
        In natural units, 1 GeV^-2 = 0.389 mb = 4e-28 cm^2.
        
        Sigma ~ 4e-28 * (1/m_gev)^2 cm^2.
        Sigma/m ~ 4e-28 / m_gev^3 cm^2.
        Convert to cm^2/g: 1 GeV ~ 1.78e-24 g.
        """
        gev_to_g = 1.78e-24
        
        # Geometric Cross Section (Compton-like)
        # sigma ~ 1/m^2
        sigma_natural = 4e-28 * (1.0 / mass_gev)**2 # cm^2
        
        # Convert to cm^2/g
        sigma_per_mass = sigma_natural / (mass_gev * gev_to_g)
        
        return sigma_natural, sigma_per_mass