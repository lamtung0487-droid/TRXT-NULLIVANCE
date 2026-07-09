"""
L2.6 Branch Q1: Orbit Stability Sweep (The Quantization Hunt)
=============================================================
Tests if V-A bound states settle into discrete orbits or continuous ones.
"""

import numpy as np
import matplotlib.pyplot as plt
import json
import sys
from pathlib import Path
from tqdm import tqdm

# Add L2.5 path for detector
l2_5_path = Path(__file__).parent.parent / "L2_5_interaction_laws"
sys.path.append(str(l2_5_path))

try:
    from l2_5b_vortex_detector import detect_vortices
except ImportError:
    print("Error: Could not import l2_5b_vortex_detector. checks paths.")
    sys.exit(1)

# ============================================================================
# SIMULATION ENGINE
# ============================================================================

class SimEngine:
    def __init__(self, size=64, seed=42, alpha=0.1):
        self.nx = size
        self.ny = size
        self.rng = np.random.RandomState(seed)
        self.alpha = alpha
        self.dim = 3
        # Init Vacuum
        self.nodes = np.zeros((self.ny, self.nx, self.dim))
        self.nodes[:, :, 0] = 1.0 
        self.nodes += 0.01 * self.rng.randn(self.ny, self.nx, self.dim)
        self.normalize()
        
    def normalize(self):
        norms = np.linalg.norm(self.nodes, axis=2, keepdims=True)
        self.nodes /= (norms + 1e-9)
        
    def step(self):
        # Consensus dynamics (Nullivance)
        n_up = np.roll(self.nodes, 1, axis=0)
        n_down = np.roll(self.nodes, -1, axis=0)
        n_left = np.roll(self.nodes, 1, axis=1)
        n_right = np.roll(self.nodes, -1, axis=1)
        neighbor_sum = n_up + n_down + n_left + n_right
        # Update: Move towards average
        self.nodes = (1 - self.alpha) * self.nodes + (self.alpha/4.0) * neighbor_sum
        self.normalize()
        
    def get_phi(self):
        # 5-point smoothing for phase extraction
        n_up = np.roll(self.nodes, 1, axis=0)
        n_down = np.roll(self.nodes, -1, axis=0)
        n_left = np.roll(self.nodes, 1, axis=1)
        n_right = np.roll(self.nodes, -1, axis=1)
        local_sum = self.nodes + n_up + n_down + n_left + n_right
        local_mean = local_sum / 5.0
        theta = np.arctan2(local_mean[:,:,1], local_mean[:,:,0])
        return theta

    def init_dipole(self, r0):
        # Initialize V-A pair at distance r0, centered
        # No forcing, let them evolve from this config
        cx, cy = self.nx / 2.0, self.ny / 2.0
        y, x = np.mgrid[0:self.ny, 0:self.nx]
        z = np.ones((self.ny, self.nx), dtype=complex)
        
        # V (+1) at -r0/2
        dx1 = (x - (cx - r0/2) + self.nx/2) % self.nx - self.nx/2
        dy1 = (y - cy + self.ny/2) % self.ny - self.ny/2
        r1 = np.sqrt(dx1**2 + dy1**2)
        z *= np.tanh(r1/2.0) * np.exp(1j * (+1) * np.arctan2(dy1, dx1))
        
        # A (-1) at +r0/2
        dx2 = (x - (cx + r0/2) + self.nx/2) % self.nx - self.nx/2
        dy2 = (y - cy + self.ny/2) % self.ny - self.ny/2
        r2 = np.sqrt(dx2**2 + dy2**2)
        z *= np.tanh(r2/2.0) * np.exp(1j * (-1) * np.arctan2(dy2, dx2))
        
        self.nodes[:,:,0] = np.real(z)
        self.nodes[:,:,1] = np.imag(z)
        self.nodes[:,:,2] = 0.1
        self.normalize()

# ============================================================================
# SWEEP LOGIC
# ============================================================================

def get_distance(sim):
    phi = sim.get_phi()
    res = detect_vortices(phi)
    
    # Ideally 1+ and 1-
    coords_p = res['coords_plus']
    coords_m = res['coords_minus']
    
    if len(coords_p) >= 1 and len(coords_m) >= 1:
        c1 = np.array(coords_p[0])
        c2 = np.array(coords_m[0])
        
        dx = abs(c1[0] - c2[0]) # x
        dy = abs(c1[1] - c2[1]) # y
        
        if dx > sim.nx/2: dx = sim.nx - dx
        if dy > sim.ny/2: dy = sim.ny - dy
        
        return np.sqrt(dx**2 + dy**2)
    return None

def run_sweep():
    # Parameters
    r_min = 3.0
    r_max = 12.0
    r_step = 0.1 # Fine resolution
    r_values = np.arange(r_min, r_max + 0.001, r_step)
    
    n_seeds = 3 # Repeats per r0 to check stability
    T_max = 500 # Long run
    
    results = [] # {r0, seed, final_r, r_trace}
    
    print(f"Starting Quantization Hunt: r=[{r_min}, {r_max}], step={r_step}")
    
    for r0 in tqdm(r_values, desc="Sweeping r0"):
        for seed in range(n_seeds):
            sim = SimEngine(size=64, seed=seed)
            sim.init_dipole(r0)
            
            trace = []
            
            for t in range(T_max):
                sim.step()
                if t > 400: # Only record late time behavior
                    if t % 2 == 0:
                        d = get_distance(sim)
                        if d is not None:
                            trace.append(d)
                
                # Check annihilation early
                if t % 50 == 0 and t < 400:
                   d = get_distance(sim)
                   if d is not None and d < 2.0:
                       # Annihilated
                       break
            
            final_r = np.nan
            if len(trace) > 10:
                final_r = np.mean(trace)
                
            results.append({
                'r0': float(r0),
                'seed': seed,
                'final_r': float(final_r) if not np.isnan(final_r) else None
            })
            
    # Save Raw
    with open("l2_6_orbital_spectrum.json", 'w') as f:
        json.dump(results, f, indent=2)
        
    plot_spectrum(results)

def plot_spectrum(results):
    import pandas as pd
    df = pd.DataFrame(results)
    df = df.dropna()
    
    if df.empty:
        print("No stable orbits found!")
        return

    # 1. Scatter Plot: r_final vs r_initial
    plt.figure(figsize=(10, 6))
    plt.scatter(df['r0'], df['final_r'], alpha=0.5, c='blue', s=20)
    plt.plot([0, 12], [0, 12], 'k--', alpha=0.3, label='Identifier y=x')
    plt.xlabel('Initial Distance (r0)')
    plt.ylabel('Final Stable Distance (r_final)')
    plt.title('Orbit Quantization Test: Stability Map')
    plt.grid(True, which='both', alpha=0.3)
    plt.savefig("l2_6_orbit_stability_map.png")
    
    # 2. Histogram of Final Radii
    plt.figure(figsize=(10, 6))
    plt.hist(df['final_r'], bins=50, color='purple', alpha=0.7, edgecolor='black')
    plt.xlabel('Final Radius')
    plt.ylabel('Count')
    plt.title('Orbital Spectrum: Search for Discrete Peaks')
    plt.grid(True, alpha=0.3)
    plt.savefig("l2_6_orbit_histogram.png")
    
    # Check for steps/plateaus
    # If quantized, histogram should have sharp peaks at R1, R2, R3...
    print("Plots saved.")

if __name__ == "__main__":
    run_sweep()
