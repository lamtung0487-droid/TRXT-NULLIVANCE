# TRXT V16 — Science‑grade Patch Notes (v2)

This file is meant to be **copy/paste friendly** into the current PDF/LaTeX draft.
It focuses on **hard correctness fixes** (numbers, dimensions, references) and on
**claim‑tightening** (what can be stated as derived vs. conjectured).

---

## 1) Critical numerical correction — Vainshtein radius

Your draft currently states a Vainshtein radius of order **~107 AU** for Solar System screening.
If you adopt the standard DGP/cubic‑Galileon scaling with a cosmological crossover scale
\(r_c \sim H_0^{-1}\), then

\[
r_V = \left(r_s\, r_c^2\right)^{1/3},
\qquad r_s = \frac{2GM_\odot}{c^2}\approx 2.95\ \mathrm{km},
\qquad r_c \approx H_0^{-1}\sim 4\ \mathrm{Gpc}.
\]

Numerically this gives

\[
r_V \approx 2.4\times 10^7\ \mathrm{AU},
\]

i.e. **many orders of magnitude larger** than the Solar System.  
This is good news (screening is extremely efficient), but the paper must use the **correct value**.

A typical post‑Newtonian deviation scales as
\[
|\gamma-1|\sim \left(\frac{r}{r_V}\right)^{3/2},
\]
so at \(r=1\,\mathrm{AU}\), one gets \( |\gamma-1|\sim 10^{-11}\), far below Cassini.

**Action:** replace the numerical value in the Solar‑System section and ensure the
choice of \(r_c\) is stated explicitly.

---

## 2) Critical dimensional‑analysis fix — derivative phonon coupling

The draft uses an interaction of the schematic form
\[
\mathcal{L}_{\rm int}\sim \frac{c_N}{\Lambda^2}\,\chi\,(\partial_\mu\theta)\,\bar N\gamma^\mu N.
\]

With \(\theta\) a superfluid phase (dimensionless), \(\partial_\mu\theta\) has mass dimension 1,
\(\bar N\gamma^\mu N\) has dimension 3, and a scalar \(\chi\) has dimension 1.
So the operator has total dimension \(1+1+3=5\), hence the coefficient must scale as **\(1/\Lambda\)**,
not \(1/\Lambda^2\), to keep \(\mathcal{L}\) dimension 4.

Two consistent options:

**(A) Scalar DM \(\chi\):**
\[
\mathcal{L}_{\rm int}= \frac{c_N}{\Lambda}\,\chi\,(\partial_\mu\theta)\,\bar N\gamma^\mu N.
\]

**(B) Fermionic DM \(\chi\):** use a DM current \(J_\chi^\mu=\bar\chi\gamma^\mu\chi\) (dimension 3):
\[
\mathcal{L}_{\rm int}= \frac{c_N}{\Lambda^3}\,(\partial_\mu\theta)\,J_\chi^\mu\,\bar N N,
\]
(or other Lorentz structures), which is dimension‑7 and properly suppressed.

Your **\(v^4\)** suppression logic can survive, but **the absolute normalization of the
direct‑detection cross section will change by powers of \(\Lambda\)**.

**Action:** choose A or B, propagate the power of \(\Lambda\) through the amplitude and
cross section, and regenerate the exclusion comparison plot.

---

## 3) Critical physics correction — SIDM cross section estimate

The draft estimates a soliton radius \(R_s\sim 1/M_*\) with \(M_*\approx 365\) GeV and uses that to
claim a sizeable \(\sigma/m\). However,

\[
1/M_* = \frac{\hbar c}{M_*}\approx \frac{0.197\ \mathrm{GeV\,fm}}{365\ \mathrm{GeV}}
\simeq 5.4\times 10^{-4}\ \mathrm{fm},
\]

which implies

\[
\frac{\sigma}{m} \sim \frac{\pi R_s^2}{m} \sim 10^{-9}\ \mathrm{cm^2/g},
\]

i.e. **far too small** for halo‑core phenomenology (\(\sigma/m\sim 0.1\)–\(1\ \mathrm{cm^2/g}\)).

Therefore, the SIDM component **cannot** be justified by a hard‑sphere geometric estimate
with \(R_s\sim 1/M_*\). You need an **enhancement mechanism**:

- near‑threshold resonance (Sommerfeld / Breit‑Wigner),
- long‑range mediator (dark phonon / dark photon) giving velocity dependence,
- collective‑mode scattering in a condensate (superfluid phonon exchange) with large
  transport cross section.

**Action:** downgrade the current SIDM claim to a **model requirement** and add a placeholder
subsection: “Mediator/Resonance needed for \(\sim 10^5\)–\(10^6\) enhancement”.

---

## 4) Internal consistency — “primitive (p,q)” vs Dark Tower labels

If you enforce “primitive” \(\gcd(p,q)=1\) for topological modes, then Dark Tower
entries like \((128,128)\) and \((256,256)\) violate that rule.

Two clean fixes:

- **Fix 1:** allow non‑primitive pairs for the *dark condensate sector* (state it explicitly).
- **Fix 2:** re‑parameterize with a primitive pair plus an integer multiplicity:
  \((p,q)=n(p_0,q_0)\) with \(\gcd(p_0,q_0)=1\). Then the dark “tower index” is \(n\).

**Action:** pick one and align the whole paper’s definitions.

---

## 5) Emergent Lorentz invariance — EFT/ghost statement

A dispersion term of the form \((\Box\phi)^2/M_{\rm Pl}^2\) is a higher‑derivative operator and
generically introduces an Ostrogradsky ghost if treated as fundamental.

You can keep it safely by stating the standard EFT condition:

- The operator is **EFT‑suppressed** and only trusted for \(p\ll \Lambda_{\rm LIV}\),
  where \(\Lambda_{\rm LIV}\lesssim M_{\rm Pl}\).
- The would‑be ghost sits above the cutoff and is not part of the low‑energy spectrum.

**Action:** add a short paragraph in the Lorentz section: “We treat LIV operators as EFT
corrections; no claim of UV‑complete ghost‑free dynamics is made.”

---

## 6) Reference corrections (high priority)

Your bibliography currently cites an **incorrect ATLAS entry** (EPJ C 84 451) as the W‑mass
measurement. That EPJ C paper is the LHC‑TeV MW working group compatibility analysis,
not the ATLAS W‑mass result.

Suggested BibTeX‑ready replacements (verify journal metadata in your .bib):

- **ATLAS W mass (2023 preliminary):** ATLAS public note / arXiv preprint (if present).
- **ATLAS W width (2024):** Eur. Phys. J. C 84 1309 (this is the width paper).

Also ensure the PDG citation is current (2024/2025 update), and that LZ/XENONnT/PandaX
citations correspond to the correct low‑mass sensitivity statements.

---

## 7) Claim‑tightening checklist for submission

Replace “validated” language with:

- “derived under Assumptions A–D” for the torus band constant \( \mathcal{C}\),
- “consistent with constraints” for Lorentz bounds,
- “requires mediator/resonance” for SIDM,
- “conditional on experimental resolution” for W‑mass (CDF vs LHC).

---

## 8) Quick numeric appendix items (copy/paste)

\[
r_V(M_\odot)\approx 2.4\times 10^7\ \mathrm{AU}\quad (r_c=4\ \mathrm{Gpc}),
\qquad
\left(\frac{1\ \mathrm{AU}}{r_V}\right)^{3/2}\approx 8.6\times 10^{-12}.
\]

\[
\frac{\hbar c}{365\ \mathrm{GeV}} = 5.4\times 10^{-4}\ \mathrm{fm}.
\]

---

End of patch notes.
