# Derivation Note — Stability of the Screening Branch and the DBI Completion (G0b)

**Author:** lab theorist role · **Date:** 2026-07-09 · **Protocol:** `.claude/skills/derive/SKILL.md`
**Target:** the G0b gate failure (X < 0 ghost/superluminal window of P(X) = c₂X + c₄X²) — the last blocker of the gate ladder.

> **Results:** (i) a small theorem shows the *naive* G0 criterion ("c_s ≤ 1 in all environments") is unsatisfiable by ANY nontrivial P(X) — the criterion itself must be refined, with justification logged; (ii) the **DBI completion P = Λ⁴(1 − √(1 − 2X/Λ⁴))** matches the derived EFT coefficients (c₂ = 1, c₄ = 1/(2Λ⁴) > 0) and is ghost-free and gradient-stable on the **entire** branch, with the X < 0 superluminality of the causally benign DBI class; (iii) a new bookkeeping inconsistency (I-12) is registered: the report's k-mouflage screening needs re-derivation because P_X *decreases* on the screening branch for c₄ > 0.

---

## Step 0 — Declarations

1. **Object:** the scalar-sector kinetic function P(X), X = −(∂φ)²/2 (report convention: static gradients ⟹ X < 0; cosmological rolling ⟹ X > 0).
2. **Observables:** ghost/gradient stability on both branches; sound-cone structure; gate G0b status.
3. **Layer:** dynamical law (EFT completion choice) + kinematics of the perturbation cone.
4. **Failure conditions:** |X| < Λ⁴/2 (DBI branch edge); classical cone analysis (quantum causality via BMV argument, F4-class citation).

## Step 1 — Framework

**(B) Classical field theory** — perturbations around backgrounds of P(X); standard k-essence cone analysis.

## Step 2 — Axioms

- **A1.** Perturbation kernel: ghost-free ⟺ P_X > 0; gradient-stable ⟺ K ≡ P_X + 2XP_XX > 0; c_s² = P_X/K.
- **A2.** Small-X EFT matching is mandatory: P(X) = c₂X + c₄X² + O(X³) with c₂ = 1 (normalization), c₄ > 0 (derived, App. C + `derivation_njl_quartic_20260709.md`).
- **A3 (refined causality criterion; replaces the naive reading — justification in 3.1).** Admissible: ghost-free + gradient-stable on the whole physical branch + a consistent causal cone structure (no closed causal curves; Babichev–Mukhanov–Vikman class — F4-flag for the citation). Naive c_s ≤ 1 is **not** required off the trivial background.

## Step 3 — Derivation body

### 3.1 Theorem (impossibility of the naive criterion)

**(1)**  c_s² − 1 = −2X·P_XX / K.

For K > 0, sign(c_s² − 1) = −sign(X·P_XX): **any P with P_XX(0) ≠ 0 is superluminal on one side of X = 0.** Since c₄ = P_XX(0)/2 > 0 is *derived* (and Derrick-required for matter to exist), demanding c_s ≤ 1 on both branches would demand P_XX ≡ 0 — a free theory with no screening and no solitons. **The naive G0 criterion is unsatisfiable in principle; it was testing for the impossible.** The physically meaningful criterion is A3 (this is the standard resolution in the k-essence literature; the report itself already implicitly used it by citing the Creminelli–Vernizzi safe class).

### 3.2 The DBI completion (adopted proposal)

**(2)**  P(X) = Λ⁴(1 − √(1 − 2X/Λ⁴)),  small-X: P = X + X²/(2Λ⁴) + … ⟹ **c₂ = 1, c₄ = 1/(2Λ⁴) > 0** ✓ matches the derived EFT; Λ identified with the screening scale Λ_eff of the report (App. C).

Exact branch-wide properties (verified symbolically and numerically this session):

**(3)**  P_X = (1 − 2X̃)^{−1/2} > 0,  K = (1 − 2X̃)^{−3/2} > 0,  c_s² = 1 − 2X̃  (X̃ ≡ X/Λ⁴ < ½).

- **Screening branch (X < 0): ghost-free and gradient-stable for ALL X** — the pathology window of the polynomial truncation is an artifact of truncation, cured non-perturbatively.
- c_s² > 1 there, but of the **DBI class**: the cone is the induced-metric cone of the brane picture; no closed causal curves arise (BMV) — precisely the benign case A3 admits. Cosmological branch (X > 0): subluminal ✓.
- The polynomial P = c₂X + c₄X² remains the correct *small-X expansion*; its X < 0 ghost at X̃ < −1/(2·2c₄Λ⁴-scale) simply lies outside the truncation's validity.

### 3.3 New inconsistency registered (I-12 / GAP-S)

For X < 0 (static sources) and c₄ > 0, P_X *decreases* with |X| — for both the polynomial and DBI forms. k-mouflage screening requires P_X ≫ 1 near sources. Either (a) the report's screening derivation (App. C/D, r_V, ε ∝ (r/r_V)^{3/2}) relies on a sign/convention inconsistent with X = −(∂φ)²/2, or (b) the actual mechanism is not P_X-enhancement k-mouflage. The v17-G4 script does not use P(X) at all (MOND-type interpolation), so the gate ladder is not immediately affected — but **the screening story requires a dedicated re-derivation with declared conventions** (GAP-S). Registered in the Atlas registry as I-12.

## Step 4 — Consistency gates

- [x] Ghost/gradient stability: PASS branch-wide under (2) — this is the point.
- [x] EFT matching (Anti-Hardcode): c₂, c₄ reproduced with Λ the already-declared screening scale; no new constants.
- [x] Consistency with specs: refines App. X's incomplete proof; registers I-12 instead of hiding it.
- [x] Criterion-change discipline: the G0b criterion update is justified by theorem (1) and logged in the gate ledger before any rerun.

## GAP list

| # | Item |
|---|---|
| GAP-S (=I-12) | Re-derive the screening mechanism with explicit sign conventions; determine whether k-mouflage or a different mechanism (e.g. the two-phase halo profile) actually does the work |
| GAP-D1 | BMV causal-consistency citation + the global-structure argument for the DBI screening cone (F4-class) |
| GAP-D2 | Derive (2) from the condensate (is DBI the natural resummation of the NJL loop? — speculative, flagged) |

## Predictions table

| # | Statement | Test |
|---|---|---|
| D-P1 | Refined G0b: DBI completion passes ghost+gradient branch-wide; polynomial truncation fails beyond its validity — both facts checkable by the gate script | `scripts/run_gates.py G0b` after criterion update |
| D-P2 | Deep-screening sound speed c_s² = 1 + 2\|X̃\| — a concrete, falsifiable cone structure for perturbations near massive bodies | Future: perturbation phenomenology |

Submitted to the **mathematician** for audit; gate update follows the logged-criterion procedure.
