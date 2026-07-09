"""
TRXT NJL MECHANISM VISUALIZATIONS
=================================
Detailed plots for the microscopic theory chapter.
- 3D Mexican Hat Potential
- Gap Equation Solutions
- Feynman Diagrams (Bubble sum)
- Heat Kernel Cutoff Regularization
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyBboxPatch, Circle, Arc, FancyArrowPatch
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / "results" / "njl_mechanism"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Set style
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['text.color'] = 'black'
plt.rcParams['font.size'] = 12

def fig_3_1_mexican_hat():
    """3D Mexican Hat Potential Visualization"""
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Grid
    x = np.linspace(-2, 2, 100)
    y = np.linspace(-2, 2, 100)
    X, Y = np.meshgrid(x, y)
    R = np.sqrt(X**2 + Y**2)
    
    # Potential V = -mu^2 |phi|^2 + lambda |phi|^4
    # Parameters for visual niceness
    mu2 = 2.0
    lam = 1.0
    Z = -mu2 * R**2 + lam * R**4
    
    # Plot
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                           linewidth=0, antialiased=True, alpha=0.9)
    
    # Add Goldstone mode path (circle at the bottom)
    theta = np.linspace(0, 2*np.pi, 100)
    r_min = np.sqrt(mu2/(2*lam)) # Min location
    x_circ = r_min * np.cos(theta)
    y_circ = r_min * np.sin(theta)
    z_circ = -mu2 * r_min**2 + lam * r_min**4
    ax.plot(x_circ, y_circ, z_circ + 0.1, color='gold', linewidth=3, label='Goldstone Mode (Massless)')

    # Add Higgs mode path (radial)
    ax.plot([r_min, 2.0], [0, 0], [z_circ, Z[50, 99]], color='green', linewidth=3, label='Higgs Mode (Massive)')

    # Axis labels
    ax.set_xlabel('Re($\\Phi$)', fontsize=12)
    ax.set_ylabel('Im($\\Phi$)', fontsize=12)
    ax.set_zlabel('Potential $V(\\Phi)$', fontsize=12)
    ax.set_title('SYMMETRY BREAKING: THE MEXICAN HAT POTENTIAL', fontsize=16, fontweight='bold')
    
    # View angle
    ax.view_init(elev=30, azim=45)
    
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / 'fig_3_1_mexican_hat.png', dpi=150)
    plt.close(fig)

def fig_3_2_gap_equation():
    """Numerical Solution of Gap Equation vs Coupling G"""
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # Dimensionless Gap Equation approximation:
    # 1 = g * (1 - m^2 * log(1/m^2)) for m << 1
    # Let x = m/Lambda, g = G / G_crit
    pass  # We will solve M vs G numerically

    g_vals = np.linspace(0.5, 2.0, 200)
    m_vals = []
    
    for g in g_vals:
        if g <= 1.0:
            m_vals.append(0)
        else:
            # Simple approximate solution for BCS-style gap
            # M ~ exp(-1 / (g-1))
            m = np.exp(-1 / (np.sqrt(g - 1 + 1e-10))) # Toy model behavior
            # More rigorous NJL behavior: M ~ sqrt(g - 1) near transition
            m = np.sqrt(max(0, g - 1)) # Mean field exponent 0.5
            m_vals.append(m)
            
    ax.plot(g_vals, m_vals, 'b-', linewidth=3)
    ax.fill_between(g_vals, 0, m_vals, where=(g_vals>1), color='blue', alpha=0.1)
    
    # Critical point
    ax.axvline(1.0, color='red', linestyle='--', linewidth=2)
    ax.text(1.02, 0.1, '$G = G_{crit}$', color='red', fontsize=14, rotation=90)
    
    # Annotations
    ax.annotate('Symmetric Phase\n(Massless)', xy=(0.7, 0.1), ha='center', fontsize=12)
    ax.annotate('Broken Phase\n(Massive Condensate)', xy=(1.5, 0.4), ha='center', fontsize=12)
    
    ax.set_xlabel('Coupling Constant $G / G_{crit}$', fontsize=14)
    ax.set_ylabel('Generated Mass $M / \Lambda$', fontsize=14)
    ax.set_title('THE GAP EQUATION: MASS GENERATION', fontsize=16, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / 'fig_3_2_gap_equation.png', dpi=150)
    plt.close(fig)

def fig_3_3_feynman_loops():
    """Visualizing the Induced Gravity Loop mechanism"""
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.axis('off')
    
    # Draw large fermion loop
    circle = Circle((0.5, 0.5), 0.25, fill=False, edgecolor='blue', linewidth=3)
    ax.add_patch(circle)
    
    # Fermion arrows on loop
    ax.add_patch(FancyArrowPatch((0.5, 0.75), (0.51, 0.75), arrowstyle='->', mutation_scale=20, color='blue'))
    ax.add_patch(FancyArrowPatch((0.5, 0.25), (0.49, 0.25), arrowstyle='->', mutation_scale=20, color='blue'))
    
    ax.text(0.5, 0.5, 'Fermion Loop\nWait for $N_f$ flavors', ha='center', va='center', color='blue', fontsize=12)
    
    # External Gravitons attached
    # Top
    ax.annotate("", xy=(0.5, 0.75), xytext=(0.5, 0.95),
               arrowprops=dict(arrowstyle="->", color='black', lw=2, linestyle='dashed'))
    ax.text(0.5, 0.97, 'Graviton $h_{\\mu\\nu}$', ha='center')
    
    # Bottom
    ax.annotate("", xy=(0.5, 0.25), xytext=(0.5, 0.05),
               arrowprops=dict(arrowstyle="->", color='black', lw=2, linestyle='dashed'))
    ax.text(0.5, 0.02, 'Graviton $h_{\\alpha\\beta}$', ha='center')
    
    # Labels for terms
    ax.text(0.15, 0.5, 'Vacuum Polarization $\Pi_{\mu\\nu}$', fontsize=14, fontweight='bold', color='purple')
    
    # Equation
    eq = r"$S_{eff} \sim \int d^4x \sqrt{-g} \left[ \Lambda^4 + M^2 R + \dots \right]$"
    ax.text(0.85, 0.5, eq, fontsize=16, bbox=dict(facecolor='#f0f0f0', edgecolor='gray'))
    
    ax.set_title('INDUCED GRAVITY: GRAVITONS EMERGE FROM LOOPS', fontsize=16, fontweight='bold')
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / 'fig_3_3_feynman_loops.png', dpi=150)
    plt.close(fig)

def fig_3_4_cutoff_regularization():
    """Visualizing Euclidean Cutoff Sphere"""
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Sphere
    u = np.linspace(0, 2 * np.pi, 50)
    v = np.linspace(0, np.pi, 50)
    x = 10 * np.outer(np.cos(u), np.sin(v))
    y = 10 * np.outer(np.sin(u), np.sin(v))
    z = 10 * np.outer(np.ones(np.size(u)), np.cos(v))
    
    ax.plot_wireframe(x, y, z, color='red', alpha=0.3)
    
    # Inner region
    ax.scatter([0], [0], [0], color='black', s=100)
    ax.text(0, 0, 0, "Low Energy\nPhysics", fontsize=10)
    
    # Cutoff Label
    ax.text(0, 8, 8, "$\Lambda_{cutoff}$", fontsize=14, color='red')
    ax.text(0, 12, 12, "Unknown Physics\n(String Theory?)", fontsize=10, color='gray')
    
    ax.set_title("MOMENTUM SPACE CUTOFF $\Lambda$", fontsize=16, fontweight='bold')
    ax.set_xlabel("$k_x$")
    ax.set_ylabel("$k_y$")
    ax.set_zlabel("$k_z$")
    
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / 'fig_3_4_cutoff.png', dpi=150)
    plt.close(fig)

if __name__ == "__main__":
    print("Generating NJL visuals...")
    fig_3_1_mexican_hat()
    fig_3_2_gap_equation()
    fig_3_3_feynman_loops()
    fig_3_4_cutoff_regularization()
    print("Done.")
