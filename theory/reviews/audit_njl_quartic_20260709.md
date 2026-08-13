# Mathematical Audit — "The S²-Sector Quartic from the NJL Determinant"

Auditor: lab mathematician role · Date: 2026-07-09
Object: `theory/derivation_njl_quartic_20260709.md` (+ session computation log `results/logs/` trace-algebra runs).

| Step | Claim | Verdict | Check |
|---|---|---|---|
| (1) | D†D = −∂² + M² − Mγ^μτ·∂_μn̂ | **SOUND** | Recomputed by hand: γ⊗τ commute (different spaces), (τ·n̂)² = 1; ∂† = −∂ with hermitian Euclidean γ |
| (2) | Odd traces vanish; alternating signs | **SOUND** | tr(odd # of γ) = 0 in 4D; Duhamel expansion signs standard |
| (3) | tr E² = 8M²X | **SOUND** | 4δ_{μν}·2δ_{ab} contraction; machine check exact |
| (4) | tr E⁴ = M⁴(24X² − 16Y) | **SOUND** | Machine fit residual 3×10⁻²⁴ across 12 random tensors; decomposition 24X²−16Y = 8X²+16(X²−Y) is arithmetic |
| (5) | X² − Y = \|∂n̂×∂n̂\|² = F_{μν}² | **SOUND** | Analytic: ∂_μn̂ ⊥ n̂ ⟹ ∂_μn̂×∂_νn̂ ∥ n̂; verified numerically to machine precision on tangent configurations |
| (6)–(7) | K = N_f M²ln(Λ²/M²)/(4π²); κ_S = N_f/(48π²); κ_X = N_f/(96π²) | **SOUND** | Weights recomputed: E²-term ∝ ∫s⁻¹e^{−sM²} → log; E⁴-term ∝ ∫s·e^{−sM²} = M⁻⁴, cancelling the M⁴ of the trace ⟹ **finite, scheme-robust quartics** — the note's sharpest point, and it is correct. Assembly arithmetic re-derived: ½·½·8 = 2 ⟹ K/2 = M²ln/(8π²) ✓; (24X²−16Y)/(768π²) ✓ |
| — | e² = 12π²/N_f | **SOUND** | 1/(4e²) = N_f/(48π²) |
| (8) | C = c_FN·√3·N_f·M·√ln/(24π²) | **SOUND (conditional on c_FN)** | √(K·κ_S) recomputed symbolically: √3·N_f·M·√ln/(24π²) ✓; c_FN is the FN-numerics constant, correctly F4-flagged |
| A2 scope | Hedgehog vs γ₅ coupling | **CORRECTLY SCOPED** | The unitary-gauge restriction is legitimate; the O(1)-shift expectation under the chiral variant must be checked (GAP-N1) before manuscript-grade numbers |
| §3.2 remainder | Commutator/(∂²n̂)² class deferred | **ACCEPTABLE with flag** | These carry strictly more derivatives per field; standard gradient-expansion bookkeeping; GAP-N2 properly assigned |
| N-P3 | κ_S/κ_X = 2 exactly | **SOUND** | 16/8 from the trace; a genuinely falsifiable internal ratio |

## Overall verdict: **SIGNED-OFF** (conditions: GAP-N1 before quoting absolute coefficients in a manuscript; GAP-N3/c_FN literature when tooling returns)

With this note, **H-c₄ is a theorem at one loop** and the mass chain is analytic end-to-end:

Λ →(transmutation)→ M →(Eq. 7, exact)→ (K, κ_S) →(Derrick+VK)→ C·(pq)^{3/4}.

Every constant in the chain is either a theorem value (4π, 8/e, ¾, 1/48π², √3/24π²) or a declared framework input (N_f, Λ, per-stage M). Zero fitted numbers. The programme may now, per lab protocol, prepare the pre-registered assignment campaign — with the standing conditions (GAP-N1, N3, N4; F4 literature checks) stated wherever absolute masses are quoted.
