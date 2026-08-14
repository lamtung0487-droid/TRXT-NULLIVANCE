# Derivation Note — Substrate Resolution: One Breaking Chain, Two Stages (Referee F1)

**Author:** lab theorist role · **Date:** 2026-07-09 · **Protocol:** `theory/protocols/workflow-v5-checklist.md`
**Target:** referee finding F1 (`referee_report_layer0_mass_20260709.md`): the numerical evidence for the mass principle lives on S² (report App. AL) while the golden-ratio spectrum lives on S⁶ = G₂/SU(3) (report p. 181) — "different theories" until unified.

> **Result:** the two targets are not rival substrates but **sequential stages of the single G₂ symmetry-breaking chain the framework already declares**, distinguished by an exact homotopy criterion: **matter (π₂ ≠ 0) can exist at a stage iff the unbroken group at that stage contains a U(1) factor.** The S⁶ stage is matterless by theorem (condensation/scale physics only); the S² stage is the matter substrate — exactly the division of labor the two bodies of evidence already exhibit.

---

## Step 0 — Declarations

1. **Object:** the vacuum-manifold (Goldstone-coset) sequence of the G₂ breaking chain and its second homotopy groups.
2. **Observables:** which stages can host topologically protected lumps; where the mass-quantization evidence and the bound-state (φ) spectrum respectively live.
3. **Layer:** kinematical structure.
4. **Failure conditions:** the theorem is exact for the stated cosets; the *physical ordering* of the chain (which breaking happens at which scale) is the framework's hypothesis H-chain, inherited from the report (§5, p. 181), not proven here.

## Step 1 — Framework

Kinematics of coset spaces (homotopy theory); no dynamics introduced.

## Step 2 — Axioms

- **A1.** The internal symmetry chain declared by the report: G₂ → SU(3) → SU(2)×U(1) → U(1) (§5.2, App. O; condensation coset G₂/SU(3) at p. 181).
- **A2.** At each stage, low-energy fields live on the Goldstone coset G/H of that breaking.
- **A3.** 2D lumps at a stage are classified by π₂(G/H).

## Step 3 — Derivation body

### 3.1 The master tool

For compact G with π₁(G) = 0 (G₂ and SU(2) are simply connected; π₂ of **any** compact Lie group vanishes — Cartan), the exact homotopy sequence of H → G → G/H gives

**(1)**  π₂(G/H) ≅ π₁(H).

*This is the same identity that classifies 't Hooft–Polyakov monopoles; here it classifies 2D lumps.*

### 3.2 The chain table (each line exact)

| Stage | Coset | π₁(H) | π₂(coset) | Can host matter? |
|---|---|---|---|---|
| G₂ → SU(3) | **S⁶** = G₂/SU(3) | π₁(SU(3)) = 0 | **0** | **No — theorem** |
| SU(3) → SU(2)×U(1) | **CP²** = SU(3)/U(2) | π₁(U(2)) = ℤ | **ℤ** | Yes (one charge) |
| SU(2) → U(1) | **S²** = SU(2)/U(1) | π₁(U(1)) = ℤ | **ℤ** | Yes (one charge) |

**(2)** Corollary (the beauty the PI asked for): **topological matter exists at a stage iff a U(1) survives there.** The winding that protects a lump *is* the winding of the unbroken U(1) — matter and electromagnetism-like charge are the same homotopy fact, the 2D shadow of the monopole identity (1).

### 3.3 Resolution of F1

- The **S⁶ stage cannot carry lumps** (π₂ = 0, line 1). Everything the framework does there — NLSM asymptotic freedom, M_cond ≈ M_GUT, the O(7) bound-state (φ) spectrum in the fermionic/GN realization — is **condensation and spectrum-of-excitations physics, not topological matter.** No mass-quantization evidence could ever have lived there, and none was claimed there.
- The **S² stage is the unique final lump-carrying coset** of the chain, and it is *exactly* the O(3) substrate the report simulates in App. AL and on which the Bogomolny evidence was obtained (E/(4πI) → 1; saturation tests).
- Therefore the two bodies of evidence were never about two rival Layer-0 theories; they are about **two stages of one declared chain**, each doing the only job homotopy permits it to do. The apparent ambiguity dissolved because the framework's own chain (A1) already contains both cosets in sequence.
- **Bonus structure (flagged, not asserted):** the intermediate CP² stage also carries lumps (π₂ = ℤ). The chain thus predicts **two species of topological charge** (CP²-stage and S²-stage) with a natural energy ordering (higher stage = heavier scale). Whether these map to two observed sectors (e.g. baryonic vs dark) is GAP-1 territory — recorded as hypothesis H-2species, *not* used anywhere.

### 3.4 What this does to GAP-1 (the L0→L1 bridge)

GAP-1 is now sharper and smaller: the bridge no longer has to choose a substrate — the chain fixes the sequence. What remains is the *dimensional lift* (2D lumps → 3+1D solitons: linear-in-Q vs Q^{3/4}) and the scale assignment of each stage. The bridge question is reduced from "which theory?" to "which lift?".

## Step 4 — Consistency gates

- [x] Anti-Hardcode: no constants introduced; (1) and the table are exact mathematics.
- [x] Consistency with specs: uses the report's own declared chain (§5.2, p. 181, App. O); contradicts nothing; explains the coexistence of App. AL (S²) and p. 181 (S⁶).
- [x] Stability/causality: untouched (kinematics only).
- [x] GR limit: untouched.

## GAP list

| # | Item |
|---|---|
| GAP-A | Physical scale assignment of the CP² and S² stages (which breaking happens where) — inherited hypothesis of the report's chain |
| GAP-B | The dimensional lift (2D → 3+1D energy–charge law) — the surviving core of GAP-1 |
| GAP-C | H-2species: do CP²-stage and S²-stage charges correspond to two observed matter sectors? (exploratory; pre-registered rules required before any assignment) |

## Predictions table

| # | Statement | Test |
|---|---|---|
| S-P1 | No topologically protected state originates at the S⁶ stage; any "particle" attributed to it must be a *bound state* (finite width above threshold), never an absolutely stable lump | Internal-consistency check on all future assignment tables |
| S-P2 | The chain admits exactly **two** lump species (CP², S²) — a third protected species would falsify the declared chain | Structural falsifier |
| S-P3 | Every protected lump carries a nonzero winding of a surviving U(1) — electrically(-like) neutral *and* topologically stable states are forbidden at coset level | Confronts the dark-sector story: a DT-like state must either carry hidden-U(1) winding or lose absolute stability |

Submitted to the **mathematician** for audit. Note S-P3's bite: it constrains the dark-matter narrative in a falsifiable way — precisely the kind of teeth the referee demanded.
