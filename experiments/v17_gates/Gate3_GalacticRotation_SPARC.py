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
    print("--- GATE 3: THE ROTATION VALID (SPARC, held-out protocol) ---")
    # Repo-relative data path (run from repo root); fixed hardcoded path 2026-07-09
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            "../../data/sparc/Rotmod_LTG"))
    files = sorted(glob.glob(os.path.join(data_dir, "*_rotmod.dat")))

    if not files:
        print(f"ERROR: No data files found in {data_dir}")
        return 2

    # Global Optimization of a0
    # We want to find the single a0 that minimizes TOTAL Chi2 across all galaxies
    # while allowing M/L ratios to vary per galaxy.
    
    def global_loss(a0_val, dataset):
        total_chi2_for_a0 = 0
        total_dof = 0

        # We can re-use the Galaxy Loop logic here
        # For efficiency, we pre-load data once (moved outside this func)

        for g_data in dataset:
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

    # --- Held-out protocol (lab gate-integrity fix, 2026-07-09) ---
    # The universal a0 is FITTED on the training half only (alphabetical
    # even indices) and the gate is scored on the untouched test half.
    # Split rule and PASS criterion (test chi2_red < 5.0) are pre-declared.
    train = preloaded_data[0::2]
    test = preloaded_data[1::2]
    print(f"  Split: {len(train)} train / {len(test)} test galaxies (alphabetical even/odd)")

    print(f"  Fitting global a0 on TRAIN half (grid 2800-3800, extended)...")
    best_a0 = 3500.0
    min_train_chi2 = 1e9
    scan_range = np.linspace(2800, 3800, 21)  # extended (a0 hit old grid edge; logged)
    for val in scan_range:
        chi2_val = global_loss(val, train)
        print(f"    a0={val:.1f} -> Train Chi2={chi2_val:.4f}")
        if chi2_val < min_train_chi2:
            min_train_chi2 = chi2_val
            best_a0 = val
    print(f"  Best a0 (train): {best_a0:.1f} with Train Chi2={min_train_chi2:.4f}")

    # Score once on the held-out half with a0 frozen
    test_rchi2 = global_loss(best_a0, test)

    print("\n[Gate 3 Results - Held-Out Validation]")
    print(f"  a0 (fitted on train): {best_a0:.1f}")
    print(f"  Train Reduced Chi2:   {min_train_chi2:.4f}")
    print(f"  TEST  Reduced Chi2:   {test_rchi2:.4f}   <- gate metric")

    if test_rchi2 < 5.0:
        print("\n>>> GATE 3 STATUS: PASS (held-out chi2_red < 5.0) <<<")
        rc = 0
    else:
        print("\n>>> GATE 3 STATUS: FAIL (held-out chi2_red >= 5.0) <<<")
        rc = 1

    # Create dummy plot for artifact compatibility
    plt.figure()
    plt.text(0.5, 0.5, f"a0 (train): {best_a0}\nTest Chi2: {test_rchi2:.4f}", ha='center')
    plt.savefig("results/figures/sparc_opt_hist.png")
    return rc

if __name__ == "__main__":
    run_sparc_analysis()
