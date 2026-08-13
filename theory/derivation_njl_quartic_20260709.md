# Derivation Note — The S²-Sector Quartic from the NJL Determinant (GAP-L2) and the Mass Constant C (GAP-L1)

**Author:** lab theorist role · **Date:** 2026-07-09 · **Protocol:** `.claude/skills/derive/SKILL.md`
**Targets:** GAP-L2 (turn hypothesis H-c₄ into a theorem: derive the Skyrme-type stabilizer of the n̂-sector from the same one-loop NJL determinant that produced c₂, c₄) and GAP-L1 (the absolute mass constant C of M = C·(pq)^{3/4}).

> **Result:** the one-loop NJL determinant with hedgehog coupling produces **exactly the Faddeev–Niemi quartic with positive coefficient**
> **κ_S = N_f/(48π²)** (plus a positive symmetric quartic κ_X = N_f/(96π²)), and the stiffness **K = N_f M² ln(Λ²/M²)/(4π²)**. H-c₄ is now a theorem at this order. The lift constant follows as
> **C = c_FN·√(K·κ_S) = c_FN·√3·N_f·M·√(ln Λ²/M²)/(24π²)** — the entire mass chain is now analytic up to one literature constant (c_FN) and the stage's constituent gap M.

---

## Step 0 — Declarations

1. **Object:** the one-loop effective action for the S²-stage field n̂ obtained by integrating out the framework's constituent fermions.
2. **Observables:** the coefficients (K, κ_S, κ_X) of the static energy; through the lift note, the mass scale C per stage.
3. **Layer:** dynamical law.
4. **Failure conditions:** one-loop, leading order in the derivative expansion (slowly-varying n̂ on the scale 1/M); the ∂²E-commutator class of 4-derivative terms not computed (GAP-N2); coupling structure as declared in A2.

## Step 1 — Framework

**(D) QFT**, Euclidean (heat-kernel/proper-time; Wick rotation standard for the positive operator D†D); fermions integrated out exactly at one loop.

## Step 2 — Axioms

- **A1.** N_f species of 4-component fermions carrying an isospin doublet index.
- **A2 (coupling).** Euclidean Dirac operator **D = γ^μ∂_μ + M τ·n̂(x)** — the isoscalar "hedgehog" coupling of the condensate direction n̂ ∈ S² to the fermions, with constituent gap M (from the stage's gap equation / dimensional transmutation, established earlier). *Scope note: the framework's full NJL has (σ, π⃗) chiral structure (γ₅ coupling); the hedgehog form is its unitary-gauge restriction to the S² direction and the simplest self-adjoint-compatible choice. O(1) coefficient shifts under the γ₅ variant are expected but positivity of the Skyrme term is robust in the chiral-quark literature (F4-class flag).*
- **A3.** UV: proper-time cutoff s₀ = 1/Λ² (the framework's physical cutoff).
- **A4.** Effective action S_eff[n̂] = −ln det D = −½ Tr ln(D†D).

## Step 3 — Derivation body

### 3.1 The fluctuation operator (exact)

**(1)**  D†D = −∂² + M² + E,  **E = −M γ^μ (τ·∂_μn̂)**  — using (τ·n̂)² = 1; E is linear in gradients and in M. *Dim check:* [E] = mass² ✓ (one M, one ∂).

### 3.2 Proper-time expansion (odd traces vanish)

**(2)**  S_eff = ½∫₀^∞ (ds/s)(4πs)^{−2} e^{−sM²} ∫d⁴x tr[𝟙 − sE + (s²/2)E² − (s³/6)E³ + (s⁴/24)E⁴ + …]

tr E (one γ) = 0; tr E³ (three γ's) = 0. Commutator corrections carry additional derivatives per power of E (the (∂²n̂)² class) — deferred, GAP-N2.

### 3.3 Exact trace algebra (computed by machine, residual 3×10⁻²⁴; session log)

With X ≡ (∂_μn̂)·(∂^μn̂), Y ≡ (∂_μn̂·∂_νn̂)(∂^μn̂·∂^νn̂):

**(3)**  tr E² = 8M²·X   (4_spinor × 2_isospin),
**(4)**  tr E⁴ = M⁴·(24X² − 16Y) = M⁴·[8X² + **16(X² − Y)**].

**(5)** Identity (verified to machine precision for tangent configurations): X² − Y = |∂_μn̂ × ∂_νn̂|² = [n̂·(∂_μn̂×∂_νn̂)]² ≡ F_{μν}F^{μν} — **the quartic trace contains exactly the Faddeev–Niemi term.**

### 3.4 Proper-time integrals and assembled coefficients (exact)

∫ds s⁻¹e^{−sM²}|_{s₀=1/Λ²} = ln(Λ²/M²) + O(1);  ∫₀^∞ ds·s·e^{−sM²} = 1/M⁴. Assembling (2)–(4), per species and summing N_f:

**(6)**  L_eff ⊃ (K/2)(∂n̂)² + κ_S·F_{μν}F^{μν} + κ_X·X²,

**(7)**  **K = N_f M² ln(Λ²/M²)/(4π²)**,  **κ_S = N_f/(48π²)**,  **κ_X = N_f/(96π²)** — all positive; the M⁴ from the trace cancels the 1/M⁴ of the integral, so the quartics are **finite and cutoff-independent** (scheme-robust), while K carries the expected logarithm.

*Dim check (4D):* [K] = mass², quartics dimensionless ✓. **H-c₄ is now a theorem at one loop: the stabilizer demanded by Derrick exists, is the Faddeev–Niemi term, and its coefficient is fixed — no freedom.** Equivalently, the FN coupling is **e² = 12π²/N_f**.

### 3.5 The mass constant (GAP-L1, reduced to one literature number)

Derrick balance (lift note Eq. 2) gives E_min = 2√(E₂E₄); for the FN functional the charge-optimal minimizers obey E(Q) = c_FN·√(K·κ_S)·Q^{3/4} with c_FN a pure number from FN numerics (Battye–Sutcliffe; F4-class flag). Hence

**(8)**  **M(p,q) = C·(pq)^{3/4},  C = c_FN·(√3/24π²)·N_f·M·√(ln Λ²/M²).**

The chain is closed analytically: **Λ (transmutation) → M (gap) → (K, κ_S) (Eq. 7, exact) → C (Eq. 8) → spectrum.** Per stage (CP², S²) with its own M: two constants, both computable, zero fitted numbers.

### 3.6 Bonus consistency check

The positive κ_X (symmetric quartic) contributes to the phase-sector P(X)-type structure with the correct sign — consistent with the c₄ > 0 the report derived in App. C by a different route. Two independent computations of the same loop now agree in sign.

## Step 4 — Consistency gates

- [x] Stability: κ_S, κ_X > 0 — static energy bounded below; Derrick stabilization operative.
- [x] No Ostrogradsky at this order (first-derivative quartics); the deferred (∂²n̂)² class is the standard gradient-expansion remainder (GAP-N2).
- [x] Anti-Hardcode: every coefficient in (7)–(8) is derived; inputs are (N_f, M, Λ), all previously declared framework quantities.
- [x] Consistency with specs: agrees in sign with App. C; supersedes nothing; completes the lift note's A3.

## GAP list

| # | Item |
|---|---|
| GAP-N1 | γ₅ (chiral) coupling variant: recompute (7) for the full (σ,π⃗) structure; expect O(1) shifts, same signs |
| GAP-N2 | The (∂²n̂)² commutator class: compute or bound; reducible on-shell |
| GAP-N3 | c_FN from FN numerics — literature (F4-class, tooling) |
| GAP-N4 | Per-stage M values (CP² vs S² gap equations) → absolute spectra |

## Predictions table

| # | Observable | Prediction | Test |
|---|---|---|---|
| N-P1 | FN coupling of the substrate | e² = 12π²/N_f — parameter-free | Lattice measurement of the substrate's quartic response |
| N-P2 | Scheme robustness | κ_S, κ_X cutoff-independent (finite); only K runs | Recompute in dimensional regularization — must agree |
| N-P3 | Ratio κ_S/κ_X = 2 exactly | Fixed by the trace algebra (16 vs 8) | Any future two-coupling fit of the substrate must land on 2 |

Submitted to the **mathematician** for audit.
