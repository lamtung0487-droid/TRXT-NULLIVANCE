"""
TRXT-NULLIVANCE: RICH ENGLISH VISUALIZATIONS (RESTORING ORIGINAL QUALITY)
========================================================================
Replicates the high-quality dark-mode visualizations from the Vietnamese report,
but strictly translates all text to English.
Source: early_universe_vis.py, late_universe_vis.py
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Wedge
import matplotlib.cm as cm
import matplotlib.patheffects as pe
import os

output_dir = "c:/Users/NC/Music/trxt nullivance v14/English_Submission/figures"
os.makedirs(output_dir, exist_ok=True)

# Set global style for "Rich/Dark" look
plt.rcParams['figure.facecolor'] = 'black'
plt.rcParams['axes.facecolor'] = 'black'
plt.rcParams['text.color'] = 'white'
plt.rcParams['axes.labelcolor'] = 'white'
plt.rcParams['xtick.color'] = 'white'
plt.rcParams['ytick.color'] = 'white'
plt.rcParams['font.family'] = 'serif'

def create_snapshot(filename, time_label, title, description, details, render_func_or_particles, color_theme='blue'):
    """Generic function to create a universe snapshot (Dark Mode)."""
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_facecolor('black')
    
    # 1. Render Logic
    if callable(render_func_or_particles):
        render_func_or_particles(ax)
        # Boundary for Late Universe
        ax.add_patch(Circle((0, 0), 0.95, fill=False, edgecolor='white', linestyle=':', alpha=0.3))
    else:
        # Particle Logic for Early Universe
        r_uni = 0.8
        if 'foam' in filename:
             theta = np.linspace(0, 2*np.pi, 200)
             r = r_uni + 0.05 * np.sin(10*theta) * np.cos(5*theta)
             x, y = r * np.cos(theta), r * np.sin(theta)
             ax.plot(x, y, color=color_theme, alpha=0.3, linestyle='--')
             ax.fill(x, y, color=color_theme, alpha=0.1)
        else:
            uni = Circle((0, 0), r_uni, color=color_theme, alpha=0.1)
            ax.add_patch(uni)
            ax.add_patch(Circle((0, 0), r_uni, fill=False, edgecolor=color_theme, linestyle='--', alpha=0.5))
            
        np.random.seed(42)
        for p_type, count, p_color, p_size, p_marker in render_func_or_particles:
             for _ in range(count):
                r = np.sqrt(np.random.rand()) * r_uni * 0.9
                theta = np.random.rand() * 2 * np.pi
                x, y = r * np.cos(theta), r * np.sin(theta)
                if p_marker == 'twist':
                    t = np.linspace(0, 4*np.pi, 20)
                    dx = 0.02 * t/max(t) * np.cos(t); dy = 0.02 * t/max(t) * np.sin(t)
                    ax.plot(x+dx, y+dy, color=p_color, linewidth=1, alpha=0.8)
                elif p_marker == 'wave_inflation':
                    # INFLATION: Long, stretched smooth waves
                    x_wave = np.linspace(-0.2, 0.2, 50)
                    y_wave = 0.02 * np.sin(20 * x_wave) 
                    # Rotate
                    angle = np.random.rand() * np.pi
                    ca, sa = np.cos(angle), np.sin(angle)
                    x_rot = x_wave * ca - y_wave * sa
                    y_rot = x_wave * sa + y_wave * ca
                    ax.plot(x + x_rot, y + y_rot, color=p_color, alpha=0.6, lw=1.5)
                elif p_marker == 'photon_wave':
                    # RECOMBINATION: Wavy photon paths (Sinusoidal light)
                    length = 0.4
                    x_p = np.linspace(0, length, 50)
                    y_p = 0.02 * np.sin(30 * x_p) # Wiggle
                    
                    angle = np.random.rand() * 2 * np.pi
                    ca, sa = np.cos(angle), np.sin(angle)
                    
                    # Transform standard wave to position
                    x_rot = x_p * ca - y_p * sa
                    y_rot = x_p * sa + y_p * ca
                    
                    ax.plot(x + x_rot, y + y_rot, color='gold', alpha=0.8, lw=1)
                    # Add arrowhead at end
                    ax.arrow(x + x_rot[-1], y + y_rot[-1], 0.01*ca, 0.01*sa, 
                             head_width=0.015, color='gold', alpha=0.8)

                else:
                    ax.scatter(x, y, s=p_size, c=p_color, marker=p_marker, alpha=0.8, edgecolors='none')

    # 2. Text Annotations
    ax.text(0, 0.9, time_label, ha='center', fontsize=16, fontweight='bold', color='#ffcc00')
    ax.text(0, 0.82, title, ha='center', fontsize=20, fontweight='bold', color='white')
    
    # 3. Description Box
    rect = FancyBboxPatch((-0.9, -1.05), 1.8, 0.35, boxstyle="round,pad=0.05", 
                         facecolor='#222222', edgecolor='gray', alpha=0.9)
    ax.add_patch(rect)
    
    desc_text = f"{description}\n\n{details}"
    ax.text(0, -0.87, desc_text, ha='center', va='center', fontsize=11, wrap=True)

    # 4. Specific Annotations for Clarity
    if '04_inflation' in filename:
        # Arrow pointing to a wave
        ax.annotate('Stretched Quantum\nFluctuation', xy=(0.2, 0.2), xytext=(0.4, 0.5),
                   arrowprops=dict(arrowstyle='->', color='yellow', lw=1.5),
                   color='yellow', fontsize=12, fontweight='bold', ha='center')
        # Arrow pointing to a "yellow dot" (Cooper pair)
        ax.annotate('Cooper Pair\n(Condensate)', xy=(-0.3, 0.3), xytext=(-0.6, 0.6),
                   arrowprops=dict(arrowstyle='->', color='gold', lw=1.5),
                   color='gold', fontsize=12, fontweight='bold', ha='center')
    elif '08_recombination' in filename:
        # Arrow pointing to a photon
        ax.annotate('CMB Photon\n(Light)', xy=(0.3, 0.3), xytext=(0.5, 0.6),
                   arrowprops=dict(arrowstyle='->', color='gold', lw=1.5),
                   color='gold', fontsize=12, fontweight='bold', ha='center')

    ax.set_xlim(-1, 1); ax.set_ylim(-1.1, 1.1); ax.axis('off')
    
    plt.tight_layout()
    fig.savefig(f"{output_dir}/{filename}", dpi=150, bbox_inches='tight', facecolor='black')
    plt.close(fig)

# --- LATE UNIVERSE RENDERERS ---



def draw_condensation(ax):
    """Draw NJL Condensation with detailed Cooper Pairs."""
    ax.set_facecolor('#1a1a00') # Dark Gold/Yellowish background
    np.random.seed(42)
    
    # Draw Cooper Pairs
    for _ in range(50):
        # Center of pair
        cx, cy = np.random.uniform(-0.8, 0.8, 2)
        angle = np.random.rand() * np.pi
        separation = 0.04
        
        # Two particles
        dx = separation/2 * np.cos(angle)
        dy = separation/2 * np.sin(angle)
        
        p1 = (cx - dx, cy - dy)
        p2 = (cx + dx, cy + dy)
        
        # Bond
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color='gold', lw=2, alpha=0.8)
        
        # Particles
        ax.scatter([p1[0], p2[0]], [p1[1], p2[1]], color='yellow', s=30, edgecolors='orange', zorder=10)
        
        # Glow
        glow = Circle((cx, cy), 0.08, color='gold', alpha=0.1)
        ax.add_patch(glow)

    # Background mist (Condensate field)
    for _ in range(100):
        x, y = np.random.uniform(-1, 1, 2)
        ax.scatter(x, y, c='yellow', s=2, alpha=0.3)
    
    ax.text(0, -0.6, r"$\langle \bar{\Psi}\Psi \rangle \neq 0$", ha='center', color='gold', fontsize=24)

def draw_inflation(ax):
    """Draw Inflation with linked Pairs and Waves."""
    ax.set_facecolor('#200000') # Dark Red background for high energy
    np.random.seed(42)
    
    # Draw coupled Pair -> Stretched Wave
    for _ in range(30):
        # Origin (Cooper Pair location)
        cx, cy = np.random.uniform(-0.8, 0.8, 2)
        
        # 1. Draw Cooper Pair (The "Seed" / Root)
        ax.scatter(cx, cy, c='gold', s=40, edgecolors='orange', zorder=10)
        
        # 2. Draw Stretched Wave emanating from this dot
        # Wave definition
        length = 0.5 + 0.3 * np.random.rand() # Long stretched line
        x_wave = np.linspace(0, length, 50)
        y_wave = 0.03 * np.sin(20 * x_wave) # Amplitude
        
        # Random direction
        angle = np.random.rand() * 2 * np.pi
        ca, sa = np.cos(angle), np.sin(angle)
        
        # Rotate and translate to start at (cx, cy)
        x_rot = x_wave * ca - y_wave * sa
        y_rot = x_wave * sa + y_wave * ca
        
        # Plot wave connected to dot
        ax.plot(cx + x_rot, cy + y_rot, color='white', alpha=0.6, lw=1.5)
        
    # Annotations - MUST MATCH THE MAIN LOGIC'S EXPECTATIONS
    ax.text(0, -0.5, "EXPONENTIAL STRETCHING", ha='center', color='white', alpha=0.2, fontsize=24, fontweight='bold')

def draw_hadronization(ax):
    ax.set_facecolor('#1a0500') 
    np.random.seed(42)
    for _ in range(15):
        cx, cy = np.random.uniform(-0.6, 0.6, 2)
        u1_pos = (cx, cy+0.05); u2_pos = (cx-0.04, cy-0.03); d_pos = (cx+0.04, cy-0.03)
        ax.plot([u1_pos[0], u2_pos[0]], [u1_pos[1], u2_pos[1]], 'w-', alpha=0.5, lw=1)
        ax.plot([u2_pos[0], d_pos[0]], [u2_pos[1], d_pos[1]], 'w-', alpha=0.5, lw=1)
        ax.plot([d_pos[0], u1_pos[0]], [d_pos[1], u1_pos[1]], 'w-', alpha=0.5, lw=1)
        ax.scatter(*u1_pos, c='red', s=40, zorder=10); ax.scatter(*u2_pos, c='red', s=40, zorder=10)
        ax.scatter(*d_pos, c='blue', s=40, zorder=10)
        ax.add_patch(Circle((cx, cy), 0.08, color='white', alpha=0.1))
    ax.text(0, 0, "Quark Confinement\nStrong Force takes over", ha='center', color='orange', alpha=0.5, fontsize=20, rotation=30)

def draw_nucleosynthesis(ax):
    ax.set_facecolor('#331100')
    np.random.seed(10)
    positions = np.random.uniform(-0.7, 0.7, (10, 2))
    for i, (cx, cy) in enumerate(positions):
        if i < 7: 
            ax.scatter(cx, cy, c='red', s=60, edgecolors='white')
            ax.text(cx+0.02, cy+0.02, "1H", fontsize=8, color='white')
        else: 
            ax.scatter(cx-0.02, cy, c='red', s=60, edgecolors='white')
            ax.scatter(cx+0.02, cy, c='red', s=60, edgecolors='white')
            ax.scatter(cx, cy+0.03, c='gray', s=60, edgecolors='white')
            ax.scatter(cx, cy-0.03, c='gray', s=60, edgecolors='white')
            ax.add_patch(Circle((cx, cy), 0.08, color='yellow', alpha=0.2))
            ax.text(cx+0.05, cy+0.05, "4He", fontsize=10, color='yellow', fontweight='bold')
    ax.arrow(-0.4, -0.4, 0.2, 0.2, head_width=0.03, color='white')
    ax.text(-0.3, -0.3, "Fusion", color='white')


def draw_recombination(ax):
    """Draw Recombination: Atoms form, Photons escape (Linked)."""
    ax.set_facecolor('#000022')
    np.random.seed(55)
    
    # Draw Atom -> Photon pairs
    for _ in range(40):
        # 1. The Atom (Source)
        cx, cy = np.random.uniform(-0.85, 0.85, 2)
        
        # Nucleus
        ax.scatter(cx, cy, c='red', s=40, zorder=5)
        # Electron Orbit
        ax.add_patch(Circle((cx, cy), 0.04, color='cyan', fill=False, alpha=0.4, lw=1))
        # Electron
        angle_e = np.random.rand() * 2 * np.pi
        ex, ey = cx + 0.04*np.cos(angle_e), cy + 0.04*np.sin(angle_e)
        ax.scatter(ex, ey, c='cyan', s=15, zorder=6)
        
        # 2. The Photon (Effect) - escaping FROM the atom
        # Wave geometry
        length = 0.4 + 0.2 * np.random.rand()
        x_wave = np.linspace(0.06, length, 50) # Start slightly outside orbit
        y_wave = 0.03 * np.sin(30 * x_wave)
        
        # Random direction OUTWARD
        angle = np.random.rand() * 2 * np.pi
        ca, sa = np.cos(angle), np.sin(angle)
        
        x_rot = x_wave * ca - y_wave * sa
        y_rot = x_wave * sa + y_wave * ca
        
        # Plot wave
        ax.plot(cx + x_rot, cy + y_rot, color='gold', alpha=0.6, lw=1)
        # Arrowhead at end
        ax.arrow(cx + x_rot[-1], cy + y_rot[-1], 0.01*ca, 0.01*sa, 
                 head_width=0.015, color='gold', alpha=0.8)

    ax.text(0, 0, "UNIVERSE BECOMES TRANSPARENT\nCMB RELEASED", ha='center', color='gold', alpha=0.3, fontsize=16, fontweight='bold')

def draw_bullet_cluster(ax):
    """Draw Bullet Cluster Separation (Rich Style)."""
    ax.set_facecolor('#000022')
    
    # Dark Matter (Blue) - Passed through
    # Left DM
    ax.add_patch(FancyBboxPatch((-0.6, -0.3), 0.3, 0.6, boxstyle="round,pad=0.1", fc='blue', alpha=0.3))
    ax.text(-0.5, 0.4, "Dark Matter\n(Passed)", color='cyan', ha='center')
    
    # Right DM
    ax.add_patch(FancyBboxPatch((0.4, -0.3), 0.3, 0.6, boxstyle="round,pad=0.1", fc='blue', alpha=0.3))
    ax.text(0.5, 0.4, "Dark Matter\n(Passed)", color='cyan', ha='center')
    
    # Gas (Red) - Stuck in middle (Shockwave)
    # Left Gas lobe
    ax.add_patch(FancyBboxPatch((-0.2, -0.25), 0.2, 0.5, boxstyle="round,pad=0.1", fc='red', alpha=0.5))
    # Right Gas lobe
    ax.add_patch(FancyBboxPatch((0.1, -0.25), 0.2, 0.5, boxstyle="round,pad=0.1", fc='red', alpha=0.5))
    
    ax.text(0, -0.5, "Hot Gas (X-ray)\n(Stuck due to Friction)", color='red', ha='center', fontsize=14)
    ax.text(0, 0, "Gravity Center != Gas Center\n(Direct Proof of DM)", color='white', alpha=0.5, ha='center', fontsize=10)


def draw_cosmic_web(ax):
    ax.set_facecolor('black')
    np.random.seed(99)
    x = np.random.uniform(-1, 1, 1000); y = np.random.uniform(-1, 1, 1000)
    from scipy.spatial import cKDTree
    tree = cKDTree(np.c_[x, y])
    pairs = tree.query_pairs(r=0.15)
    for i, j in pairs:
        ax.plot([x[i], x[j]], [y[i], y[j]], c='purple', alpha=0.1, lw=0.5)
    for i in range(len(x)):
        neighbors = len(tree.query_ball_point([x[i], y[i]], 0.15))
        if neighbors > 5:
            size = neighbors * 2; color = cm.viridis(neighbors/20)
            ax.scatter(x[i], y[i], s=size, color=color, alpha=0.8)

# --- MAIN GENERATION ---

if __name__ == "__main__":
    print("Generating Rich English Figures...")

    # 1. Quantum Foam
    create_snapshot('01_quantum_foam.png', 'Time: Undefined (t < 10^-43 s)', 'QUANTUM FOAM',
        'Topological chaotic state. No space, no time.',
        'Spacetime is torn continuously. Wormholes appear and vanish.\nMetric g_uv undefined.',
        [('wormhole', 30, 'cyan', 100, 'o'), ('fluctuation', 50, 'magenta', 50, 'o')], 'purple')

    # 2. Fermion Sea
    create_snapshot('02_fermion_sea.png', 'Time: t ~ 10^-43 s (Planck Era)', 'PLANCKIAN FERMION SEA',
        'Chiral Fermions (Psi) appear. Massless.',
        'The universe is a sea of free spin-1/2 particles.\nNo binding. No gravity yet.',
        [('fermion', 100, '#00ff00', 30, '^')], 'green')

    # 3. Condensation (Updated with custom renderer and MathText)
    create_snapshot('03_condensation.png', 'Time: t ~ 10^-36 s (GUT Era)', 'NJL CONDENSATION',
        r'Key Event: Cooper Pairing $\langle \bar{\Psi}\Psi \rangle \neq 0$',
        'Fermions pair up. Gravity emerges from stiffness of condensate.\nSpacetime forms.',
        draw_condensation)

    # 4. Inflation (Updated with linked Dot->Wave logic)
    create_snapshot('04_inflation.png', 'Time: t ~ 10^-32 s', 'SUPERFLUID INFLATION',
        'Universe expands exponentially (e^60).',
        'Condensation energy released drives expansion.\nQuantum fluctuations stretched to macro scales.',
        draw_inflation)

    # 5. Separation (Bullet Cluster)
    create_snapshot('05_separation.png', 'Time: t ~ 10^-34 s (Symmetry Breaking)', 'MATTER SEPARATION',
        'Dark Matter decouples from Baryons.',
        'Bullet Cluster evidence: Dark Matter passes through, Gas interacts and stops.',
        draw_bullet_cluster)

    # 6. Hadronization
    create_snapshot('06_hadron_epoch.png', 'Time: t ~ 10^-6 s (Hadron Epoch)', 'CONFINEMENT',
        'Universe cools, Quarks cannot be free.',
        'Strong Force becomes dominant.\nQuarks combine into Protons (uud) and Neutrons (udd).',
        draw_hadronization)

    # 7. Nucleosynthesis
    create_snapshot('07_nucleosynthesis.png', 'Time: t ~ 3 mins (Nucleosynthesis)', 'PRIMORDIAL FUSION',
        'The cosmic nuclear reactor activates.',
        'Protons and Neutrons fuse to form first Nuclei: Deuterium, He-4, Li-7.\nH:He ratio fixed at 75%:25%.',
        draw_nucleosynthesis)

    # 8. Recombination (Updated with linked Atom->Photon logic)
    create_snapshot('08_recombination.png', 'Time: t ~ 380,000 years', 'FIRST LIGHT',
        'Electrons captured by Nuclei. Atoms form.',
        'Universe becomes electrically neutral.\nPhotons (wavy lines) escape freely -> CMB born.',
        draw_recombination)
        
    # 9. Structure
    create_snapshot('09_structure_formation.png', 'Time: 100M - 13.8B years', 'COSMIC WEB & GALAXIES',
        'Gravity and Dark Matter build structure.',
        'Dark Matter (Dark Tower) clumps into Halos.\nGas falls into these wells, forming spiral galaxies along the cosmic web.',
        draw_cosmic_web)
        
    print("DONE: Restored RICH visualizations with English labels.")
