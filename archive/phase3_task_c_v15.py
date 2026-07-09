import numpy as np
import matplotlib.pyplot as plt
from TRXT_Analysis_Engine import TRXTAnalyzer

def main():
    print("=== TRXT PROTOCOL: TASK C (DARK TOWER GAP) V15 ===")
    engine = TRXTAnalyzer()
    
    # 1. Generate Candidates
    candidates = [engine.predict_mass(2**k, 2**k) for k in range(5, 8)] # 32, 64, 128 -> mass(32,32)...
    
    # 2. Prune
    GAP = 20.0
    valid_candidates = engine.prune_dark_tower(candidates, mass_gap=GAP)
    
    if not valid_candidates:
        print("[WARNING] No candidates survive the Mass Gap!")
        return

    # 3. Predict properties for Survivor (22.8 GeV)
    survivor = valid_candidates[0] # Should be 22.8
    print(f"\n[PREDICTION] Survivor Candidate: {survivor:.4f} GeV")
    
    # Calculate suppressed cross-section (Topology Suppression)
    g_eff = 1e-39 * (survivor / engine.M_STAR)**4
    print(f" -> Predicted Cross-Section (g ~ m^4): {g_eff:.2e} cm^2")
    print(f" -> DARWIN Sensitivity limit at 20 GeV: ~1e-48 cm^2")
    
    if g_eff > 1e-48:
        print(" -> STATUS: VISIBLE to Next-Gen Detectors (DARWIN/LZ).")
    else:
        print(" -> STATUS: BURRIED in Neutrino Floor.")

if __name__ == "__main__":
    main()
