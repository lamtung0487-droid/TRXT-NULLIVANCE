from typing import Dict, Tuple, Optional
from dataclasses import dataclass
import numpy as np

from nullivance.formal.syntax import Formula, Atom, Negation, Conjunction, Disjunction, Harmonization
from nullivance.core.state import NullivanceState
from nullivance.config import NullivanceConfig
from nullivance.core.math_ops import global_stability_geo

@dataclass
class ValuationEntry:
    """
    Stores the Truth-support and Falsity-support states for an atom.
    Section 11.2
    """
    alpha_T: float
    theta_T: np.ndarray
    alpha_F: float
    theta_F: np.ndarray

    def get_truth_delta(self, config: NullivanceConfig) -> float:
        # t(p) = alpha_T * Phi(Theta_T)
        phi_t = global_stability_geo(self.theta_T, config.epsilon)
        return self.alpha_T * phi_t

    def get_falsity_delta(self, config: NullivanceConfig) -> float:
        # f(p) = alpha_F * Phi(Theta_F)
        phi_f = global_stability_geo(self.theta_F, config.epsilon)
        return self.alpha_F * phi_f

class Model:
    def __init__(self, config: NullivanceConfig):
        self.config = config
        self.valuation: Dict[str, ValuationEntry] = {}

    def set_valuation(self, atom_name: str, entry: ValuationEntry):
        self.valuation[atom_name] = entry

    def evaluate(self, phi: Formula) -> Tuple[float, float]:
        """
        Evaluates V(phi) = (t(phi), f(phi)) recursively.
        Section 11.3
        """
        if isinstance(phi, Atom):
            if phi.name not in self.valuation:
                # Default to (0,0) if undefined? Or raise error.
                return (0.0, 0.0)
            entry = self.valuation[phi.name]
            return (entry.get_truth_delta(self.config), entry.get_falsity_delta(self.config))

        elif isinstance(phi, Negation):
            # t(~phi) = f(phi), f(~phi) = t(phi)
            t_sub, f_sub = self.evaluate(phi.sub)
            return (f_sub, t_sub)

        elif isinstance(phi, Conjunction):
            # t = min(t1, t2), f = max(f1, f2)
            t1, f1 = self.evaluate(phi.left)
            t2, f2 = self.evaluate(phi.right)
            return (min(t1, t2), max(f1, f2))

        elif isinstance(phi, Disjunction):
            # t = max(t1, t2), f = min(f1, f2)
            t1, f1 = self.evaluate(phi.left)
            t2, f2 = self.evaluate(phi.right)
            return (max(t1, t2), min(f1, f2))

        elif isinstance(phi, Harmonization):
            # t = min(t1, t2), f = min(f1, f2)  (Formal Oplus)
            t1, f1 = self.evaluate(phi.left)
            t2, f2 = self.evaluate(phi.right)
            return (min(t1, t2), min(f1, f2))

        else:
            raise ValueError(f"Unknown formula type: {type(phi)}")

    def check_satisfaction(self, phi: Formula) -> str:
        """
        Returns the FOUR state classification based on tau.
        Section 11.4
        """
        t, f = self.evaluate(phi)
        tau = self.config.tau_satisfaction

        satisfied = t >= tau
        falsified = f >= tau

        if satisfied and falsified:
            return "B" # Both
        elif satisfied and not falsified:
            return "T" # True
        elif not satisfied and falsified:
            return "F" # False
        else:
            return "N" # Neither

    def is_satisfied(self, phi: Formula) -> bool:
        t, _ = self.evaluate(phi)
        return t >= self.config.tau_satisfaction
