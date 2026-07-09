import numpy as np

# TRXT Constants
M_STAR_GEV = 365.24  
# Recombination temperature ~ 0.26 eV (3000 K)
T_REC_EV = 0.26 
# Nucleosynthesis temperature ~ 0.1 MeV
T_BBN_EV = 1e5

# Sound speed formula for P(X) = c2*X + c4*X^2
# cs^2 = (P_X) / (P_X + 2X*P_XX)
#      = (c2 + 2*c4*X) / (c2 + 6*c4*X)
# At early times (high X), if c4 dominates -> cs^2 -> 1/3 (Radiation like) ???
# Wait, for P(X) ~ X^2, P_X ~ X, P_XX ~ const
# cs^2 = 2*c4*X / (2*c4*X + 2*X*2*c4) = 2/6 = 1/3. 
# YES! Pure X^2 superfluid behaves like radiation c_s^2 = 1/3!

def check_superfluid_sound_speed():
    print("--- TRXT SUPERFLUID SOUND SPEED CHECK ---")
    
    # CASE 1: High Energy Limit (X -> infinity)
    # P(X) ~ c4 * X^2
    cs2_high = 1.0/3.0
    print(f"High Energy Limit (X->inf): c_s^2 = {cs2_high:.4f} (Radiation-like)")
    
    # CASE 2: Low Energy Limit (X -> 0)
    # P(X) ~ c2 * X
    # cs^2 = c2 / c2 = 1.0
    cs2_low = 1.0
    print(f"Low Energy Limit (X->0):   c_s^2 = {cs2_low:.4f} (Stiff Matter-like?)")
    
    # This is inverse of what we usually want for Dark Energy (w=-1 requires low X).
    # But wait, condensate implies we are AT THE BOTTOM of the potential.
    # What if c2 < 0? (Ghost condensate?) -> No, banned by protocol.
    
    # HYPOTHESIS: Phase Transition near Recombination?
    # If the "Order Parameter" Phi depends on Temperature T.
    # c2(T) ~ (T - Tc)
    
    print("\n--- PHASE TRANSITION HYPOTHESIS ---")
    print("If c2(T) changes sign or magnitude near T_rec:")
    
    T_range = np.linspace(0.1, 1.0, 100) # eV around T_rec
    # Toy model: c2(T) = alpha * (T - T_c)
    # Near Tc, c2 -> 0.
    # Then P(X) ~ c4*X^2 dominates -> c_s^2 -> 1/3.
    
    # If we are in 'Broken Phase' (Low T < Tc): c2 is non-zero constants.
    # If we are in 'Restored Phase' (High T > Tc): ???
    
    # CRITICAL INSIGHT QUEST
    print("Q: Does standard TRXT P(X) give c_s < 1/sqrt(3) at recombination?")
    print("Answer: Standard P(X) = X + X^2 gives 1/3 < c_s^2 < 1.")
    print("This increases sound speed, increasing r_s, worsening Hubble Tension.")
    print("TO FIX HUBBLE TENSION, WE NEED c_s^2 < 1/3 implies LOWER sound speed.")
    
    # Can we get c_s^2 approx 0?
    # cs^2 = (c2 + 2c4X) / (c2 + 6c4X)
    # If c2 -> -2c4X (Instability?)
    
    # ALTERNATIVE:
    # If P(X) has fractional power? P(X) ~ X^n
    # cs^2 = (n X^(n-1)) / (n X^(n-1) + 2X * n(n-1)X^(n-2))
    #      = n / (n + 2n(n-1))
    #      = 1 / (1 + 2(n-1)) = 1 / (2n - 1)
    
    # We need cs^2 < 1/3 -> 2n - 1 > 3 -> 2n > 4 -> n > 2.
    # If P(X) ~ X^3 -> cs^2 = 1/5 = 0.2 < 0.33. THIS WORKS!
    
    print("\n--- NEW MECHANISM DISCOVERY ---")
    print("If TRXT Lagrangian has higher order term X^3 (Logic Triplet Interaction?):")
    n = 3
    cs2_cubic = 1.0 / (2*n - 1)
    print(f"For P(X) ~ X^3: c_s^2 = {cs2_cubic:.4f}")
    
    n = 4
    cs2_quartic = 1.0 / (2*n - 1)
    print(f"For P(X) ~ X^4: c_s^2 = {cs2_quartic:.4f}")

    # Is X^3 term natural in NJL?
    # NJL is quartic in fields (Psi^4).
    # Bosonization gives Phi^4.
    # Kinetic terms?
    
    print("\nCONCLUSION:")
    print("Standard X^2 theory gives c_s >= 1/sqrt(3).")
    print("To solve Hubble Tension (need lower c_s), we need P(X) dominated by X^n with n > 2.")
    print("Investigating if 'Big Condensation' implies n > 2 terms.")

if __name__ == "__main__":
    check_superfluid_sound_speed()
