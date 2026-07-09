# Mathematical Audit — Derivation Note "Core/Tension Energy E_core"

Auditor: lab mathematician role · Date: 2026-07-09
Object: `theory/derivation_ecore_tension_20260709.md`

## Item-by-item verdicts

| Step | Claim | Verdict | Notes |
|---|---|---|---|
| 3.1 Eq. (1) | Linear map minimizes Dirichlet energy in class (p,q); E = 2π²K(p²R₂/R₁ + q²R₁/R₂) | **SOUND** | Harmonic maps T² → S¹: energy functional is convex on each affine class θ_lin + φ (φ: T²→ℝ single-valued); cross term ∫∇θ_lin·∇φ = 0 since θ_lin has constant gradient and ∫∇φ = 0 on the torus. Minimizer is exactly the linear map — no approximation. Formula recomputed independently: ✓ |
| 3.1 Eq. (2) | Growing torus (report's L_p = pL₀): E_core = 4π²K·pq | **SOUND** | ∂₁θ = 2π/L₀ (constant), Area = pq·L₀² → E = 4π²K·pq ✓. Note this is the reading MOST favorable to the framework (sub-quadratic in each winding); the conclusion below survives it |
| 3.2 Eq. (5) | Channel arithmetic | **SOUND** | Winding conservation ✓; ΔE recomputed at spot values matches the session numerics |
| 3.3 threshold | Stability ⟺ σ₀ ≥ M\*/27 ≈ 13.5 GeV | **SOUND** | Analytic: large-k expansion ΔE ≈ −2M\* + 4M\*/k + 2σ₀k², minimized at k³ = M\*/σ₀ giving ΔE_min = −2M\* + 6M\*^{2/3}σ₀^{1/3}; zero at σ₀ = M\*/27 = 13.53 GeV. Numerical scan confirms (σ₀ = 13.5 → +19.6 GeV; σ₀ = 10 → −64.4 GeV). Caveat: only the (1,1)→(1+k,1+k)+(−k,−k) family was optimized; asymmetric channels could only *raise* the required σ₀, strengthening the theorem |
| 3.2 fidelity | σ₀ bounds from W/Z/DT-1 | **SOUND** | Simple division; the DT-1 bound 3.5×10⁻⁶ GeV is the binding one. Note the tolerance choice for DT-1 (±1%) is generous to the framework; a tighter claim tightens the contradiction |
| 3.3 Eq. (6) | S ∩ F = ∅ by ~6.6 orders | **SOUND** | 13.5 / 3.5×10⁻⁶ = 3.9×10⁶ ✓ |
| 3.4 escapes | Four routes enumerated, all absent from the report | **SOUND as survey** | Route 1 note is correct: BPS bounds give E ≥ c·|topological charge| (increasing), never inverse; a BPS completion cannot rescue 1/p |
| Cor. (b) | Dark-energy-as-tension selects the unstable branch | **SOUND (conditional on the identification being quantitative)** | The report states the identification qualitatively; if the framework ever quantifies σ from Λ_obs it lands ≪ 10⁻⁶ GeV — deep in the unstable region. Flag: the report never assigns a number to its own tension; this audit treats that as the framework's omission, not the note's |

## Findings

1. The central result — **{mass law, vacuum stability, dark-energy-as-tension}: choose at most two** — is established at the level of rigor of the framework's own declared energy functional. It is robust to the choice of torus geometry (both readings checked) and to channel choice (worst case only strengthens it).
2. The note correctly withdraws prediction P1 (DT-1 at 5.707 GeV) as *unconditional*; P1 now lives or dies with GAP-1/GAP-2.
3. MINOR: Eq. (5) uses the symmetric channel family; add one line noting asymmetric channels can only raise the threshold (done in my caveat above — incorporate on next edit).
4. MINOR: quote K's naturalness argument (K ~ M\*) as an estimate, not a derivation — the note already labels it Corollary (a); acceptable.

## Overall verdict: **SIGNED-OFF**

The incompatibility theorem (Eq. 6) is mathematically sound and may be cited in manuscripts, subject to the standing conditions of the 2026-07-09 audits (the mass law itself remains hypothesis-grade; this note shows it is now *internally inconsistent* with the framework's stability and dark-energy claims absent GAP-1/GAP-2 closure).

Per RESEARCH_WORKFLOW, the theorist now owes the PI a decision memo: which two of the three pillars to keep.

## Addendum (same day) — re-audit after PI correction on dark energy

The PI correctly pointed out that dark energy in the framework is **not** the condensate tension but the relaxation/potential energy of the condensate at its NJL minimum (report §7.3: m_σ ≫ H₀ ⟹ w₀ = −1; Λ value via Kaloper–Padilla). Verified against the report text: §7.3 confirms; the abstract's "condensate tension" wording is the report's own loose phrasing.

Re-audit of the corrected note:
- **Corollary (b) retraction: CORRECT.** The dark-energy sector places no constraint on the phase stiffness K; the original corollary is withdrawn cleanly and the erratum is transparent.
- **Main theorem (Eq. 6): UNAFFECTED.** It never used the dark-energy sector; the scan over σ₀ was exhaustive. The dilemma sharpens from ternary to **binary**: pure inverse mass law XOR stable vacuum.
- **New corollary (b′): SOUND as a qualitative argument, GAP-4 correctly assigned.** That the acoustic metric requires finite phase stiffness is standard (Unruh/Volovik); the quantitative induced-G ↔ K relation remains open and is properly labelled.

**Verdict after addendum: SIGNED-OFF (unchanged).** The correction improves the note's fidelity to the framework without weakening the result.
