# TRXT-Nullivance

**Induced Superfluid Cosmology: A Theoretical Framework for Emergent Gravity and Dark Matter**

A research program exploring a unified framework in which gravity is induced and fundamental particles emerge as topological solitons (knots) in a superfluid vacuum condensate. The working mass law under investigation:

$$ m(p,q) = M^* \left( \frac{1}{p} + \frac{1}{q} \right) $$

with $p, q$ topological winding numbers on a toroidal manifold $T^2$.

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
