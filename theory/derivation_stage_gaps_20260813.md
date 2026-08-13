# Derivation Note — Per-Stage Gaps, the Absolute Tower, and the Structural Exclusion of the SM from the Tower (GAP-N4)

**Author:** lab theorist role · **Date:** 2026-08-13 · **Protocol:** `.claude/skills/derive/SKILL.md`
**Target:** GAP-N4 — the per-stage constituent gap M, hence absolute masses; and the first, structure-only half of the assignment question.

> **Results:** (i) with the framework's own two anchors, the S²-stage topological tower is absolute: **M(pq) ≈ (184–201 TeV)·(pq)^{3/4}**; (ii) a completeness-constrained, pre-registered scan **excludes the SM bosons from the tower at ≥ 6σ (typically 10²–10³σ)** — the tower is a *new heavy sector*, not a re-derivation of W/Z/H; (iii) the SM masses remain with the framework's dynamical mechanisms (amplitude mode + Seifert-exponential), which is where its genuinely successful numerics always lived. The assignment question is thereby *answered structurally*, with no fitting ever performed.

---

## Step 0 — Declarations

1. **Object:** the constituent gap M of each matter stage (CP², S²) and the resulting absolute soliton spectrum.
2. **Observables:** absolute tower masses; number of stable states below m_W; SM mass ratios vs (pq)^{3/4}.
3. **Layer:** dynamical (anchors) + measurement (exclusion scan).
4. **Failure conditions:** anchors inherit their own condition chains (declared below); one-loop cascade for CP² left as hypothesis (GAP-N4b).

## Step 1–2 — Framework & anchors (all previously declared quantities; nothing new introduced)

- **A1 (S²-stage gap).** M_{S²} ≡ M\* = 365.24 GeV — the framework's own BCS/transmutation chain (report §8.4/App. J/VF: g_eff = C/X, C = 50/3π, X = 3/2α). *Condition chain inherited:* the v_F = 1/5 derivation and its audit history; this is an anchor, not a lab theorem.
- **A2 (S⁶-stage scale).** M_cond ≈ 2.3×10¹⁶ GeV — report p. 181 (G₂/SU(3) NLSM asymptotic freedom, 1-loop, factor-4 stated uncertainty).
- **A3 (tower prefactor).** C = 3.95·N_f·M_{S²}·√(ln Λ²/M²) with N_f = 16 (Cl(6) minimal left ideal — framework's own count), from `derivation_mass_constant_20260813.md` (SIGNED-OFF).
- **A4 (CP²-stage, hypothesis H-match, GAP-N4b).** Below M_cond the CP² = SU(3)/U(2) sigma sector runs with one-loop coefficient b_{CP²} = 3 (CP^{N−1}: b = N) from the matched coupling at M_cond; its gap lands between M_cond and M_{S²}: a **superheavy second tower** (near-GUT relic class). Left symbolic pending the matching condition — no number is quoted.

## Step 3 — Derivation body

### 3.1 The absolute S²-stage tower

**(1)**  M(pq) = 3.95·16·365.24 GeV·√(ln Λ²/M²)·(pq)^{3/4}:

| Λ choice | M(1,1) | M(2) | M(3) | M(4) | M(6) |
|---|---|---|---|---|---|
| M_Pl | **201 TeV** | 339 | 459 | 570 | 772 TeV |
| M_cond | **184 TeV** | 309 | 419 | 520 | 705 TeV |

Error budget: cutoff choice ±9%; ĉ ±4%; N3b few %; plus the A1 condition chain. **The tower is a heavy sector: its ground state sits at O(200 TeV), three orders above the electroweak scale.**

### 3.2 Pre-registered structural test: are W/Z/H tower states? (rule declared before scanning)

**Rule (stated first):** if W, Z, H are tower states with pq-values a ≤ b ≤ c, then (i) (b/a)^{3/4} and (c/a)^{3/4} must match m_Z/m_W = 1.13461 ± 0.00019 and m_H/m_W = 1.55781 ± 0.00139 *within experimental precision*, and (ii) **completeness**: the tower predicts a stable state at *every* integer pq' < a (pq' = 1·pq' always exists), i.e. a − 1 unobserved absolutely stable states below m_W — bounded by collider phenomenology to a − 1 ≲ 3.

**Scan results (exhaustive, b, c ≤ 400; session log):**

| Constraint | Best (a,b,c) | Max tension |
|---|---|---|
| a ≤ 4 (completeness-compatible) | (4,5,6) | **251σ** |
| a ≤ 10 | (5,6,9) | 63σ |
| a ≤ 30 (29 hidden stable states!) | (11,13,20) | 6.0σ |
| a unbounded (≤400) | (180,213,325) | 0.2σ — but demands **179 unobserved stable states below 80 GeV** |

**(2)** **Conclusion (structural, no fit performed): the SM bosons are not states of the (pq)^{3/4} tower.** Either the ratios fail at ≥ 6σ–10³σ, or completeness demands a forest of light stable exotics excluded by experiment. The 0.2σ pocket at large a is precisely the look-elsewhere artifact the lab's null-test discipline exists to catch — quoted here as the cautionary exhibit, not as a result.

### 3.3 What this settles

- **The assignment campaign's first half is decided without a single fit:** no SM assignment exists. The temptation that produced the old numerology is structurally closed.
- **SM masses stay with the framework's dynamical sector**, where its real numerical successes always were: Higgs = amplitude mode of the condensate (report §9.7 SM-limit); fermion hierarchy via the Seifert-exponential (m_τ/m_μ = 16.8 vs 16.81); gauge masses via the standard mechanism.
- **The topological sector is a prediction, not a postdiction:** a tower of absolutely stable, surviving-U(1)-charged states starting at ~200 TeV (S² stage), plus a superheavy CP² tower (GAP-N4b). Notably: (a) O(100 TeV) is the classic unitarity-bound regime for thermal relics (Griest–Kamionkowski class), and (b) the report's own production story ("born only during the Great Condensation", collider volume-penalty invisibility, p. 53) fits a heavy non-thermal relic sector naturally — the framework had the right invisibility physics attached to the wrong mass.

## Step 4 — Consistency gates

- [x] Anti-Hardcode: no constant introduced; anchors are the framework's own derived quantities with conditions declared; the scan rule was pre-registered in-note before execution.
- [x] Consistency: supersedes the DT-1 = 5.707 GeV story (already withdrawn); consistent with S-P2/S-P3 falsifiers and the two-species structure.
- [x] Honest-null discipline: the seductive 0.2σ large-a match is reported *and rejected by the pre-registered completeness rule*.

## GAP list

| # | Item |
|---|---|
| GAP-N4b | CP²-stage gap: one-loop cascade matching at M_cond (b_{CP²} = 3) — turns the superheavy tower into numbers |
| GAP-N4c | A1 condition chain: independent lab audit of the v_F = 1/5 → M\* derivation (so far inherited, not re-proven) |
| GAP-N4d | Phenomenology gate for the 200 TeV sector: relic abundance (phase-transition production), direct/indirect signatures, charged-relic constraints under S-P3 |

## Predictions table (pre-registered)

| # | Observable | Prediction | Test |
|---|---|---|---|
| T-P1 | Lightest topological state | M(1,1) = 184–201 TeV (±~15% combined band) — absolutely stable, carries surviving-U(1) winding | Far-future colliders; cosmic-ray/heavy-relic searches; cosmological abundance consistency (GAP-N4d) |
| T-P2 | Tower ratios | M(pq')/M(pq) = (pq'/pq)^{3/4} exactly — e.g. second state at 1.682× the first | Any two discovered states of the sector |
| T-P3 | Absence prediction | NO absolutely stable topological state below M(1,1); in particular the sub-TeV range is clean | Collider stable-particle searches (currently consistent) |
| T-P4 | SM non-membership | No SM particle obeys tower ratios (≥6σ under completeness) — falsifiable by anyone re-running the scan | `results/` scan, reproducible |

Submitted to the **mathematician** for audit. **With this note, GAP-N4's S²-branch is anchored, and the assignment question — the campaign the whole programme was driving toward — is answered at the structural level: the tower is new physics at 200 TeV, and the Standard Model keeps its dynamical origin.**
