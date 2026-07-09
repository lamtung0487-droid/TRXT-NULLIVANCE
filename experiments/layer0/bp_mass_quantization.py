"""
Layer-0 test of the Bogomolny mass principle  M = 4*pi*K*|Q|.

The 2D O(3) sigma model (= the Nullivance Layer-0 substrate, report App. AL)
obeys the exact Belavin-Polyakov bound  E >= 4*pi*K*|Q|,  saturated by
(anti)holomorphic maps. If mass at Layer 0 is soliton energy, then mass is
quantized in exact units of 4*pi*K times the topological charge, and the
report's Incompleteness Functional I = integral |q| is (1/4piK) x total mass.

Test A (saturation): initialize exact Belavin-Polyakov profiles of degree
Q = 1, 2, 3 via stereographic w(z); measure E_lattice / (4*pi*Q) -> 1.

Test B (dynamical quantization): random smooth field, run the report's own
Nullivance heat-flow (neighbor average + tangent projection + renormalize),
track E(t) vs 4*pi*I(t) where I = sum |q_x| (Berg-Luscher density).
Prediction: after local relaxation, E ~= 4*pi*I (energy stored only in
topological lumps, in 4*pi quanta).

Run from repo root:  python experiments/layer0/bp_mass_quantization.py
"""
import numpy as np

rng = np.random.default_rng(20260709)


def lattice_energy(n):
    """E = sum over links (1 - n.n') ~= (K/2) int |grad n|^2 with K=1."""
    e = 0.0
    for ax in (0, 1):
        e += np.sum(1.0 - np.sum(n * np.roll(n, -1, axis=ax), axis=2))
    return e


def berg_luscher_density(n):
    """Signed spherical-triangle area per plaquette / 4pi (geometric charge)."""
    n1 = n
    n2 = np.roll(n, -1, axis=0)
    n3 = np.roll(np.roll(n, -1, axis=0), -1, axis=1)
    n4 = np.roll(n, -1, axis=1)

    def tri(a, b, c):
        num = np.sum(a * np.cross(b, c), axis=2)
        den = (1.0 + np.sum(a * b, axis=2) + np.sum(b * c, axis=2)
               + np.sum(c * a, axis=2))
        return 2.0 * np.arctan2(num, den)

    return (tri(n1, n2, n3) + tri(n1, n3, n4)) / (4.0 * np.pi)


def normalize(n):
    return n / np.linalg.norm(n, axis=2, keepdims=True)


def heat_flow_step(n, dt=0.2):
    """The report's Nullivance kernel: neighbor consensus, tangent projection."""
    nbr = (np.roll(n, 1, 0) + np.roll(n, -1, 0)
           + np.roll(n, 1, 1) + np.roll(n, -1, 1)) / 4.0
    force = nbr - n
    ndotf = np.sum(n * force, axis=2, keepdims=True)
    return normalize(n + dt * (force - ndotf * n))


def bp_field(L, zeros, rho):
    """Belavin-Polyakov profile from holomorphic w(z) = prod (z - z_i)/rho."""
    x = np.arange(L) - L / 2
    X, Y = np.meshgrid(x, x, indexing="ij")
    z = X + 1j * Y
    w = np.ones_like(z, dtype=complex)
    for z0 in zeros:
        w *= (z - z0) / rho
    # inverse stereographic projection: n = (2Re w, 2Im w, |w|^2-1)/(|w|^2+1)
    a2 = np.abs(w) ** 2
    n = np.stack([2 * w.real, 2 * w.imag, a2 - 1.0], axis=2) / (a2 + 1.0)[..., None]
    return normalize(n)


def test_A():
    print("=== TEST A: Belavin-Polyakov saturation  E / (4 pi |Q|) ===")
    L, rho = 192, 12.0
    for Q in (1, 2, 3):
        # spread zeros so lumps do not overlap
        zeros = [40j * (k - (Q - 1) / 2) for k in range(Q)]
        n = bp_field(L, zeros, rho)
        for _ in range(60):          # brief relaxation to shed lattice noise
            n = heat_flow_step(n)
        E = lattice_energy(n)
        Qbl = np.sum(berg_luscher_density(n))
        ratio = E / (4 * np.pi * abs(Qbl)) if abs(Qbl) > 0.1 else float("nan")
        print(f"  Q_target={Q}:  Q_BL={Qbl:+.3f}   E={E:8.3f}   "
              f"E/(4pi|Q|) = {ratio:.4f}")


def test_B():
    print("\n=== TEST B: dynamical quantization under the Nullivance flow ===")
    L = 128
    # smooth random field (correlated noise -> defects a few sites wide)
    raw = rng.normal(size=(L, L, 3))
    for _ in range(3):               # crude smoothing
        raw = (raw + np.roll(raw, 1, 0) + np.roll(raw, -1, 0)
               + np.roll(raw, 1, 1) + np.roll(raw, -1, 1)) / 5.0
    n = normalize(raw)
    print(f"  {'t':>6} {'E':>10} {'4pi*I':>10} {'E/(4pi*I)':>10} {'Q_net':>7}")
    for t in range(0, 2001):
        if t in (0, 50, 200, 500, 1000, 2000):
            q = berg_luscher_density(n)
            E = lattice_energy(n)
            I = np.sum(np.abs(q))
            r = E / (4 * np.pi * I) if I > 0.5 else float("nan")
            print(f"  {t:6d} {E:10.1f} {4*np.pi*I:10.1f} {r:10.3f} "
                  f"{np.sum(q):+7.2f}")
        n = heat_flow_step(n)
    print("  Prediction: E/(4pi*I) -> ~1 as smooth energy drains and only")
    print("  topological lumps (mass quanta) remain.")


if __name__ == "__main__":
    test_A()
    test_B()
