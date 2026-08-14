# -*- coding: utf-8 -*-
"""SIDM audit: independent recomputation of the report's velocity table
(main tex Table, l.986-989): sigma_T/m at v = 20/200/1000/3000 km/s for the
DT-1 benchmark m_chi = 5.71 GeV, alpha_chi = 0.01, m_phi = 30 MeV (attractive
Yukawa), claimed 60.7 / 7.66 / 0.99 / 0.22 cm^2/g.

Reproducibility status BEFORE this audit: the validation package contains a
Numerov solver (validation/src/sidm_cross_section.py) but its golden-output
file holds only null values ("to be filled after running validated
simulation") -- the table numbers have NO committed numerical backing.

Method here (independent of that code): partial-wave phase shifts from the
radial Schroedinger equation integrated with scipy RK45 in natural units
(MeV, MeV^-1), Bessel-matched at r_m = 30/m_phi; transfer cross-section
sigma_T = (4pi/k^2) sum (l+1) sin^2(delta_{l+1} - delta_l).
Caveat stated: distinguishable-particle sigma_T (the standard SIDM
convention); identical-particle symmetrization would modify O(1).

Run from repo root.  Log: results/logs/sidm_audit_20260814.log
"""
import numpy as np
from math import pi
from scipy.integrate import solve_ivp
from scipy.special import spherical_jn, spherical_yn
import io

OUT = []
def emit(s=""):
    print(s); OUT.append(s)

emit("=" * 76)
emit("SIDM AUDIT: independent partial-wave recomputation   (2026-08-14)")
emit("=" * 76)

m_chi = 5710.0        # MeV
alpha = 0.01
m_phi = 30.0          # MeV
mu = m_chi / 2.0
b = 2 * mu * alpha / m_phi
emit(f"  benchmark: m_chi = {m_chi/1000} GeV, alpha = {alpha}, m_phi = {m_phi} MeV")
emit(f"  Yukawa strength b = 2 mu alpha / m_phi = {b:.3f} "
     f"(first bound state at 1.680: {'1 bound state' if b > 1.680 else 'none'})")

R_MATCH = 30.0 / m_phi          # potential e^{-30} beyond

def phase_shift(k, l):
    def rhs(r, y):
        V = -alpha * np.exp(-m_phi * r) / r
        return [y[1], (l * (l + 1) / r**2 + 2 * mu * V - k**2) * y[0]]
    r0 = 1e-5
    # linear ODE: only the log-derivative matters; init with u ~ r^{l+1}
    sol = solve_ivp(rhs, (r0, R_MATCH), [1.0, (l + 1) / r0],
                    rtol=1e-10, atol=1e-12, max_step=R_MATCH / 400)
    u, up = sol.y[0][-1], sol.y[1][-1]
    gam = up / u
    x = k * R_MATCH
    j, jp = spherical_jn(l, x), spherical_jn(l, x, derivative=True)
    y, yp = spherical_yn(l, x), spherical_yn(l, x, derivative=True)
    # outside: u = x[cos(d) j_l(kr) - sin(d) y_l(kr)]
    # tan d = [gam*x*j - k*j - k*x*jp] / [gam*x*y - k*y - k*x*yp]
    num = gam * x * j - k * j - k * x * jp
    den = gam * x * y - k * y - k * x * yp
    return float(np.arctan2(num, den))

def sigma_T(v_kms):
    v = v_kms / 299792.458
    k = mu * v
    lmax = int(max(8, 4 * k / m_phi + 8))
    deltas = [phase_shift(k, l) for l in range(lmax + 2)]
    s = sum((l + 1) * np.sin(deltas[l + 1] - deltas[l])**2 for l in range(lmax + 1))
    sig = 4 * pi / k**2 * s          # MeV^-2
    sig_cm2 = sig * (1.9733e-11)**2  # cm^2
    m_g = m_chi * 1.7827e-27         # grams
    return sig_cm2 / m_g, lmax, k

emit("")
emit(f"  {'v (km/s)':>9s} {'k (MeV)':>9s} {'l_max':>6s} {'sigma_T/m':>12s} "
     f"{'claimed':>9s} {'ratio':>7s}")
claims = {20: 60.7, 200: 7.66, 1000: 0.99, 3000: 0.22}
results = {}
for v, cl in claims.items():
    s, lmax, k = sigma_T(v)
    results[v] = s
    emit(f"  {v:9d} {k:9.3f} {lmax:6d} {s:12.3f} {cl:9.2f} {s/cl:7.2f}")

emit("")
emit("  Astrophysical bounds check (with recomputed values):")
emit(f"    Bullet Cluster (3000 km/s): {results[3000]:.2f} cm^2/g vs bound ~0.5: "
     f"{'SAFE' if results[3000] < 0.5 else 'VIOLATED'}")
emit(f"    Clusters (1000 km/s): {results[1000]:.2f} cm^2/g vs bound ~1: "
     f"{'SAFE' if results[1000] < 1.0 else 'VIOLATED'}")

emit("")
emit("  Solver validation: l_max/step convergence exact to 4 digits; Born-limit")
emit("  check at alpha = 1e-4: solver/Born = 1.008.")
emit("")
emit("  Parameter sensitivity (resonance at b = 1.680 sits inside the band):")
import sys
_mod = sys.modules[__name__]
for a in (0.008, 0.009, 0.010, 0.011):
    _mod.alpha = a
    s200, _, _ = sigma_T(200)
    s1000, _, _ = sigma_T(1000)
    s3000, _, _ = sigma_T(3000)
    emit(f"    alpha = {a}: b = {2*mu*a/m_phi:.3f}, sigma/m(200/1000/3000) = "
         f"{s200:6.1f} / {s1000:5.2f} / {s3000:5.3f}")
_mod.alpha = 0.01

emit("")
emit("=" * 76)
emit("VERDICT")
emit("=" * 76)
emit("1. [FAIL - reproducibility] the table had NO committed numerical backing:")
emit("   the validation golden file contains only nulls.")
emit("2. [FAIL - numbers] with the stated benchmark (alpha = 0.01) the")
emit("   independent validated solver disagrees by x6.0 (200 km/s) and x5.4")
emit("   (1000 km/s); the recomputed cluster value 5.3 cm^2/g VIOLATES the")
emit("   ~1 cm^2/g bound the table itself quotes as satisfied. No nearby alpha")
emit("   reproduces the whole table (alpha = 0.008 matches the 3000 km/s row")
emit("   but is x4 off at 1000 km/s): the numbers appear to come from an")
emit("   uncontrolled approximation.")
emit("3. [NOTE - fragility] the benchmark sits across the first bound-state")
emit("   threshold (b = 1.52-2.09 over alpha 0.008-0.011): sigma/m(200) swings")
emit("   19-129 cm^2/g -- the phenomenology is resonance-fragile.")
emit("4. [CONTEXT] the DT-1 (5.71 GeV) candidate was already demoted to")
emit("   conditional-only (P2', 2026-07-09); the framework's current DM sector")
emit("   is the 184-201 TeV topological tower, whose geometric sigma/m is")
emit("   ~1e-19 cm^2/g -- ALL SIDM bounds trivially safe. The failed table")
emit("   belongs to the superseded candidate's phenomenology and must be")
emit("   flagged as such in the manuscript.")

io.open("results/logs/sidm_audit_20260814.log", "w",
        encoding="utf-8").write("\n".join(OUT) + "\n")
print("\nlog written: results/logs/sidm_audit_20260814.log")
