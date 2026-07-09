import numpy as np
from TRXT_Analysis_Engine import TRXTAnalyzer

def main():
    print("=== TRXT PROTOCOL: TASK A (INVISIBLE GHOST) V15 ===")
    engine = TRXTAnalyzer()
    
    target_mass = engine.predict_mass(16, 16)
    diff, error = engine.analyze_invisible_width(target_mass)
    
    # Logic:
    # If the 45 GeV mode exists and mixes, does it VIOLATE the LEP constraint?
    # LEP says N_nu = 2.984 +/- 0.008.
    # The "Missing" width is -2.4 MeV (SM predicts MORE than seen).
    # Adding a NEW invisible particle would ADD to the width, making the discrepancy WORSE (Data << Prediction + New).
    # UNLESS: The new particle interferes destructively.
    
    print(f"\n[INTERPRETATION] Limit Check")
    if diff < 0:
         print(" -> CAUTION: LEP data shows a DEFICIT in invisible width (-2.4 MeV vs SM).")
         print(" -> Adding a standard invisible scalar (positive width) worsens the fit.")
         print(" -> CONCLUSION: The 45 GeV Ghost must be 'Dark-Phobic' or interfere destructively to survive.")
    else:
         print(" -> Room for New Physics exists.")

if __name__ == "__main__":
    main()
