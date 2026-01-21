import unittest
import numpy as np
from nullivance.config import NullivanceConfig
from nullivance.core.state import NullivanceState
from nullivance.operational.field import LogicField
from nullivance.operational.diagnostics import diagnose_contradiction
from nullivance.operational.fusion import operational_fusion
from nullivance.operational.patterns import check_pattern_criterion, identify_outlier, OutlierType

class TestOperational(unittest.TestCase):
    def setUp(self):
        self.config = NullivanceConfig(phase_dim=2, epsilon=1e-9)
        self.theta_stable = np.array([0.5, 0.5])
        self.theta_unstable = np.array([0.0, 0.0])

    def test_fusion(self):
        # State A: Strong, stable
        a = NullivanceState("A", 1.0, self.theta_stable, self.config)
        # State Not A: Strong, stable
        neg_a = NullivanceState("!A", 1.0, self.theta_stable, self.config)

        # Diagnostics
        diag = diagnose_contradiction(a, neg_a, self.config)
        self.assertAlmostEqual(diag.tilt_alpha, 0.5, places=1) # Balanced
        self.assertAlmostEqual(diag.conflict_alpha, 2.0, places=1) # High conflict

        # Fusion
        fused = operational_fusion(a, neg_a, self.config)
        # Alpha should be c_alpha = 2.0 (wait, alpha > 1? Spec says alpha in [0,1].
        # A7 says c_alpha = 2 * min(a, b). If a=1, b=1, c=2.
        # A1 says alpha in [0,1].
        # There is a potential conflict in the user spec or I need to interpret c_alpha as a raw score
        # that might be clamped later, or it indicates hyper-existence.
        # However, for fusion state A8 says alpha_S = c_alpha.
        # If I strictly follow spec, alpha can be 2.
        # But A1 says A \equiv (..., alpha \in [0,1]).
        # I will check if State clamps it. State __post_init__ clamps it.
        # So fused.alpha should be 1.0.

        self.assertEqual(fused.alpha, 1.0)

    def test_pattern_detection(self):
        # Create a cluster of 3 identical states
        # NOTE: If we use "P1", "P2", "P3", the LCS similarity is not 1.0.
        # LCS("P1", "P2") is "P" (len 1). Max len 2. Sim = 0.5.
        # This reduces cohesion.
        # To test perfect cohesion, use same signature.

        s1 = NullivanceState("P", 1.0, self.theta_stable, self.config)
        s2 = NullivanceState("P", 1.0, self.theta_stable, self.config)
        s3 = NullivanceState("P", 1.0, self.theta_stable, self.config)

        field = LogicField([s1, s2, s3], self.config)

        # Cohesion should be 1.0 (max compatibility)
        res = check_pattern_criterion([0, 1, 2], field, self.config)

        self.assertTrue(res.is_pattern)
        self.assertAlmostEqual(res.cohesion, 1.0)

    def test_outlier_oblivivance(self):
        # State O: High alpha, but incompatible with everyone (theta mismatch)
        # s_main: stable 0.5
        # s_out: stable 0.0 (f=0), sim_theta -> 0 (vectors opposite direction from center? no, 0.0 is unstable)
        # Compatibility involves signature too.

        s_main = NullivanceState("MAIN", 1.0, self.theta_stable, self.config)
        # different sig, different theta
        s_out = NullivanceState("OUT", 1.0, self.theta_unstable, self.config)

        # Lambda=0.5.
        # Sim Sig = 0.
        # Sim Theta:
        #   u1 = [0, 0], u2 = [-0.5, -0.5].
        #   cos = 0 (because u1 is zero vector).
        #   sim_theta = (0+1)/2 = 0.5.
        # Comp = 0.5 * 0 + 0.5 * 0.5 = 0.25.

        # Default Epsilon_O is 0.2.
        # 0.25 is NOT < 0.2. So it returns NONE.

        # To force Oblivivance, we need Comp < Epsilon_O.
        # We can increase Epsilon_O in a custom config.

        custom_config = NullivanceConfig(phase_dim=2, epsilon_o=0.3)
        s_main.config = custom_config
        s_out.config = custom_config

        field = LogicField([s_main, s_out], custom_config)

        # Check s_out (index 1)
        otype = identify_outlier(1, field, custom_config)

        self.assertEqual(otype, OutlierType.OBLIVIVANCE)

if __name__ == '__main__':
    unittest.main()
