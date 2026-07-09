import numpy as np
import scipy.integrate as integrate
import scipy.optimize as optimize

# --- CONSTANTS ---
CLIGHT = 299792.458
THETA_S_ROBUST = 0.0104109
OMEGA_M_H2 = 0.1430
OMEGA_B_H2 = 0.02237
OMEGA_R_H2 = 4.1834e-5
SHOES_H0 = 73.04

def hubble_function(z, h, omega_m_h2, omega_r_h2, omega_de):
    Om = omega_m_h2 / h**2
    Or = omega_r_h2 / h**2
    return np.sqrt(Om * (1+z)**3 + Or * (1+z)**4 + omega_de)

def sound_horizon_integrand(z, h, cs_factor):
    """
    cs_factor: multiple of c (speed of light).
    If we assume CONSTANT effective sound speed during recombination era.
    """
    h_val = 100.0 * h * hubble_function(z, h, OMEGA_M_H2, OMEGA_R_H2, 1.0 - (OMEGA_M_H2+OMEGA_R_H2)/h**2)
    return (cs_factor * CLIGHT) / h_val

def angular_distance_integrand(z, h):
    h_val = 100.0 * h * hubble_function(z, h, OMEGA_M_H2, OMEGA_R_H2, 1.0 - (OMEGA_M_H2+OMEGA_R_H2)/h**2)
    return CLIGHT / h_val

def solve_required_cs():
    """
    Inverse Problem:
    Given H0 = 73.04 (Fixed)
    Find cs_factor that satisfies Theta_s = r_s / D_A
    """
    h_target = SHOES_H0 / 100.0
    z_star = 1090.0
    
    # 1. Calculate D_A (Fixed by H0 geometry)
    dm, _ = integrate.quad(lambda z: angular_distance_integrand(z, h_target), 0, z_star)
    
    # 2. Required r_s to match Theta_s
    rs_required = dm * THETA_S_ROBUST
    print(f"For H0 = {SHOES_H0}, we need Geometric D_M = {dm:.2f} Mpc")
    print(f"REQUIRED Sound Horizon r_s = {rs_required:.2f} Mpc")
    
    # 3. Find effective c_s that gives this r_s
    def rs_discrepancy(cs_guess):
        rs_calc, _ = integrate.quad(lambda z: sound_horizon_integrand(z, h_target, cs_guess), z_star, np.inf)
        return rs_calc - rs_required
        
    cs_solution = optimize.brentq(rs_discrepancy, 0.1, 0.6) # Search range 0.1c to 0.6c
    
    print(f"\nREQUIRED Effective Sound Speed c_s = {cs_solution:.5f} c")
    print(f"Standard Plasma c_s approx 0.577 c (1/sqrt(3))")
    
    cs2_req = cs_solution**2
    print(f"REQUIRED c_s^2 = {cs2_req:.5f}")
    
    # 4. Map back to Lagrangian P(X) ~ X^n
    # cs^2 = 1 / (2n - 1)  =>  2n - 1 = 1/cs^2  => 2n = 1/cs^2 + 1 => n = 0.5 * (1/cs^2 + 1)
    
    n_required = 0.5 * (1.0/cs2_req + 1.0)
    print(f"\nIMPLIED LAGRANGIAN POWER n:")
    print(f"P(X) ~ X^{n_required:.3f}")
    
    print("\n INTERPRETATION:")
    if abs(n_required - 2.5) < 0.1:
        print("Matches n=2.5 (Fractal logic?)")
    elif abs(n_required - 3.0) < 0.5:
        print("Matches n=3 (Logic Triplet) with mixing?")
    
    return n_required

if __name__ == "__main__":
    solve_required_cs()
