---
description: workflow_v3
---

# TRXT-Nullivance V3: Research Workflow
**Based on Master Protocol V2.0**

This workflow implements the "5 Gates of Doom" approach.

---

## 🛠️ Step 0: Theory Construction (The Lagrangian)
**Goal:** Define ONE single Action $S$ that contains Gravity, Scalar Field, and Matter couplings.
*   **File:** `TRXT_V3/theory/unified_lagrangian.md`
*   **Task:** Define $S = \int d^4x \sqrt{-g} [ R + K(\phi, X) + G_3(\phi, X)\Box\phi + \dots ]$
*   **Check:** Verify Vainshtein screening capability analytically.

## ☠️ Gate 1: The Bullet Proof (The Killer)
**Goal:** Prove Scalar Field can separate Lensing from Mass.
*   **Simulation:** `TRXT_V3/astro/bullet_cluster_sim.py`
    *   Input: 2 colliding galaxies (Gas + Stars).
    *   Solve: Global PDE for Scalar Field $\phi(r)$.
    *   Compute: Metric Potentials $\Phi, \Psi$.
    *   Output: Lensing Convergence Map $\kappa$ vs X-ray Map.
*   **Pass Condition:** Lensing peaks track "invisible" mass (if any) or modified gravity peaks offset from gas. If peaks track gas 100%, **FAIL**.

## 🏗️ Gate 2: Cosmology & Structure
**Goal:** Calculate Matter Power Spectrum $P(k)$.
*   **Simulation:** `TRXT_V3/cosmo/structure_growth.py` (Boltzmann Solver wrapper or approximation).
*   **Check:** $f\sigma_8$ consistency.
*   **Pass Condition:** No catastrophic suppression of structure at small scales.

## 🌀 Gate 3: Galactic Dynamics (PDE Level)
**Goal:** SPARC fit using Global Poisson Solver.
*   **Simulation:** `TRXT_V3/astro/sparc_pde_solver.py`
*   **method:** Relaxation method on grid. No algebraic shortcuts.
*   **Pass Condition:** Universal $\xi$ fits rotational curves via PDE solution.

## ☀️ Gate 4: Solar System
**Goal:** Validate Screening.
*   **Simulation:** `TRXT_V3/astro/solar_system_pde.py`
*   **Pass Condition:** $|\Phi_{scalar} / \Phi_{newton}| < 10^{-5}$.

## ⚛️ Gate 5: Quantum Emergence
**Goal:** Fermions from Bosons.
*   **Simulation:** `TRXT_V3/micro/topological_defects.py`
*   **Pass Condition:** Stable vortex/skyrmion with effective spin-1/2 statistics (optional high-level goal).

---

## 🚀 Execution Order
1.  **Define Lagrangian** (User + AI collaboration).
2.  **Build PDE Solver Core** (Reusable mesh-based solver).
3.  **Run Bullet Cluster**.
    *   If Fail $\to$ Project Over.
    *   If Pass $\to$ Proceed to G2.
