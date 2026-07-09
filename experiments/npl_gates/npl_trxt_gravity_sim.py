import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft2, ifft2

# ==============================================================================
# TRXT-NPL V10: LOGIC TENSION -> GRAVITY EMERGENCE SIMULATION
# Implements: Master Protocol V2.0 (Strict PDE Mandate, Anti-Patching)
# ==============================================================================

# Constants and Setup
N = 256  # Grid size
L = 100.0  # Physical size
dx = L / N
x = np.linspace(-L/2, L/2, N, endpoint=False)
y = np.linspace(-L/2, L/2, N, endpoint=False)
X, Y = np.meshgrid(x, y)

k_logic = 1.0  # Coupling constant for logic tension

# 1. Initialize NPL Tensor Field (alpha, Theta)
# Two distinct "Concepts" (Pre-fermions / Topological Defects)
pos1 = np.array([-15.0, 0.0])
pos2 = np.array([15.0, 0.0])
sigma = 3.0

# Existence Density (alpha)
alpha1 = np.exp(-((X - pos1[0])**2 + (Y - pos1[1])**2) / (2 * sigma**2))
alpha2 = np.exp(-((X - pos2[0])**2 + (Y - pos2[1])**2) / (2 * sigma**2))
alpha_total = alpha1 + alpha2 + 1e-4  # Background alpha to avoid div by zero

# Phase Tensor (Theta)
# Represents contradictory logical states (Phase 1 vs Phase -1)
Theta1 = 1.0
Theta2 = -1.0
# Smooth phase transition between the two peaks
Theta_field = (alpha1 * Theta1 + alpha2 * Theta2) / alpha_total

# 2. Compute Logic Tension (c_alpha)
# c_alpha corresponds to superfluid kinetic energy X = (\partial \Phi)^2
grad_Theta_x, grad_Theta_y = np.gradient(Theta_field, dx, dx)
grad_Theta_sq = grad_Theta_x**2 + grad_Theta_y**2

# Sức căng mâu thuẫn: c_alpha = alpha * |nabla Theta|^2
c_alpha = alpha_total * grad_Theta_sq

# 3. Solve Global PDE for Gravity (Master Protocol Article II.1)
# Equation: \nabla^2 \Phi_grav = 4\pi k c_alpha
# Using FFT solver for Periodic Boundary Conditions
source = 4 * np.pi * k_logic * c_alpha
source_hat = fft2(source)

# K-space frequencies
kx = np.fft.fftfreq(N, d=dx) * 2 * np.pi
ky = np.fft.fftfreq(N, d=dx) * 2 * np.pi
KX, KY = np.meshgrid(kx, ky)
K_sq = KX**2 + KY**2
K_sq[0, 0] = 1.0  # Avoid division by zero at DC component

Phi_hat = -source_hat / K_sq
Phi_hat[0, 0] = 0.0  # Zero mean potential
Phi_grav = np.real(ifft2(Phi_hat))

# 4. Compute Gravitational Field (g)
# np.gradient returns (axis0, axis1) = (y, x)
g_y, g_x = np.gradient(-Phi_grav, dx, dx)

# Effective Density modification (NPL Rules)
# g = - (1/rho_eff) \nabla \Phi_grav
# For pure vector verification, we look at the raw acceleration force vector
g_field_x = g_x
g_field_y = g_y

# Force measured at the centers
# Interpolate or just take nearest pixel
idx1_x = int((pos1[0] + L/2) / dx)
idx1_y = int((pos1[1] + L/2) / dx)
idx2_x = int((pos2[0] + L/2) / dx)
idx2_y = int((pos2[1] + L/2) / dx)

force_on_1 = np.array([g_field_x[idx1_y, idx1_x], g_field_y[idx1_y, idx1_x]])
force_on_2 = np.array([g_field_x[idx2_y, idx2_x], g_field_y[idx2_y, idx2_x]])

print(f"Force acting on Peak 1 (Left): Fx = {force_on_1[0]:.4f}, Fy = {force_on_1[1]:.4f}")
print(f"Force acting on Peak 2 (Right): Fx = {force_on_2[0]:.4f}, Fy = {force_on_2[1]:.4f}")

if force_on_1[0] > 0 and force_on_2[0] < 0:
    print("VERDICT: Attractive Gravity Emerged! (G0 PASS)")
else:
    print("VERDICT: Repulsion or Error! (FAIL)")

# 5. Visualization
plt.figure(figsize=(15, 5))

plt.subplot(131)
plt.title("NPL Existence & Phase Mismatch")
plt.imshow(Theta_field, origin='lower', extent=[-L/2, L/2, -L/2, L/2], cmap='coolwarm', alpha=0.8)
plt.contour(X, Y, alpha_total, levels=[0.1, 0.5, 0.9], colors='black', alpha=0.5)
plt.xlabel('x'); plt.ylabel('y')

plt.subplot(132)
plt.title("Logic Tension $c_\\alpha$ (Source of Gravity)")
plt.imshow(c_alpha, origin='lower', extent=[-L/2, L/2, -L/2, L/2], cmap='inferno')
plt.colorbar(fraction=0.046, pad=0.04)
plt.xlabel('x'); plt.ylabel('y')

plt.subplot(133)
plt.title("Emergent Gravitational Field $-\\nabla \\Phi$")
plt.imshow(Phi_grav, origin='lower', extent=[-L/2, L/2, -L/2, L/2], cmap='viridis', alpha=0.5)
skip = 8
plt.quiver(X[::skip, ::skip], Y[::skip, ::skip], 
           g_field_x[::skip, ::skip], g_field_y[::skip, ::skip], 
           color='white', scale=50)
plt.scatter([pos1[0], pos2[0]], [pos1[1], pos2[1]], color='red', marker='x', s=100)
plt.xlabel('x'); plt.ylabel('y')

plt.tight_layout()
plt.savefig("npl_trxt_gravity_emergence.png", dpi=300)
print("Simulation saved to npl_trxt_gravity_emergence.png")
