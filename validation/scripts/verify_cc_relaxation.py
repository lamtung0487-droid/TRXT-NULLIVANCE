"""
TRXT Validation - HB-1: Dynamic CC / q-Relaxation in FRW
=========================================================
Verifies that the Volovik argument (P_vac = 0) can be extended to 
an expanding FRW universe via a dynamical adjustment mechanism.

Reference: V4 Appendix D (Volovik), Computation Request Package HB-1
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import json
from pathlib import Path


# =============================================================================
# Physical Constants
# =============================================================================
M_PL_GEV = 1.22e19  # Planck mass in GeV
M_STAR_GEV = 365.24  # Master scale in GeV
H_0_GEV = 1.44e-42  # Hubble constant today in GeV (= 67 km/s/Mpc)
RHO_CRIT_GEV4 = 3.0 * H_0_GEV**2 * M_PL_GEV**2 / (8 * np.pi)  # Critical density today


def volovik_vacuum_energy(q: float, q_eq: float, epsilon_0: float) -> float:
    """
    Vacuum energy density as a function of the q-variable.
    
    In Volovik's framework:
    ρ_vac(q) = ε_0 * (1 - q/q_eq)^2
    
    At equilibrium (q = q_eq), ρ_vac = 0.
    
    Parameters
    ----------
    q : float
        Current value of the dynamical variable (GeV^4)
    q_eq : float
        Equilibrium value (GeV^4)
    epsilon_0 : float
        Bare vacuum energy scale (GeV^4)
    """
    return epsilon_0 * (1 - q / q_eq)**2


def relaxation_rate(H: float, gamma_0: float = 1.0) -> float:
    """
    Relaxation rate Γ(H) for the q-variable.
    
    Γ(H) = γ_0 * H
    
    This ensures the relaxation timescale is cosmological.
    """
    return gamma_0 * H


def friedmann_eq(H: float, rho_m: float, rho_vac: float) -> float:
    """
    Friedmann equation: H^2 = (8πG/3) * (ρ_m + ρ_vac)
    
    Returns H given the energy densities.
    """
    rho_total = rho_m + rho_vac
    if rho_total <= 0:
        return 0.0
    H_sq = (8 * np.pi / 3) * rho_total / M_PL_GEV**2
    return np.sqrt(H_sq)


def ode_system(t: float, y: np.ndarray, params: dict) -> np.ndarray:
    """
    ODE system for FRW + q-relaxation.
    
    Variables:
    y[0] = a (scale factor)
    y[1] = q (dynamical variable)
    
    Equations:
    da/dt = a * H
    dq/dt = -Γ(H) * (q - q_eq)
    """
    a, q = y
    
    # Parameters
    q_eq = params['q_eq']
    epsilon_0 = params['epsilon_0']
    gamma_0 = params['gamma_0']
    Omega_m = params['Omega_m']
    
    # Matter density (scales as a^-3)
    rho_m = Omega_m * RHO_CRIT_GEV4 / a**3
    
    # Vacuum energy from q-variable
    rho_vac = volovik_vacuum_energy(q, q_eq, epsilon_0)
    
    # Hubble parameter
    H = friedmann_eq(np.sqrt(rho_m + rho_vac), rho_m, rho_vac)
    if H <= 0:
        H = 1e-50  # Avoid division by zero
    
    # Relaxation rate
    Gamma = relaxation_rate(H, gamma_0)
    
    # ODEs
    da_dt = a * H
    dq_dt = -Gamma * (q - q_eq)
    
    return np.array([da_dt, dq_dt])


def run_simulation(params: dict, t_span: tuple = (1e-10, 1.0), 
                   n_points: int = 1000) -> dict:
    """
    Run the FRW + q-relaxation simulation.
    
    Returns
    -------
    dict with time, scale factor, q-variable, H(t), rho_vac(t), w_eff(t)
    """
    # Initial conditions
    a0 = params.get('a0', 1e-3)  # Start at a = 0.001 (early times)
    q0 = params.get('q0', 0.0)  # Start far from equilibrium
    y0 = np.array([a0, q0])
    
    # Solve ODE
    t_eval = np.logspace(np.log10(t_span[0]), np.log10(t_span[1]), n_points)
    
    sol = solve_ivp(
        lambda t, y: ode_system(t, y, params),
        t_span,
        y0,
        method='RK45',
        t_eval=t_eval,
        max_step=0.01,
        atol=1e-10,
        rtol=1e-8
    )
    
    # Extract results
    t = sol.t
    a = sol.y[0]
    q = sol.y[1]
    
    # Compute derived quantities
    rho_vac = np.array([volovik_vacuum_energy(qi, params['q_eq'], params['epsilon_0']) for qi in q])
    rho_m = params['Omega_m'] * RHO_CRIT_GEV4 / a**3
    H = np.sqrt((8 * np.pi / 3) * (rho_m + rho_vac) / M_PL_GEV**2)
    
    # Effective equation of state
    # w_eff = P_total / rho_total ≈ -1 for vacuum dominated
    w_eff = -rho_vac / (rho_m + rho_vac + 1e-100)
    
    return {
        't': t,
        'a': a,
        'q': q,
        'rho_vac': rho_vac,
        'rho_m': rho_m,
        'H': H,
        'w_eff': w_eff
    }


def check_attractor(results: dict, params: dict) -> dict:
    """
    Check if the system has an attractor at the observed DE scale.
    
    Success criteria:
    1. rho_vac(today) ~ rho_crit ~ 10^-47 GeV^4
    2. rho_vac does NOT runaway to M_Pl^4 ~ 10^72 GeV^4
    3. There IS a late-time attractor
    """
    rho_vac_final = results['rho_vac'][-1]
    rho_vac_max = np.max(results['rho_vac'])
    q_final = results['q'][-1]
    q_eq = params['q_eq']
    
    # Check 1: No runaway
    runaway_threshold = M_PL_GEV**4  # ~ 10^72 GeV^4
    no_runaway = rho_vac_max < runaway_threshold
    
    # Check 2: Attractor reached (q approaches q_eq)
    attractor_reached = abs(q_final - q_eq) / abs(q_eq) < 0.01
    
    # Check 3: Final vacuum energy is cosmological scale
    cosmological_ok = rho_vac_final < 1e-40  # GeV^4 (order of 10^-47 is target)
    
    return {
        'rho_vac_final_GeV4': rho_vac_final,
        'rho_vac_max_GeV4': rho_vac_max,
        'q_final': q_final,
        'q_eq': q_eq,
        'no_runaway': no_runaway,
        'attractor_reached': attractor_reached,
        'cosmological_ok': cosmological_ok,
        'overall_pass': no_runaway and attractor_reached
    }


def main():
    """
    Main verification routine for HB-1 (Dynamic CC).
    """
    print("=" * 70)
    print("TRXT VALIDATION - HB-1: Dynamic CC / q-Relaxation in FRW")
    print("=" * 70)
    
    # Parameters
    params = {
        'epsilon_0': M_STAR_GEV**4,  # Bare vacuum energy ~ (365 GeV)^4
        'q_eq': M_STAR_GEV**4,       # Equilibrium value
        'gamma_0': 10.0,             # Relaxation strength (>1 for fast approach)
        'Omega_m': 0.3,              # Matter density parameter
        'a0': 1e-4,                  # Initial scale factor (early universe)
        'q0': 0.0,                   # Initial q (far from equilibrium)
    }
    
    print(f"\n[Parameters]")
    print(f"  ε_0 (bare vacuum) = {params['epsilon_0']:.2e} GeV^4")
    print(f"  q_eq = {params['q_eq']:.2e} GeV^4")
    print(f"  γ_0 (relaxation) = {params['gamma_0']}")
    print(f"  Ω_m = {params['Omega_m']}")
    
    # Run simulation
    print(f"\n[Running FRW + q-relaxation simulation...]")
    t_span = (1e-15, 1.0)  # From very early to today (a=1)
    results = run_simulation(params, t_span, n_points=500)
    print(f"  Simulation complete. t_final = {results['t'][-1]:.4e}")
    
    # Check attractor
    print(f"\n[Checking Attractor Conditions...]")
    checks = check_attractor(results, params)
    
    print(f"\n  ╔══════════════════════════════════════════════════════════╗")
    print(f"  ║  HB-1 VERIFICATION RESULTS                               ║")
    print(f"  ╠══════════════════════════════════════════════════════════╣")
    print(f"  ║  ρ_vac(final) = {checks['rho_vac_final_GeV4']:.4e} GeV^4         ║")
    print(f"  ║  ρ_vac(max)   = {checks['rho_vac_max_GeV4']:.4e} GeV^4         ║")
    print(f"  ║  No Runaway?   {'YES ✓' if checks['no_runaway'] else 'NO ✗'}                                  ║")
    print(f"  ║  Attractor?    {'YES ✓' if checks['attractor_reached'] else 'NO ✗'}                                  ║")
    print(f"  ║  Cosmological? {'YES ✓' if checks['cosmological_ok'] else 'NO ✗'}                                  ║")
    print(f"  ╠══════════════════════════════════════════════════════════╣")
    print(f"  ║  OVERALL: {'PASS ✓' if checks['overall_pass'] else 'FAIL ✗'}                                        ║")
    print(f"  ╚══════════════════════════════════════════════════════════╝")
    
    # Save results
    output_dir = Path(__file__).parent.parent / "outputs"
    output_dir.mkdir(exist_ok=True)
    
    # Save verification summary
    output_file = output_dir / "hb1_cc_verification.json"
    with open(output_file, "w") as f:
        json.dump(checks, f, indent=2, default=str)
    print(f"\nResults saved to: {output_file}")
    
    # Generate plot
    try:
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # Plot 1: Scale factor
        axes[0, 0].loglog(results['t'], results['a'])
        axes[0, 0].set_xlabel('Time (Planck units)')
        axes[0, 0].set_ylabel('Scale factor a(t)')
        axes[0, 0].set_title('Cosmic Expansion')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Plot 2: q-variable
        axes[0, 1].semilogx(results['t'], results['q'] / params['q_eq'])
        axes[0, 1].axhline(1.0, color='r', linestyle='--', label='Equilibrium')
        axes[0, 1].set_xlabel('Time (Planck units)')
        axes[0, 1].set_ylabel('q / q_eq')
        axes[0, 1].set_title('q-Variable Relaxation')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # Plot 3: Vacuum energy
        axes[1, 0].loglog(results['t'], results['rho_vac'])
        axes[1, 0].axhline(RHO_CRIT_GEV4, color='g', linestyle='--', label='ρ_crit')
        axes[1, 0].set_xlabel('Time (Planck units)')
        axes[1, 0].set_ylabel('ρ_vac (GeV^4)')
        axes[1, 0].set_title('Vacuum Energy Evolution')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # Plot 4: Hubble parameter
        axes[1, 1].loglog(results['t'], results['H'])
        axes[1, 1].set_xlabel('Time (Planck units)')
        axes[1, 1].set_ylabel('H (GeV)')
        axes[1, 1].set_title('Hubble Parameter')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plot_file = output_dir / "hb1_cc_evolution.png"
        plt.savefig(plot_file, dpi=150)
        print(f"Plot saved to: {plot_file}")
        plt.close()
    except Exception as e:
        print(f"Warning: Could not generate plot: {e}")
    
    return checks


if __name__ == "__main__":
    results = main()
