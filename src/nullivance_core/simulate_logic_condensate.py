import numpy as np
import matplotlib.pyplot as plt
from scipy.special import softmax

class LogicFieldSimulation:
    def __init__(self, size=64, dim_D=3, coupling=1.0, feedback_strength=2.0):
        """
        Initialize the Logic Field lattice.
        size: grid size (size x size)
        dim_D: conceptual dimension of logic space (e.g., 3 for RGB-like logic)
        coupling: strength of neighbor interactions (J)
        feedback_strength: strength of self-feedback (alpha)
        """
        self.size = size
        self.dim_D = dim_D
        self.coupling = coupling
        self.alpha = feedback_strength
        
        # Initialize random logic vectors (theta) normalized via softmax
        self.theta = np.random.randn(size, size, dim_D)
        self.theta = softmax(self.theta, axis=2)
        
        self.history_entropy = []
        self.history_stiffness = []

    def entropy(self, p):
        """Calculate Shannon entropy of a logic vector."""
        # Add small epsilon to avoid log(0)
        p = np.clip(p, 1e-10, 1.0)
        return -np.sum(p * np.log(p), axis=2)

    def logic_stability(self, p):
        """
        Measure Logic Stability "Xi".
        Xi -> 1 means high ambiguity (flat).
        Xi -> 0 means high certainty (spiky).
        Inverse of entropy somewhat.
        Let's define Stiffness rho ~ 1 - H/H_max
        """
        H = self.entropy(p)
        H_max = np.log(self.dim_D)
        rho = 1.0 - (H / H_max)
        return np.maximum(rho, 0)

    def step(self):
        """
        Evolve the field using the Feedback Principle:
        Theta_new = Softmax( alpha * Theta_old + J * Laplacian(Theta_old) )
        """
        # Calculate Laplacian (neighbor average - self) using minimal convolution
        # For simplicity, just sum of 4 neighbors
        padded = np.pad(self.theta, ((1,1), (1,1), (0,0)), mode='wrap')
        neighbors = (padded[:-2, 1:-1] + padded[2:, 1:-1] + 
                     padded[1:-1, :-2] + padded[1:-1, 2:])
        
        laplacian = neighbors - 4 * self.theta
        
        # The "Input" signal for the next thought moment
        signal = self.alpha * self.theta + self.coupling * laplacian
        
        # Apply non-linearity (Decision Function)
        self.theta = softmax(signal, axis=2)
        
        # Record metrics
        avg_H = np.mean(self.entropy(self.theta))
        avg_rho = np.mean(self.logic_stability(self.theta))
        self.history_entropy.append(avg_H)
        self.history_stiffness.append(avg_rho)
    
    def run(self, steps=100):
        print(f"Running simulation for {steps} steps...")
        for i in range(steps):
            self.step()
            if i % 20 == 0:
                print(f"Step {i}: Avg Entropy = {self.history_entropy[-1]:.4f}, Stiffness = {self.history_stiffness[-1]:.4f}")

    def plot_results(self, output_file="logic_field_simulation.png"):
        """Visualize the emergent field."""
        rho = self.logic_stability(self.theta)
        
        # Phase is complex to visualize in 3D, let's map it to RGB color
        # Interpret the 3 components of theta as R, G, B
        img = self.theta
        
        plt.figure(figsize=(15, 5))
        
        # 1. Stiffness Map (Geometry)
        plt.subplot(1, 3, 1)
        plt.imshow(rho, cmap="viridis", vmin=0, vmax=1)
        plt.title("Emergent Geometry\n(Vacuum Stiffness $\\rho$)")
        plt.axis('off')
        
        # 2. Logic Phase Map (Matter/Topology)
        plt.subplot(1, 3, 2)
        plt.imshow(img)
        plt.title("Emergent Topology\n(Logic Phase State)")
        plt.axis('off')
        
        # 3. Evolution History
        plt.subplot(1, 3, 3)
        plt.plot(self.history_stiffness, label="System Stiffness (Order)")
        plt.plot(self.history_entropy, label="System Entropy (Chaos)", linestyle="--")
        plt.xlabel("Time Step")
        plt.title("Self-Organization Dynamics")
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=150)
        print(f"Results saved to {output_file}")

if __name__ == "__main__":
    # Parameters chosen to be near the critical point
    sim = LogicFieldSimulation(size=100, dim_D=3, coupling=1.5, feedback_strength=2.5)
    sim.run(steps=200)
    sim.plot_results("results/figures/fig_logic_condensate.png")
