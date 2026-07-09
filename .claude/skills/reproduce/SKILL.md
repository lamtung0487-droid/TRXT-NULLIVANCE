---
name: reproduce
description: Clean reproduction check for a TRXT-Nullivance result. Use to verify that a named experiment script still runs from the current repository state and reproduces its recorded outputs (figures/logs), e.g. before a release, after restructuring, or when a reviewer requests it.
---

# Reproducibility Check

## Procedure

1. **Environment**: verify Python ≥3.10 and `pip install -r requirements.txt` succeeds (use a venv in the scratchpad when a truly clean environment is needed). Record package versions with `pip freeze` into the report.
2. **Provenance**: record `git log -1 --oneline` and `git status --short` (a dirty tree must be noted — reproduction from a dirty tree is second-class).
3. **Data presence**: confirm the datasets the script reads exist under `data/` (check the script's file-open calls). If external data is missing, follow `data/README.md` to fetch it; never substitute synthetic data silently.
4. **Run from repo root**: `python experiments/<phase>/<script>.py`, capturing stdout/stderr to `results/logs/repro_<script>_<YYYYMMDD>.log`.
5. **Compare**:
   - Numerical outputs vs the values recorded in the original log in `results/logs/` (or in the manuscript) — state the tolerance used and justify it (solver tolerance, seed determinism).
   - Regenerated figures vs `results/figures/` — same qualitative content and axis ranges; note any drift.
6. **Verdict**: **REPRODUCED / REPRODUCED-WITH-DRIFT (quantified) / FAILED**, written at the top of the log.

## Failure handling

- Import/path errors after the 2026-07 restructuring: scripts must be run from repo root; if a script hardcodes an absolute `C:\Users\...` path, fix it to a repo-root-relative path and note the fix in the log.
- A FAILED reproduction of a manuscript-cited number is escalated immediately: flag it in `theory/reviews/` and notify the referee protocol — the number is quarantined until resolved.
