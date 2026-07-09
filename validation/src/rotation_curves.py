"""
TRXT Validation - Rotation Curves Module
=========================================
Computes galaxy rotation curves using Lane-Emden polytropic profiles.
"""

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize_scalar
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)

# Physical constants
G_NEWTON = 4.302e-6  # kpc (km/s)^2 / M_sun


def lane_emden_rhs(xi: float, y: np.ndarray, n: float) -> np.ndarray:
    """
    Right-hand side of the Lane-Emden equation.
    
    d²θ/dξ² + (2/ξ) dθ/dξ + θⁿ = 0
    
    Rewritten as system:
    y[0] = θ
    y[1] = dθ/dξ
    
    Parameters
    ----------
    xi : float
        Dimensionless radius
    y : array
        State vector [θ, dθ/dξ]
    n : float
        Polytropic index
        
    Returns
    -------
    dydt : array
        Derivatives [dθ/dξ, d²θ/dξ²]
    """
    theta, dtheta = y
    
    # Handle singularity at origin
    if xi < 1e-10:
        return np.array([dtheta, 0.0])
    
    # θ must be non-negative for real θⁿ when n is non-integer
    # Use signed power: sign(θ) * |θ|^n for stability
    if theta >= 0:
        theta_power = theta ** n
    else:
        # Beyond first zero, set to zero (physical cutoff)
        theta_power = 0.0
    
    # Lane-Emden equation
    d2theta = -2.0 / xi * dtheta - theta_power
    
    return np.array([dtheta, d2theta])


def solve_lane_emden(n: float, xi_max: float = 20.0, 
                     n_points: int = 1000,
                     rtol: float = 1e-10,
                     atol: float = 1e-12,
                     max_step: float = np.inf) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Solve the Lane-Emden equation for polytropic index n.
    
    Parameters
    ----------
    n : float
        Polytropic index (0 < n < 5 for finite extent)
    xi_max : float
        Maximum dimensionless radius
    n_points : int
        Number of output points
    rtol, atol : float
        Solver tolerances
    max_step : float
        Maximum step size for O(dx) convergence tests
        
    Returns
    -------
    xi : array
        Dimensionless radius
    theta : array
        Density profile θ(ξ)
    dtheta : array
        Derivative dθ/dξ
    """
    # Initial conditions at center: θ(0) = 1, θ'(0) = 0
    y0 = np.array([1.0, 0.0])
    
    # Evaluation points
    xi_eval = np.linspace(1e-6, xi_max, n_points)
    
    # Solve ODE
    sol = solve_ivp(
        lambda xi, y: lane_emden_rhs(xi, y, n),
        t_span=(1e-6, xi_max),
        y0=y0,
        t_eval=xi_eval,
        method='RK45',
        rtol=rtol,
        atol=atol,
        max_step=max_step
    )
    
    if not sol.success:
        logger.warning(f"Lane-Emden solver failed: {sol.message}")
    
    return sol.t, sol.y[0], sol.y[1]


def enclosed_mass(xi: np.ndarray, theta: np.ndarray, n: float) -> np.ndarray:
    """
    Compute enclosed mass profile from Lane-Emden solution.
    
    M(ξ) = 4πρ_c α³ ∫₀^ξ θⁿ ξ'² dξ' = -4πρ_c α³ ξ² dθ/dξ
    
    Parameters
    ----------
    xi : array
        Dimensionless radius
    theta : array
        Density profile
    n : float
        Polytropic index
        
    Returns
    -------
    M_enc : array
        Enclosed mass (in dimensionless units)
    """
    # Numerical integration
    # Clip negative theta to zero (beyond first zero, density is zero)
    theta_safe = np.maximum(theta, 0.0)
    integrand = theta_safe ** n * xi ** 2
    M_enc = np.zeros_like(xi)
    for i in range(1, len(xi)):
        M_enc[i] = np.trapz(integrand[:i+1], xi[:i+1])
    
    return 4 * np.pi * M_enc


def rotation_velocity(r: np.ndarray, M_enc: np.ndarray) -> np.ndarray:
    """
    Compute circular rotation velocity from enclosed mass.
    
    v(r) = sqrt(G M(r) / r)
    
    Parameters
    ----------
    r : array
        Physical radius (kpc)
    M_enc : array
        Enclosed mass (M_sun)
        
    Returns
    -------
    v : array
        Rotation velocity (km/s)
    """
    # Avoid division by zero
    r_safe = np.maximum(r, 1e-6)
    v = np.sqrt(G_NEWTON * M_enc / r_safe)
    return v


def fit_galaxy_rotation(r_data: np.ndarray, v_data: np.ndarray, 
                        v_err: np.ndarray, n: float,
                        M_total_guess: float = 1e11) -> dict:
    """
    Fit Lane-Emden rotation curve to observed data.
    
    Parameters
    ----------
    r_data : array
        Observed radii (kpc)
    v_data : array
        Observed velocities (km/s)
    v_err : array
        Velocity errors (km/s)
    n : float
        Polytropic index (fixed)
    M_total_guess : float
        Initial guess for total mass (M_sun)
        
    Returns
    -------
    result : dict
        Fit results including chi2, best-fit parameters, etc.
    """
    # Solve Lane-Emden
    xi, theta, dtheta = solve_lane_emden(n)
    M_enc_dimless = enclosed_mass(xi, theta, n)
    
    # Find xi_1 (first zero of theta)
    zero_idx = np.argmax(theta <= 0)
    if zero_idx == 0:
        xi_1 = xi[-1]  # Use max if no zero found
    else:
        xi_1 = xi[zero_idx]
    
    def objective(log_M):
        """Objective function: chi-squared."""
        M_total = 10 ** log_M
        
        # Scale factor: r = α * ξ, where α = r_1 / ξ_1
        # Assume r_1 is the outermost data point
        r_max = r_data[-1]
        alpha = r_max / xi_1
        
        # Interpolate M_enc to data points
        r_model = xi * alpha
        M_model = M_enc_dimless * M_total / M_enc_dimless[-1]
        
        # Interpolate to data radii
        M_interp = np.interp(r_data, r_model, M_model)
        v_model = rotation_velocity(r_data, M_interp)
        
        # Chi-squared (handle zeros in v_err)
        v_err_safe = np.maximum(v_err, 1.0)
        chi2 = np.sum(((v_data - v_model) / v_err_safe) ** 2)
        
        return chi2
    
    # Optimize
    result = minimize_scalar(
        objective,
        bounds=(8, 14),  # log10(M_sun)
        method='bounded'
    )
    
    M_best = 10 ** result.x
    chi2 = result.fun
    chi2_red = chi2 / (len(r_data) - 1)  # 1 free parameter
    
    return {
        'n': n,
        'M_total': M_best,
        'chi2': chi2,
        'chi2_red': chi2_red,
        'n_data': len(r_data),
        'success': result.success
    }


if __name__ == "__main__":
    # Quick test
    xi, theta, dtheta = solve_lane_emden(n=1.37)
    print(f"Lane-Emden n=1.37: xi_max={xi[-1]:.2f}, theta(xi_max)={theta[-1]:.4f}")
