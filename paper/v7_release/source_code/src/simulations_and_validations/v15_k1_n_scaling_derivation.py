"""
TRXT Phase K.1: Formal Derivation of n(rho)
===========================================
Deriving the Scale-Dependent Polytropic Index from Logic Lattice Melting.

Physical Model:
1. Lattice Phase (High Density): n -> Infinity (Incompressible)
2. Superfluid Phase (Low Density): n -> 1.5 (Acoustic condition)

Transformation:
n(rho) = n_min + (n_max - n_min) * [1 / (1 + (rho_crit/rho)^p)]
"""

import numpy as np
import matplotlib.pyplot as plt

def n_running(rho, rho_crit, n_min=1.37, n_max=20.74, p=1.0):
    """
    Returns the effective polytropic index n as a function of density rho.
    Uses the logic saturation sigmoid.
    """
    return n_min + (n_max - n_min) / (1.0 + (rho_crit / rho)**p)

def plot_n_scaling():
    # Density range from Cosmic (10^-30) to Earth-Lattice (10^2) g/cm^3
    rho = np.logspace(-30, 2, 500)
    
    # We set rho_crit to the "Logic Density" where decoherence occurs
    # Estimating rho_crit ~ 10^-27 g/cm^3 (Typical cosmic voids)
    rho_crit = 1e-26 
    
    n_vals = n_running(rho, rho_crit)
    
    plt.figure(figsize=(10, 6))
    plt.semilogx(rho, n_vals, 'b-', lw=2)
    
    # Highlighting key zones
    plt.axvline(1e-24, color='g', linestyle='--', label='Galactic Halo Scale')
    plt.axvline(1e-2, color='r', linestyle='--', label='MaVaN/Neutrino Scale')
    
    plt.axhline(1.37, color='gray', linestyle=':', label='SPARC n=1.37')
    plt.axhline(20.74, color='gray', linestyle=':', label='Lattice n=20.74')
    
    plt.title("TRXT Scale-Relativity: Running Polytropic Index $n(\\rho)$")
    plt.xlabel("Density $\\rho$ [g/cm$^3$]")
    plt.ylabel("Polytropic Index $n$")
    plt.legend()
    plt.grid(True, which="both", alpha=0.2)
    plt.savefig('v15_k1_n_scaling_curve.png')
    print("Saved 'v15_k1_n_scaling_curve.png'")

if __name__ == "__main__":
    plot_n_scaling()
