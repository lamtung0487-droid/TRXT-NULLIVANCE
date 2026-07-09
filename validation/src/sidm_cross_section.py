"""
TRXT Validation - SIDM Cross-Section Module
============================================
Computes self-interacting dark matter cross-sections using Yukawa potential.
"""

import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import spherical_jn
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)


def yukawa_potential(r: np.ndarray, alpha: float, m_phi: float) -> np.ndarray:
    """
    Yukawa potential V(r) = -α/r * exp(-m_φ * r).
    
    Parameters
    ----------
    r : array
        Distance (fm)
    alpha : float
        Coupling constant (dimensionless)
    m_phi : float
        Mediator mass (MeV)
        
    Returns
    -------
    V : array
        Potential (MeV)
    """
    # Convert m_phi to inverse fm: m_phi [MeV] * 1/197.3 [fm/MeV]
    m_phi_fm = m_phi / 197.3  # fm^-1
    
    # Avoid division by zero
    r_safe = np.maximum(r, 1e-6)
    
    return -alpha / r_safe * np.exp(-m_phi_fm * r_safe) * 197.3  # Convert to MeV


def numerov_step(y_n: float, y_nm1: float, k2_n: float, k2_np1: float, 
                 k2_nm1: float, h: float) -> float:
    """
    Single step of Numerov's method for y'' + k²(x)y = 0.
    
    Parameters
    ----------
    y_n, y_nm1 : float
        Current and previous y values
    k2_n, k2_np1, k2_nm1 : float
        k² values at current, next, and previous points
    h : float
        Step size
        
    Returns
    -------
    y_np1 : float
        Next y value
    """
    h2 = h ** 2
    
    # Numerov formula
    num = (2 - 5*h2*k2_n/6) * y_n - (1 + h2*k2_nm1/12) * y_nm1
    denom = 1 + h2*k2_np1/12
    
    return num / denom


def solve_radial_schrodinger(l: int, E: float, m_chi: float, 
                             alpha: float, m_phi: float,
                             r_max: float = 100.0, 
                             n_points: int = 10000) -> Tuple[np.ndarray, np.ndarray]:
    """
    Solve radial Schrödinger equation for partial wave l.
    
    [-ℏ²/2μ (d²/dr² - l(l+1)/r²) + V(r)] u(r) = E u(r)
    
    where u(r) = r * R(r).
    
    Parameters
    ----------
    l : int
        Angular momentum quantum number
    E : float
        Kinetic energy in center-of-mass frame (MeV)
    m_chi : float
        Dark matter mass (GeV)
    alpha : float
        Coupling constant
    m_phi : float
        Mediator mass (MeV)
    r_max : float
        Maximum radius (fm)
    n_points : int
        Number of grid points
        
    Returns
    -------
    r : array
        Radial grid (fm)
    u : array
        Radial wavefunction u(r) = r*R(r)
    """
    # Reduced mass (in MeV)
    mu = m_chi * 1000 / 2  # For identical particles
    
    # Grid
    h = r_max / n_points
    r = np.linspace(h, r_max, n_points)
    
    # k²(r) = 2μ(E - V(r))/ℏ² - l(l+1)/r²
    # In natural units with ℏc = 197.3 MeV·fm
    V = yukawa_potential(r, alpha, m_phi)
    
    hbar2_over_2mu = 197.3**2 / (2 * mu)  # MeV·fm²
    
    k2 = (E - V) / hbar2_over_2mu - l*(l+1) / r**2
    
    # Initial conditions at small r: u ~ r^(l+1)
    u = np.zeros(n_points)
    u[0] = r[0] ** (l + 1)
    u[1] = r[1] ** (l + 1)
    
    # Numerov integration outward
    for i in range(1, n_points - 1):
        u[i+1] = numerov_step(u[i], u[i-1], k2[i], k2[i+1], k2[i-1], h)
        
        # Check for overflow
        if np.abs(u[i+1]) > 1e30:
            u[i+1:] = np.sign(u[i+1]) * 1e30
            break
    
    return r, u


def compute_phase_shift(l: int, E: float, m_chi: float,
                        alpha: float, m_phi: float) -> float:
    """
    Compute phase shift δ_l for partial wave l.
    
    Parameters
    ----------
    l : int
        Angular momentum
    E : float
        Energy (MeV)
    m_chi : float
        DM mass (GeV)
    alpha : float
        Coupling
    m_phi : float
        Mediator mass (MeV)
        
    Returns
    -------
    delta : float
        Phase shift (radians)
    """
    # Solve radial equation
    r, u = solve_radial_schrodinger(l, E, m_chi, alpha, m_phi)
    
    # Wave number
    mu = m_chi * 1000 / 2
    k = np.sqrt(2 * mu * E) / 197.3  # fm^-1
    
    # Match to asymptotic form at large r
    # u(r) → A * [cos(δ) * j_l(kr) - sin(δ) * n_l(kr)] * kr
    # For large kr: j_l → sin(kr - lπ/2)/kr, n_l → -cos(kr - lπ/2)/kr
    
    # Use ratio at two points
    i1 = int(0.8 * len(r))
    i2 = int(0.9 * len(r))
    
    r1, r2 = r[i1], r[i2]
    u1, u2 = u[i1], u[i2]
    
    # Asymptotic forms
    kr1, kr2 = k * r1, k * r2
    
    j1 = spherical_jn(l, kr1)
    j2 = spherical_jn(l, kr2)
    
    # n_l is the spherical Neumann function
    from scipy.special import spherical_yn
    n1 = spherical_yn(l, kr1)
    n2 = spherical_yn(l, kr2)
    
    # Matching: u = A * (cos δ * j_l - sin δ * n_l) * kr
    # Ratio: u1/u2 = (cos δ * j1 - sin δ * n1) / (cos δ * j2 - sin δ * n2)
    # Solve for tan δ
    
    ratio = (u1 * kr2) / (u2 * kr1)
    
    # tan δ = (j1 - ratio * j2) / (n1 - ratio * n2)
    num = j1 - ratio * j2
    denom = n1 - ratio * n2
    
    if abs(denom) < 1e-10:
        return 0.0
    
    tan_delta = num / denom
    delta = np.arctan(tan_delta)
    
    return delta


def transfer_cross_section(v: float, m_chi: float, alpha: float, 
                           m_phi: float, l_max: int = 50) -> float:
    """
    Compute momentum transfer cross-section σ_T.
    
    σ_T = (4π/k²) Σ_l (l+1) sin²(δ_l - δ_{l+1})
    
    Parameters
    ----------
    v : float
        Relative velocity (km/s)
    m_chi : float
        DM mass (GeV)
    alpha : float
        Coupling
    m_phi : float
        Mediator mass (MeV)
    l_max : int
        Maximum partial wave
        
    Returns
    -------
    sigma_T : float
        Transfer cross-section (cm²)
    """
    # Convert velocity to energy
    # E = μv²/2, μ = m_chi/2 for identical particles
    v_nat = v * 1e5 / 3e10  # v/c
    mu = m_chi * 1000 / 2  # MeV
    E = 0.5 * mu * v_nat**2  # MeV
    
    if E < 1e-10:
        return 0.0
    
    # Compute phase shifts
    deltas = []
    for l in range(l_max + 1):
        try:
            delta = compute_phase_shift(l, E, m_chi, alpha, m_phi)
            deltas.append(delta)
        except Exception:
            deltas.append(0.0)
    
    # Wave number
    k = np.sqrt(2 * mu * E) / 197.3  # fm^-1
    
    # Transfer cross-section
    sigma_T = 0.0
    for l in range(len(deltas) - 1):
        diff = deltas[l] - deltas[l+1]
        sigma_T += (l + 1) * np.sin(diff)**2
    
    sigma_T *= 4 * np.pi / k**2  # fm²
    
    # Convert to cm²
    sigma_T *= 1e-26  # fm² to cm²
    
    return sigma_T


def sigma_over_m(v: float, m_chi: float, alpha: float, m_phi: float) -> float:
    """
    Compute σ_T / m (cross-section per unit mass).
    
    Parameters
    ----------
    v : float
        Relative velocity (km/s)
    m_chi : float
        DM mass (GeV)
    alpha : float
        Coupling
    m_phi : float
        Mediator mass (MeV)
        
    Returns
    -------
    sigma_m : float
        σ_T / m in cm²/g
    """
    sigma = transfer_cross_section(v, m_chi, alpha, m_phi)
    
    # m_chi in GeV → g: 1 GeV = 1.78e-24 g
    m_g = m_chi * 1.78e-24
    
    return sigma / m_g


if __name__ == "__main__":
    # Quick test
    v = 30  # km/s (dwarf scale)
    m_chi = 5.70  # GeV
    alpha = 0.01
    m_phi = 30  # MeV
    
    sigma_m = sigma_over_m(v, m_chi, alpha, m_phi)
    print(f"σ/m at v={v} km/s: {sigma_m:.2f} cm²/g")
