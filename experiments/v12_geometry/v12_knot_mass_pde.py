import numpy as np
import sys
from scipy.optimize import root_scalar

print("==========================================================")
print("TRXT V12: 'PURE GEOMETRY' RESEARCH MODULE 1")
print("TARGET: Prove topological defect complexity -> Fermion Mass")
print("PROTOCOL: Master Protocol V2.0 (The Iron Constitution)")
print("==========================================================\n")

# REAL DATA (Source of Truth - Article IV)
# Lepton masses in MeV
m_real = np.array([0.510998, 105.658, 1776.86]) 
names = ['Electron (e)', 'Muon (mu)', 'Tau (tau)']

def njl_gap_integral(m, Lambda):
    """
    Evaluates the basic right-hand side of the 3D NJL gap equation for dynamical mass generation.
    Integral of d^3p / sqrt(p^2 + m^2) from 0 to Lambda
    """
    if m <= 0:
        return Lambda**2
    # Analytical evaluation of the integral
    term1 = Lambda * np.sqrt(Lambda**2 + m**2)
    term2 = m**2 * np.arcsinh(Lambda / m)
    return 0.5 * (term1 - term2)

def solve_gap_mass(G_eff, Lambda):
    """
    Solves 1 / G_eff = (1 / 2*pi^2) * njl_gap_integral(m, Lambda)
    """
    target = (2 * np.pi**2) / G_eff
    
    # Check condition for spontaneous symmetry breaking
    if target >= 0.5 * Lambda**2:
        return 0.0 # No mass gap generated
        
    def objective(m):
        return njl_gap_integral(m, Lambda) - target
        
    try:
        # Bracket between near 0 and Lambda
        sol = root_scalar(objective, bracket=[1e-8, Lambda*10], method='brentq')
        return sol.root
    except ValueError:
        return 0.0

def evaluate_topological_model(model_name, T_n_values, Lambda_val, g_0_val):
    """
    Evaluates a specific geometric model where G_eff = g_0 * T_n
    T_n are the topological invariants for the 3 generations.
    """
    print(f"--- Testing Model: {model_name} ---")
    print(f"Topological Invariants (T_n): {T_n_values}")
    
    m_pred = np.zeros(3)
    for i, T_n in enumerate(T_n_values):
        G_eff = g_0_val * T_n
        m_pred[i] = solve_gap_mass(G_eff, Lambda_val)
        
    print(f"Predicted Masses (MeV): {m_pred}")
    print(f"Real Masses      (MeV): {m_real}")
    
    # Calculate ratios (mass hierarchy is scale-independent to the UV cutoff)
    pred_ratios = [m_pred[1]/m_pred[0] if m_pred[0]>0 else np.nan, 
                   m_pred[2]/m_pred[1] if m_pred[1]>0 else np.nan]
    real_ratios = [m_real[1]/m_real[0], m_real[2]/m_real[1]]
    
    print(f"Predicted Ratios (mu/e, tau/mu): {pred_ratios}")
    print(f"Real Ratios      (mu/e, tau/mu): {real_ratios}")
    
    # Koide parameter K = (m1+m2+m3) / (sqrt(m1)+sqrt(m2)+sqrt(m3))^2
    def koide_k(masses):
        if np.any(masses <= 0): return np.nan
        return np.sum(masses) / (np.sum(np.sqrt(masses)))**2
        
    pred_koide = koide_k(m_pred)
    real_koide = koide_k(m_real)
    
    print(f"Predicted Koide K: {pred_koide:.6f}")
    print(f"Real Koide K     : {real_koide:.6f}")
    
    # Audit Check
    if np.isnan(pred_koide) or abs(pred_koide - real_koide)/real_koide > 0.05:
        print(">> GATE STATUS: FAILED (Hierarchy or Koide constraint violated)")
    else:
        print(">> GATE STATUS: PASSED (Hierarchy organically derived!)")
    print("")

# ---------------------------------------------------------
# EXECUTION (Gate G5 Test)
# ---------------------------------------------------------
print("Executing Global Gap Equation Solvers for Geometric T_n models...\n")

# We choose a generic UV Cutoff Lambda ~ 10^4 MeV (e.g. Electroweak symmetry breaking scale)
Lambda_UV = 1e4 
# g_0 must be set organically to break chiral symmetry. We need G_eff > 2*pi^2 / (0.5*Lambda^2)
# target_min_G = (4 * np.pi**2) / (Lambda_UV**2) = 3.94e-7

# Model A: Winding Number (Hopf Charge) Q = 1, 2, 3
evaluate_topological_model(
    model_name="Winding Number (Q = 1, 2, 3)", 
    T_n_values=[1, 2, 3], 
    Lambda_val=Lambda_UV, 
    g_0_val=4.5e-7 # Minimal coupling to induce breaking
)

# Model B: Torus Knots Crossing Numbers T(2, q) -> C_N = 3, 5, 7
# (Assuming generation 1 is the simplest non-trivial knot, Trefoil)
evaluate_topological_model(
    model_name="Torus Knot Crossing Numbers (C_N = 3, 5, 7)", 
    T_n_values=[3, 5, 7], 
    Lambda_val=Lambda_UV, 
    g_0_val=1.5e-7 
)

# Model C: Geometric Knot Complement Volumes (approx for Simplest 3 Hyperbolic Knots)
# e.g., Figure-8 (2.0298), 5_2 knot (2.828), 6_1 knot (3.163)
evaluate_topological_model(
    model_name="Hyperbolic Complement Volumes", 
    T_n_values=[2.0298, 2.8281, 3.1639], 
    Lambda_val=Lambda_UV, 
    g_0_val=2.2e-7 
)

print("AUDIT COMPLETE.")
print("If all FAILED, the direct linear map G_eff = g_0 * T_n is insufficient.")
print("We must derive exactly how Seifert Area scales with T_n.")
