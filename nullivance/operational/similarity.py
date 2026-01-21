import numpy as np
from nullivance.core.math_ops import similarity_lcs, similarity_phase_cosine
from nullivance.core.state import NullivanceState
from nullivance.config import NullivanceConfig

def compatibility(state_a: NullivanceState, state_b: NullivanceState, config: NullivanceConfig) -> float:
    """
    Calculates Compatibility(A, B) = lambda * sim_sigma + (1-lambda) * sim_theta
    Section 3.3 (A5)
    """
    sim_sigma = similarity_lcs(state_a.signature, state_b.signature)
    sim_theta = similarity_phase_cosine(state_a.theta, state_b.theta, config.epsilon)

    comp = config.lambda_blend * sim_sigma + (1.0 - config.lambda_blend) * sim_theta

    # Bounded [0, 1]
    return max(0.0, min(1.0, comp))
