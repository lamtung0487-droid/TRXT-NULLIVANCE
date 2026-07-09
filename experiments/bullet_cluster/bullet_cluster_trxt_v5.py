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
    # Standard modulo wrap for periodic grid
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

def run_monistic_trxt_bullet():
    print("=== TRXT Nullivance: MONISTIC PARTICLE-MESH BULLET CLUSTER (V5 FINAL) ===")
    
    # 1. Physics Scaling (kpc, Myr, 10^11 Msun)
    G = 0.45 
    L = 5000.0 
    N = 256
    dx = L/N
    dt = 0.5   # 0.5 Myr step for higher accuracy
    steps = 120 # Total time 60 Myr (30 Myr pre-impact, 30 Myr post-impact)
    
    # 2. Monistic Initialization (Baryons and Superfluid 'Added Mass' together)
    # Total Mass ~ 1.5e15 and 0.25e15 Msun consistent with Clowe et al. 2006
    N_total = 30000
    N_main = int(0.85 * N_total)
    
    # Main Cluster (Right side moving Left)
    x_main = L/2 + 200 + 400 * np.random.normal(0, 0.7, N_main)
    y_main = L/2 + 400 * np.random.normal(0, 0.7, N_main)
    vx_main = np.zeros(N_main) - 0.5 # -500 km/s relative to center
    m_main_baryon = 1500.0 # 1.5e14 M_sun gas
    
    # Bullet Subcluster (Left side moving Right)
    N_bull = N_total - N_main
    x_bull = L/2 - 600 + 150 * np.random.normal(0, 0.5, N_bull)
    y_bull = L/2 + 100 * np.random.normal(0, 0.5, N_bull)
    vx_bull = np.zeros(N_bull) + 4.0 # +4000 km/s relative to center
    m_bull_baryon = 250.0 # 2.5e13 M_sun gas
    
    # Init Gas
    x_gas = np.concatenate([x_main, x_bull])
    y_gas = np.concatenate([y_main, y_bull])
    vx_gas = np.concatenate([vx_main, vx_bull])
    vy_gas = np.zeros(N_total)
    m_gas = np.concatenate([np.ones(N_main)*m_main_baryon/N_main, np.ones(N_bull)*m_bull_baryon/N_bull])
    
    # Init Superfluid (Added Mass)
    x_sf = np.copy(x_gas)
    y_sf = np.copy(y_gas)
    vx_sf = np.copy(vx_gas)
    vy_sf = np.zeros(N_total)
    # TRXT Ratio ~ 6.0
    m_sf = m_gas * 6.0
    
    k2 = get_k2_grid(N, L)
    print("Executing Particle-Mesh Global PDE Solver...")

    for step in range(steps):
        # A. Density
        rho_gas = cic_deposit(x_gas, y_gas, m_gas, N, L)
        rho_sf = cic_deposit(x_sf, y_sf, m_sf, N, L)
        rho_tot = rho_gas + rho_sf
        
        # B. Poisson (Article II.1 Mandate)
        rho_k = np.fft.fft2(rho_tot)
        phi_k = - 4 * np.pi * G * rho_k / k2
        phi_k[0,0] = 0.0
        Phi = np.fft.ifft2(phi_k).real
        
        Ex = -np.gradient(Phi, dx, axis=1)
        Ey = -np.gradient(Phi, dx, axis=0)
        
        # C. TRXT Inertial Superfluid (No collisional drag)
        ax_sf = cic_interp(Ex, x_sf, y_sf, N, L)
        ay_sf = cic_interp(Ey, x_sf, y_sf, N, L)
        vx_sf += ax_sf * dt
        vy_sf += ay_sf * dt
        x_sf += vx_sf * dt
        y_sf += vy_sf * dt
        
        # D. Collisional Baryons (Gas-Gas Ram Pressure)
        ax_gas = cic_interp(Ex, x_gas, y_gas, N, L)
        ay_gas = cic_interp(Ey, x_gas, y_gas, N, L)
        
        # Drag implementation: slows the gas as it hits high gas density zones
        local_rho_gas = cic_interp(rho_gas, x_gas, y_gas, N, L)
        drag_attenuation = 1.0 / (1.0 + 12.0 * local_rho_gas * dt)
        vx_gas = (vx_gas + ax_gas * dt) * drag_attenuation
        vy_gas = (vy_gas + ay_gas * dt) * drag_attenuation
        
        x_gas += vx_gas * dt
        y_gas += vy_gas * dt

    print("Collision finished. Comparing Centroids...")
    b_idx = slice(N_main, N_total)
    
    # Centroids of the Bullet Subcluster
    cx_gas = np.average(x_gas[b_idx], weights=m_gas[b_idx])
    cy_gas = np.average(y_gas[b_idx], weights=m_gas[b_idx])
    cx_len = np.average(x_sf[b_idx], weights=m_sf[b_idx])
    cy_len = np.average(y_sf[b_idx], weights=m_sf[b_idx])
    
    separation = np.abs(cx_len - cx_gas) # Physical separation along collision axis
    
    print(f"X-ray Peak (Gas): {cx_gas:.1f}")
    print(f"Lensing Peak (SF): {cx_len:.1f}")
    print(f"PHYSICAL SEPARATION: {separation:.2f} kpc")
    
    target_low, target_high = 100, 250 # Clowe 2006 range
    if target_low < separation < target_high:
        print(f"GATE 1 STATUS: PASS (Separation {separation:.1f} kpc matches observation)")
    else:
        print(f"GATE 1 STATUS: FAIL (Separation {separation:.1f} kpc outside range {target_low}-{target_high})")

    plt.figure(figsize=(10, 8))
    plt.scatter(x_gas[::4], y_gas[::4], s=2, c='red', alpha=0.3, label='TRXT Gas (Baryons)')
    plt.scatter(x_sf[::4], y_sf[::4], s=2, c='cyan', alpha=0.1, label='TRXT Superfluid Strain (Lensing)')
    plt.scatter([cx_gas], [cy_gas], marker='x', s=100, color='yellow', label='Gas Centroid')
    plt.scatter([cx_len], [cy_len], marker='+', s=200, color='white', label='Lensing Centroid')
    plt.title(f"Monistic TRXT: Emergent Lensing separation = {separation:.1f} kpc")
    plt.legend()
    plt.gca().set_facecolor('black')
    plt.savefig('bullet_cluster_trxt_pass.png', dpi=300)
    print("Results saved: bullet_cluster_trxt_pass.png")

if __name__ == '__main__':
    run_monistic_trxt_bullet()
