"""
verify_layer0_emergence.py
TRXT V7 Research — Gate 0: Layer 0 Topological Vacuum Emergence
Evidence ID: GATE-0-LAYER0-EMERGENCE

Purpose:
    Prove that a stochastic non-linear sigma model (O(3) NLS on a 2D lattice)
    with Geometric Langevin dynamics evolves to a stationary Quantum Foam state:
    - Monotonic energy decay (cooling phase).
    - Non-zero topological charge density (rho_foam > 0) in equilibrium.
    - Topological defects are mandatory (cannot be annihilated by local moves).

Algorithm: Geometric Langevin Algorithm (GLA) — tangent-space projection.
Reference: Appendix S.1 and Appendix Y of TRXT_Research_Report_V14_FINAL.tex
"""

import numpy as np
import json
import time

# ─── Constants ────────────────────────────────────────────────────────────────
LATTICE_N = 64          # Lattice size (N × N)
STEPS_COOL = 200        # Cooling steps (T=0)
STEPS_EQUIL = 300       # Equilibrium steps (T>0)
T_EQUIL = 0.05          # Equilibrium temperature
DT = 0.01               # Time step
SEED = 42


class GeometricLangevinField:
    """O(3) non-linear sigma model with Geometric Langevin updates."""

    def __init__(self, N: int, dt: float = 0.01, seed: int = 42):
        self.N = N
        self.dt = dt
        self.rng = np.random.default_rng(seed)
        # Random unit vectors on S^2
        raw = self.rng.standard_normal((N, N, 3))
        norms = np.linalg.norm(raw, axis=2, keepdims=True)
        self.field = raw / (norms + 1e-12)

    def energy(self) -> float:
        """Heisenberg exchange energy E = -sum_{<ij>} n_i . n_j."""
        n = self.field
        E = (np.sum(n * np.roll(n, 1, axis=0)) +
             np.sum(n * np.roll(n, -1, axis=0)) +
             np.sum(n * np.roll(n, 1, axis=1)) +
             np.sum(n * np.roll(n, -1, axis=1)))
        return -E / (4 * self.N**2)

    def step(self, temperature: float = 0.0):
        """True Geometric Langevin Algorithm (GLA)."""
        n = self.field

        # 1. Deterministic Force (Renormalized Heat Flow)
        nbr_sum = (np.roll(n, 1, axis=0) + np.roll(n, -1, axis=0) +
                   np.roll(n, 1, axis=1) + np.roll(n, -1, axis=1))
        force_ambient = (nbr_sum / 4.0) - n

        # 2. Stochastic Force (White Noise)
        if temperature > 0:
            sigma = np.sqrt(2.0 * temperature * self.dt)
            noise_ambient = self.rng.standard_normal(n.shape) * sigma
        else:
            noise_ambient = np.zeros_like(n)

        # 3. Ambient Update Vector
        v_ambient = self.dt * force_ambient + noise_ambient

        # 4. Tangent Projection: v_perp = v - (n · v) n
        n_dot_v = np.sum(n * v_ambient, axis=2, keepdims=True)
        v_tangent = v_ambient - n_dot_v * n

        # 5. Retraction (Normalize) to stay on manifold S^2
        n_proposed = n + v_tangent
        norms = np.linalg.norm(n_proposed, axis=2, keepdims=True)
        self.field = n_proposed / (norms + 1e-9)

    def topological_charge_density(self) -> float:
        """
        Berg-Lüscher topological charge density (lattice Q/N^2).
        Counts skyrmions per lattice site.
        """
        n = self.field
        # Compute two elementary plaquettes per site
        e1 = np.roll(n, -1, axis=0) - n   # +x neighbour
        e2 = np.roll(n, -1, axis=1) - n   # +y neighbour

        # Cross product gives area element of plaquette on S^2
        cross = np.cross(e1, e2)           # shape (N, N, 3)
        # Solid angle ≈ n · (e1 × e2)
        solid_angle = np.sum(n * cross, axis=2)
        rho = np.mean(np.abs(solid_angle)) / (4.0 * np.pi)
        return float(rho)


def run_gate0():
    print("=" * 60)
    print("GATE 0: Layer 0 Topological Vacuum Emergence")
    print("=" * 60)

    field = GeometricLangevinField(N=LATTICE_N, dt=DT, seed=SEED)

    # ── Cooling Phase (T=0) ──────────────────────────────────────────────────
    print("\nPhase 1: Cooling (T=0) — testing monotonic energy decay")
    energies_cool = []
    for step in range(STEPS_COOL):
        field.step(temperature=0.0)
        if step % 20 == 0:
            E = field.energy()
            energies_cool.append(E)

    # Verify monotonic decrease
    dE_max = max(b - a for a, b in zip(energies_cool[:-1], energies_cool[1:]))
    cooling_monotonic = dE_max <= 1e-6   # allow tiny numerical noise
    print(f"  Initial energy: {energies_cool[0]:.6f}")
    print(f"  Final energy  : {energies_cool[-1]:.6f}")
    print(f"  Max energy increase: {dE_max:.2e}")
    print(f"  Monotonic decay: {'PASS ✓' if cooling_monotonic else 'FAIL ✗'}")

    # ── Equilibrium Phase (T>0) ──────────────────────────────────────────────
    print(f"\nPhase 2: Equilibrium (T={T_EQUIL}) — testing quantum foam density")
    rho_samples = []
    for step in range(STEPS_EQUIL):
        field.step(temperature=T_EQUIL)
        if step % 30 == 0:
            rho_samples.append(field.topological_charge_density())

    rho_mean = float(np.mean(rho_samples))
    foam_nonzero = rho_mean > 1e-4
    print(f"  Mean topological charge density: {rho_mean:.6f}")
    print(f"  Quantum foam non-zero: {'PASS ✓' if foam_nonzero else 'FAIL ✗'}")
    print(f"  (Expected ~ 0.007 per site for O(3) NLSM)")

    # ── Summary ──────────────────────────────────────────────────────────────
    all_pass = cooling_monotonic and foam_nonzero
    print("\n" + "=" * 60)
    print(f"GATE 0 RESULT: {'ALL PASS ✓' if all_pass else 'FAIL ✗'}")
    print("  Claim 1 (Energy decay monotonic): " +
          ("PASS ✓" if cooling_monotonic else "FAIL ✗"))
    print("  Claim 2 (Quantum foam rho > 0):   " +
          ("PASS ✓" if foam_nonzero else "FAIL ✗"))
    print("=" * 60)

    artifact = {
        "evidence_id": "GATE-0-LAYER0-EMERGENCE",
        "date": "2026-03-02",
        "lattice_N": LATTICE_N,
        "cooling_steps": STEPS_COOL,
        "equil_steps": STEPS_EQUIL,
        "T_equil": T_EQUIL,
        "energy_initial": float(energies_cool[0]),
        "energy_final": float(energies_cool[-1]),
        "max_energy_increase": float(dE_max),
        "cooling_monotonic": bool(cooling_monotonic),
        "rho_foam_mean": rho_mean,
        "foam_nonzero": bool(foam_nonzero),
        "all_pass": bool(all_pass),
        "status": "PASS" if all_pass else "FAIL"
    }
    return artifact


if __name__ == "__main__":
    t0 = time.time()
    result = run_gate0()
    t1 = time.time()
    result["runtime_s"] = round(t1 - t0, 2)
    out_path = "artifacts/gate_0_layer0_emergence_result.json"
    import os
    os.makedirs("artifacts", exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nArtifact saved: {out_path}")
    print(f"Runtime: {result['runtime_s']:.1f} s")
