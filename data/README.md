# Data Inventory

Observational inputs for TRXT-Nullivance. Committed files are small reference tables; large datasets are gitignored and documented here for re-download.

## Committed reference data

| File/dir | Source | Notes |
|---|---|---|
| `CODATA_2022.json` | CODATA 2022 recommended values | Fundamental constants |
| `PDG_2024.json` | Particle Data Group 2024 | Particle masses/widths used by the mass-spectrum analyses |
| `Planck_2018.json` | Planck 2018 results (VI. Cosmological parameters) | Background cosmology parameters |
| `sparc/` | SPARC database (Lelli, McGaugh & Schombert 2016) | Galaxy rotation curves (`*_rotmod.dat`) — http://astroweb.cwru.edu/SPARC/ |

## Large / external data (gitignored)

| Dir | Source | How to fetch |
|---|---|---|
| `COM_PowerSpect_CMB-EE-binned/` (~385MB) | Planck Legacy Archive CMB power spectra | https://pla.esac.esa.int → Cosmology products → Power spectra |
| `raw/` (~14MB) | Bullet Cluster (1E 0657-56) Chandra X-ray + weak-lensing FITS | `python experiments/bullet_cluster/fetch_bullet_fits.py` from repo root |
| `../validation/data/` | Planck 2018 plc_3.0 likelihood (clik) | See `validation/MANUAL_DOWNLOAD_INSTRUCTIONS.md` |
| `../external/class_public/` | CLASS Boltzmann solver | `git clone https://github.com/lesgourg/class_public` into `external/` |

## Rules (see CLAUDE.md)

- Every new dataset gets a row here with source, release version, and download date.
- Raw data is never edited in place; derived/processed data goes to `results/`.
- Selection cuts are declared in the analysis log *before* fitting (no cherry-picking).
