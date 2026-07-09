# Mathematical Audit — Appendix AC.2 "Sector Assignments from G₂ Branching Rules"

Auditor: lab mathematician role · Date: 2026-07-09
Object: report pp. 156–157 (App. AC.2), claiming p_EW = 5 and p_Z = 8 are *derived* from representation theory. This was flagged as I-8 in the Atlas and GAP-3 in `derivation_pq_selection_20260709.md`.

## What is correct

1. **G₂ → SU(3): 14 → 8 ⊕ 3 ⊕ 3̄.** SOUND (standard branching; dims 8+3+3 = 14 ✓).
2. **SU(3) → SU(2)×U(1): 8 → 3₀ ⊕ 2₊ ⊕ 2₋ ⊕ 1₀.** SOUND (adjoint decomposition; 3+2+2+1 = 8 ✓).
3. The report's own statistical honesty: even granting the derivation, significance is 2.2σ (p = 0.013). Correctly computed and correctly labelled "not conclusive".

## Findings

**F1 — ERROR (selection is arbitrary).** "The electroweak sector (components carrying SU(2) charge)" is defined as 3₀ ⊕ 2₊₁, dim 5. But the components carrying SU(2) charge are 3₀ ⊕ 2₊₁ ⊕ 2₋₁, **dim 7**. Dropping exactly one doublet has no stated justification; including the *neutral* triplet 3₀ in an "electroweak-charged" block while excluding a charged doublet is internally inconsistent. The choice appears reverse-engineered to reach 5.

**F2 — ERROR (no selective power).** Exhaustive check (this session): sums of ≤3 branching-block dimensions from {1, 2, 2, 3, 3, 8, 14} reach **every integer 1–15**. A rule that can produce any small integer post hoc derives none of them. For the derivation to count, the block-combination rule must be fixed *before* looking at which integer is needed.

**F3 — ERROR (category mismatch, I-8 confirmed).** p is a winding number, an element of π₁(T²) ≅ ℤ² (report Eq. 140). AC.2 equates it to the *dimension of a Lie-algebra subrepresentation*. No map between these mathematical objects is defined anywhere in the 191 pages. "W wraps around the 5D EW irreducible block" (p. 157) is not a map; windings wrap *cycles*, not vector-space dimensions.

**F4 — MAJOR (physical mismatch).** p_Z = 8 = dim(adj SU(3)) — but this SU(3) is Stab_G₂(e₁), identified throughout the report as **color**. The Z⁰ is color-neutral; assigning its winding to "all 8 gluon directions" contradicts the framework's own identification of that block.

**F5 — QUERY (framework collision).** AC.2's p = 5 (a rep dimension) coexists with Tier-2's d = gcd(5,50) = 5 (a link-component count) and with the Hurwitz selection d ∈ {1,2,4,8} of `derivation_pq_selection_20260709.md`, which *excludes* 5. Three incompatible selection principles are now live in the programme; at most one can be kept.

**F6 — MINOR.** The cross-link p_EW = 1/v_F = D_e = 5 stacks a third object (count of independent Clifford generators) onto the same integer. Coincidence of small integers across unrelated structures is precisely the pattern the null tests warned about.

## Verdict: **NOT SIGNED-OFF — the claim "Status: C2 RESOLVED" (p. 157) must be downgraded to OPEN.**

Minimal conditions for a future sign-off: (i) define the map from representation blocks to winding classes; (ii) state the block-selection rule *before* computing its dimension, and show it excludes the alternatives (7, 4, 8, …); (iii) resolve the Z⁰/color mismatch; (iv) reconcile with (or retire) the Tier-2 gcd and Hurwitz frameworks. Until then, sector assignments remain **structural hypotheses**, exactly as the report's own p. 53 states — the later "RESOLVED" stamp overrode its own earlier honesty.
