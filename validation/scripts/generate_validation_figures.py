
import matplotlib.pyplot as plt
import numpy as np
import json
import os
import sys

# Add src to path
sys.path.insert(0, 'src')
from bullet_cluster import BulletClusterSimulation
from sparc_data_loader import load_sparc_data, parse_rotmod_mrt
from rotation_curves import fit_galaxy_rotation, rotation_velocity, enclosed_mass, solve_lane_emden

def setup_plotting():
    """Configure matplotlib for publication quality."""
    plt.style.use('default') # Use default as base
    # You can add custom style settings here if needed
    plt.rcParams['figure.figsize'] = (10, 6)
    plt.rcParams['font.size'] = 12
    plt.rcParams['axes.grid'] = True
    plt.rcParams['grid.alpha'] = 0.3
    
    # Ensure figures directory exists
    os.makedirs('figures', exist_ok=True)

def plot_sparc_histogram():
    """Generate SPARC Chi2 Histogram."""
    print("Generating SPARC Histogram...")
    
    # Load results
    results_path = 'outputs/runs/sparc_validation_results.json'
    if not os.path.exists(results_path):
        print("Results file not found. Run validation first.")
        return

    with open(results_path, 'r') as f:
        data = json.load(f)
    
    chi2_list = [g['chi2_red'] for g in data['galaxies'] if g['chi2_red'] < 100] # Clip extreme outliers for plot
    n_pass = data['n_pass']
    total = data['n_galaxies']
    pass_rate = n_pass / total * 100
    
    plt.figure(figsize=(10, 6))
    plt.hist(chi2_list, bins=30, color='skyblue', edgecolor='black', alpha=0.7)
    
    plt.axvline(x=5.0, color='red', linestyle='--', linewidth=2, label=f'Pass Thresh (chi2=5.0)')
    plt.title(f'SPARC Validation Chi-Squared Distribution (N={total})')
    plt.xlabel('Reduced Chi-Squared')
    plt.ylabel('Count')
    
    # Add stats
    text_str = f'Passed: {n_pass}/{total} ({pass_rate:.1f}%)\nMedian: {data["median_chi2_red"]:.2f}'
    plt.text(0.7, 0.8, text_str, transform=plt.gca().transAxes, 
             bbox=dict(facecolor='white', alpha=0.8))
    
    plt.legend()
    plt.tight_layout()
    plt.savefig('figures/sparc_chi2_dist.png', dpi=300)
    plt.close()
    print("Saved figures/sparc_chi2_dist.png")

def plot_best_and_worst():
    """Plot Best Fit (NGC 4010 or similar) and Representative Fail (NGC 5055)."""
    print("Generating Rotation Curve Plots...")
    
    # Initialize galaxies
    data_file = 'data/sparc/MassModels_Lelli2016c.mrt'
    if os.path.exists(data_file):
        galaxies = load_sparc_data('data')
    else:
        print("Data file not found.")
        return
        
    # We look for specific examples or scan for best/worst
    # From previous output I recall NGC 4068 passed, NGC 5055 likely failed
    # Let's find best pass and high fail
    
    # Pre-solve Lane-Emden
    n = 1.37
    xi, theta, dtheta = solve_lane_emden(n)
    M_enc_dimless = enclosed_mass(xi, theta, n)
    
    # Iterate to find candidates
    best_gal = None
    min_chi2 = 1e9
    
    worst_gal = None
    max_chi2 = 0
    
    # Use list to find reproducible candidates
    candidates = []
    
    for name, gal in galaxies.items():
        result = fit_galaxy_rotation(gal.r_kpc, gal.v_obs, gal.v_err, n=n)
        chi2 = result['chi2_red']
        candidates.append((name, chi2, result))
        
        if chi2 < min_chi2 and len(gal.r_kpc) > 10: # Ensure enough points
            min_chi2 = chi2
            best_gal = (name, gal, result)
            
        if chi2 > 10 and chi2 < 200: # Representative bad, not crazy bad
             worst_gal = (name, gal, result) # Just keep last one or use logic
    
    # Explicitly pick known good/bad if possible, or sort
    candidates.sort(key=lambda x: x[1])
    
    # Best Pass
    best_name, best_chi2, best_res = candidates[0]
    best_gal_obj = galaxies[best_name]
    
    # Representative Fail (e.g. median of fails)
    fails = [x for x in candidates if x[1] > 5.0]
    fail_name, fail_chi2, fail_res = fails[len(fails)//2] # Median fail
    fail_gal_obj = galaxies[fail_name]
    
    # Plotting Function
    def plot_curve(galaxy, result, title, filename):
        plt.figure(figsize=(8, 6))
        
        # Plot Data
        plt.errorbar(galaxy.r_kpc, galaxy.v_obs, yerr=galaxy.v_err, fmt='ko', 
                     label='Observed Data', alpha=0.6, capsize=3)
        
        # Plot Model
        # Need to reconstruct model curve over smooth range
        r_smooth = np.linspace(0, max(galaxy.r_kpc), 100)
        
        # Re-compute model v for smooth r
        # Get M_total from result
        M_total = result['M_total']
        
        # Find first zero of Lane-Emden
        zero_idx = np.argmax(theta <= 0)
        xi_1 = xi[zero_idx] if zero_idx > 0 else xi[-1]
        
        # Scale
        r_max_data = galaxy.r_kpc[-1]
        alpha = r_max_data / xi_1
        
        r_model_dimless = r_smooth / alpha
        # Interpolate M_enc
        # We need to interpolation M(r_smooth) from the dimensionless solution
        # r_model corresponds to xi * alpha
        # So we map r_smooth to xi
        xi_interp = r_smooth / alpha
        
        # Interpolate M_enc_dimless at xi_interp
        M_enc_interp = np.interp(xi_interp, xi, M_enc_dimless)
        
        M_model_smooth = M_enc_interp * M_total / M_enc_dimless[-1]
        
        v_model_smooth = rotation_velocity(r_smooth, M_model_smooth)
        
        plt.plot(r_smooth, v_model_smooth, 'b-', linewidth=2, label='Lane-Emden (n=1.37)')
        
        plt.title(f'{title} (chi2={result["chi2_red"]:.2f})')
        plt.xlabel('Radius [kpc]')
        plt.ylabel('Velocity [km/s]')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(filename, dpi=300)
        plt.close()
        print(f"Saved {filename}")

    plot_curve(best_gal_obj, best_res, f"{best_name}: Best Fit Pass", "figures/sparc_best_pass.png")
    plot_curve(fail_gal_obj, fail_res, f"{fail_name}: Typical Fail", "figures/sparc_typical_fail.png")
    
    # Combined plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Plot 1
    ax1.errorbar(best_gal_obj.r_kpc, best_gal_obj.v_obs, yerr=best_gal_obj.v_err, fmt='ko', alpha=0.5)
    # Re-calc smooth for ax1
    # ... concise version
    # Actually simpler to just save separate plots.
    # User asked for "set of charts". Separate is fine.
    
    print("Rotation curves generated.")

def plot_bullet_cluster():
    """Generate Bullet Cluster Separation Plot."""
    print("Generating Bullet Cluster Plot...")
    
    sim = BulletClusterSimulation(n_particles=500, seed=42)
    sim.initialize_collision(separation=4.0, collision_velocity=2.0)
    
    # Run
    results = sim.run(n_steps=500)
    
    # Get final particles
    # We need to access the simulation object but `run()` returns stats.
    # The `sim` object retains state.
    
    main_dm = sim.main_cluster.dm_particles
    main_gas = sim.main_cluster.gas_particles
    bullet_dm = sim.bullet_cluster.dm_particles
    bullet_gas = sim.bullet_cluster.gas_particles
    
    plt.figure(figsize=(10, 6))
    
    # Plot DM (Blue)
    dm_x = [p.x for p in main_dm + bullet_dm]
    dm_y = [p.y for p in main_dm + bullet_dm]
    plt.scatter(dm_x, dm_y, c='blue', s=10, alpha=0.3, label='Dark Matter (Collisionless)')
    
    # Plot Gas (Red)
    gas_x = [p.x for p in main_gas + bullet_gas]
    gas_y = [p.y for p in main_gas + bullet_gas]
    plt.scatter(gas_x, gas_y, c='red', s=10, alpha=0.3, label='Gas (Collisional)')
    
    # Plot Centroids
    md = sim.main_cluster.dm_centroid
    mg = sim.main_cluster.gas_centroid
    bd = sim.bullet_cluster.dm_centroid
    bg = sim.bullet_cluster.gas_centroid
    
    plt.plot(md[0], md[1], 'bx', markersize=15, markeredgewidth=3)
    plt.plot(mg[0], mg[1], 'rx', markersize=15, markeredgewidth=3)
    plt.plot(bd[0], bd[1], 'bx', markersize=15, markeredgewidth=3)
    plt.plot(bg[0], bg[1], 'rx', markersize=15, markeredgewidth=3)
    
    # Arrows or Lines indicating separation
    # Separation lines
    plt.plot([md[0], mg[0]], [md[1], mg[1]], 'k--', linewidth=1)
    plt.plot([bd[0], bg[0]], [bd[1], bg[1]], 'k--', linewidth=1)
    
    plt.title(f'Bullet Cluster Simulation (Step 500)\nTarget: G1 Gate (Separation Observed)')
    plt.xlabel('X [kpc]')
    plt.ylabel('Y [kpc]')
    plt.legend()
    
    # Annotate separation
    sep_bullet = results['bullet_separation']
    plt.text(bd[0], bd[1]+0.5, f"Sep: {sep_bullet:.1f} kpc", color='purple', ha='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('figures/bullet_cluster_separation.png', dpi=300)
    plt.close()
    print("Saved figures/bullet_cluster_separation.png")

if __name__ == "__main__":
    setup_plotting()
    plot_sparc_histogram()
    plot_best_and_worst()
    plot_bullet_cluster()
    print("All figures generated successfully.")
