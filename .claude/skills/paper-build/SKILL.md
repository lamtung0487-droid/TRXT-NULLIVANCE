---
name: paper-build
description: Manuscript work for TRXT-Nullivance - integrating validated results into a LaTeX paper tree under paper/, compiling it, and maintaining the research changelog. Use for editing .tex chapters/appendices, adding figures from results/, or producing a compilable PDF.
---

# Manuscript Integration & Build

## Paper trees (peer versions, no single canonical)

| Tree | Content |
|---|---|
| `paper/v7_release_v2/` | Newest V14–V17 line: main report + appendices + audit reports (most recently edited) |
| `paper/v7_release/` | Earlier V14 release line (frozen; contains its own `source_code/` snapshot) |
| `paper/v8_release/`, `paper/v9_campaign/` | Draft lines |
| `paper/submission_v16/` | English submission line (`TRXT_Research_Report_English.tex`) + `RESEARCH_CHANGELOG.md` |

Ask the user which tree they are targeting if not obvious from context. Treat the non-targeted trees as frozen — never edit them "for consistency".

## Integration rules

1. **Provenance gate**: a number or figure enters the .tex only if it has (a) a Gate log in `results/logs/`, and (b) an ACCEPT referee report in `theory/reviews/`. Otherwise stop and run `/peer-review` first.
2. **Figures**: copy from `results/figures/` into the paper tree's `figures/` dir (papers must be self-contained); reference the generating script in the figure caption or a comment above `\includegraphics`.
3. **Changelog**: every content change gets a dated entry in the tree's `RESEARCH_CHANGELOG.md` (create one if the tree lacks it): what changed, which log/review backs it.
4. **Honesty in prose**: postdictions are not called predictions; open GAPs from derivation notes appear in the paper's limitations section, not nowhere.

## Build

- Compile from within the paper tree: `pdflatex -interaction=nonstopmode <main>.tex` (twice for references; `bibtex` if a .bib exists). Main files: `TRXT_Research_Report_V14_FINAL.tex` (v7 trees), `TRXT_Research_Report_English.tex` (submission_v16).
- Build artifacts (.aux/.log/.out) are gitignored — do not commit them.
- On LaTeX errors, fix the source; never delete content to make it compile without flagging it.
