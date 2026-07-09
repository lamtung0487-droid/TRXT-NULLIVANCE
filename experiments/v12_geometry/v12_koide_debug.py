import numpy as np

# ACTUAL MASSES
m_real = np.array([0.510998, 105.658, 1776.86])

# Derive the exact Koide parameters from the real masses
sqrt_m = np.sqrt(m_real) 
# We need to find M_0, b_mag, and phase
# M_0 = (sqrt_m1 + sqrt_m2 + sqrt_m3) / 3
M_0_sqrt = np.sum(sqrt_m) / 3.0
M_0 = M_0_sqrt**2

print(f"Empirical M_0 = {M_0:.6f} MeV")

# The eigenvalues are sqrt(m_n) = M_0_sqrt * (1 + sqrt(2) * cos(theta_n))
# So cos(theta_n) = (sqrt(m_n)/M_0_sqrt - 1) / sqrt(2)

cos_theta = (sqrt_m / M_0_sqrt - 1.0) / np.sqrt(2)

print(f"cos(theta) values: {cos_theta}")

theta_empirical = np.arccos(cos_theta)
print(f"Theta values (rad): {theta_empirical}")
# Convert to degrees
print(f"Theta values (deg): {np.degrees(theta_empirical)}")

# Test the relation: are they separated by 120 degrees?
# Let's check theta_2 - theta_1, etc.
# Note: arccos returns [0, pi]
# The values in degrees are roughly: 
# e: arccos(-0.68) ~ 133 deg, mu: arccos(-0.19) ~ 101 deg, tau: arccos(+0.87) ~ 29 deg
# This means:
# theta_tau = 29.5 deg
# theta_mu = 101.5 deg = 29.5 + 72? No.
# Actually, the cosine argument can be negative or positive.
# For mu: cos = -0.196. This could be 180 - 101.5 = 78.5? No, cos is negative in Q2 and Q3.
# So theta_mu could be 101.5 deg or 360 - 101.5 = 258.5 deg.
# For e: cos = -0.68. theta_e could be 133.2 deg or 360 - 133.2 = 226.8 deg.
# Let's test the separations:
# 258.5 - 29.5 = 229 deg
# 133.2 - 29.5 = 103.7 deg ? Wait, 133.2 - 29.5 isn't 120.
# Ah, the Koide sequence has separation of 2/3 pi = 120 degrees.
# Let's check:
# 29.5 deg
# 29.5 + 120 = 149.5 deg. cos(149.5) = -0.86.  For e, cos is -0.68.
# 29.5 + 240 = 269.5 deg. cos(269.5) = -0.008. For mu, cos is -0.19.

# Brannen defines it with a phase delta = 2/9.
delta = 2.0 / 9.0  # radians
print(f"\nBrannen delta = {delta:.6f} radians ({np.degrees(delta):.2f} degrees)")

# Let's generate masses with delta = 2/9
m_pred = np.zeros(3)
for n in range(3):
    m_pred[n] = M_0 * (1.0 + np.sqrt(2) * np.cos(delta + 2.0*np.pi * n / 3.0))**2

m_pred.sort()
print(f"Predicted Masses from delta=2/9 rad: {m_pred}")

# Let's find the optimal phase that EXACTLY fits e, mu, tau
def objective(phase):
    # Sum of square errors of predicted mass logs
    m_p = [M_0 * (1.0 + np.sqrt(2) * np.cos(phase + 2.0*np.pi * n / 3.0))**2 for n in range(3)]
    m_p.sort()
    return sum((np.log(m_p[i]) - np.log(m_real[i]))**2 for i in range(3))

from scipy.optimize import minimize
res = minimize(objective, 0.2)
opt_phase = res.x[0]

print(f"\nOptimal phase: {opt_phase:.6f} rad ({np.degrees(opt_phase):.6f} degrees)")

m_opt = [M_0 * (1.0 + np.sqrt(2) * np.cos(opt_phase + 2.0*np.pi * n / 3.0))**2 for n in range(3)]
m_opt.sort()
print(f"Masses at optimal phase: {m_opt}")
