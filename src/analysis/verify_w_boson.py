import numpy as np

# Constants
alpha = 1/137.035999084
m_tau = 1.77686 # GeV
M_star = m_tau * 3 / (2 * alpha)
print(f"M_star calculated: {M_star:.4f} GeV")

# Experimental Values (PDG 2022)
M_Z_exp = 91.1876
M_W_exp = 80.379
M_H_exp = 125.25

# TRXT Predictions
def m_trxt(p, q):
    return M_star * (1/p + 1/q)

# Check Higgs (5, 7)
m_H = m_trxt(5, 7)
print(f"Higgs (5, 7): {m_H:.4f} GeV (Exp: {M_H_exp}) Error: {m_H - M_H_exp:.4f}")

# Check Z (8, 8)
m_Z = m_trxt(8, 8)
print(f"Z (8, 8): {m_Z:.4f} GeV (Exp: {M_Z_exp}) Error: {m_Z - M_Z_exp:.4f}")

# Check W (5, 50) - The contention point
m_W = m_trxt(5, 50)
print(f"W (5, 50): {m_W:.4f} GeV (Exp: {M_W_exp}) Error: {m_W - M_W_exp:.4f}")

# Calculate Derived Weinberg Angle
cos_theta_trxt = m_W / m_Z
cos_theta_exp = M_W_exp / M_Z_exp
print(f"Predicted cos(theta_W): {cos_theta_trxt:.5f} (22/25)")
print(f"Experimental cos(theta_W): {cos_theta_exp:.5f}")

# Check other integers for W
print("\nScanning for other integers near W mass:")
min_diff = 10.0
best_pair = (0,0)
for p in range(1, 20):
    for q in range(p, 100):
        m = m_trxt(p, q)
        diff = abs(m - M_W_exp)
        if diff < 1.0:
            print(f"Match: ({p}, {q}) -> {m:.4f} GeV (Diff: {diff:.4f})")
            if diff < min_diff:
                min_diff = diff
                best_pair = (p, q)
