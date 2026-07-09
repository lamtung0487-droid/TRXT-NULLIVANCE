"""
TRXT Systematic Mechanism Test for Hubble Tension
===================================================
Enumerates ALL possible mechanisms from the TRXT Lagrangian that could
modify cosmological c_s and tests each one.

MASTER PROTOCOL V2.0: All mechanisms derived from first principles.

The TRXT Lagrangian is:
L = L_gravity + L_superfluid + L_fermion

L_superfluid = P(X, ρ, T, μ) where various mechanisms can arise.
"""

import numpy as np
from scipy.integrate import quad
import json
from pathlib import Path


# =============================================================================
# FUNDAMENTAL CONSTANTS
# =============================================================================
M_PL_GEV = 1.22e19
M_STAR_GEV = 365.24
H_0 = 67.4  # km/s/Mpc (Planck)
T_CMB_0 = 2.725  # K (today)
K_B_GEV = 8.617e-14  # Boltzmann constant in GeV/K
C_LIGHT = 299792.458  # km/s

# Cosmological parameters
OMEGA_M = 0.315
OMEGA_B = 0.0493
OMEGA_R = 8.5e-5
OMEGA_LAMBDA = 1.0 - OMEGA_M - OMEGA_R


# =============================================================================
# MECHANISM 1: Temperature-Dependent EFT (Finite Temperature Superfluid)
# =============================================================================

def mechanism_1_temperature_eft(z: float) -> dict:
    """
    Temperature-dependent c₂, c₄ from finite-temperature field theory.
    
    In a superfluid, the condensate fraction depends on T/T_c.
    
    For BEC: ρ₀(T) = ρ₀(0) * (1 - (T/T_c)^(3/2))
    
    This modifies c₂, c₄ at high redshift (high T).
    """
    # Temperature at redshift z
    T_z = T_CMB_0 * (1 + z)  # K
    T_z_GeV = T_z * K_B_GEV
    
    # Critical temperature for TRXT superfluid
    # From BCS theory: T_c ~ Δ/1.76 where Δ is the gap
    # For TRXT: Δ ~ M* ~ 365 GeV
    T_c_GeV = M_STAR_GEV / 1.76
    
    # Condensate fraction
    ratio = T_z_GeV / T_c_GeV
    if ratio >= 1:
        # Above T_c: normal fluid
        condensate_fraction = 0.0
        c_s_sq = 1.0 / 3.0  # Normal fluid
    else:
        # Below T_c: superfluid
        condensate_fraction = 1.0 - ratio**1.5
        # Sound speed interpolates
        c_s_sq = 1.0 - 2.0/3.0 * condensate_fraction
    
    return {
        'mechanism': 'Temperature EFT',
        'z': z,
        'T_GeV': T_z_GeV,
        'T_c_GeV': T_c_GeV,
        'T_over_Tc': ratio,
        'condensate_fraction': condensate_fraction,
        'c_s_sq': c_s_sq,
        'c_s': np.sqrt(max(c_s_sq, 0))
    }


# =============================================================================
# MECHANISM 2: Higher-Order P(X) Terms
# =============================================================================

def mechanism_2_higher_order_px(z: float, X: float) -> dict:
    """
    P(X) = c₂X + c₄X² + c₆X³ + ... (higher order terms)
    
    At high X (early universe), higher-order terms dominate.
    
    c_s² = P_X / (P_X + 2X P_XX)
    """
    # EFT coefficients (from NJL at M* scale)
    c2 = 6.38e4
    c4 = 0.111
    c6 = c4 / M_STAR_GEV**2  # Dimensional estimate
    
    # P(X) and derivatives
    P = c2 * X + c4 * X**2 + c6 * X**3
    P_X = c2 + 2 * c4 * X + 3 * c6 * X**2
    P_XX = 2 * c4 + 6 * c6 * X
    
    # Sound speed
    denominator = P_X + 2 * X * P_XX
    if denominator <= 0:
        c_s_sq = 1.0
    else:
        c_s_sq = P_X / denominator
    
    return {
        'mechanism': 'Higher-order P(X)',
        'z': z,
        'X': X,
        'c6': c6,
        'c_s_sq': c_s_sq,
        'c_s': np.sqrt(max(c_s_sq, 0))
    }


# =============================================================================
# MECHANISM 3: Non-minimal Coupling to Curvature
# =============================================================================

def mechanism_3_nonminimal_coupling(z: float) -> dict:
    """
    L = (M_Pl² + ξρ²)R/2 + P(X)
    
    Non-minimal coupling modifies effective c_s via:
    c_s_eff² = c_s² / (1 + ξρ²/M_Pl²)
    """
    # Condensate amplitude at cosmological scales
    rho_DE_GeV4 = 3.0 * (1.44e-42)**2 * M_PL_GEV**2 / (8 * np.pi) * 0.7
    rho0 = rho_DE_GeV4**(1/4)
    
    # Non-minimal coupling (dimensionless)
    # From conformal coupling: ξ = 1/6
    xi = 1.0 / 6.0
    
    # Correction factor
    correction = 1 + xi * rho0**2 / M_PL_GEV**2
    
    # Base sound speed
    c_s_base_sq = 1.0  # From P(X) at low X
    
    # Effective sound speed
    c_s_eff_sq = c_s_base_sq / correction
    
    return {
        'mechanism': 'Non-minimal coupling',
        'z': z,
        'xi': xi,
        'rho0_GeV': rho0,
        'correction_factor': correction,
        'c_s_sq': c_s_eff_sq,
        'c_s': np.sqrt(max(c_s_eff_sq, 0))
    }


# =============================================================================
# MECHANISM 4: Amplitude Mode (Higgs-like) Contribution
# =============================================================================

def mechanism_4_amplitude_mode(z: float) -> dict:
    """
    Sound speed has contributions from both phase (θ) and amplitude (ρ) modes.
    
    c_s² = (c₂ + contribution from ρ-mode exchange)
    
    At high z, ρ-mode is lighter and contributes more.
    """
    # Phase mode contribution
    c_s_phase = 1.0
    
    # Amplitude mode mass (scales with T)
    T_z = T_CMB_0 * (1 + z) * K_B_GEV  # GeV
    m_rho = M_STAR_GEV * (1 - T_z / M_STAR_GEV)  # Softens at high T
    m_rho = max(m_rho, 1e-10)
    
    # Amplitude mode contribution to sound speed
    # From 1-loop: δc_s² ~ -T²/(m_ρ * f²) where f ~ M*
    delta_cs_sq = -T_z**2 / (m_rho * M_STAR_GEV**2)
    
    c_s_sq = c_s_phase + delta_cs_sq
    c_s_sq = max(c_s_sq, 0)
    
    return {
        'mechanism': 'Amplitude mode',
        'z': z,
        'T_GeV': T_z,
        'm_rho_GeV': m_rho,
        'delta_cs_sq': delta_cs_sq,
        'c_s_sq': c_s_sq,
        'c_s': np.sqrt(c_s_sq)
    }


# =============================================================================
# MECHANISM 5: Vortex/Topological Contribution
# =============================================================================

def mechanism_5_vortex_contribution(z: float) -> dict:
    """
    In a superfluid, vortices contribute to effective properties.
    
    Vortex density scales with expansion: n_v ~ H²
    
    c_s² = 1 - (n_v / n_critical)
    """
    # Hubble parameter at z
    H_z = H_0 * np.sqrt(OMEGA_M * (1 + z)**3 + OMEGA_R * (1 + z)**4 + OMEGA_LAMBDA)
    H_z_GeV = H_z * 1.44e-42 / 67.4  # Convert to GeV
    
    # Critical vortex density (from superfluid physics)
    # n_critical ~ ρ₀ / ℏ
    rho0_cosmo = (3.0 * H_0**2 * M_PL_GEV**2 / (8 * np.pi) * 0.7)**(1/4) * (1.44e-42 / 67.4)
    n_critical = rho0_cosmo
    
    # Vortex density scales with H
    n_v = H_z_GeV**2 / M_STAR_GEV
    
    # Sound speed reduction
    ratio = n_v / n_critical if n_critical > 0 else 0
    c_s_sq = 1.0 - min(ratio, 0.9)  # Cap to avoid negative
    
    return {
        'mechanism': 'Vortex contribution',
        'z': z,
        'H_z_GeV': H_z_GeV,
        'n_v': n_v,
        'n_critical': n_critical,
        'vortex_ratio': ratio,
        'c_s_sq': c_s_sq,
        'c_s': np.sqrt(max(c_s_sq, 0))
    }


# =============================================================================
# MECHANISM 6: Running Coupling (RG Flow)
# =============================================================================

def mechanism_6_running_coupling(z: float) -> dict:
    """
    c₂, c₄ run with energy scale μ ~ T(z).
    
    β(c₂) = -γ c₂² / (16π²)
    
    At high z (high T), c₂ is smaller → c_s smaller.
    """
    # Energy scale
    T_z = T_CMB_0 * (1 + z) * K_B_GEV
    mu_z = max(T_z, 1e-15)  # GeV
    mu_0 = T_CMB_0 * K_B_GEV  # Reference scale (today)
    
    # Baseline values at μ₀
    c2_0 = 6.38e4
    
    # Anomalous dimension (from NJL)
    gamma = 0.1  # Typical value
    
    # Running
    log_ratio = np.log(mu_z / mu_0) if mu_0 > 0 else 0
    c2_running = c2_0 * np.exp(-gamma * log_ratio / (16 * np.pi**2))
    
    # Sound speed with running c₂
    c4 = 0.111 * (c2_running / c2_0)  # c₄ also runs
    X = mu_z**4  # X ~ T⁴
    
    c_s_sq = (c2_running + 2 * c4 * X) / (c2_running + 6 * c4 * X)
    
    return {
        'mechanism': 'Running coupling (RG)',
        'z': z,
        'mu_GeV': mu_z,
        'c2_running': c2_running,
        'gamma': gamma,
        'c_s_sq': c_s_sq,
        'c_s': np.sqrt(max(c_s_sq, 0))
    }


# =============================================================================
# MAIN TEST ROUTINE
# =============================================================================

def compute_r_s_with_mechanism(mechanism_func, **kwargs) -> float:
    """Compute sound horizon using a given mechanism for c_s(z)."""
    
    z_recomb = 1089.9
    
    def integrand(z):
        result = mechanism_func(z, **kwargs)
        c_s = result['c_s']
        
        # Combine with plasma sound speed
        R_b = 0.75 * (OMEGA_B / OMEGA_R) / (1 + z)
        c_s_plasma = 1.0 / np.sqrt(3 * (1 + R_b))
        c_s_eff = min(c_s, c_s_plasma)
        
        H_z = H_0 * np.sqrt(OMEGA_M * (1 + z)**3 + OMEGA_R * (1 + z)**4 + OMEGA_LAMBDA)
        
        return C_LIGHT * c_s_eff / H_z
    
    r_s, _ = quad(integrand, z_recomb, 1e5, limit=200)
    return r_s


def infer_H0_from_mechanism(mechanism_func, target_rs: float = 147.09, **kwargs) -> float:
    """Find H0 that gives target r_s for a given mechanism."""
    
    def compute_rs_for_H0(H0_test):
        z_recomb = 1089.9
        
        def integrand(z):
            result = mechanism_func(z, **kwargs)
            c_s = result['c_s']
            
            R_b = 0.75 * (OMEGA_B / OMEGA_R) / (1 + z)
            c_s_plasma = 1.0 / np.sqrt(3 * (1 + R_b))
            c_s_eff = min(c_s, c_s_plasma)
            
            H_z = H0_test * np.sqrt(OMEGA_M * (1 + z)**3 + OMEGA_R * (1 + z)**4 + OMEGA_LAMBDA)
            
            return C_LIGHT * c_s_eff / H_z
        
        r_s, _ = quad(integrand, z_recomb, 1e5, limit=200)
        return r_s
    
    # Binary search
    H0_lo, H0_hi = 50, 100
    for _ in range(50):
        H0_mid = (H0_lo + H0_hi) / 2
        r_s = compute_rs_for_H0(H0_mid)
        if r_s > target_rs:
            H0_lo = H0_mid
        else:
            H0_hi = H0_mid
    
    return (H0_lo + H0_hi) / 2


def main():
    print("=" * 70)
    print("TRXT SYSTEMATIC MECHANISM TEST")
    print("Testing ALL mechanisms from TRXT Lagrangian")
    print("=" * 70)
    
    mechanisms = [
        ('1. Temperature EFT', mechanism_1_temperature_eft, {}),
        ('2. Higher-order P(X)', lambda z: mechanism_2_higher_order_px(z, X=1e-10), {}),
        ('3. Non-minimal coupling', mechanism_3_nonminimal_coupling, {}),
        ('4. Amplitude mode', mechanism_4_amplitude_mode, {}),
        ('5. Vortex contribution', mechanism_5_vortex_contribution, {}),
        ('6. Running coupling', mechanism_6_running_coupling, {}),
    ]
    
    results = []
    
    print("\n[Testing each mechanism at z = 1000 (recombination)]")
    print("-" * 70)
    
    for name, func, kwargs in mechanisms:
        # Test at recombination
        test = func(1000.0, **kwargs) if kwargs else func(1000.0)
        c_s = test['c_s']
        
        # Compute r_s
        try:
            r_s = compute_r_s_with_mechanism(func, **kwargs)
            H0_inferred = infer_H0_from_mechanism(func, **kwargs)
        except:
            r_s = float('nan')
            H0_inferred = float('nan')
        
        tension_shoes = abs(H0_inferred - 73.04) / 1.04 if not np.isnan(H0_inferred) else float('nan')
        
        print(f"\n{name}")
        print(f"  c_s(z=1000) = {c_s:.4f}")
        print(f"  r_s = {r_s:.2f} Mpc")
        print(f"  H0 = {H0_inferred:.2f} km/s/Mpc")
        print(f"  Tension vs SH0ES: {tension_shoes:.1f}σ")
        
        result = {
            'mechanism': name,
            'c_s_at_recomb': c_s,
            'r_s_Mpc': r_s,
            'H0_inferred': H0_inferred,
            'tension_shoes_sigma': tension_shoes,
            'details': test
        }
        results.append(result)
    
    # Find best mechanism
    valid_results = [r for r in results if not np.isnan(r['H0_inferred'])]
    if valid_results:
        best = min(valid_results, key=lambda x: x['tension_shoes_sigma'])
        
        print(f"\n  ╔══════════════════════════════════════════════════════════╗")
        print(f"  ║  BEST MECHANISM FOR HUBBLE TENSION                       ║")
        print(f"  ╠══════════════════════════════════════════════════════════╣")
        print(f"  ║  {best['mechanism'][:40]:<44} ║")
        print(f"  ║  H0 = {best['H0_inferred']:.2f} km/s/Mpc                           ║")
        print(f"  ║  Tension vs SH0ES: {best['tension_shoes_sigma']:.1f}σ                        ║")
        print(f"  ║  c_s(z=1000) = {best['c_s_at_recomb']:.4f}                           ║")
        print(f"  ╚══════════════════════════════════════════════════════════╝")
    
    # Save results
    output_dir = Path(__file__).parent.parent / "outputs"
    output_dir.mkdir(exist_ok=True)
    
    # Clean up for JSON serialization
    for r in results:
        r['details'] = {k: float(v) if isinstance(v, (np.floating, np.integer)) else v 
                        for k, v in r['details'].items()}
    
    output_file = output_dir / "trxt_mechanism_test_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nResults saved to: {output_file}")
    
    return results


if __name__ == "__main__":
    main()
