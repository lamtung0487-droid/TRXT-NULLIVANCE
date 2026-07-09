# Mathematical Audit — Derivation Note "Soliton Geometry and the Fate of the Static Energy"

Auditor: lab mathematician role · Date: 2026-07-09
Object: `theory/derivation_soliton_geometry_20260709.md`

| Claim | Verdict | Check |
|---|---|---|
| K.2 minimization: R\* = κp/√(2σ), E_s(R\*) = 2√2πκ√σ·p | **SOUND** | Recomputed symbolically (SymPy, this session); exact |
| T.1 gives R ∝ 1/p² ⟹ gap ∝ p², contradicting the 1/p law | **SOUND** | Direct: gap = ℏc_s/R_opt; T.1's own Eq. (161) |
| T.1's closing step is a non sequitur | **SOUND** | Text says "a more direct scaling argument… gives E = M\*(1/p+1/q)" with no derivation (report p. 105) |
| Vakulenko–Kapitanskii bound E ≥ C·Q^{3/4}, Q = pq for the Faddeev–Niemi class | **SOUND** | Classical theorem (Vakulenko & Kapitanskii 1979); applies because App. Q itself places the solitons in this class via helicity stabilization |
| I-11: WEP appendix uses total energy as inertial mass, contradicting gap-only spectrum | **SOUND — important** | Report p. 19: "the soliton mass m (the integral of the energy density)…". No reading of that sentence yields gap-only |
| Linear-version stability threshold A > M\*/8 = 45.7 GeV vs fidelity A ≤ 3.2 MeV | **SOUND** | Same minimization structure as the pq-version theorem (audited 2026-07-09); k\* = √(2M\*/A) verified |
| Decision fork F1/F2/F3 | SOUND as survey | F1's warning against integer-hunting is required by the lab's own null-test findings — retain verbatim in any manuscript |

**Verdict: SIGNED-OFF.** I-1 is resolved (T.1 excision recommended); I-2 is resolved negatively for the gap-only fiat, with I-11 as the new, independent internal contradiction. The E_core incompatibility is now established under all three static-energy scalings (p, pq, Q^{3/4}) — it is structural, not model-dependent.
