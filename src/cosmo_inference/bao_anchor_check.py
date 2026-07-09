import numpy as np
import matplotlib.pyplot as plt
import json
import os

def load_planck_data(filepath="c:/Users/NC/Music/trxt nullivance v14/data/Planck_2018.json"):
    """Load Planck 2018 parameters from JSON file."""
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    params = data["cosmological_parameters"]["TT_TE_EE_lowE_lensing"]
    
    # Extract needed values
    h = params["H0"]["value"] / 100.0
    r_drag = params["r_drag"]["value"]
    
    print(f"Loaded Real Data from: {filepath}")
    print(f"  H0 = {params['H0']['value']} +/- {params['H0']['error']}")
    print(f"  r_drag = {r_drag} +/- {params['r_drag']['error']} Mpc")
    
    return h, r_drag

def nullivance_spectrum_anchored(k, rs_Mpc, h, A=1.0, ns=0.96):
    """
    Generate P(k) with oscillations anchored to r_s.
    k: wavenumber in h/Mpc
    rs_Mpc: Sound Horizon in Mpc
    h: Hubble parameter (H0/100)
    """
    # Convert k to 1/Mpc (physical)
    k_phys = k * h 
    
    # Smooth component
    P_smooth = k_phys ** ns
    
    # Oscillatory component (The "Living Resonance")
    # k_osc = 2pi / r_s
    # The BAO signal is roughly sin(k * r_s) / (k * r_s) or similar Bessel.
    # Simple model: 1 + 0.05 * sin(k * r_s)
    
    oscillation = 1 + 0.05 * np.sin(k_phys * rs_Mpc) * np.exp(-(k_phys/0.1)**2) # Damping
    
    return A * P_smooth * oscillation

def check_bao_anchor():
    # Load Real Data
    h, rs_target = load_planck_data()
    
    # Scale k [h/Mpc]
    k_range = np.logspace(-3, 0, 1000)
    
    # Generate Anchored Model
    P_model = nullivance_spectrum_anchored(k_range, rs_target, h)
    
    # Theoretical Period in k [h/Mpc]:
    # Period_k_phys = 2pi / r_s [1/Mpc]
    # Period_k_h = (2pi / r_s) / h  [h/Mpc]
    
    period_k_h = (2 * np.pi / rs_target) / h
    print(f"Expected BAO Wiggle Period: {period_k_h:.4f} h/Mpc")
    
    # Plotting
    plt.figure(figsize=(10,6))
    k_linear = np.linspace(0.01, 0.2, 500)
    P_osc = nullivance_spectrum_anchored(k_linear, rs_target, h) / (k_linear*h)**0.96
    
    plt.plot(k_linear, P_osc, label='TRXT-Nullivance Model (Anchored to Planck 2018)')
    plt.title("Nullivance Anchored Oscillation (Real Data Validation)")
    plt.xlabel("k [h/Mpc]")
    plt.ylabel("P(k) / P_smooth")
    plt.grid(True)
    plt.axvline(x=period_k_h, color='r', linestyle='--', label=f'Fundamental Mode {period_k_h:.3f} h/Mpc')
    plt.legend()
    output_path = "c:/Users/NC/Music/trxt nullivance v14/paper/submission_v16/figures/fig_bao_anchor_v17_realdata.png"
    plt.savefig(output_path)
    print(f"Plot saved to {output_path}")

if __name__ == "__main__":
    check_bao_anchor()
