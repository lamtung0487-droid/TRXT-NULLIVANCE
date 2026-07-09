import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from TRXT_Analysis_Engine import TRXTAnalyzer

def get_cdf_digitized_data():
    # Same as Phase 2.1
    mt_bins = np.array([60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90])
    events = np.array([200, 250, 320, 450, 800, 1500, 3000, 6000, 12000, 25000, 45000, 20000, 3000, 500, 100, 20])
    errors = np.sqrt(events)
    return mt_bins, events, errors

def main():
    print("=== TRXT PROTOCOL: TASK B (W-STIFFENING) V15 ===")
    engine = TRXTAnalyzer()
    mt_grid, cdf_data, cdf_err = get_cdf_digitized_data()

    # 1. Fit Vacuum Stiffening Model
    # f(x) = A * Stiff_Model(x, delta)
    def fit_func_v15(x, norm, delta):
        model = engine.analyze_w_stiffening(x, delta)
        # Normalize shape to data max for stability
        return norm * model / np.max(model) * np.max(cdf_data)

    print("[ANALYSIS] Fitting V15 Stiffening Model...")
    try:
        # Bounds: Norm > 0, Delta in [-0.01, 0.01] (small perturbation)
        popt, pcov = curve_fit(fit_func_v15, mt_grid, cdf_data, sigma=cdf_err, 
                               p0=[1.0, 0.0005], bounds=([0.1, -0.01], [2.0, 0.01]))
        
        best_delta = popt[1]
        chi2_v15 = np.sum(((cdf_data - fit_func_v15(mt_grid, *popt)) / cdf_err)**2)
        ndof = len(mt_grid) - 2
        
        print(f" -> Best Fit Delta: {best_delta:.6f}")
        print(f" -> V15 Chi2/Ndof: {chi2_v15:.2f}/{ndof} = {chi2_v15/ndof:.2f}")
        
        if 0.0005 < best_delta < 0.002:
            print(" -> CONCLUSION: Positive Vacuum Stiffening detected! Matches 'Heavy W' direction.")
        elif best_delta < 0:
            print(" -> CONCLUSION: Negative Delta preferred (Softening). Contradicts Heavy W.")
        else:
            print(" -> CONCLUSION: Inconclusive delta.")

        # Plot
        plt.figure(figsize=(10, 6))
        plt.errorbar(mt_grid, cdf_data, yerr=cdf_err, fmt='ko', label='CDF II Data', alpha=0.7)
        plt.plot(mt_grid, fit_func_v15(mt_grid, *popt), 'g-', linewidth=2, label=f'V15 Stiff Vacuum (Delta={best_delta*1e3:.2f}e-3)')
        plt.title(f"Task B (V15): Vacuum Stiffening (Shift = {80.357*best_delta:.3f} GeV)")
        plt.xlabel("Transverse Mass [GeV]")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.savefig("trxt_task_b_v15_result.png")
        
    except Exception as e:
        print(f"[ERROR] Fit failed: {e}")

if __name__ == "__main__":
    main()
