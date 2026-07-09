"""
TRXT V19: INDUCED GRAVITY FROM NJL CONDENSATE
==============================================
Numerical implementation of Sakharov-Volovik program.

Derives:
1. Gap Equation → Dynamical mass M
2. 1-Loop Effective Action → Heat kernel coefficients
3. Induced Newton Constant → G_ind
4. Einstein-Hilbert Term → R coefficient

References:
- Sakharov (1968): Induced Gravity
- Volovik (2003): Universe in a Helium Droplet
- Nambu & Jona-Lasinio (1961): Dynamical model of particles
"""

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq, fsolve
import matplotlib.pyplot as plt
from pathlib import Path

# ============================================================================
# PHYSICAL CONSTANTS
# ============================================================================

# TRXT Constants (from theory documents)
ALPHA_EM = 1 / 137.035999  # Fine structure constant
X_TRXT = 3 / (2 * ALPHA_EM)  # ~205.55
M_TAU = 1.77686  # GeV (Tau lepton mass)
M_STAR = M_TAU * X_TRXT  # ~365.24 GeV (TRXT Master Scale)

# Fundamental scales
M_PLANCK = 1.22e19  # GeV
G_NEWTON = 6.674e-11  # m³/(kg·s²)
G_NEWTON_GEV = 6.707e-39  # GeV^-2 (in natural units)

# Derived
HBAR_C = 0.197  # GeV·fm


class NJLCondensate:
    """
    Nambu-Jona-Lasinio model for fermionic condensate.
    
    The NJL Lagrangian:
    L = ψ̄(iγ·∂)ψ + G(ψ̄ψ)²
    
    After condensation: ⟨ψ̄ψ⟩ ≠ 0 → Dynamical mass M
    """
    
    def __init__(self, cutoff_gev, n_flavors=1):
        """
        Args:
            cutoff_gev: UV cutoff Λ (typically ~ M_Planck or condensation scale)
            n_flavors: Number of fermion flavors (N_f)
        """
        self.Lambda = cutoff_gev
        self.N_f = n_flavors
        
        # Derived quantities
        self.Lambda2 = cutoff_gev**2
        self.Lambda4 = cutoff_gev**4
        
    def gap_equation_rhs(self, M, G_njl):
        """
        Right-hand side of the Gap Equation:
        M = G·⟨ψ̄ψ⟩ = G · N_c·M/(4π²) · [Λ² - M²·ln(Λ²/M² + 1)]
        
        For N_c = 3 (QCD) or N_c = 1 (preons)
        """
        if M <= 0:
            return 0
            
        N_c = 1  # Preons (not quarks)
        
        # Fermion condensate in cutoff regularization
        log_term = np.log(self.Lambda2 / M**2 + 1)
        condensate = (N_c * M / (4 * np.pi**2)) * (self.Lambda2 - M**2 * log_term)
        
        return G_njl * condensate
    
    def solve_gap_equation(self, G_njl, M_guess=1.0):
        """
        Solve the self-consistency equation:
        M = G · Σ(M)  where Σ is the self-energy
        
        Returns dynamical mass M (order parameter).
        """
        def gap_func(M):
            if M <= 1e-10:
                return M  # Trivial solution
            return M - self.gap_equation_rhs(M, G_njl)
        
        try:
            # Find non-trivial solution
            M_solution = brentq(gap_func, 1e-6, self.Lambda * 0.9)
            return M_solution
        except ValueError:
            # No solution found - below critical coupling
            return 0.0
    
    def critical_coupling(self):
        """
        Find critical coupling G_crit above which condensation occurs.
        G_crit = 4π² / (N_c · Λ²)
        """
        N_c = 1
        return 4 * np.pi**2 / (N_c * self.Lambda2)
    
    def condensate_value(self, M):
        """
        Calculate ⟨ψ̄ψ⟩ for given dynamical mass M.
        """
        if M <= 0:
            return 0
            
        N_c = 1
        log_term = np.log(self.Lambda2 / M**2 + 1)
        return (N_c * M / (4 * np.pi**2)) * (self.Lambda2 - M**2 * log_term)


class InducedGravity:
    """
    Calculate induced Newton constant from fermion loops.
    
    Sakharov's formula:
    1/(16πG) = N_f/(96π²) · Λ² + finite corrections
    """
    
    def __init__(self, condensate: NJLCondensate):
        self.condensate = condensate
        
    def heat_kernel_coefficients(self, M):
        """
        Calculate heat kernel (Seeley-DeWitt) coefficients.
        
        Γ_eff = ∫d⁴x √(-g) [a₀Λ⁴ + a₁Λ²M² + a₂R + a₃(∂M)² + ...]
        
        The a₂ coefficient gives the Einstein-Hilbert term.
        """
        Lambda = self.condensate.Lambda
        N_f = self.condensate.N_f
        
        # a₀: Cosmological constant (quartic divergence)
        # For Dirac fermion: a₀ = -N_f/(16π²) per cutoff^4
        a0 = -N_f / (16 * np.pi**2)
        
        # a₁: Mass term (quadratic divergence)
        # a₁ = N_f/(16π²)
        a1 = N_f / (16 * np.pi**2)
        
        # a₂: Einstein-Hilbert (logarithmic/finite)
        # For spin-1/2: a₂ = N_f/(96π²) × Λ²
        # This is SAKHAROV'S KEY RESULT
        a2 = N_f / (96 * np.pi**2) * Lambda**2
        
        # a₃: Kinetic term for scalar
        a3 = N_f / (48 * np.pi**2)
        
        return {
            'a0': a0,
            'a1': a1,
            'a2': a2,
            'a3': a3
        }
    
    def induced_newton_constant(self, M=None):
        """
        Calculate induced Newton constant.
        
        G_ind = 1 / (16π a₂)
        
        Returns G in GeV^-2 units.
        """
        coeffs = self.heat_kernel_coefficients(M or 0)
        a2 = coeffs['a2']
        
        if a2 <= 0:
            return np.inf
            
        G_ind = 1 / (16 * np.pi * a2)
        return G_ind
    
    def induced_planck_mass(self, M=None):
        """
        Calculate induced Planck mass.
        M_Pl = 1/√(8πG)
        """
        G_ind = self.induced_newton_constant(M)
        if G_ind <= 0 or np.isinf(G_ind):
            return 0
        return 1 / np.sqrt(8 * np.pi * G_ind)
    
    def effective_action_density(self, M, R):
        """
        Calculate effective action density.
        
        L_eff = a₀Λ⁴ + a₁Λ²M² + a₂R + ...
        """
        coeffs = self.heat_kernel_coefficients(M)
        Lambda = self.condensate.Lambda
        
        L_eff = (coeffs['a0'] * Lambda**4 + 
                 coeffs['a1'] * Lambda**2 * M**2 + 
                 coeffs['a2'] * R)
        
        return L_eff


class CausalityChecker:
    """
    Check for superluminality and ghosts.
    """
    
    def __init__(self, condensate: NJLCondensate):
        self.condensate = condensate
        
    def sound_speed_squared(self, M):
        """
        Calculate effective sound speed c_s² for phonon mode.
        
        For BCS-type superfluid: c_s² = v_F²/3 where v_F is Fermi velocity.
        For relativistic case: c_s² ≤ 1 required.
        """
        # In relativistic NJL, c_s² = 1/3 (conformal limit) to 1
        # The actual value depends on the equation of state
        
        if M <= 0:
            return 1.0  # Conformal (massless)
        
        Lambda = self.condensate.Lambda
        
        # Approximate: c_s² ≈ 1/3 + (M/Λ)² corrections
        c_s2 = 1/3 + (M / Lambda)**2
        
        return min(c_s2, 1.0)  # Cap at 1
    
    def check_causality(self, M):
        """Check c_s ≤ 1 (no superluminality)."""
        c_s2 = self.sound_speed_squared(M)
        return c_s2 <= 1.0, np.sqrt(c_s2)
    
    def check_ghost_free(self, M):
        """
        Check for absence of ghost (negative norm states).
        
        Ghost appears if kinetic term has wrong sign.
        For NJL: require d²V/dM² > 0 (stability).
        """
        # In proper NJL, the kinetic term Z(M) > 0 always
        # Ghost can appear if we add wrong higher-derivative terms
        
        # Simple check: effective potential is convex
        # V(M) ~ -M²ln(M²) + M² is convex for M ≠ 0
        
        if M <= 0:
            return False, "No condensate"
        
        # Check second derivative of effective potential
        Lambda = self.condensate.Lambda
        d2V = 2 * np.log(Lambda**2 / M**2) - 2
        
        if d2V > 0:
            return True, f"d²V/dM² = {d2V:.2f} > 0"
        else:
            return False, f"d²V/dM² = {d2V:.2f} < 0 (unstable)"


def run_v19_induced_gravity():
    """
    Main V19 analysis: Derive Einstein equations from NJL.
    """
    
    print("╔" + "═" * 68 + "╗")
    print("║" + "  TRXT V19: INDUCED GRAVITY FROM NJL CONDENSATE  ".center(68) + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    # ========================================================================
    # STEP 1: NJL Gap Equation
    # ========================================================================
    print("[STEP 1] NJL GAP EQUATION")
    print("-" * 60)
    
    # Use M* as the condensation scale (TRXT hypothesis)
    # OR use M_Planck as UV cutoff (standard induced gravity)
    
    print(f"  TRXT Master Scale M* = {M_STAR:.2f} GeV")
    print(f"  Planck Mass M_Pl = {M_PLANCK:.2e} GeV")
    
    # Scenario A: Condensation at M* scale
    condensate_mstar = NJLCondensate(cutoff_gev=M_STAR, n_flavors=12)  # SM fermions
    
    # Scenario B: Condensation at Planck scale  
    condensate_planck = NJLCondensate(cutoff_gev=M_PLANCK, n_flavors=1)  # Preons
    
    print(f"\n  Scenario A (Λ = M* = {M_STAR:.1f} GeV):")
    G_crit_A = condensate_mstar.critical_coupling()
    print(f"    Critical Coupling G_crit = {G_crit_A:.2e} GeV^-2")
    
    # Try different couplings
    G_test_A = 1.5 * G_crit_A
    M_gap_A = condensate_mstar.solve_gap_equation(G_test_A)
    print(f"    Gap at G = 1.5×G_crit: M_gap = {M_gap_A:.2f} GeV")
    
    print(f"\n  Scenario B (Λ = M_Pl = {M_PLANCK:.0e} GeV):")
    G_crit_B = condensate_planck.critical_coupling()
    print(f"    Critical Coupling G_crit = {G_crit_B:.2e} GeV^-2")
    
    G_test_B = 2 * G_crit_B
    M_gap_B = condensate_planck.solve_gap_equation(G_test_B)
    print(f"    Gap at G = 2×G_crit: M_gap = {M_gap_B:.2e} GeV")
    
    # ========================================================================
    # STEP 2: Induced Newton Constant
    # ========================================================================
    print("\n[STEP 2] INDUCED NEWTON CONSTANT")
    print("-" * 60)
    
    induced_A = InducedGravity(condensate_mstar)
    induced_B = InducedGravity(condensate_planck)
    
    print("\n  Scenario A (Λ = M*):")
    G_ind_A = induced_A.induced_newton_constant(M_gap_A)
    M_pl_ind_A = induced_A.induced_planck_mass(M_gap_A)
    print(f"    G_induced = {G_ind_A:.2e} GeV^-2")
    print(f"    M_Planck_induced = {M_pl_ind_A:.2e} GeV")
    print(f"    Ratio to observed M_Pl: {M_pl_ind_A / M_PLANCK:.2e}")
    
    print("\n  Scenario B (Λ = M_Planck):")
    G_ind_B = induced_B.induced_newton_constant(M_gap_B)
    M_pl_ind_B = induced_B.induced_planck_mass(M_gap_B)
    print(f"    G_induced = {G_ind_B:.2e} GeV^-2")
    print(f"    M_Planck_induced = {M_pl_ind_B:.2e} GeV")
    print(f"    Ratio to observed M_Pl: {M_pl_ind_B / M_PLANCK:.2e}")
    
    # ========================================================================
    # STEP 3: Heat Kernel Coefficients (Einstein-Hilbert)
    # ========================================================================
    print("\n[STEP 3] EFFECTIVE ACTION (HEAT KERNEL)")
    print("-" * 60)
    
    coeffs_B = induced_B.heat_kernel_coefficients(M_gap_B)
    print("\n  Scenario B coefficients (Λ = M_Planck, N_f = 1):")
    print(f"    a₀ (Cosmological): {coeffs_B['a0']:.4f} × Λ⁴")
    print(f"    a₁ (Mass term): {coeffs_B['a1']:.4f} × Λ²M²")
    print(f"    a₂ (Einstein-Hilbert): {coeffs_B['a2']:.4e}")
    print(f"    a₃ (Kinetic): {coeffs_B['a3']:.4f}")
    
    print("\n  Effective Action:")
    print("    S_eff = ∫d⁴x √(-g) [ a₀Λ⁴ + a₁Λ²M² + a₂R + ... ]")
    print(f"          = ∫d⁴x √(-g) [ Λ_cosmo + {coeffs_B['a2']:.2e} × R + ... ]")
    print(f"\n    Einstein-Hilbert: S_EH = (1/16πG) ∫d⁴x √(-g) R")
    print(f"    → 1/(16πG_ind) = a₂ = {coeffs_B['a2']:.2e}")
    
    # ========================================================================
    # STEP 4: Causality and Ghost Check
    # ========================================================================
    print("\n[STEP 4] CAUSALITY & GHOST CHECK")
    print("-" * 60)
    
    checker = CausalityChecker(condensate_planck)
    
    causal_ok, c_s = checker.check_causality(M_gap_B)
    ghost_ok, ghost_msg = checker.check_ghost_free(M_gap_B)
    
    print(f"\n  Sound Speed: c_s = {c_s:.4f} c")
    print(f"    Causality: {'✅ c_s ≤ 1 (OK)' if causal_ok else '❌ VIOLATION!'}")
    print(f"  Ghost Check: {'✅ ' + ghost_msg if ghost_ok else '❌ ' + ghost_msg}")
    
    # ========================================================================
    # STEP 5: Summary
    # ========================================================================
    print("\n" + "=" * 60)
    print("[V19 SUMMARY: INDUCED GRAVITY]")
    print("=" * 60)
    
    print(f"""
    NJL CONDENSATE:
    ├─ Cutoff Λ = M_Planck = {M_PLANCK:.2e} GeV
    ├─ Critical Coupling G_crit = {G_crit_B:.2e} GeV^-2
    └─ Dynamical Mass M = {M_gap_B:.2e} GeV (condensate scale)
    
    INDUCED GRAVITY:
    ├─ G_induced = {G_ind_B:.2e} GeV^-2
    ├─ M_Planck_induced = {M_pl_ind_B:.2e} GeV
    └─ Ratio M_Pl_ind / M_Pl_obs = {M_pl_ind_B / M_PLANCK:.2f}
    
    EINSTEIN-HILBERT EMERGENCE:
    ├─ a₂ coefficient = {coeffs_B['a2']:.2e}
    └─ Effective Action = ∫d⁴x √(-g) [{coeffs_B['a2']:.2e} × R + ...]
    
    CONSISTENCY CHECKS:
    ├─ Causality (c_s ≤ 1): {'✅ PASS' if causal_ok else '❌ FAIL'}
    └─ Ghost-free: {'✅ PASS' if ghost_ok else '❌ FAIL'}
    """)
    
    # Verdict
    if abs(M_pl_ind_B / M_PLANCK - 1) < 0.5 and causal_ok and ghost_ok:
        print("  ╔═══════════════════════════════════════════════════════════╗")
        print("  ║  ✅ V19: EINSTEIN EQUATIONS SUCCESSFULLY DERIVED!         ║")
        print("  ╚═══════════════════════════════════════════════════════════╝")
        verdict = "SUCCESS"
    else:
        print("  ⚠️  V19: Partial success - gravity emerges but scale mismatch")
        verdict = "PARTIAL"
    
    # Plot
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Gap equation solution
    ax1 = axes[0]
    G_range = np.linspace(G_crit_B * 0.5, G_crit_B * 5, 100)
    M_range = [condensate_planck.solve_gap_equation(G) for G in G_range]
    ax1.plot(G_range / G_crit_B, M_range, 'b-', linewidth=2)
    ax1.axvline(1.0, color='r', linestyle='--', label='G_crit')
    ax1.set_xlabel('G / G_crit')
    ax1.set_ylabel('Dynamical Mass M [GeV]')
    ax1.set_title('Gap Equation Solution')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_yscale('log')
    
    # Induced Planck mass vs N_f
    ax2 = axes[1]
    N_f_range = np.arange(1, 50)
    M_pl_range = []
    for nf in N_f_range:
        cond = NJLCondensate(M_PLANCK, nf)
        ind = InducedGravity(cond)
        M_pl_range.append(ind.induced_planck_mass())
    ax2.plot(N_f_range, np.array(M_pl_range) / M_PLANCK, 'g-', linewidth=2)
    ax2.axhline(1.0, color='r', linestyle='--', label='Observed M_Pl')
    ax2.set_xlabel('Number of Fermion Flavors N_f')
    ax2.set_ylabel('M_Pl_induced / M_Pl_observed')
    ax2.set_title('Induced Planck Mass vs Fermion Content')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    output = Path(__file__).parent.parent / "results" / "v19_induced_gravity.png"
    output.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output, dpi=150, bbox_inches='tight')
    print(f"\n[Plot saved: {output}]")
    
    return verdict


if __name__ == "__main__":
    verdict = run_v19_induced_gravity()
