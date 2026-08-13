# RESEARCH_CHANGELOG — paper/v7_release_v2

## 2026-08-13 — Genesis integration (2026 lab campaign)

All entries backed by SIGNED-OFF derivation notes / ACCEPT referee reports in
`theory/reviews/` and logs in `results/logs/` (repo git history = audit trail).

- **NEW** `chapters/Chapter_Genesis_MassChain.tex` — the theoretical spine:
  Void (Bogomolny principle, Mass = 4piK x Incompleteness, protection law) ->
  symmetry cascade (pi2 = pi1 selection; matter iff surviving U(1)) ->
  Great Condensation (transmutation, M_cond, golden-ratio doublet) ->
  lifted Universe (Derrick + NJL quartic theorem, Q_Hopf = pq, VK bound,
  tower law M = 3.95 N_f M sqrt(ln) (pq)^(3/4), 184-201 TeV, SM exclusion).
  Input into main tex before "Mathematical Formalism".
- **Abstract**: dark-energy phrase corrected (relaxed ground state, per PI);
  2026 Revision box added (sec:genesis + sec:revisionrecord cross-refs).
- **Sec. 8.4 (spectrum)**: erratum banner — harmonic law demoted to
  breathing-mode fine structure; label sec:spectrum-old added.
- **NEW Section "Revision Record" (sec:revisionrecord)** before appendices:
  the seven overturned/demoted claims with replacements (Honest Null Results law).
- **Appendix T.1**: erratum banner — Ricci-flow derivation invalidated (I-1);
  text retained as historical record.
- **Labels added**: sec:screening, sec:smlimit.
- **Bibliography**: +10 entries (Belavin-Polyakov, Struwe, Qing,
  Hasenfratz-Niedermayer, Karowski-Thun, GN kinks PRD 51 4503, Coldea 2010,
  Vakulenko-Kapitanskii, Harland 1311.2403, Sutcliffe 0705.1468).

Backing artifacts: derivation_layer0_mass_principle / substrate_resolution /
dimensional_lift / njl_quartic / mass_constant / stage_gaps / screening_branch
(+ audits, all 2026-07-09/08-13); referee_report_layer0_mass (final ACCEPT);
results/logs/gate_ledger.md (LADDER CLEAR 2026-08-13).
- Note: pre-existing dangling ref fig:h0_shift (present in HEAD; not introduced by this revision) - fix when the H0 figure is regenerated.

## 2026-08-13 (later) — Full local compile achieved: 0 errors, 165 pages

Toolchain: TinyTeX v2025.07 installed at %LOCALAPPDATA%\TinyTeX (same pdfTeX
engine family as the author's original build); packages from the era-matched
tlnet-archive snapshot (2025/07/15; tcolorbox version-pinned to match kernel).

Source fixes (content-preserving, all flagged):
- Preamble: +fontenc [T5,T1] (Vietnamese via vntex), \slashed local macro,
  \qed providecommand, alphalph (appendix sections beyond Z), tcolorbox.
- Vietnamese fragments wrapped in \vntext{}: the "Trục Rung Xuyên Tầng"
  footnote, the Appendix Y void quote, "nảy sinh" in Appendix Z.
- Markdown leakage converted to LaTeX: 61 `**bold**` -> \textbf, 7 `code`
  spans -> \texttt (11 files); mixed `\textbf{...**` on Chapter_X l.63.
- Equation fix: \cdot inside \text{} (Appendix Q r_0 formula).
- \& escaped in two subsubsection titles; Br_3 -> $Br_3$; beta char -> $\beta$;
  underscore escape in Appendix_S path.
- DISCOVERY: chapters/Chapter_{X,Y,Z} sources EXIST (the earlier
  "missing section 5" was a compile-order illusion); only the AB/AC/AD/VF
  appendix blocks remain PDF-only.
- Remaining warnings (non-blocking, tracked): duplicate \input of
  Appendix_AA (pre-existing), dangling fig:h0_shift (pre-existing),
  some undefined/multiply-defined label warnings.

Build: pdflatex -interaction=nonstopmode TRXT_Research_Report_V14_FINAL.tex (x2)
Output: TRXT_Research_Report_V14_FINAL.pdf — 165 pages, 4.7 MB, 0 errors.

## 2026-08-13 (final) — Four rewritten appendices + repo hygiene

Pre-write deep search confirmed: after the Chapter_{X,Y,Z} discovery, the
AB/AC/AD/VF blocks are genuinely PDF-only (searched all paper trees, results/,
archive; the C1C5_Resolution_Report and AUDIT_REPORT_V14_COMPREHENSIVE are
different documents - historical audit artifacts).

- NEW appendices (rewritten, not transcribed - several original claims were
  overturned): Appendix_AB_Resolutions (status table AB.1-AB.10),
  Appendix_AC_OpenProblems (honest register incl. reopened C1/C2),
  Appendix_AD_Numerical (rebuilt gate system + Layer-0 suite + reproduction),
  Appendix_VF_MasterScale (reconstructed chain with GAP-N4c condition note).
- FIX: duplicate \input of Appendix_AA commented out (pre-existing double
  inclusion; multiply-defined-labels warning eliminated).
- Repo hygiene: results/FINAL_ACADEMIC_REPORT_V25 (misplaced early Vietnamese
  draft) -> paper/early_drafts_v25; mc_null_test script -> experiments/
  mass_spectrum/; loose results/*.png -> results/figures/, *.json ->
  results/data/.
- Build: 0 errors, 172 pages. Remaining warning: pre-existing fig:h0_shift.
