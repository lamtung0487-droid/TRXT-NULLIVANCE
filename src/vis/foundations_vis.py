"""
TRXT FOUNDATIONS VISUALIZATIONS
===============================
Generates diagrams for Chapter 1 (Problems) and Chapter 2 (Foundations).
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, ArrowStyle, FancyArrowPatch, Circle
from matplotlib.sankey import Sankey
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / "results" / "foundations"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Set style
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['text.color'] = 'black'

def fig_1_1_physics_problems():
    """Diagram of Open Problems in Physics"""
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.axis('off')
    
    # Central Goal
    goal_box = FancyBboxPatch((0.35, 0.45), 0.3, 0.1, boxstyle="round,pad=0.05", 
                             facecolor='#2ecc71', alpha=0.9)
    ax.add_patch(goal_box)
    ax.text(0.5, 0.5, "UNIFIED THEORY\n(Quantum + Gravity)", ha='center', va='center', 
            fontsize=12, fontweight='bold', color='white')
    
    # Problems circling it
    problems = [
        (0.5, 0.85, "DARK MATTER\nWhat is it?", '#e74c3c'),
        (0.85, 0.5, "DARK ENERGY\nWhy Λ ~ 10⁻¹²⁰?", '#9b59b6'),
        (0.5, 0.15, "HIERARCHY ISSUE\nWhy M_Weak << M_Planck?", '#f1c40f'),
        (0.15, 0.5, "GRAVITY vs QM\nRenormalization?", '#3498db')
    ]
    
    for x, y, text, color in problems:
        # Box
        box = FancyBboxPatch((x-0.12, y-0.08), 0.24, 0.16, boxstyle="round,pad=0.02",
                            facecolor=color, alpha=0.8)
        ax.add_patch(box)
        ax.text(x, y, text, ha='center', va='center', fontsize=10, color='white', fontweight='bold')
        
        # Arrow pointing to center (Blocker)
        ax.annotate("", xy=(0.5 + (x-0.5)*0.4, 0.5 + (y-0.5)*0.4), xytext=(x, y),
                   arrowprops=dict(arrowstyle="->", color=color, lw=2, linestyle='dashed'))
        
        # Blocker X
        mid_x = 0.5 + (x-0.5)*0.6
        mid_y = 0.5 + (y-0.5)*0.6
        ax.text(mid_x, mid_y, "??", ha='center', va='center', fontsize=14, color='red', fontweight='bold')

    ax.set_title("MAJOR ROADBLOCKS IN MODERN PHYSICS", fontsize=16, fontweight='bold')
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / 'fig_1_1_physics_problems.png', dpi=150)
    plt.close(fig)

def fig_1_2_trxt_roadmap():
    """TRXT Research Roadmap Flowchart"""
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.axis('off')
    
    steps = [
        (0.1, "STEP 1\nMicroscopic Foundation\n(NJL at Planck Scale)", '#34495e'),
        (0.35, "STEP 2\nEmergence\n(Induced Gravity)", '#2980b9'),
        (0.6, "STEP 3\nPrediction\n(Dark Tower & Koide)", '#8e44ad'),
        (0.85, "STEP 4\nVerification\n(6 Gates & Real Data)", '#27ae60')
    ]
    
    for i, (x, text, color) in enumerate(steps):
        # Box
        box = FancyBboxPatch((x-0.1, 0.4), 0.2, 0.2, boxstyle="round,pad=0.02",
                            facecolor=color, alpha=0.9)
        ax.add_patch(box)
        ax.text(x, 0.5, text, ha='center', va='center', fontsize=10, color='white', fontweight='bold')
        
        # Arrow to next
        if i < len(steps) - 1:
            next_x = steps[i+1][0]
            ax.annotate("", xy=(next_x-0.11, 0.5), xytext=(x+0.11, 0.5),
                       arrowprops=dict(arrowstyle="->", color='black', lw=2))

    ax.set_title("TRXT RESEARCH METHODOLOGY (BOTTOM-UP)", fontsize=16, fontweight='bold')
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / 'fig_1_2_trxt_roadmap.png', dpi=150)
    plt.close(fig)

def fig_2_2_trxt_constants():
    """Visualizing the X Factor and Alpha relationship"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Draw scale bar
    ax.hlines(0.5, 0, 10, color='black', lw=3)
    
    # Alpha point (Fundamental)
    ax.scatter(1, 0.5, s=200, c='blue', label='Fine Structure Constant α')
    ax.text(1, 0.4, "α\n1/137", ha='center', va='top', fontsize=12, color='blue')
    
    # X Factor (Derived)
    ax.scatter(5, 0.5, s=200, c='purple', label='TRXT Scaling Factor X')
    ax.text(5, 0.4, "X\n~205.55", ha='center', va='top', fontsize=12, color='purple')
    
    # Relation arrow
    ax.annotate("X = 3 / (2α)", xy=(4.8, 0.55), xytext=(1.2, 0.55),
               arrowprops=dict(arrowstyle="->", color='black', lw=2, connectionstyle="arc3,rad=-0.2"))
    
    # Master Scale (Result)
    ax.scatter(9, 0.5, s=300, c='gold', edgecolors='black', label='Master Scale M*')
    ax.text(9, 0.4, "M*\n365.24 GeV", ha='center', va='top', fontsize=14, fontweight='bold')
    
    # Relation arrow 2
    ax.annotate("M* = m_τ × X", xy=(8.7, 0.55), xytext=(5.2, 0.55),
               arrowprops=dict(arrowstyle="->", color='black', lw=2, connectionstyle="arc3,rad=-0.2"))

    ax.set_ylim(0.2, 1.0)
    ax.axis('off')
    ax.set_title("THE GOLDEN LINK: FROM ALPHA TO MASTER SCALE", fontsize=16, fontweight='bold')
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / 'fig_2_2_trxt_constants.png', dpi=150)
    plt.close(fig)

def main():
    fig_1_1_physics_problems()
    fig_1_2_trxt_roadmap()
    fig_2_2_trxt_constants()
    print(f"Generated diagrams in {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
