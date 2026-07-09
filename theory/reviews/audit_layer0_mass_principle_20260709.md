# Mathematical Audit — Derivation Note "The Layer-0 Root Principle of Mass"

Auditor: lab mathematician role · Date: 2026-07-09
Object: `theory/derivation_layer0_mass_principle_20260709.md`

## Item-by-item verdicts

| Claim | Verdict | Check |
|---|---|---|
| Eq. (1) Bogomolny rearrangement; E ≥ 4πK\|Q\|; equality ⟺ ∂̄w = 0 | **SOUND** | Belavin–Polyakov 1975; the square completes identically; stereographic reduction to Cauchy–Riemann standard |
| Additivity ⟹ no cascade; pair cost 8πKk | **SOUND (classical)** | Triangle inequality on \|Q\|. Caveat added: saturation makes decays *marginal* at classical level; quantum corrections decide binding sign — for O(3) the exact S-matrix has no bound states, so no quantum instability either |
| Eq. (2) bubbling/energy-quantization of harmonic-map heat flow into S² | **SOUND (theorem class)** | Struwe 1985 (finite-time singularities), energy identity/quantization: Qing 1995, Ding–Tian 1995, Topping. Energy concentrates in bubbles of exactly 4πK·deg |
| Identification I[n̂] = M_total/(4πK) | **SOUND** | Follows from (1)+(2) when smooth energy has drained; matches Test B trend |
| Test A: Q=2 ratio 0.988 (slightly *below* the bound) | SOUND with note | Lattice discretization deficit O((a/ρ)²) permits sub-continuum energies; not a violation of (1), which is a continuum statement |
| Test B: monotone descent 1.536 → 1.091 with integer Q_net | **SOUND** | Reproduced from the log; the integer sequence −15 → −7 → −3 → −1 under annihilation is exactly topological conservation |
| Eq. (3) m/Λ_MS̄ = 8/e | **SOUND** | Hasenfratz–Niedermayer 1990, exact |
| Eq. (5) G₂/SU(3) ≅ S⁶ | **SOUND** | dim 14−8 = 6; transitive G₂ action on unit imaginary octonions, stabilizer SU(3) — standard |
| **Eqs. (4), (6): sine-law bound states and m₂/m₁ = φ attributed to the O(7) *sigma model*** | **ERROR → corrected** | The Zamolodchikov² minimal S-matrix of the O(N) **sigma model** (N ≥ 3) has **no bound-state poles**: its spectrum is the single vector multiplet. The sine law m_k = m·sin(kπ/(N−2))/sin(π/(N−2)) belongs to the O(N) **Gross–Neveu model** (fermionic, four-fermion interaction — the 2D relative of NJL). For O(7) GN: k = 1,2 and m₂/m₁ = 2cos(π/5) = φ ✓ (arithmetic verified). **The φ prediction survives, but its home is the fermionic model — which in fact matches the framework better** (the L1 substrate IS an NJL four-fermion theory; L0's emergent fermions live in vortex cores per §3.1.3). Erratum applied to the note; prediction L0-P3 reworded as conditional on the fermionic O(7) GN realization of the coset sector |
| E₈/CoNb₂O₆ precedent for measured φ mass ratio | SOUND | Coldea et al., Science 327, 177 (2010) |

## Overall verdict: **SIGNED-OFF WITH ONE CORRECTION (applied)**

The core principle — M = 4πK·|Q|, quantization by bubbling, transmutation scale, symmetry-fixed ratios — is mathematically sound and, unusually for this programme, **verified numerically on the framework's own kernel the same day**. The φ ratio stands as a parameter-free prediction *of the fermionic (Gross–Neveu/NJL-type) realization* of the G₂/SU(3) coset — a stronger, not weaker, statement for a framework whose substrate is NJL. GAP-1 (the L0→L1 lift, linear-in-Q vs Q^{3/4}) is correctly identified as the single blocking question.

Implementation may proceed on L0-P1/L0-P2 (higher-resolution quantization runs, ΔE histogram); GAP-3 (assignments) remains blocked pending GAP-1.
