import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Constants
ALPHA = 1/137.035999084
X_SCALE = 3 / (2 * ALPHA)
M_TAU = 1.77686  # GeV
M_STAR = M_TAU * X_SCALE # ~365.24 GeV

# Observed Data
M_W = 80.379
SIGMA_W = 0.012

# ==============================================================================
# PLOT 1: ROBUSTNESS STABILITY PLATEAUS
# ==============================================================================
def plot_robustness():
    print("Generating Robustness Plot...")
    p = 5
    m_range = np.linspace(79.0, 82.0, 1000)
    q_exact = []
    q_int = []

    for m in m_range:
        # q = p*M* / (p*m - M*)
        val = (p * m - M_STAR)
        if val == 0:
            q_val = np.inf
        else:
            q_val = p * M_STAR / val
        
        q_exact.append(q_val)
        q_int.append(round(q_val))

    plt.figure(figsize=(10, 6))
    
    # Plot Step Function
    plt.plot(m_range, q_int, 'b-', label='Interger Mode q', linewidth=2)
    # plt.plot(m_range, q_exact, 'b--', alpha=0.3, label='Exact q (continuous)')

    # Highlight W region
    plt.axvline(x=M_W, color='r', linestyle='--', label=f'Observed M_W = {M_W:.3f} GeV')
    plt.axvspan(M_W - SIGMA_W, M_W + SIGMA_W, color='r', alpha=0.3, label=f'1-sigma Uncertainty')
    
    # Highlight CDF II region (just for comparison)
    plt.axvspan(80.433 - 0.009, 80.433 + 0.009, color='g', alpha=0.1, label='CDF II (80.433 GeV)')

    # Annotate Plateau
    plt.text(80.35, 50.5, 'Stable Plateau q=50', fontsize=12, color='blue', fontweight='bold')
    
    plt.title('Robustness of W-Boson Mode Assignment (Sector p=5)', fontsize=14)
    plt.xlabel('Input Mass $M_{obs}$ (GeV)', fontsize=12)
    plt.ylabel('Calculated Mode Integer $q$', fontsize=12)
    plt.ylim(44, 56)
    plt.xlim(79.5, 81.5)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(loc='upper right')
    
    plt.tight_layout()
    plt.savefig('fig_robustness_plateau.png', dpi=300)
    print("Saved fig_robustness_plateau.png")

# ==============================================================================
# PLOT 2: PARTICLE PERIODIC TABLE (Reciprocal Space)
# ==============================================================================
def plot_periodic_table():
    print("Generating Periodic Table Plot...")
    plt.figure(figsize=(10, 8))
    
    # Axes: x = 1/p, y = 1/q
    
    # Draw Iso-mass lines: M = M* (x + y)  => y = M/M* - x
    x_vals = np.linspace(0, 0.5, 100)
    
    masses = [
        (125.25, 'Higgs (125 GeV)', 'r'),
        (91.19, 'Z (91 GeV)', 'b'),
        (80.38, 'W (80 GeV)', 'g'),
        (1.77, 'Tau (1.78 GeV)', 'gray')
    ]
    
    for mass, label, color in masses:
        y_vals = (mass / M_STAR) - x_vals
        plt.plot(x_vals, y_vals, '--', color=color, alpha=0.5, linewidth=1)
        # Label lines
        plt.text(0.02, (mass/M_STAR)-0.02, label, color=color, fontsize=9, rotation=-45)

    # Plot Modes
    # (p, q, Label, Color, Marker)
    modes = [
        (5, 7, 'Higgs (5,7)', 'red', 's'),
        (5, 50, 'W (5,50)', 'green', 'o'),
        (8, 8, 'Z (8,8)', 'blue', 'D'),
        (5, 6, 'Open (5,6)', 'orange', 'X'),
        (6, 6, 'Open (6,6)', 'purple', 'X'),
        (128, 128, 'DT-1', 'black', '^') # This will be near origin
    ]
    
    for p, q, label, color, marker in modes:
        inv_p = 1.0/p
        inv_q = 1.0/q
        plt.scatter(inv_p, inv_q, c=color, marker=marker, s=150, edgecolors='k', zorder=10)
        plt.text(inv_p + 0.015, inv_q + 0.015, label, fontsize=11, fontweight='bold')

    # Add limits and labels
    plt.xlim(0, 0.35)
    plt.ylim(0, 0.35)
    plt.xlabel('Inverse Winding $1/p$', fontsize=12)
    plt.ylabel('Inverse Winding $1/q$', fontsize=12)
    plt.title('TRXT Particle Periodic Table (Reciprocal Lattice)', fontsize=14)
    
    # Add Sector Regions
    # EW Sector p=5 => x=0.2
    plt.axvline(x=0.2, color='green', linestyle=':', alpha=0.5)
    plt.text(0.205, 0.33, 'Electroweak Sector (p=5)', color='green', rotation=90)
    
    # Neutral Sector p=q => y=x
    plt.plot([0, 0.35], [0, 0.35], 'b:', alpha=0.5)
    plt.text(0.33, 0.34, 'Neutral Sector (p=q)', color='blue', rotation=45)

    plt.grid(True, linestyle='--', alpha=0.3)
    
    # Zoom inset for Dark Tower near origin? Maybe not needed for main plot clarity
    
    plt.tight_layout()
    plt.savefig('fig_particle_periodic_table.png', dpi=300)
    print("Saved fig_particle_periodic_table.png")

if __name__ == "__main__":
    plot_robustness()
    plot_periodic_table()
