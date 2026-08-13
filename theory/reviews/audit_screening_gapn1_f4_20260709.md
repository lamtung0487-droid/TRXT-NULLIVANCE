# Mathematical Audit — Screening Branch/DBI, GAP-N1 Closure, and F4 Literature Confirmation

Auditor: lab mathematician role · Date: 2026-08-13 (campaign continuation)
Objects: `theory/derivation_screening_branch_20260709.md`; GAP-N1 numerical closure (session log); F4 literature checks (WebSearch restored).

## 1. Screening-branch note (G0b)

| Claim | Verdict | Check |
|---|---|---|
| Theorem (1): sign(c_s²−1) = −sign(X·P_XX) ⟹ naive two-branch subluminality impossible for P_XX ≠ 0 | **SOUND** | One-line algebra from c_s² = P_X/K; recomputed |
| DBI: P_X = (1−2X̃)^{−1/2} > 0, K = (1−2X̃)^{−3/2} > 0 branch-wide; c_s² = 1−2X̃ | **SOUND** | Symbolic + numeric verification in session log; small-X expansion X + X²/2 matches c₂ = 1, c₄ = 1/(2Λ⁴) ✓ |
| Criterion refinement procedure | **COMPLIANT** | Ledger entry logged *before* rerun, theorem-backed — exactly what the frozen-criteria rule requires |
| I-12/GAP-S (screening sign bookkeeping) | **SOUND and important** | For X < 0, P_X decreases for both polynomial and DBI: P_X-enhancement k-mouflage cannot be the operative mechanism under the declared convention X = −(∂φ)²/2. Registered, not hidden. The v17-G4 gate is unaffected (different mechanism) — correctly stated |
| G4n criterion v2 (Cassini bound only where Cassini-class data exists) | **SOUND** | Measurement-provenance argument is correct; Neptune/Pluto deviations reclassified as pre-registered predictions (δg/g = 1.8×10⁻⁵, 3.2×10⁻⁵) — a *gain* in falsifiability, not a loosening. Exact current ephemeris bounds still to be cited (small F4 residual) |

## 2. GAP-N1 closure (chiral coupling variant)

Machine comparison (4 random tensor configurations, exact agreement): the chiral coupling D = γ∂ + iMγ₅τ·n̂ yields D†D = −∂² + M² + E₅ with E₅ = −iMγ^μγ₅(τ·∂_μn̂), and tr E₅² , tr E₅⁴ are **identical** to the hedgehog case — analytically because γ₅ factors cancel pairwise (γ^μγ₅γ^νγ₅ = −γ^μγ^ν) against (−i)². **Verdict: SOUND — K, κ_S, κ_X are unchanged under the chiral variant. GAP-N1 CLOSED (stronger than the expected "O(1) shifts": zero shift).**

## 3. F4 literature confirmation (tooling restored 2026-08-13)

- **VK bound:** E ≥ c·|Q|^{3/4} with rigorous constant c = (3/16)^{3/8}; ¾ power optimal; Ward's conjecture c = 1 open. Sources: [Topological energy bounds for the Skyrme and Faddeev models](https://arxiv.org/pdf/1311.2403); Vakulenko–Kapitanskii 1979 as cited therein. **CONFIRMED.**
- **FN minimizers track Q^{3/4}** with knotted/linked ground states at higher Q (Q = 4, 5 restructuring): [Hietarinta–Salo, PRD 62, 081701](https://journals.aps.org/prd/abstract/10.1103/PhysRevD.62.081701) and Battye–Sutcliffe as cited. **CONFIRMED** (L1-P3 supported).
- **GN sine spectrum:** [Karowski–Thun, complete O(2N) GN S-matrix](https://www.sciencedirect.com/science/article/abs/pii/0550321381904843); bound states in all antisymmetric representations with m_j ∝ sin(jπ/(N−2))/sin(π/(N−2)), Δ = 1/h∨ = 1/(N−2); odd-N spectra with kink sectors: [Kinks and bound states in the Gross–Neveu model, PRD 51, 4503](https://link.aps.org/doi/10.1103/PhysRevD.51.4503). For N = 7: two fusion levels, **m₂/m₁ = 2cos(π/5) = φ — CONFIRMED.**

## Consolidated verdicts

- Screening-branch note: **SIGNED-OFF** (GAP-S/I-12 carried as derivation task).
- GAP-N1: **CLOSED** (coefficients exactly invariant).
- Referee F4 on the Layer-0 principle: **SATISFIED** — the φ prediction and the ¾ law now carry proper citations. Per the referee's own addendum terms, the Layer-0 mass principle moves from MINOR REVISION to **ACCEPT** (residual: F2 exponent dt/L refinement, minor; GAP-N3 exact minimizer prefactor in declared units).
- Gate ladder: **LADDER CLEAR** (2026-08-13 report) with every pass earned or theorem-backed — first clean clear in the programme's history.
