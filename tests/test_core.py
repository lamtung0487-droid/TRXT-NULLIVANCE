import unittest
import numpy as np
from nullivance.config import NullivanceConfig
from nullivance.core.math_ops import elementwise_stability, global_stability_geo, similarity_lcs, similarity_phase_cosine
from nullivance.core.state import NullivanceState

class TestCore(unittest.TestCase):
    def setUp(self):
        self.config = NullivanceConfig(phase_dim=4, epsilon=1e-9)

    def test_elementwise_stability(self):
        # f(0.5) = 1
        self.assertAlmostEqual(elementwise_stability(0.5), 1.0)
        # f(0) = 0
        self.assertAlmostEqual(elementwise_stability(0.0), 0.0)
        # f(1) = 0
        self.assertAlmostEqual(elementwise_stability(1.0), 0.0)
        # Symmetry f(0.2) == f(0.8) -> 1 - 2*0.3 = 0.4
        self.assertAlmostEqual(elementwise_stability(0.2), 0.4)
        self.assertAlmostEqual(elementwise_stability(0.8), 0.4)

    def test_global_stability_geo(self):
        # 0.5 vector -> 1.0
        theta = np.array([0.5, 0.5, 0.5, 0.5])
        self.assertAlmostEqual(global_stability_geo(theta), 1.0)

        # Scale safety / Inversion invariance
        theta_inv = 1.0 - theta
        self.assertAlmostEqual(global_stability_geo(theta_inv), 1.0)

    def test_state_scores(self):
        theta = np.array([0.5, 0.5, 0.5, 0.5])
        s = NullivanceState("test", 0.8, theta, self.config)

        self.assertAlmostEqual(s.potential_score, 1.0)
        self.assertAlmostEqual(s.manifest_score, 0.8)

class TestSimilarity(unittest.TestCase):
    def test_lcs(self):
        self.assertEqual(similarity_lcs("ABC", "ABC"), 1.0)
        self.assertEqual(similarity_lcs("ABC", "DEF"), 0.0)
        self.assertEqual(similarity_lcs("ABC", "AC"), 2/3)

    def test_cosine(self):
        theta1 = np.array([0.5, 0.5, 0.5, 0.5]) # Zero vector in centered space
        theta2 = np.array([1.0, 1.0, 1.0, 1.0]) # 0.5 vector in centered space

        # Center of theta1 is 0.
        # cos(0, v) is technically undefined or 0 depending on implementation.
        # My impl adds epsilon to norm. dot is 0. result 0.
        # sim = (0+1)/2 = 0.5
        self.assertAlmostEqual(similarity_phase_cosine(theta1, theta2), 0.5)

        theta_a = np.array([1.0, 1.0]) # centered: [0.5, 0.5]
        theta_b = np.array([0.0, 0.0]) # centered: [-0.5, -0.5]
        # opposite direction. cos = -1. sim = 0.
        self.assertAlmostEqual(similarity_phase_cosine(theta_a, theta_b), 0.0)

if __name__ == '__main__':
    unittest.main()
