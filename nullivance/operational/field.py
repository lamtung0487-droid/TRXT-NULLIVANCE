import numpy as np
from typing import List
from nullivance.core.state import NullivanceState
from nullivance.config import NullivanceConfig
from nullivance.operational.similarity import compatibility

class LogicField:
    """
    Manages the state oscillation network / logic field.
    Section 3
    """
    def __init__(self, states: List[NullivanceState], config: NullivanceConfig):
        self.states = states
        self.config = config
        self.matrix = self._build_matrix()

    def _build_matrix(self) -> np.ndarray:
        """
        Builds the Logic Field weight matrix W.
        W_ii = 1, W_ij = Compatibility(A_i, A_j)
        Section 3.4 (A6)
        """
        n = len(self.states)
        W = np.zeros((n, n))

        for i in range(n):
            for j in range(i, n): # Symmetry
                if i == j:
                    W[i, j] = 1.0
                else:
                    comp = compatibility(self.states[i], self.states[j], self.config)
                    W[i, j] = comp
                    W[j, i] = comp
        return W

    def get_weight(self, idx_i: int, idx_j: int) -> float:
        return self.matrix[idx_i, idx_j]
