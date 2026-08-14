# TRXT-Nullivance

**Induced Superfluid Cosmology: A Theoretical Framework for Emergent Gravity and Dark Matter**

A research program exploring a unified framework in which gravity is induced and fundamental particles emerge as topological solitons in a superfluid vacuum condensate.

**Current state (2026-08 standardization campaign):** the topological mass tower $M(p,q) = 3.95\,N_f M\sqrt{\ln}\,(pq)^{3/4}$ (ground state 184–201 TeV; the legacy harmonic law $M^*(1/p+1/q)$ is demoted to breathing-mode fine structure); galaxy dynamics from the participation law $u = u_N + u_0\,u_N/u$ with $a_0 = cH_0/2\pi$ (zero globally fitted parameters, ledger-preregistered pass); the CMB gate runs on real Planck 2018 binned spectra; every quantitative claim traces to committed code and a log. See `theory/RESEARCH_LOG.md` and the global referee report (`theory/reviews/referee_report_global_20260814.md`).

## Reproducibility index (verification suite)

Run from repo root with `PYTHONIOENCODING=utf-8`. Each script writes a committed log to `results/logs/`:

| Script (`experiments/verification/`) | Verifies | Log |
|---|---|---|
| `formula_audit.py` | 21 report formulas/numbers | `formula_audit_20260813.log` |
| `vf_chain_audit.py` | Cl(6)→M* chain + fragility | `vf_chain_audit_20260814.log` |
| `lattice_C_computation.py` | C = 50/(3π); 5.339 struck | `lattice_C_computation_20260814.log` |
| `quasi1d_C_model.py` | quasi-1D frame; locking; 1/q | `quasi1d_C_model_20260814.log` |
| `bcs_gap_equation_comb.py` | transmutation slope protection | `bcs_gap_comb_20260814.log` |
| `vortex_state_counting.py` | one core state per cell | `vortex_state_counting_20260814.log` |
| `bdg_vortex_comb.py` | BdG: self-consistency; CdGM count | `bdg_vortex_comb_20260814.log` |
| `scheme_conventions_audit.py` | prefactor/g=4/look-elsewhere | `scheme_conventions_20260814.log` |
| `gap_s_screening.py` | screening dichotomy theorem | `gap_s_screening_20260814.log` |
| `mu_participation_law.py` | participation law; zero-param SPARC | `mu_participation_20260814.log` |
| `gap_n4d_relic.py` | tower relic: symmetric excluded | `gap_n4d_relic_20260814.log` |
| `sidm_crosssection_audit.py` | SIDM table audit (FAIL recorded) | `sidm_audit_20260814.log` |
| `audit_sweep2.py` | Koide/neutrino/BBN sweep | `audit_sweep2_20260814.log` |

Gates: `python scripts/run_gates.py` (criteria frozen in `scripts/gates_criteria.json`; changes ledger-logged in `results/logs/gate_ledger.md`).

## Repository structure

```
├── CLAUDE.md            Lab charter: laws, gate system, agent roster
├── theory/
│   ├── specs/           Model specifications (current: specs/v17/TRXT_V17_Master_Spec.md)
│   ├── protocols/       Research laws, derivation checklist, RESEARCH_WORKFLOW.md
│   └── reviews/         Audit & referee reports
├── src/                 Core Python package (engine, analysis, visualization)
├── experiments/         Phase-organized research scripts
│   ├── v11_npl/         Non-perturbative logic transition
│   ├── v12_geometry/    Topological derivations (Koide phase, chirality, knot masses)
│   ├── v14_phase_j/     Expert-audit recovery derivations (J1–J9)
│   ├── npl_gates/       Gate 2–5 PDE validation scripts
│   ├── v17_gates/       Gate 0–5 suite (current)
│   ├── bullet_cluster/  Bullet Cluster global PDE simulations (Gate 1)
│   ├── cosmology/       Baryogenesis, decoherence, DESI w(z) fits
│   ├── mass_spectrum/   Mass solution, defect census, Layer-0 validation
│   └── misc/            Cross-checks and debug scripts
├── validation/          Self-contained expert-validation package
├── neutrino/            Neutrino sector sub-project
├── data/                Observational datasets (see data/README.md)
├── results/             figures/ and logs/ — all generated output
├── paper/               Manuscript trees: v7_release, v7_release_v2 (newest),
│                        v8_release, v9_campaign, submission_v16
├── external/            Third-party code (CLASS) — gitignored
└── archive/             Superseded scripts and working notes
```

## Getting started

```bash
pip install -r requirements.txt
# Run everything from the repository root (scripts use relative data/ paths)
python experiments/npl_gates/npl_sparc_pde_gate3.py      # example: Gate 3 (SPARC)
```

Large datasets (Planck spectra, Bullet Cluster FITS, CLASS) are not committed — see `data/README.md` for fetch instructions.

## Research methodology

The project runs as a multi-agent research lab (see `CLAUDE.md`). Every result flows through the pipeline in `theory/protocols/RESEARCH_WORKFLOW.md`:

> derivation → mathematical audit → implementation → gate validation (G0–G5) → data confrontation → adversarial peer review → publication

Core laws: parameters must emerge from theory, never be tuned to data (**Anti-Hardcode**); a failed gate falsifies the action rather than triggering a patch (**Anti-Frankenstein**); every claim declares its observables and failure conditions; all validation runs against real data (SPARC, Planck 2018, PDG 2024, Bullet Cluster).

## License

See [LICENSE](LICENSE). Research code open for scientific verification.
