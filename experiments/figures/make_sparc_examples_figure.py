# -*- coding: utf-8 -*-
"""Real-data SPARC figure: three representative rotation curves (data with
errors) vs the participation-law prediction at the fitted a0 = 3350 and the
zero-parameter a0 = cH0/2pi = 3215 (km/s)^2/kpc. Per-galaxy nuisances fitted
per the G3 protocol at the FITTED a0; the zero-parameter curve reuses them
(conservative: no re-optimization in its favor).

Provenance: data/sparc/Rotmod_LTG (SPARC, Lelli+ 2016); logs
G3_20260813.log, mu_participation_20260814.log. Run from repo root."""
import numpy as np
import os, shutil
import scipy.optimize as opt
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLUE = "#0072B2"; VERM = "#D55E00"; GREEN = "#009E73"
DATA = os.path.join("data", "sparc", "Rotmod_LTG")
GALS = ["NGC3198", "NGC2403", "DDO154"]     # classic HSB / intermediate / dwarf

def load(name):
    rows = []
    for line in open(os.path.join(DATA, f"{name}_rotmod.dat")):
        if line.startswith("#"):
            continue
        p = line.split()
        if len(p) >= 6:
            try:
                rows.append([float(x) for x in p[:6]])
            except ValueError:
                pass
    return np.array(rows)

def solve_g(gb, a0):
    return np.sqrt((gb**2 + np.sqrt(gb**4 + 4 * gb**2 * a0**2)) / 2)

fig, axes = plt.subplots(1, 3, figsize=(11.4, 3.9))
for ax, name in zip(axes, GALS):
    d = load(name)
    R, Vo, eV = d[:, 0], d[:, 1], np.maximum(d[:, 2], 1.0)
    Vg, Vd, Vb = np.abs(d[:, 3]), np.abs(d[:, 4]), np.abs(d[:, 5])
    hb = Vb.max() > 1.0

    def loss(p, a0v):
        if hb:
            Yd, Yb, f = p
        else:
            (Yd, f), Yb = p, 0.0
        V2 = np.maximum(Vg**2 + Yd * Vd**2 + Yb * Vb**2, 0.0)
        Vp = np.sqrt(solve_g(V2 / R, a0v) * f * R)
        return np.sum(((Vo - Vp) / eV)**2) + ((f - 1) / 0.15)**2

    if hb:
        res = opt.minimize(lambda p: loss(p, 3350.0), [0.5, 0.7, 1.0],
                           bounds=[(0.2, 2.0)] * 2 + [(0.7, 1.3)])
        Yd, Yb, f = res.x
    else:
        res = opt.minimize(lambda p: loss(p, 3350.0), [0.5, 1.0],
                           bounds=[(0.2, 2.0), (0.7, 1.3)])
        (Yd, f), Yb = res.x, 0.0
    V2 = np.maximum(Vg**2 + Yd * Vd**2 + Yb * Vb**2, 0.0)
    Rf = np.linspace(R.min(), R.max(), 200)
    V2i = np.interp(Rf, R, V2); Ri = Rf
    for a0v, col, lab in ((3350.0, VERM, "fitted $a_0=3350$"),
                          (3215.0, GREEN, "zero-param $a_0=cH_0/2\\pi$")):
        Vp = np.sqrt(solve_g(V2i / Ri, a0v) * f * Ri)
        ax.plot(Rf, Vp, color=col, lw=1.8,
                ls="-" if a0v == 3350.0 else "--", label=lab)
    Vbar = np.sqrt(V2 * f)
    ax.plot(R, Vbar, color="0.6", lw=1.2, ls=":", label="baryons only")
    ax.errorbar(R, Vo, yerr=eV, fmt="o", ms=3.6, color=BLUE, mec="white",
                mew=0.4, elinewidth=1.0, zorder=5, label="SPARC data")
    ax.set_title(name, fontsize=10.5)
    ax.set_xlabel("R [kpc]")
    ax.grid(color="0.9", lw=0.6)
    ax.set_axisbelow(True)
axes[0].set_ylabel("$V_{\\rm rot}$ [km/s]")
axes[0].legend(fontsize=7.6, loc="lower right", framealpha=0.95)
fig.suptitle("SPARC rotation curves vs the participation law (per-galaxy nuisances per the G3 protocol)",
             fontsize=11, y=1.0)
fig.tight_layout()
fig.savefig("results/figures/fig_sparc_examples.png", dpi=300, bbox_inches="tight")
shutil.copyfile("results/figures/fig_sparc_examples.png",
                "paper/v7_release_v2/figures/fig_sparc_examples.png")
print("figure written + paper copy")
