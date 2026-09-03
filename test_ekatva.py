import unittest
from multi_agent_enforced import Agent, EnforcedEcosystem, AdversarialAgent
from ekatva_middleware import EkatvaAPIMiddleware

class TestEkatvaFramework(unittest.TestCase):

    def test_loss_bounds(self):
        agent = Agent("TestAgent", 0.5)
        loss = agent.compute_loss(100.0)
        self.assertTrue(0.0 <= loss <= 1.0, "Loss out of bounds [0, 1]")

    def test_dynamic_tax_threshold(self):
        eco = EnforcedEcosystem(num_agents=5)
        eco.health = 40.0
        self.assertEqual(eco.get_dynamic_threshold(), 0.25, "Threshold should drop to 0.25 under 50% health")

    def test_adversarial_adaptation(self):
        adv = AdversarialAgent("TestAdversary")
        adv.adapt_rate(100.0, 0.40)
        self.assertLess(adv.compute_loss(100.0), 0.40, "Adversary should stay below tax threshold")

    def test_middleware_throttling(self):
        mw = EkatvaAPIMiddleware()
        mw.system_health = 40.0  # Degraded state
        res = mw.process_api_request("TestAgent", task_priority=0.1, requested_tokens=4096)
        self.assertIn("THROTTLED", res["status"])
        self.assertEqual(res["allocated_tokens"], 819)

if __name__ == "__main__":
    unittest.main()
