import numpy as np
from scipy import stats

# Constants
ALPHA = 1/137.035999084
X_SCALE = 3 / (2 * ALPHA)
M_TAU = 1.77686  # GeV
M_STAR = M_TAU * X_SCALE # ~365.24 GeV

print(f"TRXT Constants:")
print(f"  Alpha = {ALPHA}")
print(f"  X_scale = {X_SCALE:.4f}")
print(f"  M* = {M_STAR:.4f} GeV")
print("-" * 60)

# Observed Data (PDG 2024 approx)
PARTICLES = {
    'W': {'mass': 80.379, 'sigma': 0.012, 'sector_p': 5},
    'Z': {'mass': 91.1876, 'sigma': 0.0021, 'sector_p': 8}, # Symmetric p=q assumption implies p=8.01 -> 8
    'Higgs': {'mass': 125.25, 'sigma': 0.17, 'sector_p': 5}
}

def get_q_unique(p, m_obs):
    """
    Uniquely determines q from p and m_obs.
    Formula: m = M* (1/p + 1/q)  =>  1/q = m/M* - 1/p
    """
    term = m_obs / M_STAR - 1/p
    if term <= 0: return np.inf # Physical constraint
    q_float = 1 / term
    return round(q_float), q_float

def analyze_robustness(particle_name, p, m_obs, sigma):
    q_int, q_float = get_q_unique(p, m_obs)
    
    # Check bounds where q remains constant
    # q changes if q_float crosses integer + 0.5
    # calculate mass boundaries for q_int - 0.5 and q_int + 0.5
    
    def mass_from_q(q_val):
        return M_STAR * (1/p + 1/q_val)
    
    m_lower_bound = mass_from_q(q_int + 0.5)
    m_upper_bound = mass_from_q(q_int - 0.5)
    
    stability_range = (m_lower_bound, m_upper_bound)
    sigma_dist_lower = (m_obs - m_lower_bound) / sigma
    sigma_dist_upper = (m_upper_bound - m_obs) / sigma
    
    m_pred = mass_from_q(q_int)
    error = (m_pred - m_obs) / m_obs
    
    print(f"Particle: {particle_name}")
    print(f"  Input: M_obs={m_obs} GeV, p={p}")
    print(f"  Calculated q_exact={q_float:.4f} => Rounded q={q_int}")
    print(f"  Predicted Mass: {m_pred:.4f} GeV (Error: {error*100:.4f}%)")
    print(f"  Stability Range: [{m_lower_bound:.4f}, {m_upper_bound:.4f}] GeV")
    print(f"  Robustness in Sigma: Stable within [-{sigma_dist_lower:.1f}σ, +{sigma_dist_upper:.1f}σ]")
    
    return q_int

# 1. Main Analysis
print("1. MODE ASSIGNMENT & ROBUSTNESS")
for name, data in PARTICLES.items():
    analyze_robustness(name, data['sector_p'], data['mass'], data['sigma'])
    print("-" * 20)


# 2. Null Model Analysis
modes = []
for p in range(1, 101):
    for q in range(p, 101):
        m = M_STAR * (1/p + 1/q)
        if 50 <= m <= 200:
            modes.append(m)
modes.sort()
modes = np.array(modes)
w_neighborhood = modes[(modes > 75) & (modes < 85)]

output_log = "robustness_report.txt"
with open(output_log, "w") as f:
    # 1. Main Analysis
    f.write("1. MODE ASSIGNMENT & ROBUSTNESS\n")
    for name, data in PARTICLES.items():
        q_int = analyze_robustness(name, data['sector_p'], data['mass'], data['sigma'])
        q_float = 1 / (data['mass'] / M_STAR - 1/data['sector_p'])
        m_lower = M_STAR * (1/data['sector_p'] + 1/(q_int+0.5))
        m_upper = M_STAR * (1/data['sector_p'] + 1/(q_int-0.5))
        f.write(f"Particle: {name}\n")
        f.write(f"  Stability Range: [{m_lower:.4f}, {m_upper:.4f}] GeV\n")
        f.write("-" * 20 + "\n")

    # 2. Null Model
    f.write("\n2. NULL MODEL STATS\n")
    f.write(f"Total modes in [50, 200] GeV: {len(modes)}\n")
    local_gap = np.mean(np.diff(w_neighborhood))
    prob_chance = (0.08 * 2) / local_gap
    f.write(f"Local gap near 80 GeV: {local_gap:.4f} GeV\n")
    f.write(f"Chance of random match (0.1%): {prob_chance:.2%}\n")

