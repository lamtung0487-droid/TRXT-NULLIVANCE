# TRXT-Nullivance RESEARCH LOG
**Living document — the complete record of the 2026-07-09 lab campaign, kept for writing the next revision of the research report.**
Companion to `theory/RESEARCH_ATLAS.md` (knowledge map of the old report). Every claim here has a git-committed artifact; cite by file, never from memory.

---

## 0. THE MASTER MANUSCRIPT (for future editing)

**Canonical source to edit:** `paper/v7_release_v2/TRXT_Research_Report_V14_FINAL.tex` (2,503 lines, newest revision, date "February 27, 2026") + `paper/v7_release_v2/appendices/` (22 files, all `\input` from the main tex).

**Provenance finding (2026-07-09):** the compiled `paper/TRXT_Research_Report.pdf` (191 pp.) contains four appendix blocks whose LaTeX source exists **nowhere in this repository** and not in the author's GitHub repo (checked via API — no .tex files there):

| Missing block | PDF pages | Content |
|---|---|---|
| Appendix AB "Comprehensive Resolution" | ~150–155 | C-factor proof, 't Hooft matching, g=4, relic retraction+update, sector status, DE-EOS reconciliation, SPARC re-analysis, unified action seams |
| Appendix AC "Resolution of Critical Open Problems" | ~155–159 | Clifford-tower λ_χ, G₂-branching sectors (p=5, 8), relic with derived coupling, NJL baryogenesis, MaVaN params |
| Appendix AD/AJ "Comprehensive Numerical Verification" | ~159–174 | 6-model SPARC comparison (B2 96.5%), BBN scan, CMB distance priors |
| Appendix VF "First-Principles v_F = 1/5" | ~183–187 | Chirality Reduction chain Cl(6) → v_F → C → M\* |

**Action when editing:** these sections must be re-transcribed from the PDF (full text extraction procedure: PyPDF2, see memory note `research-atlas`) or re-written fresh — the latter is recommended since several of them are exactly the sections our audits overturned (AC.2, relic story). Everything else in the PDF maps to existing .tex files: main text → main tex ll. 1–2503; Seifert/AK → `appendices/Appendix_Z.tex`; sigma-model/AL → `Appendix_Y_Layer0.tex`; mode selection → `Appendix_W_ModeSelection.tex`; ghost proof → `Appendix_X_GhostFree.tex`; Hopfions → `Appendix_Q_SIDM.tex`(+`Appendix_T_Topology.tex`); Bullet → `Appendix_S_Bullet_Cluster.tex`.

## 1. CAMPAIGN TIMELINE (git history = authoritative)

| Commit | What happened |
|---|---|
| `f21e4f1` | Repo restructured into research-lab layout; ~1.9 GB junk removed; lab system created (CLAUDE.md charter, 5 agents, 5 skills, RESEARCH_WORKFLOW) |
| `1f76acb` | **Full-framework verification campaign**: gate ladder re-run; MC null test kills the unconstrained mass-law statistics (W p=0.225, Z p=0.590, H p=0.090; 52.5% of random masses match at 0.1%); J1 relic circularity exposed; referee verdict REJECT-as-validated / encourage-as-exploratory |
| `448e62c` | **/derive (p,q) selection**: rigid-torus axiom A2′ (SL(2,ℤ) obstruction); ERROR-1 antiparticle cascade; Hurwitz selection d ∈ {1,2,4,8} (W excluded, margins 18–158×; Z at 58.4σ); Bott endpoint 2⁷ = 128; conditional DT-1 prediction 5.707 GeV |
| `1f76acb`→`589c54d` | **E_core incompatibility theorem** (mass law ⊕ stable vacuum: σ₀ ≥ 13.5 GeV vs ≤ 3.5×10⁻⁶ GeV, gap 6.6 orders; SIGNED-OFF) |
| `0bf0dae` | **PI correction adopted**: dark energy = condensate relaxation at V_NJL minimum (report §7.3), not tension; theorem sharpens to binary dilemma; corollary b′: emergent gravity pins stiffness large |
| `0dafd83` | **RESEARCH_ATLAS**: sequential read of all 191 pages; per-phenomenon map; inconsistency registry I-1…I-10 |
| `efc6779` | **Three-task campaign**: I-1/I-2 resolved (T.1 invalid, R ∝ p geometry mandatory, static energy real; **I-11**: WEP appendix uses total energy — gap-only mass contradicts it); AC.2 audit NOT SIGNED-OFF (dim-sums reach every integer 1–15; winding ≠ rep-dimension; Z⁰/color mismatch); **gate suite rebuilt** (central runner, frozen criteria, held-out G3 test χ²=4.75, real PRyMordial BBN run Yp=0.24689, new G0b FAILS honestly on X<0) — ladder verdict now BLOCKED(G0b) |
| `983909c` | **/derive Layer-0 mass principle**: M = 4πK·\|Q\| (Belavin–Polyakov); bubbling ⟹ Mass = 4πK × Incompleteness; m = (8/e)Λ exact gap; G₂/SU(3) ≅ S⁶ ⟹ fermionic O(7) GN ratio m₂/m₁ = φ; numerics on the framework's own kernel (E/(4πI): 1.54 → 1.09; Q=2 saturation 0.988→1.0006); audit caught σ-model→GN erratum |
| `3408e59` | **Adversarial peer review of the principle: MAJOR REVISION** — F1 substrate ambiguity (S² evidence vs S⁶ φ-claim); F2 lattice charge non-conservation (Q_net −13 → +3; protection approximate; new GAP-5); F3 Q=1 seam artifact; F4 GN literature check pending; F5 Derrick scoping |

## 2. STANDING RESULTS (what the next report can assert, with artifact)

**Established (SIGNED-OFF, survives adversarial review):**
1. The pure inverse mass law M\*(1/p+1/q) cannot be the principal mass term: E_core theorem (all three scalings p, pq, Q^{3/4}), `derivation_ecore_tension_20260709.md` + audits.
2. R ∝ p is the only law-compatible geometry; App. T.1 must be excised (`derivation_soliton_geometry_20260709.md`).
3. Contradiction I-11 (WEP vs gap-only mass) — new, ours.
4. Bogomolny principle at Layer 0: M = 4πK·\|Q\|, linear/additive/cascade-immune; Mass = 4πK × Incompleteness Functional; numerically supported on the framework's own kernel (`experiments/layer0/bp_mass_quantization.py`, two logs). *Scoped by referee F1/F2/F5.*
5. Gate-suite integrity system (`scripts/run_gates.py` + `gates_criteria.json`); current honest ladder verdict **BLOCKED at G0b** (X<0 instability window — also mathematician audit Item 5).
6. First genuine local BBN computation: Yp = 0.24689, Neff = 3.044, TRXT(Tc = 1 eV) deviation 0.000% (G5b log).
7. Held-out SPARC: a0 = 3350 (train), test χ²_red = 4.75 PASS (G3 log; a0 at grid edge — extend grid).

**Overturned / downgraded (must be rewritten in the manuscript):**
- AC.2 "C2 RESOLVED" → OPEN (`audit_ac2_sectors_20260709.md`).
- Universal Stability Theorem → holds only in positive-winding sector (ERROR-1).
- Unconstrained mass-law statistics → null (`data_confrontation_20260709.md`, K.5 vs U.8 inconsistency I-3).
- DT-1 = 5.707 GeV → conditional only (withdrawn as unconditional, P2′).
- Gate-3 "χ²=4.9986 PASS" → replaced by held-out protocol.
- Gate-5 "PASS (By Design)" → replaced by real computation.

**Open problems, ranked (the research programme):**
1. **F1 + GAP-1 (merged): the substrate/bridge question** — declare Layer 0 target (S² vs S⁶ = G₂/SU(3), or S⁶-fibration → S²) and determine which energy–charge law (linear vs Q^{3/4}) the L0→L1 lift transports. Everything hangs here.
2. **F2/GAP-5:** quantify lattice charge-violation rate vs stiffness K (controlled simulation; matters for proton stability claims).
3. **G0b:** cure the X < 0 branch of P(X) (candidate: DBI completion) — unblocks the ladder.
4. **F4:** literature confirmation of odd-N O(7) GN spectrum (blocked by environment; retry when WebSearch works).
5. F3: redo Q = 1 saturation on disk geometry.
6. New assignment table under the corrected law — only after (1), under pre-registered rules + null tests.

## 3. MANUSCRIPT REVISION MAP (finding → file → action)

| # | Target (in `paper/v7_release_v2/`) | Action |
|---|---|---|
| R1 | Main tex §8.4 (mass law, ll. ~600–700 incl. Eq. 57 area & Seifert calibration l. 659) | Rewrite: demote 1/p+1/q to breathing-gap fine structure; introduce E_core budget and the Layer-0 principle as the principal term (cite our derivation notes) |
| R2 | `Appendix_T_Topology.tex` (T.1 Ricci-flow mass) | **Excise or rewrite** — internally inconsistent (I-1) |
| R3 | `Appendix_W_ModeSelection.tex` | Correct Universal Stability Theorem scope (positive-winding only); fix K.5 vs U.8 statistics inconsistency (I-3); keep the honest U.8 assessment |
| R4 | Missing App. AC (re-transcribe) | Do NOT restore "C2 RESOLVED"; state sectors as OPEN per audit; the G₂-branching idea may stay as *hypothesis* with the audit's objections noted |
| R5 | `Appendix_X_GhostFree.tex` | Extend the proof to X < 0 or state the screening-branch instability window openly (G0b, audit Item 5) |
| R6 | Main tex WEP passage (p. 19 region) + §8.4 | Resolve I-11: one consistent definition of inertial mass |
| R7 | `Appendix_Y_Layer0.tex` (AL) | Add: Bogomolny bound, bubbling quantization, Mass = 4πK×I, the numerical tests, and the F2 caveat (approximate protection on the lattice, rate TBD) |
| R8 | `Appendix_Z.tex` (AK Seifert) | Fix E_vac two-index/three-index inconsistency (torus formula on (3,3,3)); keep the m_τ/m_μ = 16.8 result (it survives) |
| R9 | Missing App. AD/AJ (re-transcribe) | Update Gate-3 numbers to held-out protocol; reconcile the three conflicting SPARC scorecards (I-5) |
| R10 | Main tex §9.10/BBN + missing AB.8 | Replace "By Design" language with the real PRyMordial run numbers |
| R11 | Abstract + §1.5 claims table | Update: mass-law status, gate verdict BLOCKED(G0b), DT-1 conditional; the claims table (p. 16) was already honest — keep its spirit |
| R12 | New appendix | The E_core incompatibility theorem + decision fork (F1 adopted branch), from our signed-off notes |

## 4. HOUSEKEEPING FACTS FOR THE NEXT SESSION

- All lab artifacts live in `theory/` (7 derivation/audit/referee docs dated 20260709) + `results/logs/` (gate logs, MC tests, quantization logs) + `experiments/layer0/`.
- Environment quirks: run from repo root with `PYTHONIOENCODING=utf-8`; Agent spawning broken (forced nonexistent model — run roles inline); WebSearch/WebFetch broken (same fault); PRyMordial works locally via `paper/v7_release/source_code/bbn_prymordial/PRyMordial`.
- Gate ledger: `results/logs/gate_ledger.md` (append-only; criteria frozen in `scripts/gates_criteria.json`).
- The PDF text extraction lives in the session scratchpad (`report_text/`, 12 chunks) — re-extract with PyPDF2 if a new session needs it.
