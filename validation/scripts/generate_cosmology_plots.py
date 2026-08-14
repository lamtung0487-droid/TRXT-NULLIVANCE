import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# Set scientific style
plt.style.use('default')
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 12,
    'axes.grid': True,
    'grid.alpha': 0.3
})

def plot_phase_transition():
    """
    Figure 3.0: Symmetry Breaking Phase Transition
    Plots V(Phi, T) = D(T^2 - Tc^2)Phi^2 + lambda Phi^4
    """
    print("Generating Figure 3.0: Phase Transition Potential...")
    
    phi = np.linspace(-400, 400, 1000)
    mu_0 = 365.24  # GeV
    lam = 0.5
    
    # Temperature dependent mass term: mu^2(T) = mu_0^2 * (1 - T^2/Tc^2)
    # Effective Potential: V = -mu^2(T)*phi^2 + lambda*phi^4
    # High T: +mu^2 * phi^2 (Restored)
    # Low T: -mu^2 * phi^2 (Broken)
    
    temps = [1.2, 1.0, 0.8, 0.0] # T/Tc ratios
    colors = cm.coolwarm(np.linspace(0.9, 0.1, len(temps)))
    
    plt.figure(figsize=(10, 6))
    
    for i, t_ratio in enumerate(temps):
        if t_ratio > 1.0:
            # Symmetry Restored: Positive mass term
            # V = +alpha * phi^2
            coef = 2.0 * (t_ratio - 1.0) * mu_0**2 # toy model coefficient
            V = 0.5 * coef * phi**2 + lam * phi**4
            label = f'T = {t_ratio} $T_c$ (Restored)'
            style = '--'
        elif t_ratio == 1.0:
            V = lam * phi**4
            label = f'T = $T_c$ (Critical)'
            style = '-.'
        else:
            # Symmetry Broken: Negative mass term
            # V = -mu^2 * phi^2
            coef = mu_0**2 * (1.0 - t_ratio**2)
            V = -0.5 * coef * phi**2 + lam * phi**4
            label = f'T = {t_ratio} $T_c$ (Broken)'
            style = '-'
            
        plt.plot(phi, V / 1e9, color=colors[i], linestyle=style, linewidth=2, label=label)

    plt.title(r'TRXT Phase Transition: The "Big Condensation"', fontsize=14)
    plt.xlabel(r'Order Parameter $\Phi$ (GeV)', fontsize=12)
    plt.ylabel(r'Effective Potential $V_{eff}$ ($10^9$ GeV$^4$)', fontsize=12)
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    
    # Annotations
    plt.text(0, 10, 'Logic Void (Layer 0)', ha='center', va='bottom', fontsize=10, bbox=dict(facecolor='white', alpha=0.8))
    plt.annotate('Spacetime Vacuum', xy=(260, -8), xytext=(300, 5),
                 arrowprops=dict(facecolor='black', shrink=0.05))
    
    plt.legend()
    plt.tight_layout()
    plt.savefig('results/figures/fig_3_0_phase_transition.png', dpi=300)
    print("Saved fig_3_0_phase_transition.png")

def plot_fractal_sound_speed():
    """
    Figure 3.1: Sound Speed vs Lagrangian Power
    Plots c_s^2 = 1 / (2n - 1)
    """
    print("Generating Figure 3.1: Fractal Sound Speed...")
    
    n = np.linspace(1.1, 4.0, 500)
    cs2 = 1.0 / (2*n - 1)
    
    plt.figure(figsize=(10, 6))
    plt.plot(n, cs2, 'b-', linewidth=3, label=r'Sound Speed $c_s^2 = \frac{1}{2n-1}$')
    
    # Critical Points
    points = [
        (2.0, 1.0/3.0, 'Standard EFT (n=2)\n$c_s^2=1/3$ (Radiation)'),
        (3.0, 1.0/5.0, 'Logic Triplet (n=3)\n$c_s^2=0.2$'),
        (2.5, 1.0/4.0, 'TRXT Fractal (n=2.5)\n$c_s^2=0.25 (H_0=73)$')
    ]
    
    colors = ['gray', 'green', 'red']
    
    for i, (nx, cy, label) in enumerate(points):
        plt.plot(nx, cy, 'o', color=colors[i], markersize=10, zorder=5)
        plt.annotate(label, xy=(nx, cy), xytext=(nx+0.1, cy+0.1),
                     arrowprops=dict(facecolor=colors[i], shrink=0.05), fontsize=10)
        
        # Drop lines
        plt.plot([nx, nx], [0, cy], '--', color=colors[i], alpha=0.5)
        plt.plot([1, nx], [cy, cy], '--', color=colors[i], alpha=0.5)

    # Shaded region for Hubble Tension Resolution
    # H0=73 requirement corresponds to cs^2 approx 0.25
    plt.fill_between(n, cs2, where=((n>=2.4) & (n<=2.6)), color='red', alpha=0.1, label='Hubble Solution Zone')

    plt.title(r'Resolution of Hubble Tension via Fractal Dynamics', fontsize=14)
    plt.xlabel(r'Lagrangian Kinetic Power $n$ ($P(X) \sim X^n$)', fontsize=12)
    plt.ylabel(r'Sound Speed Squared $c_s^2/c^2$', fontsize=12)
    plt.xlim(1.5, 3.5)
    plt.ylim(0.0, 0.6)
    
    plt.legend()
    plt.tight_layout()
    plt.savefig('results/figures/fig_3_1_fractal_sound_speed.png', dpi=300)
    print("Saved fig_3_1_fractal_sound_speed.png")

if __name__ == "__main__":
    plot_phase_transition()
    plot_fractal_sound_speed()
