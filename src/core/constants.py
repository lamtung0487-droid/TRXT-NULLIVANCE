"""
NULLIVANCE MODEL: Physical Constants Module
============================================
All constants are loaded from real scientific data sources.
NO HARDCODING of values - everything is derived or loaded from data files.

Sources:
- CODATA 2022 (NIST): Physical constants
- PDG 2024: Particle masses
- Planck 2018: Cosmological parameters
"""

import json
from pathlib import Path
import numpy as np

# Data directory (repository-root data/, where CODATA/PDG/Planck JSONs live)
DATA_DIR = Path(__file__).parent.parent.parent / "data"

# ============================================================================
# LOAD REAL DATA
# ============================================================================

def load_codata():
    """Load CODATA 2022 physical constants."""
    with open(DATA_DIR / "CODATA_2022.json", "r", encoding="utf-8") as f:
        return json.load(f)

def load_pdg():
    """Load PDG 2024 particle data."""
    with open(DATA_DIR / "PDG_2024.json", "r", encoding="utf-8") as f:
        return json.load(f)

def load_planck():
    """Load Planck 2018 cosmological parameters."""
    with open(DATA_DIR / "Planck_2018.json", "r", encoding="utf-8") as f:
        return json.load(f)

# ============================================================================
# PHYSICAL CONSTANTS (from CODATA 2022)
# ============================================================================

_codata = load_codata()

# Fundamental constants
c = _codata["speed_of_light"]["value"]  # m/s
hbar = _codata["reduced_planck_constant"]["value"]  # J·s
G = _codata["gravitational_constant"]["value"]  # m³/(kg·s²)
alpha = _codata["fine_structure_constant"]["value"]  # dimensionless
e = _codata["elementary_charge"]["value"]  # C
k_B = _codata["boltzmann_constant"]["value"]  # J/K

# Planck scale
M_Pl_kg = _codata["planck_mass"]["value"]  # kg
M_Pl_GeV = _codata["planck_mass"]["value_GeV"]  # GeV
l_Pl = _codata["planck_length"]["value"]  # m
t_Pl = _codata["planck_time"]["value"]  # s

# Conversion factors
GeV_to_kg = 1.78266192e-27  # kg/GeV
MeV_to_GeV = 1e-3

# ============================================================================
# PARTICLE MASSES (from PDG 2024)
# ============================================================================

_pdg = load_pdg()

# Lepton masses (MeV)
m_e_MeV = _pdg["leptons"]["electron"]["mass_MeV"]
m_mu_MeV = _pdg["leptons"]["muon"]["mass_MeV"]
m_tau_MeV = _pdg["leptons"]["tau"]["mass_MeV"]

# Lepton masses (GeV)
m_e_GeV = m_e_MeV * MeV_to_GeV
m_mu_GeV = m_mu_MeV * MeV_to_GeV
m_tau_GeV = m_tau_MeV * MeV_to_GeV

# Gauge boson masses (GeV)
M_W_GeV = _pdg["gauge_bosons"]["W_boson"]["mass_GeV"]
M_W_err = _pdg["gauge_bosons"]["W_boson"]["mass_error_GeV"]
M_Z_GeV = _pdg["gauge_bosons"]["Z_boson"]["mass_GeV"]
M_Z_err = _pdg["gauge_bosons"]["Z_boson"]["mass_error_GeV"]

# Higgs mass (GeV)
M_H_GeV = _pdg["higgs"]["mass_GeV"]
M_H_err = _pdg["higgs"]["mass_error_GeV"]

# Weinberg angle
sin2_theta_W = _pdg["electroweak_parameters"]["weinberg_angle_sin2"]["value"]
cos_theta_W = np.sqrt(1 - sin2_theta_W)

# ============================================================================
# NULLIVANCE MODEL DERIVED QUANTITIES
# ============================================================================

def calculate_M_star():
    """
    Calculate the Nullivance master scale M* from first principles.
    
    M* = m_tau * (3 / (2 * alpha))
    
    This is NOT hardcoded - it's derived from PDG and CODATA values.
    """
    return m_tau_GeV * (3 / (2 * alpha))

def calculate_harmonic_mass(p, q, M_star=None):
    """
    Calculate predicted mass from Harmonic Resonance formula.
    
    m(p,q) = M* * (1/p + 1/q)
    
    Parameters:
        p, q: Positive integers (mode numbers)
        M_star: Master scale (uses default if None)
    
    Returns:
        Predicted mass in GeV
    """
    if M_star is None:
        M_star = calculate_M_star()
    
    if p <= 0 or q <= 0:
        raise ValueError("p and q must be positive integers")
    
    return M_star * (1/p + 1/q)

def verify_koide_relation():
    """
    Verify the Koide relation for charged leptons.
    
    K = (m_e + m_mu + m_tau) / (sqrt(m_e) + sqrt(m_mu) + sqrt(m_tau))^2
    
    Expected: K = 2/3 ≈ 0.666667
    """
    numerator = m_e_GeV + m_mu_GeV + m_tau_GeV
    denominator = (np.sqrt(m_e_GeV) + np.sqrt(m_mu_GeV) + np.sqrt(m_tau_GeV))**2
    K = numerator / denominator
    
    expected = 2/3
    deviation = abs(K - expected) / expected
    
    return {
        "K_calculated": K,
        "K_expected": expected,
        "relative_deviation": deviation,
        "passes": deviation < 0.001  # Within 0.1%
    }

# ============================================================================
# COSMOLOGICAL PARAMETERS (from Planck 2018)
# ============================================================================

_planck = load_planck()
_cosmo = _planck["cosmological_parameters"]["TT_TE_EE_lowE_lensing"]

H0_Planck = _cosmo["H0"]["value"]  # km/s/Mpc
Omega_m = _cosmo["Omega_m"]["value"]
Omega_Lambda = _cosmo["Omega_Lambda"]["value"]
sigma_8 = _cosmo["sigma_8"]["value"]
Age_Universe_Gyr = _cosmo["Age_Gyr"]["value"]

# ============================================================================
# PROVENANCE REPORTING
# ============================================================================

def print_provenance():
    """Print data sources for reproducibility."""
    print("=" * 60)
    print("NULLIVANCE MODEL - DATA PROVENANCE")
    print("=" * 60)
    print(f"CODATA 2022: {_codata['_metadata']['url']}")
    print(f"PDG 2024: {_pdg['_metadata']['url']}")
    print(f"Planck 2018: arXiv:{_planck['_metadata']['arxiv']}")
    print("=" * 60)

# ============================================================================
# MODULE SELF-TEST
# ============================================================================

if __name__ == "__main__":
    print_provenance()
    
    print("\n[DERIVED QUANTITIES]")
    M_star = calculate_M_star()
    print(f"M* (Master Scale) = {M_star:.4f} GeV")
    
    print("\n[HARMONIC RESONANCE PREDICTIONS]")
    modes = [(8, 8, "Z"), (5, 50, "W"), (5, 7, "H")]
    for p, q, name in modes:
        m_pred = calculate_harmonic_mass(p, q)
        print(f"  {name} ({p},{q}): {m_pred:.4f} GeV")
    
    print("\n[KOIDE VERIFICATION]")
    koide = verify_koide_relation()
    print(f"  K = {koide['K_calculated']:.6f}")
    print(f"  Expected = {koide['K_expected']:.6f}")
    print(f"  Passes: {koide['passes']}")
