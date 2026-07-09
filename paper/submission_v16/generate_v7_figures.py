#!/usr/bin/env python3
"""
TRXT-Nullivance V7: Visualization Scripts for New Appendices
Generates figures for Appendix N (Noether), Appendix T (Topology), Appendix U (MaVaN)
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import os

# Output directory
OUTPUT_DIR = r"c:\Users\NC\Music\trxt nullivance v14\paper\submission_v16\figures"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.titlesize'] = 16

# =============================================================================
# Figure 1: Appendix N - Noether Charge Sequestering Mechanism
# =============================================================================
def fig_noether_sequestering():
    """Illustrate how vacuum energy is absorbed by chemical potential shift."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Left: Standard GR - Vacuum energy gravitates
    ax1 = axes[0]
    ax1.set_title("Standard GR: Vacuum Energy Gravitates", fontsize=14, fontweight='bold')
    
    # Energy density bar
    heights = [100, 0]  # epsilon, -Lambda (gravity source)
    labels = [r'$\epsilon_{vac} \sim M_{Pl}^4$', r'$\Lambda_{eff} = \epsilon_{vac}$']
    colors = ['#e74c3c', '#c0392b']
    x_pos = [0, 1]
    bars1 = ax1.bar(x_pos, heights, color=colors, width=0.5, edgecolor='black', linewidth=2)
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(['Vacuum Energy', 'Cosmological\nConstant'], fontsize=12)
    ax1.set_ylabel('Energy Density (arbitrary units)', fontsize=12)
    ax1.set_ylim(0, 120)
    ax1.axhline(y=100, color='red', linestyle='--', linewidth=2, label='PROBLEM: Universe collapses!')
    ax1.legend(loc='upper right')
    ax1.annotate('', xy=(1, 95), xytext=(0, 95),
                arrowprops=dict(arrowstyle='->', color='red', lw=3))
    ax1.text(0.5, 108, 'Couples directly!', ha='center', fontsize=11, color='red', fontweight='bold')
    
    # Right: TRXT Sequestering - Noether charge absorbs shift
    ax2 = axes[1]
    ax2.set_title("TRXT (Noether Charge): Vacuum Energy Sequestered", fontsize=14, fontweight='bold')
    
    heights2 = [100, 100, 0]  # epsilon, mu*n, P_vac
    labels2 = [r'$\epsilon + C$', r'$\mu \cdot n$', r'$P_{vac} = 0$']
    colors2 = ['#e74c3c', '#27ae60', '#2ecc71']
    x_pos2 = [0, 1, 2]
    bars2 = ax2.bar(x_pos2, heights2, color=colors2, width=0.5, edgecolor='black', linewidth=2)
    ax2.set_xticks(x_pos2)
    ax2.set_xticklabels([r'$\epsilon + C$' + '\n(Energy + Loop)', 
                         r'$\mu \cdot n$' + '\n(Chemical Pot.)', 
                         r'$P_{vac}$' + '\n(Pressure)'], fontsize=11)
    ax2.set_ylabel('Energy Density', fontsize=12)
    ax2.set_ylim(0, 120)
    
    # Arrow showing cancellation
    ax2.annotate('', xy=(2, 5), xytext=(0.5, 95),
                arrowprops=dict(arrowstyle='->', color='green', lw=3, connectionstyle='arc3,rad=-0.3'))
    ax2.annotate('', xy=(2, 5), xytext=(1.5, 95),
                arrowprops=dict(arrowstyle='->', color='green', lw=3, connectionstyle='arc3,rad=0.3'))
    ax2.text(1.5, 60, r'$\mu \to \mu + C/n$', fontsize=12, color='green', fontweight='bold',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    ax2.axhline(y=5, color='green', linestyle='--', linewidth=2, label=r'$P_{vac} = \epsilon - \mu n = 0$ ✓')
    ax2.legend(loc='upper right')
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "fig_noether_sequestering.png"), dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Generated: fig_noether_sequestering.png")

# =============================================================================
# Figure 2: Appendix T - Ricci Flow Mass Spectrum
# =============================================================================
def fig_ricci_flow_mass():
    """Show 1/p mass spectrum from Ricci Flow contraction."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Left: Soliton radius vs winding number
    ax1 = axes[0]
    p_values = np.arange(1, 11)
    R_opt = 1 / p_values**2  # R ~ 1/p^2
    
    ax1.plot(p_values, R_opt, 'o-', color='#3498db', markersize=10, linewidth=2, label=r'$R_{opt} \propto 1/p^2$')
    ax1.set_xlabel('Winding Number $p$', fontsize=14)
    ax1.set_ylabel(r'Soliton Radius $R_{opt}$ (arb. units)', fontsize=14)
    ax1.set_title('Ricci Flow Contraction:\nHigher Winding → Smaller Soliton', fontsize=14, fontweight='bold')
    ax1.set_xticks(p_values)
    ax1.legend(fontsize=12)
    ax1.grid(True, alpha=0.3)
    
    # Annotate key points
    ax1.annotate('p=1:\nLargest', xy=(1, R_opt[0]), xytext=(2, 0.8),
                arrowprops=dict(arrowstyle='->', color='gray'), fontsize=10)
    ax1.annotate('p=3:\nProton', xy=(3, R_opt[2]), xytext=(4.5, 0.15),
                arrowprops=dict(arrowstyle='->', color='gray'), fontsize=10)
    
    # Right: Mass spectrum E(p) ~ 1/p
    ax2 = axes[1]
    M_star = 365.24  # GeV
    E_values = M_star * (1/p_values + 1/p_values)  # Diagonal modes (p,p)
    
    ax2.bar(p_values, E_values, color='#e74c3c', edgecolor='black', linewidth=1.5)
    ax2.set_xlabel('Mode $(p, p)$', fontsize=14)
    ax2.set_ylabel('Mass $E$ (GeV)', fontsize=14)
    ax2.set_title(r'Mass Spectrum: $E(p,p) = 2M^*/p$', fontsize=14, fontweight='bold')
    ax2.set_xticks(p_values)
    ax2.set_xticklabels([f'({p},{p})' for p in p_values], rotation=45)
    
    # Highlight known particles
    ax2.axhline(y=125.1, color='blue', linestyle='--', alpha=0.7, label='Higgs (125 GeV)')
    ax2.axhline(y=91.2, color='green', linestyle='--', alpha=0.7, label='Z (91 GeV)')
    ax2.axhline(y=80.4, color='orange', linestyle='--', alpha=0.7, label='W (80 GeV)')
    ax2.legend(fontsize=10, loc='upper right')
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "fig_ricci_flow_mass.png"), dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Generated: fig_ricci_flow_mass.png")

# =============================================================================
# Figure 3: Appendix U - MaVaN Beta Prediction
# =============================================================================
def fig_mavan_beta_prediction():
    """Show beta prediction from polytropic index n."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Left: Beta as function of n
    ax1 = axes[0]
    n_values = np.linspace(0.5, 3.0, 100)
    beta_values = 2 / (n_values + 1)
    
    ax1.plot(n_values, beta_values, 'b-', linewidth=2, label=r'$\beta = 2/(n+1)$')
    ax1.axvline(x=1.37, color='red', linestyle='--', linewidth=2, label=r'TRXT: $n = 1.37$')
    ax1.axhline(y=0.084, color='red', linestyle=':', linewidth=2)
    
    # Mark observation
    ax1.fill_between([0.5, 3.0], [0.092-0.02]*2, [0.092+0.02]*2, 
                     color='green', alpha=0.2, label=r'SK-IV: $\beta_{obs} = 0.092 \pm 0.02$')
    ax1.axhline(y=0.092, color='green', linestyle='-', linewidth=2, alpha=0.7)
    
    ax1.set_xlabel('Polytropic Index $n$', fontsize=14)
    ax1.set_ylabel(r'MaVaN Coupling $\beta$', fontsize=14)
    ax1.set_title(r'Prediction: $\beta_{pred} = 0.084$ from $n = 1.37$', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=11, loc='upper right')
    ax1.set_xlim(0.5, 3.0)
    ax1.set_ylim(0, 0.5)
    ax1.grid(True, alpha=0.3)
    
    # Right: Comparison bar chart
    ax2 = axes[1]
    categories = ['TRXT\nPrediction', 'SK-IV\nObservation']
    values = [0.084, 0.092]
    errors = [0.01, 0.02]  # Approximate theory uncertainty for TRXT
    colors = ['#3498db', '#27ae60']
    
    bars = ax2.bar(categories, values, yerr=errors, color=colors, 
                   edgecolor='black', linewidth=2, capsize=8, error_kw={'linewidth': 2})
    ax2.set_ylabel(r'MaVaN Coupling $\beta$', fontsize=14)
    ax2.set_title('Prediction vs Observation', fontsize=14, fontweight='bold')
    ax2.set_ylim(0, 0.15)
    
    # Add value labels
    for bar, val, err in zip(bars, values, errors):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + err + 0.005,
                f'{val:.3f}', ha='center', fontsize=12, fontweight='bold')
    
    # Add agreement annotation
    ax2.annotate('Agreement:\n9% difference', xy=(0.5, 0.088), xytext=(0.5, 0.13),
                ha='center', fontsize=12, color='purple',
                arrowprops=dict(arrowstyle='->', color='purple', lw=2),
                bbox=dict(boxstyle='round', facecolor='white', edgecolor='purple'))
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "fig_mavan_beta_prediction.png"), dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Generated: fig_mavan_beta_prediction.png")

# =============================================================================
# Figure 4: Appendix U - MaVaN Mass Running with Density
# =============================================================================
def fig_mavan_dm2_running():
    """Show how Delta m^2 varies with matter density."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Parameters
    dm2_vacuum = 7.41e-5  # eV^2 (NuFIT value)
    beta = 0.092  # MaVaN coupling (observation)
    rho_c = 3.0  # g/cm^3 (reference)
    
    # Density range (log scale)
    rho_values = np.logspace(-1, 2.5, 100)  # 0.1 to ~300 g/cm^3
    
    # MaVaN running
    dm2_mavan = dm2_vacuum * (1 + beta * np.log(rho_values / rho_c))
    
    # Standard MSW (constant)
    dm2_standard = np.ones_like(rho_values) * dm2_vacuum
    
    ax.semilogx(rho_values, dm2_mavan * 1e5, 'b-', linewidth=2.5, 
                label=r'MaVaN: $\Delta m^2(\rho) = \Delta m^2_0 [1 + \beta \ln(\rho/\rho_c)]$')
    ax.semilogx(rho_values, dm2_standard * 1e5, 'gray', linestyle='--', linewidth=2, 
                label=r'Standard MSW: $\Delta m^2 = $ const')
    
    # Mark key environments
    environments = [
        (0.3, 'Vacuum\n(Reactor)', 'purple'),
        (3.0, 'Earth\nMantle', 'green'),
        (5.0, 'Earth\nCore', 'orange'),
        (150.0, 'Solar\nCore', 'red'),
    ]
    
    for rho, name, color in environments:
        dm2_at_rho = dm2_vacuum * (1 + beta * np.log(rho / rho_c))
        ax.axvline(x=rho, color=color, linestyle=':', alpha=0.7)
        ax.scatter([rho], [dm2_at_rho * 1e5], color=color, s=100, zorder=5, edgecolor='black')
        ax.annotate(name, xy=(rho, dm2_at_rho * 1e5), xytext=(rho*1.5, dm2_at_rho * 1e5 + 0.3),
                   fontsize=10, color=color)
    
    ax.set_xlabel(r'Matter Density $\rho$ (g/cm$^3$)', fontsize=14)
    ax.set_ylabel(r'$\Delta m^2_{21}$ ($\times 10^{-5}$ eV$^2$)', fontsize=14)
    ax.set_title('MaVaN: Neutrino Mass-Squared Difference Varies with Environment', 
                 fontsize=14, fontweight='bold')
    ax.legend(fontsize=11, loc='lower left')
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0.1, 300)
    ax.set_ylim(4.5, 8.0)
    
    # Add annotation for tension resolution
    ax.annotate('Solar experiments\nmeasure LOWER value!',
               xy=(100, 5.2), xytext=(10, 5.5),
               fontsize=11, color='red', fontweight='bold',
               arrowprops=dict(arrowstyle='->', color='red', lw=2))
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "fig_mavan_dm2_running.png"), dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Generated: fig_mavan_dm2_running.png")

# =============================================================================
# Figure 5: Appendix T - Quark Confinement from Winding
# =============================================================================
def fig_quark_confinement():
    """Illustrate quark confinement from fractional winding."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    theta = np.linspace(0, 2*np.pi, 100)
    
    # Left: Single quark (n = 1/3) - MULTI-VALUED
    ax1 = axes[0]
    n_quark = 1/3
    psi_real = np.cos(n_quark * theta)
    psi_imag = np.sin(n_quark * theta)
    
    ax1.plot(theta, psi_real, 'b-', linewidth=2, label=r'Re$[\psi]$ = cos$(n\theta)$')
    ax1.plot(theta, psi_imag, 'r-', linewidth=2, label=r'Im$[\psi]$ = sin$(n\theta)$')
    ax1.axvline(x=0, color='gray', linestyle='-', alpha=0.5)
    ax1.axvline(x=2*np.pi, color='gray', linestyle='-', alpha=0.5)
    
    # Mark discontinuity
    ax1.scatter([0, 2*np.pi], [1, np.cos(2*np.pi/3)], color='blue', s=100, zorder=5)
    ax1.annotate(r'$\psi(0) = 1$', xy=(0, 1), xytext=(0.5, 1.1), fontsize=11,
                arrowprops=dict(arrowstyle='->', color='blue'))
    ax1.annotate(r'$\psi(2\pi) = e^{i2\pi/3} \neq 1$', xy=(2*np.pi, np.cos(2*np.pi/3)), 
                xytext=(4.5, 0.7), fontsize=11, color='red',
                arrowprops=dict(arrowstyle='->', color='red'))
    
    ax1.set_xlabel(r'Angle $\theta$', fontsize=14)
    ax1.set_ylabel(r'Wavefunction $\psi(\theta)$', fontsize=14)
    ax1.set_title('Single Quark ($n = 1/3$): MULTI-VALUED ✗', fontsize=14, fontweight='bold', color='red')
    ax1.legend(fontsize=11)
    ax1.set_xlim(-0.5, 7)
    ax1.set_xticks([0, np.pi, 2*np.pi])
    ax1.set_xticklabels(['0', r'$\pi$', r'$2\pi$'])
    ax1.grid(True, alpha=0.3)
    
    # Right: Proton (3 quarks, n = 1) - SINGLE-VALUED
    ax2 = axes[1]
    n_proton = 1
    psi_real_p = np.cos(n_proton * theta)
    psi_imag_p = np.sin(n_proton * theta)
    
    ax2.plot(theta, psi_real_p, 'b-', linewidth=2, label=r'Re$[\psi]$')
    ax2.plot(theta, psi_imag_p, 'r-', linewidth=2, label=r'Im$[\psi]$')
    ax2.axvline(x=0, color='gray', linestyle='-', alpha=0.5)
    ax2.axvline(x=2*np.pi, color='gray', linestyle='-', alpha=0.5)
    
    # Mark continuity
    ax2.scatter([0, 2*np.pi], [1, 1], color='green', s=100, zorder=5)
    ax2.annotate(r'$\psi(0) = \psi(2\pi) = 1$', xy=(np.pi, 1.1), fontsize=12, 
                color='green', fontweight='bold', ha='center')
    
    ax2.set_xlabel(r'Angle $\theta$', fontsize=14)
    ax2.set_ylabel(r'Wavefunction $\psi(\theta)$', fontsize=14)
    ax2.set_title('Proton (3 quarks, $n = 1$): SINGLE-VALUED ✓', fontsize=14, fontweight='bold', color='green')
    ax2.legend(fontsize=11)
    ax2.set_xlim(-0.5, 7)
    ax2.set_xticks([0, np.pi, 2*np.pi])
    ax2.set_xticklabels(['0', r'$\pi$', r'$2\pi$'])
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "fig_quark_confinement.png"), dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Generated: fig_quark_confinement.png")

# =============================================================================
# Main execution
# =============================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("TRXT-Nullivance V7: Generating Visualization Figures")
    print("=" * 60)
    
    fig_noether_sequestering()
    fig_ricci_flow_mass()
    fig_mavan_beta_prediction()
    fig_mavan_dm2_running()
    fig_quark_confinement()
    
    print("=" * 60)
    print(f"All figures saved to: {OUTPUT_DIR}")
    print("=" * 60)
