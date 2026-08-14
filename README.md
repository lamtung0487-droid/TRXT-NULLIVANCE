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
├── theory/              Scientific record: protocols, derivation notes, audits
│   ├── protocols/       Research laws, derivation checklist, workflow
│   └── reviews/         Audit & referee reports (incl. the global referee review)
├── src/                 Core Python package (physics engine + analysis)
├── experiments/
│   ├── verification/    13-script independent verification suite (see index above)
│   ├── v17_gates/       Validation gates G0-G5 (current suite)
│   ├── npl_gates/       Gate PDE cross-check implementations
│   ├── figures/         Generators for every data-driven figure in the report
│   ├── bullet_cluster/  Real-survey data acquisition + figure (Gate 1 context)
│   └── layer0/          Layer-0 substrate verification (Genesis chapter)
├── validation/          Self-contained expert-validation package
├── neutrino/            Neutrino-sector computations
├── scripts/             Gate runner + frozen criteria (gates_criteria.json)
├── data/                Reference datasets (SPARC, Planck/PDG/CODATA tables)
├── results/             figures/ + logs/ — the committed evidence trail
└── paper/v7_release_v2/ The published manuscript (tex, figures, changelog)
```

## Getting started

```bash
# Python 3.9+ (tested on 3.11/3.12)
pip install -r requirements.txt
# Run everything from the repository root (scripts use relative data/ paths)
python experiments/npl_gates/npl_sparc_pde_gate3.py      # example: Gate 3 (SPARC)
```

Large datasets (Planck spectra, Bullet Cluster FITS, CLASS) are not committed — see `data/README.md` for fetch instructions.

## Research methodology

The project runs as a multi-agent research lab (see `theory/protocols/`). Every result flows through the pipeline in `theory/protocols/RESEARCH_WORKFLOW.md`:

> derivation → mathematical audit → implementation → gate validation (G0–G5) → data confrontation → adversarial peer review → publication

Core laws: parameters must emerge from theory, never be tuned to data (**Anti-Hardcode**); a failed gate falsifies the action rather than triggering a patch (**Anti-Frankenstein**); every claim declares its observables and failure conditions; all validation runs against real data (SPARC, Planck 2018, PDG 2024, Bullet Cluster).

## Citation

See  (GitHub renders a "Cite this repository" button) or the concept DOI [10.5281/zenodo.18195546](https://doi.org/10.5281/zenodo.18195546).

## License

See [LICENSE](LICENSE). Research code open for scientific verification.
