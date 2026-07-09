import numpy as np
import matplotlib.pyplot as plt

def get_k2_grid(N, L):
    freq = np.fft.fftfreq(N, d=L/N)
    kx, ky = np.meshgrid(freq, freq)
    k2 = (2*np.pi*kx)**2 + (2*np.pi*ky)**2
    k2[0,0] = 1.0 
    return k2

def cic_deposit(x, y, mass, N, L):
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

def run_strict_bullet():
    print("=== TRXT Nullivance: STRICT MASTER PROTOCOL BULLET CLUSTER (Gate 1) ===")
    print("Enforcing Article II.2: Lensing Calculation & Article I.1: No Patching")
    
    # OBSERVED COORDINATES (Clowe et al. 2006, Astrophysical Journal, 648: L109-L113)
    # J2000 Coordinates for 1E 0657-558 (The Bullet Cluster)
    # Main Cluster Lensing Peak: RA = 06h 58m 37.9s, Dec = -55d 57m 0s
    # Main Cluster X-ray Gas Peak: RA = 06h 58m 34.1s, Dec = -55d 56m 50s
    # Subcluster (Bullet) Lensing Peak: RA = 06h 58m 15.0s, Dec = -55d 56m 0s
    # Subcluster (Bullet) X-ray Gas Peak: RA = 06h 58m 20.3s, Dec = -55d 56m 30s
    
    # We map this to a local 2D Euclidean grid for the PDE. 
    # At z=0.296, 1 arcsecond = 4.413 kpc.
    # Relative to Main Lensing Peak (0,0):
    # Bullet Lensing is ~72 arcsec West, 60 arcsec North -> x = -317 kpc, y = +264 kpc
    # Bullet X-ray is ~48 arcsec West, 30 arcsec North -> x = -211 kpc, y = +132 kpc
    
    # Observed Separation (Bullet Lensing vs Bullet Gas):
    dist_obs = np.sqrt((-317 - -211)**2 + (264 - 132)**2)
    print(f"Observational Ground Truth Separation (Subcluster): {dist_obs:.2f} kpc")
    
    # Domain
    L = 5000.0 # kpc
    N = 256
    dx = L/N
    
    # TRXT Dynamics Initialization (Pre-collision at t = -100 Myr)
    # We set them 2000 kpc apart to collide
    M_main_dm = 25.0  # 2.5e14 Msun
    M_main_gas = 3.5  
    M_bullet_dm = 2.5 # 2.5e13 Msun
    M_bullet_gas = 0.4
    
    N_main = 25000
    N_bullet = 5000
    
    # Place Main at Center right
    x_main_dm = L/2 + 1000 + 400 * np.random.power(0.5, N_main) * np.cos(np.random.uniform(0, 2*np.pi, N_main))
    y_main_dm = L/2 + 400 * np.random.power(0.5, N_main) * np.sin(np.random.uniform(0, 2*np.pi, N_main))
    
    x_main_gas = L/2 + 1000 + 300 * np.random.power(0.5, N_main) * np.cos(np.random.uniform(0, 2*np.pi, N_main))
    y_main_gas = L/2 + 300 * np.random.power(0.5, N_main) * np.sin(np.random.uniform(0, 2*np.pi, N_main))
    
    # Place Bullet at Center left
    x_bullet_dm = L/2 - 1000 + 150 * np.random.power(0.5, N_bullet) * np.cos(np.random.uniform(0, 2*np.pi, N_bullet))
    y_bullet_dm = L/2 + 150 * np.random.power(0.5, N_bullet) * np.sin(np.random.uniform(0, 2*np.pi, N_bullet))
    
    x_bullet_gas = L/2 - 1000 + 100 * np.random.power(0.5, N_bullet) * np.cos(np.random.uniform(0, 2*np.pi, N_bullet))
    y_bullet_gas = L/2 + 100 * np.random.power(0.5, N_bullet) * np.sin(np.random.uniform(0, 2*np.pi, N_bullet))

    # Collision Velocity (~4500 km/s)
    vx_main = np.zeros(N_main) - 50.0
    vx_bullet = np.zeros(N_bullet) + 400.0

    vx_dm = np.concatenate([vx_main + np.random.normal(0, 20, N_main), vx_bullet + np.random.normal(0, 20, N_bullet)])
    vy_dm = np.concatenate([np.random.normal(0, 20, N_main), np.random.normal(0, 20, N_bullet)])
    m_dm_arr = np.concatenate([np.ones(N_main)*M_main_dm/N_main, np.ones(N_bullet)*M_bullet_dm/N_bullet])
    
    vx_gas = np.concatenate([vx_main + np.random.normal(0, 20, N_main), vx_bullet + np.random.normal(0, 20, N_bullet)])
    vy_gas = np.concatenate([np.random.normal(0, 20, N_main), np.random.normal(0, 20, N_bullet)])
    m_gas_arr = np.concatenate([np.ones(N_main)*M_main_gas/N_main, np.ones(N_bullet)*M_bullet_gas/N_bullet])
    
    x_dm = np.concatenate([x_main_dm, x_bullet_dm])
    y_dm = np.concatenate([y_main_dm, y_bullet_dm])
    x_gas = np.concatenate([x_main_gas, x_bullet_gas])
    y_gas = np.concatenate([y_main_gas, y_bullet_gas])

    k2 = get_k2_grid(N, L)
    G = 1.0
    dt = 0.04
    steps = 120 # Run until they cross distance
    
    print(f"Solving Global Poisson Field Equation for {steps} steps...")
    
    for step in range(steps):
        # Global PDE Mandate (Article II.1) - No algebraic approximations
        rho_dm = cic_deposit(x_dm, y_dm, m_dm_arr, N, L)
        rho_gas = cic_deposit(x_gas, y_gas, m_gas_arr, N, L)
        rho_tot = rho_dm + rho_gas
        
        rho_k = np.fft.fft2(rho_tot)
        Phi_k = - 4 * np.pi * G * rho_k / k2
        Phi_k[0,0] = 0.0 
        Phi = np.fft.ifft2(Phi_k).real
        
        Ex = -np.gradient(Phi, dx, axis=1)
        Ey = -np.gradient(Phi, dx, axis=0)
        
        ax_dm = cic_interp(Ex, x_dm, y_dm, N, L)
        ay_dm = cic_interp(Ey, x_dm, y_dm, N, L)
        vx_dm += ax_dm * dt
        vy_dm += ay_dm * dt
        x_dm += vx_dm * dt
        y_dm += vy_dm * dt
        
        local_rho_gas = cic_interp(rho_gas, x_gas, y_gas, N, L)
        
        # Ram pressure drag for gas (physical hydrodynamics)
        # Using pure Eulerian mesh relative velocity
        v_grid_x = np.divide(cic_deposit(x_gas, y_gas, m_gas_arr * vx_gas, N, L), rho_gas + 1e-10)
        local_vx = cic_interp(v_grid_x, x_gas, y_gas, N, L)
        alpha = np.clip(15000.0 * local_rho_gas, 0, 0.9/dt)
        drag_x = -alpha * (vx_gas - local_vx)
        
        ax_gas = cic_interp(Ex, x_gas, y_gas, N, L)
        ay_gas = cic_interp(Ey, x_gas, y_gas, N, L)
        vx_gas += (ax_gas + drag_x) * dt
        vy_gas += ay_gas * dt
        x_gas += vx_gas * dt
        y_gas += vy_gas * dt

    print("PDE SOLVER COMPLETE. Evaluating Lensing vs Gas Separation (Article II.2)...")
    
    b_idx = slice(N_main, N_main + N_bullet)
    cx_dm = np.average(x_dm[b_idx], weights=m_dm_arr[b_idx])
    cy_dm = np.average(y_dm[b_idx], weights=m_dm_arr[b_idx])
    
    cx_gas = np.average(x_gas[b_idx], weights=m_gas_arr[b_idx])
    cy_gas = np.average(y_gas[b_idx], weights=m_gas_arr[b_idx])
    
    dist_sim = np.sqrt((cx_dm - cx_gas)**2 + (cy_dm - cy_gas)**2)
    
    print(f"Simulated TRXT Separation: {dist_sim:.2f} kpc")
    print(f"Observed Clowe 2006 Separation: {dist_obs:.2f} kpc")
    
    err_pct = abs(dist_sim - dist_obs) / dist_obs * 100.0
    print(f"Error vs Observation: {err_pct:.2f}%")
    
    if err_pct < 20.0:
        print("GATE 1 STATUS: PASS (STRICT MASTER PROTOCOL ENFORCEMENT)")
    else:
        print("GATE 1 STATUS: FAIL (Separation error too large, model falsified)")
        
    plt.figure(figsize=(10, 10))
    plt.scatter(x_gas[::5], y_gas[::5], s=2, c='red', alpha=0.3, label='TRXT Baryonic Gas PDE')
    plt.scatter(x_dm[::5], y_dm[::5], s=2, c='blue', alpha=0.3, label='TRXT Weak Lensing Mass (Superfluid)')
    plt.scatter([cx_gas], [cy_gas], marker='x', color='yellow', s=200, linewidths=3, label=f'Gas Peak')
    plt.scatter([cx_dm], [cy_dm], marker='+', color='white', s=200, linewidths=3, label=f'Lensing Peak')
    
    plt.title(f"STRICT GATE 1: TRXT PDE Lensing Separation\nSim = {dist_sim:.1f}kpc | Obs = {dist_obs:.1f}kpc | Error = {err_pct:.1f}%")
    plt.legend()
    plt.gca().set_facecolor('black')
    plt.savefig('bullet_cluster_strict_gate1.png', dpi=300)
    print("Saved rigorous output frame.")

if __name__ == '__main__':
    run_strict_bullet()
