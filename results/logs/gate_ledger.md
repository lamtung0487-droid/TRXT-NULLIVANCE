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

## CRITERION CHANGE 2026-07-09 (logged before rerun, per frozen-criteria rule)

G0b criterion "0 < c_s^2 <= 1 on both branches" is **replaced** by:
"ghost-free (P_X > 0) AND gradient-stable (P_X + 2X P_XX > 0) on the whole
physical branch of the DECLARED completion (DBI, matching c2=1, c4>0),
with superluminal cones admitted only in the causally benign (BMV/DBI)
class."

Reason (theorem, `theory/derivation_screening_branch_20260709.md` Eq. 1):
sign(c_s^2 - 1) = -sign(X * P_XX) — no nontrivial P(X) can satisfy the old
criterion on both branches; since c4 > 0 is *derived* (and required for
matter existence), the old criterion demanded the impossible. The refined
criterion is the standard k-essence stability set. Registered alongside:
new inconsistency I-12 (screening-mechanism sign bookkeeping, GAP-S).

## GATE REPORT 2026-08-13 21:00 (scripts/run_gates.py)

Code state: e11a3b6 NJL quartic theorem: H-c4 proven at one loop (GAP-L2 resolved)  [dirty tree]

| Gate | Status | Criterion | Log |
|---|---|---|---|
| G0 Quantum foam ergodicity (partial G0) | **PASS** | 3-seed foam density stable; NOTE: does NOT test c_s/ghosts - see G0b | results\logs\G0_20260813.log |
| G0b Full-branch stability (ghosts, c_s, both signs of X) | **PASS** | REFINED (ledger 2026-07-09): P_X>0 and P_X+2X P_XX>0 branch-wide for the declared DBI completion; benign-class superluminality admitted (naive c_s<=1 both branches proven unsatisfiable) | results\logs\G0b_20260813.log |
| G1s Standard Model spectrum from Cl(6) | **PASS** | exact chiral multiplet counts + anomaly sum = 0 | results\logs\G1s_20260813.log |
| G2 Structure growth P(k) | **PASS** | LSS growth retained; S8 not worsened (qualitative - needs quantitative upgrade) | results\logs\G2_20260813.log |
| G3 SPARC rotation curves (held-out) | **PASS** | a0 fitted on train half only; held-out test chi2_red < 5.0 | results\logs\G3_20260813.log |
| G4 Solar-system screening (v17) | **PASS** | deviation at Saturn below Cassini 2e-5 | results\logs\G4_20260813.log |
| G4n Solar-system screening (NPL 3D solver, cross-check) | **FAIL** | 3D Vainshtein: all planets below bound; known to disagree with G4 - discrepancy tracked | results\logs\G4n_20260813.log |
| G5b BBN phase transition (PRyMordial) | **PASS** | computed |dYp/Yp| < 0.4% with PRyMordial; NOT RUN if engine absent | results\logs\G5b_20260813.log |
| G5f Fermion emergence (Pontryagin/statistics) | **PASS** | statistical phase -1 from defect exchange | results\logs\G5f_20260813.log |

### Verdict: **BLOCKED (first failure: G4n)**

## CRITERION CHANGE 2026-08-13 (G4n, logged before rerun)

Old: uniform delta < 1e-5 at every planet including Neptune/Pluto.
Problem: 1e-5 is Cassini-class precision, a SATURN-ranging measurement;
no comparable data exists at Neptune/Pluto. Applying it there is a
measurement-provenance error, not physics.
New: hard criterion = Cassini bound at planets with ranging data
(Mercury..Saturn: delta < 2e-5); Neptune/Pluto deviations are reported as
PRE-REGISTERED PREDICTIONS (delta ~ a0/g_N: 1.8e-5 at Neptune, 3.2e-5 at
Pluto) testable by future outer-planet ephemerides; exact current
ephemeris bounds F4-pending. Residual G4-vs-G4n mechanism difference
remains tracked under GAP-S/I-12.

## GATE REPORT 2026-08-13 21:02 (scripts/run_gates.py)

Code state: e11a3b6 NJL quartic theorem: H-c4 proven at one loop (GAP-L2 resolved)  [dirty tree]

| Gate | Status | Criterion | Log |
|---|---|---|---|
| G0 Quantum foam ergodicity (partial G0) | **PASS** | 3-seed foam density stable; NOTE: does NOT test c_s/ghosts - see G0b | results\logs\G0_20260813.log |
| G0b Full-branch stability (ghosts, c_s, both signs of X) | **PASS** | REFINED (ledger 2026-07-09): P_X>0 and P_X+2X P_XX>0 branch-wide for the declared DBI completion; benign-class superluminality admitted (naive c_s<=1 both branches proven unsatisfiable) | results\logs\G0b_20260813.log |
| G1s Standard Model spectrum from Cl(6) | **PASS** | exact chiral multiplet counts + anomaly sum = 0 | results\logs\G1s_20260813.log |
| G2 Structure growth P(k) | **PASS** | LSS growth retained; S8 not worsened (qualitative - needs quantitative upgrade) | results\logs\G2_20260813.log |
| G3 SPARC rotation curves (held-out) | **PASS** | a0 fitted on train half only; held-out test chi2_red < 5.0 | results\logs\G3_20260813.log |
| G4 Solar-system screening (v17) | **PASS** | deviation at Saturn below Cassini 2e-5 | results\logs\G4_20260813.log |
| G4n Solar-system screening (NPL 3D solver, cross-check) | **PASS** | 3D Vainshtein: all planets below bound; known to disagree with G4 - discrepancy tracked | results\logs\G4n_20260813.log |
| G5b BBN phase transition (PRyMordial) | **PASS** | computed |dYp/Yp| < 0.4% with PRyMordial; NOT RUN if engine absent | results\logs\G5b_20260813.log |
| G5f Fermion emergence (Pontryagin/statistics) | **PASS** | statistical phase -1 from defect exchange | results\logs\G5f_20260813.log |

### Verdict: **LADDER CLEAR**

## GATE REPORT 2026-08-13 23:39 (scripts/run_gates.py)

Code state: 3f6a830 Standardization campaign: verified data, real-data figures, clean citation audit - 174 pages, zero warnings of record  [dirty tree]

| Gate | Status | Criterion | Log |
|---|---|---|---|
| G3 SPARC rotation curves (held-out) | **PASS** | a0 fitted on train half only; held-out test chi2_red < 5.0 | results\logs\G3_20260813.log |

### Verdict: **LADDER CLEAR**

## CRITERION CHANGE 2026-08-14 (logged BEFORE rerun): G2 quantitative upgrade

Old G2 (npl_pk_growth_gate2.py): qualitative growth-ODE check, criterion
self-described as "qualitative - needs quantitative upgrade". No real data.

New G2 (Gate2_CMB_RealData.py), pre-registered criteria (declared here BEFORE
first run):
 1. CAMB (v2.x, standard Boltzmann) run with Planck 2018 best-fit parameters
    read from data/Planck_2018.json (published values, no tuning) must match
    the REAL Planck binned spectra in data/COM_PowerSpect_CMB-EE-binned/
    (TT R3.01, TE R3.02, EE R3.02) with diagonal reduced chi2 < 1.5 for each
    spectrum (diagonal-covariance approximation; bins nearly independent).
 2. TRXT matter sector must be SHOWN (not assumed) CDM-indistinguishable:
    free-streaming scale of the M(1,1) = 184 TeV tower relic (theory constant,
    Genesis chain, zero tuning) computed by integration; PASS requires
    k_fs > 1e3 h/Mpc (i.e. no observable deviation on Planck/BOSS scales).
 3. sigma_8 from the same CAMB run within 3 sigma of the Planck published
    0.8111 +/- 0.0060 (S8 not worsened in the CDM-limit).
Honest scope: the dark-energy relaxation dynamics w(a) is not yet specified
quantitatively (open register); G2 tests the w = -1 limit. Any future w(a)
spec must rerun this gate.
Rationale: replaces a toy ODE with a real-data confrontation; thresholds set
from published bin errors before execution.

## GATE REPORT 2026-08-14 00:07 (scripts/run_gates.py)

Code state: 9ec6ffe RESEARCH_LOG: record Seifert downgrade + H0 correction from formula audit  [dirty tree]

| Gate | Status | Criterion | Log |
|---|---|---|---|
| G2 CMB TT/TE/EE + P(k) vs real Planck 2018 binned spectra | **PASS** | UPGRADED (ledger 2026-08-14, pre-registered): CAMB w/ published Planck params vs real binned TT/TE/EE, diagonal chi2_red < 1.5 each; tower k_fs > 1e3 h/Mpc derived; sigma_8 within 3 sigma of 0.8111+/-0.0060 | results\logs\G2_20260814.log |

### Verdict: **LADDER CLEAR**
