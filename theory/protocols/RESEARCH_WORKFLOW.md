# TRXT-Nullivance Research Workflow

The pipeline every research thread follows. Each stage has an owner (a lab agent from `.claude/agents/`), an entry condition, and a written artifact. No stage may be skipped; a stage without its artifact did not happen.

```
 Hypothesis
     │
     ▼
 [1] DERIVATION            owner: theorist        skill: /derive
     │  artifact: theory/derivation_<topic>_<date>.md (axioms, steps, GAP list, predictions table)
     ▼
 [2] RIGOR AUDIT           owner: mathematician
     │  artifact: theory/reviews/audit_<topic>_<date>.md
     │  verdict SIGNED-OFF required to proceed; BLOCKED → back to [1]
     ▼
 [3] IMPLEMENTATION        owner: computational-physicist
     │  artifact: code in src/ or experiments/ + convergence study in results/logs/
     ▼
 [4] GATE VALIDATION       owner: computational-physicist   skill: /validate-gates
     │  artifact: results/logs/gate<N>_<date>.log + entry in results/logs/gate_ledger.md
     │  FAIL → escalate to theorist as potential falsification (no patching — Anti-Frankenstein Law)
     ▼
 [5] DATA CONFRONTATION    owner: data-analyst
     │  artifact: confrontation report (results/logs/) with verdict CONSISTENT / TENSION / EXCLUDED
     ▼
 [6] ADVERSARIAL REVIEW    owner: referee          skill: /peer-review
     │  artifact: theory/reviews/referee_report_<topic>_<date>.md
     │  verdict ACCEPT required to proceed; MAJOR → back to [1], MINOR → fix and re-review
     ▼
 [7] PUBLICATION           owner: theorist + user  skill: /paper-build
        artifact: .tex update + RESEARCH_CHANGELOG.md entry in the target paper tree
```

## Definition of Done, per stage

| Stage | Done means |
|---|---|
| 1 Derivation | All 6 axiom items declared, no unlabelled gaps, predictions table present |
| 2 Audit | Every step verdicted SOUND/GAP/ERROR; overall SIGNED-OFF |
| 3 Implementation | Runs from repo root; parameters only via `src/core/constants.py`; ≥3-resolution convergence study |
| 4 Gates | Pass metric vs pre-declared criterion recorded; ledger updated |
| 5 Data | Full declared sample, χ²/dof + error budget, null model beaten with corrected significance |
| 6 Review | All six audits run; verdict on file |
| 7 Paper | Changelog entry links the number → gate log → referee report |

## Cross-cutting rules

- **Falsification is a result.** A thread that dies at stage 4 or 5 is written up honestly in `results/logs/` and the spec is updated. Threads are never silently abandoned.
- **One thread, one topic.** Parallel hypotheses get separate derivation notes; never blend them mid-pipeline.
- **Reproducibility on demand.** Any artifact number must survive `/reproduce` at any time; a failed reproduction quarantines the number.
- **Version discipline.** Spec changes land in `theory/specs/` with a version bump note; the current master spec is `theory/specs/v17/TRXT_V17_Master_Spec.md`.

## Typical invocations

- New idea: ask the **theorist** agent to run `/derive` on it.
- "Is this derivation sound?": launch **mathematician** on the note.
- "Did we break anything?": `/validate-gates` (full ladder).
- Before editing the paper: `/peer-review` the claim, then `/paper-build`.
- Reviewer asks "can you reproduce Fig. 3?": `/reproduce` with the generating script.
