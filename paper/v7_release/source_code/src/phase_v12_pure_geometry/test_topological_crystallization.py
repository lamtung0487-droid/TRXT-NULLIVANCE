import numpy as np
import matplotlib.pyplot as plt

# TRXT V6 Topological Crystallization Test
# ----------------------------------------
# Simulates the "Freeze-out" of Topological Defects during a Phase Transition.
# Hypothesis: As "Logic Temperature" drops (percolation probability p increases),
# clusters form, trapping vortices (winding numbers) inside.

def calculate_winding(phase_grid, r, c, loop_size=2):
    """
    Calculates winding number around a loop at (r, c).
    Uses discrete phase differences.
    """
    h, w = phase_grid.shape
    winding = 0.0
    
    # Define loop path (small square)
    path = [
        (r, c), (r, c+1),
        (r+1, c+1), (r+1, c),
        (r, c) # Close loop
    ]
    
    for i in range(len(path)-1):
        y1, x1 = path[i]
        y2, x2 = path[i+1]
        
        # Periodic BCs for torus topology
        y1 %= h; x1 %= w; y2 %= h; x2 %= w
        
        p1 = phase_grid[y1, x1]
        p2 = phase_grid[y2, x2]
        
        diff = p2 - p1
        # Normalize to [-pi, pi]
        while diff > np.pi: diff -= 2*np.pi
        while diff < -np.pi: diff += 2*np.pi
        
        winding += diff
        
    return winding / (2*np.pi)

def lattice_simulation(size=50, cooling_steps=20):
    print(f"--- Simulating Topological Crystallization (Lattice {size}x{size}) ---")
    
    # 1. State 0: Hot Foam (Random Phases)
    # ------------------------------------
    phases = np.random.uniform(-np.pi, np.pi, (size, size))
    temperatures = np.linspace(2.0, 0.1, cooling_steps) # Logic Temp
    
    defect_counts = []
    
    for T in temperatures:
        # Metropolis-Hastings / Relaxation Step (Simulate 'Time' Flow)
        # Minimize local gradient energy E ~ (grad phi)^2
        new_phases = np.copy(phases)
        for _ in range(5): # Relaxation iterations per temp step
            for r in range(size):
                for c in range(size):
                    # Neighbors
                    neighbors = []
                    for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                        ny, nx = (r+dr)%size, (c+dc)%size
                        neighbors.append(phases[ny,nx])
                    
                    # Local 'mean field' alignment (Ferromagnetic/Superfluid order)
                    avg_sin = np.mean(np.sin(neighbors))
                    avg_cos = np.mean(np.cos(neighbors))
                    target_angle = np.arctan2(avg_sin, avg_cos)
                    
                    # Thermal Noise
                    noise = np.random.normal(0, T)
                    new_phases[r,c] = target_angle + noise
        
        phases = new_phases
        
        # Detect Defects (Vortices)
        vortices = 0
        antivortices = 0
        for r in range(size):
            for c in range(size):
                w = calculate_winding(phases, r, c)
                if abs(w - 1.0) < 0.1: vortices += 1
                if abs(w + 1.0) < 0.1: antivortices += 1
        
        total_defects = vortices + antivortices
        defect_counts.append(total_defects)
        print(f"Temp {T:.2f}: {total_defects} defects trapped.")

    return temperatures, defect_counts, phases

def main():
    temps, defect_counts, final_map = lattice_simulation(size=64, cooling_steps=15)
    
    # Analysis
    # --------
    # Expectation: Kibble-Zurek Mechanism
    # Defect density should drop as Correlation Length increases (lower T)
    # But some should remain 'frozen' due to topology.
    
    print("\nFinal State Analysis:")
    print(f"Residual Defects: {defect_counts[-1]}")
    if defect_counts[-1] > 0:
        print("SUCCESS: Topology successfully trapped defects (Particles)!")
    else:
        print("WARNING: All defects annealed out (Need faster quench or topology constraint).")
    
    # Plot
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(temps, defect_counts, 'o-')
    plt.gca().invert_xaxis() # High T to Low T
    plt.xlabel("Logic Temperature (Noise)")
    plt.ylabel("Number of Topological Defects")
    plt.title("Defect Freeze-out (Crystallization)")
    plt.grid(True)
    
    plt.subplot(1, 2, 2)
    plt.imshow(final_map, cmap='hsv')
    plt.colorbar(label='Phase Angle')
    plt.title("Final Condensate Phase Map")
    
    plt.tight_layout()
    plt.savefig("topological_crystallization.png")
    print("Saved plot to topological_crystallization.png")

if __name__ == "__main__":
    main()
