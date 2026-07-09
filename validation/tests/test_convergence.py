
import numpy as np
import pytest
import sys
import os
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from rotation_curves import solve_lane_emden

def test_lane_emden_convergence():
    """
    Verify that the Lane-Emden solver converges with 2nd order accuracy.
    Method: Self-convergence test (Richardson extrapolation style).
    We use a very high resolution run as the 'truth'.
    """
    n = 1.37  # Standard Polytropic index used in TRXT
    xi_max = 20.0
    
    # Resolutions to test
    # We use N+1 points to ensure alignment if possible, but interp is safer
    resolutions = [100, 200, 400, 800, 1600]
    ref_res = 3200
    
    print(f"Running Convergence Test (n={n}, xi_max={xi_max})...")
    
    # Run Reference High-Res Simulation with strict tolerance
    ref_dx = xi_max / (ref_res - 1)
    xi_ref, theta_ref, _ = solve_lane_emden(n, xi_max, ref_res, 
                                            rtol=1e-14, atol=1e-14, 
                                            max_step=ref_dx)
    
    # Create interpolator for reference solution (Cubic spline is O(h^4), safe for testing O(h^2))
    ref_interp = interp1d(xi_ref, theta_ref, kind='cubic', bounds_error=False, fill_value=0.0)
    
    errors = []
    dxs = []
    
    for res in resolutions:
        # Calculate step size
        dx = xi_max / (res - 1)
        dxs.append(dx)
        
        # Run solver with fixed step control (forcing dx)
        # We set LOOSE tolerances so that max_step becomes the active constraint
        # RK45 error ~ h^5. If tolerances are tight, it adapts h < max_step.
        xi, theta, _ = solve_lane_emden(n, xi_max, res, 
                                      rtol=1.0, atol=1e-3, 
                                      max_step=dx)
        
        # Compare with reference at the grid points of the COARSE solution
        theta_true = ref_interp(xi)
        
        # L_inf Error (Max absolute difference)
        max_err = np.max(np.abs(theta - theta_true))
        errors.append(max_err)
        
        print(f"N={res:4d}, dx={dx:.4f}, MaxError={max_err:.2e}")

    # Analyze Convergence Rate (Slope on log-log plot)
    # log(E) = p * log(dx) + C  => p = slope
    log_dx = np.log(dxs)
    log_err = np.log(errors)
    
    # Linear regression
    slope, intercept = np.polyfit(log_dx, log_err, 1)
    
    # Scatter plot
    plt.figure(figsize=(8, 6))
    plt.loglog(dxs, errors, 'bo-', label='Measured Error')
    
    # Plot ideal 2nd order line
    # y = C * x^2. Pick C to match last point
    C = errors[-1] / (dxs[-1]**2)
    y_ideal = [C * d**2 for d in dxs]
    plt.loglog(dxs, y_ideal, 'r--', label='Order 2 Reference')
    
    plt.xlabel('Step Size (dx)')
    plt.ylabel('Max Absolute Error')
    plt.title(f'Lane-Emden Convergence (Slope = {slope:.2f})')
    plt.grid(True, which="both", ls="-")
    plt.legend()
    
    # Save figure
    os.makedirs('figures', exist_ok=True)
    out_path = 'figures/convergence_test.png'
    plt.savefig(out_path)
    print(f"Saved convergence plot to {out_path}")
    
    print(f"\nConvergence Order (Slope): {slope:.4f}")
    print(f"Expected Order: ~2.0 (RK45 is 5th/4th order adaptive, but local errors accumulate)")
    
    # Assertion
    assert slope > 1.8, f"Convergence order {slope:.2f} is too low! Expected > 1.8"
    print("PASS: Solver is converging at expected high order.")

if __name__ == "__main__":
    test_lane_emden_convergence()
