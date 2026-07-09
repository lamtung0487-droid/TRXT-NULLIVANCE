# MaVaN Neutrino Research Project
## Mass-Varying Neutrino Validation for Induced Superfluid Cosmology

**Author**: Research Team  
**Date**: 2026-02-02  
**Status**: Validated ✓

---

## Project Structure

```
neutrino/
├── docs/                          # Documentation
│   ├── MaVaN_Research_Report.md   # Main research report (Appendix for ISC)
│   └── README.md                  # This file
├── data/                          # Input data files
│   ├── T_table.dat                # Bahcall B-8 solar neutrino spectrum
│   ├── prem.dat                   # PREM Earth density model
│   ├── sk_zenith_data.csv         # SK-IV zenith angle data
│   └── sk_energy_data.csv         # SK-IV energy spectrum data
├── output/                        # Simulation outputs
│   ├── out_mavans_ADN_vs_E.csv    # Day-Night asymmetry vs Energy
│   └── out_mavans_ADN_vs_cosZ.csv # Day-Night asymmetry vs Zenith
├── scripts/                       # Analysis scripts
│   └── (future plotting scripts)
└── sk_mavans_prem_pipeline.py     # Main simulation code
```

---

## Quick Start

### Run Standard Simulation
```bash
python sk_mavans_prem_pipeline.py --beta_solar 0.092 --beta_earth 0.0
```

### Run Full Validation Suite
```bash
# Energy spectrum validation
python sk_mavans_prem_pipeline.py --beta_solar 0.092 --validate_energy

# Zenith shape validation
python sk_mavans_prem_pipeline.py --beta_solar 0.092 --validate

# Low-energy consistency check
python sk_mavans_prem_pipeline.py --beta_solar 0.092 --validate_low_e

# Hyper-K forecast
python sk_mavans_prem_pipeline.py --beta_solar 0.092 --forecast
```

---

## Key Results

| Test | Result | Status |
|---|---|---|
| Solar-Reactor $\Delta m^2$ Tension | $R(\beta) = 0.64$ | ✓ Resolved |
| SK-IV Zenith Shape | $\chi^2 = 4.5/6$ | ✓ Pass |
| SK-IV Energy Spectrum | $\chi^2 = 2.5/7$ | ✓ Pass |
| Borexino Consistency | $<5\%$ deviation | ✓ Pass |
| Numerical Robustness | Slab vs RK4 agree | ✓ Pass |

---

## Connection to ISC

This research provides **particle physics evidence** for the scalar-field-induced mass modification predicted by Induced Superfluid Cosmology.

The MaVaN parameter $\beta \approx 0.092$ corresponds to a neutrino-scalar coupling:

$$g_\phi \sim 0.1 \times \frac{m_\nu}{\Phi_0^2}$$

See `docs/MaVaN_Research_Report.md` for full theoretical derivation.

---

## References

1. Super-K IV: PRD 94, 052010 (2016)
2. KamLAND: PRL 100, 221803 (2008)
3. Borexino: Nature 562, 505 (2018)
4. NuFIT 5.2: www.nu-fit.org (2022)
