# Mathematical Audit — "Quantitative Closure: the Mass Constant C and the Protection-Law Exponent"

Auditor: lab mathematician role · Date: 2026-08-13
Object: `theory/derivation_mass_constant_20260813.md` + logs.

| Claim | Verdict | Check |
|---|---|---|
| Source normalization Eq. 2.1 (1/32π²√2 prefactor, Skyrme term with ½) | **SOUND (verified at source)** | Extracted from the paper's own PDF text this session — not from memory; the F4-class caveat that plagued earlier quotes is fully discharged |
| ĉ = 1.21 ± 0.05 from E/Q^{3/4} ∈ [1.16, 1.26], Q = 1–16 | **SOUND** | Paper states "consistently around 20% above the conjectured bound"; E₁ = 1.22, E₂ = 2.00 cross-check (2.00/2^{3/4} = 1.189 ∈ range ✓). Spread correctly treated as systematic; GAP-N3b (per-Q values) properly opened |
| Conversion algebra (1): b = 2√(κ_S/K), μ = 32π²√2·√(Kκ_S) | **SOUND** | Re-derived independently: matching bK/2 = μA, κ_S/b = μA/2 ⟹ b² = 4κ_S/K, μA = √(Kκ_S) ✓; W-vs-½W bookkeeping between the two functionals is consistent (both sum over ordered ij) |
| (2): C = (4√6/3)·ĉ·N_f·M·√ln ≈ 3.95·N_f·M·√ln | **SOUND** | 32√2·√3/24 = 4√6/3 ≈ 3.266 ✓; ×1.21 = 3.95 ✓; dimension = mass ✓ |
| Sanity check "soliton mass ~ N_f × constituent mass" | **SOUND as remark** | Genuine structural parallel to Skyrmion/large-N_c baryon masses; correctly presented as a check, not evidence |
| (3): τ_c invariant under dt ∈ {0.1, 0.2}, L ∈ {96, 128}; ln τ_c ≈ 1.14ρ | **SOUND** | Log verified: four identical columns. Note: identity to the last digit reflects the 10-step sampling grid; the conclusion "no dt/L dependence at sampling resolution" is the correctly hedged statement, and Q-P2 pre-registers the refinement |

## Verdict: **SIGNED-OFF**

GAP-N3 closed (with GAP-N3b as a few-percent bookkeeping refinement); referee residual F2 closed. The L1 mass law now reads, fully explicitly,

**M(p,q) = 3.95 · N_f · M_stage · √(ln Λ²/M²_stage) · (pq)^{3/4} × [1 ± 0.04 (ĉ) ± few % (N3b)]**,

with **GAP-N4 (per-stage M) the single remaining unknown** between the programme and its pre-registered assignment campaign.
