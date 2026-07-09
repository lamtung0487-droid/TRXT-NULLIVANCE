# Referee Report — The Layer-0 Mass Principle M = 4πK·|Q|

Reviewer: lab referee role (hostile-but-fair, PRD standard) · Date: 2026-07-09
Object: `theory/derivation_layer0_mass_principle_20260709.md` (+ audit, + `experiments/layer0/bp_mass_quantization.py`, logs `bp_quantization_20260709.log`, `bp_quantization_robustness_20260709.log`).

## Restated claim

At Layer 0 (the framework's discrete O(3) substrate), soliton mass equals 4πK times the topological charge — exactly, by Bogomolny self-duality; the heat flow sheds energy only in 4πK quanta (so the Incompleteness Functional is the mass functional); the mass *scale* arises by dimensional transmutation (m = (8/e)Λ at O(3) level); and the fermionic O(7) realization of the G₂/SU(3) sector has two bound states with m₂/m₁ = φ, parameter-free.

## The six audits

1. **Hardcode audit — PASS.** The constants 4π (target-sphere area), 8/e (Hasenfratz–Niedermayer), φ = 2cos(π/5) (bootstrap) are theorem values, not fits. Simulation parameters (L, ρ, dt, seed, smoothing depth) are lattice knobs, all varied under audit 5. K is declared an undetermined unit (GAP-2) — acceptable.
2. **Circularity audit — PASS.** All theorem constants predate this framework by decades; the numerical tests were forward predictions (the E/(4πI) ratio starts at 1.54 and was predicted to descend toward 1 — it was not engineered to start at 1).
3. **Degrees-of-freedom audit — one serious discrete choice found (F1).** No continuous parameter was fitted anywhere. But the *choice of target manifold* for each sub-claim is a real degree of freedom the note exercises silently: the numerical verification uses the S² substrate (report App. AL), while the φ prediction uses the S⁶ = G₂/SU(3) sector (report p. 181). See F1.
4. **Reproduction — PASS (exact).** Fresh-shell rerun reproduces every number in the note to all printed digits (deterministic seed).
5. **Robustness — MIXED; two findings (F2, F3).** New seed (777), L = 160, t → 4000: the dynamical ratio again descends monotonically to **1.092** (vs 1.091 original) — the central quantization trend is robust. Larger-lump saturation improves to **E/(4π·2) = 1.0006** for Q = 2. However see F2 (charge wandering) and F3 (Q = 1 artifact).
6. **Exclusion/literature check — PARTIALLY BLOCKED (F4).** BP bound, bubbling/energy-identity theorems, HN gap: standard, textbook-verifiable. The odd-N O(7) Gross–Neveu bound-state range could not be literature-verified in this session (WebSearch/WebFetch disabled by an environment fault); it rests on the reviewer's recollection of the standard sine spectrum (DHN 1975; Zamolodchikov² 1978; Karowski–Thun 1981). CoNb₂O₆/E₈ golden-ratio measurement (Coldea et al. 2010) is established.

## Findings

**F1 — MAJOR (substrate ambiguity).** The framework now has **two different Layer-0 target manifolds in play**: S² (App. AL — the simulated substrate, source of the 4πK quantization evidence) and S⁶ ≅ G₂/SU(3) (p. 181 — source of the O(7)/φ prediction). The note quietly benefits from both. Until the framework declares *which* manifold (or which fibration relates them) is Layer 0, the φ prediction and the numerical verification belong to *different theories*. Required: a single declared substrate, or an explicit reduction map S⁶ → S² with its effect on (1)–(6).

**F2 — MAJOR (lattice charge non-conservation).** Robustness run: Q_net wanders **−13 → −1 → +2 → +3** across the flow. The Berg–Lüscher charge is integer at every snapshot but is NOT conserved by the discrete kernel: lumps shrink below the lattice scale and "fall through." Consequence: **on the framework's own discrete substrate, topological protection is approximate, not exact.** Since the report elsewhere rests proton stability and matter permanence on exact topological conservation (App. R.3), the violation rate must be quantified (expected ~e^{−cK} tunneling-like suppression; compute it) — or the continuum limit must be declared fundamental, at the ontological cost of demoting the "discrete logic field" to an approximation. The note's phrasing "Q_net stays exactly integer through every annihilation" is technically true but rhetorically misleading; it must be corrected to acknowledge wandering.

**F3 — MINOR (Test A design flaw at Q = 1).** The Q = 1 saturation ratio *worsens* with lattice size (1.286 at L = 192 → 1.727 at L = 256): the non-periodic BP profile forced onto a torus creates a seam whose energy grows with L. The Q = 2 result (1.0006) shows the physics is right when the seam cancels. Required: rerun Q = 1, 3 on a disk with fixed boundary or with charge-compatible periodic embeddings; do not quote the current Q = 1 number.

**F4 — QUERY (literature verification blocked).** Before any manuscript use, the O(7) GN bound-state count and mass formula (k = 1, 2; odd-N kink-sector subtleties) must be verified against Zamolodchikov² and Karowski–Thun. Environment fault (broken WebSearch model) prevented this today. Status: PLAUSIBLE, not CONFIRMED.

**F5 — MINOR (Derrick marginality in 2+1D).** As static 2+1D particles, pure-O(3) BP lumps are scale-marginal and known to collapse under generic perturbation (Piette–Zakrzewski). Physical stabilization (Skyrme term, potential, or the lattice/temperature of the substrate itself) necessarily deforms E = 4πK|Q| to E = 4πK|Q| + corrections. The principle survives as the *leading term*; the word "exact" must be scoped to the 2D/self-dual statement.

**F6 — MINOR.** Bubbling theorems are continuum statements; the discrete kernel only approximates them (already flagged in the note's failure conditions — adequate).

## Reproduction result

**PASS** — all published numbers reproduced exactly; robustness reproduces the central trend (1.091 vs 1.092 at matched epochs; Q=2 saturation improves with resolution, as a true bound should).

## Verdict: **MAJOR REVISION**

The Bogomolny linearity, the 4π quantization trend, and the transmutation scale are solid and survived hostile testing — this is the most defensible mass-origin result the programme has produced. But the claim may not enter any manuscript until: (i) F1 substrate ambiguity is resolved by a declared single target (or explicit reduction map); (ii) F2 charge-violation rate on the discrete substrate is quantified and the note's conservation rhetoric corrected; (iii) F3's Q=1 test is redone properly; (iv) F4's literature check is completed when tooling permits.

**Editor's sentence:** a genuinely beautiful and largely verified organizing principle, currently attached to an ambiguously specified substrate — fix the foundation it stands on before engraving the equation.

Per RESEARCH_WORKFLOW: MAJOR findings reopen `/derive` (F1, F2), not merely the wording.
