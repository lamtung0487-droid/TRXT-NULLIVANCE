# -*- coding: utf-8 -*-
"""Figure for Sec 9.3 (2026 GAP-S resolution): solar-system fifth-force fraction
from the G3-validated standard interpolation law, vs the superseded
(r/r_V)^{3/2} claim and the Cassini bound.

Provenance: gap_s_screening_20260814.log; a0 = 3350 (km/s)^2/kpc (Gate 3).
Run from repo root."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import shutil

BLUE = "#0072B2"; VERM = "#D55E00"; GRAY = "0.55"
G = 6.67430e-11; M_sun = 1.989e30; AU = 1.496e11
a0 = 3350 * 3.24e-14

r = np.logspace(-0.6, 2.0, 400)          # 0.25 - 100 AU
gN = G * M_sun / (r * AU)**2
u = a0 / gN
delta_new = np.sqrt(1 + u**2) - 1        # standard-form law (validated at G3)
rV = 2.38e7                              # old claimed Vainshtein radius [AU]
delta_old = (r / rV)**1.5                # superseded law

fig, ax = plt.subplots(figsize=(6.8, 4.6))
ax.loglog(r, delta_new, color=BLUE, lw=2.0,
          label="Standard interpolation law (this work): $\\delta=\\sqrt{1+u^2}-1$")
ax.loglog(r, delta_old, color=GRAY, lw=1.6, ls="--",
          label="Superseded: $(r/r_V)^{3/2}$ (struck by the 2026 audit)")
planets = [("Earth", 1.0), ("Saturn", 9.537), ("Neptune", 30.07), ("Pluto", 39.48)]
for name, rau in planets:
    gg = G * M_sun / (rau * AU)**2
    dd = np.sqrt(1 + (a0 / gg)**2) - 1
    ax.plot(rau, dd, "o", ms=6, color=BLUE, mec="white", mew=0.6, zorder=5)
    ax.annotate(name, (rau, dd), textcoords="offset points", xytext=(6, -11),
                fontsize=8.2, color="0.25")
ax.plot(9.537, 2.3e-5, "v", ms=8, color=VERM, mec="white", mew=0.6, zorder=5)
ax.annotate("Cassini bound", (9.537, 2.3e-5), textcoords="offset points",
            xytext=(8, 2), fontsize=8.6, color=VERM)
ax.set_xlabel("Heliocentric distance $r$ [AU]")
ax.set_ylabel("Fifth-force fraction $\\delta = (g_{\\rm tot}-g_N)/g_N$")
ax.set_title("Solar-system suppression from the G3-validated law (parameter-free)",
             fontsize=10.5)
ax.set_ylim(1e-18, 1e-3)
ax.grid(color="0.9", lw=0.6, which="both")
ax.set_axisbelow(True)
ax.legend(fontsize=8.2, loc="upper left", framealpha=0.95)
fig.tight_layout()
fig.savefig("results/figures/fig_g4_screening_audited.png", dpi=300)
shutil.copyfile("results/figures/fig_g4_screening_audited.png",
                "paper/v7_release_v2/figures/fig_g4_screening_audited.png")
print("figure written + paper copy")
