"""
run_trxt_bbn_phase_transition.py
TRXT V7 Research — BBN Phase Transition Modifier
Evidence ID: GATE-5-BBN-PHASE-TRANSITION

Purpose:
    Compute the TRXT extra-species contribution f_TRXT during BBN by tracking
    a phase-transition tanh switch around a critical temperature Tc.

    The TRXT scalar field φ enters BBN as a modification to the effective
    number of relativistic degrees of freedom g*(T) through:
        f_TRXT(T) = f_BBN × ½[1 - tanh((T - Tc)/dT)]

    This smoothly switches off TRXT contribution below the phase transition.

Reference: Appendix S.5 of TRXT_Research_Report_V14_FINAL.tex
           Based on run_trxt_bbn.py (bbn_prymordial/)
"""

import numpy as np
import json
import time

# ─── Constants ────────────────────────────────────────────────────────────────
T_BBN_START_MEV = 10.0    # MeV  (well before weak freeze-out)
T_BBN_END_MEV   = 0.01    # MeV  (after nucleosynthesis)
NUM_T_STEPS     = 1000


def make_trxt_phase_transition(
    f_BBN: float = 0.1,
    w_sf: float = 1.0 / 3.0,
    Tc_MeV: float = 1.0,
    dT_MeV: float = 0.2,
):
    """
    Build arrays T_MeV, f_TRXT(T), rho_NP(T) for BBN epoch.

    Parameters
    ----------
    f_BBN    : Total TRXT energy fraction at T >> Tc  (default 0.1 = 10%)
    w_sf     : Equation-of-state parameter of the TRXT scalar field (default 1/3)
    Tc_MeV   : Phase-transition temperature in MeV
    dT_MeV   : Transition width in MeV

    Returns
    -------
    T_arr    : Temperature array (MeV), descending from T_BBN_START
    f_arr    : f_TRXT(T) — fraction of energy density in TRXT field
    rho_arr  : ρ_NP(T) in units of ρ_rad(T); effective n_eff correction
    n_eff_arr: Effective N_eff shift due to TRXT at each T
    """
    phase = 3 * (1 + w_sf)              # dilution exponent n = 3(1+w)
    T_arr = np.linspace(T_BBN_START_MEV, T_BBN_END_MEV, NUM_T_STEPS)

    # Smooth step: 1 above Tc, 0 below Tc
    switch = 0.5 * (1.0 - np.tanh((T_arr - Tc_MeV) / dT_MeV))

    # TRXT energy fraction modulation
    f_arr = f_BBN * switch

    # ρ_NP relative to standard ρ_rad ∝ T⁴ can be parameterised as:
    #   ρ_NP / ρ_rad = f_BBN × (T/Tc)^(phase) × switch
    rho_arr = f_BBN * (T_arr / Tc_MeV) ** phase * switch

    # ΔN_eff ≈ (43/7) × f_arr  (rough conversion for radiation-like component)
    n_eff_arr = (43.0 / 7.0) * rho_arr

    return T_arr, f_arr, rho_arr, n_eff_arr


def compute_effective_bbn_parameters(f_BBN, Tc_MeV, dT_MeV):
    """
    Evaluate the effective BBN parameters at weak freeze-out T ≈ 0.7 MeV
    and at nucleosynthesis T ≈ 0.07 MeV.
    """
    T_wr = 0.7     # weak freeze-out temperature (MeV)
    T_nuc = 0.07   # nucleosynthesis temperature (MeV)

    T_arr, f_arr, rho_arr, n_eff_arr = make_trxt_phase_transition(
        f_BBN=f_BBN, Tc_MeV=Tc_MeV, dT_MeV=dT_MeV
    )

    def interp(T_target, arr):
        idx = np.argmin(np.abs(T_arr - T_target))
        return float(arr[idx])

    return {
        "T_wf_MeV": T_wr,
        "f_TRXT_at_wf": interp(T_wr, f_arr),
        "DeltaN_eff_at_wf": interp(T_wr, n_eff_arr),
        "T_nuc_MeV": T_nuc,
        "f_TRXT_at_nuc": interp(T_nuc, f_arr),
        "DeltaN_eff_at_nuc": interp(T_nuc, n_eff_arr),
    }


def run_bbn_phase_transition():
    print("=" * 60)
    print("GATE 5: BBN Phase Transition Verification")
    print("=" * 60)

    # Default TRXT parameters from research report
    f_BBN = 0.10        # 10% energy fraction
    Tc_MeV = 1.0        # transition at T ~ 1 MeV (near weak freeze-out)
    dT_MeV = 0.20       # transition width

    print(f"\n  f_BBN         = {f_BBN}")
    print(f"  Tc            = {Tc_MeV} MeV")
    print(f"  dT            = {dT_MeV} MeV")

    params = compute_effective_bbn_parameters(f_BBN, Tc_MeV, dT_MeV)

    print(f"\n  At weak freeze-out (T ≈ {params['T_wf_MeV']} MeV):")
    print(f"    f_TRXT       = {params['f_TRXT_at_wf']:.4f}")
    print(f"    ΔN_eff       = {params['DeltaN_eff_at_wf']:.4f}")
    print(f"\n  At nucleosynthesis (T ≈ {params['T_nuc_MeV']} MeV):")
    print(f"    f_TRXT       = {params['f_TRXT_at_nuc']:.6f}")
    print(f"    ΔN_eff       = {params['DeltaN_eff_at_nuc']:.6f}")

    # Observational bound: ΔN_eff < 0.30 (BBN+CMB combined, 2σ)
    DELTA_NEFF_LIMIT = 0.30
    neff_wf = params["DeltaN_eff_at_wf"]
    gate_pass = neff_wf < DELTA_NEFF_LIMIT

    print(f"\n  ΔN_eff at weak freeze-out: {neff_wf:.4f}")
    print(f"  BBN bound (< {DELTA_NEFF_LIMIT}): {'PASS ✓' if gate_pass else 'FAIL ✗'}")

    print("\n" + "=" * 60)
    print(f"GATE 5 RESULT: {'PASS ✓' if gate_pass else 'FAIL ✗'}")
    print("=" * 60)

    artifact = {
        "evidence_id": "GATE-5-BBN-PHASE-TRANSITION",
        "date": "2026-03-02",
        "input": {"f_BBN": f_BBN, "Tc_MeV": Tc_MeV, "dT_MeV": dT_MeV},
        "results": params,
        "DeltaN_eff_limit": DELTA_NEFF_LIMIT,
        "gate_pass": bool(gate_pass),
        "status": "PASS" if gate_pass else "FAIL",
    }
    return artifact


if __name__ == "__main__":
    import os
    t0 = time.time()
    result = run_bbn_phase_transition()
    t1 = time.time()
    result["runtime_s"] = round(t1 - t0, 2)
    out_path = "artifacts/gate_5_bbn_phase_transition_result.json"
    os.makedirs("artifacts", exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nArtifact saved: {out_path}")
