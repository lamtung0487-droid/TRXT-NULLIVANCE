"""
Nullivance Layer 0: The Core Engine
===================================
Implementation of the Discrete Nonlinear Sigma Model (NLSM) kernel.
This class provides the fundamental substrate for all emergent physics in the project.

Theory:
Psi_{t+1} = Normalize( (1-alpha)*Psi_t + alpha*Mean(Neighbors) )
"""

import numpy as np

class SimEngine:
    """
    The Core Engine of Nullivance.
    
    Attributes:
        size (int): Grid size (NxN).
        dim (int): Vector dimension of the field (default 3 for O(3)).
        alpha (float): Coupling constant / Time step.
        nodes (ndarray): The O(n) field state.
    """
    def __init__(self, size=128, seed=42, alpha=0.1):
        self.nx = size
        self.ny = size
        self.rng = np.random.RandomState(seed)
        self.alpha = alpha
        self.dim = 3
        
        # Init Vacuum with tiny random fluctuations
        # Corresponds to a "Hot Start" or "Perturbed Vacuum"
        self.nodes = np.zeros((self.ny, self.nx, self.dim))
        self.nodes[:, :, 0] = 1.0  # Polarize along Z
        self.nodes += 0.01 * self.rng.randn(self.ny, self.nx, self.dim)
        self.normalize()
        
    def normalize(self):
        """
        Enforce the Non-linear Constraint: |Psi| = 1.
        This projection is what makes the model a 'Submanifold' evolution (Sigma Model).
        """
        norms = np.linalg.norm(self.nodes, axis=2, keepdims=True)
        self.nodes /= (norms + 1e-9)
        
    def step(self):
        """
        Execute one Consensus Step.
        Roughly equivalent to heat equation diffusion on a sphere.
        """
        # 1. Topological Consensus (Gather Neighbor Info)
        n_up = np.roll(self.nodes, 1, axis=0)
        n_down = np.roll(self.nodes, -1, axis=0)
        n_left = np.roll(self.nodes, 1, axis=1)
        n_right = np.roll(self.nodes, -1, axis=1)
        neighbor_sum = n_up + n_down + n_left + n_right
        
        # 2. Relaxational Dynamics (Move towards mean)
        # alpha acts as dt * DiffusionCoefficient
        self.nodes = (1 - self.alpha) * self.nodes + (self.alpha/4.0) * neighbor_sum
        
        # 3. Constraint Enforcement
        self.normalize()

    def get_phi(self):
        """
        Extract the Topological Phase Angle (Theta).
        This is the relevant observable for Layer 1 and 2.
        """
        # 5-point smoothing to reduce lattice noise
        n_up = np.roll(self.nodes, 1, axis=0)
        n_down = np.roll(self.nodes, -1, axis=0)
        n_left = np.roll(self.nodes, 1, axis=1)
        n_right = np.roll(self.nodes, -1, axis=1)
        local_sum = self.nodes + n_up + n_down + n_left + n_right
        local_mean = local_sum / 5.0
        
        # Theta = atan2(y, x)
        theta = np.arctan2(local_mean[:,:,1], local_mean[:,:,0])
        return theta
