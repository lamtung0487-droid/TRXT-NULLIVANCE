from dataclasses import dataclass
from typing import Optional

@dataclass
class NullivanceConfig:
    """
    Configuration parameters for Nullivance Logic System v1.0.
    Adheres to Section 15 of the spec.
    """
    # Core Dimension
    phase_dim: int = 8  # 'd' in spec

    # Numerical Epsilon (globally)
    epsilon: float = 1e-9  # 'epsilon' in spec

    # Compatibility Blend
    lambda_blend: float = 0.5  # 'lambda' in spec (0.5 means equal weight to sigma and theta)

    # Pattern Thresholds
    kappa: float = 0.7  # Cohesion threshold (Section 6.2)
    tau_pattern: float = 0.6  # Manifest score threshold for patterns (Section 6.2)

    # Formal Logic Thresholds
    tau_satisfaction: float = 0.5  # 'tau' in spec for NPL-2D satisfaction (Section 11.2)

    # Outlier Thresholds (Section 7)
    epsilon_o: float = 0.2  # Max compatibility for Oblivivance
    epsilon_alpha: float = 0.1  # Low alpha threshold (Quasivance) / High alpha (Oblivivance)
    epsilon_rho: float = 0.8  # High potential threshold (Quasivance)
    epsilon_w: float = 0.7  # High connectivity threshold (Quasivance)

    # Operational/Transition
    beta_temp: float = 1.0  # Temperature for softmax transition

    def validate(self):
        if not (0 < self.tau_satisfaction <= 1):
            raise ValueError("tau_satisfaction must be in (0, 1]")
        if not (0 <= self.lambda_blend <= 1):
            raise ValueError("lambda_blend must be in [0, 1]")
