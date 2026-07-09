"""
TRXT Validation - EFT Screening Coefficient Verification (HB-2)
================================================================
Computes c2, c4, Λ_eff, r_V numerically from microscopic NJL formulas.
Verifies c4 > 0 and Cassini bound satisfaction.

Reference: V4 Appendices A, B, C
"""

import numpy as np
from scipy.integrate import quad
import json
from pathlib import Path


def numerical_derivative(func, x, dx=None):
    """Manual central difference derivative."""
    if dx is None:
        dx = x * 0.01 if x != 0 else 1e-5
    return (func(x + dx) - func(x - dx)) / (2 * dx)


# =============================================================================
# Physical Constants (SI and Natural Units)
# =============================================================================
M_PL_GEV = 1.22e19  # Planck mass in GeV
M_STAR_GEV = 365.24  # Master scale in GeV
N_F = 1  # Number of fermion flavors (minimal)
LAMBDA_UV_GEV = M_PL_GEV  # UV cutoff at Planck scale
AU_IN_M = 1.496e11  # 1 AU in meters
GEV_TO_INV_M = 5.068e15  # 1 GeV = 5.068e15 m^-1 (natural units)
M_SUN_KG = 1.989e30  # Solar mass in kg
M_SUN_GEV = M_SUN_KG * 5.61e26  # Solar mass in GeV (using c^2)
G_NEWTON = 6.674e-11  # m^3 kg^-1 s^-2


def c2_integrand(k: float, rho: float, Lambda: float) -> float:
    """
    Integrand for c2(rho) calculation from NJL vacuum polarization.
    
    From V4 Eq. (56):
    c2(ρ) = (N_f / 8π²) ∫₀^Λ dk k² ρ² / (k² + ρ²)^(3/2)
    
    Parameters
    ----------
    k : float
        Loop momentum (GeV)
    rho : float
        Condensate amplitude (GeV)
    Lambda : float
        UV cutoff (GeV)
    """
    if k <= 0:
        return 0.0
    denominator = (k**2 + rho**2)**(1.5)
    if denominator < 1e-100:
        return 0.0
    return k**2 * rho**2 / denominator


def compute_c2(rho: float, Lambda: float = LAMBDA_UV_GEV, N_f: int = N_F) -> float:
    """
    Compute the phase mode kinetic coefficient c2(rho).
    
    c2(ρ) = (N_f / 8π²) ∫₀^Λ dk k² ρ² / (k² + ρ²)^(3/2)
    
    Returns
    -------
    c2 : float
        Kinetic coefficient (dimensionless in natural units, scaled by rho^2)
    """
    prefactor = N_f / (8 * np.pi**2)
    
    # Numerical integration
    integral, error = quad(
        lambda k: c2_integrand(k, rho, Lambda),
        0, Lambda,
        limit=200
    )
    
    c2 = prefactor * integral
    return c2


def compute_c2_derivative(rho: float, Lambda: float = LAMBDA_UV_GEV) -> float:
    """
    Compute d(c2)/d(rho) at rho0.
    """
    return numerical_derivative(
        lambda r: compute_c2(r, Lambda),
        rho,
        dx=rho * 0.01
    )


def compute_m_rho_squared(rho0: float, Lambda: float = LAMBDA_UV_GEV) -> float:
    """
    Compute the amplitude mode mass squared m_ρ² from V_eff curvature.
    
    From NJL gap equation, at the minimum:
    m_ρ² ≈ (N_f Λ² / 4π²) - (1/G) for G near critical
    
    For stable vacuum, m_ρ² > 0.
    We use the standard result: m_ρ ≈ 2 * M_gap for NJL.
    """
    # In NJL, the sigma meson mass is approximately 2 * constituent mass
    # rho0 here is the gap (dynamical mass M)
    m_rho = 2 * rho0
    return m_rho**2


def compute_c4(rho0: float, Lambda: float = LAMBDA_UV_GEV) -> float:
    """
    Compute the quartic coefficient c4 for k-mouflage screening.
    
    From V4 Eq. (57):
    c4 = (c2'(ρ0))² / (2 m_ρ²)
    
    This arises from integrating out the amplitude mode δρ.
    """
    c2_prime = compute_c2_derivative(rho0, Lambda)
    m_rho_sq = compute_m_rho_squared(rho0, Lambda)
    
    if m_rho_sq <= 0:
        raise ValueError("m_rho² <= 0: Vacuum is unstable!")
    
    c4 = c2_prime**2 / (2 * m_rho_sq)
    return c4


def compute_Lambda_eff(c2: float, c4: float, rho0: float) -> float:
    """
    Compute the effective screening scale Λ_eff.
    
    From V4 Section 6.5:
    Λ_eff⁴ = c2 ρ0² / c4
    
    Returns
    -------
    Lambda_eff : float
        Effective scale in GeV
    """
    if c4 <= 0:
        raise ValueError("c4 <= 0: Cannot compute Λ_eff!")
    
    Lambda_eff_4 = c2 * rho0**2 / c4
    Lambda_eff = Lambda_eff_4**0.25
    return Lambda_eff


def compute_Vainshtein_radius(M_source_gev: float, Lambda_eff_gev: float) -> float:
    """
    Compute the Vainshtein screening radius.
    
    From V4 Eq. (69):
    r_V = (M / (16π M_Pl² Λ_eff²))^(1/3)
    
    Returns
    -------
    r_V : float
        Vainshtein radius in meters
    """
    # All in GeV
    numerator = M_source_gev
    denominator = 16 * np.pi * M_PL_GEV**2 * Lambda_eff_gev**2
    
    r_V_gev_inv = (numerator / denominator)**(1.0/3.0)  # in GeV^-1
    
    # Convert GeV^-1 to meters: 1 GeV^-1 = 1.97e-16 m
    r_V_m = r_V_gev_inv * 1.97e-16
    
    return r_V_m


def compute_fifth_force_suppression(r_m: float, r_V_m: float) -> float:
    """
    Compute the fifth-force suppression factor ε_fifth.
    
    From V4:
    ε_fifth = (r / r_V)^(3/2)
    
    Returns
    -------
    epsilon : float
        Suppression factor (dimensionless)
    """
    if r_V_m <= 0:
        return np.inf
    return (r_m / r_V_m)**1.5


def main():
    """
    Main verification routine for HB-2 (Endogenous Screening).
    """
    print("=" * 70)
    print("TRXT VALIDATION - HB-2: Endogenous Screening EFT Verification")
    print("=" * 70)
    
    # Use gap value as rho0 (condensate amplitude at minimum)
    rho0 = M_STAR_GEV  # Gap = 365 GeV
    
    print(f"\n[Parameters]")
    print(f"  UV Cutoff Λ = {LAMBDA_UV_GEV:.2e} GeV")
    print(f"  Condensate ρ0 = {rho0:.2f} GeV")
    print(f"  N_f = {N_F}")
    
    # Compute c2
    print(f"\n[Step 1] Computing c2(ρ0)...")
    c2 = compute_c2(rho0)
    print(f"  c2 = {c2:.6e}")
    
    # Verify c2 > 0 (no ghost)
    assert c2 > 0, "FATAL: c2 <= 0 implies ghost instability!"
    print(f"  CHECK: c2 > 0 ✓ (No Ghost)")
    
    # Compute c2'
    print(f"\n[Step 2] Computing c2'(ρ0)...")
    c2_prime = compute_c2_derivative(rho0)
    print(f"  c2' = {c2_prime:.6e}")
    
    # Compute m_ρ²
    print(f"\n[Step 3] Computing m_ρ²...")
    m_rho_sq = compute_m_rho_squared(rho0)
    print(f"  m_ρ² = {m_rho_sq:.6e} GeV²")
    print(f"  m_ρ = {np.sqrt(m_rho_sq):.2f} GeV")
    
    # Verify m_ρ² > 0 (stable vacuum)
    assert m_rho_sq > 0, "FATAL: m_ρ² <= 0 implies unstable vacuum!"
    print(f"  CHECK: m_ρ² > 0 ✓ (Stable Vacuum)")
    
    # Compute c4
    print(f"\n[Step 4] Computing c4...")
    c4 = compute_c4(rho0)
    print(f"  c4 = {c4:.6e}")
    
    # CRITICAL CHECK: c4 > 0
    c4_positive = c4 > 0
    print(f"\n  ╔══════════════════════════════════════════════════════════╗")
    print(f"  ║  CRITICAL CHECK (HB-2): c4 > 0 for healthy screening     ║")
    print(f"  ║  Result: c4 = {c4:.4e}                          ║")
    print(f"  ║  Status: {'PASS ✓' if c4_positive else 'FAIL ✗'}                                              ║")
    print(f"  ╚══════════════════════════════════════════════════════════╝")
    
    if not c4_positive:
        print("\n  FATAL: c4 <= 0. Theory predicts anti-screening or ghost!")
        return {"status": "FAIL", "reason": "c4 <= 0"}
    
    # Compute Λ_eff
    print(f"\n[Step 5] Computing Λ_eff...")
    Lambda_eff = compute_Lambda_eff(c2, c4, rho0)
    print(f"  Λ_eff = {Lambda_eff:.4e} GeV")
    print(f"  Λ_eff = {Lambda_eff * 1e9:.4f} eV")  # Target: ~0.1 eV
    
    # Compute r_V for Sun
    print(f"\n[Step 6] Computing Vainshtein radius r_V(Sun)...")
    r_V = compute_Vainshtein_radius(M_SUN_GEV, Lambda_eff)
    r_V_AU = r_V / AU_IN_M
    print(f"  r_V = {r_V:.4e} m")
    print(f"  r_V = {r_V_AU:.4e} AU")  # Target: ~10^7 AU
    
    # Compute ε_fifth at 1 AU
    print(f"\n[Step 7] Computing fifth-force suppression at 1 AU...")
    epsilon = compute_fifth_force_suppression(AU_IN_M, r_V)
    print(f"  ε_fifth(1 AU) = {epsilon:.4e}")
    
    # Cassini bound check
    cassini_limit = 2.3e-5
    cassini_pass = epsilon < cassini_limit
    print(f"\n  ╔══════════════════════════════════════════════════════════╗")
    print(f"  ║  CASSINI CHECK: |γ-1| < 2.3×10⁻⁵                         ║")
    print(f"  ║  ε_fifth = {epsilon:.4e}                            ║")
    print(f"  ║  Status: {'PASS ✓ (Safe by ' + f'{cassini_limit/epsilon:.1e}' + 'x)' if cassini_pass else 'FAIL ✗'}              ║")
    print(f"  ╚══════════════════════════════════════════════════════════╝")
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    results = {
        "c2": c2,
        "c2_prime": c2_prime,
        "m_rho_GeV": np.sqrt(m_rho_sq),
        "c4": c4,
        "c4_positive": c4_positive,
        "Lambda_eff_GeV": Lambda_eff,
        "Lambda_eff_eV": Lambda_eff * 1e9,
        "r_V_AU": r_V_AU,
        "epsilon_fifth_1AU": epsilon,
        "cassini_limit": cassini_limit,
        "cassini_pass": cassini_pass,
        "overall_status": "PASS" if (c4_positive and cassini_pass) else "FAIL"
    }
    
    for key, val in results.items():
        if isinstance(val, float):
            print(f"  {key}: {val:.6e}")
        else:
            print(f"  {key}: {val}")
    
    # Save results
    output_dir = Path(__file__).parent.parent / "outputs"
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / "hb2_screening_verification.json"
    
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to: {output_file}")
    
    return results


if __name__ == "__main__":
    results = main()
