"""
TRXT-NULLIVANCE: Abrikosov Vortex Lattice Comparison
====================================================
Generates a scientific plot comparing triangular and square vortex lattices.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, RegularPolygon
import os

output_dir = "c:/Users/NC/Music/trxt nullivance v14/github_release/docs/figures"

def plot_abrikosov_comparison():
    """Generate comparison of triangular vs square vortex lattice."""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Left: Triangular lattice
    ax1 = axes[0]
    ax1.set_facecolor('#1a1a2e')
    
    # Generate triangular lattice points
    a = 1.0  # lattice constant
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
    ax1.text(2.25, -0.3, r'$\beta_A = 1.1596$', fontsize=14, ha='center', color='#00ff88', fontweight='bold')
    ax1.text(2.25, 3.7, 'LOW ENERGY (Stable)', fontsize=12, ha='center', color='#00ff88', fontweight='bold')
    ax1.axis('off')
    
    # Middle: Square lattice
    ax2 = axes[1]
    ax2.set_facecolor('#1a1a2e')
    
    # Generate square lattice points
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
    ax2.text(2, -0.3, r'$\beta_A = 1.1803$', fontsize=14, ha='center', color='#ff6b6b', fontweight='bold')
    ax2.text(2, 4.2, 'HIGH ENERGY (Unstable)', fontsize=12, ha='center', color='#ff6b6b', fontweight='bold')
    ax2.axis('off')
    
    # Right: Energy comparison bar chart
    ax3 = axes[2]
    lattices = ['Triangular\n($C_6$)', 'Square\n($C_4$)']
    beta_values = [1.1596, 1.1803]
    colors = ['#00ff88', '#ff6b6b']
    
    bars = ax3.bar(lattices, beta_values, color=colors, edgecolor='black', linewidth=2)
    ax3.set_ylabel(r'Abrikosov Parameter $\beta_A$', fontsize=12)
    ax3.set_title('Lattice Energy Comparison\n(Lower = More Stable)', fontsize=14)
    ax3.set_ylim(1.14, 1.20)
    
    # Add value labels
    for bar, val in zip(bars, beta_values):
        ax3.annotate(f'{val:.4f}',
                    xy=(bar.get_x() + bar.get_width()/2, val),
                    xytext=(0, 3), textcoords='offset points',
                    ha='center', fontsize=12, fontweight='bold')
    
    # Add arrow showing energy difference
    ax3.annotate('', xy=(0, 1.1596), xytext=(1, 1.1803),
                arrowprops=dict(arrowstyle='->', color='white', lw=2))
    ax3.text(0.5, 1.17, 'ΔE < 0\nTriangular\nStable!', fontsize=10, ha='center', 
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/fig_abrikosov_lattice.png", dpi=150, bbox_inches='tight', 
                facecolor='#0d1117')
    plt.close()
    print(f"✅ Generated: {output_dir}/fig_abrikosov_lattice.png")

if __name__ == "__main__":
    plot_abrikosov_comparison()
    print("Done!")
