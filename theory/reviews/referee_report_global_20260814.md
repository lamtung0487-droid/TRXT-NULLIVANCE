# Global Referee Report — TRXT Research Report V14 (184 pp, state at commit 2ca4c79)

**Date:** 2026-08-14 · **Role:** adversarial referee (inline) · **Scope:** entire manuscript
+ full verification trail (all `results/logs/*_2026081[34].log`, gate ledger, derivation notes)

## 1. Method

Full-protocol attack: hardcode audit, circularity audit, degrees-of-freedom count,
reproduction status, robustness probes, literature-exclusion check, stale-claim sweep
across all summary surfaces (abstract, gate lists, conclusions).

## 2. Hardcode audit — PASS with named residuals

Post-campaign state: no undeclared tuned parameter found anywhere in the active claims.
Every remaining discretionary input is *named in the manuscript itself*: two [ARG]-level
selections in the M* chain (sharp cutoff scheme; Λ = 1/ℓ_P), the [HYP-micro] status of
the participation law, ν = (q−1)/q closure formality (2D BdG), and the GAP-N4d-asym
target. The galaxy sector now runs with zero global parameters (T3, ledger). This is the
cleanest hardcode state the framework has ever been in.

## 3. Circularity audit — PASS with one required caution

- M* chain: inputs are α, M_Pl, structure; m_τ is an *output* (0.5%). The 0.012%
  inversion agreement is correctly quoted with its 2σ–3σ look-elsewhere weight. OK.
- Participation law: a0 from H0; SPARC not used to set anything in T3. OK.
- **Caution (mandatory wording):** the report's self-consistent H0 = 68.7 fits SPARC
  better than Planck H0 in T3 (4.83 vs 4.92). This must never be quoted as *independent*
  support: the H0-audit and the a0-identification share the sound-horizon anchor. Keep
  T2 labeled secondary.

## 4. Degrees-of-freedom count

| Sector | Fitted global params | Status |
|---|---|---|
| Galaxy rotation (T3 variant) | 0 | passes established criterion |
| Solar system | 0 | parameter-free δ = u²/2 |
| CMB/G2 | 0 (published Planck values) | χ²ν ≈ 1.0–1.2 |
| Tower masses | 0 (2 [ARG] selections) | ratios anchor-free |
| Tower abundance | 0 computed; 1 open target (Y_Δ) | symmetric excluded |
| Lepton masses | open (Seifert demoted) | honest |

## 5. Reproduction status — PASS

Every quantitative claim standing in the manuscript now has committed generating code +
log. Claims that failed reproduction were struck or downgraded *in the text itself*
(VF lattice 5.339; Seifert <1%; H0 70.6; SIDM table; Vainshtein (r/r_V)^{3/2};
unitarity-thermal relic phrasing). Verified by sweep of all audit boxes vs logs.

## 6. Robustness probes — main risks, ranked

1. **The M* anchor's evidential weight is 2σ–3σ** (look-elsewhere), and the G3
   zero-parameter pass sits at 4.92 vs threshold 5.0 — both healthy but *thin margins*.
   A modest adverse dataset (e.g. an extended SPARC release) could break either.
2. **GAP-N4d-asym is now load-bearing for the DM identity.** Without the asymmetry
   mechanism, the framework has mass spectrum but no dark matter abundance.
3. **Lepton sector is open** (Seifert demoted; Koide is numerology-grade until the 2/9
   derivation is produced — see Finding F3).
4. Fractal-H0 mechanism relies on the percolation identification [LIT+HYP]; residual
   tension ~3σ is honestly stated but remains a live exposure.

## 7. Literature-exclusion check

Berezhiani–Khoury and Tulin–Yu: cited. **Missing (mandatory): Milgrom 1983** (the a0
scale and the a0 ~ cH0 coincidence are his original observations — the participation-law
subsection currently reads as if the coincidence were novel) **and Verlinde 2016**
(emergent-gravity apparent-DM relation g_D ~ √(a_M g_B) shares the quadrature structure;
a one-sentence comparison is required to delimit novelty: the participation law's novelty
is the *exact* standard-μ equivalence + n = 1 uniqueness + zero-parameter test, not the
scale coincidence).

## 8. Stale-claim sweep — FINDINGS (mandatory fixes)

- **F1 (l.1679):** V9 summary still lists "Relic Density: PASS, Ωh² = 0.1241" — that is
  the *superseded* DT-1 freeze-out; after GAP-N4d it is misleading in a summary surface.
  Flag as superseded with pointer to the tower computation.
- **F2 (l.1087 ff):** the DT-1 relic subsection's "Key result" block lacks a superseded
  banner (its SIDM sibling has one).
- **F3 (l.764):** "we **proved** this phase corresponds to the Topological Spin h = 2/9"
  — no such proof exists in the repository. Downgrade to identification [HYP] while
  keeping the (spectacular) 0.001% numerical agreement.
- **F4 (abstract, 2026 box):** predates the 2026-08-13/14 campaigns; must mention:
  real-data gate upgrades, the zero-parameter galaxy sector, and the symmetric-relic
  exclusion → asymmetric target (the abstract currently overstates the production story
  by omission).
- **F5 (bibliography):** add Milgrom 1983; Verlinde 2016; cite at the participation-law
  subsection.

## 9. Verdict

**MINOR REVISION → then preprint-ready.** The framework's honest-labeling discipline is
now exemplary: every failed claim is struck in place, every open item is named with a
falsifier, all numbers trace to committed code. Mandatory: F1–F5 (mechanical, same-day).
Recommended next research (not blocking): GAP-N4d-asym mechanism; participation-law
hydrodynamics; 2D BdG formality; Chandra-based G1.

**Publication-readiness statement:** with F1–F5 applied, this referee finds no remaining
claim in the manuscript that is stated above its evidential grade.
