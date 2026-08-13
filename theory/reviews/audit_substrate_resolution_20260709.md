# Mathematical Audit — "Substrate Resolution: One Breaking Chain, Two Stages" + F2/F3 numerics

Auditor: lab mathematician role · Date: 2026-07-09
Objects: `theory/derivation_substrate_resolution_20260709.md`; `experiments/layer0/referee_response_tests.py` + log `results/logs/referee_response_tests_20260709.log`.

## Theory audit

| Claim | Verdict | Check |
|---|---|---|
| π₂(G) = 0 for every compact Lie group | **SOUND** | Cartan's theorem; standard |
| Exact sequence ⟹ π₂(G/H) ≅ π₁(H) when π₁(G) = π₂(G) = 0, H connected | **SOUND** | π₂(G)→π₂(G/H)→π₁(H)→π₁(G); all H in the chain (SU(3), U(2), U(1)) are connected ✓; G₂ and SU(2) simply connected ✓ |
| Chain table: π₂(S⁶) = 0; π₂(CP²) = ℤ; π₂(S²) = ℤ | **SOUND** | Line 1: π₁(SU(3)) = 0; line 2: SU(3)/S(U(2)×U(1)) = CP², π₁(U(2)) = ℤ; line 3: standard |
| Corollary (2) "matter iff a U(1) survives" | **SOUND with one scope note** | For the groups in this chain, exact. In general π₁(H) can be finite torsion (e.g. H = SO(3) ⟹ ℤ₂ lumps) — the "iff" should read "ℤ-valued charge iff a U(1) factor survives; torsion π₁ would give finite-valued charge." Wording adjusted expectation, not a defect of the chain result |
| F1 resolution logic (S⁶ = matterless condensation stage; S² = matter stage; same declared chain) | **SOUND** | Follows from the table + the report's own chain (§5.2, p. 181, App. AL). The referee's "different theories" objection is answered by an exact criterion, not by fiat |
| S-P3 (protected lump ⟺ surviving-U(1) winding; neutral+stable forbidden at coset level) | **SOUND as stated, correctly flagged as having bite** | Direct reading of (1). Note: "hidden U(1)" escape is honestly listed |

## Numerics audit (F2, F3)

- **F3 v3 protocol is now correct**: disk-interior link energy; boundary frozen to the BP tail (the two earlier failed protocols — north-pole pinning, whole-lattice energy — are documented in the log; their failure modes are understood analytically: seam wall ~8πρ²/R_d, frozen-seam inclusion). Results E/(4π|Q_in|) = 0.9952 / 0.9972 / 0.9986 for ρ = 6/8/12, each lying in [analytic disk fraction, 1] and → 1: **Q = 1 saturation CONFIRMED. Referee F3: RESOLVED.**
- **F2 scaling**: t_c(ρ) = 10, 30, 310, 2960, 15465 for ρ = 5, 6, 8, 10, 12 (L = 128, dt = 0.2, sampling every 5 steps — the ρ = 5 point is resolution-limited, flag retained). Growth is super-power-law (global log-log slope ≈ 8; quasi-exponential fit ln t_c ≈ 1.1ρ over the mid-range). Verdict: **protection on the discrete substrate is approximate but its violation is very strongly suppressed in (defect size)/(lattice spacing) — GAP-5 now has a measured law.** Referee F2: **QUANTIFIED** (first pass; a dt-refinement and L-dependence study would firm the exponent, listed as follow-up).

## Overall verdict: **SIGNED-OFF**

F1 is resolved at theorem level; F3 is resolved numerically; F2 is quantified with an explicit suppression law. Remaining from the referee report: F4 (literature confirmation of the odd-N GN spectrum — blocked by environment tooling) and F5 (Derrick scoping — already applied to wording).
