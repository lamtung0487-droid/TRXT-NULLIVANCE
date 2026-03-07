# TRXT-NULLIVANCE: Source Code & Verification Scripts

**TRXT V7 — Tensor-Recursive eXtended Topology**

Source code, mathematical proofs, falsifiable predictions, and numerical verification scripts accompanying the TRXT V7 research report.

## Repository Structure

```
source_code/
├── baryogenesis/           # δ_CP derivation and baryogenesis proofs
│   ├── proof_delta_cp_*.py # CP-violation phase derivations
│   ├── step1_bubble_wall_profile.py
│   ├── steps234_cp_source_eta_B.py
│   ├── results/            # JSON verification outputs
│   └── reports/            # Research reports (Markdown)
├── predictions/            # Model predictions (post-dictions & falsifiable)
│   ├── predict_*.py        # 4 post-diction scripts
│   ├── falsifiable_*.py    # 4 genuinely falsifiable prediction scripts
│   └── results/            # JSON prediction outputs
├── v34_proof_program.py    # Core TRXT proof program
├── v35_Mstar_gap_research.py
└── regenerate_blank_figures.py

code/
└── bbn/
    └── PRyMordial/         # BBN verification (git submodule)
```

## Falsifiable Predictions

| Prediction | Observable | Expected Value | Experiment |
|---|---|---|---|
| Neutrino sector | Σm_ν | 0.059–0.081 eV | KATRIN, JUNO, DESI |
| Dark phonon | m_φ | 10–100 MeV | NA62, LDMX |
| Sigma meson | m_σ | 400–550 MeV | BESIII, LHCb |
| Dark energy (DESI) | w₀, wₐ | w₀ ≈ −0.85, wₐ ≈ −0.55 | DESI BAO Y3/Y5 |

## Requirements

- Python ≥ 3.10
- NumPy, SciPy

## License

See [LICENSE](LICENSE) for details.
