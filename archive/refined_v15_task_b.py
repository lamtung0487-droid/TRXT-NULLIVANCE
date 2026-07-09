import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit, minimize
from TRXT_Analysis_Engine import TRXTAnalyzer

def get_cdf_digitized_data():
    mt_bins = np.array([60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90])
    events = np.array([200, 250, 320, 450, 800, 1500, 3000, 6000, 12000, 25000, 45000, 20000, 3000, 500, 100, 20])
    errors = np.sqrt(events)
    return mt_bins, events, errors

def w_jacobian_model(x_axis, mass, width, norm):
    return norm * np.exp(-0.5 * ((x_axis - mass)/2.0)**2)

def main():
    print("=== TRXT PROTOCOL: REFINED V15 TASK B (HEAVY MODE) ===")
    engine = TRXTAnalyzer()
    mt_grid, cdf_data, cdf_err = get_cdf_digitized_data()
    
    mw_sm = 80.357
    
    # 1. Fit SM (Reference)
    def fit_func_sm(x, norm):
        return w_jacobian_model(x, mw_sm, 2.0, norm)
    popt_sm, _ = curve_fit(fit_func_sm, mt_grid, cdf_data, sigma=cdf_err, p0=[np.max(cdf_data)])
    chi2_sm = np.sum(((cdf_data - fit_func_sm(mt_grid, *popt_sm)) / cdf_err)**2)
    
    # 2. Fit Refined V15: SM + Heavy Mode (85 GeV)
    # Allows constructive interference (adding events on the right shoulder)
    # This effectively pulls the "Mean Mass" of the combination upwards.
    
    def fit_func_heavy(x, norm_sm, coupling_heavy):
        sm = w_jacobian_model(x, mw_sm, 2.0, norm_sm)
        # Heavy Mode at 85 GeV
        heavy = engine.generate_voigt_template(x, 85.0, 2.5, 2.0, coupling_heavy)
        return sm + heavy
        
    popt_h, _ = curve_fit(fit_func_heavy, mt_grid, cdf_data, sigma=cdf_err, p0=[popt_sm[0], 1000.0], bounds=([0, 0], [np.inf, np.inf]))
    model_heavy = fit_func_heavy(mt_grid, *popt_h)
    chi2_h = np.sum(((cdf_data - model_heavy) / cdf_err)**2)
    
    print(f" -> Model 0 (SM): Chi2 = {chi2_sm:.2f}")
    print(f" -> Model 1 (SM + 85GeV Mode): Chi2 = {chi2_h:.2f}")
    print(f" -> Delta Chi2 = {chi2_sm - chi2_h:.2f}")
    print(f" -> Best Fit Coupling (Heavy): {popt_h[1]:.2f}")
    
    if chi2_h < chi2_sm and popt_h[1] > 100:
        print(" -> CONCLUSION: Heavy Mode (85 GeV) IMPROVES the fit. Compatible with CDF direction.")
    else:
        print(" -> CONCLUSION: Heavy Mode does not improve fit significantly.")

    # Plot
    plt.figure(figsize=(10, 6))
    plt.errorbar(mt_grid, cdf_data, yerr=cdf_err, fmt='ko', label='CDF II Data')
    plt.plot(mt_grid, fit_func_sm(mt_grid, *popt_sm), 'b--', label='SM')
    plt.plot(mt_grid, model_heavy, 'r-', linewidth=2, label=f'SM + 85GeV (C={popt_h[1]:.0f})')
    plt.yscale('log')
    plt.title("Refined V15: W-Anomaly with Heavy Mode (85 GeV)")
    plt.xlabel("Mt [GeV]")
    plt.ylabel("Events")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig("trxt_refined_v15_task_b.png")

if __name__ == "__main__":
    main()
