
"""
TRXT-NULLIVANCE: SCIENTIFIC VISUALIZATION V3 (PROFESSIONAL GRADE)
================================================================
Generates high-fidelity, scientific-grade figures for the TRXT research report.
Focuses on physical accuracy: Fields, Density Maps, Phase Transitions.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Ellipse, PathPatch
from matplotlib.path import Path
import matplotlib.cm as cm
import matplotlib.colors as mcolors
from scipy.stats import multivariate_normal
import os

# Configuration
output_dir = "c:/Users/NC/Music/trxt nullivance v14/English_Submission/figures"
os.makedirs(output_dir, exist_ok=True)

# Style Overrides for "Scientific Dark Mode"
plt.style.use('dark_background')
plt.rcParams.update({
    'font.family': 'serif',
    'axes.labelsize': 12,
    'font.size': 10,
    'legend.fontsize': 10,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'text.color': 'white',
    'axes.labelcolor': 'white',
    'xtick.color': 'white',
    'ytick.color': 'white'
})

def save_fig(fig, filename):
    fig.savefig(f"{output_dir}/{filename}", dpi=200, bbox_inches='tight', facecolor='black')
    plt.close(fig)

# ------------------------------------------------------------------
# 1. QUANTUM FOAM: Topological Field Fluctuations
# ------------------------------------------------------------------
def plot_quantum_foam():
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 1. Background Scalar Field (Metric Fluctuations)
    x = np.linspace(-3, 3, 200)
    y = np.linspace(-2, 2, 200)
    X, Y = np.meshgrid(x, y)
    
    # Create "Foamy" noise structure
    np.random.seed(42)
    Z = np.zeros_like(X)
    for k in range(1, 6):
        freq = 2**k
        phase = np.random.rand()*2*np.pi
        Z += (1/freq) * np.sin(freq*X + phase) * np.cos(freq*Y + phase)
    
    # Heatmap
    contour = ax.pcolormesh(X, Y, Z, cmap='magma', shading='gouraud', alpha=0.6)
    
    # 2. Topological Defects (Wormholes / Handles)
    # Draw "holes" in the manifold
    for _ in range(15):
        cx, cy = np.random.uniform(-2.5, 2.5), np.random.uniform(-1.5, 1.5)
        # Draw a black hole with a glowing rim
        ax.add_patch(Circle((cx, cy), 0.15, color='black', zorder=10))
        ax.add_patch(Circle((cx, cy), 0.18, color='cyan', alpha=0.6, zorder=9))
        # Connection line (handle)
        if np.random.rand() > 0.5:
            cx2, cy2 = cx + np.random.uniform(-0.5, 0.5), cy + np.random.uniform(-0.5, 0.5)
            ax.plot([cx, cx2], [cy, cy2], color='cyan', alpha=0.2, lw=1)

    ax.set_title("QUANTUM FOAM (Planck Scale)\nTopological Fluctuations & Metric Noise", fontsize=14, fontweight='bold', color='#ffcc00')
    ax.text(0, -1.8, r"Metric $g_{\mu\nu}$ is ill-defined", ha='center', color='white', alpha=0.7)
    
    ax.set_xlim(-3, 3); ax.set_ylim(-2, 2); ax.axis('off')
    save_fig(fig, "01_quantum_foam.png")

# ------------------------------------------------------------------
# 2. INFLATION: Scalar Field Rolling & Stretching
# ------------------------------------------------------------------
def plot_inflation():
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_facecolor('#110000')
    
    # Gradient flow background (Expansion)
    x = np.linspace(0, 10, 100)
    y = np.linspace(-4, 4, 100)
    X, Y = np.meshgrid(x, y)
    # Expansion factor increases with x
    Z = np.exp(0.3 * X) 
    ax.imshow(Z, extent=[0, 10, -4, 4], cmap='inferno', aspect='auto', alpha=0.4)

    # 1. Quantum Fluctuations (Small ripples on left)
    # 2. Stretching (Long waves on right)
    
    np.random.seed(10)
    for i in range(20):
        # Start y position
        y_start = np.random.uniform(-3, 3)
        
        # Fluctuation wave
        x_wave = np.linspace(0, 10, 200)
        # Frequency decreases (wavelength increases) as x increases
        # Amplitude stays roughly constant or grows slightly
        wavelength = 0.2 * np.exp(0.4 * x_wave) 
        y_wave = y_start + 0.1 * np.sin(2 * np.pi * x_wave / (0.5 + 0.1*x_wave)) # Wiggle
        
        # But we want to show STRETCHING explicitly.
        # Let's draw discrete packets that get longer.
        
        # Packet 1 (Early)
        ax.plot([0.5, 1.5], [y_start, y_start + 0.1*np.sin(10)], color='white', alpha=0.5, lw=1)
        # Packet 2 (Mid) - Stretched
        ax.plot([3, 5], [y_start, y_start+0.2], color='gold', alpha=0.7, lw=2)
        # Packet 3 (Late) - Super stretched
        ax.plot([7, 10], [y_start, y_start], color='gold', alpha=0.9, lw=2)

    # Conformal grid lines expanding
    for x_grid in np.exp(np.linspace(0, 2.3, 10)) - 1: # 0 to ~9
        ax.axvline(x=x_grid, color='gray', alpha=0.2, linestyle='--')

    # Annotations
    ax.annotate("Quantum\nFluctuation", xy=(1, 0), xytext=(1, -3.5), 
                arrowprops=dict(facecolor='white', arrowstyle='->'), ha='center')
    ax.annotate("Stretched to\nMacro Scale", xy=(8.5, 0), xytext=(8.5, -3.5), 
                arrowprops=dict(facecolor='gold', arrowstyle='->'), ha='center', color='gold')

    ax.set_title("SUPERFLUID INFLATION\nExponential Stretching of Modes", fontsize=16, fontweight='bold', color='#ffcc00')
    ax.axis('off')
    save_fig(fig, "04_inflation.png")

# ------------------------------------------------------------------
# 3. RECOMBINATION: Surface of Last Scattering
# ------------------------------------------------------------------
def plot_recombination():
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Split screen: Opaque Plasma (Left) vs Transparent (Right)
    # Gradient transition at x=0
    
    x = np.linspace(-5, 5, 200)
    y = np.linspace(-3, 3, 200)
    X, Y = np.meshgrid(x, y)
    
    # Fog density
    Fog = 1 / (1 + np.exp(2*X)) # Sigmoid transition High -> Low
    ax.imshow(Fog, extent=[-5, 5, -3, 3], cmap='Blues_r', aspect='auto', alpha=0.8)
    
    # 1. Plasma Era (Left) - Scattering
    np.random.seed(55)
    for _ in range(50):
        gx, gy = np.random.uniform(-4.5, -0.5), np.random.uniform(-2.8, 2.8)
        # Proton
        ax.scatter(gx, gy, c='red', s=30, alpha=0.8)
        # Electron
        ax.scatter(gx + np.random.uniform(-0.2, 0.2), gy + np.random.uniform(-0.2, 0.2), c='cyan', s=10, alpha=0.8)
        # Trapped Photon (Zigzag)
        px, py = gx, gy
        for _ in range(3):
            next_px = px + np.random.uniform(-0.3, 0.3)
            next_py = py + np.random.uniform(-0.3, 0.3)
            ax.plot([px, next_px], [py, next_py], color='yellow', lw=1, alpha=0.5)
            px, py = next_px, next_py

    # 2. Recombination Event (At x ~ 0)
    ax.axvline(x=0, color='white', linestyle='--', alpha=0.5)
    ax.text(0, 3.1, "Last Scattering Surface\n(T ~ 3000 K)", ha='center', color='white', fontweight='bold')

    # 3. Transparent Era (Right) - Free Streaming
    for i in range(30):
        # Start at surface
        sy = np.random.uniform(-2.8, 2.8)
        
        # Atom formed
        ax.scatter(0, sy, c='white', s=40, edgecolors='cyan', lw=1.5, zorder=10) # Neutral H
        
        # Photon Stream
        x_stream = np.linspace(0, 5, 100)
        y_stream = sy + 0.1 * np.sin(5 * x_stream + i) # Coherent wave
        ax.plot(x_stream, y_stream, color='gold', lw=1.2, alpha=0.9)
        
        # Arrowhead
        ax.arrow(4.8, y_stream[-5], 0.1, 0, color='gold', head_width=0.1)

    ax.text(-2.5, -2.5, "OPAQUE PLASMA\n(Charged)", ha='center', color='cyan', fontsize=12)
    ax.text(2.5, -2.5, "TRANSPARENT UNIVERSE\n(Neutral)", ha='center', color='gold', fontsize=12)
    
    ax.set_xlim(-5, 5); ax.set_ylim(-3, 3); ax.axis('off')
    save_fig(fig, "08_recombination.png")


# ------------------------------------------------------------------
# 4. BULLET CLUSTER: Density Contours
# ------------------------------------------------------------------
def plot_bullet_cluster():
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_facecolor('black')
    
    grid_size = 200
    x = np.linspace(-4, 4, grid_size)
    y = np.linspace(-3, 3, grid_size)
    X, Y = np.meshgrid(x, y)
    pos = np.dstack((X, Y))
    
    # 1. Dark Matter (Blue) - Collisionless, moved ahead
    # Left DM center (passed to left)
    dm_left = multivariate_normal(mean=[-2, 0], cov=[[0.5, 0], [0, 0.8]])
    # Right DM center (passed to right)
    dm_right = multivariate_normal(mean=[2, 0], cov=[[0.5, 0], [0, 0.8]])
    
    Z_dm = dm_left.pdf(pos) + dm_right.pdf(pos)
    
    # Contour for DM
    ax.contour(X, Y, Z_dm, levels=6, colors='blue', linewidths=1.5, alpha=0.8)
    ax.contourf(X, Y, Z_dm, levels=6, cmap='Blues', alpha=0.3)
    
    # 2. Hot Gas (Red) - Stuck in middle (Collisional)
    # Shockwave shape (flattened on collision side)
    gas_left = multivariate_normal(mean=[-0.8, 0], cov=[[0.2, 0], [0, 1.0]])
    gas_right = multivariate_normal(mean=[0.8, 0], cov=[[0.2, -0.1], [0, 1.0]]) # Tilted bullet
    
    Z_gas = gas_left.pdf(pos) + gas_right.pdf(pos)
    
    # Contour for Gas
    ax.contour(X, Y, Z_gas, levels=8, colors='red', linewidths=1.5, alpha=0.8)
    ax.contourf(X, Y, Z_gas, levels=100, cmap='hot', alpha=0.5) # Glowing core
    
    # 3. Galaxies (Stars) - Follow DM but point-like
    np.random.seed(99)
    # Left cluster galaxies
    for _ in range(30):
        gx, gy = np.random.normal(-2, 0.6), np.random.normal(0, 0.8)
        ax.scatter(gx, gy, c='white', s=np.random.uniform(5, 20), alpha=0.7)
    # Right cluster galaxies
    for _ in range(30):
        gx, gy = np.random.normal(2, 0.6), np.random.normal(0, 0.8)
        ax.scatter(gx, gy, c='white', s=np.random.uniform(5, 20), alpha=0.7)

    # 4. Annotations
    ax.annotate("Dark Matter (Mass Center)\nObserved via Lensing", xy=(-2, 1.2), xytext=(-3, 2.2),
                arrowprops=dict(facecolor='cyan', arrowstyle='->'), ha='center', color='cyan')
    
    ax.annotate("Hot Gas (X-ray)\nStuck due to Drag", xy=(0, 0.8), xytext=(0, 2.2),
                arrowprops=dict(facecolor='orange', arrowstyle='->'), ha='center', color='orange')

    ax.set_title("BULLET CLUSTER (1E 0657-56)\nProof of Dark Matter separation from Baryons", fontsize=14, color='white')
    ax.axis('off')
    
    save_fig(fig, "05_separation.png")


if __name__ == "__main__":
    print("Generating Scientific Figures (V3)...")
    plot_quantum_foam()
    plot_inflation()
    plot_recombination()
    plot_bullet_cluster()
    print("DONE.")
