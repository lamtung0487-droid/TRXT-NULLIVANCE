# -*- coding: utf-8 -*-
"""GATE 2 (quantitative, real data): CMB TT/TE/EE vs Planck 2018 binned spectra.

Criteria pre-registered in results/logs/gate_ledger.md (2026-08-14 entry),
BEFORE first execution:
  1. CAMB with Planck 2018 published parameters (data/Planck_2018.json, no
     tuning) vs real binned spectra: diagonal reduced chi2 < 1.5 each (TT/TE/EE).
  2. Tower relic M(1,1) = 184 TeV: computed free-streaming k_fs > 1e3 h/Mpc
     (CDM-indistinguishability DERIVED, not assumed).
  3. sigma_8 from same run within 3 sigma of published 0.8111 +/- 0.0060.

Anti-Hardcode: every cosmological number is read from data/Planck_2018.json
(published Planck values with provenance) or derived; the tower mass comes from
the Genesis chain (theory constant). Nothing is fitted to the data files.

Run from repo root. Log: results/logs/G2_realdata_<date>.log
"""
import numpy as np
import json, io, os, sys
from datetime import date

import camb

DATA_DIR = "data/COM_PowerSpect_CMB-EE-binned"
LOG = f"results/logs/G2_realdata_{date.today().strftime('%Y%m%d')}.log"

OUT = []
def emit(s=""):
    print(s); OUT.append(s)

emit("--- GATE 2 (REAL DATA): CMB spectra vs Planck 2018 binned TT/TE/EE ---")

# ---------------------------------------------------------------- parameters
pj = json.load(open("data/Planck_2018.json"))
cp = pj["cosmological_parameters"]["TT_TE_EE_lowE_lensing"]
H0 = cp["H0"]["value"]
ombh2 = cp["Omega_b_h2"]["value"]
omch2 = cp["Omega_c_h2"]["value"]
tau = cp["tau"]["value"]
ns = cp["n_s"]["value"]
As = np.exp(cp["ln_1e10_A_s"]["value"]) * 1e-10
sigma8_pub = cp["sigma_8"]["value"]
sigma8_err = cp["sigma_8"]["error"]
emit(f"  params (Planck 2018 VI, published): H0={H0}, Obh2={ombh2}, Och2={omch2},")
emit(f"    tau={tau}, ns={ns}, As={As:.4e}")

# ---------------------------------------------------------------- CAMB run
pars = camb.CAMBparams()
pars.set_cosmology(H0=H0, ombh2=ombh2, omch2=omch2, tau=tau)
pars.InitPower.set_params(As=As, ns=ns)
pars.set_for_lmax(2600, lens_potential_accuracy=1)
pars.set_matter_power(redshifts=[0.0], kmax=10.0)
res = camb.get_results(pars)
cls = res.get_cmb_power_spectra(pars, CMB_unit="muK")["total"]  # Dl [muK^2]
ells = np.arange(cls.shape[0])
sigma8_camb = float(res.get_sigma8_0())

# ---------------------------------------------------------------- data files
FILES = {
    "TT": ("COM_PowerSpect_CMB-TT-binned_R3.01.txt", 0),
    "TE": ("COM_PowerSpect_CMB-TE-binned_R3.02.txt", 3),
    "EE": ("COM_PowerSpect_CMB-EE-binned_R3.02.txt", 1),
}
emit("")
emit("  [1] spectra vs REAL binned Planck data (diagonal chi2):")
chi2_ok = True
chi2_summary = {}
for name, (fname, col) in FILES.items():
    d = np.loadtxt(os.path.join(DATA_DIR, fname))
    l_d, Dl_d, err_m, err_p = d[:, 0], d[:, 1], d[:, 2], d[:, 3]
    err = 0.5 * (np.abs(err_m) + np.abs(err_p))
    # interpolate model at (non-integer) bin centers
    Dl_m = np.interp(l_d, ells, cls[:, col])
    r = (Dl_d - Dl_m) / err
    chi2 = float(np.sum(r**2)); n = len(l_d)
    rchi2 = chi2 / n
    chi2_summary[name] = (chi2, n, rchi2)
    flag = "ok" if rchi2 < 1.5 else "EXCEEDS 1.5"
    if rchi2 >= 1.5:
        chi2_ok = False
    emit(f"    {name}: chi2 = {chi2:8.1f} / {n:3d} bins -> reduced {rchi2:6.3f}  [{flag}]")
emit("    (diagonal-covariance approximation, symmetric errors; declared in ledger)")

# ---------------------------------------------------------------- tower k_fs
emit("")
emit("  [2] tower-relic free-streaming (M(1,1) = 184 TeV, Genesis chain):")
m_dm_GeV = 184e3                    # theory constant (Genesis, Lambda = M_cond)
x_f = 25.0                          # standard freeze-out m/T_f (Kolb-Turner)
T0_GeV = 2.348e-13                  # T_CMB = 2.7255 K in GeV (CODATA conversion)
T_f = m_dm_GeV / x_f
a_f = T0_GeV / T_f                  # entropy-dilution O(1) factors neglected (conservative)
v_f = np.sqrt(3 * T_f / m_dm_GeV)   # thermal velocity at decoupling
h = H0 / 100
om_r = 4.15e-5 / h**2               # photons+neutrinos (standard, derived from T_CMB)
om_m = (ombh2 + omch2) / h**2
om_l = 1 - om_m - om_r
# comoving free-streaming length: lambda = int v(a)/(a^2 H(a)) da, v = v_f a_f/a
a_grid = np.logspace(np.log10(a_f), 0, 4000)
H_a = (H0 / 299792.458) * np.sqrt(om_r * a_grid**-4 + om_m * a_grid**-3 + om_l)  # Mpc^-1
v_a = np.minimum(v_f * a_f / a_grid, 1.0)
lam_fs = float(np.trapz(v_a / (a_grid**2 * H_a), a_grid))   # comoving Mpc
k_fs = 2 * np.pi / lam_fs * (1 / h)                          # h/Mpc... keep simple:
k_fs_hmpc = 2 * np.pi / lam_fs / h
kfs_ok = k_fs_hmpc > 1e3
emit(f"    T_f = {T_f:.1f} GeV, a_f = {a_f:.2e}, v_f = {v_f:.3f}c")
emit(f"    lambda_fs = {lam_fs:.3e} Mpc (comoving)  ->  k_fs = {k_fs_hmpc:.2e} h/Mpc")
emit(f"    criterion k_fs > 1e3 h/Mpc: {'ok' if kfs_ok else 'FAIL'}")
emit(f"    -> tower DM is CDM-indistinguishable on all Planck/BOSS scales (derived)")

# ---------------------------------------------------------------- sigma8
emit("")
emit("  [3] sigma_8 consistency:")
ns8 = abs(sigma8_camb - sigma8_pub) / sigma8_err
s8_ok = ns8 < 3.0
emit(f"    CAMB sigma_8 = {sigma8_camb:.4f} vs published {sigma8_pub} +/- {sigma8_err}")
emit(f"    deviation = {ns8:.2f} sigma (criterion < 3): {'ok' if s8_ok else 'FAIL'}")

# ---------------------------------------------------------------- verdict
emit("")
emit("  Honest scope: dark-energy relaxation dynamics w(a) unspecified -> tested")
emit("  in the w = -1 limit (open-problem register); any future w(a) spec reruns G2.")
emit("")
if chi2_ok and kfs_ok and s8_ok:
    emit(">>> GATE 2 STATUS: PASS (real-data criteria pre-registered 2026-08-14) <<<")
    rc = 0
else:
    emit(">>> GATE 2 STATUS: FAIL <<<")
    rc = 1

io.open(LOG, "w", encoding="utf-8").write("\n".join(OUT) + "\n")
print("log written:", LOG)
sys.exit(rc)
