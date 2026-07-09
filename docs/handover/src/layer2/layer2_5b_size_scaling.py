"""
L2.5b Branch B3: Finite-Size Scaling
====================================
Verifies stability of Topological Gas properties across grid sizes.
"""

import numpy as np
import matplotlib.pyplot as plt
import json
from pathlib import Path
from tqdm import tqdm

try:
    from l2_5b_vortex_detector import detect_vortices
    # Reuse SimEngine logic from B2 if possible, or copy minimal
    # Copying minimal for independence
except ImportError:
    print("Error imports")

class SimEngine:
    def __init__(self, size=128, seed=42, alpha=0.1, is_random=False):
        self.nx = size
        self.ny = size
        self.rng = np.random.RandomState(seed)
        self.alpha = alpha
        self.is_random = is_random
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
        if self.is_random:
            noise = self.alpha * self.rng.randn(self.ny, self.nx, self.dim)
            self.nodes += noise
        else:
            # Consensus
            n_up = np.roll(self.nodes, 1, axis=0)
            n_down = np.roll(self.nodes, -1, axis=0)
            n_left = np.roll(self.nodes, 1, axis=1)
            n_right = np.roll(self.nodes, -1, axis=1)
            neighbor_sum = n_up + n_down + n_left + n_right
            self.nodes = (1 - self.alpha) * self.nodes + (self.alpha/4.0) * neighbor_sum
        self.normalize()
        
    def get_phi(self):
        n_up = np.roll(self.nodes, 1, axis=0)
        n_down = np.roll(self.nodes, -1, axis=0)
        n_left = np.roll(self.nodes, 1, axis=1)
        n_right = np.roll(self.nodes, -1, axis=1)
        local_sum = self.nodes + n_up + n_down + n_left + n_right
        local_mean = local_sum / 5.0
        theta = np.arctan2(local_mean[:,:,1], local_mean[:,:,0])
        return theta
        
    def inject_gas(self, density=1/200.0):
        # N ~ Area * density
        area = self.nx * self.ny
        N = int(area * density)
        if N % 2 != 0: N += 1
        
        print(f"Injecting {N} vortices (Density={density:.4f}) on {self.nx}x{self.ny}")
        
        q_list = [1]*(N//2) + [-1]*(N//2)
        self.rng.shuffle(q_list)
        
        # Simple injection (random pos)
        # Using complex field superposition
        z = np.ones((self.ny, self.nx), dtype=complex)
        y, x = np.mgrid[0:self.ny, 0:self.nx]
        
        positions = []
        for _ in range(N):
            positions.append((self.rng.randint(0, self.nx), self.rng.randint(0, self.ny)))
            
        for (vx, vy), q in zip(positions, q_list):
            dx = (x - vx + self.nx/2) % self.nx - self.nx/2
            dy = (y - vy + self.ny/2) % self.ny - self.ny/2
            r = np.sqrt(dx**2 + dy**2)
            th = q * np.arctan2(dy, dx)
            z *= np.tanh(r/2.0) * np.exp(1j * th)
            
        self.nodes[:,:,0] = np.real(z)
        self.nodes[:,:,1] = np.imag(z)
        self.nodes[:,:,2] = 0.0 # mostly planar
        self.normalize()

def count_stats(phi, size):
    res = detect_vortices(phi)
    plus = res['coords_plus']
    minus = res['coords_minus']
    
    n_total = len(plus) + len(minus)
    
    # Bound pairs?
    # Simple check: fraction of + with a - neighbor < 6.0
    n_bound = 0
    
    # KDTree or brute force (N is small enough usually < 500)
    # Brute force
    used_minus = set()
    
    for px, py in plus:
        # Find closest minus
        min_d = 9999
        best_idx = -1
        
        for i, (mx, my) in enumerate(minus):
            if i in used_minus: continue
            
            dx = abs(px - mx)
            dy = abs(py - my)
            if dx > size/2: dx = size - dx
            if dy > size/2: dy = size - dy
            d = np.sqrt(dx*dx+dy*dy)
            
            if d < min_d:
                min_d = d
                best_idx = i
        
        if min_d < 8.0: # Bound threshold
            n_bound += 1 # Count pairs
            used_minus.add(best_idx)
            
    bound_frac = (n_bound * 2) / n_total if n_total > 0 else 0
    return n_total, bound_frac

def run_scaling():
    sizes = [64, 128, 256]
    n_seeds = 3
    results = []
    
    out_dir = Path("results/l2_5b")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    for size in sizes:
        print(f"Scaling Test: Size {size}...")
        
        density_trace = []
        bound_trace = []
        
        for seed in range(n_seeds):
            sim = SimEngine(size=size, seed=seed)
            sim.inject_gas(density=0.005) # 0.5% density
            
            # Evolve
            for t in range(50):
                sim.step()
                
            # Measure
            phi = sim.get_phi()
            n, b_frac = count_stats(phi, size)
            
            area = size*size
            final_density = n / area
            
            density_trace.append(final_density)
            bound_trace.append(b_frac)
            
        mean_rho = np.mean(density_trace)
        std_rho = np.std(density_trace)
        mean_b = np.mean(bound_trace)
        std_b = np.std(bound_trace)
        
        results.append({
            'size': size,
            'mean_density': mean_rho,
            'std_density': std_rho,
            'mean_bound_frac': mean_b,
            'std_bound_frac': std_b
        })
        
    print(json.dumps(results, indent=2))
    
    with open(out_dir / "l2_5b_size_scaling_stats.json", 'w') as f:
        json.dump(results, f, indent=2)
        
    # Plot
    sizes_arr = [r['size'] for r in results]
    rho = [r['mean_density'] for r in results]
    rho_err = [r['std_density'] for r in results]
    bf = [r['mean_bound_frac'] for r in results]
    bf_err = [r['std_bound_frac'] for r in results]
    
    fig, ax1 = plt.subplots(figsize=(8, 5))
    
    ax1.errorbar(sizes_arr, rho, yerr=rho_err, fmt='bo-', label='Vortex Density')
    ax1.set_xlabel('Grid Size L')
    ax1.set_ylabel('Density (1/pix^2)', color='b')
    ax1.tick_params(axis='y', labelcolor='b')
    ax1.set_ylim(bottom=0)
    
    ax2 = ax1.twinx()
    ax2.errorbar(sizes_arr, bf, yerr=bf_err, fmt='rs-', label='Bound Fraction')
    ax2.set_ylabel('Bound Fraction', color='r')
    ax2.tick_params(axis='y', labelcolor='r')
    ax2.set_ylim(0, 1)
    
    plt.title("Finite-Size Scaling: Gas Properties")
    plt.savefig(out_dir / "l2_5b_size_scaling.png")
    print("Saved Scaling Plot.")

if __name__ == "__main__":
    run_scaling()
