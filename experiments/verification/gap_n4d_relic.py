# -*- coding: utf-8 -*-
"""GAP-N4d: relic abundance of the topological tower from the Great Condensation.

Pipeline (each stage with stated uncertainty bands):
  A. Kibble-Zurek production at T_c ~ M_cond = 2.3e16 GeV: freeze-out
     correlation length xi^ = xi0 (tau_Q/tau0)^{nu/(1+nu z)}, defect yield
     Y_KZ = f / (s/T_c^3) / (xi^ T_c)^3. Bands: critical exponents (z = 1, 2;
     nu = 0.71, 3D O(3) class [LIT]), formation fraction f in [1e-3, 1e-1],
     g* in [10, 1000].
  B. Soliton-antisoliton annihilation burn-down: solitons are EXTENDED objects
     (size ~ 1/M*), so annihilation is geometric and unsuppressed, while
     THERMAL PRODUCTION of coherent solitons is exponentially suppressed
     (Drukier-Nussinov class) -> one-way Boltzmann equation
         dY/dx = -(lambda(x)/x^2) Y^2,  lambda = s(M)<sigma v>/H(M)
     integrated from x_i = M/T_c. Bands: sigma = pi R^2 with R in
     {1/M*, 1/M(1,1)}; v(x) = min(1, sqrt(3/x)).
  C. Verdict on the SYMMETRIC scenario, and the required primordial
     topological asymmetry if the tower is to be the dark matter.
  D. Context: the 'unitarity-regime thermal relic' phrasing (Genesis) is
     unavailable to solitons (production suppression) -- honest revision.

Run from repo root.  Log: results/logs/gap_n4d_relic_20260814.log
"""
import numpy as np
from math import pi, sqrt, log
from scipy.integrate import quad
import io

OUT = []
def emit(s=""):
    print(s); OUT.append(s)

emit("=" * 76)
emit("GAP-N4d: TOWER RELIC FROM THE GREAT CONDENSATION   (2026-08-14)")
emit("=" * 76)

M_PL = 1.22091e19          # GeV
T_C = 2.3e16               # GeV (M_cond, verified p.181 chain)
M_SOL = 1.84e5             # GeV (M(1,1), Lambda = M_cond anchor)
MS = 365.26                # GeV (M*, soliton size scale 1/M*)
Y_REQ_COEF = 2.74e8        # Omega h^2 = 2.74e8 * M[GeV] * Y
OMEGA_DM = 0.12
Y_REQ = OMEGA_DM / (Y_REQ_COEF * M_SOL)
emit(f"  scales: T_c = {T_C:.1e} GeV, M(1,1) = {M_SOL:.2e} GeV, size ~ 1/M* = 1/{MS} GeV")
emit(f"  required yield for Omega h^2 = 0.12:  Y_req = {Y_REQ:.2e}")

# ---------------------------------------------------------------- A. KZ
emit("")
emit("--- A. Kibble-Zurek production at the transition ---")
nu = 0.71
emit(f"  quench ratio tau_Q/tau0 = T_c/H(T_c):")
for gstar in (10, 100, 1000):
    H_c = 1.66 * sqrt(gstar) * T_C**2 / M_PL
    ratio = T_C / H_c
    emit(f"    g* = {gstar:4d}: H_c = {H_c:.2e} GeV, tau_Q/tau0 = {ratio:.1f}")
emit("  (near-Planckian transition -> only a moderately slow quench)")
Y_KZ_band = []
for gstar in (10, 100, 1000):
    H_c = 1.66 * sqrt(gstar) * T_C**2 / M_PL
    ratio = T_C / H_c
    s_coef = (2 * pi**2 / 45) * gstar
    for z in (1, 2):
        xi_hat = ratio**(nu / (1 + nu * z))       # in units 1/T_c
        for f in (1e-3, 1e-2, 1e-1):
            Y = f / (s_coef * xi_hat**3)
            Y_KZ_band.append(Y)
Y_KZ_min, Y_KZ_max = min(Y_KZ_band), max(Y_KZ_band)
emit(f"  Y_KZ band (over z, f, g*): [{Y_KZ_min:.1e}, {Y_KZ_max:.1e}]")
emit(f"  vs Y_req = {Y_REQ:.1e}: OVERPRODUCTION by "
     f"{log(Y_KZ_min/Y_REQ)/log(10):.0f}-{log(Y_KZ_max/Y_REQ)/log(10):.0f} orders")
emit("  (the classic monopole-problem situation -- annihilation must be examined)")

# ---------------------------------------------------------------- B. burn-down
emit("")
emit("--- B. annihilation burn-down (one-way Boltzmann; production suppressed) ---")
emit("  thermal creation of coherent solitons is exponentially suppressed")
emit("  (Drukier-Nussinov class) -> Y_eq term dropped; annihilation geometric.")
x_i = M_SOL / T_C
emit(f"  x_i = M/T_c = {x_i:.1e}")
results_B = {}
for gstar in (10, 100):
    H_M = 1.66 * sqrt(gstar) * M_SOL**2 / M_PL
    s_M = (2 * pi**2 / 45) * gstar * M_SOL**3
    for Rname, R in (("1/M* (365 GeV)", 1 / MS), ("1/M(1,1) (compact)", 1 / M_SOL)):
        sigma = pi * R**2
        # 1/Y_f = 1/Y_KZ + integral_{x_i}^{inf} lambda(x)/x^2 dx,
        # lambda = s(M) sigma v(x) / H(M), v = min(1, sqrt(3/x))
        def integrand(lnx):
            x = np.exp(lnx)
            v = min(1.0, sqrt(3.0 / x))
            return (s_M * sigma * v / H_M) / x**2 * x   # extra x: d lnx
        I, _ = quad(integrand, log(x_i), log(1e6), limit=400)
        for Y0 in (Y_KZ_min, Y_KZ_max):
            Y_f = 1.0 / (1.0 / Y0 + I)
            results_B[(gstar, Rname, Y0)] = Y_f
        Y_f_mid = 1.0 / (1.0 / Y_KZ_max + I)
        omega = Y_REQ_COEF * M_SOL * Y_f_mid
        emit(f"  g* = {gstar:3d}, R = {Rname:19s}: Y_f = {Y_f_mid:.2e} "
             f"-> Omega h^2 = {omega:.1e}")
Yfs = list(results_B.values())
om_lo = Y_REQ_COEF * M_SOL * min(Yfs)
om_hi = Y_REQ_COEF * M_SOL * max(Yfs)
emit(f"  full band: Omega h^2 (symmetric) in [{om_lo:.0e}, {om_hi:.0e}]")
emit(f"  -> the SYMMETRIC tower component annihilates to irrelevance:")
emit(f"     {log(OMEGA_DM/om_hi)/log(10):.0f}+ orders BELOW the observed dark matter.")
emit(f"  (Y_f is an attractor ~ H/(s sigma v) at T_c: INDEPENDENT of Y_KZ --")
emit(f"   the KZ overproduction is erased, robustly across all bands.)")

# ---------------------------------------------------------------- C. verdict
emit("")
emit("--- C. what CAN make the tower the dark matter: topological asymmetry ---")
Y_B = 8.7e-11
m_p = 0.9383
eta_ratio = Y_REQ / Y_B
emit(f"  required net-charge yield: Y_Delta = {Y_REQ:.2e}")
emit(f"  = (Omega_DM/Omega_B)(m_p/M) x Y_B: check "
     f"{5.36 * (m_p / M_SOL) * Y_B:.2e}  (identity verified)")
emit(f"  i.e. eta_top/eta_B = {eta_ratio:.1e} ~ 5.4 m_p/M(1,1).")
emit(f"  If the Great Condensation generates a NET topological charge with this")
emit(f"  yield (cogenesis with the baryon asymmetry suppressed by m_p/M), the")
emit(f"  anti-solitons annihilate away and the excess survives EXACTLY as")
emit(f"  asymmetric dark matter. This is now a sharp, falsifiable TARGET, not a")
emit(f"  free story. Prediction: NO annihilation signals today (no partners) --")
emit(f"  consistent with, indeed demanded by, the indirect-detection nulls.")

# ---------------------------------------------------------------- D. thermal
emit("")
emit("--- D. the 'unitarity-regime thermal relic' phrasing (Genesis) ---")
v_f = 0.3
sv_unit = 4 * pi / (M_SOL**2 * v_f)
x_f = 35
gstar = 100
omega_th = 1.07e9 * x_f / (sqrt(gstar) * M_PL * sv_unit)
emit(f"  IF the tower were a point particle in thermal equilibrium with")
emit(f"  unitarity-saturating annihilation: Omega h^2 ~ {omega_th:.2f} -- the")
emit(f"  famous ~100 TeV coincidence. BUT solitons cannot reach thermal")
emit(f"  equilibrium from below (coherent-object production is exponentially")
emit(f"  suppressed), so this channel is UNAVAILABLE: the phrasing must be")
emit(f"  revised in the manuscript.")

emit("")
emit("--- E. isocurvature note ---")
emit("  Production at a post-inflationary transition with uniform T_c inherits")
emit("  the adiabatic curvature perturbations; no isocurvature component at")
emit("  leading order for either the KZ or the asymmetric channel. [OK]")

emit("")
emit("=" * 76)
emit("VERDICT (GAP-N4d)")
emit("=" * 76)
emit("1. [COMPUTED] KZ production at the Great Condensation OVERPRODUCES the")
emit("   tower by 8-11 orders; geometric soliton annihilation then erases the")
emit("   symmetric component to Omega h^2 ~ 1e-17..1e-12 -- robustly, across")
emit("   all uncertainty bands. THE SYMMETRIC SCENARIO IS EXCLUDED.")
emit("2. [TARGET] The tower is viable as dark matter ONLY with a primordial")
emit("   topological asymmetry Y_Delta = 2.4e-15 (eta_top ~ 5.4 (m_p/M) eta_B):")
emit("   a quantitative cogenesis target, falsifiable, and predicting null")
emit("   indirect-detection signals.")
emit("3. [REVISION] Genesis's 'unitarity-regime thermal relic' phrasing is")
emit("   unavailable to solitons and must be corrected.")
emit("4. NEW REGISTER ITEM (GAP-N4d-asym): a mechanism generating the net")
emit("   topological charge at the transition (CP-violating condensation")
emit("   dynamics) with the target yield.")

io.open("results/logs/gap_n4d_relic_20260814.log", "w",
        encoding="utf-8").write("\n".join(OUT) + "\n")
print("\nlog written: results/logs/gap_n4d_relic_20260814.log")
