
import numpy as np
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path("trxt_validation/src").absolute()))

from rotation_curves import (
    solve_lane_emden,
    enclosed_mass,
    rotation_velocity,
    fit_galaxy_rotation
)

def debug_grid_refinement():
    print("\n=== DEBUG: Grid Refinement ===")
    n = 1.5
    errors = []
    n_points_list = [100, 200, 400, 800]
    
    # Reference solution with very fine grid
    xi_ref, theta_ref, _ = solve_lane_emden(n=n, n_points=2000, xi_max=5.0)
    print(f"Reference grid size: {len(xi_ref)}")
    
    for n_pts in n_points_list:
        xi, theta, _ = solve_lane_emden(n=n, n_points=n_pts, xi_max=5.0)
        
        # Interpolate reference to current grid
        theta_interp = np.interp(xi, xi_ref, theta_ref)
        
        # L_inf error
        error = np.max(np.abs(theta - theta_interp))
        errors.append(error)
        print(f"N={n_pts}, Error={error:.2e}")
    
    if errors[-1] < errors[0]:
        print("PASS: Error decreased.")
    else:
        print("FAIL: Error did not decrease.")
        print(f"Error[0] = {errors[0]}")
        print(f"Error[-1] = {errors[-1]}")

def debug_fit_galaxy():
    print("\n=== DEBUG: fit_galaxy_rotation ===")
    # Generate synthetic rotation curve from Lane-Emden
    n_true = 1.5
    xi, theta, dtheta = solve_lane_emden(n=n_true, xi_max=10)
    M_enc = enclosed_mass(xi, theta, n=n_true)
    
    # Convert to physical units
    alpha = 5.0  # kpc
    M_total = 1e11  # M_sun
    
    r_data = xi[10::20] * alpha
    M_data = M_enc[10::20] * M_total / M_enc[-1]
    v_data = rotation_velocity(r_data, M_data)
    v_err = 0.05 * v_data  # 5% error
    
    # Add small noise
    np.random.seed(42)
    v_noisy = v_data + np.random.normal(0, 0.02 * v_data)
    
    try:
        # Fit
        result = fit_galaxy_rotation(r_data, v_noisy, v_err, n=n_true)
        print("Result:", result)
        if result['success'] and result['chi2_red'] < 5.0:
            print("PASS: Fit successful.")
        else:
            print("FAIL: Fit failed or chi2 too high.")
    except Exception as e:
        print(f"FAIL: Exception during fit: {e}")

if __name__ == "__main__":
    debug_grid_refinement()
    debug_fit_galaxy()
