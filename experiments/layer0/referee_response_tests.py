"""
Referee-response tests for the Layer-0 mass principle (referee report F2, F3).
Final methodology (v3) — reproduces results/logs/referee_response_tests_20260709.log.

F3 (Q=1 Bogomolny saturation, done right): the torus seam invalidated the
original Q=1 test. Correct protocol: disk geometry, boundary frozen to the
BP tail values (not the north pole), and energy measured over disk-interior
links only. Result: E/(4pi|Q|) = 0.995-0.999, matching the analytic disk
fraction 1/(1+(rho/R_d)^2). Q=1 saturation CONFIRMED.

F2 (charge-violation rate): the discrete kernel lets lumps shrink and fall
through the lattice. Protocol: seam-free Q=2 profile of core size rho; record
first time t_c at which |Q_BL| < 1.5. Result (L=128, dt=0.2):
    rho:  5    6    8    10     12
    t_c:  10   30   310  2960   15465
Super-power-law growth (effective local exponent ~6-10, quasi-exponential
ln t_c ~ 1.1*rho over the mid range): topological protection on the lattice
is approximate but its violation is very strongly suppressed with defect
size in lattice units. This is the GAP-5 protection-time law.

Run from repo root: python experiments/layer0/referee_response_tests.py
"""
import numpy as np
import sys, os

sys.path.insert(0, os.path.dirname(__file__))
from bp_mass_quantization import (berg_luscher_density, heat_flow_step,
                                  bp_field)


def disk_energy(n, inside):
    """Energy of links whose both endpoints lie inside the disk."""
    E = 0.0
    for ax in (0, 1):
        link = inside & np.roll(inside, -1, axis=ax)
        E += np.sum((1.0 - np.sum(n * np.roll(n, -1, axis=ax), axis=2))[link])
    return E


def test_F3_disk():
    print("=== F3 (v3): Q=1 saturation, disk-interior energy, BP-tail BC ===")
    L = 160
    x = np.arange(L) - L / 2
    X, Y = np.meshgrid(x, x, indexing="ij")
    Rg = np.sqrt(X**2 + Y**2)
    for rho, Rd in ((6.0, 70.0), (8.0, 70.0), (12.0, 70.0)):
        inside = Rg < Rd
        n0 = bp_field(L, [0j], rho)
        n = n0.copy()
        for _ in range(300):
            n = heat_flow_step(n)
            n[~inside] = n0[~inside]          # freeze exterior to BP tail
        q = berg_luscher_density(n)
        Qin = np.sum(q * inside)
        E = disk_energy(n, inside)
        pred = 1.0 / (1.0 + (rho / Rd) ** 2)
        print(f"  rho={rho:5.1f}: Q_in={Qin:+.3f}   "
              f"E_disk/(4pi|Q_in|) = {E/(4*np.pi*abs(Qin)):.4f}   "
              f"(analytic disk fraction {pred:.4f})")


def test_F2_violation_rate():
    print("\n=== F2: lattice charge-violation time t_c(rho), Q=2 seam-free ===")
    L = 128
    results = []
    for rho, cap in ((5.0, 2000), (6.0, 2000), (8.0, 4000),
                     (10.0, 12000), (12.0, 30000)):
        n = bp_field(L, [15j, -15j], rho)
        for _ in range(20):
            n = heat_flow_step(n)
        t_c = None
        for t in range(cap):
            n = heat_flow_step(n)
            if t % 5 == 0 and abs(np.sum(berg_luscher_density(n))) < 1.5:
                t_c = t
                break
        results.append((rho, t_c))
        print(f"  rho={rho:5.1f}: t_c = {t_c if t_c is not None else f'>{cap}'}")
    pts = [(r, t) for r, t in results if t]
    if len(pts) >= 3:
        lr = np.log([r for r, _ in pts]); lt = np.log([t for _, t in pts])
        alpha = np.polyfit(lr, lt, 1)[0]
        beta = np.polyfit([r for r, _ in pts], lt, 1)[0]
        print(f"  Global power-law slope: t_c ~ rho^{alpha:.1f}; "
              f"quasi-exponential fit ln t_c ~ {beta:.2f}*rho")
        print("  => protection is approximate but violation is very strongly")
        print("     suppressed with defect size in lattice units (GAP-5 law).")


if __name__ == "__main__":
    test_F3_disk()
    test_F2_violation_rate()
