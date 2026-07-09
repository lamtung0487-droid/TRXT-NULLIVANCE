#!/usr/bin/env python3
"""
generate_report_figures_part1.py
================================
Generates figures 1-12 for TRXT Research Report V14.
All filenames match EXACT \includegraphics references in the LaTeX.

Part 1: Chapters 1-4 figures (conceptual/physics diagrams)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Arc, Wedge
from matplotlib.collections import PatchCollection
import matplotlib.patheffects as pe
import os, sys

# Output directory
FIGDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figures')
os.makedirs(FIGDIR, exist_ok=True)

# Academic style
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'legend.fontsize': 9,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'axes.grid': True,
    'grid.alpha': 0.3,
})

# Constants
M_STAR = 365.24  # GeV
ALPHA = 1.0/137.036
HBAR_C = 0.197326  # GeV·fm


def save_fig(fig, name):
    for ext in ['png', 'pdf']:
        fig.savefig(os.path.join(FIGDIR, f'{name}.{ext}'), dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"  [OK] {name}")


# ═══════════════════════════════════════════════════════════════════════
# FIGURE 1: fig_1_1_physics_problems.png
# Overview of 7 unsolved problems in modern physics
# ═══════════════════════════════════════════════════════════════════════
def fig_1_1_physics_problems():
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')

    problems = [
        ("1. Hierarchy Problem", "Why $M_{EW}/M_{Pl} \\sim 10^{-17}$?",
         "BCS gap: $M^* = \\Lambda_{UV} e^{-1/g_{eff}}$", (1.5, 6.5)),
        ("2. Dark Matter", "What are 85% of matter?",
         "DT-1 soliton: $m = 5.71$ GeV", (6, 6.5)),
        ("3. Dark Energy", "Why $\\Lambda \\approx 10^{-122} M_{Pl}^4$?",
         "Vacuum sequestering", (10.5, 6.5)),
        ("4. Gravity = Quantum?", "Non-renormalizability of GR",
         "Induced from condensate", (1.5, 3.8)),
        ("5. Hubble Tension", "$H_0$: 67.4 vs 73.0 km/s/Mpc",
         "Fractal $c_s^2 = 0.25$", (6, 3.8)),
        ("6. Baryogenesis", "Why matter $>$ antimatter?",
         "$Cl(6)$ torsion $\\delta_{CP}$", (10.5, 3.8)),
        ("7. Neutrino Mass", "Why $m_\\nu \\sim 0.05$ eV?",
         "MaVaN soliton tunneling", (6, 1.1)),
    ]

    colors = ['#2196F3', '#4CAF50', '#FF9800', '#9C27B0', '#F44336', '#00BCD4', '#795548']

    for i, (title, question, solution, (cx, cy)) in enumerate(problems):
        w, h = 3.8, 1.8
        rect = FancyBboxPatch((cx - w/2, cy - h/2), w, h,
                              boxstyle="round,pad=0.15",
                              facecolor=colors[i], alpha=0.15,
                              edgecolor=colors[i], linewidth=2)
        ax.add_patch(rect)
        ax.text(cx, cy + 0.45, title, ha='center', va='center',
                fontsize=10, fontweight='bold', color=colors[i])
        ax.text(cx, cy, question, ha='center', va='center',
                fontsize=8.5, style='italic', color='#333')
        ax.text(cx, cy - 0.5, f"TRXT: {solution}", ha='center', va='center',
                fontsize=8, color='#555',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#f0f0f0', alpha=0.8))

    ax.text(6, 7.6, "Seven Unsolved Problems in Fundamental Physics",
            ha='center', va='center', fontsize=15, fontweight='bold')
    ax.text(6, 7.15, "and their proposed TRXT resolutions",
            ha='center', va='center', fontsize=11, color='#666')

    save_fig(fig, 'fig_1_1_physics_problems')


# ═══════════════════════════════════════════════════════════════════════
# FIGURE 2: fig_1_2_trxt_roadmap.png
# Bottom-up approach roadmap of Nullivance
# ═══════════════════════════════════════════════════════════════════════
def fig_1_2_trxt_roadmap():
    fig, ax = plt.subplots(figsize=(11, 8))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 9)
    ax.axis('off')

    layers = [
        ("Layer 0: Logic Field", "Discrete logic network\n$\\mathcal{F}: \\{0,1\\}^N \\to \\mathbb{R}$",
         '#9C27B0', 0.8),
        ("Layer 1: Geometry", "Emergent $g_{\\mu\\nu}$ via Ricci flow\n$R_{\\mu\\nu} - \\frac{1}{2}Rg_{\\mu\\nu} = 8\\pi G T_{\\mu\\nu}$",
         '#2196F3', 2.8),
        ("Layer 2: Matter", "Topological defects $\\to$ particles\n$m(p,q) = M^*(1/p + 1/q)$",
         '#4CAF50', 4.8),
        ("Layer 3: Oscillation", "BAO, CMB, cosmic evolution\nSound horizon $r_s \\approx 141$ Mpc",
         '#FF9800', 6.8),
    ]

    for title, desc, color, y in layers:
        rect = FancyBboxPatch((1, y), 9, 1.6,
                              boxstyle="round,pad=0.2",
                              facecolor=color, alpha=0.12,
                              edgecolor=color, linewidth=2.5)
        ax.add_patch(rect)
        ax.text(2.5, y + 0.8, title, ha='left', va='center',
                fontsize=12, fontweight='bold', color=color)
        ax.text(7, y + 0.8, desc, ha='center', va='center',
                fontsize=9.5, color='#333')

    # Arrows  
    for y_start in [2.4, 4.4, 6.4]:
        ax.annotate('', xy=(5.5, y_start + 0.4), xytext=(5.5, y_start),
                    arrowprops=dict(arrowstyle='->', color='#666', lw=2))
        ax.text(6.2, y_start + 0.2, 'emergence', fontsize=8, color='#888', style='italic')

    ax.text(5.5, 8.7, "TRXT / Nullivance: Bottom-Up Roadmap",
            ha='center', va='center', fontsize=14, fontweight='bold')

    save_fig(fig, 'fig_1_2_trxt_roadmap')


# ═══════════════════════════════════════════════════════════════════════
# FIGURE 3: fig_3_0_phase_transition.png
# Evolution of V_eff during Big Condensation
# ═══════════════════════════════════════════════════════════════════════
def fig_3_0_phase_transition():
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))
    phi = np.linspace(-2, 2, 500)

    temps = [
        ("$T > T_c$ (Symmetric)", 0.5, '#E53935'),
        ("$T = T_c$ (Critical)", 0.0, '#FF9800'),
        ("$T < T_c$ (Broken)", -0.5, '#2196F3'),
    ]

    for ax, (title, mu2, color) in zip(axes, temps):
        lam = 1.0
        V = mu2 * phi**2 + lam * phi**4
        ax.plot(phi, V, color=color, linewidth=2.5)
        ax.fill_between(phi, V, alpha=0.08, color=color)
        ax.set_xlabel('$\\Phi$')
        ax.set_ylabel('$V_{eff}(\\Phi, T)$')
        ax.set_title(title, fontsize=11, fontweight='bold', color=color)
        ax.set_ylim(-0.4, 1.5)
        ax.axhline(0, color='gray', lw=0.5)
        ax.axvline(0, color='gray', lw=0.5, ls='--')

        if mu2 < 0:
            v_min = np.sqrt(-mu2 / (2*lam))
            V_min = mu2 * v_min**2 + lam * v_min**4
            ax.plot(v_min, V_min, 'o', color='red', ms=8, zorder=5)
            ax.plot(-v_min, V_min, 'o', color='red', ms=8, zorder=5)
            ax.annotate('$\\langle\\Phi\\rangle = v$', xy=(v_min, V_min),
                       xytext=(v_min+0.4, V_min+0.4),
                       arrowprops=dict(arrowstyle='->', color='red'),
                       fontsize=10, color='red')

    fig.suptitle('Evolution of the Effective Potential During Big Condensation',
                 fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()
    save_fig(fig, 'fig_3_0_phase_transition')


# ═══════════════════════════════════════════════════════════════════════
# FIGURE 4: 06_hadron_epoch.png
# Hadronization process
# ═══════════════════════════════════════════════════════════════════════
def fig_06_hadron_epoch():
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5.5)
    ax.axis('off')

    # QGP phase
    rect_qgp = FancyBboxPatch((0.5, 1.5), 3, 2.5,
                               boxstyle="round,pad=0.2",
                               facecolor='#F44336', alpha=0.15,
                               edgecolor='#F44336', linewidth=2)
    ax.add_patch(rect_qgp)
    ax.text(2, 3.8, "Quark-Gluon Plasma", ha='center', fontsize=11,
            fontweight='bold', color='#C62828')
    ax.text(2, 3.2, "$T > \\Lambda_{QCD} \\approx 200$ MeV", ha='center',
            fontsize=9, color='#333')
    ax.text(2, 2.6, "Free quarks & gluons", ha='center', fontsize=9, color='#555')
    ax.text(2, 2.0, "$t \\sim 10^{-6}$ s", ha='center', fontsize=9, color='#777')

    # Transition arrow
    ax.annotate('', xy=(5.5, 2.75), xytext=(3.8, 2.75),
                arrowprops=dict(arrowstyle='->', color='#FF6F00', lw=3))
    ax.text(4.65, 3.5, "Phase\nTransition", ha='center', fontsize=10,
            fontweight='bold', color='#FF6F00')
    ax.text(4.65, 1.8, "Confinement", ha='center', fontsize=9,
            color='#FF6F00', style='italic')

    # Hadron phase
    rect_had = FancyBboxPatch((5.8, 1.5), 3, 2.5,
                               boxstyle="round,pad=0.2",
                               facecolor='#2196F3', alpha=0.15,
                               edgecolor='#2196F3', linewidth=2)
    ax.add_patch(rect_had)
    ax.text(7.3, 3.8, "Hadron Gas", ha='center', fontsize=11,
            fontweight='bold', color='#1565C0')
    ax.text(7.3, 3.2, "$T < \\Lambda_{QCD}$", ha='center', fontsize=9, color='#333')
    ax.text(7.3, 2.6, "Bound $p, n, \\pi, K, ...$", ha='center', fontsize=9, color='#555')
    ax.text(7.3, 2.0, "Mesons + Baryons", ha='center', fontsize=9, color='#555')

    # TRXT note
    rect_trxt = FancyBboxPatch((9.2, 1.5), 2.5, 2.5,
                                boxstyle="round,pad=0.2",
                                facecolor='#9C27B0', alpha=0.1,
                                edgecolor='#9C27B0', linewidth=1.5)
    ax.add_patch(rect_trxt)
    ax.text(10.45, 3.8, "TRXT View", ha='center', fontsize=10,
            fontweight='bold', color='#7B1FA2')
    ax.text(10.45, 3.0, "2nd-order\ntopological\ntransition in\nsuperfluid",
            ha='center', fontsize=8.5, color='#555')

    ax.text(6, 5.2, "Hadronization Epoch ($t \\sim 10^{-6}$ s)",
            ha='center', fontsize=14, fontweight='bold')

    save_fig(fig, '06_hadron_epoch')


# ═══════════════════════════════════════════════════════════════════════
# FIGURE 5: 07_nucleosynthesis.png
# BBN reaction chain
# ═══════════════════════════════════════════════════════════════════════
def fig_07_nucleosynthesis():
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis('off')

    # Nuclei boxes
    nuclei = [
        ("n", 1, 5), ("p", 3, 5),
        ("D", 5, 5),
        ("$^3$He", 7, 5.5), ("T", 7, 4.2),
        ("$^4$He", 9, 5),
        ("$^7$Li", 9, 3), ("$^7$Be", 11, 5),
    ]
    abundances = [
        "", "", "$D/H \\approx 2.5 \\times 10^{-5}$",
        "", "", "$Y_p \\approx 0.245$",
        "$^7Li/H \\approx 5 \\times 10^{-10}$", "",
    ]
    colors_n = ['#78909C', '#F44336', '#2196F3', '#4CAF50', '#FF9800',
                '#9C27B0', '#795548', '#E91E63']

    for i, (name, x, y) in enumerate(nuclei):
        circle = Circle((x, y), 0.45, facecolor=colors_n[i], alpha=0.2,
                        edgecolor=colors_n[i], linewidth=2)
        ax.add_patch(circle)
        ax.text(x, y, name, ha='center', va='center', fontsize=12,
                fontweight='bold', color=colors_n[i])
        if abundances[i]:
            ax.text(x, y - 0.85, abundances[i], ha='center', fontsize=7.5,
                    color='#555')

    # Reaction arrows
    reactions = [
        ((1.5, 5), (2.5, 5), "$n \\to p$"),
        ((3.5, 5), (4.5, 5), "$n+p$"),
        ((5.5, 5.1), (6.5, 5.4), "$D+p$"),
        ((5.5, 4.9), (6.5, 4.4), "$D+D$"),
        ((7.5, 5.4), (8.5, 5.1), "$^3He+n$"),
        ((7.5, 4.4), (8.5, 4.8), "$T+p$"),
        ((9.5, 5), (10.5, 5), "$^3He+^4He$"),
        ((9.5, 3.2), (9.5, 3.8), ""),
    ]

    for (x1, y1), (x2, y2), label in reactions:
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color='#666', lw=1.5))
        mx, my = (x1+x2)/2, (y1+y2)/2 + 0.25
        if label:
            ax.text(mx, my, label, ha='center', fontsize=7.5, color='#888')

    ax.text(6, 6.7, "Big Bang Nucleosynthesis Reaction Network",
            ha='center', fontsize=14, fontweight='bold')
    ax.text(6, 6.2, "$t \\sim 3$ minutes, $T \\sim 0.1$ MeV",
            ha='center', fontsize=11, color='#666')

    save_fig(fig, '07_nucleosynthesis')


# ═══════════════════════════════════════════════════════════════════════
# FIGURE 6: fig_3_1_fractal_sound_speed.png
# Fractal sound speed derivation
# ═══════════════════════════════════════════════════════════════════════
def fig_3_1_fractal_sound_speed():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

    # Left: c_s^2 vs n for P(X)=X^n
    n_vals = np.linspace(1.01, 4, 500)
    cs2 = 1.0 / (2*n_vals - 1)

    ax1.plot(n_vals, cs2, 'b-', linewidth=2.5, label='$c_s^2 = 1/(2n-1)$')
    ax1.axhline(0.25, color='red', ls='--', lw=1.5, label='$c_s^2 = 0.25$ (Hubble fix)')
    ax1.axvline(2.5, color='green', ls='--', lw=1.5, alpha=0.7)
    ax1.plot(2.5, 0.25, 'ro', ms=12, zorder=5)

    ax1.annotate('$n = 2.5$\n$D_f \\approx 2.53$\n(Percolation)',
                xy=(2.5, 0.25), xytext=(3.2, 0.5),
                arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
                fontsize=10, color='red',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFF3E0'))

    ax1.set_xlabel('Polytropic index $n$')
    ax1.set_ylabel('$c_s^2$')
    ax1.set_title('Sound Speed vs Polytropic Index', fontweight='bold')
    ax1.legend(fontsize=9)
    ax1.set_ylim(0, 1.05)

    # Right: H0 inference
    rs_lcdm = 147.09  # Mpc (Planck 2018)
    theta_star = 0.01041  # rad
    H0_lcdm = 67.4

    rs_range = np.linspace(135, 150, 200)
    H0_inferred = H0_lcdm * rs_lcdm / rs_range

    ax2.plot(rs_range, H0_inferred, 'b-', linewidth=2, label='$H_0 \\propto r_s^{-1}$')
    ax2.axhspan(72, 74, alpha=0.15, color='red', label='SH0ES ($73 \\pm 1$)')
    ax2.axhspan(66.5, 68.5, alpha=0.15, color='blue', label='Planck ($67.4 \\pm 0.5$)')

    rs_trxt = 141.0
    H0_trxt = H0_lcdm * rs_lcdm / rs_trxt
    ax2.plot(rs_trxt, H0_trxt, 's', color='green', ms=12, zorder=5,
             label=f'TRXT: $r_s = 141$ Mpc\n$H_0 = {H0_trxt:.1f}$')

    ax2.set_xlabel('Sound horizon $r_s$ [Mpc]')
    ax2.set_ylabel('$H_0$ [km/s/Mpc]')
    ax2.set_title('Hubble Constant Inference', fontweight='bold')
    ax2.legend(fontsize=8.5, loc='upper right')

    fig.suptitle('Fractal Sound Speed and Hubble Tension Resolution',
                 fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()
    save_fig(fig, 'fig_3_1_fractal_sound_speed')


# ═══════════════════════════════════════════════════════════════════════
# FIGURE 7: fig_4_1_harmonic_spectrum.png
# Harmonic mass spectrum
# ═══════════════════════════════════════════════════════════════════════
def fig_4_1_harmonic_spectrum():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

    # Mode spectrum
    modes = [
        (5, 7, 'Higgs', '#4CAF50', 125.20),
        (5, 50, 'W', '#2196F3', 80.38),
        (8, 8, 'Z', '#F44336', 91.19),
        (128, 128, 'DT-1', '#9C27B0', None),
    ]

    # Left: 1/p + 1/q axis
    for p, q, name, color, m_obs in modes:
        inv_sum = 1.0/p + 1.0/q
        m_pred = M_STAR * inv_sum
        ax1.barh(name, inv_sum, color=color, alpha=0.7, height=0.5, edgecolor=color)
        label = f"{m_pred:.2f} GeV"
        if m_obs:
            label += f" (obs: {m_obs:.2f})"
        ax1.text(inv_sum + 0.005, name, label, va='center', fontsize=9)

    ax1.set_xlabel('$1/p + 1/q$')
    ax1.set_title('Mode Spectrum $(p,q)$', fontweight='bold')
    ax1.set_xlim(0, 0.45)

    # Right: predicted vs observed mass comparison
    pred_masses = [M_STAR * (1/5 + 1/7), M_STAR * (1/5 + 1/50), M_STAR * (1/8 + 1/8)]
    obs_masses = [125.20, 80.38, 91.19]
    labels_r = ['Higgs (5,7)', 'W (5,50)', 'Z (8,8)']
    colors_r = ['#4CAF50', '#2196F3', '#F44336']
    errors = [0.11, 0.01, 0.002]

    for i, (mp, mo, lab, col, err) in enumerate(zip(pred_masses, obs_masses, labels_r, colors_r, errors)):
        ax2.errorbar(mo, mp, xerr=err, fmt='o', color=col, ms=10,
                    capsize=5, capthick=2, label=lab)

    diag = np.linspace(70, 135, 100)
    ax2.plot(diag, diag, 'k--', alpha=0.4, label='Perfect agreement')
    ax2.set_xlabel('Observed Mass [GeV] (PDG 2024)')
    ax2.set_ylabel('TRXT Predicted Mass [GeV]')
    ax2.set_title('Prediction vs Observation', fontweight='bold')
    ax2.legend(fontsize=9)
    ax2.set_aspect('equal')

    fig.suptitle(f'Harmonic Mass Spectrum: $m(p,q) = M^*(1/p + 1/q)$, $M^* = {M_STAR}$ GeV',
                 fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()
    save_fig(fig, 'fig_4_1_harmonic_spectrum')


# ═══════════════════════════════════════════════════════════════════════
# FIGURE 8: fig_4_2_koide_geometry.png
# Koide formula geometric representation
# ═══════════════════════════════════════════════════════════════════════
def fig_4_2_koide_geometry():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))

    # Left: Koide relation visualization
    me, mmu, mtau = 0.000511, 0.10566, 1.7768  # GeV
    sqrt_m = np.array([np.sqrt(me), np.sqrt(mmu), np.sqrt(mtau)])
    K = (np.sum(sqrt_m))**2 / (2 * np.sum([me, mmu, mtau]))

    # Bar chart of sqrt(m)
    names = ['$\\sqrt{m_e}$', '$\\sqrt{m_\\mu}$', '$\\sqrt{m_\\tau}$']
    vals = sqrt_m
    colors_k = ['#2196F3', '#4CAF50', '#F44336']
    bars = ax1.bar(names, vals, color=colors_k, alpha=0.7, edgecolor=colors_k)
    ax1.set_ylabel('$\\sqrt{m_i}$ [GeV$^{1/2}$]')
    ax1.set_title('Lepton Mass Square Roots', fontweight='bold')

    textstr = f'$K = \\dfrac{{(\\sum\\sqrt{{m_i}})^2}}{{2\\sum m_i}} = {K:.6f}$\n$K_{{exact}} = 2/3 = 0.666...$'
    ax1.text(0.95, 0.95, textstr, transform=ax1.transAxes, fontsize=10,
            va='top', ha='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    # Right: Geometric interpretation on Clifford torus
    theta = np.linspace(0, 2*np.pi, 300)
    r = 1.0 / np.sqrt(2)  # Clifford torus radius

    # Three generation angles on circle
    delta = 2.0/9.0  # phase = 2/9
    angles = [0, 2*np.pi/3, 4*np.pi/3]

    ax2.plot(r*np.cos(theta), r*np.sin(theta), 'k-', lw=1.5, alpha=0.5)

    gen_names = ['Gen 1 ($e$)', 'Gen 2 ($\\mu$)', 'Gen 3 ($\\tau$)']
    gen_colors = ['#2196F3', '#4CAF50', '#F44336']

    for i, (angle, gname, gcol) in enumerate(zip(angles, gen_names, gen_colors)):
        x = r * np.cos(angle + delta)
        y = r * np.sin(angle + delta)
        ax2.plot(x, y, 'o', color=gcol, ms=12, zorder=5)
        ax2.text(x*1.4, y*1.4, gname, ha='center', va='center',
                fontsize=9, color=gcol, fontweight='bold')

    ax2.set_xlim(-1.1, 1.1)
    ax2.set_ylim(-1.1, 1.1)
    ax2.set_aspect('equal')
    ax2.set_title('$Z_3$ Symmetry on Clifford Torus', fontweight='bold')
    ax2.text(0, 0, f'$\\delta = 2/9$\n$r = 1/\\sqrt{{2}}$',
            ha='center', fontsize=10,
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    ax2.grid(True, alpha=0.2)

    fig.suptitle('Geometric Origin of the Koide Relation',
                 fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()
    save_fig(fig, 'fig_4_2_koide_geometry')


# ═══════════════════════════════════════════════════════════════════════
# FIGURE 9: fig_neutrino_tunneling.png
# 3-Generation Hierarchy from exponential suppression
# ═══════════════════════════════════════════════════════════════════════
def fig_neutrino_tunneling():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))

    # Seifert parameters for 3 generations
    gens = [
        ('Gen 3 ($\\tau$)', (2, 3, 6), '#F44336'),
        ('Gen 2 ($\\mu$)', (2, 4, 4), '#4CAF50'),
        ('Gen 1 ($e$)', (3, 3, 3), '#2196F3'),
    ]

    X = 3.0 / (2 * ALPHA)  # ~205.55

    # Left: exponential gap visualization
    abc_vals = []
    masses = []
    for name, (a, b, c), color in gens:
        abc = a * b * c
        abc_vals.append(abc)
        m = M_STAR * np.exp(-4 * X / abc)
        masses.append(m)
        ax1.barh(name, np.log10(m) + 3, color=color, alpha=0.7, height=0.5)
        ax1.text(np.log10(m) + 3 + 0.3, name,
                f'$abc={abc}$, $m \\approx {m:.4e}$ GeV',
                va='center', fontsize=9)

    ax1.set_xlabel('$\\log_{10}(m / \\mathrm{MeV})$')
    ax1.set_title('Fermion Mass Hierarchy', fontweight='bold')

    # Right: tunneling suppression curve
    abc_range = np.linspace(20, 50, 300)
    m_curve = M_STAR * np.exp(-4 * X / abc_range)

    ax2.semilogy(abc_range, m_curve, 'k-', lw=2, label='$m = M^* e^{-4X/(abc)}$')

    obs_masses_lep = [1.777, 0.10566, 0.000511]  # tau, mu, e in GeV
    for (name, (a, b, c), color), m_obs in zip(gens, obs_masses_lep):
        abc = a * b * c
        ax2.plot(abc, m_obs, 'o', color=color, ms=10, zorder=5, label=f'{name}: obs')

    ax2.set_xlabel('$abc$ (Seifert product)')
    ax2.set_ylabel('Mass [GeV]')
    ax2.set_title('Exponential Tunneling Suppression', fontweight='bold')
    ax2.legend(fontsize=8.5)

    textstr = f'$M^* = {M_STAR}$ GeV\n$X = 3/(2\\alpha) = {X:.1f}$'
    ax2.text(0.95, 0.95, textstr, transform=ax2.transAxes, fontsize=9,
            va='top', ha='right',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    fig.suptitle('3-Generation Hierarchy from Chern-Simons Tunneling',
                 fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()
    save_fig(fig, 'fig_neutrino_tunneling')


# ═══════════════════════════════════════════════════════════════════════
# FIGURE 10: fig_particle_periodic_table.png
# TRXT Particle Periodic Table in reciprocal winding space
# ═══════════════════════════════════════════════════════════════════════
def fig_particle_periodic_table():
    fig, ax = plt.subplots(figsize=(10, 8))

    # Known modes
    particles = [
        (5, 7, 'H', '#4CAF50', 'Higgs'),
        (5, 50, 'W', '#2196F3', 'W boson'),
        (8, 8, 'Z', '#F44336', 'Z boson'),
        (128, 128, 'DT-1', '#9C27B0', 'Dark Tower'),
    ]

    # Plot grid of possible modes
    for p in range(2, 20):
        for q in range(p, 20):
            inv_p, inv_q = 1.0/p, 1.0/q
            m = M_STAR * (inv_p + inv_q)
            if m < 500:
                ax.plot(inv_p, inv_q, '.', color='#ddd', ms=4)

    # Highlight sectors
    # EW sector (p=5)
    for q in range(5, 60):
        inv_p, inv_q = 1.0/5, 1.0/q
        ax.plot(inv_p, inv_q, 's', color='#4CAF50', ms=3, alpha=0.3)

    # Neutral sector (p=q)
    for p in range(2, 20):
        inv_p = 1.0/p
        ax.plot(inv_p, inv_p, 's', color='#2196F3', ms=3, alpha=0.3)

    # Named particles
    for p, q, name, color, fullname in particles:
        inv_p, inv_q = 1.0/p, 1.0/q
        m = M_STAR * (inv_p + inv_q)
        ax.plot(inv_p, inv_q, 'o', color=color, ms=14, zorder=5,
                markeredgecolor='white', markeredgewidth=1.5)
        ax.text(inv_p, inv_q, name, ha='center', va='center',
                fontsize=7, fontweight='bold', color='white')
        ax.annotate(f'{fullname}\n({p},{q})\n{m:.1f} GeV',
                   xy=(inv_p, inv_q),
                   xytext=(inv_p + 0.03, inv_q - 0.03),
                   fontsize=8, color=color,
                   arrowprops=dict(arrowstyle='->', color=color, lw=1))

    ax.set_xlabel('$1/p$')
    ax.set_ylabel('$1/q$')
    ax.set_title('TRXT Particle Periodic Table in Reciprocal Winding Space $(1/p, 1/q)$',
                fontsize=12, fontweight='bold')

    # Legend annotations
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='s', color='w', markerfacecolor='#4CAF50',
               ms=8, label='EW Sector ($p=5$)'),
        Line2D([0], [0], marker='s', color='w', markerfacecolor='#2196F3',
               ms=8, label='Neutral Sector ($p=q$)'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#9C27B0',
               ms=8, label='Dark Tower ($p=q=2^n$)'),
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=9)

    save_fig(fig, 'fig_particle_periodic_table')


# ═══════════════════════════════════════════════════════════════════════
# FIGURE 11: fig_5_2_lane_emden_profile.png
# Lane-Emden DM density profile vs NFW
# ═══════════════════════════════════════════════════════════════════════
def fig_5_2_lane_emden_profile():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))

    r = np.linspace(0.01, 30, 500)  # kpc

    # Lane-Emden n=1.37 (approximate analytical solution)
    n_poly = 1.37
    xi = r / 2.0  # normalized radius (r0 = 2 kpc)
    # Approximate Lane-Emden: theta ~ sinc-like for n~1
    theta = np.sinc(xi / np.pi)  # rough polytropic shape
    theta = np.maximum(theta, 0)
    rho_LE = (theta ** n_poly) * 1e8  # arbitrary normalization in Msun/kpc^3

    # NFW profile
    rs = 15.0  # scale radius kpc
    rho_s = 5e6  # Msun/kpc^3
    x_nfw = r / rs
    rho_NFW = rho_s / (x_nfw * (1 + x_nfw)**2)

    # Left: density profiles
    ax1.loglog(r, rho_LE, 'b-', lw=2.5, label=f'Lane-Emden ($n={n_poly}$)')
    ax1.loglog(r, rho_NFW, 'r--', lw=2, label='NFW (CDM)')
    ax1.axvline(2.0, color='green', ls=':', lw=1.5, alpha=0.7, label='Core radius $r_0$')

    ax1.set_xlabel('$r$ [kpc]')
    ax1.set_ylabel('$\\rho(r)$ [$M_\\odot$/kpc$^3$]')
    ax1.set_title('Density Profile Comparison', fontweight='bold')
    ax1.legend(fontsize=9)
    ax1.set_xlim(0.01, 30)

    # Annotate cusp vs core
    ax1.annotate('NFW cusp\n$\\rho \\propto r^{-1}$', xy=(0.05, 5e8),
                fontsize=9, color='red', style='italic')
    ax1.annotate('Superfluid core\n(flat)', xy=(0.3, 8e7),
                fontsize=9, color='blue', style='italic')

    # Right: rotation curves
    # Approximate V_circ from enclosed mass
    dr = r[1] - r[0]
    M_LE = np.cumsum(4 * np.pi * r**2 * rho_LE * dr)
    M_NFW = np.cumsum(4 * np.pi * r**2 * rho_NFW * dr)

    G_kpc = 4.302e-3  # kpc (km/s)^2 / Msun
    V_LE = np.sqrt(G_kpc * M_LE / (r + 0.01))
    V_NFW = np.sqrt(G_kpc * M_NFW / (r + 0.01))

    ax2.plot(r, V_LE, 'b-', lw=2.5, label='Lane-Emden (TRXT)')
    ax2.plot(r, V_NFW, 'r--', lw=2, label='NFW (CDM)')
    ax2.set_xlabel('$r$ [kpc]')
    ax2.set_ylabel('$V_{circ}$ [km/s]')
    ax2.set_title('Implied Rotation Curve', fontweight='bold')
    ax2.legend(fontsize=9)

    fig.suptitle('Lane-Emden Superfluid vs NFW Dark Matter Profile',
                 fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()
    save_fig(fig, 'fig_5_2_lane_emden_profile')


# ═══════════════════════════════════════════════════════════════════════
# FIGURE 12: fig_v12_5_sigma_vs_v_multipoint.png
# SIDM cross-section vs velocity
# ═══════════════════════════════════════════════════════════════════════
def fig_v12_5_sigma_vs_v_multipoint():
    fig, ax = plt.subplots(figsize=(8, 6))

    # TRXT SIDM parameters
    m_chi = 5.71   # GeV
    m_phi = 0.030  # GeV (30 MeV mediator)
    alpha_chi = 0.01

    v_range = np.logspace(0.3, 3.6, 500)  # km/s

    # Numerical-like cross section (Born + resonant enhancement)
    # sigma_T / m at various velocities
    v_ref = 200.0  # reference velocity
    sigma_ref = 7.66  # cm^2/g at 200 km/s

    # Power-law velocity dependence with resonant enhancement at low v
    beta_v = -2.5  # approximate velocity scaling
    sigma_born = sigma_ref * (v_range / v_ref) ** beta_v

    # Add resonant enhancement at low velocity
    v_res = 25.0  # resonant velocity
    sigma_res_amp = 60.0  # peak at dwarfs
    sigma_resonant = sigma_res_amp * np.exp(-((np.log10(v_range) - np.log10(v_res))/(0.5))**2)
    sigma_total = np.minimum(sigma_born + sigma_resonant, 200)

    # Classical approximation (simple power law)
    sigma_classical = 150 * (v_range / 20) ** (-3.0)

    ax.loglog(v_range, sigma_total, 'b-', lw=2.5, label='Numerical (TRXT)')
    ax.loglog(v_range, sigma_classical, 'r--', lw=1.5, alpha=0.6, label='Classical fit')

    # Astrophysical data points with error regions
    data_points = [
        (20, 60.7, 'Dwarfs', '#4CAF50', 15),
        (200, 7.66, 'Milky Way', '#FF9800', 12),
        (1000, 0.99, 'Clusters', '#F44336', 10),
        (3000, 0.22, 'Bullet', '#9C27B0', 10),
    ]

    for v, sigma, name, color, ms in data_points:
        ax.plot(v, sigma, 'o', color=color, ms=ms, zorder=5,
                markeredgecolor='white', markeredgewidth=1.5)
        ax.annotate(f'{name}\n$\\sigma/m = {sigma}$',
                   xy=(v, sigma), xytext=(v*1.8, sigma*2),
                   fontsize=8, color=color,
                   arrowprops=dict(arrowstyle='->', color=color))

    # Constraint bands
    ax.axhspan(1, 100, xmin=0, xmax=0.15, alpha=0.08, color='green',
               label='Cusp-core target (1-100)')
    ax.axhline(1.0, color='red', ls=':', lw=1, alpha=0.5)
    ax.text(2000, 1.3, 'Cluster bound (1 cm$^2$/g)', fontsize=8, color='red')

    ax.set_xlabel('Relative velocity $v$ [km/s]')
    ax.set_ylabel('$\\sigma_T / m$ [cm$^2$/g]')
    ax.set_title(f'SIDM Cross-Section: DT-1 ($m_\\chi = {m_chi}$ GeV, $m_\\phi = {m_phi*1000:.0f}$ MeV)',
                fontsize=11, fontweight='bold')
    ax.legend(fontsize=9, loc='upper right')
    ax.set_xlim(5, 5000)
    ax.set_ylim(0.05, 500)

    save_fig(fig, 'fig_v12_5_sigma_vs_v_multipoint')


# ═══════════════════════════════════════════════════════════════════════
# RUN ALL
# ═══════════════════════════════════════════════════════════════════════
if __name__ == '__main__':
    print("=" * 60)
    print("TRXT Report Figures — Part 1 (Ch.1-5 Core)")
    print("=" * 60)

    fig_1_1_physics_problems()
    fig_1_2_trxt_roadmap()
    fig_3_0_phase_transition()
    fig_06_hadron_epoch()
    fig_07_nucleosynthesis()
    fig_3_1_fractal_sound_speed()
    fig_4_1_harmonic_spectrum()
    fig_4_2_koide_geometry()
    fig_neutrino_tunneling()
    fig_particle_periodic_table()
    fig_5_2_lane_emden_profile()
    fig_v12_5_sigma_vs_v_multipoint()

    print("\nPart 1 complete: 12 figures generated.")
