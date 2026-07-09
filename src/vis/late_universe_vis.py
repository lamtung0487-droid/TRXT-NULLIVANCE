"""
TRXT LATE UNIVERSE EXPERIMENTAL VISUALIZATIONS
==============================================
Generates detailed snapshots of the universe's evolution:
Matter Formation -> Atoms -> Stars -> Galaxies.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Wedge
import matplotlib.cm as cm
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / "results" / "late_universe"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Set style
plt.rcParams['figure.facecolor'] = 'black'
plt.rcParams['axes.facecolor'] = 'black'
plt.rcParams['text.color'] = 'white'

def create_snapshot(filename, time_label, title, description, details, render_func):
    """Generic function to create a universe snapshot."""
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_facecolor('black')
    
    # Render specific content
    render_func(ax)
    
    # Boundary/Context (Scanning view)
    ax.add_patch(Circle((0, 0), 0.95, fill=False, edgecolor='white', linestyle=':', alpha=0.3))

    # Text annotations
    ax.text(0, 0.9, time_label, ha='center', fontsize=16, fontweight='bold', color='#ffcc00')
    ax.text(0, 0.82, title, ha='center', fontsize=20, fontweight='bold', color='white')
    
    # Description box
    rect = FancyBboxPatch((-0.9, -1.05), 1.8, 0.35, boxstyle="round,pad=0.05", 
                         facecolor='#222222', edgecolor='gray', alpha=0.9)
    ax.add_patch(rect)
    
    desc_text = f"{description}\n\n{details}"
    ax.text(0, -0.87, desc_text, ha='center', va='center', fontsize=11, wrap=True)

    ax.set_xlim(-1, 1)
    ax.set_ylim(-1.1, 1.1)
    ax.axis('off')
    
    plt.tight_layout()
    output_path = OUTPUT_DIR / filename
    fig.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='black')
    print(f"Saved: {output_path.name}")
    plt.close(fig)

def draw_hadronization(ax):
    """Draw quarks combining into protons/neutrons."""
    # Background: cooling plasma
    ax.set_facecolor('#1a0500') 
    
    np.random.seed(42)
    # Draw confinement process
    for _ in range(15):
        cx, cy = np.random.uniform(-0.6, 0.6, 2)
        
        # Proton (uud)
        u1_pos = (cx, cy+0.05)
        u2_pos = (cx-0.04, cy-0.03)
        d_pos  = (cx+0.04, cy-0.03)
        
        # Gluon strings
        ax.plot([u1_pos[0], u2_pos[0]], [u1_pos[1], u2_pos[1]], 'w-', alpha=0.5, linewidth=1)
        ax.plot([u2_pos[0], d_pos[0]], [u2_pos[1], d_pos[1]], 'w-', alpha=0.5, linewidth=1)
        ax.plot([d_pos[0], u1_pos[0]], [d_pos[1], u1_pos[1]], 'w-', alpha=0.5, linewidth=1)
        
        # Quarks
        ax.scatter(*u1_pos, c='red', s=40, zorder=10, label='u')
        ax.scatter(*u2_pos, c='red', s=40, zorder=10)
        ax.scatter(*d_pos, c='blue', s=40, zorder=10, label='d')
        
        # Confinement bubble
        circle = Circle((cx, cy), 0.08, color='white', alpha=0.1)
        ax.add_patch(circle)

    ax.text(0, 0, "Quark Confinement\nStrong Force takes over", ha='center', color='orange', alpha=0.5, fontsize=20, rotation=30)

def draw_nucleosynthesis(ax):
    """Draw protons and neutrons fusing."""
    # Background: hot orange
    ax.set_facecolor('#331100')
    
    np.random.seed(10)
    # Draw Deuterium (p+n) and Helium (2p+2n)
    positions = np.random.uniform(-0.7, 0.7, (10, 2))
    
    for i, (cx, cy) in enumerate(positions):
        if i < 7: # Hydrogen (Singular protons)
            ax.scatter(cx, cy, c='red', s=60, edgecolors='white')
            ax.text(cx+0.02, cy+0.02, "¹H", fontsize=8, color='white')
        else: # Helium-4 (2p 2n)
            # 2 protons
            ax.scatter(cx-0.02, cy, c='red', s=60, edgecolors='white')
            ax.scatter(cx+0.02, cy, c='red', s=60, edgecolors='white')
            # 2 neutrons
            ax.scatter(cx, cy+0.03, c='gray', s=60, edgecolors='white')
            ax.scatter(cx, cy-0.03, c='gray', s=60, edgecolors='white')
            
            circle = Circle((cx, cy), 0.08, color='yellow', alpha=0.2)
            ax.add_patch(circle)
            ax.text(cx+0.05, cy+0.05, "⁴He", fontsize=10, color='yellow', fontweight='bold')
            
    ax.arrow(-0.4, -0.4, 0.2, 0.2, head_width=0.03, color='white')
    ax.text(-0.3, -0.3, "Fusion", color='white')

def draw_recombination(ax):
    """Draw atoms forming and light escaping."""
    # Background: fading to black
    ax.set_facecolor('#000022')
    
    np.random.seed(55)
    # Atoms (nucleus + electron orbit)
    for _ in range(20):
        # Nucleus
        cx, cy = np.random.uniform(-0.8, 0.8, 2)
        ax.scatter(cx, cy, c='red', s=30) 
        
        # Electron orbit
        orbit = Circle((cx, cy), 0.04, color='cyan', fill=False, alpha=0.5)
        ax.add_patch(orbit)
        # Electron
        angle = np.random.rand() * 2 * np.pi
        ex = cx + 0.04 * np.cos(angle)
        ey = cy + 0.04 * np.sin(angle)
        ax.scatter(ex, ey, c='cyan', s=10)
    
    # CMB Photons (Straight lines now!)
    for _ in range(30):
        x1, y1 = np.random.uniform(-0.9, 0.9, 2)
        angle = np.random.rand() * 2 * np.pi
        length = 0.3
        x2 = x1 + length * np.cos(angle)
        y2 = y1 + length * np.sin(angle)
        
        ax.plot([x1, x2], [y1, y2], color='gold', alpha=0.6, linewidth=1)
        
    ax.text(0, 0, "UNIVERSE BECOMES TRANSPARENT\nCMB RELEASED", ha='center', color='gold', alpha=0.3, fontsize=16, fontweight='bold')

def draw_cosmic_web(ax):
    """Draw galaxy formation and cosmic web."""
    # Background: deep space
    ax.set_facecolor('black')
    
    np.random.seed(99)
    # Filamentary structure (using random walk or noise approx)
    x = np.random.uniform(-1, 1, 1000)
    y = np.random.uniform(-1, 1, 1000)
    
    # Create simple clustering
    from scipy.spatial import cKDTree
    tree = cKDTree(np.c_[x, y])
    pairs = tree.query_pairs(r=0.15)
    
    for i, j in pairs:
        ax.plot([x[i], x[j]], [y[i], y[j]], c='purple', alpha=0.1, linewidth=0.5)
        
    # Galaxies at nodes
    for i in range(len(x)):
        neighbors = len(tree.query_ball_point([x[i], y[i]], 0.15))
        if neighbors > 5:
            size = neighbors * 2
            color = cm.viridis(neighbors/20)
            ax.scatter(x[i], y[i], s=size, color=color, alpha=0.8)
            
            # Spiral arms for big ones
            if neighbors > 12:
                # Simple spiral hint
                theta = np.linspace(0, 2*np.pi, 20)
                r = np.linspace(0, 0.02, 20)
                dx = r * np.cos(theta)
                dy = r * np.sin(theta)
                ax.plot(x[i]+dx, y[i]+dy, color='white', alpha=0.5)
                ax.plot(x[i]-dx, y[i]-dy, color='white', alpha=0.5)

def main():
    print("Generating Late Universe Snapshots...")

    # 6. T ~ 10^-6 s: HADRONIZATION
    create_snapshot(
        filename='06_hadron_epoch.png',
        time_label='Time: t ~ 10⁻⁶ s (Hadron Epoch)',
        title='CONFINEMENT (GIAM HÃM QUARK)',
        description='Vũ trụ nguội đi, Quarks không thể tự do.',
        details='Lực mạnh (Strong Force) trở nên áp đảo. \nQuark kết hợp thành Proton (uud) và Neutron (udd). \nKeo hồ Gluon giữ chặt chúng lại.',
        render_func=draw_hadronization
    )

    # 7. T ~ 3 min: NUCLEOSYNTHESIS
    create_snapshot(
        filename='07_nucleosynthesis.png',
        time_label='Time: t ~ 3 phút (Nucleosynthesis)',
        title='PRIMORDIAL FUSION (TỔNG HỢP HẠT NHÂN)',
        description='Lò phản ứng hạt nhân vũ trụ hoạt động.',
        details='Proton và Neutron va chạm tạo thành hạt nhân đầu tiên: Deuterium, Helium-4, Lithium-7. \nTỷ lệ H:He được cố định ở mức 75%:25%.',
        render_func=draw_nucleosynthesis
    )

    # 8. T ~ 380,000 nam: RECOMBINATION
    create_snapshot(
        filename='08_recombination.png',
        time_label='Time: t ~ 380,000 năm',
        title='FIRST LIGHT (ÁNH SÁNG ĐẦU TIÊN)',
        description='Electron bị hạt nhân bắt giữ. Nguyên tử hình thành.',
        details='Vũ trụ trở nên trung hòa về điện.\nPhoton không còn bị tán xạ liên tục, chúng thoát ra tự do -> CMB (Bức xạ nền vi sóng) ra đời.',
        render_func=draw_recombination
    )

    # 9. T ~ 100M - 13.8B nam: STRUCTURE
    create_snapshot(
        filename='09_structure_formation.png',
        time_label='Time: 100 triệu - 13.8 tỷ năm',
        title='COSMIC WEB & GALAXIES (MẠNG LƯỚI VŨ TRỤ)',
        description='Trọng lực và Vật chất tối kiến tạo cấu trúc.',
        details='Vật chất tối (Dark Tower) tụ lại thành các Halo.\nKhí gas rơi vào giếng thế hấp dẫn này, tạo thành các thiên hà xoắn ốc và các cụm thiên hà dọc theo mạng lưới vũ trụ.',
        render_func=draw_cosmic_web
    )

if __name__ == "__main__":
    main()
