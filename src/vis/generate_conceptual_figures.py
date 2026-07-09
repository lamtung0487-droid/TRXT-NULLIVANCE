"""
TRXT-NULLIVANCE: CONCEPTUAL ENGLISH FIGURES
===========================================
Generates schematic diagrams for abstract concepts 
(Quantum Foam, Nucleosynthesis, etc.) with ENGLISH labels
to replace the Vietnamese raster images.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle, PathPatch
from matplotlib.path import Path
import os

output_dir = "c:/Users/NC/Music/trxt nullivance v14/English_Submission/figures"
os.makedirs(output_dir, exist_ok=True)

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 12

def plot_quantum_foam():
    """01_quantum_foam: Bubbles of spacetime (Academic Style)."""
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_facecolor('white')
    
    # Random bubbles with outlines
    np.random.seed(42)
    for _ in range(300):
        x, y = np.random.rand(2)
        r = np.random.rand() * 0.08 + 0.01
        # Grayscale/Pastel for academic look
        color = plt.cm.Greys(np.random.rand() * 0.5 + 0.1)
        ax.add_patch(Circle((x, y), r, fc=color, ec='black', lw=0.5, alpha=0.6))
        
    ax.text(0.5, 0.5, "Quantum Foam\n(Planck Scale)", color='black', ha='center', va='center', fontsize=20, fontweight='bold', bbox=dict(facecolor='white', alpha=0.9, edgecolor='black'))
    ax.text(0.5, 0.35, "Fluctuating Geometry", color='black', ha='center', va='center', fontsize=12, bbox=dict(facecolor='white', alpha=0.9, edgecolor='none'))
    
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
    plt.savefig(f"{output_dir}/01_quantum_foam.png", dpi=300)
    plt.close()

def plot_fermion_sea():
    """02_fermion_sea: Dirac Sea (Academic Style)."""
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_facecolor('white')
    
    # Grid of particles
    x = np.linspace(0.1, 0.9, 10)
    y = np.linspace(0.1, 0.9, 10)
    X, Y = np.meshgrid(x, y)
    
    # Blue dots for fermions
    ax.scatter(X, Y, c='blue', s=100, alpha=0.6, edgecolors='black', label='Fermions')
    ax.text(0.5, 0.95, "Fermion Sea (Vacuum)", color='black', ha='center', fontsize=16, fontweight='bold')
    
    # A fluctuation
    ax.add_patch(Circle((0.5, 0.5), 0.15, fc='yellow', ec='orange', alpha=0.5, lw=2))
    ax.text(0.5, 0.5, "Excitation", color='black', ha='center', fontsize=10, fontweight='bold')
    
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
    plt.savefig(f"{output_dir}/02_fermion_sea.png", dpi=300)
    plt.close()

def plot_hadron_epoch():
    """06_hadron_epoch: Quarks forming Hadrons."""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_facecolor('white')
    
    # Proton (uud)
    c1 = Circle((0.3, 0.5), 0.15, fc='lightgray', ec='black', lw=2)
    ax.add_patch(c1)
    ax.text(0.3, 0.5, "Proton\n(uud)", ha='center', va='top')
    
    # Quarks inside
    ax.add_patch(Circle((0.25, 0.55), 0.03, fc='red', label='u')); ax.text(0.25, 0.55, 'u', ha='center', va='center', color='white')
    ax.add_patch(Circle((0.35, 0.55), 0.03, fc='green', label='u')); ax.text(0.35, 0.55, 'u', ha='center', va='center', color='white')
    ax.add_patch(Circle((0.3, 0.45), 0.03, fc='blue', label='d')); ax.text(0.3, 0.45, 'd', ha='center', va='center', color='white')
    
    # Neutron (udd)
    c2 = Circle((0.7, 0.5), 0.15, fc='lightgray', ec='black', lw=2)
    ax.add_patch(c2)
    ax.text(0.7, 0.5, "Neutron\n(udd)", ha='center', va='top')
    
    # Quarks inside
    ax.add_patch(Circle((0.65, 0.55), 0.03, fc='red')); ax.text(0.65, 0.55, 'u', ha='center', va='center', color='white')
    ax.add_patch(Circle((0.75, 0.55), 0.03, fc='blue')); ax.text(0.75, 0.55, 'd', ha='center', va='center', color='white')
    ax.add_patch(Circle((0.7, 0.45), 0.03, fc='green')); ax.text(0.7, 0.45, 'd', ha='center', va='center', color='white')
    
    ax.set_title("Hadron Epoch: Confinement (T < 200 MeV)")
    ax.set_xlim(0, 1); ax.set_ylim(0.2, 0.8); ax.axis('off')
    plt.savefig(f"{output_dir}/06_hadron_epoch.png", dpi=300)
    plt.close()

def plot_nucleosynthesis():
    """07_nucleosynthesis: BBN."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Reaction n + p -> D + gamma
    ax.text(0.2, 0.5, "n", fontsize=20, ha='center', bbox=dict(boxstyle='circle', fc='lightgray'))
    ax.text(0.3, 0.5, "+", fontsize=20, ha='center')
    ax.text(0.4, 0.5, "p", fontsize=20, ha='center', bbox=dict(boxstyle='circle', fc='lightgray'))
    
    ax.arrow(0.45, 0.5, 0.1, 0, head_width=0.05, color='black')
    
    ax.text(0.65, 0.5, "D", fontsize=20, ha='center', bbox=dict(boxstyle='circle', fc='yellow'))
    ax.text(0.75, 0.5, "+", fontsize=20, ha='center')
    ax.text(0.85, 0.5, r"$\gamma$", fontsize=20, ha='center')
    
    ax.text(0.5, 0.8, "Primordial Nucleosynthesis (BBN)", fontsize=16, fontweight='bold', ha='center')
    ax.text(0.5, 0.2, "Formation of Deuterium (First Step)", fontsize=14, ha='center')
    
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
    plt.savefig(f"{output_dir}/07_nucleosynthesis.png", dpi=300)
    plt.close()

def plot_cutoff_diagram():
    """fig_3_4_cutoff: Visual representation of UV Cutoff."""
    fig, ax = plt.subplots(figsize=(8, 6))
    
    x = np.linspace(0, 10, 100)
    y = np.exp(-x**2/10)
    
    ax.plot(x, y, 'b-', lw=3, label='Physical Theory')
    ax.axvline(5, color='r', ls='--', lw=2, label='Cutoff Lambda')
    ax.fill_between(x, y, where=(x<5), color='blue', alpha=0.2, label='Valid Region')
    ax.fill_between(x, 1.2, where=(x>5), color='gray', alpha=0.3, label='Unknown UV Physics')
    
    ax.text(2.5, 0.5, "Effective Field Theory\n(General Relativity)", ha='center', color='blue', fontweight='bold')
    ax.text(7.5, 0.5, "Quantum Foam\n(Planck Scale)", ha='center', color='gray', fontweight='bold')
    
    ax.set_xlabel("Energy Scale E")
    ax.set_ylabel("Validity of Theory")
    ax.set_title("UV Cutoff Regularization")
    ax.set_yticks([])
    ax.legend(loc='upper right')
    
    plt.savefig(f"{output_dir}/fig_3_4_cutoff.png", dpi=300)
    plt.close()

if __name__ == "__main__":
    print("Generating Conceptual Figures...")
    plot_quantum_foam()
    plot_fermion_sea()
    plot_hadron_epoch()
    plot_nucleosynthesis()
    plot_cutoff_diagram()
    print("Conceptual Figures Updated.")
