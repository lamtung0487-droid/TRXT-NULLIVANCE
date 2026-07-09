"""
TRXT EARLY UNIVERSE DETAILED VISUALIZATIONS
===========================================
Generates detailed snapshots of the universe's first moments.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Arrow
import matplotlib.patheffects as pe
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / "results" / "early_universe"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Set style
plt.rcParams['figure.facecolor'] = 'black'
plt.rcParams['axes.facecolor'] = 'black'
plt.rcParams['text.color'] = 'white'
plt.rcParams['axes.labelcolor'] = 'white'
plt.rcParams['xtick.color'] = 'white'
plt.rcParams['ytick.color'] = 'white'

def create_snapshot(filename, time_label, title, description, details, particles, color_theme):
    """Generic function to create a universe snapshot."""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Background
    ax.set_facecolor('black')
    
    # Draw "Universe" boundary (expanding)
    r_uni = 0.8
    if 'foam' in filename:
        # Irregular boundary for quantum foam
        theta = np.linspace(0, 2*np.pi, 200)
        r = r_uni + 0.05 * np.sin(10*theta) * np.cos(5*theta)
        x, y = r * np.cos(theta), r * np.sin(theta)
        ax.plot(x, y, color=color_theme, alpha=0.3, linestyle='--')
        ax.fill(x, y, color=color_theme, alpha=0.1)
    else:
        # Smooth boundary
        uni = Circle((0, 0), r_uni, color=color_theme, alpha=0.1)
        ax.add_patch(uni)
        ax.add_patch(Circle((0, 0), r_uni, fill=False, edgecolor=color_theme, linestyle='--', alpha=0.5))

    # Draw particles/features
    np.random.seed(42)  # Fixed seed for reproducibility
    for p_type, count, p_color, p_size, p_marker in particles:
        for _ in range(count):
            r = np.sqrt(np.random.rand()) * r_uni * 0.9
            theta = np.random.rand() * 2 * np.pi
            x, y = r * np.cos(theta), r * np.sin(theta)
            
            if p_marker == 'twist':
                # Draw small spirals (vortices)
                t = np.linspace(0, 4*np.pi, 20)
                dx = 0.02 * t/max(t) * np.cos(t)
                dy = 0.02 * t/max(t) * np.sin(t)
                ax.plot(x+dx, y+dy, color=p_color, linewidth=1, alpha=0.8)
            elif p_marker == 'wave':
                # Draw small waves
                wx = np.linspace(-0.03, 0.03, 10)
                wy = 0.01 * np.sin(50*wx)
                ax.plot(x+wx, y+wy, color=p_color, linewidth=1, alpha=0.8)
            else:
                ax.scatter(x, y, s=p_size, c=p_color, marker=p_marker, alpha=0.8, edgecolors='none')

    # Add text annotations
    ax.text(0, 0.95, time_label, ha='center', fontsize=16, fontweight='bold', color='#ffcc00')
    ax.text(0, 0.88, title, ha='center', fontsize=20, fontweight='bold', color='white')
    
    # Description box
    rect = FancyBboxPatch((-0.9, -1.0), 1.8, 0.3, boxstyle="round,pad=0.05", 
                         facecolor='#222222', edgecolor='gray', alpha=0.9)
    ax.add_patch(rect)
    
    desc_text = f"{description}\n\n{details}"
    ax.text(0, -0.85, desc_text, ha='center', va='center', fontsize=12, wrap=True)

    ax.set_xlim(-1, 1)
    ax.set_ylim(-1.1, 1.1)
    ax.axis('off')
    
    plt.tight_layout()
    output_path = OUTPUT_DIR / filename
    fig.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='black')
    print(f"Saved: {output_path.name}")
    plt.close(fig)

def main():
    print("Generating Early Universe Snapshots...")

    # 1. T < 0: QUANTUM FOAM
    create_snapshot(
        filename='01_quantum_foam.png',
        time_label='Time: Undefined (t < 10⁻⁴³ s)',
        title='QUANTUM FOAM (BỌT LƯỢNG TỬ)',
        description='Trạng thái hỗn loạn tôpô. Chưa có không gian, chưa có thời gian.',
        details='Không-thời gian bị xé rách liên tục. Các lỗ sâu (wormholes) xuất hiện và biến mất. \nMetric g_uv không xác định.',
        particles=[
            ('wormhole', 30, 'cyan', 100, 'o'),  # Holes
            ('fluctuation', 50, 'magenta', 50, 'o'), # Abstract dots for fluctuations
        ],
        color_theme='purple'
    )

    # 2. T ~ 10^-43s: FERMION SEA
    create_snapshot(
        filename='02_fermion_sea.png',
        time_label='Time: t ~ 10⁻⁴³ s (Planck Era)',
        title='PLANCKIAN FERMION SEA (BIỂN FERMION)',
        description='Các hạt Fermion Chiral (Ψ) xuất hiện. Chưa có khối lượng.',
        details='Vũ trụ là một biển các hạt spin-1/2 tự do. \nChưa có liên kết. Chưa có trọng lực.',
        particles=[
            ('fermion', 100, '#00ff00', 30, '^'), # Green triangles for chiral fermions
        ],
        color_theme='green'
    )

    # 3. T ~ 10^-36s: CONDENSATION
    create_snapshot(
        filename='03_condensation.png',
        time_label='Time: t ~ 10⁻³⁶ s (GUT Era)',
        title='NJL CONDENSATION (NGƯNG TỤ)',
        description='Sự kiện quan trọng nhất: Cooper Pairing <ΨΨ> ≠ 0',
        details='Các Fermion kết cặp với nhau. \nTrọng lực (Gravity) xuất hiện từ độ cứng của condensate. \nKhông-thời gian thành hình.',
        particles=[
            ('pair', 80, 'gold', 60, '8'),   # Pairs looking like 8
            ('glue', 40, 'yellow', 10, '.'), # Background glow
        ],
        color_theme='gold'
    )

    # 4. T ~ 10^-32s: INFLATION
    create_snapshot(
        filename='04_inflation.png',
        time_label='Time: t ~ 10⁻³² s',
        title='SUPERFLUID INFLATION (LẠM PHÁT)',
        description='Vũ trụ giãn nở khủng khiếp (e⁶⁰ lần).',
        details='Năng lượng ngưng tụ giải phóng đẩy vũ trụ giãn ra. \nCác biến động lượng tử bị kéo giãn thành cấu trúc vĩ mô.',
        particles=[
            ('pair', 20, 'gold', 30, '8'),   # Diluted pairs
            ('wave', 50, 'white', 1, 'wave'), # Stretch marks/waves
        ],
        color_theme='red'
    )

    # 5. T ~ 10^-12s: SEPARATION OF FORCES
    create_snapshot(
        filename='05_separation.png',
        time_label='Time: t ~ 10⁻¹² s (Electroweak)',
        title='GENERATION OF MASS (TẠO KHỐI LƯỢNG)',
        description='Các hạt nhận khối lượng. 4 lực tách rời.',
        details='W, Z bosons trở nên nặng. Photon vẫn không khối lượng. \nCác xoáy (vortices) hình thành vật chất (quark, lepton).',
        particles=[
            ('matter', 30, 'blue', 50, 'o'),   # Massive particles
            ('light', 50, 'yellow', 1, 'wave'), # Photons
            ('higgs', 20, 'red', 40, '*'),     # Higgs mechanism active
        ],
        color_theme='blue'
    )

if __name__ == "__main__":
    main()
