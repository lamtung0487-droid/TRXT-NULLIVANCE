import numpy as np
import matplotlib.pyplot as plt

def get_k2_grid(N, L):
    """ Fourier space k^2 grid for global Poisson solver """
    freq = np.fft.fftfreq(N, d=L/N)
    kx, ky = np.meshgrid(freq, freq)
    k2 = (2*np.pi*kx)**2 + (2*np.pi*ky)**2
    k2[0,0] = 1.0 
    return k2

def cic_deposit(x, y, mass, N, L):
    """ Cloud-in-Cell density deposition """
    rho = np.zeros((N, N))
    dx = L/N
    # Force coordinates into [0, L)
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
    """ Cloud-in-Cell field interpolation """
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

def run_true_trxt_bullet():
    print("=== TRXT Nullivance: TRUE MONISTIC BULLET CLUSTER (Gate 1) ===")
    print("Article I: No independent DM particles. Lensing emerges from Superfluid Strain.")
    
    # 1. SCALE AND UNITS (Normalized to physical cluster scales)
    # L = 5000 kpc (5 Mpc box)
    # Mass unit = 1e13 M_sun
    # Velocity unit = 1000 km/s (1 kpc/Myr)
    # Time unit = 1 Myr
    # G in these units: a = G*M/r^2 -> (kpc/Myr^2) = G * (1e13 Msun) / (kpc^2)
    # G = 4.5e-12 (Mpc^3 Msun^-1 Myr^-2) -> In kpc: 4.5e-12 * 1e9 = 4.5e-3
    # G_norm = 4.5e-3 * 1e13 (mass unit) = 45000.0 ? No.
    # Let's be precise: G = 44.97 (kpc^3 / (1e10 M_sun * Myr^2))
    # Using 1e14 Msun as unit mass and kpc as distance: G = 0.0045
    G = 0.0045
    L = 5000.0  # kpc
    N = 256     # Grid resolution
    dx = L/N
    
    # 2. INITIAL CONDITIONS (Baryons only!)
    # Main Cluster
    M_main_gas = 30.0 # 3e14 M_sun
    N_main = 30000
    x_main = L/2 + 500 + 400 * np.random.normal(0, 0.5, N_main)
    y_main = L/2 + 400 * np.random.normal(0, 0.5, N_main)
    vx_main = np.zeros(N_main) - 1.0 # -1000 km/s
    
    # Bullet (Subcluster)
    M_bullet_gas = 5.0 # 5e13 M_sun
    N_bullet = 10000
    x_bullet = L/2 - 1500 + 150 * np.random.normal(0, 0.5, N_bullet)
    y_bullet = L/2 + 150 * np.random.normal(0, 0.5, N_bullet)
    vx_bullet = np.zeros(N_bullet) + 3.5 # +3500 km/s (collision velocity)
    
    # Consolidate Gas
    x = np.concatenate([x_main, x_bullet])
    y = np.concatenate([y_main, y_bullet])
    vx = np.concatenate([vx_main, vx_bullet])
    vy = np.concatenate([np.random.normal(0, 0.1, N_main), np.random.normal(0, 0.1, N_bullet)])
    masses = np.concatenate([np.ones(N_main)*M_main_gas/N_main, np.ones(N_bullet)*M_bullet_gas/N_bullet])
    
    # 3. SUPERFLUID FIELD INITIALIZATION
    # In TRXT, the 'Dark Matter' signal is the induced strain in the superfluid background phi.
    # We represent the superfluid displacement field as a 2D density map rho_sf.
    # Initially, it follows the gas.
    rho_sf = cic_deposit(x, y, masses * 6.0, N, L) # DM/Gas ratio ~ 6:1
    # We define superfluid velocity fields to track its own inertia
    v_sf_x = np.zeros((N, N))
    v_sf_y = np.zeros((N, N))
    # Initial SF velocity matches gas
    v_sf_x[ (x/dx).astype(int)%N, (y/dx).astype(int)%N ] = vx 
    # (Actually better to use CIC for velocity field)
    v_sf_x = cic_deposit(x, y, masses * 6.0 * vx, N, L) / (rho_sf + 1e-10)
    
    dt = 0.5 # 0.5 Myr
    steps = 150
    k2 = get_k2_grid(N, L)
    
    print(f"Propagating {N_main+N_bullet} Gas Particles and Superfluid Field...")
    
    for step in range(steps):
        # A. Deposit current Gas density
        rho_gas = cic_deposit(x, y, masses, N, L)
        
        # B. Calculate Total Gravitational Potential (Article II.1 Global FFT)
        rho_tot = rho_gas + rho_sf
        rho_k = np.fft.fft2(rho_tot)
        Phi_k = - 4 * np.pi * G * rho_k / k2
        Phi_k[0,0] = 0.0
        Phi = np.fft.ifft2(Phi_k).real
        
        # C. Field Gradients (Forces)
        Ex = -np.gradient(Phi, dx, axis=1)
        Ey = -np.gradient(Phi, dx, axis=0)
        
        # D. SUPERFLUID EVOLUTION (Added Mass Hydrodynamics)
        # SF is a superfluid: it flows with inertia, no internal pressure/viscosity.
        # It's coupled to gas via gravitohydraulic drag.
        # Advect SF density (Standard continuity)
        # We use a simple upwind or centered scheme for SF advection
        
        # Update SF velocities by local gravity
        v_sf_x += Ex * dt
        v_sf_y += Ey * dt
        
        # Continuity equation for SF: d(rho)/dt + div(rho*v) = 0
        flux_x = rho_sf * v_sf_x
        flux_y = rho_sf * v_sf_y
        drho = - (np.gradient(flux_x, dx, axis=1) + np.gradient(flux_y, dx, axis=0)) * dt
        rho_sf += drho
        # Diffusion for numerical stability (minimal)
        rho_sf += 0.01 * (np.gradient(np.gradient(rho_sf, dx, axis=1), dx, axis=1) + 
                         np.gradient(np.gradient(rho_sf, dx, axis=0), dx, axis=0)) 
        
        # E. GAS EVOLUTION (Collisional Hydrodynamics)
        ax = cic_interp(Ex, x, y, N, L)
        ay = cic_interp(Ey, x, y, N, L)
        
        # Ram Pressure Check
        # Gas particles collide with other gas. If rho_gas is high, slow down vx.
        local_rho_gas = cic_interp(rho_gas, x, y, N, L)
        # Interaction only happens if gas is moving through other gas
        # We model this as a drag dependent on local gas density
        # The factor matches the gas-gas collisional cross section
        drag_coeff = 2.0 
        # Calculate local mean gas velocity to find relative speed
        v_mean_x = cic_interp( cic_deposit(x, y, masses*vx, N, L)/(rho_gas+1e-10), x, y, N, L)
        drag_force_x = -drag_coeff * local_rho_gas * (vx - v_mean_x)
        
        vx += (ax + drag_force_x) * dt
        vy += ay * dt
        x += vx * dt
        y += vy * dt

    # 4. ANALYSIS: Lensing (SF + Gas) vs X-ray (Gas only)
    print("Simulation complete. Analyzing centroids...")
    # Subcluster (Bullet) particles are the last N_bullet entries
    b_idx = slice(N_main, N_main + N_bullet)
    cx_gas_bullet = np.average(x[b_idx], weights=masses[b_idx])
    cy_gas_bullet = np.average(y[b_idx], weights=masses[b_idx])
    
    # The Lensing Peak is where rho_tot is max in the Bullet region
    # Look in the vicinity of the bullet gas
    search_r = 500.0
    mask = (np.abs(np.arange(N)*dx - cx_gas_bullet) < search_r)[:, None] & \
           (np.abs(np.arange(N)*dx - cy_gas_bullet) < search_r)[None, :]
    
    # Find peak of rho_tot (Lensing Map)
    masked_rho_tot = rho_tot * mask
    iy_len, ix_len = np.unravel_index(np.argmax(masked_rho_tot), masked_rho_tot.shape)
    cx_len_bullet = ix_len * dx
    cy_len_bullet = iy_len * dx
    
    separation = np.sqrt((cx_len_bullet - cx_gas_bullet)**2 + (cy_len_bullet - cy_gas_bullet)**2)
    
    print(f"\nTRXT MONISTIC RESULTS:")
    print(f"Gas Peak (X-ray): {cx_gas_bullet:.1f}, {cy_gas_bullet:.1f}")
    print(f"Lensing Peak (Strain): {cx_len_bullet:.1f}, {cy_len_bullet:.1f}")
    print(f"Physical Separation: {separation:.2f} kpc")
    
    # Ground Truth: 1E 0657-56 separation is ~150-200 kpc.
    if 50 < separation < 300:
        print("GATE 1 STATUS: PASS (Emergent Lensing separation from Monistic SF)")
    else:
        print("GATE 1 STATUS: FAIL (Separation mismatch)")

    # Plot
    plt.figure(figsize=(10, 8))
    plt.imshow(rho_tot, extent=[0, L, 0, L], origin='lower', cmap='Blues', alpha=0.9, label='Lensing (SF Strain)')
    plt.scatter(x[::5], y[::5], s=1, c='orange', alpha=0.3, label='Baryonic Gas')
    plt.scatter([cx_gas_bullet], [cy_gas_bullet], marker='x', color='red', s=100, label='X-ray Peak')
    plt.scatter([cx_len_bullet], [cy_len_bullet], marker='+', color='white', s=150, label='Lensing Peak')
    plt.title(f"TRXT Monistic Bullet Cluster: Separation = {separation:.1f} kpc")
    plt.legend()
    plt.savefig('bullet_cluster_trxt_monistic.png', dpi=300)
    print("Saved 'bullet_cluster_trxt_monistic.png'.")

if __name__ == '__main__':
    run_true_trxt_bullet()
