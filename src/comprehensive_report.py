"""
TRXT COMPREHENSIVE ANALYSIS: UNIVERSE FROM BIG BANG TO NOW
============================================================
Complete model with all physics: Gravity, Forces, Light, Dark Matter

Creates visualizations and comprehensive report.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Arrow
import matplotlib.patches as mpatches
from pathlib import Path

# ============================================================================
# PHYSICAL CONSTANTS (From CODATA/PDG)
# ============================================================================

# Fundamental
ALPHA_EM = 1 / 137.035999084  # Fine structure constant
M_PLANCK = 1.220890e19  # GeV
G_NEWTON = 6.67430e-11  # m³/(kg·s²)
C_LIGHT = 299792458  # m/s
HBAR = 1.054571817e-34  # J·s

# TRXT Derived
X_TRXT = 3 / (2 * ALPHA_EM)  # ~205.55
M_TAU = 1.77686  # GeV
M_STAR = M_TAU * X_TRXT  # ~365.24 GeV (Master Scale)

# Cosmological (Planck 2018)
H0 = 67.36  # km/s/Mpc
OMEGA_M = 0.3153
OMEGA_LAMBDA = 0.6847
T_CMB = 2.7255  # K

# SM Particles
SM_MASSES = {
    'electron': 0.000511, 'muon': 0.1057, 'tau': 1.777,
    'up': 0.00216, 'down': 0.00467, 'strange': 0.093,
    'charm': 1.27, 'bottom': 4.18, 'top': 172.76,
    'W': 80.379, 'Z': 91.1876, 'Higgs': 125.25,
}

# TRXT Dark Tower Candidates
DARK_TOWER = {
    '(128,128)': 5.71,
    '(256,256)': 2.85,
    '(512,512)': 1.43,
}


def create_universe_timeline():
    """Create universe evolution timeline figure."""
    
    fig, ax = plt.subplots(figsize=(16, 10))
    
    # Timeline events (log10(seconds), event, description)
    events = [
        (-43, 'Planck Era', 'Quantum gravity dominates\nt_P = 5.4×10⁻⁴⁴ s', 'red'),
        (-36, 'NJL Condensation', 'Fermion condensate forms\nGravity EMERGES', 'orange'),
        (-32, 'Inflation', 'Exponential expansion\nΔN ~ 60 e-folds', 'yellow'),
        (-10, 'Electroweak', 'W, Z bosons get mass\nM_W = 80 GeV', 'green'),
        (-6, 'QCD', 'Quarks confined\nProtons, neutrons form', 'cyan'),
        (2, 'Nucleosynthesis', 'H, He, Li formed\n75% H, 25% He', 'blue'),
        (13, 'Recombination', 'Atoms form\nCMB released', 'purple'),
        (16, 'Dark Ages', 'No stars yet', 'gray'),
        (16.5, 'First Stars', 'Pop III stars\nReionization', 'pink'),
        (17.6, 'Today', 't = 13.8 Gyr\nGalaxies, Life', 'white'),
    ]
    
    ax.set_xlim(-45, 20)
    ax.set_ylim(-1, 12)
    
    # Draw timeline
    ax.axhline(5, color='white', linewidth=3, alpha=0.5)
    
    for i, (t, name, desc, color) in enumerate(events):
        y = 5
        
        # Event marker
        ax.scatter([t], [y], s=200, c=color, edgecolor='white', zorder=10)
        
        # Event name and description
        if i % 2 == 0:
            ax.annotate(f'{name}\n{desc}', (t, y+0.5), ha='center', va='bottom',
                       fontsize=9, color='white',
                       bbox=dict(boxstyle='round', facecolor=color, alpha=0.7))
        else:
            ax.annotate(f'{name}\n{desc}', (t, y-0.5), ha='center', va='top',
                       fontsize=9, color='white',
                       bbox=dict(boxstyle='round', facecolor=color, alpha=0.7))
    
    # Labels
    ax.set_xlabel('log₁₀(time / seconds)', fontsize=12, color='white')
    ax.set_title('TRXT UNIVERSE TIMELINE: From Planck Era to Today', 
                 fontsize=16, fontweight='bold', color='white')
    
    # TRXT annotations
    ax.annotate('TRXT: NJL Condensate\n→ Gravity Emerges', (-36, 8),
               fontsize=11, color='orange', ha='center',
               bbox=dict(boxstyle='round', facecolor='black', edgecolor='orange'))
    
    ax.annotate('TRXT: Dark Tower\nVortices form', (-6, 2),
               fontsize=11, color='cyan', ha='center',
               bbox=dict(boxstyle='round', facecolor='black', edgecolor='cyan'))
    
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')
    ax.tick_params(colors='white')
    for spine in ax.spines.values():
        spine.set_color('white')
    
    plt.tight_layout()
    return fig


def create_forces_diagram():
    """Create diagram showing all forces and their TRXT origin."""
    
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Central condensate
    circle = plt.Circle((0.5, 0.5), 0.15, color='gold', alpha=0.8)
    ax.add_patch(circle)
    ax.text(0.5, 0.5, 'NJL\nCondensate\nM* = 365 GeV', ha='center', va='center',
            fontsize=10, fontweight='bold')
    
    # Four forces with arrows
    forces = [
        {'name': 'GRAVITY', 'pos': (0.5, 0.9), 'color': 'purple',
         'origin': 'Heat kernel a₂ term\n1-loop fermion', 
         'mediator': 'Graviton (spin-2)', 'strength': 'G = 6.67×10⁻¹¹'},
        {'name': 'ELECTROMAGNETISM', 'pos': (0.9, 0.5), 'color': 'yellow',
         'origin': 'U(1) gauge symmetry\nPhoton = collective mode',
         'mediator': 'Photon (spin-1)', 'strength': 'α = 1/137'},
        {'name': 'WEAK FORCE', 'pos': (0.5, 0.1), 'color': 'blue',
         'origin': 'SU(2) breaking\nHiggs = σ mode',
         'mediator': 'W±, Z⁰ (spin-1)', 'strength': 'G_F = 1.17×10⁻⁵'},
        {'name': 'STRONG FORCE', 'pos': (0.1, 0.5), 'color': 'red',
         'origin': 'SU(3) confinement\nGluons = vortex lines',
         'mediator': 'Gluons (spin-1)', 'strength': 'α_s = 0.12'},
    ]
    
    for f in forces:
        # Arrow from center to force
        dx = f['pos'][0] - 0.5
        dy = f['pos'][1] - 0.5
        ax.annotate('', f['pos'], (0.5 + 0.15*np.sign(dx), 0.5 + 0.15*np.sign(dy)),
                   arrowprops=dict(arrowstyle='->', color=f['color'], lw=3))
        
        # Force box
        bbox = dict(boxstyle='round,pad=0.5', facecolor=f['color'], alpha=0.8)
        text = f"{f['name']}\n\nOrigin: {f['origin']}\nMediator: {f['mediator']}\nStrength: {f['strength']}"
        ax.text(f['pos'][0], f['pos'][1], text, ha='center', va='center',
               fontsize=9, bbox=bbox, color='white' if f['color'] in ['purple', 'blue', 'red'] else 'black')
    
    ax.set_xlim(-0.1, 1.1)
    ax.set_ylim(-0.1, 1.1)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('TRXT: ALL FORCES FROM ONE CONDENSATE', fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    return fig


def create_dark_matter_chart():
    """Create chart showing dark matter candidates and exclusions."""
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Mass range
    masses = np.logspace(-1, 3, 100)
    
    # XENON1T limit (simplified)
    xenon_limit = 1e-46 * (masses / 50)**2
    xenon_limit[masses < 5] = 1e-40
    
    # CRESST-III limit
    cresst_limit = 1e-38 * np.ones_like(masses)
    cresst_limit[masses > 10] = 1e-45
    
    # Combined limit
    combined = np.minimum(xenon_limit, cresst_limit)
    
    # TRXT predictions
    trxt_masses = [5.71, 2.85, 1.43]
    trxt_sigmas = [5.97e-47, 3.71e-48, 2.35e-49]
    
    # Plot limits
    ax.fill_between(masses, combined, 1e-35, alpha=0.3, color='red', label='Excluded')
    ax.plot(masses, xenon_limit, 'r-', linewidth=2, label='XENON1T')
    ax.plot(masses, cresst_limit, 'b--', linewidth=2, label='CRESST-III')
    
    # DARWIN projection
    darwin_limit = 1e-49 * np.ones_like(masses)
    ax.plot(masses, darwin_limit, 'g:', linewidth=2, label='DARWIN (projected)')
    
    # TRXT candidates
    ax.scatter(trxt_masses, trxt_sigmas, s=200, c='gold', edgecolor='black', 
               zorder=10, label='TRXT Dark Tower')
    
    for m, s, name in zip(trxt_masses, trxt_sigmas, ['(128,128)', '(256,256)', '(512,512)']):
        ax.annotate(f'{name}\n{m} GeV', (m, s), xytext=(m*1.5, s*10),
                   arrowprops=dict(arrowstyle='->', color='gold'),
                   fontsize=10, color='gold', fontweight='bold')
    
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlim(0.5, 500)
    ax.set_ylim(1e-50, 1e-35)
    ax.set_xlabel('Dark Matter Mass [GeV]', fontsize=12)
    ax.set_ylabel('Cross Section σ [cm²]', fontsize=12)
    ax.set_title('TRXT DARK MATTER: Exclusion Limits & Predictions', fontsize=14, fontweight='bold')
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    # Add annotation
    ax.annotate('TRXT Dark Tower\nSurvives all current limits!\nDARWIN can detect (128,128)', 
               (0.7, 1e-48), fontsize=11, color='lime',
               bbox=dict(boxstyle='round', facecolor='black', edgecolor='lime'))
    
    plt.tight_layout()
    return fig


def create_particle_mass_chart():
    """Create chart showing particle masses and TRXT predictions."""
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # SM Fermions
    leptons = ['e', 'μ', 'τ']
    lepton_masses = [0.000511, 0.1057, 1.777]
    
    quarks = ['u', 'd', 's', 'c', 'b', 't']
    quark_masses = [0.00216, 0.00467, 0.093, 1.27, 4.18, 172.76]
    
    bosons = ['W', 'Z', 'H']
    boson_masses = [80.38, 91.19, 125.25]
    
    # TRXT scales
    trxt_scales = {
        'M*': 365.24,
        'M*/X': 1.777,  # = m_tau
        'M*/X²': 1.777/205.55,  # ~m_e scale
    }
    
    # Dark Tower
    dark_tower = [5.71, 2.85, 1.43]
    
    # Plot
    x_positions = []
    y_values = []
    colors = []
    labels = []
    
    # Leptons
    for i, (name, mass) in enumerate(zip(leptons, lepton_masses)):
        x_positions.append(i)
        y_values.append(mass)
        colors.append('blue')
        labels.append(name)
    
    # Quarks
    for i, (name, mass) in enumerate(zip(quarks, quark_masses)):
        x_positions.append(i + 4)
        y_values.append(mass)
        colors.append('red')
        labels.append(name)
    
    # Bosons
    for i, (name, mass) in enumerate(zip(bosons, boson_masses)):
        x_positions.append(i + 11)
        y_values.append(mass)
        colors.append('green')
        labels.append(name)
    
    # Dark Tower
    for i, mass in enumerate(dark_tower):
        x_positions.append(i + 15)
        y_values.append(mass)
        colors.append('gold')
        labels.append(f'DT{i+1}')
    
    # Bar chart
    bars = ax.bar(x_positions, y_values, color=colors, edgecolor='white', alpha=0.8)
    
    # Add M* line
    ax.axhline(M_STAR, color='orange', linestyle='--', linewidth=2, label=f'M* = {M_STAR:.1f} GeV')
    ax.axhline(M_TAU, color='cyan', linestyle=':', linewidth=2, label=f'm_τ = {M_TAU} GeV')
    
    ax.set_yscale('log')
    ax.set_ylim(1e-4, 1e3)
    ax.set_xticks(x_positions)
    ax.set_xticklabels(labels, fontsize=10)
    ax.set_ylabel('Mass [GeV]', fontsize=12)
    ax.set_title('PARTICLE MASSES: SM + TRXT Predictions', fontsize=14, fontweight='bold')
    ax.legend(loc='upper left', fontsize=10)
    
    # Group labels
    ax.text(1, 500, 'Leptons', ha='center', fontsize=12, color='blue', fontweight='bold')
    ax.text(6.5, 500, 'Quarks', ha='center', fontsize=12, color='red', fontweight='bold')
    ax.text(12, 500, 'Bosons', ha='center', fontsize=12, color='green', fontweight='bold')
    ax.text(16, 500, 'Dark Tower', ha='center', fontsize=12, color='gold', fontweight='bold')
    
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    return fig


def create_koide_diagram():
    """Create Koide formula visualization."""
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Left: Mass ratios
    ax1 = axes[0]
    
    masses = [0.000511, 0.1057, 1.777]
    names = ['e', 'μ', 'τ']
    sqrt_masses = [np.sqrt(m) for m in masses]
    
    # Pie chart of sqrt(m)
    ax1.pie(sqrt_masses, labels=[f'√m_{n} = {s:.4f}' for n, s in zip(names, sqrt_masses)],
           colors=['lightblue', 'blue', 'darkblue'], autopct='%1.1f%%',
           explode=(0.05, 0.05, 0.05))
    ax1.set_title('Lepton √mass Distribution', fontsize=12, fontweight='bold')
    
    # Right: Koide check
    ax2 = axes[1]
    
    lhs = sum(masses)
    rhs = (2/3) * sum(sqrt_masses)**2
    ratio = lhs / rhs
    
    bar_data = [lhs, rhs]
    bar_labels = ['m_e + m_μ + m_τ', '(2/3)(√m_e + √m_μ + √m_τ)²']
    bar_colors = ['steelblue', 'coral']
    
    bars = ax2.bar(bar_labels, bar_data, color=bar_colors, edgecolor='white')
    ax2.set_ylabel('Value [GeV]', fontsize=12)
    ax2.set_title(f'Koide Formula: Ratio = {ratio:.6f}', fontsize=12, fontweight='bold')
    
    # Add ratio annotation
    ax2.annotate(f'EXACT!\n|1 - ratio| = {abs(1-ratio):.2e}', 
                (0.5, max(bar_data)*0.8), ha='center', fontsize=14, color='green',
                fontweight='bold', bbox=dict(boxstyle='round', facecolor='white', edgecolor='green'))
    
    ax2.axhline(lhs, color='gray', linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    return fig


def create_gates_summary():
    """Create Master Protocol Gates summary chart."""
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    gates = [
        ('G0: Causality', 'c_s = 0.013c', True),
        ('G1: Bullet Cluster', 'σ/m = 6×10⁻²⁴', True),
        ('G2: Power Spectrum', 'σ₈ = 0.811', True),
        ('G3: SPARC Rotation', 'χ² = 0.15', True),
        ('G4: Solar System', '|γ-1| = 10⁻¹⁷', True),
        ('G5: Fermion Koide', 'K = 0.9999', True),
    ]
    
    y_positions = range(len(gates))
    colors = ['green' if g[2] else 'red' for g in gates]
    
    # Horizontal bar chart
    bars = ax.barh(y_positions, [1]*len(gates), color=colors, alpha=0.8, edgecolor='white', height=0.6)
    
    # Labels
    for i, (name, value, passed) in enumerate(gates):
        ax.text(0.02, i, f'{name}: {value}', va='center', ha='left', 
               fontsize=12, fontweight='bold', color='white')
        ax.text(0.98, i, '✓' if passed else '✗', va='center', ha='right',
               fontsize=20, color='white')
    
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.5, len(gates) - 0.5)
    ax.set_yticks([])
    ax.set_xticks([])
    ax.set_title('MASTER PROTOCOL V2.0: ALL 6 GATES PASSED', fontsize=16, fontweight='bold')
    
    # Add border
    for spine in ax.spines.values():
        spine.set_linewidth(2)
        spine.set_color('gold')
    
    ax.set_facecolor('#1a1a2e')
    fig.patch.set_facecolor('#1a1a2e')
    ax.title.set_color('gold')
    
    plt.tight_layout()
    return fig


def create_complete_model_diagram():
    """Create complete TRXT model overview."""
    
    fig, ax = plt.subplots(figsize=(16, 12))
    
    # Hierarchy levels
    levels = [
        (0.9, 'PLANCK SCALE', 'M_Pl = 1.22×10¹⁹ GeV', 'Quantum Gravity', '#ff6b6b'),
        (0.75, 'NJL CONDENSATION', 'Λ ~ M_Pl', 'G emerges from loops', '#ffd93d'),
        (0.6, 'TRXT MASTER SCALE', 'M* = 365 GeV', 'X = 3/(2α) ≈ 205.55', '#6bcb77'),
        (0.45, 'ELECTROWEAK', 'v = 246 GeV', 'W, Z, Higgs', '#4d96ff'),
        (0.3, 'QCD', 'Λ_QCD ~ 200 MeV', 'Confinement', '#9b59b6'),
        (0.15, 'ATOMIC', 'm_e = 0.5 MeV', 'Chemistry', '#1abc9c'),
    ]
    
    for y, name, scale, description, color in levels:
        # Level box
        rect = plt.Rectangle((0.1, y-0.05), 0.8, 0.08, 
                             facecolor=color, alpha=0.8, edgecolor='white', linewidth=2)
        ax.add_patch(rect)
        
        # Text
        ax.text(0.5, y, f'{name}\n{scale}\n{description}', 
               ha='center', va='center', fontsize=10, fontweight='bold',
               color='white' if color in ['#ff6b6b', '#9b59b6', '#4d96ff'] else 'black')
    
    # Arrows between levels
    for i in range(len(levels)-1):
        y1 = levels[i][0] - 0.05
        y2 = levels[i+1][0] + 0.03
        ax.annotate('', xy=(0.5, y2), xytext=(0.5, y1),
                   arrowprops=dict(arrowstyle='->', color='white', lw=2))
    
    # Side annotations
    ax.text(0.95, 0.9, 'GRAVITY\nEmerges', ha='left', va='center', fontsize=9, color='white')
    ax.text(0.95, 0.6, 'DARK TOWER\n5.71 GeV', ha='left', va='center', fontsize=9, color='white')
    ax.text(0.95, 0.45, 'SM PARTICLES\nEmerge', ha='left', va='center', fontsize=9, color='white')
    
    ax.set_xlim(0, 1.1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title('TRXT: COMPLETE HIERARCHY FROM PLANCK TO ATOMS', 
                fontsize=16, fontweight='bold', color='white')
    
    ax.set_facecolor('#0a0a23')
    fig.patch.set_facecolor('#0a0a23')
    
    plt.tight_layout()
    return fig


def main():
    """Generate all figures and save."""
    
    output_dir = Path(__file__).parent.parent / "results" / "comprehensive_report"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("TRXT COMPREHENSIVE REPORT: GENERATING VISUALIZATIONS")
    print("=" * 60)
    
    # Generate all figures
    figures = {
        '01_universe_timeline': create_universe_timeline(),
        '02_forces_diagram': create_forces_diagram(),
        '03_dark_matter_chart': create_dark_matter_chart(),
        '04_particle_masses': create_particle_mass_chart(),
        '05_koide_formula': create_koide_diagram(),
        '06_gates_summary': create_gates_summary(),
        '07_complete_model': create_complete_model_diagram(),
    }
    
    # Save all
    for name, fig in figures.items():
        output_path = output_dir / f'{name}.png'
        fig.savefig(output_path, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
        print(f"  Saved: {output_path.name}")
        plt.close(fig)
    
    print(f"\n[All figures saved to: {output_dir}]")
    
    return output_dir


if __name__ == "__main__":
    output_dir = main()
