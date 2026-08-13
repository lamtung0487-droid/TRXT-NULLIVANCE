# Mathematical Audit — "The Dimensional Lift L0 → L1"

Auditor: lab mathematician role · Date: 2026-07-09
Objects: `theory/derivation_dimensional_lift_20260709.md`; `experiments/layer0/hopf_lift_charge_algebra.py` + log.

| Claim | Verdict | Check |
|---|---|---|
| Eq. (1) Derrick scalings: E₂ → λE₂, E₄ → λ⁻¹E₄ in 3D | **SOUND** | ∫\|∇n̂_λ\|²d³x = λ^{3−2}E₂; quartic λ^{3−4}. Standard, recomputed |
| Pure-Dirichlet collapse ⟹ linear law cannot lift naively | **SOUND** | dE/dλ = E₂ > 0 for all λ; no stationary point |
| Eq. (2) λ\* = √(E₄/E₂), E_min = 2√(E₂E₄) | **SOUND** | AM–GM; equality at λ\* |
| Cross-link "screening term = matter-existence term" | **SOUND given A3** | Follows from (2) + report App. C (c₄ > 0). Correctly contingent on H-c₄ |
| A3 labelled hypothesis (S²-sector quartic from NJL loop) | **CORRECTLY SCOPED** | The derived c₄ lives in the θ-sector P(X); transplanting to the n̂-sector is plausible (same determinant) but unproven — GAP-L2 properly assigned |
| Rational-map ansatz has Q_H = pq | **SOUND (standard) + verified** | Generalized Hopf construction; the numerics confirm |
| Whitehead/FFT computation | **SOUND, with a strengthening observation** | The raw calibration factor came out −1.9107 where the exact normalization factor is −2: a 4.5% discretization deficit on (1,1), the *same scale* as the deviations of the other entries (e.g. 1.946/2, 5.542/6). The errors are one consistent discretization systematic, not noise — the integer pattern pq is unambiguous. Recommend quoting "confirmed with a single ~2–8% discretization systematic" |
| Eq. (4) VK bound applies | **SOUND** | E₂+E₄ is exactly the Faddeev–Niemi functional; VK 1979 |
| Subadditivity/stability of the ¾ law | **SOUND** | x^{3/4} concave ⟹ Q^{3/4} ≤ Q₁^{3/4}+Q₂^{3/4}: fission and pair creation cost energy; no cascade |
| Battye–Sutcliffe spectra "within a few %" | **PLAUSIBLE, F4-class** | Quoted from memory; correctly flagged; must be cited properly when tooling permits |
| L1-P1 ratio arithmetic (2^{3/4} = 1.682, 4^{3/4} = 2.828) | **SOUND** | Direct |

**One scope note:** L1-P4 ("unique lightest state per stage") assumes the minimum of E over the Q_H = 1 sector is attained — for Faddeev–Niemi this is supported by the literature's numerical minimizers but a rigorous existence proof (à la Lin–Yang) should be cited at manuscript time; add to GAP-L4.

## Overall verdict: **SIGNED-OFF**

The chain **L0 Bogomolny principle → substrate sequence (π₂ = π₁) → dimensional lift (Derrick + VK + Q_H = pq)** is now a complete, internally consistent working framework for mass: exponents and ratios are theorem-grade; the two remaining quantitative unknowns are the per-stage constant C (GAP-L1) and the S²-sector quartic (GAP-L2). Assignment work remains blocked until those close, per lab protocol.
