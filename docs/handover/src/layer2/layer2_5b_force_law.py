"""
L2.5b Branch B2: Robust Force Law Statistics
============================================
Performs high-statistics measurement of effective force law between vortices.
Uses Topological Detector (L2.5b/B1) for robust tracking.
"""

import numpy as np
import matplotlib.pyplot as plt
import json
import joblib
from pathlib import Path
from tqdm import tqdm
from scipy.optimize import curve_fit

# Import L2.5b Detector
try:
    from l2_5b_vortex_detector import detect_vortices
except ImportError:
    print("Error: l2_5b_vortex_detector not found.")
    import sys
    sys.exit(1)

# ============================================================================
# SIMULATOR (Self-Contained for reproducibility)
# ============================================================================

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
        # 5-point smoothing
        n_up = np.roll(self.nodes, 1, axis=0)
        n_down = np.roll(self.nodes, -1, axis=0)
        n_left = np.roll(self.nodes, 1, axis=1)
        n_right = np.roll(self.nodes, -1, axis=1)
        local_sum = self.nodes + n_up + n_down + n_left + n_right
        local_mean = local_sum / 5.0
        theta = np.arctan2(local_mean[:,:,1], local_mean[:,:,0])
        return theta # Return just phase for detector

    def init_pair(self, sep, q1, q2):
        cx, cy = self.nx / 2.0, self.ny / 2.0
        y, x = np.mgrid[0:self.ny, 0:self.nx]
        z = np.ones((self.ny, self.nx), dtype=complex)
        
        # V1
        dx1 = (x - (cx - sep/2) + self.nx/2) % self.nx - self.nx/2
        dy1 = (y - cy + self.ny/2) % self.ny - self.ny/2
        r1 = np.sqrt(dx1**2 + dy1**2)
        z *= np.tanh(r1/2.0) * np.exp(1j * q1 * np.arctan2(dy1, dx1))
        
        # V2
        dx2 = (x - (cx + sep/2) + self.nx/2) % self.nx - self.nx/2
        dy2 = (y - cy + self.ny/2) % self.ny - self.ny/2
        r2 = np.sqrt(dx2**2 + dy2**2)
        z *= np.tanh(r2/2.0) * np.exp(1j * q2 * np.arctan2(dy2, dx2))
        
        # Set
        self.nodes[:,:,0] = np.real(z) # Simplified projection
        self.nodes[:,:,1] = np.imag(z)
        self.nodes[:,:,2] = 0.1 # Small z-component
        self.normalize()

# ============================================================================
# TRACKING & MEASUREMENT
# ============================================================================

def track_distance(sim, steps=80):
    dist_history = []
    
    for t in range(steps):
        sim.step()
        if t % 2 == 0: # Sample every 2 steps
            theta = sim.get_phi()
            res = detect_vortices(theta)
            
            # Simple 2-particle tracking
            coords = res['coords_plus'] + res['coords_minus']
            
            # Should have 2
            if len(coords) >= 2:
                # Take first 2 (assuming they are limits of initial ones)
                # Or find closest to center?
                # Usually cleanest 2 work.
                c1 = np.array(coords[0])
                c2 = np.array(coords[1])
                
                dx = abs(c1[1] - c2[1]) # x is col index (1), y is row (0)
                dy = abs(c1[0] - c2[0])
                
                if dx > sim.nx/2: dx = sim.nx - dx
                if dy > sim.ny/2: dy = sim.ny - dy
                
                d = np.sqrt(dx**2 + dy**2)
                dist_history.append(d)
            else:
                dist_history.append(np.nan) # Clean miss
                
    return np.array(dist_history)

def calculate_initial_acceleration(dist_trace, dt_step=2.0):
    # Fit parabola to first K points -> d(t) = d0 + v0*t + 0.5*a*t^2
    # Or just d'' numerical
    
    # Filter NaNs
    valid = dist_trace[~np.isnan(dist_trace)]
    if len(valid) < 10: return None
    
    # Take first 20 points (short time)
    y = valid[:15]
    x = np.arange(len(y)) * dt_step
    
    if len(y) < 5: return None
    
    # Quadratic fit
    coeffs = np.polyfit(x, y, 2) # [0.5*a, v0, d0]
    acc = coeffs[0] * 2.0
    
    return acc

# ============================================================================
# MAIN EXPERIMENT
# ============================================================================

def run_experiment():
    r_vals = list(range(4, 25, 2)) # 4, 6, ..., 24
    n_seeds = 20
    results_dir = Path("results/l2_5b")
    results_dir.mkdir(exist_ok=True, parents=True)
    
    all_data = {'VV': [], 'VA': []}
    
    params = {'VV': (1,1), 'VA': (1,-1)}
    
    for pair_type, (q1, q2) in params.items():
        print(f"Running {pair_type} sweep...")
        
        for r0 in tqdm(r_vals, desc=f"{pair_type} Distance"):
            for seed in range(n_seeds):
                sim = SimEngine(size=128, seed=seed)
                sim.init_pair(r0, q1, q2)
                
                trace = track_distance(sim)
                acc = calculate_initial_acceleration(trace)
                
                if acc is not None:
                    # Store (r, a)
                    # Use actual measured initial distance? Or r0. 
                    # r0 is cleaner for plot X-axis.
                    # But measured d0 might vary slightly. Let's use r0.
                    all_data[pair_type].append({
                        'r0': r0,
                        'acc': acc,
                        'seed': seed
                    })
                    
    # Save Data
    with open(results_dir / "l2_5b_force_data_raw.json", 'w') as f:
        json.dump(all_data, f, indent=2)
        
    # Fit & Plot
    fit_results = {}
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Log model: log(|a|) = log(k*r^alpha) = log(k) + alpha*log(r)
    
    for i, ptype in enumerate(['VV', 'VA']):
        data = [d for d in all_data[ptype] if d['acc'] is not None]
        if not data: continue
        
        rs = np.array([d['r0'] for d in data])
        # Acceleration direction: VV repel (a>0), VA attract (a<0).
        # We take abs(a) for log plot.
        accs = np.array([d['acc'] for d in data])
        
        # Check expected sign
        if ptype == 'VV':
            # Repulsion -> acc > 0
            mask = accs > 0
        else:
            # Attraction -> acc < 0
            mask = accs < 0
            
        rs_clean = rs[mask]
        accs_clean = np.abs(accs[mask])
        
        # Log-Log Fit
        if len(rs_clean) > 5:
            log_r = np.log(rs_clean)
            log_a = np.log(accs_clean)
            
            # Linear Fit
            pOpt, pCov = np.polyfit(log_r, log_a, 1, cov=True)
            alpha = pOpt[0]
            log_k = pOpt[1]
            k = np.exp(log_k)
            alpha_err = np.sqrt(pCov[0,0])
            
            fit_results[ptype] = {
                'alpha': alpha,
                'alpha_err': alpha_err,
                'k': k
            }
            
            # Plot
            ax = axes[i]
            ax.scatter(rs_clean, accs_clean, alpha=0.3, label='Data')
            
            # Plot Fit Line
            r_fit = np.linspace(min(rs_clean), max(rs_clean), 100)
            a_fit = k * (r_fit ** alpha)
            ax.plot(r_fit, a_fit, 'r--', label=f"Fit: a ~ r^{{{alpha:.2f}}}")
            
            ax.set_xscale('log')
            ax.set_yscale('log')
            ax.set_xlabel("Distance r")
            ax.set_ylabel("Acceleration |a|")
            ax.set_title(f"{ptype} Force Law (Exp = {alpha:.3f} ± {alpha_err:.3f})")
            ax.legend()
            ax.grid(True, which="both", ls="-", alpha=0.2)
            
    plt.tight_layout()
    plt.savefig(results_dir / "l2_5b_force_law_loglog.png")
    
    # Save Stats
    with open(results_dir / "l2_5b_force_law_stats.json", 'w') as f:
        json.dump(fit_results, f, indent=2)
        
    print("Completed B2 Force Law Analysis.")
    print(json.dumps(fit_results, indent=2))

if __name__ == "__main__":
    run_experiment()
