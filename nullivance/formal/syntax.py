from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

class Formula(ABC):
    @abstractmethod
    def __repr__(self):
        pass

@dataclass(frozen=True)
class Atom(Formula):
    name: str
    def __repr__(self):
        return self.name

@dataclass(frozen=True)
class Negation(Formula):
    sub: Formula
    def __repr__(self):
        return f"¬{self.sub}"

@dataclass(frozen=True)
class Conjunction(Formula):
    left: Formula
    right: Formula
    def __repr__(self):
        return f"({self.left} ∧ {self.right})"

@dataclass(frozen=True)
class Disjunction(Formula):
    left: Formula
    right: Formula
    def __repr__(self):
        return f"({self.left} ∨ {self.right})"

@dataclass(frozen=True)
class Harmonization(Formula):
    left: Formula
    right: Formula
    def __repr__(self):
        return f"({self.left} ⊕ {self.right})"

# Implication is a derived macro: phi => psi := neg phi v psi
def Implication(phi: Formula, psi: Formula) -> Formula:
    return Disjunction(Negation(phi), psi)
