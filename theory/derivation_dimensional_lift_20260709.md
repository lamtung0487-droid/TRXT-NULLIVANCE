# Derivation Note — The Dimensional Lift L0 → L1: from M = 4πK|Q| to M = C·(pq)^{3/4}

**Author:** lab theorist role · **Date:** 2026-07-09 · **Protocol:** `.claude/skills/derive/SKILL.md`
**Target:** GAP-B (RESEARCH_LOG problem #1) — which energy–charge law does the lift from the 2D substrate to 3+1D particles transport?

> **Result:** the lift is forced, not chosen. Derrick's theorem forbids the linear 2D law from surviving unchanged in 3D; the framework's own quartic EFT term supplies the mandatory stabilizer; the fibration charge algebra is **Q_Hopf = p·q** (numerically verified today); and the exact Vakulenko–Kapitanskii bound then fixes the L1 working mass law:
> **M(p,q) = C·(pq)^{3/4}** — with the old (p,q) surviving as fibration data and the old 1/p+1/q surviving only as breathing-mode fine structure.

---

## Step 0 — Declarations

1. **Object:** the energy–charge law of 3+1D topological solitons (Hopfions, π₃(S²) = ℤ) built by lifting 2D substrate lumps (π₂(S²) = ℤ) along closed fibers.
2. **Observables:** parameter-free mass *ratios* M(p',q')/M(p,q) = (p'q'/pq)^{3/4}; existence condition for stable matter (c₄ > 0); knotted/linked minimizer geometry at higher pq.
3. **Layer:** dynamical law (L1), built on the kinematics fixed by `derivation_substrate_resolution_20260709.md`.
4. **Failure conditions:** classical, static solitons; the constant C and quantum corrections not computed here (GAPs); charge numerics at 1–8% discretization accuracy.

## Step 1 — Framework

**(B) Classical field theory.** Static energy of the S²-stage field n̂: ℝ³ → S² with vacuum boundary condition (one-point compactification ⟹ maps classified by π₃(S²) = ℤ, the Hopf invariant).

## Step 2 — Axioms

- **A1.** Substrate sequence and S²-stage field as established (substrate-resolution note, SIGNED-OFF).
- **A2.** Quadratic (Dirichlet) energy E₂ = (K/2)∫|∇n̂|² d³x, inherited from Layer 1 stiffness.
- **A3 (H-c₄ hypothesis, flagged).** The S²-sector EFT contains a positive quartic-derivative (Skyrme-type) term E₄ = (κ₄/4)∫|∂ᵢn̂ × ∂ⱼn̂|² d³x. *Motivation:* the framework's own bosonized EFT already generates a quartic derivative term in the phase sector (P(X) = c₂X + c₄X², c₄ > 0 derived from NJL loops — report App. B/C); the same one-loop determinant generically produces the quartic invariant in every Goldstone sector. Until the S²-sector coefficient is computed from the NJL determinant, A3 is a hypothesis, not a theorem (GAP-L2).
- **A4.** Charges: p = 2D lump charge of the fiber cross-section; q = twist number of the fiber loop.

## Step 3 — Derivation body

### 3.1 Derrick's obstruction: the linear law CANNOT survive the lift (exact)

Under the rescaling n̂_λ(x) = n̂(x/λ):

**(1)**  E₂ → λ·E₂ (3D Dirichlet),  E₄ → λ⁻¹·E₄.

With E₄ = 0, dE/dλ = E₂ > 0: every configuration lowers its energy by shrinking without bound — **no stable 3D soliton exists in the pure-Dirichlet theory.** Whatever mass law L1 has, it is *not* obtained by naively integrating the 2D linear law over a third dimension. *Dim check:* [E₂] = [K]·L (3D) — K here is the 3D stiffness with [K] = energy/length ✓.

### 3.2 The framework's own stabilizer (and a cross-link that earns its keep)

With A3, **(2)**  E(λ) = λE₂ + E₄/λ ⟹ λ\* = √(E₄/E₂), E_min = 2√(E₂E₄) — a stable size exists iff **c₄-type quartic > 0**.

**Corollary (new internal cross-link):** the *same* quartic that produces Vainshtein/k-mouflage screening (report §9.3) is what permits matter to exist at all. Screening and matter stability are one term seen twice. This upgrades c₄ > 0 from a phenomenological virtue to an *existence condition for matter* — and yields falsifier L1-P2 below.

### 3.3 The charge algebra of the lift: Q_H = p·q (numerically verified)

Construction: rational-map ansatz ψ = (Z₁ᵖ, Z₂^q) on the compactified ℝ³ → S³, projected to n̂ (regular everywhere). Whitehead integral Q_H = (1/8π²)∫A·B d³x with ∇×A = B, B_k = ε_kij n̂·(∂ᵢn̂×∂ⱼn̂) components, computed by FFT (Coulomb gauge). Results (`experiments/layer0/hopf_lift_charge_algebra.py`, log `results/logs/hopf_lift_20260709.log`; 96³ grid, calibrated on the exact case Q_H(1,1) = 1):

| (p,q) | (2,1) | (1,2) | (2,2) | (3,1) | (3,2) |
|---|---|---|---|---|---|
| Q_H measured | 1.988 | 1.946 | 3.841 | 2.908 | 5.542 |
| Q_H = pq | 2 | 2 | 4 | 3 | 6 |

**(3)**  Q_H(p,q) = p·q, confirmed to 1–8% (error grows with pq — under-resolved gradients; refinement listed as follow-up). **The old framework's (p,q) labels survive the lift as fibration data: p = cross-sectional lump charge, q = fiber twist; the conserved invariant is their product.** This also explains *why* the old T² worldvolume story kept finding (p,q) pairs: they are real, but their invariant combination is pq, not 1/p + 1/q.

### 3.4 The energy law: Vakulenko–Kapitanskii fixes the exponent

For the functional E₂ + E₄ (Faddeev–Niemi class), the exact topological bound is

**(4)**  E ≥ c·|Q_H|^{3/4} = c·(pq)^{3/4},

(Vakulenko–Kapitanskii 1979; the ¾ arises because the Hopf charge is a *linking* — its energy cost can be partially delocalized along the fiber, unlike the pointwise-protected 2D charge). Numerical minimization in the Faddeev–Niemi literature (Battye–Sutcliffe et al.) finds minimizers tracking the bound, E ≈ c·Q^{3/4} within a few %, with unknotted rings at low Q and **knots/links at higher Q**. *(Literature values quoted from memory — F4-class caveat; confirm citations when web tooling returns.)*

### 3.5 The lift theorem (summary) and the fate of both old laws

**(5)**  M_L1(p,q) = C·(pq)^{3/4},  C = C(K, κ₄) per stage (two stages ⟹ two constants C_CP², C_S²).

- The **2D linear law is not lost**: it is the rigid/thin-fiber limit (fixed cross-section, no Derrick relaxation) — exactly the regime the old K.2 computation inhabited. The physical 3D minimizer relaxes it to the ¾ law.
- The **1/p+1/q law survives demoted**: it is the breathing gap of these same objects (fine structure on top of (5)), as established in `derivation_layer0_mass_principle_20260709.md` §3.5.
- Vacuum stability: (pq)^{3/4} is subadditive-safe — pair creation of (±k) costs 2C·k^{3/4}·(…) > 0; no cascade (consistency with the E_core theorem's F1 branch).

## Step 4 — Consistency gates

- [x] Stability: guaranteed by construction (3.2) given A3; no Ostrogradsky (first-order energies; the quartic is first-derivative-quartic, standard Skyrme-safe).
- [x] Anti-Hardcode: exponents (1, −1, ¾) are theorem values; C left symbolic (GAP-L1); no fits.
- [x] Consistency with specs: supersedes the 1/p+1/q principal law (flagged everywhere since the E_core theorem); consistent with substrate-resolution note and with the framework's own c₄ > 0 (App. C).
- [ ] GR limit: untouched.

## GAP list

| # | Item |
|---|---|
| GAP-L1 | Compute C from (K, κ₄), i.e. from the NJL determinant — sets the absolute mass scale of each stage |
| GAP-L2 | Derive the S²-sector quartic coefficient κ₄ from the same NJL loop that gives c₄ (turns A3 from hypothesis into theorem) |
| GAP-L3 | Refine charge numerics (higher grid, richer (p,q)); quantify the discretization systematic |
| GAP-L4 | Quantum/breathing corrections on top of (5); connect to the demoted 1/p+1/q fine structure quantitatively |

## Predictions table (pre-registered, parameter-free ratios)

| # | Observable | Prediction | Test |
|---|---|---|---|
| L1-P1 | Mass ratios within one stage | M(p',q')/M(p,q) = (p'q'/pq)^{3/4}; e.g. M(2,1)/M(1,1) = 2^{3/4} = 1.682, M(2,2)/M(1,1) = 4^{3/4} = 2.828 | Any future assignment table must obey these ratios — falsifiable before any fit |
| L1-P2 | Matter-existence ⇔ screening | In any environment where the quartic term is tuned away (c₄ → 0), stable solitons must disappear | Internal consistency check; links two sectors of the theory |
| L1-P3 | Minimizer geometry | Higher-pq states are knotted/linked field configurations, not larger rings | Structural (numerical FN minimization) |
| L1-P4 | Lightest state | Q_H = 1 = (1,1): the unique lightest topological state per stage; two stages ⟹ exactly two "ground species" | Confronts assignment tables |

Submitted to the **mathematician** for audit. Note to PI: with this note, the chain **L0 principle → substrate sequence → dimensional lift** is complete at working-law level. What remains before touching particle assignments: GAP-L1/L2 (the constant C), and the standing F4 literature checks.
