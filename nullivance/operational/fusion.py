import numpy as np
from nullivance.core.state import NullivanceState
from nullivance.config import NullivanceConfig
from nullivance.operational.diagnostics import diagnose_contradiction

def operational_fusion(state_a: NullivanceState, state_neg_a: NullivanceState, config: NullivanceConfig) -> NullivanceState:
    """
    Implements the Operational Operator (oplus_S) for fusion.
    Section 5 (A8)
    """
    diag = diagnose_contradiction(state_a, state_neg_a, config)

    # Fusion properties
    alpha_s = diag.conflict_alpha # c_alpha

    # Weighted phase fusion
    eps = config.epsilon
    numerator = state_a.alpha * state_a.theta + state_neg_a.alpha * state_neg_a.theta
    denominator = state_a.alpha + state_neg_a.alpha + eps
    theta_s = numerator / denominator

    # Create new signature (Operational convention)
    # The spec doesn't strictly define the signature string of the fused state,
    # but implying it's a fusion is good practice.
    sig_s = f"FUSION({state_a.signature}|{state_neg_a.signature})"

    return NullivanceState(
        signature=sig_s,
        alpha=alpha_s,
        theta=theta_s,
        config=config
    )
