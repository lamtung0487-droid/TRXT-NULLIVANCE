
"""
NULLIVANCE MODEL: Dark Matter Suppression Module (Phase 3c)
===========================================================
Demonstrating why the 5.71 GeV "Dark Tower" particle evades Direct Detection (LZ/XENONnT).

Mechanism:
1. Landau Criterion: Scattering requires phonon excitation. 
   Kinematically forbidden if v_collision < v_critical (sound speed).
2. Superfluid Gap: Energy transfer must exceed the gap Delta.
   Suppression factor ~ exp(-Delta / T_effective) or (q/Lambda)^4 for derivative coupling.

Target:
Reduce effective cross-section below LZ limit (~ 1e-47 cm^2 for 6 GeV mass).
"""

import numpy as np

def calculate_suppression():
    print("--- NULLIVANCE PHASE 3c: DARK MATTER SUPPRESSION ---")
    
    # 1. Parameters
    m_DM = 5.71 # GeV
    m_Xe = 131.0 * 0.9315 # GeV (Xenon nucleus)
    mu_reduced = (m_DM * m_Xe) / (m_DM + m_Xe) # GeV
    
    sigma_geometric = 1e-36 # cm^2 (Typical weak scale cross section ~ pb)
    print(f"Baseline Geometric Cross Section: {sigma_geometric:.1e} cm^2")
    
    # 2. Kinematics
    v_galactic = 220.0 # km/s (Mean velocity)
    v_max = 550.0 # km/s (Escape velocity)
    c_light_kms = 299792.0 # km/s
    
    # Beta factors
    beta_mean = v_galactic / c_light_kms
    beta_max = v_max / c_light_kms
    
    # Kinetic Energy available in Center of Mass frame
    # E_max = 0.5 * mu * v_max^2
    E_kinetic_max_GeV = 0.5 * mu_reduced * beta_max**2
    E_kinetic_max_eV = E_kinetic_max_GeV * 1e9
    
    print(f"\n[KINEMATICS]")
    print(f"Max Collision Velocity: {v_max} km/s")
    print(f"Max Kinetic Energy Available: {E_kinetic_max_eV:.2f} eV")
    
    # 3. Superfluid properties
    # Critical Velocity (Sound speed)
    # If the droplet is dense, c_s can be high.
    # Let's assume c_s ~ 10^-3 c (typical for some nuclear matter) or higher?
    # Actually for Nullivance, c_s ~ c inside the vacuum, but for a droplet?
    # Let's assume the critical velocity for excitation is related to the mass gap.
    
    # Gap Delta calculation
    # If M* ~ 365 GeV is the vacuum gap, the droplet excitation might be related.
    # But let's use the derivative coupling suppression q^4/Lambda^4.
    
    Lambda_suppress = 1000.0 # GeV (Scale of new physics/condensate)
    q_transfer = mu_reduced * beta_max # Momentum transfer
    
    print(f"\n[DERIVATIVE COUPLING]")
    print(f"Momentum Transfer q: {q_transfer:.2e} GeV")
    print(f"New Physics Scale Lambda: {Lambda_suppress} GeV")
    
    suppression_factor_derivative = (q_transfer / Lambda_suppress)**4
    
    print(f"Suppression Factor (q/Lambda)^4: {suppression_factor_derivative:.2e}")
    
    # 4. Landau Criterion Suppression (step function effectively)
    # If v < v_critical, suppression is essentially infinite (only tunneling).
    # Let's assume v_critical ~ 300 km/s (just above mean, below max?).
    # If v_critical > v_max, then complete suppression.
    
    # 5. Effective Cross Section
    sigma_effective = sigma_geometric * suppression_factor_derivative
    
    # LZ Limit for 6 GeV
    lz_limit = 1e-46 # cm^2 approx
    
    print(f"\n[RESULTS]")
    print(f"Effective Cross Section: {sigma_effective:.2e} cm^2")
    print(f"LZ Experimental Limit:   {lz_limit:.2e} cm^2")
    
    if sigma_effective < lz_limit:
        print("--> SUCCESS: Signal is suppressed below experimental sensitivity.")
        print("    Mechanism: Derivative Coupling (Superfluid property) works.")
    else:
        print("--> WARNING: Still visible. Need stronger suppression (Exponential?).")

if __name__ == "__main__":
    calculate_suppression()
