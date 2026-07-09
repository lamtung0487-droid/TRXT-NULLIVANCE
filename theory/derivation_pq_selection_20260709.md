# Derivation Note — Topological Selection of (p,q) Mode Assignments

**Author:** lab theorist role · **Date:** 2026-07-09 · **Protocol:** `.claude/skills/derive/SKILL.md`
**Status after derivation: PARTIAL — see GAP/ERROR list. This note derives selection rules; the derived rules partially falsify the current Standard-Model assignments and yield one clean pre-registered prediction.**

---

## Step 0 — Declarations

1. **Physical object:** topological winding sectors of the condensate order parameter Φ: Σ → S¹ (vacuum manifold 𝓜 = S¹, per main text §Topological Charges), on a spatial 2-torus worldvolume Σ = T².
2. **Observables:** particle rest masses via E(p,q) = M\*(1/p + 1/q); specifically (a) consistency of W/Z/Higgs assignments, (b) the mass of the lightest dark-sector state (direct-detection experiments: LZ, XENONnT, DarkSide-LowMass; collider mono-X searches).
3. **Layer:** kinematical structure (charge classification) + measurement (predictions table). The dynamical law producing E(p,q) itself is **inherited as an ansatz** — flagged GAP-0, not re-derived here (see mathematician audit 2026-07-09, Item 2).
4. **Failure conditions:** applies only below the condensation scale Λ (winding description meaningless above healing length⁻¹); assumes the T² worldvolume is rigid (see Axiom A2′); silent on electrically charged sectors' gauge coupling.

## Step 1 — Framework

**(B) Classical field theory** of the order parameter Φ = A e^{iθ} on fixed background, solitonic sectors quantized topologically. No higher derivatives introduced (no new Ostrogradsky risk). Quantum mechanics enters only through charge quantization (homotopy classes), not through operator dynamics.

## Step 2 — Minimal axioms

- **A1.** Fundamental variable: θ(x) ∈ S¹ on Σ = T² = S¹₁ × S¹₂; amplitude A frozen at vacuum value (deep-condensate limit).
- **A2.** Symmetry: global U(1) shifts of θ; spatial diffeomorphisms of Σ.
- **A2′ (Rigid-torus axiom, NEW — required, see Eq. 3).** The condensate torus carries a *marked* pair of cycles (a fixed geometric basis, R₁ = R₂). This explicitly breaks the mapping class group SL(2,ℤ) down to the ℤ₂ exchange p ↔ q. Without A2′ the mass formula is inconsistent (Eq. 3).
- **A3.** Dynamics: energy functional whose sectoral minimum is E(p,q) = M\*(1/p + 1/q) [ansatz, GAP-0].
- **A4.** Causality: inherited from the condensate EFT; not modified by this note.
- **A5.** Energy positivity: E(p,q) > 0 for all nonzero windings; but see **ERROR-1** for boundedness of the *charge-extended* spectrum.
- **A6.** Measurement coupling: M\* = (3/2)·m_τ/α, with m_τ = 1776.86 ± 0.12 MeV (PDG 2024) and α = α(0) = 1/137.035999 — **declared measured inputs** (Thomson-limit scheme declared; see GAP-4). Numerically M\* = 365.24 GeV.

## Step 3 — Derivation body

### 3.1 Charge classification (SOUND)

Homotopy classes of maps T² → S¹ are classified by the first cohomology (S¹ = K(ℤ,1)):

**(1)**  [T², S¹] ≅ H¹(T²; ℤ) ≅ ℤ ⊕ ℤ ∋ (p, q).

*Dimension check:* charges are dimensionless integers. ✓
(p,q) are genuine topological invariants; this part of the framework is rigorous.

### 3.2 The SL(2,ℤ) obstruction and the rigid-torus axiom (NEW RESULT)

Large diffeomorphisms of T² form the mapping class group SL(2,ℤ), acting on (p,q) as a lattice vector. SL(2,ℤ) orbits of ℤ² are classified by **gcd(p,q) alone** (any primitive vector extends to a lattice basis; Smith normal form). Therefore:

**(3)**  If the torus is unmarked, any diffeomorphism-invariant energy must satisfy E(p,q) = f(gcd(p,q)). But M\*(1/p + 1/q) is **not** SL(2,ℤ)-invariant: (1,1) ↦ (2,1) under T = [[1,1],[0,1]] yet E(1,1) = 2M\* ≠ 1.5M\* = E(2,1).

**Consequence:** the mass formula secretly requires a preferred cycle basis — Axiom A2′ — i.e. the condensate must spontaneously fix a torus marking. This was nowhere declared in the framework before. A physical mechanism selecting the marking is **GAP-1**.

### 3.3 Tier classification from knot theory (SOUND as taxonomy)

For gcd(p,q) = 1 the winding embeds as a torus **knot** T(p,q); for gcd(p,q) = d > 1 it is a d-component torus **link** (standard result). This puts Appendix W's tiers on rigorous footing:

- **Tier 1 (matter):** primitive vectors, gcd = 1 — irreducible torus knots.
- **Tier 2 (gauge composite):** d-component links, d > 1 — d coherent copies of the primitive core (p₀, q₀).
- **Tier 3 (dark tower):** the sub-family d = 2ⁿ (see 3.5).

*This is classification, not selection — it does not by itself pick integers.*

### 3.4 Stability re-examined: the antiparticle cascade (**ERROR-1, decisive**)

Appendix W's Universal Stability Theorem (convexity of 1/x) is correct **only in the positive-winding sector** (all fragments p_i, q_i ≥ 1). A relativistic theory must admit charge conjugates (negative windings), with E(−k,−l) = M\*(1/k + 1/l) by parity of the ansatz. Consider the winding-conserving channel

**(4)**  (p,q) → (p+k, q+l) + (−k, −l),  ΔE = M\*[ (1/(p+k) − 1/p) + (1/(q+l) − 1/q) + 1/k + 1/l ].

As k, l → ∞, ΔE → −M\*(1/p + 1/q) < 0. Numerically (verified, `results/logs/` session log): (1,1) → (11,11) + (−10,−10) releases 1.62 M\*; (1,1) → (101,101) + (−100,−100) releases 1.96 M\*.

**Every mode is unstable to pair-emission of large-winding states, cascading toward infinite winding at vanishing cost.** The inverse-winding energy ansatz makes high-charge states arbitrarily cheap — thermodynamically pathological: the vacuum would boil into large-|winding| pairs.

**Consequences:** (a) the Universal Stability Theorem is an artifact of forbidding antiparticles; (b) either a **soliton-number superselection rule** must be added as a new axiom with a physical origin (none currently exists in the framework — **GAP-2**), or the energy ansatz E ∝ 1/p is untenable as a topological energy. Note a conventional winding energy E ∝ √(p² + q²) is convex, SL(2,ℤ)-compatible on gcd classes, and cascade-stable — but it is a *different theory*.

### 3.5 Sector selection — the strongest honest attempts

**Route A (Hurwitz / division algebras) → derives d ∈ {1, 2, 4, 8}.**
Hypothesis **H2**: a d-fold coherent gauge-composite mode requires a normed composition algebra acting on its d components (closure of the multi-component phase algebra). By Hurwitz's theorem, normed division algebras over ℝ exist only in dimensions **1, 2, 4, 8** (ℝ, ℂ, ℍ, 𝕆). Then allowed gauge multiplicities are d ∈ {1,2,4,8}.
- **Z⁰ = (8,8) = 8·(1,1): ALLOWED** (octonionic breathing mode). The only assignment in the current table that survives.
- **W± = (5,50) = 5·(1,10): EXCLUDED** — d = 5 is not a division-algebra dimension. No rationale in the framework's declared structures produces 5 (checked: parallelizable spheres S¹,S³,S⁷ give {1,3,7}; Hopf fibrations give {1,2,4,8}; Bott gives {2ⁿ}; "first stable prime" is undefined — 2 and 3 are smaller primes). **The p = 5 electroweak sector is not derivable — GAP-3 — and under H2 it is positively excluded.**

**Route A consequence for the W (no scanning used — pure consistency):** the W target E/M\* = 0.22004 requires 1/p₀ + 1/q₀ = 0.4401 (d=2), 0.8802 (d=4), or 1.7604 (d=8). None admits an integer solution (exhaustive by bounding: for d=4,8 one needs p₀=1 and 1/q₀ non-positive or non-integer; for d=2 the nearest coprime pairs miss by ≫ experimental error). **Under the derived selection rule, the W boson has NO allowed mode.**

**Route B (Bott periodicity / Clifford tower) → derives the dark tower and its endpoint.**
Hypothesis **H3**: dark-sector multiplicities follow the real Clifford algebra doubling Cl(n) → Cl(n+1), giving d = 2ⁿ. Real Clifford algebras are periodic with period 8 (Bott: Cl(n+8) ≅ Cl(n) ⊗ ℝ(16)), so the *primitive* tower is n ∈ {0,…,7}, terminating at

**(5)**  d_max = 2⁷ = 128 ⟹ lightest primitive dark state DT-1 = (128,128), m = 2M\*/128 = **M\*/64**.

This replaces Appendix W's unexplained choice of 128 with a topological endpoint. *Conditional on H3* (why dark multiplicities track Clifford doubling remains a hypothesis) *and on resolution of ERROR-1.*

### 3.6 Confrontation of the one derivable SM assignment

Z⁰ = (8,8): E = M\*/4 = 91.3102 GeV vs 91.1876 ± 0.0021 GeV (PDG) → Δ = 122.6 MeV = **58.4σ** (0.13% fractional). The single assignment that survives selection is excluded at high significance unless O(0.1%) corrections are derived (none currently are — the appendix's "higher-order corrections" are unspecified, **GAP-5**).

## Step 4 — Consistency gates

- [x] **GR/Newton limit:** untouched by this note (classification only).
- [ ] **No ghosts / stability:** **FAILS** — ERROR-1 (antiparticle cascade). Blocking.
- [x] **Consistency with SYSTEM_OF_EQUATIONS.md:** contradiction FLAGGED, not hidden: the mass formula requires the rigid-torus axiom A2′ absent from all specs.
- [x] **Anti-Hardcode:** integers here trace to Hurwitz (1,2,4,8) and Bott (2ⁿ, n ≤ 7) only. p = 5 is *rejected* precisely because it traces to nothing. M\* traces to declared measured inputs (A6).

## GAP / ERROR list

| # | Item | Severity |
|---|---|---|
| GAP-0 | E(p,q) = M\*(1/p+1/q) still underived from any Hamiltonian (inherited) | blocking for the law itself |
| GAP-1 | Physical mechanism marking the torus (breaking SL(2,ℤ)) undeclared | major |
| ERROR-1 | Antiparticle cascade destabilizes every mode; stability theorem artifact | **blocking** |
| GAP-2 | Soliton-number superselection rule needed to evade ERROR-1: no origin | major |
| GAP-3 | p = 5 (EW sector) not derivable; excluded under H2 | major (falsifies W assignment) |
| GAP-4 | α-scheme ambiguity in M\* (α(0) vs α(m_τ)): ±2.6% scale systematic | minor (declared) |
| GAP-5 | Z⁰ at 58.4σ; required 0.13% correction not derived | major |

## Predictions table (pre-registered, conditional on H2/H3 + ERROR-1 resolution)

| # | Observable | Prediction | Test |
|---|---|---|---|
| P1 | Lightest dark-sector state DT-1 = (128,128) | m = M\*/64 = **5.707 ± 0.001 GeV** (α(0) scheme; scheme band 5.4–5.7) | Low-mass direct detection (DarkSide-LowMass, XENONnT S2-only, LZ); mono-X at LHC |
| P2 | No stable dark state lighter than DT-1 | mass gap below 5.7 GeV in the dark sector | Any confirmed dark particle < 5.4 GeV falsifies H3 |
| P3 | Gauge-composite multiplicities | all gauge-boson modes have d ∈ {1,2,4,8} | **Already in tension: W± admits no allowed mode (3.5); Z⁰ at 58.4σ (3.6)** |
| P4 | Fermion/matter modes are torus knots | gcd(p,q) = 1 for all fundamental matter assignments | Internal consistency check on any future assignment table |

**Registered now, before any dark-sector measurement: P1 is the framework's make-or-break number.**

## Verdict requested

Submitted to the **mathematician** for audit per RESEARCH_WORKFLOW stage 2. Implementation and manuscript integration remain **BLOCKED** until sign-off. Note to PI: the honest headline is that first-principles selection *falsifies the W and strains the Z assignment* while producing exactly one clean falsifiable prediction (P1). Under MASTER-PROTOCOL Article I, if ERROR-1 and GAP-5 cannot be closed, the inverse-winding mass law dies and P1 dies with it.
