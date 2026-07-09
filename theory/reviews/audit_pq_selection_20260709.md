# Mathematical Audit — Derivation Note "Topological Selection of (p,q) Mode Assignments"

Auditor: lab mathematician role · Date: 2026-07-09
Object: `theory/derivation_pq_selection_20260709.md`

## Item-by-item verdicts

| Step | Claim | Verdict | Notes |
|---|---|---|---|
| 3.1 | [T², S¹] ≅ H¹(T²;ℤ) ≅ ℤ² | **SOUND** | S¹ = K(ℤ,1); standard obstruction theory |
| 3.2 | SL(2,ℤ) orbits of ℤ² classified by gcd | **SOUND** | Primitive vector completes to a basis (Bézout); Smith normal form |
| 3.2 | E = M\*(1/p+1/q) not SL(2,ℤ)-invariant ⟹ rigid-torus axiom A2′ required | **SOUND** | Example verified: T·(1,1)ᵀ = (2,1)ᵀ, E drops 2M\* → 1.5M\*. (Typo (1,2) in draft corrected to (2,1) — conclusion unaffected.) This is a genuine, previously undeclared axiom of the framework |
| 3.3 | gcd = 1 ⟺ torus knot; gcd = d ⟺ d-component torus link | **SOUND** | Standard knot theory (Rolfsen §10) |
| 3.4 | Antiparticle cascade instability, Eq. (4) | **SOUND (conditional)** | Arithmetic verified independently: ΔE[(1,1)→(11,11)+(−10,−10)] = −1.618 M\*; limit ΔE → −M\*(1/p+1/q). Conditional on E(−k,−l) = E(k,l), which follows from CPT of the emergent low-energy theory the framework itself claims. The only escapes are (i) a soliton-number superselection rule (no origin in the axioms — GAP-2 correctly flagged) or (ii) abandoning the 1/p energy ansatz. ERROR-1 classification is justified |
| 3.5 A | Hurwitz: normed division algebras only in dim 1,2,4,8 | **SOUND** | Hurwitz 1898. But note: hypothesis H2 (composite modes require a composition algebra) is physical, not mathematical — correctly labelled hypothesis |
| 3.5 A | W± admits no allowed mode under d ∈ {2,4,8} | **SOUND — strengthened** | Independently verified by exhaustive search (p₀ ≤ 100, q₀ ≤ 2000, coprime): closest misses are Δ(1/p₀+1/q₀) = 6.8×10⁻³ (d=2), 4.7×10⁻² (d=4), 2.4×10⁻¹ (d=8) vs PDG tolerance 3.8×10⁻⁴, 7.6×10⁻⁴, 1.5×10⁻³. Exclusion margins: 18×, 62×, 158×. The bound p₀ ≤ 100 suffices since 1/p₀+1/q₀ ≥ target requires p₀ ≤ 1/target |
| 3.5 B | Bott periodicity: real Clifford period 8 ⟹ primitive tower ends at 2⁷ = 128 | **SOUND (conditional)** | Cl(n+8) ≅ Cl(n) ⊗ ℝ(16) is correct. The step "primitive tower = one Bott period" is hypothesis H3, correctly labelled. It removes the arbitrariness of 128 *given* H3, but H3 itself is underived |
| 3.6 | Z⁰ = (8,8) at 58.4σ | **SOUND** | (365.2407/4 − 91.1876)/0.0021 = 58.4. Fractional 0.13% |
| A6 | M\* = (3/2)m_τ/α = 365.2407 GeV | **SOUND** | Recomputed from `data/PDG_2024.json` (m_τ = 1776.86 ± 0.12 MeV): M\* = 365.24068, DT-1 = M\*/64 = 5.70689 GeV. **MINOR:** the committed JSON carries the pre-2024 world average; current PDG 2024 lists m_τ = 1776.93 ± 0.09 MeV → M\* = 365.255, DT-1 = 5.70711 GeV. Difference (0.2 MeV) is inside the quoted ±1 MeV band; update the JSON and re-quote |
| P1 | DT-1 = 5.707 ± 0.001 GeV (α(0) scheme) | **SOUND as a conditional prediction** | Cleanly pre-registered; scheme ambiguity honestly declared (GAP-4) |

## Findings requiring action

1. **ERROR-1 is blocking and is now the central open problem of the framework** — more fundamental than the sector question the note was asked to solve. Either exhibit a conserved soliton number from the condensate dynamics, or the mass law E ∝ (1/p + 1/q) is mathematically dead. No manuscript may cite the Universal Stability Theorem without this caveat.
2. **GAP-1 (torus marking)**: A2′ must be added to `theory/specs/SYSTEM_OF_EQUATIONS.md` or the formula is inconsistent with its own diffeomorphism class. Currently the spec is self-contradictory and the note correctly flags it.
3. **The W exclusion (3.5) and Z tension (3.6) must appear in any manuscript that keeps the mass law.** Suppressing them while quoting the 3.23σ sector-constrained significance (Appendix W Test 4) would be misrepresentation: that significance assumed p = 5, which this derivation shows is underivable and H2-excluded.
4. MINOR: update `data/PDG_2024.json` tau mass to the actual 2024 value with provenance note.

## Overall verdict: **SIGNED-OFF WITH CONDITIONS**

The derivation note is mathematically correct in every checked step and honest in its hypothesis labelling. Sign-off covers: (a) the classification results (3.1–3.3), (b) the ERROR-1 instability finding, (c) the conditional selection rules and their falsifying consequences (3.5–3.6), (d) prediction P1 *as a conditional, pre-registered statement*.

Sign-off does **not** cover any use of the mass law as an established result. Per RESEARCH_WORKFLOW stage 4, the next pipeline stage for P1 is implementation of the DT-1 confrontation (direct-detection exclusion curves vs 5.707 GeV), and the theorist owes resolutions of ERROR-1 and GAP-1 before the law re-enters any manuscript as more than a hypothesis.
