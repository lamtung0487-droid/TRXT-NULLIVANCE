import unittest
import numpy as np
from nullivance.config import NullivanceConfig
from nullivance.formal.syntax import Atom, Negation, Implication
from nullivance.formal.semantics import Model, ValuationEntry

class TestFormal(unittest.TestCase):
    def setUp(self):
        self.config = NullivanceConfig(phase_dim=2, tau_satisfaction=0.5)
        self.model = Model(self.config)

    def test_soundness_witness(self):
        """
        Section 12.3 Soundness Witness
        Verify that p and neg p can be satisfied simultaneously without explosion (q not satisfied).
        """
        # Create p: Both true and false support are strong
        # Theta=0.5 (perfect stability), Alpha=1.0
        # t(p) = 1.0, f(p) = 1.0
        p_entry = ValuationEntry(
            alpha_T=1.0, theta_T=np.array([0.5, 0.5]),
            alpha_F=1.0, theta_F=np.array([0.5, 0.5])
        )
        self.model.set_valuation("p", p_entry)

        # Create q: Neither true nor false support
        # Alpha=0.0
        # t(q) = 0.0, f(q) = 0.0
        q_entry = ValuationEntry(
            alpha_T=0.0, theta_T=np.array([0.5, 0.5]),
            alpha_F=0.0, theta_F=np.array([0.5, 0.5])
        )
        self.model.set_valuation("q", q_entry)

        p = Atom("p")
        neg_p = Negation(p)
        q = Atom("q")

        # Check p
        self.assertEqual(self.model.check_satisfaction(p), "B") # Both
        self.assertTrue(self.model.is_satisfied(p))

        # Check neg p
        # t(~p) = f(p) = 1.0 >= 0.5
        self.assertEqual(self.model.check_satisfaction(neg_p), "B")
        self.assertTrue(self.model.is_satisfied(neg_p))

        # Check explosion: p, neg p |- q ?
        # In classical logic, this holds. In paraconsistent, it should not necessarily hold.
        # Here we check that q is NOT satisfied despite p and ~p being satisfied.
        self.assertEqual(self.model.check_satisfaction(q), "N") # Neither
        self.assertFalse(self.model.is_satisfied(q))

    def test_implication(self):
        # p => q  is  ~p v q
        # t = max(f(p), t(q))

        # Case: p is True (t=1, f=0), q is False (t=0, f=1)
        # t(p=>q) = max(0, 0) = 0 -> Not satisfied. Correct.
        p_entry = ValuationEntry(1.0, np.array([0.5, 0.5]), 0.0, np.array([0.0, 0.0])) # T
        q_entry = ValuationEntry(0.0, np.array([0.0, 0.0]), 1.0, np.array([0.5, 0.5])) # F

        self.model.set_valuation("p", p_entry)
        self.model.set_valuation("q", q_entry)

        imp = Implication(Atom("p"), Atom("q"))
        self.assertFalse(self.model.is_satisfied(imp))

if __name__ == '__main__':
    unittest.main()
