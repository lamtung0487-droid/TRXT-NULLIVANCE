# -*- coding: utf-8 -*-
"""
Publication figures for the Genesis chapter — built ONLY from real computed data.
Every number below is transcribed from a dated log in results/logs/ (cited per figure).
Outputs: paper/v7_release_v2/figures/fig_genesis_*.pdf/.png and results/figures/.

Style: Okabe-Ito CVD-safe palette, single axis, thin marks, direct labels,
recessive grid (dataviz standard).
Run from repo root: python experiments/figures/make_genesis_figures.py
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLUE, VERM, GREEN, GRAY = "#0072B2", "#D55E00", "#009E73", "#666666"
plt.rcParams.update({
    "font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.alpha": 0.25, "grid.linewidth": 0.5,
    "legend.frameon": False, "figure.dpi": 200,
})

OUTS = [r"paper/v7_release_v2/figures", r"results/figures"]
for o in OUTS:
    os.makedirs(o, exist_ok=True)

def save(fig, name):
    for o in OUTS:
        fig.savefig(os.path.join(o, name + ".pdf"), bbox_inches="tight")
        fig.savefig(os.path.join(o, name + ".png"), bbox_inches="tight")
    plt.close(fig)
    print("saved", name)

# ---------------------------------------------------------------- Figure 1
# Bogomolny quantization. Data: bp_quantization_20260709.log (seed 42, L=128)
# and bp_quantization_robustness_20260709.log (seed 777, L=160);
# saturation: referee_response_tests_20260709.log (disk protocol v3) + Q=2 torus.
t1 = [0, 50, 200, 500, 1000, 2000]
r1 = [1.536, 1.267, 1.216, 1.158, 1.125, 1.091]
t2 = [0, 200, 1000, 2000, 4000]
r2 = [1.555, 1.205, 1.123, 1.109, 1.092]

fig, (ax, bx) = plt.subplots(1, 2, figsize=(8.2, 3.1),
                             gridspec_kw={"width_ratios": [1.5, 1], "wspace": 0.55})
ax.plot(t1, r1, "-o", color=BLUE, lw=2, ms=5, label="run A (seed 42, $L=128$)")
ax.plot(t2, r2, "-s", color=VERM, lw=2, ms=5, label="run B (seed 777, $L=160$)")
ax.axhline(1.0, color=GRAY, ls="--", lw=1)
ax.text(3900, 1.012, "Bogomolny limit  $E = 4\\pi K\\, I$", color=GRAY,
        ha="right", fontsize=9)
ax.set_xlabel("flow time  $t$")
ax.set_ylabel(r"$E\,/\,(4\pi K\, I)$")
ax.set_title("(a) Dynamical quantization under the Nullivance flow", fontsize=10)
ax.legend(loc="upper right", fontsize=9)

# saturation panel: disk protocol Q=1 (rho = 6, 8, 12) and torus Q=2
labels = [r"$Q{=}1,\ \rho{=}6$", r"$Q{=}1,\ \rho{=}8$",
          r"$Q{=}1,\ \rho{=}12$", r"$Q{=}2$ (torus)"]
vals = [0.9952, 0.9972, 0.9986, 1.0006]
y = np.arange(len(vals))[::-1]
bx.scatter(vals, y, s=45, color=BLUE, zorder=3)
bx.axvline(1.0, color=GRAY, ls="--", lw=1)
for yi, v, lab in zip(y, vals, labels):
    bx.text(v, yi - 0.33, f"{v:.4f}", ha="center", fontsize=8, color=BLUE)
bx.set_yticks(y, labels, fontsize=9)
bx.set_xlim(0.9905, 1.0045)
bx.set_ylim(-0.7, 3.5)
bx.set_xlabel(r"$E\,/\,(4\pi K\,|Q|)$")
bx.set_title("(b) Saturation of the bound", fontsize=10)
fig.suptitle("")
save(fig, "fig_genesis_quantization")

# ---------------------------------------------------------------- Figure 2
# Hopf charge algebra. Data: hopf_lift_20260709.log (96^3 Whitehead integral,
# calibrated on Q_H(1,1) = 1).
pq_pred = [2, 2, 4, 3, 6]
qh_meas = [1.988, 1.946, 3.841, 2.908, 5.542]
tags = ["(2,1)", "(1,2)", "(2,2)", "(3,1)", "(3,2)"]

fig, ax = plt.subplots(figsize=(4.4, 3.6))
lim = [0, 7]
ax.plot(lim, lim, color=GRAY, ls="--", lw=1, label=r"$Q_{\rm Hopf}=p\,q$ (exact)")
ax.scatter(pq_pred, qh_meas, s=55, color=VERM, zorder=3, label="Whitehead integral ($96^3$)")
offs = {"(2,1)": (0.15, -0.32), "(1,2)": (-0.72, 0.12), "(2,2)": (0.15, -0.3),
        "(3,1)": (0.15, -0.3), "(3,2)": (0.15, -0.3)}
for x, yv, tag in zip(pq_pred, qh_meas, tags):
    dx, dy = offs[tag]
    ax.text(x + dx, yv + dy, tag, fontsize=9, color=VERM)
ax.set_xlim(lim); ax.set_ylim(lim)
ax.set_xlabel(r"predicted  $p\cdot q$")
ax.set_ylabel(r"measured  $Q_{\rm Hopf}$")
ax.set_title("Charge algebra of the dimensional lift", fontsize=10)
ax.legend(loc="upper left", fontsize=9)
save(fig, "fig_genesis_hopf")

# ---------------------------------------------------------------- Figure 3
# Charge-protection law. Data: f2_refinement_20260813.log — tau_c identical
# across dt in {0.1, 0.2} and L in {96, 128}; rho=12 point from
# bp_quantization_robustness (15465 steps x dt 0.2).
rho = np.array([5, 6, 8, 10, 12])
tau = np.array([2.0, 6.0, 62.0, 592.0, 3093.0])

fig, ax = plt.subplots(figsize=(4.6, 3.4))
ax.semilogy(rho, tau, "o", color=BLUE, ms=6, zorder=3,
            label=r"measured $\tau_c$ (all $dt\times L$ combos identical)")
beta, c0 = np.polyfit(rho, np.log(tau), 1)
xs = np.linspace(4.6, 12.4, 50)
ax.semilogy(xs, np.exp(c0 + beta * xs), color=VERM, lw=1.5,
            label=rf"$\ln\tau_c = {beta:.2f}\,\rho {c0:+.1f}$")
ax.set_xlabel(r"defect core size  $\rho$  (lattice units)")
ax.set_ylabel(r"charge-violation time  $\tau_c$")
ax.set_title("Topological protection on the discrete substrate", fontsize=10)
ax.legend(loc="upper left", fontsize=8.5)
save(fig, "fig_genesis_protection")

# ---------------------------------------------------------------- Figure 4
# Tower spectrum. M(pq) = 3.95 N_f M* sqrt(ln) (pq)^{3/4}; band = cutoff choice
# (Lambda = M_cond ... M_Pl) => 184-201 TeV at pq=1 (derivation_stage_gaps_20260813).
pqs = np.arange(1, 9)
lo = 184.0 * pqs ** 0.75
hi = 201.4 * pqs ** 0.75

fig, ax = plt.subplots(figsize=(5.6, 3.6))
for x, l, h in zip(pqs, lo, hi):
    ax.fill_between([x - 0.3, x + 0.3], [l, l], [h, h], color=BLUE, alpha=0.75,
                    linewidth=0)
ax.fill_betweenx([0, 184], 0.4, 8.6, color=GRAY, alpha=0.10, linewidth=0)
ax.text(4.5, 60, "no absolutely stable topological state\n(pre-registered absence prediction T-P3)",
        ha="center", fontsize=8.5, color=GRAY)
ax.text(1, hi[0] + 28, "ground state\n184–201 TeV", ha="center", fontsize=8.5, color=BLUE)
ax.set_xlabel(r"Hopf charge  $Q_{\rm Hopf}=p\,q$")
ax.set_ylabel("tower mass  $M$  (TeV)")
ax.set_xticks(pqs)
ax.set_xlim(0.4, 8.6)
ax.set_ylim(0, 1250)
ax.set_title(r"The topological tower  $M = 3.95\,N_f M^{*}\sqrt{\ln}\;(pq)^{3/4}$",
             fontsize=10)
save(fig, "fig_genesis_tower")

print("ALL FIGURES DONE")
