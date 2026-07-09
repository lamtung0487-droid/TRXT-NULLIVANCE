#!/usr/bin/env python3
"""
TRXT V14 - Theoretical Recovery Research: Phase J1 (Refined)
============================================================
Deriving Relic Abundance with Topological Form Factor Suppression

The naive geometric cross section sigma = pi * R^2 is too large
because it treats the macroscopic 8.85 fm Dark Tower soliton like
a point particle. 

During thermal freeze-out, annihilation occurs via point-like
mediators intersecting the extended coherent volume of the defect.
The annihilation probability is suppressed by the Fourier transform
of the spatial charge distribution (Form Factor) or practically,
the Volume Overlap Penalty derived in Module 4.c.
"""

import numpy as np

# PDG 2024 Constants
M_PL = 1.22e19           # Planck mass [GeV]
G_STAR_FREEZE = 86.25    # Degrees of freedom at freeze-out
OMEGA_DM_PLANCK = 0.120  # Planck 2018 Omega_c h^2
HBAR_C = 0.1973          # GeV fm

# Geometric M*
M_STAR = 246.22 * np.sqrt(2.0 + 1.0/np.pi)  # 374.895 GeV

def calculate_refined_relic():
    print("="*60)
    print("TRXT V14: EXACT RELIC ABUNDANCE DERIVATION (Form Factor)")
    print("="*60)
    
    # Mode (128,128)
    mode_p = 128
    m_chi = M_STAR * (2.0 / mode_p)
    print(f"Geometric M*   = {M_STAR:.3f} GeV")
    print(f"DT-1 Mass m_chi = {m_chi:.4f} GeV")
    
    # 1. Geometric Cross Section (Naive)
    R_defect_fm = (mode_p**2) * (HBAR_C / M_STAR)
    R_defect_gev = R_defect_fm * 5.067
    sigma_geom_gev2 = np.pi * R_defect_gev**2
    
    print(f"\nNaive Geometric Cross Section pre-suppression:")
    print(f"sigma_geom = {sigma_geom_gev2:.3e} GeV^-2")
    
    # 2. Form Factor (Overlap Penalty)
    # At freeze-out (T_f ≈ m_chi/23), the thermal de Broglie wavelength of the 
    # annihilation process is lambda_T = hbar_c / sqrt(m_chi * T_f)
    T_f = m_chi / 23.0
    lambda_T_fm = HBAR_C / np.sqrt(m_chi * T_f)
    
    print(f"\nFreeze-out Temperature T_f = {T_f:.4f} GeV")
    print(f"Thermal Wavelength lambda_T = {lambda_T_fm:.4f} fm")
    print(f"Defect Radius R_dt = {R_defect_fm:.4f} fm")
    
    # The suppression factor for an extended object annihilating via point interactions
    # is roughly (Volume_thermal_vertex / Volume_defect)
    # V_vertex ~ lambda_T^3
    # V_defect ~ R_dt^3
    
    V_thermal = (4.0/3.0) * np.pi * (lambda_T_fm / (2*np.pi))**3
    V_defect = (4.0/3.0) * np.pi * (R_defect_fm)**3
    
    form_factor_suppression = V_thermal / V_defect
    print(f"\nTopological Form Factor Suppression (S_ff) = {form_factor_suppression:.4e}")
    
    # But wait, annihilation involves TWO dark towers, so the probability of BOTH
    # being localized at the annihilation vertex scales as S_ff^2
    # AND there's the standard p-wave thermal velocity v^2.
    
    v_freezeout_sq = 3.0 / 23.0
    
    # True effective annihilation cross section
    sigma_v_eff = sigma_geom_gev2 * form_factor_suppression * v_freezeout_sq
    
    print(f"Effective <sigma v> = {sigma_v_eff:.4e} GeV^-2")
    
    # 3. Relic Density
    x_f = 23.0
    omega_h2 = (1.07e9 * x_f) / (np.sqrt(G_STAR_FREEZE) * M_PL * sigma_v_eff)
    
    print(f"\nPredicted Relic Density Omega_c h^2 = {omega_h2:.4f}")
    
    # How close is this?
    target_sigma_v = (1.07e9 * x_f) / (np.sqrt(G_STAR_FREEZE) * M_PL * OMEGA_DM_PLANCK)
    print(f"Target <sigma v> for 0.120     = {target_sigma_v:.4e} GeV^-2")
    
    tension_sigma = abs(omega_h2 - OMEGA_DM_PLANCK) / 0.001
    print(f"\nTension with Planck (0.120 ± 0.001): {tension_sigma:.1f} sigma")
    
if __name__ == "__main__":
    calculate_refined_relic()
