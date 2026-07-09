#!/usr/bin/env python3
"""
verify_sidm_v12_5.py — Independent reproduction of V12.5 SIDM closure
- Solves Yukawa scattering via partial-wave Schrödinger (Numerov)
- Uses multipoint matching (0.90R, 0.95R, 1.00R) with pi-unwrapped averaging for δ_l
- Computes σ_T/mχ as function of v, and MB-averaged <σ_T/mχ>(v0)
Outputs:
  sidm_v12_5_full_curve_improved.csv
  sidm_v12_5_velocity_averaged.csv
  sidm_v12_5_hotspots_convergence.csv
  fig_v12_5_sigma_vs_v_multipoint.png
  fig_v12_5_velocity_averaged.png
  fig_v12_5_hotspot_stability.png
Dependencies: numpy, scipy, pandas, matplotlib
"""
import math, numpy as np, pandas as pd
import matplotlib.pyplot as plt
from scipy.special import spherical_jn, spherical_yn

GEV2_to_cm2 = 0.389379e-27
GEV_to_g = 1.78266192e-24
c_kms = 299792.458
SQRT_PI = math.sqrt(math.pi)

def to_cm2_per_g(sig_GeV2, mchi_GeV):
    return (sig_GeV2 * GEV2_to_cm2) / (mchi_GeV * GEV_to_g)

def yukawa_V(r, alpha, mphi):
    return -alpha * np.exp(-mphi * r) / r

def unwrap_pi(seq):
    out = [seq[0]]
    for x in seq[1:]:
        k = round((out[-1] - x) / math.pi)
        out.append(x + k*math.pi)
    return np.array(out)

def delta_from_u(uR, uRprime, ell, k, xR):
    j = spherical_jn(ell, xR)
    n = spherical_yn(ell, xR)
    jp = spherical_jn(ell, xR, derivative=True)
    np_ = spherical_yn(ell, xR, derivative=True)
    Nnum = j*(uRprime/k) - jp*uR
    Dden = n*(uRprime/k) - np_*uR
    return math.atan2(-Nnum, Dden)

def numerov_phase_shifts_multipoint(mchi, mphi, alpha, v_kms, *,
                                   Rmatch_factor=30.0, h=0.25, lmax_extra=25,
                                   points=(0.90,0.95,1.00)):
    v = v_kms / c_kms
    mu = mchi/2.0
    k = mu * v
    if k <= 0:
        raise ValueError("k<=0")

    Rmatch = Rmatch_factor / mphi

    # step: resolve oscillations, but keep runtime reasonable
    h_eff = min(h, math.pi/(10*k))
    h_eff = max(h_eff, 0.2)

    r = np.arange(h_eff, Rmatch + h_eff, h_eff)
    N = len(r)
    V = yukawa_V(r, alpha, mphi)

    lmax = int(max(10, k*Rmatch + lmax_extra))
    delta_mean = np.zeros(lmax+1)
    delta_std = np.zeros(lmax+1)

    idxs = [min(N-1, max(2, int(p*(N-1)))) for p in points]
    idxs = sorted(list(dict.fromkeys(idxs)))
    r_pts = [float(r[i]) for i in idxs]

    for ell in range(lmax+1):
        Q = (k**2) - (ell*(ell+1))/(r**2) - 2*mu*V
        u = np.zeros(N)
        u[0] = r[0]**(ell+1)
        u[1] = r[1]**(ell+1)
        h2 = h_eff*h_eff
        for n in range(1, N-1):
            k0 = 1 + h2*Q[n+1]/12.0
            k1 = 2*(1 - 5*h2*Q[n]/12.0)
            k2 = 1 + h2*Q[n-1]/12.0
            u[n+1] = (k1*u[n] - k2*u[n-1]) / k0

        deltas=[]
        for i, rp in zip(idxs, r_pts):
            uR = u[i]
            uRprime = (u[i] - u[i-1]) / h_eff
            xR = k * rp
            deltas.append(delta_from_u(uR, uRprime, ell, k, xR))

        deltas_u = unwrap_pi(deltas)
        delta_mean[ell] = float(np.mean(deltas_u))
        delta_std[ell]  = float(np.std(deltas_u))

    meta = dict(mu=mu, k=k, Rmatch=Rmatch, h=h_eff, lmax=lmax, r_pts=r_pts)
    return delta_mean, delta_std, meta

def sigma_T_from_deltas(delta, k):
    s=0.0
    for ell in range(len(delta)-1):
        s += (ell+1) * (math.sin(delta[ell+1]-delta[ell])**2)
    return (4*math.pi/(k*k))*s

def sigma_T_classical_fit(mchi, mphi, alpha, v_kms):
    v = v_kms / c_kms
    beta = (2*alpha*mphi)/(mchi*(v**2))
    if beta < 0.1:
        sig = (4*math.pi/(mphi**2))*(beta**2)*math.log(1+1/beta)
    elif beta <= 1e3:
        sig = (8*math.pi/(mphi**2))*(beta**2)/(1+1.5*(beta**1.65))
    else:
        lb=math.log(beta)
        sig = (math.pi/(mphi**2))*((lb+1-1/(2*lb))**2)
    return sig, float(beta)

def f_MB(v, v0):
    return (4.0/SQRT_PI) * (v**2 / (v0**3)) * np.exp(-(v**2)/(v0**2))

def velocity_average(v_grid, sigma_grid, v0, vmax_cap=6000.0):
    vmax = min(vmax_cap, 6*v0)
    vv = np.linspace(0, vmax, 900)[1:]
    sig = np.interp(vv, v_grid, sigma_grid, left=sigma_grid[0], right=sigma_grid[-1])
    w = f_MB(vv, v0)
    Z = np.trapz(w, vv)
    return float(np.trapz(w*sig, vv) / Z)

def main():
    # Default benchmark used in V11–V12.5
    mchi=10.0
    mphi=0.03  # 30 MeV
    alpha=0.01

    v_grid = np.logspace(math.log10(5), math.log10(3000), 60)
    rec=[]
    for v in v_grid:
        delta, delta_std, meta = numerov_phase_shifts_multipoint(
            mchi, mphi, alpha, float(v),
            Rmatch_factor=30.0, h=0.25, lmax_extra=25,
            points=(0.90,0.95,1.00)
        )
        sig_num = sigma_T_from_deltas(delta, meta["k"])
        sig_fit, beta = sigma_T_classical_fit(mchi, mphi, alpha, float(v))
        lcut=min(50, len(delta_std))
        rec.append(dict(
            v_kms=float(v),
            beta=beta,
            sigmaT_over_m_num_cm2g=to_cm2_per_g(sig_num, mchi),
            sigmaT_over_m_fit_cm2g=to_cm2_per_g(sig_fit, mchi),
            ratio_num_fit=to_cm2_per_g(sig_num, mchi)/to_cm2_per_g(sig_fit, mchi),
            lmax=int(meta["lmax"]),
            h_GeVinv=float(meta["h"]),
            Rmatch_GeVinv=float(meta["Rmatch"]),
            delta_std_mean_lowL=float(np.mean(delta_std[:lcut])),
            delta_std_max_lowL=float(np.max(delta_std[:lcut])),
            match_r_pts_GeVinv=",".join([f"{x:.1f}" for x in meta["r_pts"]]),
        ))
    df=pd.DataFrame(rec)
    df.to_csv("sidm_v12_5_full_curve_improved.csv", index=False)

    # Hotspots: recompute at stronger numerical settings
    hot = df.sort_values("delta_std_max_lowL", ascending=False).head(6)
    hot_rows=[]
    for _, row in hot.iterrows():
        v=float(row["v_kms"])
        sig_base=float(row["sigmaT_over_m_num_cm2g"])
        delta2, delta2_std, meta2 = numerov_phase_shifts_multipoint(
            mchi, mphi, alpha, v,
            Rmatch_factor=60.0, h=0.2, lmax_extra=55,
            points=(0.85,0.92,1.00)
        )
        sig2 = sigma_T_from_deltas(delta2, meta2["k"])
        sig2_cm2g = to_cm2_per_g(sig2, mchi)
        lcut2=min(50, len(delta2_std))
        hot_rows.append(dict(
            v_kms=v,
            sigma_base_cm2g=sig_base,
            sigma_strong_cm2g=sig2_cm2g,
            rel_diff=(sig2_cm2g-sig_base)/sig2_cm2g if sig2_cm2g!=0 else float("nan"),
            std_max_lowL_base=float(row["delta_std_max_lowL"]),
            std_max_lowL_strong=float(np.max(delta2_std[:lcut2])),
            lmax_strong=int(meta2["lmax"]),
            h_strong=float(meta2["h"]),
            Rmatch_strong=float(meta2["Rmatch"]),
        ))
    pd.DataFrame(hot_rows).to_csv("sidm_v12_5_hotspots_convergence.csv", index=False)

    # Velocity averaging
    v0_grid = np.logspace(math.log10(10), math.log10(3000), 40)
    sigma_num = df["sigmaT_over_m_num_cm2g"].values
    sigma_fit = df["sigmaT_over_m_fit_cm2g"].values
    avg_num=np.array([velocity_average(df["v_kms"].values, sigma_num, float(v0)) for v0 in v0_grid])
    avg_fit=np.array([velocity_average(df["v_kms"].values, sigma_fit, float(v0)) for v0 in v0_grid])
    pd.DataFrame(dict(
        v0_kms=v0_grid,
        avg_sigma_num_cm2g=avg_num,
        avg_sigma_fit_cm2g=avg_fit,
        ratio_avg_num_fit=avg_num/avg_fit
    )).to_csv("sidm_v12_5_velocity_averaged.csv", index=False)

    # Figures
    plt.figure(figsize=(9.2,6.6))
    plt.loglog(df["v_kms"], df["sigmaT_over_m_num_cm2g"], marker="o", markersize=3, linestyle="-", label="Numerical (multipoint)")
    plt.loglog(df["v_kms"], df["sigmaT_over_m_fit_cm2g"], linestyle="--", label="Classical fit")
    for y in [0.1,1,10]: plt.axhline(y, linestyle=":", linewidth=1)
    for x in [10,30,200,1000,3000]: plt.axvline(x, linestyle=":", linewidth=1)
    plt.xlabel("v (km/s)"); plt.ylabel(r"$\sigma_T/m_\chi$ (cm$^2$/g)")
    plt.title("V12.5 SIDM: σ_T/mχ vs v (numerical multipoint)")
    plt.grid(True, which="both", ls=":", alpha=0.35)
    plt.legend(); plt.tight_layout()
    plt.savefig("fig_v12_5_sigma_vs_v_multipoint.png", dpi=220); plt.close()

    plt.figure(figsize=(9.2,6.5))
    plt.loglog(v0_grid, avg_num, marker="o", markersize=3, linestyle="-", label="⟨σ⟩ Numerical (MB avg)")
    plt.loglog(v0_grid, avg_fit, linestyle="--", label="⟨σ⟩ Fit (MB avg)")
    for y in [0.1,1,10]: plt.axhline(y, linestyle=":", linewidth=1)
    for x in [20,200,1000,3000]: plt.axvline(x, linestyle=":", linewidth=1)
    plt.xlabel("v0 (km/s)"); plt.ylabel(r"$\langle\sigma_T/m_\chi\rangle$ (cm$^2$/g)")
    plt.title("V12.5 SIDM: velocity-averaged cross section")
    plt.grid(True, which="both", ls=":", alpha=0.35)
    plt.legend(); plt.tight_layout()
    plt.savefig("fig_v12_5_velocity_averaged.png", dpi=220); plt.close()

    hotdf = pd.DataFrame(hot_rows)
    plt.figure(figsize=(9.0,6.2))
    plt.semilogx(hotdf["v_kms"], np.abs(hotdf["rel_diff"]), marker="o", linestyle="None")
    plt.axhline(0.02, linestyle="--", linewidth=1)
    plt.xlabel("v (km/s)"); plt.ylabel("|(strong-base)/strong|")
    plt.title("V12.5 Diagnostic: hotspot stability")
    plt.grid(True, which="both", ls=":", alpha=0.35)
    plt.tight_layout()
    plt.savefig("fig_v12_5_hotspot_stability.png", dpi=220); plt.close()

if __name__ == "__main__":
    main()
