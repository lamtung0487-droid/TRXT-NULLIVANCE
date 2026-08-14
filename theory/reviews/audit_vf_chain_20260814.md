# Independent Audit: Master-Scale Chain Cl(6) → v_F → C → M* (GAP-N4c)

**Date:** 2026-08-14 · **Auditor role:** mathematician (inline) · **Subject:** Appendix VF
(`paper/v7_release_v2/appendices/Appendix_VF_MasterScale.tex`)
**Evidence:** `experiments/verification/vf_chain_audit.py` → `results/logs/vf_chain_audit_20260814.log`

## Scope

The VF chain anchors every absolute mass in the framework
(M_stage = M* in the Genesis tower; m_τ = (2α/3)M*). It was inherited from the
February compilation without independent audit — flagged as GAP-N4c. This audit
recomputes each step from scratch and quantifies the chain's sensitivity structure.

## Findings

### Verified (machine precision unless noted)

| Step | Claim | Result |
|---|---|---|
| VF.1 | Cl(6): Γ₇²=1; Γ₆ = +iΓ₅Γ₄Γ₃Γ₂Γ₁ on chiral subspace ⇒ D_e = 5 | PASS — independent 8×8 rep built from Pauli Kroneckers; dev = 0 |
| VF.2/4 | v_F = (2/D_e)sin(π/q) = 1/5; cross-checked via 1D band route 2t·sin(5π/6) | PASS — exact |
| VF.4 | C = g·(L_F/4π²)·(2/v_F) = 50/(3π) | PASS — arithmetic exact |
| VF.5 | M* = 2M_Pl·e^{−X/C} → m_τ | PASS — 363.5 GeV → m_τ to 0.47% |
| Inversion | C required by PDG m_τ vs 50/(3π) | agree to **0.012%** |

### Central result: fragility quantification

The transmutation exponent amplifies upstream error by **|d ln M*/d ln C| = X/C = 38.7**:

- 0.1% error in C ⇒ 3.9% error in M*.
- The "lattice cross-check" C = 5.339 quoted in VF.4 (0.64% above analytic) ⇒ **M* +28%, τ mass missed entirely**. The chain works *only* with the continuum value.
- BCS prefactor 1 vs 2: factor **2.0** in M*. Full vs reduced Planck cutoff: factor **5.0**.

### Failures / open items

1. **[FAIL] Lattice cross-check irreproducible.** No code in the repository generates
   C = 5.339. `src/analysis/verify_C_band_structure.py` is **circular**: it re-evaluates
   the same analytic formula and compares it to itself. The "0.7% finite-size effect"
   sentence in VF.4 is unverifiable as stated.
2. **[OPEN] g = 4** (Kramers × particle–hole) and the per-channel 1D reduction are
   asserted, not derived.
3. **[OPEN] Discrete conventions** (prefactor 2, full M_Pl) are load-bearing and unfixed.
4. **[LIT] Abrikosov ratios** β_A = 1.1596 (triangular) < 1.1803 (square)
   (Kleiner–Roth–Autler 1964) accepted as literature, not recomputed; they carry the
   q = 6 selection.

## Verdict

**Arithmetic: SOUND. Status as derivation: NOT YET.** The 0.012% inversion agreement is
striking but, under the Anti-Hardcode Law, cannot count as evidence while three unfixed
choices (each worth ×2–×5, against a ×38.7 amplifier) remain free: the chain currently has
enough discrete freedom to hit m_τ. GAP-N4c stays **open at the justification level**, now
with quantified stakes.

**What would close it:**
1. A reproducible lattice/DOS computation (committed code) distinguishing 50/(3π) from
   nearby values at the 0.1% level — this is decisive either way, since 5.339 vs 5.305
   changes M* by 28%.
2. First-principles fixing of the BCS prefactor, the cutoff identification, and g = 4.
3. Scheme-dependence analysis of the one-loop matching (as VF.6 already requested).

Manuscript action (done same day): VF.6 replaced with the audit-results subsection;
Appendix AC register updated.

---

## Addendum (same day): the decisive lattice computation — executed

`experiments/verification/lattice_C_computation.py` → `results/logs/lattice_C_computation_20260814.log`
(v2 after an internal referee pass caught three bugs in v1: square-window contour
leakage (+43% in the validation!), wrong K point, non-monotone bisection).

**Method validation:** contour-integral machinery reproduces the known exact answer of the
isotropic model to 1e-6 (single Γ circle, no spurious branches).

**Results:**
1. **5.339 struck.** For the isotropic/1D-channel model that the appendix identities
   actually describe, the exact contour integral equals the linearized value identically —
   there is NO 0.6%-level lattice correction. None of the tested artifact classes
   (Lorentzian broadening, energy-bin histogram, coarse-grid histogram) cleanly reproduce
   +0.64% (closest +0.76%). The number has no code and no explanation; struck from VF.4.
   **The +28% threat to M* is retired.**
2. **Van Hove obstruction (new).** On the true C6 triangular band, 5/6 edge-locking lands
   ABOVE the van Hove energy in both natural directions (E_F = +0.493/+0.515 vs
   E_vH = +0.400) → Fermi surface is K-pockets, isotropic linearization off by −29%/+75%.
   C = 50/(3π) belongs to the idealized isotropic model only.
3. **Unit mixing (new).** C = g·(L_F/4π²)(2/v_F) mixes fraction-units (L_F) with
   radian-units (v_F). Consistent evaluations give 50/3 or 50/(3π²) → m_τ missed by >10
   orders. Only the mixed evaluation lands on m_τ — a fourth load-bearing unfixed choice.

**Updated GAP-N4c closure list:** honest 2D model compatible with Γ-circle locking;
principled unit convention; prefactor/cutoff/g=4. The anchor survives 5.339 but its
"derivation" status is further away, not closer, after honest scrutiny.

---

## Addendum 2 (same day, evening): quasi-1D frame — the constructive answer

`experiments/verification/quasi1d_C_model.py` + `theory/derivation_quasi1d_C_20260814.md`.
C = g·De/(q·π·vF) (unit-consistent) = 50/(3π) exactly; coincides with the legacy formula
iff De = q−1 (the Cl(6) identity). Closes the unit and 2D-model debts; derives locking
(commensuration, ν = 5/6 [HYP]) and 1/q dilution. New primary falsifier: core-strength
tension (|V0| ≲ 1e-6 bandwidth required; enhancement ≈ 4.6|V0|^0.75). Remaining:
ν-filling, core tension, prefactor/cutoff/g=4.
