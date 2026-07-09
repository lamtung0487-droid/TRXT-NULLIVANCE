"""
TRXT-NULLIVANCE: ENGLISH FIGURES GENERATION
============================================
Generates all scientific plots with English labels for the academic report.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle
import os

output_dir = "c:/Users/NC/Music/trxt nullivance v14/github_release/docs/figures"
os.makedirs(output_dir, exist_ok=True)

# Set English font
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 11

def compute_band_structure():
    """Compute the Dirac band structure on T² lattice."""
    t = t2 = 0.8
    kx = np.linspace(-np.pi, np.pi, 500)
    ky = np.linspace(-np.pi, np.pi, 500)
    KX, KY = np.meshgrid(kx, ky)
    
    dx = t * np.sin(KX)
    dy = t * np.sin(KY)
    dz = t2 * (2 - np.cos(KX) - np.cos(KY))
    
    E = np.sqrt(dx**2 + dy**2 + dz**2)
    return KX, KY, E, t, t2

def plot_band_and_fermi_surface():
    """Generate band structure and Fermi surface contour plot in English."""
    KX, KY, E, t, t2 = compute_band_structure()
    
    k_star_x = 5 * np.pi / 6
    k_star_y = 0
    dx_star = t * np.sin(k_star_x)
    dy_star = t * np.sin(k_star_y)
    dz_star = t2 * (2 - np.cos(k_star_x) - np.cos(k_star_y))
    epsilon_0 = np.sqrt(dx_star**2 + dy_star**2 + dz_star**2)
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Left: Band structure
    ax1 = axes[0]
    im = ax1.contourf(KX, KY, E, levels=50, cmap='viridis')
    ax1.contour(KX, KY, E, levels=[epsilon_0], colors='red', linewidths=2)
    ax1.scatter([k_star_x], [k_star_y], c='yellow', s=100, marker='*', zorder=5, 
               label=r'$k^* = (5\pi/6, 0)$')
    ax1.set_xlabel(r'$k_x$', fontsize=12)
    ax1.set_ylabel(r'$k_y$', fontsize=12)
    ax1.set_title(f'Band Structure $E(k)$ on $T^2$\n($t = t_2 = {t}$)', fontsize=14)
    ax1.set_xlim(-np.pi, np.pi)
    ax1.set_ylim(-np.pi, np.pi)
    ax1.legend()
    plt.colorbar(im, ax=ax1, label='$E(k)$')
    
    # Right: Fermi Surface
    ax2 = axes[1]
    ax2.set_facecolor('#1a1a2e')
    ax2.contour(KX, KY, E, levels=[epsilon_0], colors='#00ff88', linewidths=3)
    ax2.scatter([0], [0], c='white', s=150, marker='o', zorder=5, label=r'$\Gamma$ (Dirac point)')
    ax2.scatter([k_star_x], [k_star_y], c='yellow', s=100, marker='*', zorder=5, 
               label=r'$k^* = 5\pi/6$')
    ax2.axhline(0, color='white', alpha=0.3, linestyle='--')
    ax2.axvline(0, color='white', alpha=0.3, linestyle='--')
    ax2.set_xlabel(r'$k_x$', fontsize=12, color='white')
    ax2.set_ylabel(r'$k_y$', fontsize=12, color='white')
    ax2.set_title(f'Topological Fermi Surface $\\Sigma_F$\n$\\varepsilon_0 = {epsilon_0:.4f}$', 
                 fontsize=14, color='white')
    ax2.set_xlim(-np.pi, np.pi)
    ax2.set_ylim(-np.pi, np.pi)
    ax2.legend(facecolor='#1a1a2e', labelcolor='white')
    ax2.tick_params(colors='white')
    for spine in ax2.spines.values():
        spine.set_color('white')
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/fig_band_fermi_surface.png", dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✅ Generated: fig_band_fermi_surface.png")

def plot_bcs_exponential():
    """Generate BCS exponential suppression plot in English."""
    g_eff = np.linspace(0.01, 0.1, 100)
    Lambda_UV = 1.22e19
    M_star = 2 * Lambda_UV * np.exp(-1 / g_eff)
    
    g_actual = 0.0258
    M_actual = 365
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.semilogy(g_eff, M_star, 'b-', linewidth=2, 
               label=r'$M^* = 2\Lambda_{UV} \exp(-1/g_{eff})$')
    ax.axhline(M_actual, color='red', linestyle='--', linewidth=2, 
              label=f'$M^* = {M_actual}$ GeV (target)')
    ax.axvline(g_actual, color='green', linestyle='--', linewidth=2, 
              label=f'$g_{{eff}} = {g_actual}$')
    
    ax.scatter([g_actual], [M_actual], c='yellow', s=200, marker='*', zorder=5, 
              edgecolors='black', linewidths=2)
    
    ax.set_xlabel(r'$g_{eff} = G \cdot N(0)$', fontsize=14)
    ax.set_ylabel(r'$M^*$ (GeV)', fontsize=14)
    ax.set_title('BCS Dimensional Transmutation\nExponential Suppression from Planck to EW Scale', 
                fontsize=14)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0.01, 0.1)
    ax.set_ylim(1e0, 1e20)
    
    ax.annotate(f'17-order gap!\n$\\Lambda_{{UV}} / M^* \\sim 10^{{17}}$',
               xy=(g_actual, M_actual), xytext=(0.06, 1e10),
               arrowprops=dict(arrowstyle='->', color='black'),
               fontsize=12, ha='center')
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/fig_bcs_exponential.png", dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✅ Generated: fig_bcs_exponential.png")

def plot_hierarchy_verification():
    """Generate hierarchy verification bar chart in English."""
    data = {
        'L_F': 14.998,
        'I_F': 26.345,
        'η': 0.569,
        'C': 5.339,
    }
    
    target_C = 5.30
    error_percent = abs(data['C'] - target_C) / target_C * 100
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Left: H.21 numerical results
    ax1 = axes[0]
    labels = [r'$L_F$', r'$I_F$', r'$\eta$', r'$\mathcal{C}$', 'Target $\mathcal{C}$']
    values = [data['L_F'], data['I_F'], data['η'], data['C'], target_C]
    colors = ['#3498db', '#2ecc71', '#e74c3c', '#9b59b6', '#f39c12']
    
    bars = ax1.bar(labels, values, color=colors, edgecolor='black', linewidth=1.5)
    ax1.set_ylabel('Value', fontsize=12)
    ax1.set_title('H.21 Numerical Verification Results', fontsize=14)
    ax1.axhline(target_C, color='orange', linestyle='--', linewidth=2, 
               label=f'Target $\\mathcal{{C}}$ = {target_C}')
    
    for bar, val in zip(bars, values):
        height = bar.get_height()
        ax1.annotate(f'{val:.3f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
    ax1.legend()
    
    # Right: Hierarchy chain
    ax2 = axes[1]
    chain_labels = [r'$\alpha(0)\to X$', 'Abrikosov\n$q=6$', r'$k_F=5/6$', 
                   'H.21\n$\\eta=0.569$', 'NJL\n$t$ lock', r'$\mathcal{C}=5.339$', 
                   r'$g_{eff}$'+'\n=0.026']
    chain_values = [205.5, 6, 5/6, 0.569, 0.8, 5.339, 0.0258]
    chain_normalized = [np.log10(max(v, 0.001)) + 3 for v in chain_values]
    
    ax2.barh(chain_labels, chain_normalized, 
            color=plt.cm.Blues(np.linspace(0.3, 0.9, len(chain_labels))))
    ax2.set_xlabel('Normalized Value (log scale + offset)', fontsize=12)
    ax2.set_title(f'Hierarchy Chain Verification\nError from target: {error_percent:.2f}%', 
                 fontsize=14)
    
    for i, (label, val) in enumerate(zip(chain_labels, chain_values)):
        ax2.annotate(f'{val:.4f}' if val < 10 else f'{val:.1f}',
                    xy=(chain_normalized[i], i),
                    xytext=(5, 0), textcoords="offset points",
                    ha='left', va='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/fig_hierarchy_verification.png", dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✅ Generated: fig_hierarchy_verification.png")

def plot_abrikosov_lattice():
    """Generate Abrikosov lattice comparison in English."""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Left: Triangular lattice
    ax1 = axes[0]
    ax1.set_facecolor('#1a1a2e')
    a = 1.0
    rows = 5
    for row in range(rows):
        for col in range(rows):
            x = col * a + (row % 2) * a/2
            y = row * a * np.sqrt(3)/2
            circle = Circle((x, y), 0.1, color='#00ff88', fill=True)
            ax1.add_patch(circle)
    
    ax1.set_xlim(-0.5, 5)
    ax1.set_ylim(-0.5, 4)
    ax1.set_aspect('equal')
    ax1.set_title('Triangular Lattice\n$C_6$ Symmetry', fontsize=14, color='white')
    ax1.text(2.25, -0.3, r'$\beta_A = 1.1596$', fontsize=14, ha='center', 
            color='#00ff88', fontweight='bold')
    ax1.text(2.25, 3.7, '✓ MINIMUM ENERGY', fontsize=12, ha='center', 
            color='#00ff88', fontweight='bold')
    ax1.axis('off')
    
    # Middle: Square lattice
    ax2 = axes[1]
    ax2.set_facecolor('#1a1a2e')
    for row in range(5):
        for col in range(5):
            x = col * a
            y = row * a
            circle = Circle((x, y), 0.1, color='#ff6b6b', fill=True)
            ax2.add_patch(circle)
    
    ax2.set_xlim(-0.5, 4.5)
    ax2.set_ylim(-0.5, 4.5)
    ax2.set_aspect('equal')
    ax2.set_title('Square Lattice\n$C_4$ Symmetry', fontsize=14, color='white')
    ax2.text(2, -0.3, r'$\beta_A = 1.1803$', fontsize=14, ha='center', 
            color='#ff6b6b', fontweight='bold')
    ax2.text(2, 4.2, '✗ HIGHER ENERGY', fontsize=12, ha='center', 
            color='#ff6b6b', fontweight='bold')
    ax2.axis('off')
    
    # Right: Energy comparison
    ax3 = axes[2]
    lattices = ['Triangular\n($C_6$)', 'Square\n($C_4$)']
    beta_values = [1.1596, 1.1803]
    colors = ['#00ff88', '#ff6b6b']
    
    bars = ax3.bar(lattices, beta_values, color=colors, edgecolor='black', linewidth=2)
    ax3.set_ylabel(r'Abrikosov Parameter $\beta_A$', fontsize=12)
    ax3.set_title('Lattice Energy Comparison\n(Lower = More Stable)', fontsize=14)
    ax3.set_ylim(1.14, 1.20)
    
    for bar, val in zip(bars, beta_values):
        ax3.annotate(f'{val:.4f}',
                    xy=(bar.get_x() + bar.get_width()/2, val),
                    xytext=(0, 3), textcoords='offset points',
                    ha='center', fontsize=12, fontweight='bold')
    
    ax3.annotate('', xy=(0, 1.1596), xytext=(1, 1.1803),
                arrowprops=dict(arrowstyle='->', color='white', lw=2))
    ax3.text(0.5, 1.17, r'$\Delta E < 0$'+'\nTriangular\nis stable!', fontsize=10, ha='center', 
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/fig_abrikosov_lattice.png", dpi=150, bbox_inches='tight', 
                facecolor='#0d1117')
    plt.close()
    print(f"✅ Generated: fig_abrikosov_lattice.png")

def plot_hierarchy_chain():
    """Generate hierarchy chain flowchart in English."""
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_facecolor('#0d1117')
    
    chain = [
        (r'$\alpha(0) = 1/137$', '#3498db', 'Fine Structure Constant'),
        ('$X = 205.5$', '#2980b9', r'$3/(2\alpha(0))$'),
        ('$q = 6$', '#27ae60', 'Abrikosov $C_6$ lattice'),
        ('$k_F = 5/6$', '#2ecc71', 'Edge-locking'),
        (r'$\eta = 0.569$', '#f39c12', 'H.21 numerical'),
        ('$t$ locked', '#e67e22', 'NJL self-consistency'),
        (r'$\mathcal{C} = 5.339$', '#9b59b6', 'Master formula'),
        ('$g_{eff} = 0.026$', '#8e44ad', r'$\mathcal{C}/X$'),
        ('$M^* = 365$ GeV', '#e74c3c', 'BCS exponential'),
    ]
    
    n = len(chain)
    box_width = 2.5
    box_height = 0.8
    spacing = 1.2
    y_positions = [(n - i - 1) * spacing for i in range(n)]
    x_center = 5
    
    for i, (label, color, desc) in enumerate(chain):
        y = y_positions[i]
        box = FancyBboxPatch((x_center - box_width/2, y - box_height/2),
                             box_width, box_height,
                             boxstyle="round,pad=0.05,rounding_size=0.2",
                             facecolor=color, edgecolor='white', linewidth=2)
        ax.add_patch(box)
        ax.text(x_center, y, label, ha='center', va='center',
               fontsize=12, fontweight='bold', color='white')
        ax.text(x_center + box_width/2 + 0.3, y, desc, ha='left', va='center',
               fontsize=10, color='lightgray')
        
        if i < n - 1:
            ax.annotate('', xy=(x_center, y_positions[i+1] + box_height/2 + 0.05),
                       xytext=(x_center, y - box_height/2 - 0.05),
                       arrowprops=dict(arrowstyle='->', color='white', lw=2))
    
    ax.text(x_center, y_positions[0] + 1.2, 
            'HIERARCHY PROBLEM: Complete Derivation Chain',
            ha='center', va='center', fontsize=16, fontweight='bold', color='white')
    
    conclusion_y = y_positions[-1] - 1.5
    conclusion_box = FancyBboxPatch((x_center - 3, conclusion_y - 0.4),
                                    6, 0.8,
                                    boxstyle="round,pad=0.1,rounding_size=0.2",
                                    facecolor='#27ae60', edgecolor='gold', linewidth=3)
    ax.add_patch(conclusion_box)
    ax.text(x_center, conclusion_y, 'HIERARCHY MECHANISM PROPOSED', 
           ha='center', va='center', fontsize=14, fontweight='bold', color='white')
    
    ax.annotate('', xy=(x_center, conclusion_y + 0.4),
               xytext=(x_center, y_positions[-1] - box_height/2 - 0.05),
               arrowprops=dict(arrowstyle='->', color='gold', lw=3))
    
    ax.text(x_center + 4.5, y_positions[6], 
            'Error < 1%\nvs target 5.30',
            ha='left', va='center', fontsize=10, color='#2ecc71',
            bbox=dict(boxstyle='round', facecolor='#1a1a2e', edgecolor='#2ecc71'))
    
    ax.set_xlim(0, 12)
    ax.set_ylim(-3, 12)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/fig_hierarchy_chain_flowchart.png", dpi=150, 
                bbox_inches='tight', facecolor='#0d1117')
    plt.close()
    print(f"✅ Generated: fig_hierarchy_chain_flowchart.png")

if __name__ == "__main__":
    print("=" * 60)
    print("TRXT-NULLIVANCE: Generating English Figures")
    print("=" * 60)
    
    plot_band_and_fermi_surface()
    plot_bcs_exponential()
    plot_hierarchy_verification()
    plot_abrikosov_lattice()
    plot_hierarchy_chain()
    
    print("\n" + "=" * 60)
    print("✅ All English figures generated successfully!")
    print("=" * 60)
