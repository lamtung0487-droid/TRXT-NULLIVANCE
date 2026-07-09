
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import label
from scipy.optimize import curve_fit

def simulate_percolation_and_measure_dimension(L=100, trials=5):
    """
    Simulates site percolation on a 3D lattice at critical probability p_c.
    Measures the Fractal Dimension D_f of the largest cluster.
    
    Standard 3D Site Percolation Threshold p_c ~ 0.3116
    """
    p_c = 0.311607 # Literature value for 3D simple cubic
    
    dimensions = []
    
    print(f"Running {trials} percolation trials on {L}x{L}x{L} lattice...")
    
    for i in range(trials):
        # 1. Generate random lattice
        lattice = np.random.rand(L, L, L) < p_c
        
        # 2. Label clusters
        labeled_array, num_features = label(lattice)
        
        if num_features == 0:
            continue
            
        # 3. Find largest cluster (Giant Component)
        counts = np.bincount(labeled_array.ravel())
        counts[0] = 0 # Ignore background
        largest_cluster_id = np.argmax(counts)
        largest_cluster_mask = (labeled_array == largest_cluster_id)
        
        # 4. Measure Fractal Dimension via Sandbox Method (Ensemble Average)
        # Choosing random points ON the cluster as centers is crucial for fractal dimension
        coords = np.argwhere(largest_cluster_mask)
        n_centers = min(50, len(coords))
        center_indices = np.random.choice(len(coords), n_centers, replace=False)
        centers = coords[center_indices]
        
        # Radii to probe (limited by L/2 to avoid lattice boundary)
        max_r = L // 4 
        radii = np.unique(np.logspace(0, np.log10(max_r), 15).astype(int))
        radii = radii[radii > 0]
        
        avg_masses = np.zeros(len(radii))
        
        for i_c, center in enumerate(centers):
            # Calculate distances from this center to ALL cluster points
            # Optimization: Pre-filter points in a bounding box if huge, but for L=128 numpy is fast enough
            dists = np.linalg.norm(coords - center, axis=1)
            
            row_masses = []
            for r in radii:
                m = np.sum(dists <= r)
                row_masses.append(m)
            avg_masses += np.array(row_masses)
            
        avg_masses /= n_centers
        
        # Fit M(R) ~ R^D
        valid = avg_masses > 0
        log_r = np.log(radii[valid])
        log_m = np.log(avg_masses[valid])
        
        slope, intercept = np.polyfit(log_r, log_m, 1)
        dimensions.append(slope)
        print(f"Trial {i+1}: D_f = {slope:.4f} (Sandbox Method)")
        
    avg_dimension = np.mean(dimensions)
    std_dimension = np.std(dimensions)
    
    print(f"\nFinal Result: D_f = {avg_dimension:.4f} +/- {std_dimension:.4f}")
    print(f"Target TRXT Value (Hypothesis): 2.50")
    print(f"Standard Percolation Value (Literature): ~2.53")
    
    return avg_dimension, std_dimension

if __name__ == "__main__":
    simulate_percolation_and_measure_dimension(L=128, trials=3)
