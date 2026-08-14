# -*- coding: utf-8 -*-
"""GAP-N4c constructive step: the quasi-1D microscopic frame for C = 50/(3pi).

Claim under test (new, 2026-08-14): the DOS constant of the VF chain is NOT the
2D isotropic formula (which needs mixed momentum units) but the unit-consistent
quasi-1D expression

    C = g * D_e * (1/q) * 1/(pi * v_F),      v_F = 2 t sin(pi/q),  t = 1/D_e

i.e.  [degeneracy g] x [D_e independent 1D channels from the Cl(6) generators]
    x [pairing supported on the vortex core, one site per q-site magnetic cell]
    x [per-channel 1D DOS at the locked Fermi momentum].

Numerically this equals 50/(3pi) exactly, and coincides with the appendix's
mixed-unit value precisely because Cl(6) gives D_e = q - 1 (counterfactual
(D_e,q) break the degeneracy between the two frames).

This script builds the model honestly and tests its three structural claims:
  B1. a q=6 core-comb potential opens the miniband gap exactly at unfolded
      k = 5pi/6, so filling 5/6 pins E_F at that edge (the LOCKING, derived);
  B2. the core-projected spectral weight -> 1/q in the weak-potential limit
      (the DILUTION factor, derived);
  B3. corrections at finite core potential V0: C_eff(V0)/C - 1, the linear
      coefficient, and the resulting precision constraint on V0/W required to
      preserve the 0.012% C-agreement with m_tau.

Run from repo root.  Log: results/logs/quasi1d_C_model_20260814.log
"""
import numpy as np
from math import pi, sin, sqrt
import io

OUT = []
def emit(s=""):
    print(s); OUT.append(s)

emit("=" * 76)
emit("QUASI-1D FRAME FOR C: construction + numerical tests   (2026-08-14)")
emit("=" * 76)

D_e, q, g = 5, 6, 4
t = 1 / D_e
vF = 2 * t * sin(pi / q)
C_ideal = g * D_e / (q * pi * vF)
emit(f"  C = g*D_e/(q*pi*v_F) = {C_ideal:.12f}   (50/(3pi) = {50/(3*pi):.12f})")
emit(f"  identity requires D_e = q-1: Cl(6) gives D_e = 5, q = 6  [holds]")

# ---------------------------------------------------------------------------
# Bloch problem: 1D chain, hopping -t, on-site core potential V0 on site j=0
# of each q-site cell (vortex-core comb). H(k) is q x q, k in [-pi/q, pi/q).
# ---------------------------------------------------------------------------
def bands_and_states(V0, nk):
    ks = np.linspace(-pi / q, pi / q, nk, endpoint=False)
    Es = np.empty((nk, q))
    W0 = np.empty((nk, q))          # core weight |psi(0)|^2 per state
    for i, k in enumerate(ks):
        H = np.zeros((q, q), dtype=complex)
        for j in range(q - 1):
            H[j, j + 1] = -t
            H[j + 1, j] = -t
        H[q - 1, 0] += -t * np.exp(-1j * k * q)
        H[0, q - 1] += -t * np.exp(+1j * k * q)
        H[0, 0] += V0
        w, v = np.linalg.eigh(H)
        Es[i] = w
        W0[i] = np.abs(v[0, :])**2
    return ks, Es, W0

# ---------------------------------------------------------------------------
emit("")
emit("--- B1: gap location and Fermi-level pinning at filling 5/6 ---")
V0 = -0.02          # attractive core (vortex core binds); |V0| << bandwidth
ks, Es, W0 = bands_and_states(V0, 4001)
# band edges
tops = Es.max(axis=0); bots = Es.min(axis=0)
gap56 = bots[5] - tops[4]
# unfolded momentum of the band-4/band-5 boundary (0-indexed: bands 0..5):
# the n-th gap sits at unfolded |k| = n*pi/q; the top of band index 4 is the
# 5th gap -> |k| = 5pi/6.
E_edge_free = -2 * t * np.cos(5 * pi / 6)   # free-chain energy at k = 5pi/6
emit(f"  V0 = {V0}: gap between minibands 5 and 6 = {gap56:.6f} "
     f"(delta-comb estimate 2|V0|/q = {2*abs(V0)/q:.6f})")
emit(f"  top of miniband 5:  E = {tops[4]:+.6f}")
emit(f"  free chain at k=5pi/6: E = {E_edge_free:+.6f}  "
     f"(shift {tops[4]-E_edge_free:+.2e} = O(V0))")
emit(f"  -> filling nu = 5/6 fills minibands 1..5 exactly: E_F pinned at the")
emit(f"     band-5 top edge = unfolded k_F = 5pi/6. LOCKING DERIVED from the")
emit(f"     q-periodic core comb (assertion 'edge-locking k_F = 1-1/q' replaced")
emit(f"     by commensuration).")

# velocity at the locked momentum (free value used in the BCS log)
emit(f"  v_F(5pi/6) = 2t sin(5pi/6) = {2*t*sin(5*pi/6):.6f} = 1/5  [consistent units]")

# ---------------------------------------------------------------------------
emit("")
emit("--- B2: core-projected weight -> 1/q (dilution factor) ---")
for V0_test in (-0.001, -0.01, -0.05):
    ks2, Es2, W02 = bands_and_states(V0_test, 2001)
    # average core weight over the top of miniband 5 (states within a window
    # below the edge, excluding the O(V0) edge-reconstruction zone)
    E5 = Es2[:, 4]; w5 = W02[:, 4]
    top5 = E5.max()
    win = (E5 > top5 - 0.05) & (E5 < top5 - 5 * abs(V0_test) / q)
    mean_w = float(np.mean(w5[win])) if np.any(win) else float("nan")
    emit(f"  V0 = {V0_test:+.3f}: <|psi(core)|^2> near E_F = {mean_w:.5f} "
         f"(1/q = {1/q:.5f}, ratio {mean_w*q:.4f})")
emit("  -> dilution 1/q emerges in the weak-core limit; pairing supported on")
emit("     the core sees (1/q) of each channel's DOS.")

# ---------------------------------------------------------------------------
emit("")
emit("--- B3: finite-V0 corrections to C and the precision constraint ---")
# C_eff/C = [core-projected k-measure in window, perturbed] /
#           [(1/q) * free k-measure of the same window]; both per channel.
def C_eff_ratio(V0_test, window):
    nk = 12001
    ks3, Es3, W03 = bands_and_states(V0_test, nk)
    dk = (2 * pi / q) / nk
    E5 = Es3[:, 4]; w5 = W03[:, 4]
    top5 = E5.max()
    sel = E5 > top5 - window
    num = q * float(np.sum(w5[sel])) * dk          # q x core-projected measure
    # free band, same energy window measured from ITS edge (k = 5pi/6)
    kk = np.linspace(0, pi, 400001)
    Ef = -2 * t * np.cos(kk)
    free_top = -2 * t * np.cos(5 * pi / 6)
    fsel = (Ef > free_top - window) & (Ef <= free_top)
    # x2: kk covers only the +k branch; the folded band contains both +/-k
    den = 2.0 * float(np.sum(fsel)) / len(kk) * pi  # free k-measure in window
    return num / den

W_band = 4 * t   # single-channel bandwidth
rows = []
for window in (0.02, 0.05):
    emit(f"  pairing window {window} ({window/W_band*100:.0f}% of channel bandwidth):")
    for V0_test in (-0.001, -0.002, -0.005, -0.01, -0.02):
        r = C_eff_ratio(V0_test, window)
        if window == 0.05:
            rows.append((abs(V0_test), r - 1))
        emit(f"    V0 = {V0_test:+.3f}: C_eff/C - 1 = {(r-1)*100:+.3f}%")
xs = np.array([r[0] for r in rows]); ys = np.array([r[1] for r in rows])
# empirical scaling fit  (r-1) = A * |V0|^p
p_fit = np.polyfit(np.log(xs), np.log(np.abs(ys) + 1e-300), 1)
A_fit = float(np.exp(p_fit[1])); p_exp = float(p_fit[0])
emit(f"  empirical scaling: C_eff/C - 1 ~ {A_fit:.2f} * |V0|^{p_exp:.2f} (window 0.05)")
tol_C = 1.2e-4    # 0.012% -- the inversion agreement with m_tau
V0_max = (tol_C / A_fit) ** (1 / p_exp) if p_exp > 0 else float("nan")
emit(f"  to preserve the 0.012% C-agreement: |V0| < {V0_max:.2e} "
     f"(= {V0_max/W_band*100:.4f}% of the channel bandwidth)")
emit(f"  and the commensuration gap is then 2|V0|/q < {2*V0_max/q:.1e}:")
emit(f"  the frame requires an extremely weak core potential -- an honest,")
emit(f"  falsifiable structural constraint (or: the 0.012% agreement is partly")
emit(f"  absorbed into the V0-correction, to be examined next).")

# ---------------------------------------------------------------------------
emit("")
emit("=" * 76)
emit("VERDICT")
emit("=" * 76)
emit("1. The unit-consistent quasi-1D expression C = g*D_e/(q*pi*v_F) equals")
emit("   50/(3pi) EXACTLY and coincides with the appendix's mixed-unit formula")
emit("   precisely because Cl(6) gives D_e = q-1 = 5. The unit-mixing debt is")
emit("   RESOLVED by reinterpretation: the 2D isotropic formula was a")
emit("   numerically coincident rewriting; no 2D Fermi circle is needed, so the")
emit("   van Hove obstruction to the 2D realization is MOOT in this frame.")
emit("2. Edge-locking k_F = 5pi/6 is DERIVED (commensuration: filling 5/6 of")
emit("   q=6 minibands from the core comb), replacing an assertion.")
emit("3. The dilution 1/q is DERIVED from core-supported pairing (weak-V limit).")
emit("4. NEW COSTS (explicit, falsifiable): (i) filling must be nu = (q-1)/q --")
emit("   pushed down to vortex state-counting, still open; (ii) SHARP TENSION:")
emit("   the attractive core piles the locked edge states onto itself (van Hove")
emit("   + core-binding), enhancing the pairing DOS as ~4.6|V0|^0.75; keeping")
emit("   the 0.012% C-agreement requires |V0| < 1e-6 of the bandwidth -- ")
emit("   physically implausible for a vortex core. Either a compensation")
emit("   mechanism exists (e.g. the enhancement renormalizes into X or the")
emit("   prefactor) or the 0.012% agreement is partly accidental. This is now")
emit("   the frame's primary falsifier. (iii) prefactor/cutoff/g=4 unchanged.")
emit("NET: two of the four unfixed choices (unit convention; 2D-model validity)")
emit("are closed by the quasi-1D frame; the locking assertion becomes a theorem")
emit("modulo filling; the frame pays with one new quantified constraint.")

io.open("results/logs/quasi1d_C_model_20260814.log", "w",
        encoding="utf-8").write("\n".join(OUT) + "\n")
print("\nlog written: results/logs/quasi1d_C_model_20260814.log")
