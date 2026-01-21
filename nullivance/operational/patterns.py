from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional
import numpy as np

from nullivance.core.state import NullivanceState
from nullivance.config import NullivanceConfig
from nullivance.operational.field import LogicField
from nullivance.core.math_ops import global_stability_geo

class OutlierType(Enum):
    NONE = auto()
    OBLIVIVANCE = auto() # Incompatibility outlier
    QUASIVANCE = auto()  # Super-isolated potential

@dataclass
class PatternResult:
    is_pattern: bool
    pattern_state: Optional[NullivanceState]
    pattern_type: str # "Template" or "Emergent"
    cluster_indices: List[int]
    cohesion: float

def calculate_cohesion(cluster_indices: List[int], field: LogicField) -> float:
    """
    Calculates Cohesion(C) = avg(W_ij) for i < j in C.
    Section 6.1
    """
    if len(cluster_indices) < 2:
        return 1.0 # Singleton cluster cohesion is implicitly 1 or handled separately

    total_weight = 0.0
    count = 0

    for idx_i in cluster_indices:
        for idx_j in cluster_indices:
            if idx_i < idx_j:
                total_weight += field.get_weight(idx_i, idx_j)
                count += 1

    return total_weight / count if count > 0 else 0.0

def create_emergent_pattern(cluster_indices: List[int], field: LogicField, config: NullivanceConfig) -> NullivanceState:
    """
    Creates an Emergent Pattern from a cluster.
    Section 6.4
    """
    cluster_states = [field.states[i] for i in cluster_indices]

    # Manifest weights u_i = delta(A_i)
    u_vals = [s.manifest_score for s in cluster_states]
    sum_u = sum(u_vals)

    # Phase pattern: Weighted average by manifest score
    # Theta(P) = sum(u_i * Theta_i) / (sum(u_i) + eps)
    numerator = np.zeros(config.phase_dim)
    for s, u in zip(cluster_states, u_vals):
        numerator += u * s.theta

    theta_p = numerator / (sum_u + config.epsilon)

    # Existence pattern (union-like)
    # alpha(P) = 1 - prod(1 - alpha(A_i))
    prod_inv = 1.0
    for s in cluster_states:
        prod_inv *= (1.0 - s.alpha)
    alpha_p = 1.0 - prod_inv

    sig_p = f"PATTERN(n={len(cluster_states)})"

    return NullivanceState(sig_p, alpha_p, theta_p, config)

def check_pattern_criterion(cluster_indices: List[int], field: LogicField, config: NullivanceConfig) -> PatternResult:
    """
    Checks if a cluster forms a valid pattern.
    Section 6.2 (A9)
    """
    coh = calculate_cohesion(cluster_indices, field)

    # We construct the potential pattern state to check its manifest score
    pattern_state = create_emergent_pattern(cluster_indices, field, config)
    delta_p = pattern_state.manifest_score

    is_valid = (coh >= config.kappa) and (delta_p >= config.tau_pattern)

    return PatternResult(
        is_pattern=is_valid,
        pattern_state=pattern_state if is_valid else None,
        pattern_type="Emergent",
        cluster_indices=cluster_indices,
        cohesion=coh
    )

def identify_outlier(index: int, field: LogicField, config: NullivanceConfig) -> OutlierType:
    """
    Identifies if a state is an outlier (Oblivivance or Quasivance).
    Section 7
    """
    state = field.states[index]
    n = len(field.states)

    # Calculate max compatibility with others
    max_w = 0.0
    if n > 1:
        w_values = []
        for j in range(n):
            if index != j:
                w_values.append(field.get_weight(index, j))
        if w_values:
            max_w = max(w_values)

    # 7.1 Oblivivance (Incompatibility outlier)
    # max_w < eps_o AND alpha > eps_alpha
    if max_w < config.epsilon_o and state.alpha > config.epsilon_alpha:
        return OutlierType.OBLIVIVANCE

    # 7.2 Quasivance (Super-isolated potential)
    # alpha < eps_alpha AND rho > eps_rho AND max_w > eps_w (wait, spec says max_w > eps_w?)
    # Re-reading spec Section 7.2:
    # "max_{j != i} W_{ij} > epsilon_w"
    # Yes, Quasivance has high connectivity/relation potential despite low alpha.

    rho = state.potential_score
    if (state.alpha < config.epsilon_alpha and
        rho > config.epsilon_rho and
        max_w > config.epsilon_w):
        return OutlierType.QUASIVANCE

    return OutlierType.NONE
