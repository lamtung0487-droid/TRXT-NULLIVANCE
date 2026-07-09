---
name: validate-gates
description: Run the TRXT-Nullivance Gate validation suite (G0-G5) or a single gate, compare results against pass criteria, and write a structured gate log. Use after any change to the theory, constants, or solver code, and before any manuscript update.
---

# Gate Validation Suite

The Gates are the falsification ladder from `theory/protocols/MASTER-PROTOCOL-V2.md` (Article III). Run from **repo root** always.

## Gate inventory

| Gate | Script(s) | Pass criterion |
|---|---|---|
| G0 Causality/ghosts | `experiments/v17_gates/Gate0_QuantumFoam.py` | c_s ≤ 1 and no E<0 modes, all environments |
| G1 Bullet Cluster | `experiments/npl_gates/../bullet_cluster/` (latest: `bullet_cluster_trxt_v6.py`), `experiments/v17_gates/` | Lensing centroid ≠ gas centroid from global PDE |
| G2 P(k) growth | `experiments/npl_gates/npl_pk_growth_gate2.py` | LSS growth consistent with Planck/BOSS, S_8 not worsened |
| G3 SPARC rotation | `experiments/npl_gates/npl_sparc_pde_gate3.py`, `experiments/v17_gates/Gate3_GalacticRotation_SPARC.py` | χ² < 5 with zero per-galaxy tuning |
| G4 Solar screening | `experiments/npl_gates/npl_solar_vainshtein_gate4.py`, `experiments/v17_gates/Gate4_SolarSystem_Screening.py` | Vainshtein 3D, precision ~1e-5 |
| G5 Fermion emergence | `experiments/npl_gates/npl_fermion_emergence_gate5.py`, `experiments/v17_gates/Gate5_BBN_PhaseTransition.py` | Explicit topological defect mechanism / BBN consistency |

## Procedure

1. Confirm clean state: `git status` — note any uncommitted changes in the log header.
2. Run the requested gate(s) from repo root; capture stdout to `results/logs/gate<N>_<YYYYMMDD>.log`.
3. Extract the quantitative pass metric from output; compare against the criterion table above. **The criterion is fixed before the run** — never adjust a threshold to match an output.
4. If a gate FAILS: stop the ladder (gates run in order), record the failure verbatim, and do NOT propose new Lagrangian terms as fixes (Anti-Frankenstein Law). A failure is escalated to the theorist as a potential falsification.
5. Write the summary block:

```
GATE REPORT <date>
Code state: <git describe / dirty files>
G0: PASS/FAIL (metric=..., criterion=...)
...
Verdict: LADDER CLEAR / BLOCKED AT G<n>
```

append it to `results/logs/gate_ledger.md` (create if missing) so the pass history is auditable over time.

## Notes

- Long PDE runs: reduce grid size only for smoke tests and label the log SMOKE — a SMOKE pass never counts as a Gate pass.
- Missing data (e.g. Bullet Cluster FITS) → run `experiments/bullet_cluster/fetch_bullet_fits.py`, document the download in `data/README.md`.
