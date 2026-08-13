# Derivation Note — Quantitative Closure: the Mass Constant C (GAP-N3) and the Protection-Law Exponent (F2 final)

**Author:** lab theorist role · **Date:** 2026-08-13 · **Protocol:** `.claude/skills/derive/SKILL.md`
**Targets:** GAP-N3 (the Faddeev–Niemi minimizer prefactor in the lab's declared units) and the referee's final F2 residual (dt/L dependence of the charge-violation exponent).

> **Results:** with the literature normalization pinned from the source paper, the L1 mass law becomes fully numerical up to the per-stage gap M:
> **M(p,q) = (4√6/3)·ĉ · N_f·M·√(ln Λ²/M²) · (pq)^{3/4} ≈ 3.95 · N_f·M·√(ln Λ²/M²) · (pq)^{3/4}**, ĉ = 1.21 ± 0.05.
> The charge-protection time is **τ_c invariant under dt and L** at measured precision: the law is a continuum-time property. Both referee residuals on the Layer-0 principle are now closed; the only remaining unknown in the chain is the per-stage M (GAP-N4).

---

## Step 0 — Declarations

1. **Object:** (i) the numerical prefactor connecting the FN minimizer spectrum to the lab's (K, κ_S) units; (ii) the discretization-dependence of the Layer-0 charge-violation law.
2. **Observables:** absolute soliton masses (up to M); the protection-time exponent.
3. **Layer:** measurement/normalization (i); numerical verification (ii).
4. **Failure conditions:** ĉ taken from Q ≤ 16 minimizers (slow drift within [1.16, 1.26] — treated as systematic); τ_c scan at ρ ≤ 10, sampling resolution 10 steps.

## Step 1–2 — Framework & inputs

Unit conversion between two declared energy functionals (algebra); inputs: Sutcliffe's normalization and spectrum ([arXiv:0705.1468](https://arxiv.org/abs/0705.1468), PDF obtained and text-extracted this session); our one-loop coefficients (K, κ_S) from `derivation_njl_quartic_20260709.md`.

## Step 3 — Derivation body

### 3.1 The source normalization (extracted verbatim)

Sutcliffe (2007), Eq. (2.1): **E_S = (1/32π²√2) ∫ [ ∂ᵢφ·∂ᵢφ + ½ (∂ᵢφ×∂ⱼφ)·(∂ᵢφ×∂ⱼφ) ] d³x**, in which Ward's conjectured bound reads E ≥ Q^{3/4} and the computed minimizers satisfy **E/Q^{3/4} ∈ [1.16, 1.26] for Q = 1–16** ("consistently around 20% above the conjectured bound"); E₁ = 1.22, E₂ = 2.00. We adopt **ĉ = 1.21 ± 0.05** (central value with the table's spread as systematic). Rigorous floor: VK constant c = (3/16)^{3/8} ([arXiv:1311.2403](https://arxiv.org/pdf/1311.2403)).

### 3.2 Unit conversion (exact algebra)

Our static energy: E = ∫[(K/2)X + κ_S W], X = Σᵢ|∂ᵢn̂|², W = Σ_{ij}|∂ᵢn̂×∂ⱼn̂|². Rescaling x = b·x̃ (X-term ∝ b, W-term ∝ 1/b) and matching to the Sutcliffe form μ·A·[X̃ + W̃/2], A ≡ 1/(32π²√2):

**(1)**  b = 2√(κ_S/K),  μ = √(K·κ_S)/A = 32π²√2·√(K·κ_S)  ⟹  **E(Q) = 32π²√2·√(Kκ_S)·Ê(Q)**.

*Dim check:* [√(Kκ_S)] = mass (K ~ mass², κ_S dimensionless) ✓.

### 3.3 The constant, assembled

With √(Kκ_S) = √3·N_f·M·√(ln Λ²/M²)/(24π²) (one-loop theorem, audited):

**(2)**  **C = 32π²√2·√(Kκ_S)·ĉ = (4√6/3)·ĉ·N_f·M·√(ln Λ²/M²) ≈ 3.95·N_f·M·√(ln Λ²/M²)**  (ĉ = 1.21).

**Sanity check (nontrivial):** the lightest soliton mass ≈ 4·N_f·M·√ln — the direct analogue of the Skyrme-physics result "baryon mass ~ N_c × constituent mass". The chain reproduces a known physical pattern it was never fitted to.

### 3.4 F2 final: the protection law is discretization-independent

Physical violation time τ_c = steps×dt for a seam-free Q = 2 pair, scanned over dt ∈ {0.1, 0.2} and L ∈ {96, 128} (log `results/logs/f2_refinement_20260813.log`):

| ρ (sites) | 5 | 6 | 8 | 10 |
|---|---|---|---|---|
| τ_c (all four dt×L combos, identical) | 2.0 | 6.0 | 62.0 | 592.0 |

**(3)**  τ_c is invariant under dt-halving and L-growth at sampling resolution; fits: ln τ_c ≈ **1.14·ρ** (quasi-exponential), local power α ≈ 8.2. The protection law is a property of the continuum-time flow with spatial discreteness — exactly the regime the framework's "discrete logic substrate" declares. **Referee residual F2: CLOSED.**

## Step 4 — Consistency gates

- [x] Anti-Hardcode: ĉ is a *measured literature constant with citation and stated systematic*, not a fit to our data; conversion (1) is exact algebra.
- [x] Consistency: completes the chain of `derivation_dimensional_lift_20260709.md` (GAP-L1) with no change to any prior result.

## GAP list

| # | Item |
|---|---|
| GAP-N4 | Per-stage constituent gap M (CP², S² gap equations) — **the single remaining unknown of the mass chain** |
| GAP-N3b | ĉ drift with Q (use per-Q table values once the full Table 2 is transcribed; affects masses at the few-% level) |

## Predictions table

| # | Observable | Prediction | Test |
|---|---|---|---|
| Q-P1 | Lightest S²-stage soliton | M(1,1) = 3.95·N_f·M_{S²}·√ln — fixed once GAP-N4 closes | The assignment campaign |
| Q-P2 | Protection-law universality | τ_c(ρ) unchanged under further dt/L refinement | Higher-resolution rerun |

Submitted to the **mathematician** for audit.
