"""
Numerical verification of the L0->L1 lift charge algebra: Q_Hopf = p*q.

Construction (standard rational-map ansatz): compactify R^3 -> S^3 via
  Z1 = sin(f) (x+iy)/r,   Z2 = cos(f) + i sin(f) z/r,   f = 2 arctan(r0/r),
then the (p,q) configuration is psi = (Z1^p, Z2^q) and
  n = ( 2 Re(u vbar), 2 Im(u vbar), |u|^2 - |v|^2 ) / (|u|^2 + |v|^2),
u = Z1^p, v = Z2^q. Claim: Hopf invariant Q_H = p*q.

Q_H is computed by the Whitehead integral: with F_ij = n.(d_i n x d_j n),
B = (F_23, F_31, F_12), solve curl A = B (Coulomb gauge, FFT), then
  Q_H = (1/(8 pi^2)) * integral A.B d^3x.
The (1,1) case (known Q_H = 1) calibrates the discretization.

Run from repo root: python experiments/layer0/hopf_lift_charge_algebra.py
"""
import numpy as np

L = 96                # grid points per axis
HALF = 12.0           # box half-size
R0 = 3.0              # hopfion scale


def build_field(p, q):
    x = np.linspace(-HALF, HALF, L, endpoint=False)
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
    r = np.sqrt(X**2 + Y**2 + Z**2) + 1e-12
    f = 2.0 * np.arctan(R0 / r)
    Z1 = np.sin(f) * (X + 1j * Y) / r
    Z2 = np.cos(f) + 1j * np.sin(f) * Z / r
    u = Z1**p
    v = Z2**q
    den = np.abs(u)**2 + np.abs(v)**2 + 1e-300
    uv = u * np.conj(v)
    n = np.stack([2 * uv.real / den, 2 * uv.imag / den,
                  (np.abs(u)**2 - np.abs(v)**2) / den], axis=-1)
    return n, x[1] - x[0]


def hopf_charge(n, h):
    def d(a, ax):
        return (np.roll(a, -1, axis=ax) - np.roll(a, 1, axis=ax)) / (2 * h)
    dn = [d(n, ax) for ax in range(3)]
    F = {}
    for i in range(3):
        for j in range(i + 1, 3):
            F[(i, j)] = np.sum(n * np.cross(dn[i], dn[j]), axis=-1)
    B = np.stack([F[(1, 2)], -F[(0, 2)], F[(0, 1)]], axis=-1)  # B_k = eps_kij F_ij /2 *2

    # Solve curl A = B in Coulomb gauge via FFT
    k = 2 * np.pi * np.fft.fftfreq(L, d=h)
    KX, KY, KZ = np.meshgrid(k, k, k, indexing="ij")
    K2 = KX**2 + KY**2 + KZ**2
    K2[0, 0, 0] = 1.0
    Bh = [np.fft.fftn(B[..., c]) for c in range(3)]
    # A = i k x B / |k|^2
    Ah = [1j * (KY * Bh[2] - KZ * Bh[1]) / K2,
          1j * (KZ * Bh[0] - KX * Bh[2]) / K2,
          1j * (KX * Bh[1] - KY * Bh[0]) / K2]
    A = np.stack([np.real(np.fft.ifftn(c)) for c in Ah], axis=-1)

    return np.sum(A * B) * h**3 / (8 * np.pi**2)


def main():
    print("=== L0->L1 lift: charge algebra Q_Hopf(p,q) = p*q ===")
    print(f"    grid {L}^3, box +/-{HALF}, r0={R0}")
    cal = None
    for (p, q) in ((1, 1), (2, 1), (1, 2), (2, 2), (3, 1), (3, 2)):
        n, h = build_field(p, q)
        Q = hopf_charge(n, h)
        if cal is None:
            cal = Q / 1.0          # calibrate on known Q_H(1,1) = 1
            print(f"  (1,1): raw Q_H = {Q:+.4f}  -> calibration factor {cal:+.4f}")
            continue
        print(f"  ({p},{q}): Q_H = {Q/cal:+.4f}   (predicted {p*q})")


if __name__ == "__main__":
    main()
