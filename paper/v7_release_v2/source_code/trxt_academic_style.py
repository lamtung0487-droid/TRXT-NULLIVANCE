"""
TRXT Academic Figure Style Module
==================================
Consistent, publication-quality styling for all TRXT research figures.
Follows PRL/PRD conventions: Okabe-Ito colorblind-safe palette,
serif typeface (Computer Modern), inward ticks, minimal grid.

Usage:
    import trxt_academic_style as tas
    tas.apply()
    fig, ax = plt.subplots(figsize=tas.DOUBLE_COL)
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

# ════════════════════════════════════════════════════════════════════
# Okabe-Ito Colorblind-Safe Palette  (doi:10.1038/nmeth.1618)
# ════════════════════════════════════════════════════════════════════
BLUE       = '#0072B2'   # primary theory line
ORANGE     = '#E69F00'   # secondary data / observation
GREEN      = '#009E73'   # model B / comparison
VERMILLION = '#D55E00'   # highlight / exclusion region
SKY_BLUE   = '#56B4E9'   # confidence-band fill
PURPLE     = '#CC79A7'   # supplementary
YELLOW     = '#F0E442'   # fill accents only
BLACK      = '#000000'   # reference / SM baseline
GREY       = '#999999'   # subdued reference lines

PALETTE = [BLUE, ORANGE, GREEN, VERMILLION, SKY_BLUE, PURPLE, YELLOW, BLACK]

# ════════════════════════════════════════════════════════════════════
# Standard figure sizes (inches)   — PRL / PRD conventions
# ════════════════════════════════════════════════════════════════════
SINGLE_COL = (3.375, 2.8)    # single-column figure
DOUBLE_COL = (7.0, 4.5)      # double-column figure
WIDE       = (7.0, 3.5)      # wide single-row
TALL       = (3.375, 5.0)    # tall single-column
SQUARE     = (4.0, 4.0)      # square plot


def apply():
    """Apply the full TRXT academic style to matplotlib rcParams."""
    params = {
        # ── Font ──
        'font.family':       'serif',
        'font.serif':        ['CMU Serif', 'Computer Modern', 'Times New Roman',
                              'DejaVu Serif', 'serif'],
        'mathtext.fontset':  'cm',
        'font.size':         9,

        # ── Axes ──
        'axes.labelsize':    10,
        'axes.titlesize':    10,
        'axes.linewidth':    0.7,
        'axes.grid':         False,
        'axes.prop_cycle':   mpl.cycler(color=PALETTE),
        'axes.unicode_minus': True,
        'axes.formatter.use_mathtext': True,
        'axes.labelpad':     6,
        'axes.titlepad':     8,

        # ── Ticks (physics convention: inward, all four sides) ──
        'xtick.direction':   'in',
        'ytick.direction':   'in',
        'xtick.top':         True,
        'ytick.right':       True,
        'xtick.minor.visible': True,
        'ytick.minor.visible': True,
        'xtick.major.size':  4.5,
        'ytick.major.size':  4.5,
        'xtick.minor.size':  2.5,
        'ytick.minor.size':  2.5,
        'xtick.major.width': 0.6,
        'ytick.major.width': 0.6,
        'xtick.minor.width': 0.4,
        'ytick.minor.width': 0.4,
        'xtick.labelsize':   8,
        'ytick.labelsize':   8,

        # ── Lines ──
        'lines.linewidth':   1.2,
        'lines.markersize':  5,

        # ── Legend ──
        'legend.fontsize':   8,
        'legend.frameon':    False,
        'legend.handlelength': 1.8,
        'legend.handletextpad': 0.5,
        'legend.labelspacing': 0.35,
        'legend.borderaxespad': 0.5,

        # ── Layout ──
        'figure.constrained_layout.use': True,
        'figure.dpi':        150,
        'savefig.dpi':       300,
        'savefig.bbox':      'tight',
        'savefig.pad_inches': 0.03,

        # ── PDF export ──
        'pdf.fonttype':      42,
        'ps.fonttype':       42,

        # ── Error bars ──
        'errorbar.capsize':  2.5,

        # ── Histogram ──
        'hist.bins':         'auto',

        # ── Patch ──
        'patch.linewidth':   0.5,
    }
    mpl.rcParams.update(params)


# ════════════════════════════════════════════════════════════════════
# Helper functions
# ════════════════════════════════════════════════════════════════════

def panel_label(ax, label, loc='upper left', fontsize=11):
    """Add bold panel label (a), (b), ... at specified location."""
    locs = {
        'upper left':  (0.03, 0.95),
        'upper right': (0.95, 0.95),
        'lower left':  (0.03, 0.08),
        'lower right': (0.95, 0.08),
    }
    x, y = locs.get(loc, loc)
    ha = 'left' if x < 0.5 else 'right'
    ax.text(x, y, f'$\\mathbf{{({label})}}$', transform=ax.transAxes,
            fontsize=fontsize, fontweight='bold', va='top', ha=ha)


def theory_band(ax, x, y_central, y_lower, y_upper,
                color=BLUE, label=None, alpha=0.20):
    """Plot theory curve with confidence band."""
    ax.plot(x, y_central, color=color, lw=1.4, label=label, zorder=3)
    ax.fill_between(x, y_lower, y_upper, color=color, alpha=alpha, zorder=2)


def data_points(ax, x, y, yerr=None, xerr=None, color=ORANGE, label=None,
                marker='o', ms=5, hollow=False):
    """Plot experimental data points (open markers by default)."""
    fc = 'white' if hollow else color
    ax.errorbar(x, y, yerr=yerr, xerr=xerr, fmt='none', ecolor=color,
                elinewidth=0.8, capsize=2.5, zorder=4)
    ax.scatter(x, y, marker=marker, s=ms**2, facecolors=fc,
               edgecolors=color, linewidths=0.8, label=label, zorder=5)


def add_hline(ax, y, label=None, color=GREY, ls='--', lw=0.8):
    """Add horizontal reference line."""
    ax.axhline(y, color=color, ls=ls, lw=lw, label=label, zorder=1)


def add_vline(ax, x, label=None, color=GREY, ls='--', lw=0.8):
    """Add vertical reference line."""
    ax.axvline(x, color=color, ls=ls, lw=lw, label=label, zorder=1)


def add_region(ax, xmin, xmax, color=VERMILLION, alpha=0.08, label=None):
    """Add shaded exclusion/highlight region."""
    ax.axvspan(xmin, xmax, color=color, alpha=alpha, label=label, zorder=0)


def savefig(fig, path, **kwargs):
    """Save figure with academic defaults."""
    fig.savefig(path, dpi=300, bbox_inches='tight', pad_inches=0.03, **kwargs)
    plt.close(fig)


def set_log_ticks(ax, which='both'):
    """Set log-scale tick formatting."""
    from matplotlib.ticker import LogLocator, NullFormatter
    for axis_name in (['xaxis', 'yaxis'] if which == 'both'
                      else [f'{which}axis']):
        axis = getattr(ax, axis_name)
        axis.set_major_locator(LogLocator(base=10, numticks=12))
        axis.set_minor_locator(LogLocator(base=10, subs=np.arange(2, 10)*0.1,
                                          numticks=12))
        axis.set_minor_formatter(NullFormatter())
