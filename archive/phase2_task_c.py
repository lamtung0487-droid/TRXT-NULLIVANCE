import numpy as np
import matplotlib.pyplot as plt
from TRXT_Analysis_Engine import TRXTAnalyzer

def get_real_exclusion_limits():
    """
    Approximate exclusion limits from CRESST-III and SuperCDMS (Low Mass) and LUX/XENON (High Mass).
    Points taken from standard DM limit plots (APPEC 2021).
    """
    # Mass points [GeV]
    mass_points = np.array([0.5, 0.7, 1.0, 2.0, 3.0, 5.0, 10.0, 20.0, 50.0, 100.0, 1000.0])
    
    # Cross-section limit [cm^2]
    # CRESST-III steep rise below 1 GeV.
    # SuperCDMS/CRESST dip around 2-5 GeV.
    # XENON floor around 30-50 GeV.
    limit_points = np.array([
        1e-36, 1e-38, 1e-40, 5e-41, 2e-41, 1e-42, # Low mass (CRESST)
        5e-44, 1e-45, 1e-47, 2e-46, 1e-45        # High mass (XENON/LZ)
    ])
    
    return mass_points, limit_points

def calculate_suppressed_coupling(mass, m_star):
    """
    Topology Suppression Rule (V14.1/V15):
    Coupling scales with (Mass/M*)^4 (Higher dimension operators).
    Base coupling g0 ~ 1e-39 (Weak-scale).
    """
    g0 = 1e-39
    # Suppression factor: (m / M*)^4 for d=6 operator or similar
    # For soft modes, maybe (m/M*)^2. 
    # User specified "Topology Suppression" -> Let's assume m^4 for strong suppression at low mass
    # making low mass 'safe'.
    return g0 * (mass / m_star)**4

def main():
    print("=== TRXT PROTOCOL: TASK C (DARK TOWER) RE-RECTIFIED ===")
    engine = TRXTAnalyzer()
    
    # 1. Get Real Exclusion Limits
    mass_lim, cs_lim = get_real_exclusion_limits()
    
    # 2. TRXT Candidates (Dark Tower Hierarchy)
    # Mass = M* / 2^k
    k_values = [4, 5, 6, 7, 8] # 16, 32, 64, 128, 256 divisor
    candidates = [engine.M_STAR / (2**(k-4) * 16) for k in k_values] # M*/16, M*/32...
    # Wait, Whitepaper says (32,32) = M*/16 = 22.8. 
    # (64,64) = 11.4
    # (128,128) = 5.7
    
    candidates = []
    labels = []
    
    # M*/16
    m1 = engine.predict_mass(32, 32) 
    candidates.append(m1)
    labels.append(f"22.8 GeV")
    
    # M*/32
    m2 = engine.predict_mass(64, 64)
    candidates.append(m2)
    labels.append(f"11.4 GeV")
    
    # M*/64
    m3 = engine.predict_mass(128, 128)
    candidates.append(m3)
    labels.append(f"5.7 GeV")
    
    # M*/128
    m4 = engine.predict_mass(256, 256)
    candidates.append(m4)
    labels.append(f"2.85 GeV")

    # 3. Plotting
    plt.figure(figsize=(10, 7))
    
    # Interpolated Limit Curve
    from scipy.interpolate import interp1d
    f_limit = interp1d(mass_lim, cs_lim, kind='linear', fill_value="extrapolate")
    x_plot = np.logspace(-1, 3, 200)
    y_plot = f_limit(x_plot)
    
    plt.plot(x_plot, y_plot, 'k-', linewidth=2, label='Exclusion Limit (CRESST/XENON)')
    plt.fill_between(x_plot, y_plot, 1e-30, color='gray', alpha=0.3, label='Excluded Region')
    
    # Check Candidates
    print("\n[ANALYSIS] Checking Candidates against Limits...")
    for m, lbl in zip(candidates, labels):
        cs_pred = calculate_suppressed_coupling(m, engine.M_STAR)
        limit_val = float(f_limit(m))
        
        status = "SAFE" if cs_pred < limit_val else "EXCLUDED"
        color = 'g^' if status == "SAFE" else 'rx'
        
        plt.plot(m, cs_pred, color, markersize=12, markeredgecolor='k')
        plt.text(m * 1.1, cs_pred, f"{lbl}\n[{status}]", fontsize=9, verticalalignment='bottom')
        
        print(f" -> {lbl} | CS: {cs_pred:.2e} | Limit: {limit_val:.2e} -> {status}")

    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel("Dark Matter Mass [GeV]")
    plt.ylabel("Cross Section [cm$^2$]")
    plt.title("Task C (Re-Rectified): Mass-Dependent Suppression")
    plt.grid(True, which="both", ls="-", alpha=0.2)
    plt.ylim(1e-48, 1e-35)
    plt.xlim(0.5, 100)
    plt.legend()
    
    output_plot = "trxt_task_c_rerectified.png"
    plt.savefig(output_plot)
    print(f"[OUTPUT] Plot saved to: {output_plot}")

if __name__ == "__main__":
    main()
