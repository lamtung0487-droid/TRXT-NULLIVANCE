# Derivation note: the quasi-1D frame for the DOS constant C (GAP-N4c constructive step)

**Date:** 2026-08-14 · **Role:** theorist (inline) · **Status:** SIGNED-OFF with conditions (see audit)
**Code:** `experiments/verification/quasi1d_C_model.py` → `results/logs/quasi1d_C_model_20260814.log`

## 1. Framework declaration (layer separation)

- **Kinematics:** D_e = 5 independent hopping channels from the Cl(6) chirality reduction
  (Γ₆ dependent on Γ₁…Γ₅ on the chiral subspace — verified at machine precision in
  `vf_chain_audit.py`). A q = 6 periodic superstructure imposed on each channel by the
  Abrikosov C₆ vortex lattice (Z₆ holonomy, [LIT] Kleiner–Roth–Autler 1964).
- **Dynamics:** per-channel 1D tight-binding, hopping t = 1/D_e (bandwidth equipartition,
  Schur), plus a core potential V₀ on one site per q-site magnetic cell (vortex core);
  BCS pairing with interaction supported on the core site.
- **Measurement layer:** the BCS coupling constant g_eff = C/X entering
  M* = 2Λ e^{−1/g_eff}.

## 2. Result [THM-level algebra + NUM]

**C = g · D_e · (1/q) · 1/(π v_F), with v_F = 2t·sin(π/q) in consistent radian units,
equals 50/(3π) exactly.**

Factor origins: g = 4 (degeneracy, inherited [OPEN]); D_e channels (Cl(6) [THM]);
1/q = core-projected fraction of each channel's DOS ([NUM] B2: ⟨q·|ψ(core)|²⟩ → 1 as
V₀ → 0); 1/(π v_F) = per-channel 1D DOS at the locked Fermi momentum k_F = 5π/6.

**Locking derived [NUM B1]:** the core comb folds each channel into q = 6 minibands with
gaps at k = nπ/6 (gap = 2|V₀|/q verified); filling ν = 5/6 fills minibands 1–5 exactly →
E_F pinned at the band-5 top edge = unfolded k = 5π/6. The appendix's asserted
"edge-locking k_F = 1 − 1/q" becomes a commensuration statement, conditional on ν = (q−1)/q.

**Coincidence theorem [THM]:** the appendix's mixed-unit 2D formula g·k_F/(π v_F) equals
the quasi-1D expression iff k_F = D_e/q, i.e. **D_e = q − 1** — exactly what Cl(6) gives
(5 = 6 − 1). Counterfactual (D_e, q) pairs break the degeneracy (verified: (5,4) ratio 0.60,
(4,6) ratio 1.25, (7,8) ratio 1.00). The 2D isotropic formula is thus a numerically
coincident rewriting; the unit-mixing pathology and the van Hove obstruction both belonged
to the discarded 2D reading, not to the structure itself.

## 3. What this closes and what it opens

**Closed:** (i) the unit-convention debt (all quantities dimensionless-consistent);
(ii) the 2D-model debt (no Fermi circle is needed; the C₆ triangular band's van Hove
obstruction is moot); (iii) edge-locking upgraded from assertion to conditional theorem.

**Opened / retained:**
1. **Filling ν = (q−1)/q [HYP]** — must come from vortex-core state counting (one empty
   miniband ↔ one core level per cell); not yet derived.
2. **PRIMARY FALSIFIER — core-strength tension [NUM B3]:** the attractive core piles the
   locked edge states onto itself; the pairing-active (core-projected) DOS is enhanced by
   ≈ 4.6·|V₀|^0.75 (empirical over the sampled range, window 6% of bandwidth). Preserving
   the 0.012% C-agreement with m_τ requires |V₀| ≲ 10⁻⁶ bandwidth — physically implausible
   for a vortex core. Either a compensation mechanism exists (renormalization of the
   enhancement into X or the prefactor), or the 0.012% agreement is partly accidental.
3. BCS prefactor 2, cutoff = full M_Pl, g = 4: unchanged [OPEN].

## 4. Falsifiers (declared)

- F-Q1: if vortex state counting gives ν ≠ (q−1)/q, the locking fails → frame dies.
- F-Q2: if no compensation mechanism for the V₀-enhancement is found and the physical core
  strength is O(bandwidth), the 0.012% agreement must be declared partly accidental and
  the M* chain loses its precision claim (ratios survive).
- F-Q3 (internal): any future derivation fixing (D_e, q) with D_e ≠ q − 1 breaks the
  coincidence with the legacy formula and must repropagate M*.

---

## Mathematician audit (inline, same day)

- Algebra of C and the coincidence condition D_e = q−1: **verified** (exact, machine
  precision; counterfactual table checked).
- B1 gap position/magnitude: matches delta-comb perturbation theory (2|V₀|/q, 3%
  second-order deviation at V₀ = −0.02, consistent). Fermi pinning at ν = 5/6: exact by
  construction; the physical content sits entirely in ν — correctly flagged [HYP].
- B2 estimator: window excludes the O(V₀) edge-reconstruction zone; ratios → 1
  monotonically in the sampled V₀ range. Sound.
- B3 estimator history: two normalization bugs (offset ×2π/q-type and ±k branch double
  count) were caught and fixed before acceptance; final estimator's V₀ → 0 limit → 1
  verified analytically and numerically. The 0.75 exponent is empirical; do not quote it
  as a theorem.
- **Sign-off: YES for the manuscript**, with the mandatory conditions that (a) ν = (q−1)/q
  is labeled [HYP], (b) the core-strength tension is presented as the frame's primary
  falsifier, and (c) the coincidence theorem is stated as motivation, not proof, of the
  quasi-1D reading.
