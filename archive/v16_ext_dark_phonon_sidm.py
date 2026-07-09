import numpy as np
import matplotlib.pyplot as plt
from TRXT_Analysis_Engine import TRXTAnalyzer

def dark_phonon_cross_section(v_km_s, m_dm_gev, m_phi_mev, alpha_x):
    """
    Velocity-dependent SIDM cross-section via Dark Phonon exchange.
    
    σ(v) ~ (α_X^2 / m_DM^2) * (m_DM^4 / (m_phi^2 * m_DM * v)^2)
    
    For Yukawa-like potential with light mediator:
    σ/m ~ (4π * α_X^2 / m_DM^3) * 1 / (1 + (v/v_0)^4)
    
    where v_0 ~ m_phi * c / m_DM (characteristic velocity)
    """
    # Convert units
    c_km_s = 3e5  # Speed of light in km/s
    m_phi_gev = m_phi_mev / 1000.0
    
    # Characteristic velocity
    v_0 = (m_phi_gev / m_dm_gev) * c_km_s
    
    # Cross-section (in GeV^-2)
    # σ ~ 4π * α^2 / m_DM^2
    sigma_0_gev2 = 4 * np.pi * alpha_x**2 / m_dm_gev**2
    
    # Convert to cm^2: 1 GeV^-2 = 0.389e-27 cm^2
    sigma_0_cm2 = sigma_0_gev2 * 0.389e-27
    
    # Velocity suppression factor
    suppression = 1.0 / (1.0 + (v_km_s / v_0)**4)
    
    sigma_cm2 = sigma_0_cm2 * suppression
    
    # σ/m in cm^2/g
    gev_to_g = 1.78e-24
    sigma_per_m = sigma_cm2 / (m_dm_gev * gev_to_g)
    
    return sigma_cm2, sigma_per_m, v_0

def main():
    print("=== TRXT V16 EXTENDED: DARK PHONON SIDM MODEL ===")
    engine = TRXTAnalyzer()
    
    # SIDM Constraints
    V_DWARF = 30.0     # km/s (Dwarf Galaxies - need cores)
    V_CLUSTER = 1000.0 # km/s (Bullet Cluster - must be low)
    
    SIGMA_M_DWARF_MIN = 1.0   # cm^2/g (need > 1 for cores)
    SIGMA_M_CLUSTER_MAX = 1.0 # cm^2/g (need < 1 for Bullet)
    
    # Dark Tower Candidates
    m_dm = 5.71  # GeV (Primary candidate)
    
    print(f"[TARGET CONSTRAINTS]")
    print(f"  Dwarf Galaxies (v ~ {V_DWARF} km/s): σ/m > {SIGMA_M_DWARF_MIN} cm²/g")
    print(f"  Bullet Cluster (v ~ {V_CLUSTER} km/s): σ/m < {SIGMA_M_CLUSTER_MAX} cm²/g")
    print(f"  Dark Matter Mass: {m_dm} GeV")
    
    # ===== PARAMETER SCAN =====
    print(f"\n[PARAMETER SCAN: Finding valid (α_X, m_φ)]")
    
    # Grid search - EXPANDED RANGE
    alpha_range = np.logspace(-2, 1, 100)  # 0.01 to 10
    m_phi_range = np.logspace(-1, 3, 100)  # 0.1 to 1000 MeV
    
    valid_params = []
    
    for alpha_x in alpha_range:
        for m_phi in m_phi_range:
            _, sigma_m_dwarf, v0 = dark_phonon_cross_section(V_DWARF, m_dm, m_phi, alpha_x)
            _, sigma_m_cluster, _ = dark_phonon_cross_section(V_CLUSTER, m_dm, m_phi, alpha_x)
            
            if sigma_m_dwarf > SIGMA_M_DWARF_MIN and sigma_m_cluster < SIGMA_M_CLUSTER_MAX:
                valid_params.append((alpha_x, m_phi, sigma_m_dwarf, sigma_m_cluster, v0))
    
    if valid_params:
        print(f"  Found {len(valid_params)} valid parameter sets!")
        
        # Show a few examples
        print(f"\n  {'α_X':<10} | {'m_φ [MeV]':<12} | {'σ/m (Dwarf)':<15} | {'σ/m (Cluster)':<15} | {'v_0 [km/s]'}")
        print("  " + "-" * 75)
        for i, (a, m, sd, sc, v0) in enumerate(valid_params[:5]):
            print(f"  {a:<10.4f} | {m:<12.1f} | {sd:<15.2f} | {sc:<15.4f} | {v0:<10.1f}")
        
        # Best candidate (maximize ratio)
        best = max(valid_params, key=lambda x: x[2] / max(x[3], 1e-10))
        print(f"\n  [BEST FIT]")
        print(f"    α_X = {best[0]:.4f}")
        print(f"    m_φ = {best[1]:.1f} MeV")
        print(f"    σ/m (Dwarf) = {best[2]:.2f} cm²/g")
        print(f"    σ/m (Cluster) = {best[3]:.4f} cm²/g")
        print(f"    Characteristic v_0 = {best[4]:.1f} km/s")
        
        # Plot
        v_range = np.logspace(0.5, 3.5, 100)  # 3 to 3000 km/s
        sigma_m_curve = []
        for v in v_range:
            _, sm, _ = dark_phonon_cross_section(v, m_dm, best[1], best[0])
            sigma_m_curve.append(sm)
        
        plt.figure(figsize=(10, 6))
        plt.loglog(v_range, sigma_m_curve, 'b-', linewidth=2, label=f'TRXT Dark Phonon (α={best[0]:.3f}, m_φ={best[1]:.0f} MeV)')
        plt.axhline(1.0, color='gray', linestyle='--', label='SIDM Threshold')
        plt.axvline(30, color='g', linestyle=':', alpha=0.5, label='Dwarf (v~30 km/s)')
        plt.axvline(1000, color='r', linestyle=':', alpha=0.5, label='Cluster (v~1000 km/s)')
        plt.xlabel("Velocity [km/s]")
        plt.ylabel("σ/m [cm²/g]")
        plt.title(f"TRXT Dark Phonon SIDM (m_DM = {m_dm} GeV)")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.ylim(1e-4, 1e3)
        plt.savefig("trxt_v16_dark_phonon_sidm.png")
        print(f"\n[OUTPUT] Plot saved to: trxt_v16_dark_phonon_sidm.png")
        
        print(f"\n[CONCLUSION]")
        print("  ✓ A valid Dark Phonon parameter space EXISTS!")
        print("  ✓ TRXT can act as Self-Interacting Dark Matter with velocity dependence.")
        print("  STATUS: VALIDATED (SIDM mechanism)")
        
    else:
        print("  ✗ No valid parameter set found in the scanned range.")
        print("  STATUS: REQUIRES EXTENDED SEARCH")

if __name__ == "__main__":
    main()
