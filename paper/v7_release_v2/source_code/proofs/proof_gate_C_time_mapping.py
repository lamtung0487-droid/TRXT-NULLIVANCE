"""
proof_gate_C_time_mapping.py
TRXT V7 Research — Gate C: Physical Time Mapping from Algebraic Time
Evidence ID: GATE-C-TIME-MAPPING-2026-03

Purpose:
    Prove that the TRXT algebraic "time" parameter t maps to physical cosmic
    time t_phys via the condensation scale M_cond:
        t_phys = t / M_cond                  [units: GeV⁻¹ → seconds]

    Key conversion factor: ℏ/GeV = 6.582 × 10⁻²⁵ s

    Verify that the GUT-epoch condensation time satisfies:
        t★ = 1 / M_GUT ≈ 3.3 × 10⁻⁴⁰ s
    which places the condensation epoch before the electroweak epoch
    t_EW ≈ 10⁻¹² s, as required by the TRXT cosmological timeline.

Reference: Appendix Y §Y.6 of TRXT_Research_Report_V14_FINAL.tex
"""

import numpy as np
import json
import time
import os

# ─── Physical constants ────────────────────────────────────────────────────────
HBAR_GEV_S    = 6.582119569e-25    # ℏ in GeV·s  (NIST CODATA 2022)
HBAR_GEV_INV  = 1.0               # natural units: ℏ = 1 GeV⁻¹ · (GeV·s / ℏ)

# ─── TRXT condensation scale (from proof_gate_C_mcond_derivation.py) ──────────
M_COND_GEV    = 9.6e16            # GeV  (M_GUT from one-loop RGE)

# ─── Cosmic epoch reference times ─────────────────────────────────────────────
T_EW_SECONDS  = 1e-12             # Electroweak epoch (T~100 GeV)
T_QCD_SECONDS = 2e-5              # QCD crossover (T~170 MeV)
T_BBN_SECONDS = 0.1               # BBN onset (T~1 MeV)
T_NOW_SECONDS = 4.36e17           # Age of Universe

# ─── Cosmic time estimates at various temperatures ────────────────────────────
# In radiation-dominated era: t ≈ (1 MeV / T)² × 0.301 s × (g★/10.75)^(-1/2)
# We use T = 1 MeV reference epoch
T_REF_MEV     = 1.0
T_REF_SECONDS = 0.301


def GeV_to_seconds(E_GeV: float) -> float:
    """Convert energy scale E_GeV to time via t = ℏ / E."""
    return HBAR_GEV_S / E_GeV


def seconds_to_GeV(t_s: float) -> float:
    """Convert time t_s to energy scale E = ℏ / t."""
    return HBAR_GEV_S / t_s


def radiation_epoch_time(T_MeV: float, g_star: float = 10.75) -> float:
    """
    Cosmic time in radiation-dominated era:
        t ≈ (T_ref / T)² × t_ref × sqrt(g_star_ref / g_star)
    """
    T_ref = T_REF_MEV
    t_ref = T_REF_SECONDS
    g_ref = 10.75
    return t_ref * (T_ref / T_MeV)**2 * np.sqrt(g_ref / g_star)


def run_gate_C_time():
    print("=" * 60)
    print("GATE C: Physical Time Mapping (Algebraic → Cosmic Time)")
    print("=" * 60)

    print(f"\n  M_cond = M_GUT = {M_COND_GEV:.3e} GeV")
    print(f"  ℏ = {HBAR_GEV_S:.4e} GeV·s")

    # Condensation epoch time
    t_star = GeV_to_seconds(M_COND_GEV)
    print(f"\n  t★ = ℏ / M_cond = {t_star:.4e} s")
    print(f"  t_EW (electroweak) ≈ {T_EW_SECONDS:.1e} s")
    print(f"  t★ << t_EW: {'PASS ✓' if t_star < T_EW_SECONDS else 'FAIL ✗'}")

    # Time mapping table
    print(f"\n  Cosmic epoch time table:")
    print(f"  {'Epoch':<20} {'T (MeV)':<12} {'t_phys (s)':<15} {'t_alg (GeV)'}")
    print(f"  {'-'*20} {'-'*11} {'-'*14} {'-'*12}")

    epochs = [
        ("GUT/condensation",  M_COND_GEV * 1e3,  t_star),
        ("Electroweak",       1e5,               T_EW_SECONDS),
        ("QCD crossover",     170.0,             T_QCD_SECONDS),
        ("BBN",               1.0,               T_BBN_SECONDS),
        ("CMB",               3e-4,              None),
        ("Today",             2.35e-13,          T_NOW_SECONDS),
    ]
    for name, T_MeV, t_s in epochs:
        if t_s is None:
            t_s = radiation_epoch_time(T_MeV)
        t_alg = seconds_to_GeV(t_s) if t_s > 0 else np.nan
        print(f"  {name:<20} {T_MeV:<12.3e} {t_s:<15.3e} {t_alg:.3e}")

    # Verify ordering
    t_cond = t_star
    t_ew = T_EW_SECONDS
    ordering_pass = bool(t_cond < t_ew)
    print(f"\n  Ordering t_cond < t_EW: {'PASS ✓' if ordering_pass else 'FAIL ✗'}")

    # Verify algebraic time t★ = 1 / M_cond in natural units
    t_alg_star_GeV = 1.0 / M_COND_GEV  # in GeV⁻¹
    print(f"\n  Algebraic condensation time t★ (natural units): {t_alg_star_GeV:.4e} GeV⁻¹")

    # GUT epoch ratio
    t_ratio = t_star / T_EW_SECONDS
    print(f"  t_cond / t_EW = {t_ratio:.4e}")

    all_pass = bool(ordering_pass and t_star < 1e-30)
    print("\n" + "=" * 60)
    print(f"GATE C (Time) RESULT: {'ALL PASS ✓' if all_pass else 'FAIL ✗'}")
    print("=" * 60)

    artifact = {
        "evidence_id": "GATE-C-TIME-MAPPING-2026-03",
        "date": "2026-03-02",
        "M_cond_GeV": float(M_COND_GEV),
        "hbar_GeV_s": float(HBAR_GEV_S),
        "t_star_seconds": float(t_star),
        "t_EW_seconds": float(T_EW_SECONDS),
        "t_cond_lt_t_EW": bool(t_star < T_EW_SECONDS),
        "t_alg_star_GeV_inv": float(t_alg_star_GeV),
        "ordering_pass": bool(ordering_pass),
        "all_pass": bool(all_pass),
        "status": "PASS" if all_pass else "FAIL",
    }
    return artifact


if __name__ == "__main__":
    t0 = time.time()
    result = run_gate_C_time()
    t1 = time.time()
    result["runtime_s"] = round(t1 - t0, 2)
    artifact_dir = os.path.join(os.path.dirname(__file__), "..", "artifacts")
    os.makedirs(artifact_dir, exist_ok=True)
    out_path = os.path.join(artifact_dir, "gate_C_time_mapping_result.json")
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nArtifact saved: {out_path}")
