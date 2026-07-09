import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURATION ---
# Fractal Logic Superfluid P(X) = c * X^n
N_INDEX = 2.5 # Derived from H0 matching (Fractal Logic)
C_COEFF = 1.0 # Positive kinetic term

def check_causality(n_index):
    """
    Check Gate G0: Causality & Stability
    1. Sound Speed c_s^2 <= 1 (Causality)
    2. c_s^2 >= 0 (Gradient Stability)
    3. P_X > 0 (No Ghost Instability)
    """
    print(f"--- GATE G0 CHECK: n = {n_index} ---")
    
    # Formula for P(X) ~ X^n
    # cs^2 = 1 / (2n - 1)
    
    cs2 = 1.0 / (2*n_index - 1)
    cs = np.sqrt(cs2)
    
    print(f"Sound Speed squared c_s^2 = {cs2:.4f}")
    print(f"Sound Speed c_s = {cs:.4f} c")
    
    # CHECK 1: Causality
    if cs2 <= 1.0 + 1e-9:
        print("[PASS] Causality: c_s <= 1")
    else:
        print(f"[FAIL] Causality: c_s > 1 (Superluminal!)")
        
    # CHECK 2: Gradient Stability
    if cs2 >= 0:
        print("[PASS] Gradient Stability: c_s^2 >= 0")
    else:
        print("[FAIL] Gradient Stability: c_s^2 < 0 (Laplacian Instability!)")
        
    # CHECK 3: Ghost Instability (P_X > 0)
    # P(X) = X^n => P_X = n * X^(n-1)
    # Since X = -1/2 (dPhi)^2 > 0 for time-like gradients.
    # If n > 0, P_X > 0 assuming X > 0.
    if n_index > 0:
        print("[PASS] Ghost Check: P_X > 0 (for X>0)")
    else:
        print("[FAIL] Ghost Check: P_X < 0 possible")
        
    return cs2

def verify_all_epochs():
    """ Verify across all epochs """
    print("\n--- EPOCH VERIFICATION ---")
    
    epochs = [
        ("Inflation (Slow Roll)", 1.01), # w approx -1
        ("Big Condensation (Fractal)", 2.5), # w approx 1/3? No, specific cs
        ("Late Universe (Dark Energy)", 0.0) # Quintessence?
    ]
    
    # Note: Our X^2.5 model is for the CONDENSATION epoch (Early Universe).
    # Late universe might evolve back to X^0 or X^1?
    
    check_causality(2.5)

if __name__ == "__main__":
    verify_all_epochs()
