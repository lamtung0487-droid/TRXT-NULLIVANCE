import numpy as np
import matplotlib.pyplot as plt

def get_k2_grid(N, L):
    """ Fourier space k^2 grid """
    freq = np.fft.fftfreq(N, d=L/N)
    kx, ky = np.meshgrid(freq, freq)
    k2 = (2*np.pi*kx)**2 + (2*np.pi*ky)**2
    k2[0,0] = 1.0 # Avoid division by zero at k=0
    return k2

def cic_deposit(x, y, mass, N, L):
    """ Cloud-In-Cell density assignment onto the discrete grid """
    rho = np.zeros((N, N))
    dx = L/N
    fx = (x / dx) % N
    fy = (y / dx) % N
    
    ix = np.floor(fx).astype(int)
    iy = np.floor(fy).astype(int)
    
    wx = fx - ix
    wy = fy - iy
    
    ix1 = (ix + 1) % N
    iy1 = (iy + 1) % N
    
    np.add.at(rho, (iy, ix), mass * (1-wx)*(1-wy))
    np.add.at(rho, (iy, ix1), mass * wx*(1-wy))
    np.add.at(rho, (iy1, ix), mass * (1-wx)*wy)
    np.add.at(rho, (iy1, ix1), mass * wx*wy)
    
    return rho

def cic_interp(field, x, y, N, L):
    """ Cloud-In-Cell interpolation from discrete grid back to particles """
    dx = L/N
    fx = (x / dx) % N
    fy = (y / dx) % N
    
    ix = np.floor(fx).astype(int)
    iy = np.floor(fy).astype(int)
    
    wx = fx - ix
    wy = fy - iy
    
    ix1 = (ix + 1) % N
    iy1 = (iy + 1) % N
    
    val = (field[iy, ix] * (1-wx)*(1-wy) +
           field[iy, ix1] * wx*(1-wy) +
           field[iy1, ix] * (1-wx)*wy +
           field[iy1, ix1] * wx*wy)
    return val

def run_bullet_pm():
    print("=== TRXT Nullivance: Bullet Cluster PDE Simulation (Gate 1) ===")
    print("Implementing Particle-Mesh FFT to satisfy Global PDE Mandate.")
    
    N = 256  # Grid resolution
    L = 3000.0 # Physical box size (kpc)
    dx = L/N
    
    G = 1.0 # Gravitational internal units
    
    # 1. Main Cluster Definition
    N_main = 20000
    R_main = 300.0
    M_main_dm = 40.0
    M_main_gas = 8.0
    
    # 2. Bullet Cluster Definition
    N_bullet = 10000
    R_bullet = 150.0
    M_bullet_dm = 8.0
    M_bullet_gas = 1.6
    
    # 3. Initialize Particles
    # Main Cluster
    theta_m = np.random.uniform(0, 2*np.pi, N_main)
    r_m = R_main * np.random.power(0.5, N_main)
    x_main_dm = L/2 + 500 + r_m * np.cos(theta_m)
    y_main_dm = L/2 + r_m * np.sin(theta_m)
    vx_main_dm = np.random.normal(0, 5, N_main) - 20.0 
    vy_main_dm = np.random.normal(0, 5, N_main)
    
    theta_g = np.random.uniform(0, 2*np.pi, N_main)
    r_g = R_main * 0.7 * np.random.power(0.5, N_main) # Gas more concentrated
    x_main_gas = L/2 + 500 + r_g * np.cos(theta_g)
    y_main_gas = L/2 + r_g * np.sin(theta_g)
    vx_main_gas = np.random.normal(0, 5, N_main) - 20.0
    vy_main_gas = np.random.normal(0, 5, N_main)
    
    # Bullet Cluster
    theta_mb = np.random.uniform(0, 2*np.pi, N_bullet)
    r_mb = R_bullet * np.random.power(0.5, N_bullet)
    x_bullet_dm = L/2 - 500 + r_mb * np.cos(theta_mb)
    y_bullet_dm = L/2 + r_mb * np.sin(theta_mb)
    vx_bullet_dm = np.random.normal(0, 5, N_bullet) + 300.0
    vy_bullet_dm = np.random.normal(0, 5, N_bullet)
    
    theta_gb = np.random.uniform(0, 2*np.pi, N_bullet)
    r_gb = R_bullet * 0.7 * np.random.power(0.5, N_bullet)
    x_bullet_gas = L/2 - 500 + r_gb * np.cos(theta_gb)
    y_bullet_gas = L/2 + r_gb * np.sin(theta_gb)
    vx_bullet_gas = np.random.normal(0, 5, N_bullet) + 300.0
    vy_bullet_gas = np.random.normal(0, 5, N_bullet)
    
    # Concatenate all arrays
    x_dm = np.concatenate([x_main_dm, x_bullet_dm])
    y_dm = np.concatenate([y_main_dm, y_bullet_dm])
    vx_dm = np.concatenate([vx_main_dm, vx_bullet_dm])
    vy_dm = np.concatenate([vy_main_dm, vy_bullet_dm])
    m_dm_arr = np.concatenate([np.ones(N_main)*M_main_dm/N_main, np.ones(N_bullet)*M_bullet_dm/N_bullet])
    
    x_gas = np.concatenate([x_main_gas, x_bullet_gas])
    y_gas = np.concatenate([y_main_gas, y_bullet_gas])
    vx_gas = np.concatenate([vx_main_gas, vx_bullet_gas])
    vy_gas = np.concatenate([vy_main_gas, vy_bullet_gas])
    m_gas_arr = np.concatenate([np.ones(N_main)*M_main_gas/N_main, np.ones(N_bullet)*M_bullet_gas/N_bullet])
    
    # 4. Global Solvers
    k2 = get_k2_grid(N, L)
    dt = 0.05
    steps = 90
    
    print("Simulating collision dynamics...")
    for step in range(steps):
        # I. Global Poisson Equation PDE Solver
        rho_dm = cic_deposit(x_dm, y_dm, m_dm_arr, N, L)
        rho_gas = cic_deposit(x_gas, y_gas, m_gas_arr, N, L)
        rho_tot = rho_dm + rho_gas
        
        # FFT
        rho_k = np.fft.fft2(rho_tot)
        Phi_k = - 4 * np.pi * G * rho_k / k2
        Phi_k[0,0] = 0.0 # Zero mode
        Phi = np.fft.ifft2(Phi_k).real
        
        # II. Calculate Field Gradients (Accelerations)
        Ex = -np.gradient(Phi, dx, axis=1)
        Ey = -np.gradient(Phi, dx, axis=0)
        
        # III. Propagate Dark Matter (Collisionless)
        ax_dm = cic_interp(Ex, x_dm, y_dm, N, L)
        ay_dm = cic_interp(Ey, x_dm, y_dm, N, L)
        
        vx_dm += ax_dm * dt
        vy_dm += ay_dm * dt
        x_dm += vx_dm * dt
        y_dm += vy_dm * dt
        
        # IV. Propagate Gas (Collisional with Ram Pressure/Drag)
        v_grid_x = np.divide(cic_deposit(x_gas, y_gas, m_gas_arr * vx_gas, N, L), rho_gas + 1e-10)
        v_grid_y = np.divide(cic_deposit(x_gas, y_gas, m_gas_arr * vy_gas, N, L), rho_gas + 1e-10)
        
        ax_gas = cic_interp(Ex, x_gas, y_gas, N, L)
        ay_gas = cic_interp(Ey, x_gas, y_gas, N, L)
        
        local_vx = cic_interp(v_grid_x, x_gas, y_gas, N, L)
        local_vy = cic_interp(v_grid_y, x_gas, y_gas, N, L)
        local_rho = cic_interp(rho_gas, x_gas, y_gas, N, L)
        
        k_drag = 100000.0 # Greatly increase drag to realistically model gas collision cross section
        
        # We clip to prevent numerical instability, ensuring gas doesn't overshoot grid velocity
        # Maximum deceleration is that which brings velocity to local_v in one timestep
        alpha = np.clip(k_drag * local_rho, 0, 0.9/dt)
        drag_x = -alpha * (vx_gas - local_vx)
        drag_y = -alpha * (vy_gas - local_vy)
        
        vx_gas += (ax_gas + drag_x) * dt
        vy_gas += (ay_gas + drag_y) * dt
        x_gas += vx_gas * dt
        y_gas += vy_gas * dt

    print("Simulation complete. Calculating centroids...")
    
    # 5. Extract Bullet Centers
    # The first N_main indices belong to main cluster. The remaining belong to bullet.
    b_idx = slice(N_main, N_main + N_bullet)
    cx_bullet_dm = np.average(x_dm[b_idx], weights=m_dm_arr[b_idx])
    cy_bullet_dm = np.average(y_dm[b_idx], weights=m_dm_arr[b_idx])
    
    cx_bullet_gas = np.average(x_gas[b_idx], weights=m_gas_arr[b_idx])
    cy_bullet_gas = np.average(y_gas[b_idx], weights=m_gas_arr[b_idx])
    
    separation = np.sqrt((cx_bullet_dm - cx_bullet_gas)**2 + (cy_bullet_dm - cy_bullet_gas)**2)
    
    print("\n--- RESULTS ---")
    print(f"Bullet Dark Matter Centroid: ({cx_bullet_dm:.1f}, {cy_bullet_dm:.1f})")
    print(f"Bullet Gas Centroid:         ({cx_bullet_gas:.1f}, {cy_bullet_gas:.1f})")
    print(f"Separation:                  {separation:.2f} kpc")
    
    pass_gate = "PASS" if separation > 50 else "FAIL"
    print(f"GATE 1 STATUS:               {pass_gate}")
    
    # 6. Visualization
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Downsample for scatter plot clarity
    ax.scatter(x_gas[::5], y_gas[::5], s=2, c='red', alpha=0.3, label='Baryonic Gas (Collisional)')
    ax.scatter(x_dm[::5], y_dm[::5], s=2, c='#0055ff', alpha=0.3, label='Superfluid Dark Matter')
    
    ax.scatter([cx_bullet_gas], [cy_bullet_gas], marker='x', color='yellow', s=150, linewidths=3, label='Gas Centroid (Bullet)')
    ax.scatter([cx_bullet_dm], [cy_bullet_dm], marker='+', color='cyan', s=200, linewidths=3, label='DM Centroid (Bullet)')
    
    ax.set_xlim(L/2 - 600, L/2 + 600)
    ax.set_ylim(L/2 - 600, L/2 + 600)
    ax.set_title(f"Gate 1: Bullet Cluster Collision using Global PDE\nSeparation = {separation:.1f} kpc", fontsize=14)
    ax.legend(loc='upper right')
    ax.set_xlabel("X coordinate (kpc)")
    ax.set_ylabel("Y coordinate (kpc)")
    plt.tight_layout()
    plt.savefig('bullet_cluster_sim_pde.png', dpi=300)
    print("Saved high-res visualization to 'bullet_cluster_sim_pde.png'")

if __name__ == "__main__":
    run_bullet_pm()
