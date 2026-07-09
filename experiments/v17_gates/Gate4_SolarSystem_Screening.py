import numpy as np
import matplotlib.pyplot as plt

# Constants (in SI Units for Solar System)
G = 6.674e-11 # m^3 kg^-1 s^-2
M_sun = 1.989e30 # kg
AU = 1.496e11 # m
a0_universal_si = 1.15e-10 # m/s^2 (converted from Gate 3: 3550 (km/s)^2/kpc)

# Gate 3 Value: 3550 (km/s)^2 / kpc
# 1 (km/s)^2 / kpc = (1e3 m/s)^2 / (3.086e19 m) = 1e6 / 3.086e19 = 3.24e-14 m/s^2
# 3550 * 3.24e-14 = 1.15e-10 m/s^2. Correct.

def solve_field_equation_si(g_bar, a0):
    """
    Standard MOND / Vainshtein form:
    g_tot * mu(x) = g_bar, with mu(x) = x/sqrt(1+x^2)
    This corresponds to the 'Standard' form used in Gate 3 that passed.
    """
    # Root: g^2 = (g_N^2 + sqrt(g_N^4 + 4 g_N^2 a0^2)) / 2
    # g_tot = sqrt(g^2)
    
    term = np.sqrt(g_bar**4 + 4.0 * g_bar**2 * a0**2)
    g2 = (g_bar**2 + term) / 2.0
    g_tot = np.sqrt(g2)
    return g_tot

def check_solar_screening():
    print("--- GATE 4: THE SOLAR SCREEN (Vainshtein Limits) ---")
    print(f"  Using Unified Parameter a0 = {a0_universal_si:.2e} m/s^2 (from Gate 3)")
    
    # Test Points: Mercury, Earth, Saturn
    planets = {
        "Mercury": 0.39 * AU,
        "Earth": 1.0 * AU,
        "Saturn": 9.54 * AU,
        "Kuiper Cliff": 50.0 * AU
    }
    
    print(f"\n{'Planet':<15} | {'Radius (AU)':<12} | {'g_Newton (m/s2)':<18} | {'g_TRXT (m/s2)':<18} | {'Delta g/g':<15}")
    print("-" * 90)
    
    max_delta = 0.0
    
    for name, r in planets.items():
        # Newtonian Field
        g_N = G * M_sun / r**2
        
        # TRXT Field (Screened)
        g_tot = solve_field_equation_si(g_N, a0_universal_si)
        
        # Deviation
        delta_g = g_tot - g_N
        ratio = delta_g / g_N
        
        if abs(ratio) > max_delta:
            max_delta = abs(ratio)
            
        print(f"{name:<15} | {r/AU:<12.2f} | {g_N:<18.5e} | {g_tot:<18.5e} | {ratio:<15.2e}")

    # Cassini Bound Analysis
    # Cassini constraint on PPN gamma: |gamma - 1| < 2.3e-5.
    # Effect on force: F = F_N (1 + delta).
    # Relation roughly: delta ~ (gamma-1).
    # So we need delta < 2e-5 at Saturn orbit (Cassini).
    
    print("\n[Gate 4 Analysis]")
    print(f"  Max Deviation (Saturn/Kuiper): {max_delta:.2e}")
    print(f"  Cassini Bound (Saturn): ~ 2.00e-05")
    
    saturn_delta = (solve_field_equation_si(G*M_sun/(9.54*AU)**2, a0_universal_si) - G*M_sun/(9.54*AU)**2) / (G*M_sun/(9.54*AU)**2)
    
    if saturn_delta < 2.0e-5:
        print("\n>>> GATE 4 STATUS: PASS <<<")
        print(f"  √ Solar System Screening is effective.")
        print(f"  √ Deviation at Saturn ({saturn_delta:.2e}) is below Cassini limit (2e-5).")
    else:
        print("\n>>> GATE 4 STATUS: FAIL <<<")
        print(f"  X Deviation at Saturn ({saturn_delta:.2e}) exceeds observation limit.")
        print("  The Theory predicts too much 'Dark Matter Force' inside the Solar System.")

if __name__ == "__main__":
    check_solar_screening()
