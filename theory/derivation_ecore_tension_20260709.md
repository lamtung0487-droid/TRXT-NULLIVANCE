# Derivation Note — Core/Tension Energy E_core of the (p,q) Worldvolume Defect

**Author:** lab theorist role · **Date:** 2026-07-09 · **Protocol:** `theory/protocols/workflow-v5-checklist.md`
**Question:** what is the classical gradient/tension energy of a (p,q) winding, using the framework's **own** tension sector (Layer 1: E ∝ Ξ|∇θ|², report §3.1.2 p.18; abstract: "dark energy as the condensate tension"), and can any value of the tension make the vacuum stable while preserving the mass law m = M\*(1/p + 1/q)?

**Result: NO — the two requirements are incompatible by ≥ 6.6 orders of magnitude. This closes the dilemma of `report_reading_three_problems_20260709.md` in the negative for the pure inverse-winding mass law.**

---

## Step 0 — Declarations

1. **Physical object:** classical field energy of the condensate phase θ(x) in a fixed winding class (p,q) ∈ [T², S¹]; the order parameter's stiffness (tension) sector declared by the framework itself.
2. **Observables:** total rest mass M(p,q) = E_core(p,q) + E_gap(p,q); vacuum stability against winding-pair emission; consistency of the W/Z/DT-1 mass table.
3. **Layer:** dynamical law (energy functional) + measurement (spectrum comparison).
4. **Failure conditions:** classical (mean-field) treatment; valid below condensation scale, distances ≫ healing length ξ. Quantum corrections to E_core are O(ℏ) relative and cannot cancel a classical term scale-by-scale without fine-tuning (noted in GAP-2).

## Step 1 — Framework

**(B) Classical field theory.** Phase field θ: T² → S¹ on the defect worldvolume, energy functional from the framework's Layer-1 declaration. Amplitude Ξ (Existence Intensity) frozen at bulk value outside cores; the report's Ξ-quenching (Ξ ∝ r², report Eq. 4) regularizes core singularities but does **not** remove bulk gradient energy — that is the point of this note.

## Step 2 — Axioms

- **A1.** θ ∈ S¹ on T² with marked cycles (axiom A2′ of `derivation_pq_selection_20260709.md`), radii R₁, R₂.
- **A2.** Energy density (framework's own Layer 1): ℰ = (K/2)·Ξ·|∇θ|², K > 0 the phase stiffness. [K] = energy (2D worldvolume integration). Ξ → 1 in bulk.
- **A3.** Dynamics: minimize E[θ] in fixed winding class (harmonic map problem).
- **A4.** Causality: inherited; not modified.
- **A5.** E ≥ 0; boundedness of the full spectrum is the question under investigation.
- **A6.** Measured inputs: M\* = 365.2407 GeV (as before); match tolerances from PDG errors and the framework's own claimed precisions (W: ±16 MeV ≈ its claimed 0.02% match; Z: ±2.1 MeV PDG; DT-1: ±1% of 5.707 GeV).

## Step 3 — Derivation body

### 3.1 Minimum gradient energy in class (p,q) — exact

The Dirichlet minimizer in class (p,q) on a flat torus is the linear map θ = p·x₁/R₁ + q·x₂/R₂ (harmonic; standard result). Its energy:

**(1)**  E_core = (K/2)·Area·|∇θ|² = (K/2)(4π²R₁R₂)(p²/R₁² + q²/R₂²) = 2π²K (p²R₂/R₁ + q²R₁/R₂).

*Dimension check:* [K] = GeV, rest dimensionless. ✓

Two geometric readings, both used by the report:
- **(i) Growing torus** (report §8.4: L_p = pL₀, i.e. R₁ = pL₀/2π, R₂ = qL₀/2π): |∇θ|² = 2(2π/L₀)², Area = pq·L₀², giving
  **(2)**  E_core = σ₀ · pq,  σ₀ ≡ 4π²K.
- **(ii) Fixed torus** (R₁ = R₂): **(3)** E_core = σ₀ · (p² + q²)/2.

**In both readings E_core grows with winding.** There is no geometry in which the framework's own Layer-1 energy density gives a decreasing or zero core energy: 1/p scaling of the *gap* coexists with +pq (or +p²+q²) scaling of the *core*. (Reading (i) used below — it is the report's own geometry and the more favorable one for the framework.)

### 3.2 Total mass and the two requirements

**(4)**  M(p,q) = σ₀·pq + M\*(1/p + 1/q).

**Requirement S (vacuum stability).** Pair-emission channel (1,1) → (1+k, 1+k) + (−k,−k) (worst case; cf. ERROR-1). Total energy change:

**(5)**  ΔE(k) = M\*[2/(1+k) + 2/k − 2] + σ₀[(1+k)² + k² − 1].

Numerical minimization over k (verified this session, `results/logs/` session record): ΔE > 0 for all k **iff σ₀ ≳ 13.5 GeV** (analytic estimate σ₀ > M\*/27 = 13.53 GeV, confirmed: σ₀ = 13.5 → min ΔE = +19.6 GeV; σ₀ = 10 → −64.4 GeV, unstable).

**Requirement F (spectrum fidelity).** The core term must not spoil the claimed matches:

| State | pq | Tolerance | Bound on σ₀ |
|---|---|---|---|
| W (5,50) | 250 | 16 MeV | σ₀ < 6.4×10⁻⁵ GeV |
| Z (8,8) | 64 | 2.1 MeV | σ₀ < 3.3×10⁻⁵ GeV |
| DT-1 (128,128) | 16384 | ~57 MeV | **σ₀ < 3.5×10⁻⁶ GeV** |

### 3.3 The incompatibility theorem (main result)

**(6)**  Requirement S: σ₀ ≥ 13.5 GeV.  Requirement F: σ₀ ≤ 3.5×10⁻⁶ GeV.
**S ∩ F = ∅, with a gap of 6.6 orders of magnitude.** (Fixed-torus reading (3): worse — DT-1 core ∝ (p²+q²)/2 = 16384 identically here, same bound, but Z bound tightens.)

Corollaries:
- **(a)** The framework's *natural* stiffness K ~ M\* gives σ₀ = 4π²M\* ≈ 14.4 TeV: vacuum stable, spectrum destroyed by 9 orders (W core term ≈ 3.6 TeV).
- **(b) [CORRECTED 2026-07-09, PI correction]** ~~Original corollary tied σ₀ to the observed Λ via "dark energy = condensate tension" (abstract wording).~~ **Retracted:** per report §7.3, dark energy is the *potential energy of the condensate field settled at the minimum of V_NJL* (m_σ ≫ H₀ ⟹ w₀ = −1), with the Λ *value* set by Kaloper–Padilla sequestering (§9.12 item 1) — it does **not** constrain the phase stiffness K. The abstract's "condensate tension" phrasing is loose terminology within the report itself. Consequently σ₀ is a free scale of the framework and the theorem sharpens from "choose 2 of 3" to a **binary dilemma** (see below).
- **(b′) NEW — emergent gravity pins K away from zero.** The stiffness K cannot be dialed small to satisfy Requirement F: the same Ξ|∇θ|² sector *is* the acoustic-metric substrate (report §3.1.2: the metric is "woven" from Ξ and ∇θ; induced gravity requires finite phase stiffness). A framework with σ₀ < 10⁻⁵ GeV has a condensate too floppy to carry the emergent geometry it claims. Quantifying the induced-G ↔ K relation is GAP-4 (assigned to the standing induced-gravity gap of the 2026-07-09 framework audit, Item 1).
- **(c)** ERROR-1 of `derivation_pq_selection_20260709.md` is therefore not an artifact of ignoring tension — including the framework's own tension sector *quantifies* it and shows no parameter value resolves it.

### 3.4 Enumerated escape routes (all currently GAPs, none in the report)

1. **BPS-type cancellation** — a second charge/pressure term canceling σ₀·pq exactly for all (p,q) while leaving the 1/p gap intact. No such structure exists in the declared action; would require a new symmetry (GAP-1). Note BPS energies are ∝ |charge|, i.e. *increasing* — a BPS version would still not give 1/p.
2. **Soliton-number superselection** (GAP-2 of the previous note) — forbids pair creation kinematically. Needs a conserved current from the condensate dynamics; none exhibited.
3. **Resonance reinterpretation** — (p,q) states as finite-width worldvolume resonances, not stable solitons. Kills the DT-1 dark-matter stability claim (Tier 3 requires absolute stability) — self-defeating.
4. **Winding-dependent stiffness** K → K(p,q) ∝ 1/(pq) — ad hoc, violates locality of the Layer-1 energy density (K is a property of the medium, not of the excitation), and is Anti-Hardcode-noncompliant tuning.

## Step 4 — Consistency gates

- [x] GR/Newton limit: untouched.
- [ ] Stability: **the subject of the note — FAILS for all σ₀ compatible with the spectrum** (Eq. 6).
- [x] Consistency with specs: contradiction flagged — SYSTEM_OF_EQUATIONS.md and report §8.4 omit E_core entirely; report §3.1.2 supplies the very energy density that generates it.
- [x] Anti-Hardcode: no constant introduced beyond declared M\*, tolerances (PDG), and the free parameter σ₀ which is *scanned exhaustively*, not fitted.

## GAP list

| # | Item |
|---|---|
| GAP-1 | Exhibit a cancellation mechanism (new symmetry) that removes E_core for all (p,q) — currently no candidate |
| GAP-2 | Or exhibit a soliton-number superselection rule from the condensate action |
| GAP-3 | Or re-derive the spectrum from M(p,q) = σ₀pq + M\*(1/p+1/q) with σ₀ ≥ 13.5 GeV and find *new* assignments matching data (a different theory; the current table dies) |

## Predictions table

| # | Statement | Test |
|---|---|---|
| P1′ | If the framework keeps "dark energy = condensate tension" (tiny σ₀), its vacuum is unstable to winding-pair cascade: **internal falsification, no experiment needed** | Theoretical — already decided by Eq. (6) |
| P2′ | If instead σ₀ ≥ 13.5 GeV, all light states acquire core masses ≥ σ₀·pq: no particle below ~13.5 GeV can be a (p,q) mode with pq ≥ 1 — DT-1 at 5.707 GeV is then impossible as (128,128) | The DT-1 prediction of `derivation_pq_selection_20260709.md` P1 is **withdrawn as unconditional**; it survives only if GAP-1/GAP-2 close |

## Verdict requested

Submitted to the **mathematician** for audit. Honest headline for the PI (post-correction): **the dilemma is binary — the pure mass law m = M\*(1/p+1/q) and a stable vacuum cannot coexist for any value of the condensate stiffness** (Eq. 6). Dark energy is not implicated (corollary b retracted; the relaxation mechanism of §7.3 is untouched by this note). Emergent gravity, if anything, pushes σ₀ large (corollary b′), i.e. toward the branch where the current mass table dies and assignments must be re-derived from M(p,q) = σ₀·pq + M\*(1/p + 1/q).
