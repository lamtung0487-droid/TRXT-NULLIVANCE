# Data Confrontation Report — 2026-07-09

Analyst: lab data-analyst role. Datasets: `data/PDG_2024.json`, `data/sparc/Rotmod_LTG/` (175 rotmod files, SPARC LTG sample), Planck 2018 parameters. Provenance: PDG/SPARC files present and readable; Bullet Cluster FITS absent.

## Claim 1 — Harmonic mass law m(p,q) = M*(1/p + 1/q)

**Degrees-of-freedom accounting.** The scanner (`src/analysis/harmonic_spectrum.py`) searches p,q ∈ [1,200], q ≥ p → 20,100 (p,q) pairs per particle, and selects the best match. M* = 365.2407 GeV is computed from m_τ and α (measured inputs), i.e. the scale itself is data-anchored.

**Mode density.** The lattice yields 1,246 distinct modes in [50, 200] GeV; median gap between adjacent modes 0.030 GeV. The lab's own `robustness_report_real_data.txt` already concedes: "Chance of random match (0.1%): 144.93%".

**Monte Carlo null test** (`experiments/mass_spectrum/mc_null_test_mass_law.py`, log `results/logs/mc_null_test_20260709.log`, 100,000 random masses uniform in [50,200] GeV):

| Particle | Best match error | Look-elsewhere-corrected p-value |
|---|---|---|
| W (80.3692) | 0.020% | **0.225** |
| Z (91.1876) | 0.134% | **0.590** |
| Higgs (125.20) | 0.006% | **0.090** |

52.5% of *random* masses match some mode within 0.1%. Fisher-combined p ≈ 0.18. No individual or combined significance.

**Verdict: NUMEROLOGY — NOT DISTINGUISHABLE FROM NULL.** With a 20,100-point search lattice this dense, matching W/Z/Higgs demonstrates nothing; the law currently has no statistical support. To become falsifiable it must (a) fix (p,q) assignments from theory *before* comparison, and (b) predict an unmeasured mass.

**M* provenance.** `experiments/v14_phase_j/v14_j1_final_m_star_relic.py` line 72 computes its target ⟨σv⟩ *from* Ω_DM h² = 0.120 (Planck), then reports agreement with the same 0.120 as a "prediction" (lines 78–81) while the docstring claims "without ANY arbitrary parameters". This is circular. Classification: **postdiction presented as prediction.**

## Claim 2 — SPARC rotation curves, χ² < 5, zero per-galaxy tuning

- `experiments/v17_gates/Gate3_GalacticRotation_SPARC.py`: uses the **real** full 175-galaxy LTG sample (no cherry-picking found — good). But it grid-scans a universal acceleration scale a0 over [3400, 3700] and picks the χ²-minimizing value (3550), landing at χ²_red = 4.9986 — 0.03% under the pass threshold of 5. One global parameter fitted on the validation data; "zero per-galaxy tuning" is technically true but "no tuning" is not.
- `experiments/npl_gates/npl_sparc_pde_gate3.py`: **synthetic data** — generates 175 mock galaxies and sets `v_obs = v_model + noise` (lines 131–133). Its χ² = 0.98 is meaningless as validation.

**Verdict: TENSION.** The real-data fit is marginal (χ²_red ≈ 5 with a fitted global scale; for comparison, MOND-type fits on SPARC typically report χ²_red ≈ 1–2 with M/L as the only free parameter). The claim "passes SPARC" overstates the current evidence; the mock-data gate must never be cited as validation.

## Required next steps

1. Freeze (p,q) assignments theoretically; publish a pre-registered predicted mass for an unmeasured/poorly measured state.
2. Re-run SPARC with a0 fixed from theory (or from an independent dataset half), report χ² on the held-out half.
3. Fetch Bullet Cluster FITS and actually run G1 — it is the protocol's own "killer test" and currently has no runnable evidence.
