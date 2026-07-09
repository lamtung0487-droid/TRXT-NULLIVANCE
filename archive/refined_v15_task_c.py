import numpy as np
import matplotlib.pyplot as plt
from TRXT_Analysis_Engine import TRXTAnalyzer

# Re-use limits from Phase 2.2
def get_real_exclusion_limits():
    mass_points = np.array([0.5, 0.7, 1.0, 2.0, 3.0, 5.0, 10.0, 20.0, 50.0])
    limit_points = np.array([1e-36, 1e-38, 1e-40, 5e-41, 2e-41, 1e-42, 5e-44, 1e-45, 1e-47])
    return mass_points, limit_points

def calculate_suppressed_coupling(mass, m_star):
    g0 = 1e-39
    return g0 * (mass / m_star)**4

def main():
    print("=== TRXT PROTOCOL: REFINED V15 TASK C (LOW MASS SANCTUARY) ===")
    engine = TRXTAnalyzer()
    
    # 1. Full Spectrum Generation
    k_values = [4, 5, 6, 7, 8] 
    raw_candidates = [engine.M_STAR / (2**(k-4) * 16) for k in k_values] # 22.8 down to 2.85
    # Fix mapping: (32,32)=22.8, (64,64)=11.4, (128,128)=5.7, (256,256)=2.85
    raw_candidates = [engine.predict_mass(2**k, 2**k) for k in range(5, 9)]
    
    # 2. Refined Pruning
    THRESHOLD = 6.0
    valid_candidates = engine.prune_dark_tower_refined(raw_candidates, upper_threshold=THRESHOLD)
    
    # 3. Verify Survivors
    mass_lim, cs_lim = get_real_exclusion_limits()
    
    print("\n[ANALYSIS] Verifying Survivors against CRESST-III...")
    from scipy.interpolate import interp1d
    f_limit = interp1d(mass_lim, cs_lim, kind='linear', fill_value="extrapolate")
    
    plt.figure(figsize=(10, 6))
    x_plot = np.logspace(-1, 2, 100)
    plt.plot(x_plot, f_limit(x_plot), 'k-', label='Exclusion Limit')
    plt.fill_between(x_plot, f_limit(x_plot), 1e-30, color='gray', alpha=0.3)
    
    for m in valid_candidates:
        cs = calculate_suppressed_coupling(m, engine.M_STAR)
        limit = float(f_limit(m))
        status = "SAFE" if cs < limit else "EXCLUDED"
        
        print(f" -> Candidate {m:.2f} GeV | CS: {cs:.2e} | Limit: {limit:.2e} -> {status}")
        
        plt.plot(m, cs, 'g^', markersize=12)
        plt.text(m, cs*1.5, f"{m:.2f}\n{status}", fontsize=9, ha='center')

    plt.xscale('log')
    plt.yscale('log')
    plt.ylim(1e-45, 1e-35)
    plt.title(f"Refined V15: Low Mass Sanctuary (< {THRESHOLD} GeV)")
    plt.xlabel("Mass [GeV]")
    plt.ylabel("Cross Section")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig("trxt_refined_v15_task_c.png")

if __name__ == "__main__":
    main()
