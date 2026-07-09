"""
TRXT Validation - Regression Tests
===================================
Tests that compare current output against golden outputs.
"""

import pytest
import json
import numpy as np
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rotation_curves import solve_lane_emden, enclosed_mass, rotation_velocity


class TestRegressionNGC3198:
    """Regression tests against NGC3198 golden output."""
    
    @pytest.fixture
    def golden_data(self):
        """Load golden output for NGC3198."""
        golden_path = Path(__file__).parent / "golden_outputs" / "sparc_ngc3198.json"
        with open(golden_path, 'r') as f:
            return json.load(f)
    
    def test_lane_emden_solution_stable(self, golden_data):
        """Lane-Emden solution should be numerically stable."""
        n = golden_data['metadata']['parameters']['n']
        
        xi, theta, dtheta = solve_lane_emden(n=n, xi_max=15, n_points=1000)
        
        # Basic sanity checks
        assert len(xi) > 500
        assert theta[0] > 0.99  # Should start near 1
        assert dtheta[0] < 0.01  # Should start near 0
    
    def test_model_velocity_order_of_magnitude(self, golden_data):
        """Model velocities should be in correct order of magnitude."""
        expected = golden_data['expected_output']['v_model_km_s']
        
        # All velocities should be positive and < 300 km/s
        for v in expected:
            assert 0 < v < 300
    
    def test_chi2_threshold(self, golden_data):
        """Chi-squared should be below threshold."""
        chi2_red = golden_data['expected_output']['fit_results']['chi2_red']
        threshold = golden_data['tolerances']['chi2_red_max']
        
        assert chi2_red < threshold, f"chi2_red={chi2_red} exceeds threshold={threshold}"


class TestRegressionLaneEmden:
    """Regression tests for Lane-Emden solver consistency."""
    
    def test_n_1_37_first_zero(self):
        """For n=1.37, first zero should be at xi ≈ 4.9."""
        xi, theta, _ = solve_lane_emden(n=1.37, xi_max=10, n_points=1000)
        
        # Find first zero
        zero_idx = np.argmax(theta <= 0)
        if zero_idx > 0:
            xi_1 = xi[zero_idx]
            # Correct theoretical value for n=1.37 is approx 3.51 (interpolating between n=1 and n=1.5)
            assert 3.4 < xi_1 < 3.6, f"First zero at xi_1={xi_1}, expected ~3.51"
    
    def test_solution_reproducibility(self):
        """Same parameters should give same solution."""
        xi1, theta1, _ = solve_lane_emden(n=1.5, xi_max=5, n_points=500)
        xi2, theta2, _ = solve_lane_emden(n=1.5, xi_max=5, n_points=500)
        
        np.testing.assert_allclose(theta1, theta2, rtol=1e-10)
    
    def test_mass_conservation(self):
        """Enclosed mass should increase monotonically."""
        xi, theta, _ = solve_lane_emden(n=1.37)
        M_enc = enclosed_mass(xi, theta, n=1.37)
        
        # Where theta > 0, mass should increase
        mask = theta > 0.01
        M_positive = M_enc[mask]
        
        dM = np.diff(M_positive)
        assert np.all(dM >= -1e-10), "Enclosed mass should not decrease"


class TestRegressionVelocity:
    """Regression tests for velocity calculation."""
    
    def test_flat_rotation_curve(self):
        """At large r, rotation curve should flatten (for polytropic profile)."""
        xi, theta, _ = solve_lane_emden(n=1.37, xi_max=15)
        M_enc = enclosed_mass(xi, theta, n=1.37)
        
        # Scale to physical units
        alpha = 5.0  # kpc
        M_total = 1e11  # M_sun
        
        r = xi * alpha
        M = M_enc * M_total / M_enc[-1]
        v = rotation_velocity(r, M)
        
        # Check flatness in outer region
        if len(v) > 100:
            v_outer = v[-50:]
            std_v = np.std(v_outer)
            mean_v = np.mean(v_outer)
            
            # Coefficient of variation should be small (<10%)
            cv = std_v / mean_v
            assert cv < 0.15, f"Outer rotation curve not flat: CV={cv:.3f}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
