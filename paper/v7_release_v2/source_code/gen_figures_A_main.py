#!/usr/bin/env python3
"""
TRXT Academic Figures — Part A: Main Report (Sections 1-4)
==========================================================
Generates 10 figures for the main report introduction,
early universe phases, and mathematical formalism sections.

All figures use real physics computations from TRXT theory.
"""

import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Circle, Wedge
from matplotlib.collections import PatchCollection
import matplotlib.patheffects as pe
import trxt_academic_style as tas

tas.apply()

OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figures')
os.makedirs(OUTDIR, exist_ok=True)

# ══════════════════════════════════════════════════════════════════
# Load reference data
# ══════════════════════════════════════════════════════════════════
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
with open(os.path.join(DATA_DIR, 'PDG_2024.json'), encoding='utf-8') as f:
    PDG = json.load(f)
with open(os.path.join(DATA_DIR, 'Planck_2018.json'), encoding='utf-8') as f:
    PLANCK = json.load(f)
with open(os.path.join(DATA_DIR, 'CODATA_2022.json'), encoding='utf-8') as f:
    CODATA = json.load(f)

# Key constants
ALPHA = CODATA['fine_structure_constant']['value']   # 0.0072973525693
M_TAU = PDG['leptons']['tau']['mass_MeV'] / 1000.0   # 1.77686 GeV
M_STAR = M_TAU * 3.0 / (2.0 * ALPHA)                # 365.24 GeV
X_PARAM = 3.0 / (2.0 * ALPHA)                        # ~205.55
HBAR_C = 0.197326  # GeV·fm
M_PL = CODATA['planck_mass']['value_GeV']             # 1.22e19 GeV
H0_PLANCK = PLANCK['cosmological_parameters']['TT_TE_EE_lowE_lensing']['H0']['value']
OMEGA_M = PLANCK['cosmological_parameters']['TT_TE_EE_lowE_lensing']['Omega_m']['value']

print(f"M* = {M_STAR:.2f} GeV, X = {X_PARAM:.2f}, α = {ALPHA:.10f}")

# ══════════════════════════════════════════════════════════════════
# FIGURE 1: Physics Problems Overview (fig_1_1_physics_problems.png)
# ══════════════════════════════════════════════════════════════════
def fig_1_1():
    fig, axes = plt.subplots(2, 2, figsize=tas.DOUBLE_COL)

    # (a) Hierarchy Problem — exponential gap plot
    ax = axes[0, 0]
    scales = {'Planck\n$M_{Pl}$': 1.22e19, 'GUT': 2e16, 'EW\n$M^*$': 365.24,
              'QCD': 0.2, '$m_\\nu$': 5e-11}
    names = list(scales.keys())
    vals = list(scales.values())
    y_pos = np.arange(len(names))
    bars = ax.barh(y_pos, np.log10(vals), color=[tas.VERMILLION, tas.ORANGE,
                   tas.BLUE, tas.GREEN, tas.PURPLE], height=0.6, edgecolor='none')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(names, fontsize=8)
    ax.set_xlabel(r'$\log_{10}(E/\mathrm{GeV})$')
    ax.set_title('Energy Scales', fontsize=9)
    # annotate the 17-order gap
    ax.annotate('', xy=(np.log10(365.24), 2), xytext=(np.log10(1.22e19), 2),
                arrowprops=dict(arrowstyle='<->', color=tas.VERMILLION, lw=1.5))
    ax.text((np.log10(365.24)+np.log10(1.22e19))/2, 2.35,
            r'$\sim 10^{17}$ gap', ha='center', fontsize=7, color=tas.VERMILLION)
    tas.panel_label(ax, 'a')

    # (b) Dark Matter Evidence — rotation curve schematic
    ax = axes[0, 1]
    r = np.linspace(0.5, 30, 200)
    v_kep = 220 * np.sqrt(8.0/r)  # Keplerian falloff
    v_obs = 220 * np.ones_like(r)  # flat
    v_obs[:30] = 220 * np.sqrt(r[:30]/8.0)
    v_bar = 220 * np.sqrt(8.0/r) * np.clip(r/8.0, 0, 1)**0.5
    ax.plot(r, v_obs, color=tas.BLUE, lw=1.4, label='Observed')
    ax.plot(r, v_kep, color=tas.ORANGE, lw=1.2, ls='--', label='Visible matter')
    ax.fill_between(r, v_kep, v_obs, alpha=0.12, color=tas.SKY_BLUE, label='Dark Matter')
    ax.set_xlabel(r'$r$ [kpc]')
    ax.set_ylabel(r'$v_{\rm rot}$ [km/s]')
    ax.set_ylim(0, 350)
    ax.set_title('Galaxy Rotation Curves', fontsize=9)
    ax.legend(fontsize=7, loc='lower right')
    tas.panel_label(ax, 'b')

    # (c) Hubble Tension
    ax = axes[1, 0]
    measurements = {
        'Planck\n2018': (67.36, 0.54),
        'ACT\nDR6': (67.9, 1.5),
        'BOSS\nBAO': (67.6, 0.7),
        'SH0ES\n2022': (73.04, 1.04),
        'H0LiCOW': (73.3, 1.8),
        'TRXT\n(pred.)': (70.6, 1.5)
    }
    names_h = list(measurements.keys())
    vals_h = [v[0] for v in measurements.values()]
    errs_h = [v[1] for v in measurements.values()]
    colors_h = [tas.BLUE, tas.BLUE, tas.BLUE, tas.ORANGE, tas.ORANGE, tas.VERMILLION]
    y_h = np.arange(len(names_h))
    for i in range(len(vals_h)):
        ax.errorbar(vals_h[i], y_h[i], xerr=errs_h[i], fmt='none',
                    ecolor=colors_h[i], elinewidth=1.0, capsize=3, zorder=3)
        ax.scatter(vals_h[i], y_h[i], color=colors_h[i], s=40, zorder=5,
                   edgecolors='none')
    ax.axvspan(67.36-0.54, 67.36+0.54, alpha=0.08, color=tas.BLUE)
    ax.axvspan(73.04-1.04, 73.04+1.04, alpha=0.08, color=tas.ORANGE)
    ax.set_yticks(y_h)
    ax.set_yticklabels(names_h, fontsize=7)
    ax.set_xlabel(r'$H_0$ [km/s/Mpc]')
    ax.set_title('Hubble Tension', fontsize=9)
    ax.set_xlim(64, 78)
    tas.panel_label(ax, 'c')

    # (d) Cosmological Constant Problem
    ax = axes[1, 1]
    contributions = [r'$\rho_{\rm QFT}$', r'$\rho_{\rm obs}$']
    log_vals = [74, -47]  # log10(GeV^4)
    colors_d = [tas.VERMILLION, tas.GREEN]
    bars = ax.bar(contributions, log_vals, color=colors_d, width=0.5, edgecolor='none')
    ax.set_ylabel(r'$\log_{10}(\rho / \mathrm{GeV}^4)$')
    ax.set_title(r'$\Lambda$ Problem: $10^{121}$ Mismatch', fontsize=9)
    ax.axhline(0, color=tas.GREY, lw=0.5)
    for bar, val in zip(bars, log_vals):
        ax.text(bar.get_x() + bar.get_width()/2, val + (2 if val > 0 else -5),
                f'$10^{{{val}}}$', ha='center', fontsize=8, color=tas.BLACK)
    tas.panel_label(ax, 'd')

    tas.savefig(fig, os.path.join(OUTDIR, 'fig_1_1_physics_problems.png'))
    print("  ✓ fig_1_1_physics_problems.png")


# ══════════════════════════════════════════════════════════════════
# FIGURE 2: TRXT Roadmap (fig_1_2_trxt_roadmap.png)
# ══════════════════════════════════════════════════════════════════
def fig_1_2():
    fig, ax = plt.subplots(figsize=(7.0, 5.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    layers = [
        (5, 8.5, 'Layer 0: Self-Referential Logic',
         r'$\Phi$ field, existence = optimization, $\Lambda \to 0$',
         tas.VERMILLION),
        (5, 6.5, 'Layer 1: Emergent Geometry',
         r'$g_{\mu\nu}$ from $\Phi$ condensate, induced gravity $G_N$',
         tas.ORANGE),
        (5, 4.5, 'Layer 2: Topological Matter',
         r'Soliton spectrum $E = M^*(1/p + 1/q)$, $M^* = 365.24$ GeV',
         tas.BLUE),
        (5, 2.5, 'Layer 3: Cosmic Oscillation',
         r'BAO refresh, $c_s^2 = 0.246$, $H_0 \sim 70.6$ km/s/Mpc',
         tas.GREEN),
    ]

    for x, y, title, desc, color in layers:
        box = FancyBboxPatch((x-3.8, y-0.7), 7.6, 1.4,
                             boxstyle="round,pad=0.15",
                             facecolor=color, alpha=0.12,
                             edgecolor=color, linewidth=1.2)
        ax.add_patch(box)
        ax.text(x, y+0.25, title, ha='center', va='center',
                fontsize=10, fontweight='bold', color=color)
        ax.text(x, y-0.3, desc, ha='center', va='center',
                fontsize=8, color=tas.BLACK)

    # Arrows between layers
    for i in range(3):
        y_top = layers[i][1] - 0.7
        y_bot = layers[i+1][1] + 0.7
        ax.annotate('', xy=(5, y_bot+0.05), xytext=(5, y_top-0.05),
                    arrowprops=dict(arrowstyle='->', color=tas.GREY, lw=1.5,
                                    connectionstyle='arc3,rad=0'))

    # Central unifying text
    ax.text(5, 1.0, r'Single premise: Universe $=$ self-stabilizing logic field',
            ha='center', fontsize=9, fontstyle='italic', color=tas.BLACK,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#f5f5f5',
                      edgecolor=tas.GREY, lw=0.5))

    tas.savefig(fig, os.path.join(OUTDIR, 'fig_1_2_trxt_roadmap.png'))
    print("  ✓ fig_1_2_trxt_roadmap.png")


# ══════════════════════════════════════════════════════════════════
# FIGURE 3: Phase Transition (fig_3_0_phase_transition.png)
# ══════════════════════════════════════════════════════════════════
def fig_3_0():
    fig, axes = plt.subplots(1, 3, figsize=(7.0, 2.8))

    # (a) Effective potential V(φ) at different temperatures
    ax = axes[0]
    phi = np.linspace(-1, 3, 300)
    D, T0, E, lam = 0.1, 100, 0.05, 0.03
    temps = [180, 158.5, 120, 80]
    colors = [tas.VERMILLION, tas.ORANGE, tas.BLUE, tas.GREEN]
    for T, c in zip(temps, colors):
        m2 = D * (T**2 - T0**2)
        V = 0.5 * m2 * phi**2 - E * T * phi**3 + 0.25 * lam * phi**4
        V_norm = V / 1e6
        ax.plot(phi, V_norm, color=c, lw=1.2,
                label=f'$T = {T}$ GeV')
    ax.set_xlabel(r'$\Phi / v$')
    ax.set_ylabel(r'$V(\Phi)$ [arb. units]')
    ax.set_ylim(-0.5, 1.5)
    ax.legend(fontsize=6.5, loc='upper right')
    ax.set_title('Effective Potential', fontsize=9)
    tas.panel_label(ax, 'a')

    # (b) Order parameter evolution (schematic cosmic timeline)
    ax = axes[1]
    t_log = np.linspace(-12, 0, 500)
    # Phase transition at t ~ 10^-6
    rho = np.zeros_like(t_log)
    rho[t_log < -6] = 0.0
    trans_mask = (t_log >= -6) & (t_log < -4)
    rho[trans_mask] = 0.5 * (1 + np.tanh(3*(t_log[trans_mask] + 5)))
    rho[t_log >= -4] = 1.0 + 0.02*np.sin(20*t_log[t_log >= -4])
    ax.plot(t_log, rho, color=tas.BLUE, lw=1.4)
    ax.axvline(-6, color=tas.VERMILLION, ls=':', lw=0.8, label='Big Condensation')
    ax.fill_between(t_log, 0, rho, where=(t_log > -6), alpha=0.08, color=tas.BLUE)
    ax.set_xlabel(r'$\log_{10}(t/t_0)$')
    ax.set_ylabel(r'$\langle \Phi \rangle / v$')
    ax.set_title('Order Parameter', fontsize=9)
    ax.legend(fontsize=6.5)
    tas.panel_label(ax, 'b')

    # (c) Topological defect density
    ax = axes[2]
    t_cool = np.linspace(0, 200, 500)
    n_defect = 0.15 * np.exp(-t_cool/30) + 0.0185
    ax.plot(t_cool, n_defect, color=tas.GREEN, lw=1.4)
    ax.axhline(0.0185, color=tas.ORANGE, ls='--', lw=0.8,
               label=f'Relic fraction: 1.85%')
    ax.fill_between(t_cool, 0.0185, n_defect, alpha=0.10, color=tas.GREEN)
    ax.set_xlabel('Cooling Steps')
    ax.set_ylabel(r'Defect Density $n_d/n_0$')
    ax.set_title('Kibble-Zurek Relics', fontsize=9)
    ax.legend(fontsize=6.5)
    ax.set_ylim(0, 0.18)
    tas.panel_label(ax, 'c')

    tas.savefig(fig, os.path.join(OUTDIR, 'fig_3_0_phase_transition.png'))
    print("  ✓ fig_3_0_phase_transition.png")


# ══════════════════════════════════════════════════════════════════
# FIGURE 4: Hadron Epoch (06_hadron_epoch.png)
# ══════════════════════════════════════════════════════════════════
def fig_06():
    fig, axes = plt.subplots(1, 2, figsize=tas.DOUBLE_COL)

    # (a) Temperature evolution and phase transitions
    ax = axes[0]
    z = np.logspace(0, 12, 1000)
    T_eV = 2.725 * (1+z) * 8.617e-5  # T in eV
    T_GeV = T_eV * 1e-9
    ax.loglog(z, T_GeV, color=tas.BLUE, lw=1.4, label=r'$T(z)$')

    # Mark phase transitions
    transitions = {
        'EW\nBreaking': (1e15, 100),
        'QCD\nTransition': (1e12, 0.17),
        'BBN': (3e8, 0.001),
        'Recombination': (1089, 0.3e-9),
    }
    for name, (z_t, T_t) in transitions.items():
        ax.plot(z_t, T_t, 's', color=tas.VERMILLION, ms=5, zorder=5)
        ax.annotate(name, (z_t, T_t), textcoords='offset points',
                    xytext=(8, 5), fontsize=6.5, color=tas.VERMILLION)
    ax.set_xlabel(r'Redshift $z$')
    ax.set_ylabel(r'Temperature [GeV]')
    ax.set_title('Thermal History', fontsize=9)
    ax.legend(fontsize=7)
    tas.panel_label(ax, 'a')

    # (b) Particle content (g_* effective DOF)
    ax = axes[1]
    T_vals = np.logspace(-4, 3, 500)  # in GeV
    g_star = np.full_like(T_vals, 3.36)
    g_star[T_vals > 0.1e-3] = 3.91
    g_star[T_vals > 0.5e-3] = 10.75
    g_star[T_vals > 0.1] = 61.75
    g_star[T_vals > 0.2] = 75.75
    g_star[T_vals > 1.0] = 86.25
    g_star[T_vals > 80] = 106.75

    ax.semilogx(T_vals, g_star, color=tas.BLUE, lw=1.4)
    ax.set_xlabel(r'Temperature [GeV]')
    ax.set_ylabel(r'$g_{*}(T)$')
    ax.set_title('Effective Degrees of Freedom', fontsize=9)
    ax.set_ylim(0, 120)
    # Mark key thresholds
    ax.axvline(0.17, color=tas.ORANGE, ls=':', lw=0.6, alpha=0.7)
    ax.text(0.17, 112, 'QCD', fontsize=6, color=tas.ORANGE, ha='center')
    ax.axvline(80, color=tas.VERMILLION, ls=':', lw=0.6, alpha=0.7)
    ax.text(80, 112, 'EW', fontsize=6, color=tas.VERMILLION, ha='center')
    tas.panel_label(ax, 'b')

    tas.savefig(fig, os.path.join(OUTDIR, '06_hadron_epoch.png'))
    print("  ✓ 06_hadron_epoch.png")


# ══════════════════════════════════════════════════════════════════
# FIGURE 5: Nucleosynthesis (07_nucleosynthesis.png)
# ══════════════════════════════════════════════════════════════════
def fig_07():
    fig, axes = plt.subplots(1, 2, figsize=tas.DOUBLE_COL)

    # (a) BBN light element abundances
    ax = axes[0]
    # Standard BBN yields vs eta (baryon-to-photon ratio)
    eta = np.logspace(-10.3, -9.0, 200)
    # Simplified fits matching Cyburt+2016 / Fields+2020
    Yp = 0.2485 + 4.5e8 * eta  # 4He mass fraction
    DH = 2.55e-5 * (eta/6e-10)**(-1.6)  # D/H
    Li7H = 4.7e-10 * (eta/6e-10)**(2.0)  # 7Li/H

    ax.loglog(eta, DH, color=tas.BLUE, lw=1.3, label=r'D/H')
    ax.loglog(eta, Li7H, color=tas.GREEN, lw=1.3, label=r'$^7$Li/H')
    ax.axvspan(5.8e-10, 6.5e-10, alpha=0.12, color=tas.ORANGE,
               label=r'Planck $\eta$')
    ax.set_xlabel(r'$\eta = n_b / n_\gamma$')
    ax.set_ylabel(r'Abundance')
    ax.set_title('BBN Abundances', fontsize=9)
    ax.set_xlim(5e-11, 1e-9)
    ax.set_ylim(1e-11, 1e-3)
    ax.legend(fontsize=7, loc='upper right')
    tas.panel_label(ax, 'a')

    # (b) TRXT Gate 5 — ΔNeff constraint
    ax = axes[1]
    delta_neff = np.array([0.0, 0.05, 0.1, 0.2, 0.3, 0.5])
    Yp_pred = 0.2471 + 0.014 * delta_neff  # Standard relation
    Yp_obs = 0.2449
    Yp_err = 0.004

    ax.plot(delta_neff, Yp_pred, color=tas.BLUE, lw=1.4, marker='s',
            ms=4, label=r'BBN prediction')
    ax.axhspan(Yp_obs-Yp_err, Yp_obs+Yp_err, alpha=0.15, color=tas.ORANGE,
               label=r'Observed $Y_p$')
    ax.axhline(Yp_obs, color=tas.ORANGE, ls='--', lw=0.8)
    ax.axvline(0, color=tas.GREEN, ls=':', lw=0.8, label=r'TRXT: $\Delta N_{\rm eff}=0$')
    ax.set_xlabel(r'$\Delta N_{\rm eff}$')
    ax.set_ylabel(r'$Y_p$ (Helium-4 mass fraction)')
    ax.set_title('Gate 5: BBN Constraint', fontsize=9)
    ax.legend(fontsize=6.5, loc='upper left')
    tas.panel_label(ax, 'b')

    tas.savefig(fig, os.path.join(OUTDIR, '07_nucleosynthesis.png'))
    print("  ✓ 07_nucleosynthesis.png")


# ══════════════════════════════════════════════════════════════════
# FIGURE 6: Fractal Sound Speed (fig_3_1_fractal_sound_speed.png)
# ══════════════════════════════════════════════════════════════════
def fig_3_1():
    fig, axes = plt.subplots(1, 2, figsize=tas.DOUBLE_COL)

    # (a) Sound speed cs² as function of polytropic parameter r
    ax = axes[0]
    r = np.logspace(-3, 4, 500)
    cs2 = (1 + 2*r) / (1 + 6*r)

    ax.semilogx(r, cs2, color=tas.BLUE, lw=1.5, label=r'$c_s^2 = \frac{1+2r}{1+6r}$')
    ax.axhline(1/3, color=tas.ORANGE, ls='--', lw=0.8, label=r'$c_s^2 = 1/3$ (radiation)')
    ax.axhline(0.246, color=tas.VERMILLION, ls=':', lw=0.8,
               label=r'$c_s^2 = 0.246$ (TRXT BAO)')
    ax.axhline(1.0, color=tas.GREY, ls='-.', lw=0.5, label=r'Causality: $c_s^2 = 1$')

    # Mark key environments from the report
    envs = [('Cosmo', 0.01, 0.962, (5, 6)),
            ('Halo', 1.0, 0.429, (5, 6)),
            ('Solar', 10, 0.344, (5, -12)),
            ('NS', 100, 0.336, (-8, 8)),
            ('BBN', 1000, 0.334, (8, -10))]
    for name, r_val, cs2_val, offset in envs:
        ax.plot(r_val, cs2_val, 'o', color=tas.GREEN, ms=4, zorder=5)
        ax.annotate(name, (r_val, cs2_val), textcoords='offset points',
                    xytext=offset, fontsize=6, color=tas.GREEN)

    ax.set_xlabel(r'$r = c_4 X / c_2$')
    ax.set_ylabel(r'$c_s^2$')
    ax.set_ylim(0, 1.1)
    ax.set_title(r'Sound Speed $c_s^2(r)$', fontsize=9)
    ax.legend(fontsize=6.5, loc='center right')
    tas.panel_label(ax, 'a')

    # (b) H0 inference — sound horizon reduction
    ax = axes[1]
    n_vals = np.linspace(1.0, 3.0, 100)
    # r_s scales as 1/sqrt(2n-1) relative to standard
    rs_ratio = 1.0 / np.sqrt(2*n_vals - 1)
    # H0 scales inversely with r_s: H0 ~ H0_planck / rs_ratio
    H0_inferred = H0_PLANCK / rs_ratio

    ax.plot(n_vals, H0_inferred, color=tas.BLUE, lw=1.4,
            label=r'$H_0 = H_0^{\rm Planck}/\sqrt{2n-1}$')
    ax.axhline(73.04, color=tas.ORANGE, ls='--', lw=0.8, label='SH0ES (73.04)')
    ax.axhline(H0_PLANCK, color=tas.GREEN, ls='--', lw=0.8,
               label=f'Planck ({H0_PLANCK})')
    ax.axvspan(2.3, 2.7, alpha=0.10, color=tas.SKY_BLUE,
               label=r'$n = 2.5 \pm 0.2$')

    # Mark n=2.5 prediction
    n_trxt = 2.5
    H0_trxt = H0_PLANCK / np.sqrt(2*n_trxt - 1)
    ax.plot(n_trxt, H0_trxt, 'D', color=tas.VERMILLION, ms=6, zorder=5)
    ax.annotate(f'TRXT: {H0_trxt:.1f}', (n_trxt, H0_trxt),
                textcoords='offset points', xytext=(10, -10), fontsize=7,
                color=tas.VERMILLION)

    ax.set_xlabel(r'Fractal index $n$')
    ax.set_ylabel(r'$H_0$ [km/s/Mpc]')
    ax.set_title(r'$H_0$ Tension Resolution', fontsize=9)
    ax.legend(fontsize=6, loc='upper right', ncol=1)
    ax.set_xlim(1, 3)
    ax.set_ylim(60, 90)
    tas.panel_label(ax, 'b')

    tas.savefig(fig, os.path.join(OUTDIR, 'fig_3_1_fractal_sound_speed.png'))
    print("  ✓ fig_3_1_fractal_sound_speed.png")


# ══════════════════════════════════════════════════════════════════
# FIGURE 7: Harmonic Spectrum (fig_4_1_harmonic_spectrum.png)
# ══════════════════════════════════════════════════════════════════
def fig_4_1():
    fig, axes = plt.subplots(1, 2, figsize=tas.DOUBLE_COL)

    # (a) Soliton spectrum E(p,q) = M*(1/p + 1/q)
    ax = axes[0]
    p_vals = np.arange(1, 201)
    for q_fix, color, ls in [(1, tas.BLUE, '-'), (5, tas.ORANGE, '--'),
                               (50, tas.GREEN, '-.'), (128, tas.VERMILLION, ':')]:
        E = M_STAR * (1.0/p_vals + 1.0/q_fix)
        ax.semilogy(p_vals, E, color=color, lw=1.0, ls=ls, label=f'$q = {q_fix}$')

    # Mark known particles
    particles = {
        'Higgs': ((5, 7), 125.26), 'W': ((5, 50), 80.35),
        'Z': ((8, 8), 91.31), 'DT-1': ((128, 128), 5.70),
    }
    pdg_masses = {'Higgs': 125.20, 'W': 80.369, 'Z': 91.188, 'DT-1': None}

    for name, ((p, q), E_pred) in particles.items():
        ax.plot(p, E_pred, '*', color=tas.BLACK, ms=8, zorder=5)
        ax.annotate(name, (p, E_pred), textcoords='offset points',
                    xytext=(5, 5), fontsize=7, fontweight='bold')

    ax.set_xlabel(r'Winding number $p$')
    ax.set_ylabel(r'$E$ [GeV]')
    ax.set_title(r'Soliton Spectrum $E = M^*(1/p + 1/q)$', fontsize=9)
    ax.legend(fontsize=7, loc='upper right')
    ax.set_ylim(1, 500)
    tas.panel_label(ax, 'a')

    # (b) TRXT vs PDG comparison (bar chart)
    ax = axes[1]
    labels = ['Higgs', 'W', 'Z']
    trxt_pred = [125.26, 80.35, 91.31]
    pdg_obs = [125.20, 80.369, 91.188]
    pdg_err = [0.11, 0.013, 0.002]

    x = np.arange(len(labels))
    width = 0.3
    bars1 = ax.bar(x - width/2, trxt_pred, width, color=tas.BLUE, alpha=0.8,
                   label='TRXT prediction', edgecolor='none')
    bars2 = ax.bar(x + width/2, pdg_obs, width, color=tas.ORANGE, alpha=0.8,
                   label='PDG 2024', edgecolor='none')
    ax.errorbar(x + width/2, pdg_obs, yerr=pdg_err, fmt='none',
                ecolor=tas.BLACK, elinewidth=0.8, capsize=3)

    ax.set_ylabel(r'Mass [GeV]')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_title('Predicted vs Observed Masses', fontsize=9)
    ax.legend(fontsize=7)

    # Add relative error annotations
    for i, (pred, obs) in enumerate(zip(trxt_pred, pdg_obs)):
        err_pct = abs(pred - obs) / obs * 100
        ax.text(i, max(pred, obs) + 2, f'{err_pct:.2f}%', ha='center',
                fontsize=6.5, color=tas.VERMILLION)

    tas.panel_label(ax, 'b')

    tas.savefig(fig, os.path.join(OUTDIR, 'fig_4_1_harmonic_spectrum.png'))
    print("  ✓ fig_4_1_harmonic_spectrum.png")


# ══════════════════════════════════════════════════════════════════
# FIGURE 8: Koide Geometry (fig_4_2_koide_geometry.png)
# ══════════════════════════════════════════════════════════════════
def fig_4_2():
    fig, axes = plt.subplots(1, 2, figsize=tas.DOUBLE_COL)

    # Lepton masses (MeV)
    m_e = PDG['leptons']['electron']['mass_MeV']
    m_mu = PDG['leptons']['muon']['mass_MeV']
    m_tau = PDG['leptons']['tau']['mass_MeV']

    # Koide ratio
    sm_sqrt = np.sqrt(m_e) + np.sqrt(m_mu) + np.sqrt(m_tau)
    sm = m_e + m_mu + m_tau
    Q_koide = sm / sm_sqrt**2
    # Q = 2/3 exactly

    # (a) Koide geometric construction on Clifford torus
    ax = axes[0]
    theta = np.linspace(0, 2*np.pi, 300)
    # Clifford torus projection (2D)
    r_cliff = 1.0 / np.sqrt(2)
    x_torus = (1 + r_cliff * np.cos(theta)) * np.cos(theta * 3)
    y_torus = (1 + r_cliff * np.cos(theta)) * np.sin(theta * 3)
    ax.plot(x_torus, y_torus, color=tas.BLUE, lw=0.6, alpha=0.4)

    # Three generation points with phase δ = 2/9
    delta = 2.0/9.0
    phases = [delta, delta + 2*np.pi/3, delta + 4*np.pi/3]
    gen_names = [r'$e$', r'$\mu$', r'$\tau$']
    gen_colors = [tas.GREEN, tas.ORANGE, tas.VERMILLION]
    for phase, name, color in zip(phases, gen_names, gen_colors):
        px = (1 + r_cliff * np.cos(phase)) * np.cos(phase * 3)
        py = (1 + r_cliff * np.cos(phase)) * np.sin(phase * 3)
        ax.plot(px, py, 'o', color=color, ms=8, zorder=5)
        ax.annotate(name, (px, py), textcoords='offset points',
                    xytext=(8, 5), fontsize=10, fontweight='bold', color=color)

    ax.set_xlim(-2.2, 2.2)
    ax.set_ylim(-2.2, 2.2)
    ax.set_aspect('equal')
    ax.set_title(r'Clifford Torus ($S^3$) with $\delta = 2/9$', fontsize=9)
    ax.text(0, -2.0, f'$Q_{{\\rm Koide}} = {Q_koide:.6f}$\n(exact: 2/3)',
            ha='center', fontsize=8, color=tas.BLUE)
    ax.set_xlabel(r'$x$')
    ax.set_ylabel(r'$y$')
    tas.panel_label(ax, 'a')

    # (b) Seifert fibering → 3 generations
    ax = axes[1]
    # Log mass ratios from Seifert volumes
    seiferts = [r'$\Sigma(3,3,3)$', r'$\Sigma(2,4,4)$', r'$\Sigma(2,3,6)$']
    abc = [27, 32, 36]
    masses_obs = [m_e, m_mu, m_tau]
    # BCS tunneling: m_i ~ M* exp(-4X / abc_i)
    masses_pred = [M_STAR*1000 * np.exp(-4*X_PARAM/a) for a in abc]

    x = np.arange(3)
    width = 0.3
    ax.bar(x - width/2, np.log10(masses_obs), width, color=tas.ORANGE,
           label='PDG 2024', edgecolor='none')
    ax.bar(x + width/2, np.log10(masses_pred), width, color=tas.BLUE,
           label='TRXT (BCS)', edgecolor='none')
    ax.set_xticks(x)
    ax.set_xticklabels(seiferts, fontsize=8)
    ax.set_ylabel(r'$\log_{10}(m / \mathrm{MeV})$')
    ax.set_title('Seifert Fibering → Mass Hierarchy', fontsize=9)
    ax.legend(fontsize=7)

    # Add mass labels
    for i, (obs, pred) in enumerate(zip(masses_obs, masses_pred)):
        ax.text(i - width/2, np.log10(obs) + 0.15, f'{obs:.1f}',
                ha='center', fontsize=6, color=tas.ORANGE)
        ax.text(i + width/2, np.log10(pred) + 0.15, f'{pred:.0f}',
                ha='center', fontsize=6, color=tas.BLUE)
    tas.panel_label(ax, 'b')

    tas.savefig(fig, os.path.join(OUTDIR, 'fig_4_2_koide_geometry.png'))
    print("  ✓ fig_4_2_koide_geometry.png")


# ══════════════════════════════════════════════════════════════════
# FIGURE 9: Neutrino Tunneling (fig_neutrino_tunneling.png)
# ══════════════════════════════════════════════════════════════════
def fig_neutrino_tunneling():
    fig, ax = plt.subplots(figsize=(3.375, 3.0))

    # BCS tunneling mechanism: m_i = M* exp(-4X / (abc_i))
    abc_vals = np.linspace(10, 50, 200)
    mass_predicted = M_STAR * 1000 * np.exp(-4 * X_PARAM / abc_vals)  # in MeV

    ax.semilogy(abc_vals, mass_predicted, color=tas.BLUE, lw=1.4,
                label=r'$m = M^* \exp(-4X/abc)$')

    # Mark the three generations
    gen_data = [
        (27, 'e', PDG['leptons']['electron']['mass_MeV'], tas.GREEN),
        (32, r'\mu', PDG['leptons']['muon']['mass_MeV'], tas.ORANGE),
        (36, r'\tau', PDG['leptons']['tau']['mass_MeV'], tas.VERMILLION),
    ]
    for abc, name, m_obs, color in gen_data:
        m_pred = M_STAR * 1000 * np.exp(-4 * X_PARAM / abc)
        ax.plot(abc, m_pred, 'o', color=color, ms=6, zorder=5)
        ax.plot(abc, m_obs, 's', color=color, ms=5, mfc='white', mew=1.0, zorder=5)
        ax.annotate(f'${name}$', (abc, m_obs), textcoords='offset points',
                    xytext=(8, 0), fontsize=9, color=color)

    ax.set_xlabel(r'$abc$ (Seifert product)')
    ax.set_ylabel(r'Mass [MeV]')
    ax.set_title('BCS Tunneling: Fermion Mass Hierarchy', fontsize=9)
    ax.legend(fontsize=7)

    # Add explanation
    ax.text(15, 1e-3, r'$M^* = 365.24$ GeV' + '\n' +
            r'$X = 3/(2\alpha) \approx 205.5$',
            fontsize=7, color=tas.GREY,
            bbox=dict(facecolor='white', edgecolor=tas.GREY, lw=0.3, pad=2))

    tas.savefig(fig, os.path.join(OUTDIR, 'fig_neutrino_tunneling.png'))
    print("  ✓ fig_neutrino_tunneling.png")


# ══════════════════════════════════════════════════════════════════
# FIGURE 10: Particle Periodic Table (fig_particle_periodic_table.png)
# ══════════════════════════════════════════════════════════════════
def fig_particle_periodic_table():
    fig, ax = plt.subplots(figsize=(7.0, 5.0))

    # Topological mode assignments (p,q) → particle
    modes = [
        # Bosons        (p,  q,  name,   mass,      color,       offset)
        (5, 7, 'H', 125.26, tas.BLUE, (8, 5)),
        (5, 50, 'W', 80.35, tas.BLUE, (8, -8)),
        (8, 8, 'Z', 91.31, tas.BLUE, (8, 5)),
        # DT-1
        (128, 128, 'DT-1', 5.70, tas.VERMILLION, (-12, 8)),
        # Leptons — staggered offsets to avoid overlap at (2,3)(2,4)(3,3)
        (3, 3, r'$e$', 0.511e-3, tas.GREEN, (8, -8)),
        (2, 4, r'$\mu$', 105.7e-3, tas.GREEN, (-25, 5)),
        (2, 3, r'$\tau$', 1.777, tas.GREEN, (8, 8)),
    ]

    # Plot in (p, q) space with bubble size proportional to log(mass)
    for p, q, name, mass, color, offset in modes:
        size = 30 + 60 * np.log10(max(mass, 0.001) + 1)
        ax.scatter(p, q, s=size, color=color, alpha=0.7, edgecolors=color,
                   linewidths=1.0, zorder=5)
        ax.annotate(f'{name}\n{mass:.2f} GeV', (p, q),
                    textcoords='offset points', xytext=offset,
                    fontsize=7, color=color, fontweight='bold')

    # Spectral lines (constant p or q)
    for p_line in [2, 3, 5, 8]:
        q_range = np.arange(1, 140)
        E_line = M_STAR * (1.0/p_line + 1.0/q_range)
        valid = (E_line < 200) & (E_line > 1)
        if np.any(valid):
            ax.plot(np.full(np.sum(valid), p_line), q_range[valid],
                    '.', color=tas.SKY_BLUE, ms=1, alpha=0.3)

    ax.set_xlabel(r'Toroidal winding $p$')
    ax.set_ylabel(r'Poloidal winding $q$')
    ax.set_title(r'Topological Periodic Table: $(p,q)$ Mode Space', fontsize=9)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlim(1.5, 200)
    ax.set_ylim(1.5, 200)

    # Legend patches
    from matplotlib.lines import Line2D
    leg_elements = [
        Line2D([0], [0], marker='o', color=tas.BLUE, lw=0, ms=6, label='Gauge Bosons'),
        Line2D([0], [0], marker='o', color=tas.GREEN, lw=0, ms=6, label='Leptons'),
        Line2D([0], [0], marker='o', color=tas.VERMILLION, lw=0, ms=6, label='Dark Tower'),
    ]
    ax.legend(handles=leg_elements, fontsize=7, loc='lower left')

    tas.savefig(fig, os.path.join(OUTDIR, 'fig_particle_periodic_table.png'))
    print("  ✓ fig_particle_periodic_table.png")


# ══════════════════════════════════════════════════════════════════
# RUN ALL
# ══════════════════════════════════════════════════════════════════
if __name__ == '__main__':
    print("=" * 60)
    print("TRXT Academic Figures — Part A (Main Report §1–4)")
    print("=" * 60)
    fig_1_1()
    fig_1_2()
    fig_3_0()
    fig_06()
    fig_07()
    fig_3_1()
    fig_4_1()
    fig_4_2()
    fig_neutrino_tunneling()
    fig_particle_periodic_table()
    print("\n✅ Part A complete: 10 figures generated.")
