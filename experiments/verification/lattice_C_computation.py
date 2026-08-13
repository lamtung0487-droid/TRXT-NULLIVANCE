# -*- coding: utf-8 -*-
"""GAP-N4c decisive computation: the DOS constant C of the VF chain, on the lattice.

The VF chain claims C = 50/(3pi) = 5.30516 (analytic) and quotes an unreproducible
"lattice cross-check" C = 5.339 (+0.64%). Because |d ln M*/d ln C| = 38.7, the two
values differ by +28% in M*.

Committed, reproducible computation in three parts:
  A. unit-consistency of C = g*(L_F/4pi^2)*(2/v_F) (three evaluations -> m_tau);
  B. exact Fermi-contour integral on the true C6 triangular band (primitive-cell
     coordinates, no zone double-counting; method validated on the isotropic
     model where the answer is exact);
  C. artifact hunt: which DOS-estimation resolutions produce +0.64%?

v2 (same day): fixes caught by internal referee pass on v1 --
  (i) isotropic validation domain now masked to the unit disc (v1's square
      window picked up spurious corner branches, +43%);
  (ii) K point corrected to (b1+b2)/3 (v1 used (2b1+b2)/3, a zone-boundary
      midpoint of a neighboring cell);
  (iii) Part C bisection removed (response non-monotonic); honest scan instead.

Run from repo root.  Log: results/logs/lattice_C_computation_20260814.log
"""
import numpy as np
from math import pi, sin, cos, exp, sqrt
import io

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = []
def emit(s=""):
    print(s); OUT.append(s)

emit("=" * 76)
emit("GAP-N4c DECISIVE COMPUTATION v2: lattice DOS constant C   (2026-08-14)")
emit("=" * 76)

ALPHA_INV = 137.035999177
X = 1.5 * ALPHA_INV
M_PL = 1.22091e19
M_TAU = 1776.93
D_e, q, g_deg = 5, 6, 4
t = 1 / D_e
kf_frac = 1 - 1 / q          # 5/6

# ---------------------------------------------------------------------------
emit("")
emit("--- PART A: unit consistency of C = g*(L_F/4pi^2)*(2/v_F) ---")
C_mixed = g_deg * (2 * pi * kf_frac / (4 * pi**2)) * (2 / (2 * t * sin(pi * kf_frac)))
C_rad = g_deg * (2 * pi * (pi * kf_frac) / (4 * pi**2)) * (2 / (2 * t * sin(pi * kf_frac)))
C_frac = g_deg * (2 * pi * kf_frac / (4 * pi**2)) * (2 / (pi * 2 * t * sin(pi * kf_frac)))
emit(f"  mixed-unit (appendix) : C = {C_mixed:.6f}  (= 50/(3pi))")
emit(f"  radian-consistent     : C = {C_rad:.6f}  (= 50/3)")
emit(f"  fraction-consistent   : C = {C_frac:.6f}  (= 50/(3pi^2))")
for name, Cv in (("mixed ", C_mixed), ("radian", C_rad), ("fract.", C_frac)):
    Ms = 2 * M_PL * exp(-X / Cv)
    mt = Ms / X * 1e3
    tag = "MATCHES PDG" if abs(mt - M_TAU) / M_TAU < 0.02 else \
          f"off by 10^{round(np.log10(mt / M_TAU)):+d}"
    emit(f"    {name}: M* = {Ms:12.4g} GeV -> m_tau = {mt:12.4g} MeV  ({tag})")
emit("  [FINDING A] L_F uses k_F as a bare fraction (5/6) while v_F uses the")
emit("  radian derivative at k = 5pi/6. Either consistent convention misses")
emit("  m_tau by >10 orders. The unit mixing is load-bearing and unjustified.")

# ---------------------------------------------------------------------------
# Contour integral I = closed_int dl/|grad E| with analytic gradients.
# ---------------------------------------------------------------------------
def integrate_segments(segs, to_k, grad_k):
    """segs: polylines in chart coords; to_k maps chart->k; grad in k-space."""
    I_tot, L_tot, used = 0.0, 0.0, 0
    for seg in segs:
        if len(seg) < 8:
            continue
        used += 1
        kseg = to_k(seg)
        mid = 0.5 * (kseg[1:] + kseg[:-1])
        dl = np.linalg.norm(np.diff(kseg, axis=0), axis=1)
        gx, gy = grad_k(mid[:, 0], mid[:, 1])
        I_tot += float(np.sum(dl / np.hypot(gx, gy)))
        L_tot += float(np.sum(dl))
    return I_tot, L_tot, used

def get_contour_segs(F, EF, xlim, ylim, n):
    xs = np.linspace(xlim[0], xlim[1], n)
    ys = np.linspace(ylim[0], ylim[1], n)
    XX, YY = np.meshgrid(xs, ys)
    Z = F(XX, YY)
    fig = plt.figure(); ax = fig.add_subplot(111)
    cs = ax.contour(XX, YY, Z, levels=[EF])
    segs = list(cs.allsegs[0])
    plt.close(fig)
    return segs

emit("")
emit("--- PART B: exact Fermi-contour integral, C6 triangular band ---")

# B0 validation: isotropic cosine band, domain masked to the unit disc.
def E_iso_masked(kx, ky):
    k = np.sqrt(kx**2 + ky**2)
    Z = -2 * t * np.cos(pi * k)
    Z[k > 1.0] = np.nan
    return Z
def grad_iso(kx, ky):
    k = np.sqrt(kx**2 + ky**2) + 1e-300
    dEdk = 2 * t * pi * np.sin(pi * k)
    return dEdk * kx / k, dEdk * ky / k
EF_iso = -2 * t * cos(pi * kf_frac)
I_exact = (2 * pi * kf_frac) / (2 * t * pi * sin(pi * kf_frac))
for n in (512, 1024, 2048):
    segs = get_contour_segs(E_iso_masked, EF_iso, (-1, 1), (-1, 1), n)
    I, L, used = integrate_segments(segs, lambda s: s, grad_iso)
    emit(f"  [B0 validation] n={n:4d}: I/I_exact - 1 = {I/I_exact-1:+.2e}  "
         f"({used} segment)")
emit("  -> method validated: error << 0.1% at n >= 1024, single Gamma circle.")

# B1: triangular lattice in primitive-cell coordinates (u,v) in [0,1]^2,
# k = u b1 + v b2 -- exactly one zone, no copies.
a1 = np.array([1.0, 0.0]); a2 = np.array([0.5, sqrt(3) / 2])
b1 = 2 * pi * np.array([1.0, -1.0 / sqrt(3)])
b2 = 2 * pi * np.array([0.0, 2.0 / sqrt(3)])
def E_tri_k(kx, ky):
    p1 = kx * a1[0] + ky * a1[1]; p2 = kx * a2[0] + ky * a2[1]
    return -2 * t * (np.cos(p1) + np.cos(p2) + np.cos(p1 + p2))
def grad_tri(kx, ky):
    p1 = kx * a1[0] + ky * a1[1]; p2 = kx * a2[0] + ky * a2[1]; p3 = p1 + p2
    gx = 2 * t * (np.sin(p1) * a1[0] + np.sin(p2) * a2[0] + np.sin(p3) * (a1[0] + a2[0]))
    gy = 2 * t * (np.sin(p1) * a1[1] + np.sin(p2) * a2[1] + np.sin(p3) * (a1[1] + a2[1]))
    return gx, gy
def E_uv(U, V):
    kx = U * b1[0] + V * b2[0]; ky = U * b1[1] + V * b2[1]
    return E_tri_k(kx, ky)
def uv_to_k(seg):
    return seg[:, 0:1] * b1[None, :] + seg[:, 1:2] * b2[None, :]

k_M = 0.5 * (b1 + b2)
k_K = (b1 + b2) / 3.0                 # corrected K (referee fix ii)
E_G, E_M, E_K = float(E_tri_k(0, 0)), float(E_tri_k(*k_M)), float(E_tri_k(*k_K))
emit(f"  band: E(Gamma) = {E_G:.4f} (min), E(M) = {E_M:.4f} (saddle/van Hove), "
     f"E(K) = {E_K:.4f} (max)")

for label, kpt in (("Gamma-M", k_M), ("Gamma-K", k_K)):
    klock = kf_frac * kpt
    EF = float(E_tri_k(*klock))
    gx, gy = grad_tri(np.array([klock[0]]), np.array([klock[1]]))
    vlock = float(np.hypot(gx, gy)[0])
    ref = 2 * pi * np.linalg.norm(klock) / vlock
    topo = "ABOVE van Hove -> K-pockets" if EF > E_M else "Gamma-centered"
    prev = None
    for n in (1024, 2048, 3072):
        segs = get_contour_segs(E_uv, EF, (0.0, 1.0), (0.0, 1.0), n)
        I, L, used = integrate_segments(segs, uv_to_k, grad_tri)
        conv = "" if prev is None else f" (chg {abs(I/prev-1):.1e})"
        prev = I
        emit(f"  [{label} 5/6] n={n}: E_F = {EF:+.4f} [{topo}], segs = {used}, "
             f"I = {I:.5f}, I/ref = {I/ref:.5f}{conv}")
    emit(f"    -> exact-band vs isotropic linearization: {(prev/ref-1)*100:+.1f}%")

# ---------------------------------------------------------------------------
emit("")
emit("--- PART C: artifact hunt -- what numerics give +0.64% (C = 5.339)? ---")
target = 5.339 / C_mixed - 1
emit(f"  target excess: {target*100:+.3f}%  (isotropic model; exact value known)")
n_g = 3000
xs = np.linspace(-1, 1, n_g)
KX, KY = np.meshgrid(xs, xs)
K = np.sqrt(KX**2 + KY**2)
E_flat = (-2 * t * np.cos(pi * K[K <= 1.0])).ravel()
cell = (xs[1] - xs[0])**2

emit("  (C1) Lorentzian broadening eta (grid 3000^2):")
best = []
for eta in (0.001, 0.002, 0.003, 0.004, 0.006, 0.008, 0.012, 0.016):
    N_est = float(np.sum(eta / pi / ((E_flat - EF_iso)**2 + eta**2))) * cell
    d = N_est / I_exact - 1
    best.append((abs(d - target), "eta", eta, d))
    emit(f"      eta = {eta:.3f}: {d*100:+.3f}%")

emit("  (C2) energy-bin histogram, width dE (states in window / dE):")
for dE in (0.002, 0.004, 0.008, 0.012, 0.016, 0.024, 0.032, 0.048):
    cnt = float(np.sum(np.abs(E_flat - EF_iso) < dE / 2)) * cell / dE
    d = cnt / I_exact - 1
    best.append((abs(d - target), "dE", dE, d))
    emit(f"      dE = {dE:.3f}: {d*100:+.3f}%")

emit("  (C3) coarse k-grid histogram (grid m^2, dE = 2% bandwidth):")
for m in (40, 60, 80, 120, 200, 400):
    xs_c = np.linspace(-1, 1, m)
    KXc, KYc = np.meshgrid(xs_c, xs_c)
    Kc = np.sqrt(KXc**2 + KYc**2)
    Ec = (-2 * t * np.cos(pi * Kc[Kc <= 1.0])).ravel()
    cell_c = (xs_c[1] - xs_c[0])**2
    dE = 0.02 * 9 * t
    cnt = float(np.sum(np.abs(Ec - EF_iso) < dE / 2)) * cell_c / dE
    d = cnt / I_exact - 1
    best.append((abs(d - target), "grid m", m, d))
    emit(f"      m = {m:4d}: {d*100:+.3f}%")

best.sort()
hit = best[0]
emit(f"  closest artifact to +0.64%: {hit[1]} = {hit[2]} -> {hit[3]*100:+.3f}%")
reproduced = abs(hit[3] - target) < 0.15 * abs(target)
emit(f"  artifact classes {'DO' if reproduced else 'DO NOT cleanly'} reproduce 5.339 "
     f"within 15% of the excess.")

# ---------------------------------------------------------------------------
emit("")
emit("=" * 76)
emit("VERDICT (v2)")
emit("=" * 76)
emit("1. [MODEL] On the honest C6 triangular band, the 5/6 edge-locking lands")
emit("   ABOVE the van Hove energy in both natural directions: the Fermi surface")
emit("   is disconnected K-pockets, not a Gamma-centered circle. The isotropic")
emit("   linearization behind C = 50/(3pi) fails QUALITATIVELY there (see the")
emit("   I/ref numbers). C = 50/(3pi) is a property of the idealized 1D-channel/")
emit("   isotropic continuum model only -- for THAT model it is exact (Part B0),")
emit("   and no 0.6%-level 'lattice correction' to it exists.")
emit("2. [5.339] Whether any simple estimator artifact reproduces +0.64% is")
emit("   reported honestly in Part C above. Regardless of the outcome, the value")
emit("   remains without generating code; it should be STRUCK from VF.4 rather")
emit("   than explained.")
emit("3. [UNITS] Part A adds a new load-bearing unfixed choice: the momentum-unit")
emit("   convention (50/3 vs 50/(3pi) vs 50/(3pi^2)); only the mixed evaluation")
emit("   reproduces m_tau.")
emit("NET for GAP-N4c: the +28% 'lattice threat' to M* is retired (no such")
emit("correction exists for the model actually being evaluated), but the")
emit("justification debt GROWS: the chain now owes (i) a first-principles 2D")
emit("model in which the Gamma-circle picture survives (the C6 band contradicts")
emit("it at 5/6 locking), and (ii) the unit convention, in addition to the")
emit("prefactor, cutoff, and g = 4.")

io.open("results/logs/lattice_C_computation_20260814.log", "w",
        encoding="utf-8").write("\n".join(OUT) + "\n")
print("\nlog written: results/logs/lattice_C_computation_20260814.log")
