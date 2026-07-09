# TRXT-Nullivance Research Laboratory

**Induced Superfluid Cosmology: A Theoretical Framework for Emergent Gravity and Dark Matter**

This repository is operated as a virtual research laboratory. All work — human or agent — is bound by the laws below, distilled from `theory/protocols/MASTER-PROTOCOL-V2.md` and the derivation checklist in `theory/protocols/workflow-v5-checklist.md`.

## Repository map

| Path | Contents |
|---|---|
| `theory/RESEARCH_ATLAS.md` | **Master knowledge base** — full map of the 191-page report (mechanisms, equations, page index, inconsistency registry). **Consult this FIRST before re-reading the report or specs** |
| `theory/specs/` | Model specifications, system of equations, whitepaper, version notes (latest spec: `theory/specs/v17/TRXT_V17_Master_Spec.md`) |
| `theory/protocols/` | Research laws, derivation checklist, workflow (`RESEARCH_WORKFLOW.md`) |
| `theory/reviews/` | Peer-review and audit reports |
| `src/` | Core Python package (physics engine, analysis, visualization) |
| `experiments/` | Phase-organized research scripts: `v11_npl/`, `v12_geometry/`, `v14_phase_j/`, `npl_gates/`, `bullet_cluster/`, `cosmology/`, `mass_spectrum/`, `v17_gates/`, `misc/` |
| `validation/` | Self-contained expert-validation package (own src/tests/configs) |
| `neutrino/` | Neutrino sector sub-project |
| `data/` | Observational datasets (Planck 2018, SPARC, PDG 2024, CODATA, Bullet Cluster) — see `data/README.md` |
| `results/figures/`, `results/logs/` | All generated outputs go here, never to repo root |
| `paper/` | Manuscript trees, peer versions: `v7_release/`, `v7_release_v2/` (newest), `v8_release/`, `v9_campaign/`, `submission_v16/` |
| `external/` | Third-party code (CLASS Boltzmann solver) — gitignored, re-downloadable |
| `archive/` | Superseded scripts and working notes |

## The Laws (non-negotiable)

1. **Anti-Hardcode Law.** Framework parameters (M*, n, β, Ω_Λ, winding numbers p,q) must emerge from the theory's structure. Tuning a parameter to fit a dataset and presenting it as a derivation is falsification of results.
2. **Single Lagrangian Commitment.** The full action S is declared before any code is written. If the action fails a Gate, the action dies — no post-hoc terms to rescue it (Anti-Frankenstein Law).
3. **Three-layer separation.** Every claim must state its layer: kinematical structure (state space, symmetries), dynamical law (action/EoM), or measurement/phenomenology (observables, statistics, errors).
4. **Falsifiability.** Every model statement must declare its observables and its failure conditions (energy scale, density, curvature regime where it does not apply).
5. **Global PDE Mandate.** No local algebraic shortcuts (e.g. `v = v_N·sqrt(1+α)`). Forces come from derivatives of globally solved potentials (SOR/FFT relaxation).
6. **Stability & Causality.** Any scalar sector must be checked for ghosts (E < 0), superluminality (c_s > 1), and Ostrogradsky instabilities in all environments. Violation = disqualification.
7. **Honest Null Results.** A failed Gate is reported as a failure, in full, in `results/logs/`. Cherry-picking datasets or seeds is forbidden.

## The Gate System (validation ladder)

| Gate | Test | Pass criterion |
|---|---|---|
| G0 | Theorist check | Causality (c_s ≤ 1) and no ghosts, all environments |
| G1 | Bullet Cluster | Lensing centroid ≠ gas centroid from the global PDE |
| G2 | Structure growth | P(k) consistent with Planck/BOSS; S_8 tension not worsened |
| G3 | Galaxy rotation | Global PDE vs SPARC, χ² < 5 with **zero** per-galaxy tuning |
| G4 | Solar system | 3D Vainshtein screening to ~10⁻⁵ precision |
| G5 | Fermion emergence | Explicit topological-defect mechanism |

Gate scripts live in `experiments/npl_gates/` and `experiments/v17_gates/`. A numerical claim enters a manuscript only after passing its Gate and surviving `/peer-review`.

## Working conventions

- **Run everything from repo root** — experiment scripts use relative `data/...` paths.
- Outputs: figures → `results/figures/`, logs → `results/logs/`. Never write to repo root.
- Windows environment; Python via `pip install -r requirements.txt`.
- Every research stage leaves a written artifact (derivation note, gate log, review report) — see `theory/protocols/RESEARCH_WORKFLOW.md`.
- Manuscript changes are logged in the active paper tree's `RESEARCH_CHANGELOG.md`.

## The lab roster (subagents in `.claude/agents/`)

- **theorist** — theoretical physicist: model construction, Lagrangians, physical consistency
- **mathematician** — rigor auditor: well-posedness, self-adjointness, dimensional analysis, sign-off on derivations
- **computational-physicist** — simulations, PDE solvers, convergence studies
- **data-analyst** — real-data confrontation, statistics, error budgets
- **referee** — adversarial peer reviewer; hunts hidden tuning and irreproducibility

Skills: `/derive`, `/validate-gates`, `/peer-review`, `/reproduce`, `/paper-build` — see `.claude/skills/`.
