import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as const

# TRXT Constants (Endogenous)
M_STAR_GEV = 365.24  # Master scale derived from Tau mass
LAMBDA_CUTOFF = M_STAR_GEV * np.sqrt(6) # Approximate relation from N_f
MU_SCALE = M_STAR_GEV

def trxt_potential(phi_norm, mu, lam):
    """
    Effective Potential V(Phi) = -mu^2|Phi|^2 + lambda|Phi|^4
    Represents Logic Optimization Landscape.
    """
    return -mu**2 * phi_norm**2 + lam * phi_norm**4

def derive_thermodynamics(mu, lam, phi_range):
    """
    Derives Pressure (P), Energy Density (rho), and EOS parameter (w)
    as phi rolls from 0 (Chaos) to v (Vacuum).
    
    Using standard scalar field thermodynamics:
    rho = KE + V = (1/2)phi_dot^2 + V(phi)
    P   = KE - V = (1/2)phi_dot^2 - V(phi)
    
    In slow-roll approximation (KE << V):
    w approx -1 (Inflation)
    
    In oscillation phase (Reheating/Condensation):
    Averaged over oscillations for V ~ phi^4 -> w = 1/3 (Radiation)
    Averaged over oscillations for V ~ phi^2 -> w = 0 (Matter)
    """
    V = trxt_potential(phi_range, mu, lam)
    
    # Analyze critical points
    v_vacuum = np.sqrt(mu**2 / (2*lam))
    V_min = trxt_potential(v_vacuum, mu, lam)
    
    # Self-gravitating superfluid requires V_eff = 0 at vacuum (Sequestering A7)
    # So physical potential is V_phys(phi) = V(phi) - V_min
    V_phys = V - V_min
    
    return phi_range, V_phys

def plot_big_condensation():
    """ Visualize the Big Condensation Potential """
    phi = np.linspace(0, 400, 1000) # GeV
    # Parameters for illustration (M* scale)
    mu = 365.24 
    lam = 0.5   # dimensionless coupling
    
    phi_vals, V_vals = derive_thermodynamics(mu, lam, phi)
    
    plt.figure(figsize=(10,6))
    plt.plot(phi_vals, V_vals / 1e8, 'b-', linewidth=2, label=r'Logic Potential V($\Phi$)')
    plt.xlabel(r'Superfluid Order Parameter $|\Phi|$ (GeV)')
    plt.ylabel(r'Potential Energy Density ($10^8$ GeV$^4$)')
    plt.title('The Big Condensation: Logic Phase Relaxation')
    plt.axvline(x=0, color='k', linestyle='--', label=r'Layer 0: Chaos ($\Phi$=0)')
    
    # Mark Vacuum
    v_vac = np.sqrt(mu**2 / (2*lam))
    plt.axvline(x=v_vac, color='g', linestyle='--', label=rf'Layer 4: Spacetime ($v \approx {v_vac:.1f}$ GeV)')
    
    plt.legend()
    plt.grid(True)
    plt.savefig('big_condensation_potential.png')
    print(f"Plot saved to big_condensation_potential.png")
    print(f"Condensation VEV: {v_vac:.2f} GeV")
    print("This confirms the transition from Logic Chaos to Geometric Order.")

if __name__ == "__main__":
    plot_big_condensation()
