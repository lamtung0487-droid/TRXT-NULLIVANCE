"""
L2.6 Branch Q2: Energy Level Analysis
=====================================
Calculates the effective Hamiltonian energy of stable topological orbitals.
H ~ Sum(1 - cos(dTheta))
"""

import numpy as np
import matplotlib.pyplot as plt
import json
from pathlib import Path
from tqdm import tqdm

class SimAnalysis:
    def __init__(self, size=64):
        self.nx = size
        self.ny = size
        self.dim = 3
        # No dynamics needed, just static analysis of constructed fields
        
    def construct_dipole(self, r0):
        # Construct ideal dipole field
        # We can also relax it, but let's measure the "Ideal" energy of the configuration
        # found in the stability sweep.
        cx, cy = self.nx / 2.0, self.ny / 2.0
        y, x = np.mgrid[0:self.ny, 0:self.nx]
        z = np.ones((self.ny, self.nx), dtype=complex)
        
        # V (+1)
        dx1 = (x - (cx - r0/2) + self.nx/2) % self.nx - self.nx/2
        dy1 = (y - cy + self.ny/2) % self.ny - self.ny/2
        r1 = np.sqrt(dx1**2 + dy1**2)
        z *= np.tanh(r1/2.0) * np.exp(1j * (+1) * np.arctan2(dy1, dx1))
        
        # A (-1)
        dx2 = (x - (cx + r0/2) + self.nx/2) % self.nx - self.nx/2
        dy2 = (y - cy + self.ny/2) % self.ny - self.ny/2
        r2 = np.sqrt(dx2**2 + dy2**2)
        z *= np.tanh(r2/2.0) * np.exp(1j * (-1) * np.arctan2(dy2, dx2))
        
        return np.angle(z)

    def calculate_energy(self, theta):
        # XY Model Hamiltonian
        # E = Sum_{<ij>} [1 - cos(theta_i - theta_j)]
        
        # X-bonds
        dx = np.roll(theta, -1, axis=1) - theta
        E_x = np.sum(1 - np.cos(dx))
        
        # Y-bonds
        dy = np.roll(theta, -1, axis=0) - theta
        E_y = np.sum(1 - np.cos(dy))
        
        return E_x + E_y

def run_energy_scan():
    # Use the stable radii found (approx) and some intermediate ones to show the wells
    # Found: ~3.5, ~7.1
    # Let's scan radius continuous to see the Energy Landscape V(r)
    
    r_scan = np.linspace(2.0, 12.0, 100)
    energies = []
    
    analyzer = SimAnalysis(size=64)
    
    print("Scanning Effective Energy Landscape...")
    for r in r_scan:
        theta = analyzer.construct_dipole(r)
        E = analyzer.calculate_energy(theta)
        energies.append(E)
        
    # Find Local Minima in Energy
    energies = np.array(energies)
    # Simple derivative check for minima
    # dE/dr = 0 and d2E/dr2 > 0
    
    # Smooth slightly
    # energies_smooth = np.convolve(energies, np.ones(3)/3, mode='valid')
    # r_smooth = r_scan[1:-1]
    
    plt.figure(figsize=(10, 6))
    plt.plot(r_scan, energies, 'k-', lw=2, label='Effective Energy E(r)')
    
    # Highlight stable radii found in Q1
    stable_radii = [3.5, 7.1] # Approximate from Q1
    for sr in stable_radii:
        theta = analyzer.construct_dipole(sr)
        e_val = analyzer.calculate_energy(theta)
        plt.plot(sr, e_val, 'ro', ms=10, label=f'Stable Orbit r={sr}')
        
    plt.xlabel('Dipole Separation r')
    plt.ylabel('Effective Energy (XY Hamiltonian)')
    plt.title('Emergent Quantization: Energy Landscape')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig("l2_6_energy_landscape.png")
    
    # Save Data
    results = {
        'r': r_scan.tolist(),
        'E': energies.tolist(),
        'stable_candidates': stable_radii
    }
    with open("l2_6_energy_levels.json", 'w') as f:
        json.dump(results, f, indent=2)
        
    print("Energy Scan Complete.")

if __name__ == "__main__":
    run_energy_scan()
