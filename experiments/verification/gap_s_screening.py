# -*- coding: utf-8 -*-
"""GAP-S: screening re-derivation with fixed sign bookkeeping (resolves I-12).

Signature fixed once: (+,-,-,-), X = (1/2) g^{mu nu} d phi d phi.
Static spherical profile: X = -(1/2) phi'^2 < 0.  Timelike (cosmology): X = +(1/2) phidot^2.

PART 1 -- BRANCH DICHOTOMY THEOREM (pure P(X)):
  The static EoM integrates to the flux law  P_X(phi') * phi' = S(r),
  S(r) = beta M / (4 pi M_Pl r^2).  For the DBI pair:
    Branch A (G0b-healthy):  P = L^4 (1 - sqrt(1 - 2X/L^4))
        statics: P_X = (1 + phi'^2/L^4)^(-1/2)  -> flux SATURATES at L^2:
        no static solution where S > L^2, and phi' > S below it (ANTI-screening);
        timelike: c_s^2 = 1 - phidot^2/L^4 <= 1 (subluminal, why G0b chose it).
    Branch B (screening):     P = L^4 (sqrt(1 + 2|X|/L^4) - 1)-type
        statics: P_X = (1 - phi'^2/L^4)^(-1/2) -> phi' <= L^2 bounded,
        force saturates -> SCREENS (eps ~ r^2);
        timelike: c_s^2 = 1 + phidot^2/L^4 >= 1 (superluminal -> fails G0).
  => within pure P(X), {G0-healthy} and {k-mouflage screening} are mutually
  exclusive branches. I-12 is therefore not a bookkeeping slip but a real
  obstruction: the old Sec 9.3 'derived Vainshtein (r/r_V)^(3/2)' story cannot
  come from the declared action (X^2 k-mouflage would give 4/3; the 3/2 needs
  a cubic galileon (d phi)^2 box phi, absent from the action).

PART 2 -- THE OPERATIVE, CONSISTENT SCREENING:
  The G3-validated interpolation (standard form, root of
  g^4 - g_N^2 g^2 - g_N^2 a0^2 = 0) has the high-acceleration expansion
  g_tot = g_N sqrt(1+u^2) ~ g_N (1 + u^2/2), u = a0/g_N: the fifth-force
  fraction is delta = u^2/2, PARAMETER-FREE given a0 from Gate 3 (3350
  (km/s)^2/kpc -> 1.0854e-10 m/s^2). Solar-system table + Cassini margin.
  The earlier pre-registered Neptune/Pluto values (1.8e-5, 3.2e-5) equal the
  FIRST power u -- the tail of the 'simple' mu-function, inconsistent with the
  G3-validated standard form: corrected here (ledger-logged; no ranging data
  at that precision exists, so the prediction update is legitimate and dated).

Run from repo root.  Log: results/logs/gap_s_screening_20260814.log
"""
import numpy as np
from math import pi, sqrt
import io

OUT = []
def emit(s=""):
    print(s); OUT.append(s)

emit("=" * 76)
emit("GAP-S: SCREENING RE-DERIVATION (I-12 resolution)   (2026-08-14)")
emit("=" * 76)

# ------------------------------------------------------- Part 1: dichotomy
emit("")
emit("--- PART 1: branch dichotomy (pure P(X), statics vs timelike) ---")
L2 = 1.0                       # Lambda^2 in units where it = 1
S_over_L2 = np.logspace(-2, 1.5, 200)

def phi_branch_A(S):           # flux phi'/sqrt(1+phi'^2) = S  (units L=1)
    if S >= 1.0:
        return np.nan          # saturation: no static solution
    return S / sqrt(1 - S**2)

def phi_branch_B(S):           # flux phi'/sqrt(1-phi'^2) = S -> phi' bounded
    return S / sqrt(1 + S**2)

rows = []
for S in (0.03, 0.3, 0.9, 0.999, 1.5, 10.0):
    pA = phi_branch_A(S)
    pB = phi_branch_B(S)
    eA = pA / S if np.isfinite(pA) else float("nan")   # force / linear force
    eB = pB / S
    rows.append((S, pA, eA, pB, eB))
emit(f"  {'S/L^2':>8s} | {'phi_A':>9s} {'F_A/F_lin':>10s} | {'phi_B':>9s} {'F_B/F_lin':>10s}")
for S, pA, eA, pB, eB in rows:
    sA = f"{pA:9.3f} {eA:10.3f}" if np.isfinite(pA) else "  NO SOLUTION (flux>L^2)"
    emit(f"  {S:8.3f} | {sA:>20s} | {pB:9.4f} {eB:10.4f}")
emit("  Branch A (G0b-healthy): force/linear >= 1 and DIVERGES as S -> L^2;")
emit("    beyond that no static solution: ANTI-screening + obstruction.")
emit("  Branch B: force saturates at L^2 -> screening eps ~ (r/r_K)^2; but its")
emit("    timelike c_s^2 = 1 + phidot^2/L^4 > 1: fails the G0 criterion.")
emit("  [THEOREM] pure P(X): G0-healthy XOR k-mouflage-screening. I-12 is a")
emit("  real obstruction, not a sign slip. The X^2-EFT limit gives eps ~ r^{4/3}")
emit("  in the screening branch; the manuscript's 3/2 exponent matches NEITHER")
emit("  (it is the cubic-galileon law; no such term exists in the action).")

# ------------------------------------------------------- Part 2: operative
emit("")
emit("--- PART 2: operative screening from the G3-validated law ---")
G = 6.67430e-11; M_sun = 1.989e30; AU = 1.496e11
a0 = 3350 * 3.24e-14           # G3 (2026-08-13 rerun, interior optimum) -> SI
emit(f"  a0 = 3350 (km/s)^2/kpc = {a0:.4e} m/s^2 (Gate-3 provenance)")
emit(f"  g_tot = g_N sqrt(1+u^2), u = a0/g_N  =>  delta = sqrt(1+u^2)-1 ~ u^2/2")
emit(f"  {'body':<10s} {'r (AU)':>7s} {'g_N (m/s^2)':>12s} {'u=a0/g_N':>10s} "
     f"{'delta (exact)':>13s} {'old presc. (u)':>14s}")
planets = [("Mercury", 0.387), ("Earth", 1.0), ("Saturn", 9.537),
           ("Uranus", 19.19), ("Neptune", 30.07), ("Pluto", 39.48)]
for name, rau in planets:
    gN = G * M_sun / (rau * AU)**2
    u = a0 / gN
    delta = sqrt(1 + u**2) - 1
    emit(f"  {name:<10s} {rau:7.2f} {gN:12.3e} {u:10.2e} {delta:13.2e} {u:14.2e}")
gN_sat = G * M_sun / (9.537 * AU)**2
delta_sat = sqrt(1 + (a0 / gN_sat)**2) - 1
emit(f"  Cassini bound at Saturn: 2.3e-5; predicted delta = {delta_sat:.1e}")
emit(f"  -> margin {2.3e-5/delta_sat:.0e}x. PASS with seven orders to spare.")
emit("  CORRECTION OF PRE-REGISTERED PREDICTIONS: the earlier Neptune/Pluto")
emit("  values 1.8e-5/3.2e-5 equal u (the 'simple'-mu tail) -- inconsistent")
emit("  with the standard form validated at G3. Corrected predictions:")
gNn = G * M_sun / (30.07 * AU)**2; gNp = G * M_sun / (39.48 * AU)**2
emit(f"    Neptune: delta = {sqrt(1+(a0/gNn)**2)-1:.1e}   Pluto: delta = {sqrt(1+(a0/gNp)**2)-1:.1e}")
emit("  (no ranging data at either precision exists; the update is dated and")
emit("  ledger-logged BEFORE any confrontation -- Honest Null compliant.)")
emit("  FALSIFIER: any future detection of a fifth-force fraction ~ 1e-5 at")
emit("  Neptune/Pluto would CONTRADICT the standard form and revive simple-mu.")

emit("")
emit("=" * 76)
emit("VERDICT")
emit("=" * 76)
emit("1. I-12 RESOLVED as a theorem: the declared action's healthy branch does")
emit("   not k-mouflage-screen; the screening branch is superluminal. The old")
emit("   Sec 9.3 'endogenous Vainshtein (r/r_V)^{3/2}' derivation is struck.")
emit("2. Solar-system safety does NOT depend on that mechanism: the")
emit("   G3-validated interpolation law itself suppresses the fifth force as")
emit("   u^2/2 (parameter-free), passing Cassini by ~7 orders.")
emit("3. OPEN (register): the microscopic origin of the interpolation function")
emit("   (the resummation that produces the standard mu from the condensate)")
emit("   -- GAP-S continues at that level, now with the dichotomy theorem as a")
emit("   hard constraint on any candidate derivation.")

io.open("results/logs/gap_s_screening_20260814.log", "w",
        encoding="utf-8").write("\n".join(OUT) + "\n")
print("\nlog written: results/logs/gap_s_screening_20260814.log")
