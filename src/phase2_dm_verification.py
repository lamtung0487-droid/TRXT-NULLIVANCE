
"""
NULLIVANCE PHASE 2: DM PHONON-MEDIATED SUPPRESSION VERIFICATION
===============================================================
Verifying the "Derivative Coupling" mechanism proposed in Phase 2.

Goal:
Calculate the effective cross-section suppression at low momentum transfer q
to confirm that a 5.71 GeV Dark Matter particle evades LZ/XENONnT limits.

Formulas (from Phase 2 derivation):
sigma_N(q) ~ (c_N^4 / 16pi) * (q^4 / (K^2 c_s^4)) * (1 / Lambda^8) * (1 / mu^2)

Simplification for order of magnitude:
sigma_eff(q) = sigma_0 * (q / Lambda)^4
where sigma_0 is a geometric/weak-scale cross section ~ 1 pb = 1e-36 cm^2.

LZ Limit for 6 GeV: ~ 1e-46 cm^2 (approx).
"""

import numpy as np
import matplotlib.pyplot as plt

def verify_phase2_suppression():
    print("--- PHASE 2: DM SUPPRESSION VERIFICATION ---")
    
    # 1. Constants & Parameters
    m_DM = 5.71 # GeV
    m_N = 0.939 # GeV (Nucleon)
    mu = (m_DM * m_N) / (m_DM + m_N) # Reduced mass
    print(f"DM Mass: {m_DM} GeV")
    print(f"Reduced Mass mu: {mu:.4f} GeV")

    # 2. Momentum Transfer q
    # q_eff = sqrt(2 * m_T * E_R)
    # Using simple kinematic estimate q ~ 2 * mu * v
    v_gal = 1e-3 # v/c approx 220 km/s
    q_max = 2 * mu * v_gal # GeV
    
    print(f"Max Momentum Transfer q_max: {q_max:.2e} GeV ({q_max*1000:.2f} MeV)")
    
    # 3. LZ constraint
    sigma_limit_LZ = 1e-45 # cm^2 (Conservative for ~6 GeV)
    # Note: LZ is very sensitive, limits drop to 1e-47 at 30 GeV, but rise sharply at low mass.
    # At 6 GeV, it's weaker. Let's use 10^-45 as a target.
    
    # 4. Calculate Bound on Lambda
    # Condition: sigma_eff < sigma_limit
    # sigma_eff = sigma_geom * (q/Lambda)^4
    sigma_geom = 1e-36 # cm^2 (pb scale)
    
    # (q/Lambda)^4 < sigma_limit / sigma_geom
    # Lambda > q * (sigma_geom / sigma_limit)^(1/4)
    
    ratio = sigma_geom / sigma_limit_LZ
    Lambda_bound = q_max * (ratio**0.25)
    
    print(f"\n[BOUND CALCULATION]")
    print(f"Geometric Sigma: {sigma_geom:.1e} cm^2")
    print(f"Target Limit:    {sigma_limit_LZ:.1e} cm^2")
    print(f"Suppression Needed: {ratio:.1e}")
    
    print(f"Lower Bound on Lambda: > {Lambda_bound:.2f} GeV")
    
    # 5. Evaluate typical Lambda candidates
    lambdas = [100.0, 365.24, 1000.0] # GeV
    print(f"\n[SCENARIO CHECK]")
    for L in lambdas:
        suppression = (q_max / L)**4
        sigma_result = sigma_geom * suppression
        status = "PASS" if sigma_result < sigma_limit_LZ else "FAIL"
        print(f"Lambda = {L:6.2f} GeV | Sigma_eff = {sigma_result:.2e} cm^2 | {status}")

    # Conclusion
    if Lambda_bound < 1000.0:
        print("\n--> CONCLUSION: Feasible. A cutoff Lambda ~ 1 TeV easily suppresses the signal.")
    else:
        print("\n--> CONCLUSION: Tight. Requires very high Lambda.")

if __name__ == "__main__":
    verify_phase2_suppression()
