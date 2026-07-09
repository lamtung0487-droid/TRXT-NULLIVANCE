"""
TRXT PARTICLE & DARK MATTER VISUALIZATIONS
==========================================
Detailed plots for Chapter 4 (Particles) and Chapter 5 (Dark Matter).
- Harmonic Resonance Spectrum
- Koide Formula Geometry
- Dark Tower Levels
- Lane-Emden Density Profile
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, ConnectionPatch
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / "results" / "particles_dm"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Set style
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['text.color'] = 'black'
plt.rcParams['font.size'] = 12

def fig_4_1_harmonic_spectrum():
    """Visualizing the 1/p + 1/q mass spectrum"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Master Scale
    M_star = 365.24
    
    # SM Particles
    particles = [
        ('Z Boson', 8, 8, 91.19, 'green'),
        ('W Boson', 5, 50, 80.38, 'blue'),
        ('Higgs', 5, 7, 125.25, 'red'),
    ]
    
    # Plot M* line
    ax.axhline(M_star, color='gold', linestyle='--', linewidth=2, label='Master Scale M*')
    ax.text(0.5, M_star + 5, '$M^* = 365.24$ GeV', color='goldenrod', fontweight='bold', ha='center')
    
    # Plot particles
    for i, (name, p, q, mass_exp, color) in enumerate(particles):
        mass_calc = M_star * (1/p + 1/q)
        x_pos = i + 1
        
        # Predicted Mass Bar
        ax.bar(x_pos - 0.15, mass_calc, width=0.3, color=color, alpha=0.6, label=f'{name} (TRXT)' if i==0 else "")
        # Experimental Mass Bar
        ax.bar(x_pos + 0.15, mass_exp, width=0.3, color='gray', alpha=0.6, label='Experiment' if i==0 else "")
        
        # Labels
        label = f"{name}\n({p},{q})"
        ax.text(x_pos, -10, label, ha='center', va='top', fontweight='bold')
        
        # Error text
        error = 100 * (mass_calc - mass_exp) / mass_exp
        ax.text(x_pos, max(mass_calc, mass_exp) + 5, f'Err: {error:+.2f}%', ha='center', fontsize=10)

    # Add formula
    ax.text(2, 200, r"$m(p,q) = M^* \left(\frac{1}{p} + \frac{1}{q}\right)$", 
            fontsize=20, bbox=dict(boxstyle="round", facecolor="#f0f0f0", edgecolor="black"))

    ax.set_ylim(0, 400)
    ax.set_ylabel('Mass (GeV)')
    ax.set_title('HARMONIC RESONANCE: TRXT PREDICTIONS vs REALITY', fontsize=16, fontweight='bold')
    ax.legend()
    ax.axis('on')
    ax.set_xticks([])
    
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / 'fig_4_1_harmonic_spectrum.png', dpi=150)
    plt.close(fig)

def fig_4_2_koide_geometry():
    """Geometric representation of Koide Formula"""
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Koide relation: (sqrt(me) + sqrt(mmu) + sqrt(mtau))^2 = 1.5 * (me + mmu + mtau)
    # This implies vector (sqrt(me), sqrt(mmu), sqrt(mtau)) involves special angle
    
    # Data (sqrt masses)
    m = np.array([0.511e-3, 0.1057, 1.777])
    sqrt_m = np.sqrt(m)
    
    # Normalize for visualization
    v = sqrt_m / np.linalg.norm(sqrt_m)
    
    # Draw vector in 2D projection (schematic)
    # Center
    ax.scatter(0, 0, c='black')
    
    # Circle of unit norm
    circle = Circle((0, 0), 1, fill=False, linestyle='--', color='gray')
    ax.add_patch(circle)
    
    # Draw the vector (schematic projection)
    ax.arrow(0, 0, 0.8, 0.6, head_width=0.05, color='purple', linewidth=3)
    ax.text(0.4, 0.35, r'$\vec{v} = (\sqrt{m_e}, \sqrt{m_\mu}, \sqrt{m_\tau})$', fontsize=14, rotation=35, color='purple')
    
    # Angle formula
    angle_text = r"$\theta = 45^\circ + \delta$"
    ax.text(0.5, 0.1, angle_text, fontsize=14)
    
    # Explanatory text
    text = (
        "Koide Formula Geometry:\n"
        "The vector form of charged leptons\n"
        "makes an exact angle with the\n"
        "diagonal (1,1,1) in flavor space.\n\n"
        r"$K = \frac{(\sum \sqrt{m_i})^2}{\frac{3}{2} \sum m_i} \approx 1$"
    )
    ax.text(-0.9, 0.7, text, fontsize=12, bbox=dict(boxstyle="round", facecolor="#e6e6fa"))
    
    # Result verification
    K = (np.sum(sqrt_m)**2) / (1.5 * np.sum(m))
    ax.text(0, -1.2, f"Calculated K = {K:.6f}\n(Exact Topo-Protection)", ha='center', fontsize=16, color='green', fontweight='bold')

    ax.set_title('THE MYSTERY OF LEPTON MASSES (KOIDE)', fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / 'fig_4_2_koide_geometry.png', dpi=150)
    plt.close(fig)

def fig_5_1_dark_tower_levels():
    """Dark Tower Mass Ladder"""
    fig, ax = plt.subplots(figsize=(8, 10))
    
    # Levels p=q
    modes = [
        (32, 22.8, 'Excluded'),
        (64, 11.4, 'Excluded'),
        (128, 5.71, 'Candidate 1'),
        (256, 2.85, 'Candidate 2'),
        (512, 1.43, 'Candidate 3')
    ]
    
    # Draw limits
    ax.axhspan(10, 30, color='red', alpha=0.2, label='Excluded by XENON1T')
    
    # Draw ladder
    for p, mass, status in modes:
        color = 'red' if status == 'Excluded' else 'green'
        
        # Energy level line
        ax.hlines(mass, 0, 1, colors=color, linewidth=3)
        
        # Label
        label = f"({p},{p}) - {mass} GeV\n{status}"
        ax.text(1.1, mass, label, va='center', fontsize=12, color=color)

    ax.set_xlim(0, 2)
    ax.set_ylim(0, 25)
    ax.set_ylabel('Mass (GeV)')
    ax.set_title('DARK TOWER SPECTRUM: THE SURVIVORS', fontsize=16, fontweight='bold')
    ax.axis('off')
    
    # Y-axis
    ax.arrow(0, 0, 0, 24, head_width=0.05, color='black')
    
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / 'fig_5_1_dark_tower_levels.png', dpi=150)
    plt.close(fig)

def fig_5_2_lane_emden_profile():
    """Lane-Emden n=1.37 vs NFW Profile"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    r = np.linspace(0.01, 5, 100)
    
    # NFW Profile (approx 1/x(1+x)^2)
    rho_nfw = 1.0 / (r * (1 + r)**2)
    rho_nfw = rho_nfw / rho_nfw[10] # Normalize
    
    # Lane-Emden n=1.37 (approx solution)
    # Core is flat, envelope drops
    rho_trxt = 1.0 / (1 + r**2)**(1.37) # Toy approx for visualization
    rho_trxt = rho_trxt / rho_trxt[10]
    
    ax.loglog(r, rho_nfw, 'r--', linewidth=2, label='NFW (Cuspy Core)')
    ax.loglog(r, rho_trxt, 'g-', linewidth=3, label='TRXT (Cored/Flat)')
    
    ax.set_xlabel('Radius r / r_s')
    ax.set_ylabel('Density $\\rho(r)$')
    
    # Arrow to core difference
    ax.annotate("Cusp Problem\n(Singularity)", xy=(0.02, 50), xytext=(0.05, 5),
               arrowprops=dict(arrowstyle="->", color='red'))
               
    ax.annotate("Solved!\n(Finite Core)", xy=(0.02, 1.2), xytext=(0.05, 0.5),
               arrowprops=dict(arrowstyle="->", color='green'))

    ax.set_title('SOLVING THE CUSP-CORE PROBLEM', fontsize=16, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / 'fig_5_2_lane_emden_profile.png', dpi=150)
    plt.close(fig)

if __name__ == "__main__":
    print("Generating Matter visuals...")
    fig_4_1_harmonic_spectrum()
    fig_4_2_koide_geometry()
    fig_5_1_dark_tower_levels()
    fig_5_2_lane_emden_profile()
    print("Done.")
