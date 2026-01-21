import numpy as np
from dataclasses import dataclass, field
from nullivance.core.math_ops import global_stability_geo
from nullivance.config import NullivanceConfig

@dataclass
class NullivanceState:
    """
    Represents a State A = (sigma, alpha, Theta, d).
    Section 1.1
    """
    signature: str          # sigma
    alpha: float            # existence level [0, 1]
    theta: np.ndarray       # phase vector [0, 1]^d
    config: NullivanceConfig = field(default_factory=NullivanceConfig)

    def __post_init__(self):
        # A1 Boundedness Check
        self.theta = np.asarray(self.theta)

        # Validate dimensions
        if self.theta.shape[0] != self.config.phase_dim:
            # We might want to allow variable d, but spec says d is config param.
            # However, for robustness, we just check if it matches expectations or if we should enforce it.
            # Spec says "d is config parameter".
            if self.theta.shape[0] != self.config.phase_dim:
                 raise ValueError(f"Theta dimension {self.theta.shape[0]} does not match config {self.config.phase_dim}")

        # Validate bounds
        if not (0 <= self.alpha <= 1):
            # Clamp or raise? Spec says "clamp/validate" in A1.
            # Let's clamp for resilience, but warning would be good.
            self.alpha = max(0.0, min(1.0, self.alpha))

        # Clamp Theta
        self.theta = np.clip(self.theta, 0.0, 1.0)

    @property
    def potential_score(self) -> float:
        """
        Potential score (rho) = Phi_geo(Theta)
        Section 2.3
        """
        return global_stability_geo(self.theta, self.config.epsilon)

    @property
    def manifest_score(self) -> float:
        """
        Manifest score (delta) = alpha * rho
        Section 2.3
        """
        return self.alpha * self.potential_score

    def __repr__(self):
        return f"State({self.signature}, a={self.alpha:.2f}, rho={self.potential_score:.2f}, delta={self.manifest_score:.2f})"
