# Data Directory — TRXT V7

## Included Data

### SPARC Galaxy Rotation Curves (`sparc/`)
Three galaxies from the SPARC (Spitzer Photometry & Accurate Rotation Curves) database:

| File | Galaxy | Size |
|------|--------|------|
| `F568-3_rotmod.dat` | F568-3 (LSB dwarf) | 1.7 KB |
| `NGC5055_rotmod.dat` | NGC 5055 (Sunflower) | 1.7 KB |
| `UGC06787_rotmod.dat` | UGC 06787 | 1.7 KB |

**Format:** ASCII columns — radius (kpc), observed velocity (km/s), gas, disk, bulge components.  
**Source:** [SPARC Database](http://astroweb.cwru.edu/SPARC/) (Lelli, McGaugh, Schombert 2016)

## Not Included (Too Large for GitHub)

### Planck 2018 CMB Map (`planck_2018/`)
- **File:** `COM_CMB_IQU-smica-nosz_2048_R3.00_full.fits`
- **Size:** 384 MB (exceeds GitHub 100 MB limit)
- **Content:** Full-sky temperature + polarization map (SMICA component separation, N_side=2048)
- **Download:** [Planck Legacy Archive](https://pla.esac.esa.int/)

To download manually:
```bash
mkdir -p data/planck_2018
cd data/planck_2018
wget "https://irsa.ipac.caltech.edu/data/Planck/release_3/all-sky-maps/maps/component-maps/cmb/COM_CMB_IQU-smica-nosz_2048_R3.00_full.fits"
```

> Note: The Planck map is referenced in the manuscript but is NOT required by any Python script in this repository. All prediction scripts are self-contained.
