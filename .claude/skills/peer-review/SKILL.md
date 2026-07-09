---
name: peer-review
description: Adversarial internal peer review of a TRXT-Nullivance claim, derivation, or manuscript section before it is considered established. Runs the referee attack protocol (hardcode audit, circularity audit, degrees-of-freedom count, reproduction attempt, robustness probes, literature exclusion check) and produces a verdict report.
---

# Internal Peer Review Protocol

Launch the **referee** agent (`.claude/agents/referee.md`) with the claim under review, or execute this protocol directly. The standard is a hostile-but-fair PRD/JCAP referee.

## Inputs required before starting

- The precise claim (one sentence, quantitative)
- Where it lives: derivation note in `theory/`, script in `experiments/` or `src/`, manuscript section in `paper/`
- Which Gate log supports it (`results/logs/`)

If any of the three is missing, the review verdict is automatically **NOT READY** — send it back.

## The six audits (all mandatory)

1. **Hardcode audit** — trace every parameter to a derivation or a declared measured input; grep solver code for magic numbers.
2. **Circularity audit** — verify no dataset both fixed a parameter and "confirmed" it; check changelog dates for postdictions labelled as predictions.
3. **Degrees-of-freedom audit** — honest count of ALL adjustable quantities including discrete choices (mode assignments, galaxy selections, prior boundaries). Demand look-elsewhere-corrected significance for any scanned pattern.
4. **Reproduction** — rerun the supporting script(s) from repo root in a fresh shell; numbers must match the claim to stated precision.
5. **Robustness** — perturb inputs within 1σ, vary seed/resolution; the conclusion must survive.
6. **Exclusion check** — known constraints: solar-system PPN, BBN abundances, CMB, GW170817 (|c_T/c − 1| ≲ 1e-15), lab gravity, PDG limits. WebSearch when uncertain; cite specifically.

## Output

`theory/reviews/referee_report_<topic>_<YYYYMMDD>.md` with:
- Restated claim
- Numbered findings tagged MAJOR / MINOR / QUERY with file:line references
- Reproduction result (both sets of numbers if mismatch)
- **Verdict: ACCEPT / MAJOR REVISION / REJECT**

A claim enters a manuscript only with an ACCEPT on file. MAJOR findings reopen the derivation stage (`/derive`), not the wording.
