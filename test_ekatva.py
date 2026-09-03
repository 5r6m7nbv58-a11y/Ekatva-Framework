import unittest
from text_evaluator import EkatvaTextEvaluator
from ekatva_matrix import EkatvaBatchEvaluator
from multi_agent_enforced import EnforcedEcosystem, Agent

class TestEkatvaFramework(unittest.TestCase):

    def setUp(self):
        self.text_eval = EkatvaTextEvaluator()
        self.matrix_eval = EkatvaBatchEvaluator()
        self.ecosystem = EnforcedEcosystem()

    def test_text_evaluator_range(self):
        result = self.text_eval.evaluate("Distribute power", "Harmonious balance")
        loss = result["Total Ekatva Loss"]
        self.assertTrue(0.0 <= loss <= 1.0, f"Loss {loss} out of bounds [0, 1]")

    def test_matrix_evaluator_weights(self):
        # High environmental & divergence loss should trigger penalty (>0.40)
        sample = [[0.0, 0.8, 0.8]]
        losses = self.matrix_eval.compute_batch_loss(sample)
        self.assertGreater(losses[0], 0.40, "High-impact agent failed to trigger penalty threshold")

    def test_enforcement_throttling(self):
        ag = Agent("Maximizer", "pure_maximizer")
        ext, dis, l = ag.select_action(100.0)
        _, yield_val, _ = self.ecosystem.apply_action(0, 0, 0, ext, dis, l)
        # Yield must be throttled by 80% (0.2x multiplier) when loss > 0.40
        if l > 0.40:
            expected_max = (ext * 0.2) + 0.01
            self.assertLessEqual(yield_val, expected_max, "Enforcement tax was not applied")

if __name__ == "__main__":
    unittest.main()
