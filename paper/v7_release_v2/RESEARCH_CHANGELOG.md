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

## 2026-08-13 (standardization campaign) — Data verification, real-data figures, citation audit

DATA (independently verified against pdgLive this session):
- m_tau = 1776.93 +/- 0.09 MeV (repo carried old average 1776.86 - CORRECTED)
- m_Z = 91.1879 +/- 0.0020 GeV (was 91.1876 - updated)
- m_W = 80.3692 +/- 0.0133 GeV (confirmed)
- data/PDG_2024.json updated with verification block (date, method, corrections)
- Derived: M* 365.24 -> 365.26 GeV (+0.004%, inside all quoted precisions);
  tower 184-201 TeV unchanged; Z(8,8) tension 58.4 -> 62.9 sigma
- SPARC: 175/175 files verified, structure spot-checked (NGC3198)
- VF appendix: M* updated + Data Provenance paragraph added

FIGURES (all rebuilt from real computed data; generator committed):
- experiments/figures/make_genesis_figures.py -> 4 publication figures
  (Okabe-Ito CVD-safe, dataviz standard): quantization convergence +
  saturation, Hopf charge algebra, protection law, tower spectrum
- Inserted into the Genesis chapter with provenance-citing captions

CITATION AUDIT (from compile-log census):
- 5 missing bibitems added (Baez 2002 Octonions; Kaloper-Padilla PRL 112;
  Clowe 2006 ApJL 648; Friedan PRL 45; Hull-Townsend NPB 274)
- chap:division_algebras label added; fig:h0_shift dangler resolved by
  rewording to the derivation (figure never existed)

FINAL STATE: 0 errors, 0 undefined citations, 0 undefined references,
0 multiply-defined labels, 174 pages.

## 2026-08-13 (later): Formula audit — two claims corrected; real Bullet data

AUDIT (experiments/verification/formula_audit.py; log results/logs/formula_audit_20260813.log;
21 independent recomputations: 18 PASS / 2 NOTE / 1 FAIL):

- Seifert lepton hierarchy (Sec 8.4.4 "Problem C" + Appendix Z + Genesis):
  recomputed m_tau/m_mu = 17.37 vs 16.82 observed (3.3%, NOT the "<1%"
  claimed); same exponents give m_mu/m_e = 116.5 vs 206.77 (44% FAIL).
  Claim downgraded from "quantitative resolution" to "candidate organizing
  principle"; audit boxes added in Sec 8.4.4 and Appendix Z; Genesis
  cross-reference updated. Absolute form m_i = M* e^{-4XS_i} flagged
  ratio-only.
- H0 inference (Sec 7.2/7.4 + Conclusions): the quoted 70.6 km/s/Mpc mixed
  two sound-horizon anchors (r_drag = 147.09 vs r_* = 144.43 behind the
  D_A ~ 13800 baseline). Self-consistent value from the report's own
  Eq. (eq:da_inference): H0 = 67.4 x 13800/13544 = 68.7; tension reduction
  ~23% (4sigma -> ~3sigma), not ">60%". All four occurrences corrected +
  audit box; fractal-figure caption overclaim ("H0 ~ 73") reworded.

GATE 3 (grid-edge issue closed): a0 grid extended 3300-3700/9pts ->
2800-3800/21pts; best a0 = 3350 now interior; held-out test chi2_red =
4.746 PASS (log results/logs/G3_20260813.log). Criterion unchanged.

REAL DATA (Bullet Cluster, first real-survey data in repo):
- data/raw/bullet_optical.fits (DSS) + bullet_xray.fits fetched via
  astroquery SkyView. First fetch used 'RASS Background 1' (a modeled
  background map) — caught in audit, re-fetched as 'RASS-Cnt Broad'
  photon counts; fetch script corrected.
- New figure fig_bullet_realdata.png (generator
  experiments/bullet_cluster/plot_bullet_realdata.py, log
  results/logs/bullet_realdata_20260813.log): DSS + smoothed RASS contours;
  X-ray centroid RA 104.62, Dec -55.95 coincides with cluster position.
  Honest scope in caption: location only, substructure needs Chandra.
  Inserted after the extreme-environment figure (label fig:bullet_realdata).
- data/README.md raw/ row corrected (was mislabeled "Chandra + weak-lensing").
