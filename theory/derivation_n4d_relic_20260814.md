# Derivation note: tower relic abundance from the Great Condensation (GAP-N4d)

**Date:** 2026-08-14 · **Role:** theorist + computational (inline) · **Status:** SIGNED-OFF
**Code:** `experiments/verification/gap_n4d_relic.py` → `results/logs/gap_n4d_relic_20260814.log`

## 1. Question

The Genesis chapter claims the 184–201 TeV topological tower is the dark-matter sector,
"produced in the Great Condensation." This note computes the abundance.

## 2. Pipeline and results

**A. Kibble–Zurek production [computed, banded].** At T_c ~ M_cond = 2.3×10¹⁶ GeV the
quench ratio τ_Q/τ₀ = T_c/H_c = 10–101 (g* = 1000–10): a near-Planckian transition is
only moderately slow. With 3D O(3) exponents (ν = 0.71; z ∈ {1,2}) and formation fraction
f ∈ [10⁻³, 10⁻¹]: **Y_KZ ∈ [1.3×10⁻⁷, 3.9×10⁻⁴]** — overproduction vs the required
Y_req = 2.38×10⁻¹⁵ by **8–11 orders** (the monopole-problem situation).

**B. Annihilation burn-down [computed, banded].** Solitons are extended (size ~ 1/M*):
soliton–antisoliton annihilation is geometric and unsuppressed, while *thermal creation*
of coherent solitons is exponentially suppressed (Drukier–Nussinov class) — a one-way
Boltzmann equation. Integrating dY/dx = −(λ/x²)Y² from x_i = M/T_c = 8×10⁻¹²:
the final yield is an attractor ~ H/(sσv)|_{T_c}, **independent of Y_KZ**:

    Ωh²(symmetric) ∈ [3×10⁻¹⁸, 2×10⁻¹²]   (bands: g* 10–100; R = 1/M* or 1/M)

**⇒ THE SYMMETRIC SCENARIO IS EXCLUDED — 11+ orders below the observed dark matter,
robustly across every band.** (An honest null of the first rank: the KZ overproduction
and the annihilation catastrophe cancel into irrelevance, not into 0.12.)

**C. The viable channel: topological asymmetry [target, exact].** If the condensation
generates a net topological charge, anti-solitons annihilate away and the excess
survives as asymmetric dark matter. Required:

    Y_Δ = 2.38×10⁻¹⁵  ⟺  η_top = (Ω_DM/Ω_B)(m_p/M)·η_B ≈ 5.4·(m_p/M)·η_B

i.e. a cogenesis mechanism suppressed relative to baryogenesis by exactly m_p/M(1,1).
Falsifiable structure: asymmetric DM ⇒ **no annihilation signals today** — consistent
with (and now *demanded* by) indirect-detection nulls; the Genesis "absence prediction"
gains a second leg.

**D. Correction to Genesis phrasing.** The "unitarity-bound regime of thermal relics"
suggestion is unavailable: a thermal-equilibrium abundance (which would give
Ωh² ~ 0.25 for a point particle at unitarity — the famous ~100 TeV coincidence) requires
thermal *production*, exponentially suppressed for coherent solitons. Phrasing revised.

**E. Isocurvature [OK].** Post-inflationary uniform-T_c production inherits adiabatic
perturbations; no leading-order isocurvature in either channel.

## 3. Register

- GAP-N4d: **partially closed** — production computed, symmetric channel excluded,
  asymmetric target quantified.
- **NEW: GAP-N4d-asym** — derive the net topological charge of the condensation
  (CP-violating transition dynamics) with yield Y_Δ = 2.4×10⁻¹⁵.

## Falsifiers

- F-R1: a confirmed DM annihilation signal (e.g. Galactic-Center line at ~90 TeV) would
  contradict the asymmetric channel → tower-as-DM dies entirely (symmetric already dead).
- F-R2: a future mechanism computation giving η_top orders away from the target kills
  the tower-DM identification.
- F-R3: detection of a stable ~200 TeV relic abundance *above* the asymmetric target.

---

## Mathematician audit (inline, same day)

- KZ scaling exponents and quench identification standard [LIT]; bands honest.
- Boltzmann reduction: the 1/x² integral is dominated by x_i, giving the attractor
  Y_f ≈ x_i·H(M)/(s(M)σv) — verified analytically and numerically; the conclusion is
  insensitive to Y_KZ, v-treatment, and both R choices (11 orders of margin).
- Dropping the production term requires the Drukier–Nussinov suppression argument [LIT];
  it is the load-bearing qualitative input and is correctly flagged.
- The asymmetric-target identity Y_Δ = (Ω_DM/Ω_B)(m_p/M)Y_B is exact bookkeeping.
- **Sign-off: YES.** Conditions: quote the symmetric exclusion with its band; keep
  [LIT] tags on the two borrowed suppression/exponent inputs; GAP-N4d-asym enters the
  register as open.
