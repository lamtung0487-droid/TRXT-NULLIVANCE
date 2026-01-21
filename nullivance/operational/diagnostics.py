import numpy as np
from dataclasses import dataclass
from nullivance.core.state import NullivanceState
from nullivance.config import NullivanceConfig

@dataclass
class ContradictionDiagnostic:
    tilt_alpha: float  # b_alpha
    conflict_alpha: float # c_alpha
    tilt_delta: float  # b_delta
    conflict_delta: float # c_delta

def diagnose_contradiction(state_a: NullivanceState, state_neg_a: NullivanceState, config: NullivanceConfig) -> ContradictionDiagnostic:
    """
    Calculates diagnostics for a contradictory pair (A, neg A).
    Section 4 (A7/A7b)
    """
    eps = config.epsilon

    # 4.1 Alpha-space diagnostics
    alpha_a = state_a.alpha
    alpha_neg = state_neg_a.alpha

    b_alpha = alpha_a / (alpha_a + alpha_neg + eps)
    c_alpha = 2.0 * min(alpha_a, alpha_neg)

    # 4.2 Delta-space diagnostics
    delta_a = state_a.manifest_score
    delta_neg = state_neg_a.manifest_score

    b_delta = delta_a / (delta_a + delta_neg + eps)
    c_delta = 2.0 * min(delta_a, delta_neg)

    return ContradictionDiagnostic(b_alpha, c_alpha, b_delta, c_delta)
