import os
import glob
import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt

# Constants
G = 4.301e-6 # kpc km^2/s^2 M_sun^-1

def load_galaxy_data(filepath):
    """Parses SPARC .dat file."""
    data = []
    try:
        with open(filepath, 'r') as f:
            for line in f:
                if line.startswith("#"): continue
                parts = line.split()
                if len(parts) < 6: continue
                try:
                    # Rad(kpc), Vobs, errV, Vgas, Vdisk, Vbul
                    R = float(parts[0])
                    Vobs = float(parts[1])
                    errV = float(parts[2])
                    Vgas = float(parts[3])
                    Vdisk = float(parts[4])
                    Vbul = float(parts[5])
                    data.append([R, Vobs, errV, Vgas, Vdisk, Vbul])
                except ValueError:
                    continue
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None
        
    return np.array(data)

def solve_field_equation(g_bar, a0):
    # Standard MOND form: mu(x) = x / sqrt(1+x^2)
    # Emerges from P(X) ~ X^3? No, specific resummation.
    # Root: g^4 - g_N^2 g^2 - g_N^2 a0^2 = 0
    # g^2 = (g_N^2 + sqrt(g_N^4 + 4 g_N^2 a0^2)) / 2
    
    # Numerical stability
    term = np.sqrt(g_bar**4 + 4.0 * g_bar**2 * a0**2)
    g2 = (g_bar**2 + term) / 2.0
    g_tot = np.sqrt(g2)
    return g_tot

def run_sparc_analysis():
    print("--- GATE 3: THE ROTATION VALID (SPARC) ---")
    data_dir = r"C:\Users\NC\Music\trxt nullivance v14\data\sparc\Rotmod_LTG"
    files = glob.glob(os.path.join(data_dir, "*_rotmod.dat"))
    
    if not files:
        print(f"ERROR: No data files found in {data_dir}")
        return

    # Global Optimization of a0
    # We want to find the single a0 that minimizes TOTAL Chi2 across all galaxies
    # while allowing M/L ratios to vary per galaxy.
    
    def global_loss(a0_val):
        total_chi2_for_a0 = 0
        total_dof = 0
        
        # We can re-use the Galaxy Loop logic here
        # For efficiency, we pre-load data once (moved outside this func)
        
        for g_data in preloaded_data:
            # Unpack
            R, Vobs, errV, Vgas, Vdisk, Vbul = g_data['data']
            has_bulge = g_data['has_bulge']
            
            # Loss function for this galaxy
            # Params: [Upsilon_disk, Upsilon_bulge, Distance_Factor]
            def loss(params):
                Y_d = params[0]
                if has_bulge:
                    Y_b = params[1]
                    f = params[2]
                else:
                    Y_b = 0.0
                    f = params[1]
                    
                # Physics Scaling Laws for Distance change D_new = f * D_old
                # R_new = f * R_old
                # V_bar_new^2 = f * V_bar_old^2 (since M ~ f^2, R ~ f)
                # g_bar_new = V_bar_new^2 / R_new = (f * V_bar^2) / (f * R) = g_bar (Invariant!)
                
                # Baryonic Newton
                Vbar2_old = Vgas**2 + Y_d * Vdisk**2 + Y_b * Vbul**2
                Vbar2_old = np.maximum(Vbar2_old, 0.0)
                g_bar = Vbar2_old / R # Invariant
                
                # TRXT Field Solve (Standard Form)
                g_tot = solve_field_equation(g_bar, a0_val)
                
                # Prediction
                # V_pred^2 = g_tot * R_new = g_tot * (f * R)
                V_pred = np.sqrt(g_tot * f * R)
                
                # Chi2 Data
                chi2_data = np.sum(((Vobs - V_pred) / errV)**2)
                
                # Chi2 Prior on Distance (15% error standard)
                # We assume SPARC distances are typical estimates with ~15% error
                chi2_prior = ((f - 1.0) / 0.15)**2
                
                return chi2_data + chi2_prior

            # Optimize
            # Y_d, Y_b in [0.2, 1.5], f in [0.7, 1.3] (allow 30% swing but penalized)
            if has_bulge:
                p0 = [0.5, 0.7, 1.0]
                bounds = [(0.2, 2.0), (0.2, 2.0), (0.7, 1.3)]
                res = opt.minimize(loss, p0, bounds=bounds)
            else:
                p0 = [0.5, 1.0]
                bounds = [(0.2, 2.0), (0.7, 1.3)]
                res = opt.minimize(loss, p0, bounds=bounds)
            
            total_chi2_for_a0 += res.fun
            
            # Degrees of freedom: N_data + N_prior - N_parameters
            # N_data = len(R)
            # N_prior = 1 (for distance factor f)
            # N_parameters = 3 (Yd, Yb, f) if has_bulge, else 2 (Yd, f)
            dof = len(R) + 1 - (3 if has_bulge else 2)
            total_dof += max(dof, 1) # Ensure dof is at least 1 to avoid division by zero

        return total_chi2_for_a0 / total_dof

    # 1. Preload Data
    print("  Preloading data for optimization...")
    preloaded_data = []
    for filepath in files:
        gal_name = os.path.basename(filepath).replace("_rotmod.dat", "")
        d = load_galaxy_data(filepath)
        if d is None or len(d) == 0: continue
        
        # Parse columns
        R = d[:, 0]
        Vobs = d[:, 1]
        errV = np.maximum(d[:, 2], 1.0)
        Vgas = np.abs(d[:, 3])
        Vdisk = np.abs(d[:, 4])
        Vbul = np.abs(d[:, 5])
        has_bulge = np.max(Vbul) > 1.0
        
        preloaded_data.append({
            'name': gal_name,
            'data': (R, Vobs, errV, Vgas, Vdisk, Vbul),
            'has_bulge': has_bulge
        })

    print(f"  Starting Global a0 Optimization (Fine-Tuning 3300-3700)...")
    
    best_a0 = 3500.0
    min_global_chi2 = 1e9
    
    # Fine Grid Search
    scan_range = np.linspace(3300, 3700, 9) 
    
    for val in scan_range:
        chi2_val = global_loss(val)
        print(f"    a0={val:.1f} -> Global Chi2={chi2_val:.4f}")
        if chi2_val < min_global_chi2:
            min_global_chi2 = chi2_val
            best_a0 = val
            
    print(f"  Best a0 found: {best_a0:.1f} with Chi2={min_global_chi2:.4f}")
    
    # Final Run with Best a0 to print details
    global_rchi2 = min_global_chi2 # approximate
    results = [] # we could re-run to populate this if needed for CSV
    
    print("\n[Gate 3 Results - Optimized Global a0]")
    print(f"  Optimal a0: {best_a0:.1f}")
    print(f"  Global Reduced Chi2: {global_rchi2:.4f}")
    
    if global_rchi2 < 5.0:
        print("\n>>> GATE 3 STATUS: PASS <<<")
        print("  Superfluid Vacuum fits SPARC Data with Optimal Universal a0.")
    else:
        print("\n>>> GATE 3 STATUS: FAIL <<<")
        print(f"  Chi2 ({global_rchi2:.4f}) still high (>5).")
        print("  The 'Simple' interpolating function might be incorrect.")

    # Create dummy plot for artifact compatibility
    plt.figure()
    plt.text(0.5, 0.5, f"Best a0: {best_a0}\nChi2: {global_rchi2:.4f}", ha='center')
    plt.savefig("sparc_opt_hist.png")

if __name__ == "__main__":
    run_sparc_analysis()
