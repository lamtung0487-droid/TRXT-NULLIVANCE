# -*- coding: utf-8 -*-
"""Publication figure for Gate 2 (real data): Planck 2018 binned TT/TE/EE points
vs CAMB spectrum computed from published Planck parameters (no tuning).

Provenance: parameters data/Planck_2018.json; data files
data/COM_PowerSpect_CMB-EE-binned/ (PLA R3.01/R3.02); gate log
results/logs/G2_realdata_20260814.log. Run from repo root.
"""
import numpy as np
import json, os, shutil
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import camb

BLUE = "#0072B2"   # Okabe-Ito: data
VERM = "#D55E00"   # Okabe-Ito: model
DATA_DIR = "data/COM_PowerSpect_CMB-EE-binned"
OUT = "results/figures/fig_g2_cmb_realdata.png"
PAPER = "paper/v7_release_v2/figures/fig_g2_cmb_realdata.png"

cp = json.load(open("data/Planck_2018.json"))["cosmological_parameters"]["TT_TE_EE_lowE_lensing"]
pars = camb.CAMBparams()
pars.set_cosmology(H0=cp["H0"]["value"], ombh2=cp["Omega_b_h2"]["value"],
                   omch2=cp["Omega_c_h2"]["value"], tau=cp["tau"]["value"])
pars.InitPower.set_params(As=np.exp(cp["ln_1e10_A_s"]["value"]) * 1e-10,
                          ns=cp["n_s"]["value"])
pars.set_for_lmax(2600, lens_potential_accuracy=1)
cls = camb.get_results(pars).get_cmb_power_spectra(pars, CMB_unit="muK")["total"]
ells = np.arange(cls.shape[0])

SPECS = [
    ("TT", "COM_PowerSpect_CMB-TT-binned_R3.01.txt", 0, 1.008),
    ("TE", "COM_PowerSpect_CMB-TE-binned_R3.02.txt", 3, 1.171),
    ("EE", "COM_PowerSpect_CMB-EE-binned_R3.02.txt", 1, 1.118),
]

fig, axes = plt.subplots(3, 1, figsize=(7.0, 8.6), sharex=True)
for ax, (name, fname, col, rchi2) in zip(axes, SPECS):
    d = np.loadtxt(os.path.join(DATA_DIR, fname))
    l_d, Dl_d = d[:, 0], d[:, 1]
    err = 0.5 * (np.abs(d[:, 2]) + np.abs(d[:, 3]))
    sel = ells >= 30
    ax.plot(ells[sel], cls[sel, col], color=VERM, lw=1.8, zorder=3,
            label="CAMB, published Planck 2018 parameters (no tuning)")
    ax.errorbar(l_d, Dl_d, yerr=err, fmt="o", ms=3.4, color=BLUE, mec="white",
                mew=0.4, elinewidth=1.0, capsize=0, zorder=4,
                label="Planck 2018 binned data (PLA R3)")
    ax.text(0.985, 0.92, f"{name}   $\\chi^2_\\nu = {rchi2:.3f}$",
            transform=ax.transAxes, ha="right", va="top", fontsize=10)
    ax.set_ylabel(f"$\\mathcal{{D}}_\\ell^{{{name}}}$ [$\\mu$K$^2$]")
    ax.grid(color="0.88", lw=0.6, zorder=0)
    ax.set_axisbelow(True)
axes[0].legend(loc="upper right", bbox_to_anchor=(1.0, 0.86), fontsize=8.4,
               frameon=True, framealpha=0.95)
axes[1].axhline(0, color="0.6", lw=0.7)
axes[2].set_xlabel("Multipole $\\ell$")
axes[2].set_xlim(0, 2100)
axes[0].set_title("Gate 2 (real data): CMB spectra vs Planck 2018 binned measurements",
                  fontsize=11)
fig.align_ylabels(axes)
fig.tight_layout()
fig.savefig(OUT, dpi=300)
shutil.copyfile(OUT, PAPER)
print("written:", OUT, "and paper copy")
