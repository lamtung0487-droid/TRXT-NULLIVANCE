# Mathematical Audit — "Per-Stage Gaps, the Absolute Tower, and the Structural Exclusion of the SM from the Tower"

Auditor: lab mathematician role · Date: 2026-08-13
Object: `theory/derivation_stage_gaps_20260813.md` + session scan logs.

| Claim | Verdict | Check |
|---|---|---|
| Anchors A1/A2 correctly labelled as *inherited framework quantities with condition chains*, not lab theorems | **SOUND (and important)** | A1 (M\* = 365.24 GeV via v_F = 1/5 chain) has NOT been independently re-derived by the lab — GAP-N4c correctly opened. The note does not overclaim |
| Tower arithmetic (1): 3.95·16·365.24·√ln → 201 TeV (Λ = M_Pl), 184 TeV (Λ = M_cond) | **SOUND** | Recomputed: √(2ln(1.22e19/365.24)) = 8.72 ✓; 3.95×16×365.24×8.72 = 2.01×10⁵ GeV ✓; (pq)^{3/4} columns ✓ |
| Completeness rule (every integer pq' < a is an occupied level) | **SOUND** | pq' = 1·pq' realizes every integer; stability is unconditional (topological); hence a − 1 stable states below the candidate W — the rule is forced, not chosen |
| Scan results: 251σ (a≤4), 63σ (a≤10), 6.0σ (a≤30), 0.2σ only at a = 180 | **SOUND** | Spot-recomputed the a ≤ 4 branch by hand: best (4,5,6) gives (5/4)^{3/4} = 1.1822 vs 1.13461 ± 0.00019 → ~250σ ✓. Exhaustive bounds honored |
| Conclusion (2): SM bosons excluded from the tower | **SOUND** | The dichotomy (ratio failure XOR light-stable-forest) is exhaustive under the pre-registered rule; the look-elsewhere pocket is correctly displayed and rejected |
| Reframing: SM = dynamical sector; tower = new 200 TeV sector | **SOUND as interpretation** | Follows from (2) + the framework's own SM-limit (§9.7) and Seifert-exponential results; correctly flagged that the invisibility/production story (report p. 53) transfers naturally |
| Unitarity-regime remark (Griest–Kamionkowski class) | **PLAUSIBLE, flagged** | Qualitative; GAP-N4d assigns the quantitative relic work |
| H-match/CP² (A4) | **CORRECTLY DEFERRED** | No number quoted; b_{CP²} = 3 is the standard CP^{N−1} coefficient |

**One audit remark for the record:** the exclusion (2) is the programme's first *structure-level* negative result obtained under a rule stated before the scan — methodologically, this is the exact inverse of the original Appendix-W scanning procedure, and it is what closes the numerology chapter permanently: there is no assignment left to hunt for.

## Verdict: **SIGNED-OFF**

GAP-N4 (S²-branch) closed at anchor level with conditions declared; the structural half of the assignment campaign is **complete and decided**. Remaining programme: GAP-N4b (CP² cascade), GAP-N4c (independent audit of the M\* chain), GAP-N4d (200 TeV sector phenomenology gate), plus the standing bookkeeping items (GAP-S screening re-derivation, GAP-N2, GAP-N3b).
