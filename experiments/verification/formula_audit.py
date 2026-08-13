# -*- coding: utf-8 -*-
"""
Formula & number audit: recompute the report's quantitative claims independently.
Each check cites the report location. Verdicts: PASS (<1%), NOTE (1-5%), FAIL (>5%).
Run from repo root: python experiments/verification/formula_audit.py
"""
import numpy as np
from math import log, exp, sqrt, pi

# Verified inputs (pdgLive 2026-08-13; CODATA)
ALPHA_INV = 137.035999084
M_TAU = 1.77693        # GeV
M_MU  = 0.1056584
M_E   = 0.000510999
M_PL  = 1.22e19        # GeV
HBARC = 197.3269804    # MeV fm

results = []
def check(name, where, claimed, computed, tol_note=0.01, tol_fail=0.05):
    dev = abs(computed - claimed) / abs(claimed) if claimed else float("inf")
    v = "PASS" if dev < tol_note else ("NOTE" if dev < tol_fail else "FAIL")
    results.append((v, name, where, claimed, computed, dev))

# --- 1. Master-scale chain (App VF / App J) ---
X = 1.5 * ALPHA_INV                       # 3/(2 alpha)
C = 50 / (3 * pi)
g_eff = C / X
Ms_bcs = 2 * M_PL * exp(-1 / g_eff)       # BCS prefactor 2 (App J: Delta = 2 L e^{-1/g})
check("M* from BCS chain (2*Lambda*e^{-1/g}, g=C/X)", "App VF/J", 365.26, Ms_bcs)
Ms = 1.5 * M_TAU * ALPHA_INV              # M* = 3 m_tau/(2 alpha)
check("M* = 3 m_tau/(2 alpha)", "p.47 Eq.61", 365.26, Ms)
check("g_eff = C/X", "App A/J", 0.0258, g_eff)

# --- 2. Compton radius r0 (App Q) ---
r0 = HBARC / (Ms * 1000)                  # fm
check("r0 = hbar c / M* [fm]", "App Q Q.1", 5.4e-4, r0)

# --- 3. Sound-speed table c_s^2 = (1+2r)/(1+6r) (Table 9, p.66) ---
for r, claimed in ((0.01, 0.962), (1.0, 0.429), (10, 0.344), (100, 0.336), (1000, 0.334)):
    check(f"c_s^2 at r={r}", "Table 9", claimed, (1 + 2*r) / (1 + 6*r))

# --- 4. Fractal sound speed & H0 chain (Sec 8.1-8.2) ---
D = 2.53
cs2 = 1 / (2 * D - 1)
check("c_s^2 = 1/(2D-1), D=2.53", "Sec 8.1", 0.246, cs2)
# D_A = r_s/theta*: 141/0.010411 = 13543 Mpc (claimed 13544)
check("D_A = r_s/theta* [Mpc]", "Eq.53", 13544, 141 / 0.010411)
# H0 scaling: H0 = 67.4 * (13800/13544)
check("H0 inferred [km/s/Mpc]", "Sec 8.2", 70.6, 67.4 * 13800 / (141 / 0.010411))

# --- 5. Seifert-exponential lepton hierarchy (Sec 8.4.4 / App AK.4) ---
# m_i = M* exp(-4X S_i), S_i = 1/(abc): e:(3,3,3)->1/27, mu:(2,4,4)->1/32, tau:(2,3,6)->1/36
ratio_tau_mu = exp(4 * X * (1/32 - 1/36))
check("m_tau/m_mu from Seifert exponential", "p.50 'predicted 16.8 vs 16.81'",
      16.8, ratio_tau_mu)
check("m_tau/m_mu observed", "PDG", M_TAU / M_MU, 16.817, 0.001)
ratio_mu_e = exp(4 * X * (1/27 - 1/32))
check("m_mu/m_e from Seifert exponential vs observed 206.77", "AK.4 implication",
      M_MU / M_E, ratio_mu_e)

# --- 6. M_cond from G2/SU(3) NLSM (p.181) ---
check("M_cond = M_Pl exp(-4pi/2) [GeV]", "p.181", 2.3e16, M_PL * exp(-4 * pi / 2))

# --- 7. Vainshtein numbers (Sec 9.3) ---
# eps(1AU) = (1/2.38e7)^{3/2}
check("eps_fifth at 1 AU", "Eq.84", 8.6e-12, (1 / 2.38e7) ** 1.5)

# --- 8. Tower numbers (Genesis) ---
for Lam, name, claimed in ((M_PL, "Planck", 201.4e3), (2.3e16, "M_cond", 184.0e3)):
    Cw = 3.95 * 16 * Ms * sqrt(2 * log(Lam / Ms))
    check(f"tower M(1,1), Lambda={name} [GeV]", "Genesis 3.1", claimed, Cw)

# --- 9. Z(8,8) tension (Genesis / lab) ---
check("Z(8,8) prediction M*/4 [GeV]", "Sec 8.4 table", 91.31, Ms / 4)

# --- 10. Golden ratio (Genesis 3.4) ---
check("2 cos(pi/5) = phi", "Genesis Eq.6", 1.618034, 2 * np.cos(pi / 5), 1e-6)

# --- Report ---
print(f"{'V':4s} {'check':47s} {'where':28s} {'claimed':>12s} {'computed':>12s} {'dev':>8s}")
print("-" * 118)
fails = 0
for v, name, where, cl, co, dev in results:
    print(f"{v:4s} {name:47s} {where:28s} {cl:12.6g} {co:12.6g} {dev*100:7.2f}%")
    if v == "FAIL":
        fails += 1
print("-" * 118)
print(f"total: {len(results)} checks, {fails} FAIL, "
      f"{sum(1 for r in results if r[0]=='NOTE')} NOTE")
