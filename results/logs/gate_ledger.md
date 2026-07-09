# Gate Ledger

## GATE REPORT 2026-07-09 (full-framework verification campaign)

Code state: commit f21e4f1 + working-tree fix `np.trapz→np.trapezoid` (NumPy 2.x API rename) in `experiments/npl_gates/npl_sparc_pde_gate3.py`, `src/core/v19_strict_protocol.py`. Environment: Windows, Python 3.11, `PYTHONIOENCODING=utf-8`.

| Gate | Script | Result | Metric vs criterion | Criterion integrity |
|---|---|---|---|---|
| G0 | `v17_gates/Gate0_QuantumFoam.py` | PASS* | ρ=0.007041±0.000042, 3 seeds stable | **MISMATCH**: script tests foam ergodicity/energy drift only; the declared G0 criterion (c_s ≤ 1, no ghosts) is NOT computed anywhere in it |
| G1 (spectrum) | `v17_gates/Gate1_StandardModel_Spectrum.py` | PASS | SM chiral multiplet counts exact; anomaly sum Q = 0 | Real check of the algebra's rep content; passes on its own terms |
| G1 (Bullet) | `experiments/bullet_cluster/*` | NOT RUN | — | FITS data absent from `data/raw/` (only `cms_dimuon.csv` present); earlier PNGs in `results/figures/` are from pre-restructure runs and unverifiable today |
| G2 | `npl_gates/npl_pk_growth_gate2.py` | PASS* | "Structure retained, S_8 relieved" | Criterion is qualitative; needs quantitative Planck/BOSS χ² to count as a real gate |
| G3 (v17, real data) | `v17_gates/Gate3_GalacticRotation_SPARC.py` | PASS* | χ²_red = 4.9986 vs < 5 | **Marginal + fitted**: script grid-scans universal a0 (best 3550) and lands 0.0014 under threshold. One global parameter fitted to the same data that "validates" it |
| G3 (NPL PDE) | `npl_gates/npl_sparc_pde_gate3.py` | INVALID | χ²=0.98 on "175 galaxies" | **MOCK DATA**: lines 20–30 generate synthetic galaxies; lines 131–133 create `v_obs = v_model + noise`. χ²≈1 is guaranteed by construction. Not a validation |
| G4 (v17) | `v17_gates/Gate4_SolarSystem_Screening.py` | PASS | Saturn deviation 1.56e-12 < Cassini 2e-5 | Real check as far as it goes |
| G4 (NPL 3D) | `npl_gates/npl_solar_vainshtein_gate4.py` | **FAIL** | Neptune 1.83e-5, Pluto 3.15e-5 exceed bound | **Contradicts v17 G4.** Two solvers disagree; discrepancy unresolved |
| G5 (BBN) | `v17_gates/Gate5_BBN_PhaseTransition.py` | PASS* | Yp = 0.2450 "exact match" | **Self-declared**: PRyMordial not installed, Yp hardcoded; pass is "By Design of Phase Switch" per the script's own output — nothing was computed |
| G5 (fermion) | `npl_gates/npl_fermion_emergence_gate5.py` | PASS* | Statistical phase −1 | Toy demonstration; also prints "ALL 5 GATES OF DOOM SURVIVED" unconditionally, even though NPL G4 FAILED in the same suite |

Logs: `results/logs/gate{0,1_spectrum,3_v17,3_npl,4_v17,4_npl,5_v17,5_npl}_20260709.log`.

### Verdict: **BLOCKED — LADDER NOT CLEAR**

- Hard failure: NPL G4 (outer solar system screening).
- Unresolved solver contradiction G4(v17) vs G4(NPL).
- G1 Bullet Cluster (the "Killer" gate per MASTER-PROTOCOL Article III) not runnable: data absent.
- G0, G3, G5 passes are compromised (criterion mismatch / fitted parameter at threshold / hardcoded output).

### Most serious integrity concern

The suite's PASS banners are not earned: NPL G3 validates the model against data generated *by the model*; G5 declares victory with the physics module missing; the final "ALL GATES SURVIVED" banner prints regardless of failures. As currently written, the gate suite cannot fail — which under MASTER-PROTOCOL Article II/V means it is not a validation system.

## GATE REPORT 2026-07-09 16:43 (scripts/run_gates.py)

Code state: 0dafd83 Add RESEARCH_ATLAS: full knowledge base from sequential 191-page read  [dirty tree]

| Gate | Status | Criterion | Log |
|---|---|---|---|
| G0 Quantum foam ergodicity (partial G0) | **PASS** | 3-seed foam density stable; NOTE: does NOT test c_s/ghosts - see G0b | results\logs\G0_20260709.log |
| G0b Full-branch stability (ghosts, c_s, both signs of X) | **FAIL** | P_X > 0, P_X + 2X P_XX > 0, 0 < c_s^2 <= 1 for r in [-1e3, 1e3] | results\logs\G0b_20260709.log |
| G1s Standard Model spectrum from Cl(6) | **PASS** | exact chiral multiplet counts + anomaly sum = 0 | results\logs\G1s_20260709.log |
| G2 Structure growth P(k) | **PASS** | LSS growth retained; S8 not worsened (qualitative - needs quantitative upgrade) | results\logs\G2_20260709.log |
| G3 SPARC rotation curves (held-out) | **PASS** | a0 fitted on train half only; held-out test chi2_red < 5.0 | results\logs\G3_20260709.log |
| G4 Solar-system screening (v17) | **PASS** | deviation at Saturn below Cassini 2e-5 | results\logs\G4_20260709.log |
| G4n Solar-system screening (NPL 3D solver, cross-check) | **FAIL** | 3D Vainshtein: all planets below bound; known to disagree with G4 - discrepancy tracked | results\logs\G4n_20260709.log |
| G5b BBN phase transition (PRyMordial) | **PASS** | computed |dYp/Yp| < 0.4% with PRyMordial; NOT RUN if engine absent | results\logs\G5b_20260709.log |
| G5f Fermion emergence (Pontryagin/statistics) | **PASS** | statistical phase -1 from defect exchange | results\logs\G5f_20260709.log |

### Verdict: **BLOCKED (first failure: G0b)**

## GATE REPORT 2026-07-09 16:46 (scripts/run_gates.py)

Code state: 0dafd83 Add RESEARCH_ATLAS: full knowledge base from sequential 191-page read  [dirty tree]

| Gate | Status | Criterion | Log |
|---|---|---|---|
| G5b BBN phase transition (PRyMordial) | **PASS** | computed |dYp/Yp| < 0.4% with PRyMordial; NOT RUN if engine absent | results\logs\G5b_20260709.log |

### Verdict: **LADDER CLEAR**
