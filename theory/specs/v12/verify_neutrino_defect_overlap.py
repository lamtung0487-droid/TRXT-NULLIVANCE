#!/usr/bin/env python3
"""
verify_neutrino_defect_overlap.py — Independent check of the neutrino mass mechanism used in the patch set.

Core idea (as in the patch):
  m_ν ≈ M* exp(-L/ξ), where:
    - M* is the Nullivance electroweak scale used in the report (e.g., 365.24 GeV)
    - L is the typical separation between topological defects in the vacuum network
    - ξ is a coherence (healing) length of the condensate/defect core
If defects have number density n_def, then L ≈ n_def^{-1/3}.

This script:
  (1) Solves for n_def given (mν, M*, ξ)
  (2) Or solves for ξ given (mν, M*, n_def)
  (3) Prints sensitivity derivatives for reviewer-style discussion.

Dependencies: numpy only
"""
import numpy as np

def n_def_from_mnu(mnu_eV, Mstar_GeV, xi_GeVinv):
    # Convert eV -> GeV
    mnu_GeV = mnu_eV * 1e-9
    # exp(-L/xi) = mnu/M*
    ratio = mnu_GeV / Mstar_GeV
    if ratio <= 0:
        raise ValueError("ratio<=0")
    L = -xi_GeVinv * np.log(ratio)  # in GeV^-1
    n_def = 1.0 / (L**3)           # in GeV^3
    return float(n_def), float(L)

def mnu_from_n_def(n_def_GeV3, Mstar_GeV, xi_GeVinv):
    L = (n_def_GeV3)**(-1/3)
    mnu_GeV = Mstar_GeV * np.exp(-L/xi_GeVinv)
    return float(mnu_GeV*1e9), float(L)  # eV, GeV^-1

def main():
    # Default numbers aligned with your latest instruction:
    Mstar = 365.24     # GeV
    mnu  = 0.05        # eV (representative atmospheric scale)
    # xi is model-dependent; choose a starting value and solve n_def.
    # You can scan xi to match the "≈ 1880 GeV^3" target density.
    xi_list = [0.8, 1.0, 1.2, 1.5, 2.0]  # GeV^-1 (example scan)

    print("=== Neutrino from defect overlap: n_def needed ===")
    for xi in xi_list:
        ndef, L = n_def_from_mnu(mnu, Mstar, xi)
        print(f"xi={xi:>4.2f} GeV^-1 -> n_def={ndef:>10.3g} GeV^3,  L={L:>9.3g} GeV^-1")

    # Example: if you want to back-solve mnu from n_def
    n_def_example = 1880.0  # GeV^3 (your stated target order)
    xi_example    = 1.2     # GeV^-1 (example)
    mnu_pred, L = mnu_from_n_def(n_def_example, Mstar, xi_example)
    print("\n=== Predict mnu from n_def (example) ===")
    print(f"n_def={n_def_example:g} GeV^3, xi={xi_example:g} GeV^-1 -> mnu≈{mnu_pred:.3g} eV, L≈{L:.3g} GeV^-1")

if __name__ == "__main__":
    main()
