# -*- coding: utf-8 -*-
"""Real-data Bullet Cluster figure: DSS optical + ROSAT All-Sky Survey X-ray contours.

Data: data/raw/bullet_optical.fits (Digitized Sky Survey), data/raw/bullet_xray.fits
(RASS-Cnt Broad, photon counts), both fetched via astroquery.skyview by
fetch_bullet_fits.py on 2026-08-13 (field center 06h58m20s -55d56m00s, 30'x30').

Honesty note: RASS is shallow (few counts at this position); after Gaussian
smoothing it shows the cluster's X-ray emission location, NOT the bullet
substructure (that requires Chandra, Markevitch et al. 2002). The figure
documents real-survey data acquisition and sky context for Gate 1.

Run from repo root. Outputs: results/figures/fig_bullet_realdata.png (+ paper copy),
results/logs/bullet_realdata_20260813.log
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.wcs import WCS
from scipy.ndimage import gaussian_filter
import os, shutil

OPT = "data/raw/bullet_optical.fits"
XRAY = "data/raw/bullet_xray.fits"
OUT = "results/figures/fig_bullet_realdata.png"
PAPER = "paper/v7_release_v2/figures/fig_bullet_realdata.png"
LOG = "results/logs/bullet_realdata_20260813.log"

VERM = "#D55E00"  # Okabe-Ito vermillion (X-ray)
BLUE = "#0072B2"  # Okabe-Ito blue (markers)

opt_h = fits.open(OPT)[0]
x_h = fits.open(XRAY)[0]
wcs = WCS(opt_h.header)

opt = opt_h.data.astype(float)
xr = x_h.data.astype(float)

# X-ray: smooth the sparse RASS counts (sigma = 3 px = 18 arcsec)
xs = gaussian_filter(xr, sigma=3.0)

# Optical stretch: asinh on background-subtracted image
o = opt - np.nanmedian(opt)
o = np.arcsinh(np.clip(o, 0, None) / 300.0)

fig = plt.figure(figsize=(7.2, 6.4))
ax = fig.add_subplot(111, projection=wcs)
ax.imshow(o, origin="lower", cmap="gray_r", interpolation="nearest")

# Contours at fractions of smoothed X-ray peak
peak = np.nanmax(xs)
levels = peak * np.array([0.35, 0.5, 0.65, 0.8, 0.95])
cs = ax.contour(xs, levels=levels, colors=VERM, linewidths=1.6, alpha=0.9)

# Centroids: X-ray (flux-weighted within 50% contour) vs optical field center
mask = xs > 0.5 * peak
yy, xx = np.mgrid[0:xs.shape[0], 0:xs.shape[1]]
cx = float(np.sum(xx[mask] * xs[mask]) / np.sum(xs[mask]))
cy = float(np.sum(yy[mask] * xs[mask]) / np.sum(xs[mask]))
ax.plot(cx, cy, "x", ms=11, mew=2.4, color=VERM, label="X-ray centroid (RASS)")

ra_c, dec_c = wcs.wcs_pix2world([[cx, cy]], 0)[0]

ax.set_xlabel("Right Ascension (J2000)")
ax.set_ylabel("Declination (J2000)")
ax.coords.grid(color="0.75", ls=":", alpha=0.6)
ax.legend(loc="upper right", frameon=True, framealpha=0.9, fontsize=9)
ax.set_title("Bullet Cluster 1E 0657$-$56: DSS optical + RASS X-ray (real survey data)",
             fontsize=11)
fig.text(0.5, 0.015,
         "DSS optical (grayscale, asinh) + ROSAT All-Sky Survey broad-band contours "
         "(Gaussian $\\sigma$=18\").\n"
         "RASS depth shows emission location only; bullet substructure requires Chandra "
         "(Markevitch et al. 2002). Fetched 2026-08-13 via astroquery.skyview.",
         fontsize=7.2, color="0.35", ha="center")
fig.tight_layout(rect=(0, 0.04, 1, 1))
os.makedirs(os.path.dirname(OUT), exist_ok=True)
fig.savefig(OUT, dpi=300)
shutil.copyfile(OUT, PAPER)

with open(LOG, "w", encoding="utf-8") as f:
    f.write("Bullet Cluster real-data figure log (2026-08-13)\n")
    f.write("=" * 60 + "\n")
    f.write("Optical: DSS via astroquery SkyView, 300x300, CDELT 6\"/px\n")
    f.write("X-ray:   RASS-Cnt Broad (photon counts) via astroquery SkyView\n")
    f.write("         NOTE: first fetch used 'RASS Background 1' (a modeled\n")
    f.write("         background map) -- caught in audit and re-fetched as counts.\n")
    f.write(f"X-ray raw counts: max={np.nanmax(xr):.0f}, total={np.nansum(xr):.0f} "
            f"(shallow survey; smoothed sigma=3px for contours)\n")
    f.write(f"Flux-weighted X-ray centroid (>50% contour): "
            f"RA={ra_c:.4f} deg, Dec={dec_c:.4f} deg\n")
    f.write("Field center requested: 06h58m20s -55d56m00s = (104.583, -55.933)\n")
    f.write(f"Centroid offset from field center: "
            f"dRA={(ra_c-104.583)*60*np.cos(np.radians(-55.93)):.2f}', "
            f"dDec={(dec_c+55.9333)*60:.2f}'\n")
    f.write("Honest scope: figure documents real-data acquisition + emission\n")
    f.write("location; it does NOT resolve the merger substructure (Chandra needed).\n")
    f.write(f"Outputs: {OUT}; copied to {PAPER}\n")

print("figure written:", OUT)
print(f"X-ray centroid: RA={ra_c:.4f}, Dec={dec_c:.4f}  "
      f"(field center 104.583, -55.9333)")
print(f"raw counts total={np.nansum(xr):.0f}, max={np.nanmax(xr):.0f}")
