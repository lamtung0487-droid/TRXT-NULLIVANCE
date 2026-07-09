---
name: derive
description: Rigorous derivation protocol for TRXT-Nullivance theoretical work. Use when constructing or extending any theoretical result - a new mechanism, Lagrangian term, mass formula, or cosmological prediction. Enforces the axiomatic checklist (framework declaration, symmetries, dynamics, stability, observables, failure conditions) and produces a structured derivation note in theory/.
---

# Rigorous Derivation Protocol

English operationalization of `theory/protocols/workflow-v5-checklist.md`. A derivation that skips a section below is not a derivation; it is a sketch and must be labelled SKETCH.

## Step 0 — Declarations (before any equation)

State explicitly:
1. **Physical object**: particle / field / geometry / information / order parameter?
2. **Observables**: which measurable quantities this derivation ultimately predicts (cross sections, spectra, phase shifts, rotation velocities, power spectra) and which experiment measures them.
3. **Layer**: kinematical structure, dynamical law, or measurement/phenomenology.
4. **Failure conditions**: energy scale, density, curvature, temperature range where the derivation does NOT apply.

## Step 1 — Framework selection (choose exactly one, or state the gluing conditions)

- **(A) Classical mechanics**: configuration manifold Q, Lagrangian/Hamiltonian, symplectic form ω, Poisson bracket.
- **(B) Classical field theory**: fields φᵃ(x) on M, action S[φ], variation domain, boundary conditions, highest derivative order (Ostrogradsky check mandatory above 2nd order).
- **(C) Quantum mechanics**: Hilbert space, self-adjoint observables with domains (self-adjointness proven, not assumed from formal Hermiticity), unitary dynamics.
- **(D) QFT**: Minkowski or Euclidean (Wick rotation validity stated), particle content/spectrum, Fock space if applicable, microcausality.

## Step 2 — Minimal axiom list (finite, numbered)

1. Fundamental variables and their value domains
2. Symmetry group G and its action on the variables
3. Dynamical principle (action extremum / Schrödinger / Heisenberg)
4. Causality/propagation condition (hyperbolic PDE, microcausality — or an explicit statement of what replaces it and at what cost)
5. Energy definition and stability (Hamiltonian bounded below)
6. Coupling rule to sources/measurement (how correlators/cross sections arise)

## Step 3 — Derivation body

- Numbered equations; every step is a named operation (variation, integration by parts with boundary term stated, expansion in named small parameter to stated order, symmetry argument with the group element).
- No "it can be shown". Unclosed steps are marked **GAP-n** and listed at the end.
- Dimensional check after every displayed result.

## Step 4 — Consistency gates (all mandatory)

- [ ] Reduces to GR / Newton in the appropriate limit (show it)
- [ ] No ghosts, no gradient instability, c_s ≤ 1 in all environments (or explicit constraint mechanism)
- [ ] Consistent with `theory/specs/SYSTEM_OF_EQUATIONS.md` — contradictions flagged, not hidden
- [ ] Anti-Hardcode: every constant introduced is derived or declared as measured input with source

## Step 5 — Output artifact

Write `theory/derivation_<topic>_<YYYYMMDD>.md` containing sections 0–4, the GAP list, and a **Predictions** table (observable, predicted value/range, dataset that can test it). Then request the **mathematician** agent's audit; implementation is blocked until the audit verdict is SIGNED-OFF.
