# TRXT Validation Codebase

Reproducible computational validation for the TRXT-Nullivance research project.

## Quick Start

```bash
# Clone repository
git clone https://github.com/<username>/trxt-validation.git
cd trxt-validation

# Create environment
conda env create -f environment.yml
conda activate trxt-validation

# OR use pip
pip install -r requirements.txt

# Run full validation pipeline
python scripts/run_all.py
```

## Project Structure

```
trxt_validation/
├── config/               # Configuration files
│   ├── run_config.yaml   # Master run configuration
│   └── pre_registration.yaml  # Pre-registered analysis protocol
├── data/                 # Data files (not tracked, use manifest)
│   └── data_manifest.json
├── src/                  # Source code
├── tests/                # Unit and regression tests
├── outputs/              # Run outputs and manifests
└── scripts/              # Automation scripts
```

## Reproducibility

All results in the manuscript can be reproduced with:

```bash
python scripts/run_all.py --config config/run_config.yaml
```

This will:
1. Validate data integrity (check hashes)
2. Run unit tests
3. Execute SPARC pipeline with pre-registered split
4. Generate all figures and tables
5. Create run manifest with commit hash and timestamp

## Pre-Registration

The analysis protocol is pre-registered in `config/pre_registration.yaml`.
This file was committed **before** running the validation.
Any deviation from the protocol is marked as "exploratory" in the results.

## Data

Data files are not tracked in git due to size. Download from:
- **SPARC:** http://astroweb.cwru.edu/SPARC/
- **Planck:** https://pla.esac.esa.int/

Verify integrity with:
```bash
python scripts/verify_data.py
```

## Citation

If you use this code, please cite:
```
Trinh, T.L. (2026). Induced Superfluid Cosmology: A Theoretical Framework 
for Emergent Gravity and Dark Matter. arXiv:XXXX.XXXXX
```

## License

MIT License
