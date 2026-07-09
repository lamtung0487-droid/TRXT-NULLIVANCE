"""
TRXT-NULLIVANCE: Hierarchy Chain Flowchart
===========================================
Generates a flowchart showing the complete derivation chain.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os

output_dir = "c:/Users/NC/Music/trxt nullivance v14/paper/submission_v16/figures"

def plot_hierarchy_chain():
    """Generate hierarchy chain flowchart."""
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_facecolor('#0d1117')
    
    # Chain data
    chain = [
        ('α(0) = 1/137', '#3498db', 'Fine Structure Constant'),
        ('X = 205.5', '#2980b9', '3/(2α(0))'),
        ('q = 6', '#27ae60', 'Abrikosov C₆ lattice'),
        ('k_F = 5/6', '#2ecc71', 'Edge-locking'),
        ('η = 0.569', '#f39c12', 'H.21 numerical'),
        ('t locked', '#e67e22', 'NJL self-consistency'),
        ('C = 5.339', '#9b59b6', 'Master formula'),
        ('g_eff = 0.026', '#8e44ad', 'C/X'),
        ('M* = 365 GeV', '#e74c3c', 'BCS exponential'),
    ]
    
    n = len(chain)
    box_width = 2.5
    box_height = 0.8
    spacing = 1.2
    
    # Calculate positions (vertical layout)
    y_positions = [(n - i - 1) * spacing for i in range(n)]
    x_center = 5
    
    for i, (label, color, desc) in enumerate(chain):
        y = y_positions[i]
        
        # Draw box
        box = FancyBboxPatch((x_center - box_width/2, y - box_height/2),
                             box_width, box_height,
                             boxstyle="round,pad=0.05,rounding_size=0.2",
                             facecolor=color, edgecolor='white', linewidth=2)
        ax.add_patch(box)
        
        # Add label
        ax.text(x_center, y, label, ha='center', va='center',
               fontsize=12, fontweight='bold', color='white')
        
        # Add description on the right
        ax.text(x_center + box_width/2 + 0.3, y, desc, ha='left', va='center',
               fontsize=10, color='lightgray')
        
        # Draw arrow to next box
        if i < n - 1:
            ax.annotate('', xy=(x_center, y_positions[i+1] + box_height/2 + 0.05),
                       xytext=(x_center, y - box_height/2 - 0.05),
                       arrowprops=dict(arrowstyle='->', color='white', lw=2))
    
    # Add title
    ax.text(x_center, y_positions[0] + 1.2, 
            'HIERARCHY PROBLEM: Complete Derivation Chain',
            ha='center', va='center', fontsize=16, fontweight='bold', color='white')
    
    # Add final conclusion box
    conclusion_y = y_positions[-1] - 1.5
    conclusion_box = FancyBboxPatch((x_center - 3, conclusion_y - 0.4),
                                    6, 0.8,
                                    boxstyle="round,pad=0.1,rounding_size=0.2",
                                    facecolor='#27ae60', edgecolor='gold', linewidth=3)
    ax.add_patch(conclusion_box)
    ax.text(x_center, conclusion_y, '🏆 HIERARCHY PROBLEM SOLVED!', 
           ha='center', va='center', fontsize=14, fontweight='bold', color='white')
    
    # Arrow to conclusion
    ax.annotate('', xy=(x_center, conclusion_y + 0.4),
               xytext=(x_center, y_positions[-1] - box_height/2 - 0.05),
               arrowprops=dict(arrowstyle='->', color='gold', lw=3))
    
    # Add error annotation
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
    print(f"✅ Generated: {output_dir}/fig_hierarchy_chain_flowchart.png")

if __name__ == "__main__":
    plot_hierarchy_chain()
    print("Done!")
