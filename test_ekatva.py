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

    def test_high_scale_agent_distribution(self):
        eco = EnforcedEcosystem(num_agents=1000)
        self.assertEqual(len(eco.agents), 1000, "Ecosystem should instantiate exactly 1000 agents")
        allocators = [a for a in eco.agents if a.role == "allocator"]
        self.assertEqual(len(allocators), 50, "Expected 50 allocators (5%) in 1000-agent ecosystem")

    def test_middleware_throttling(self):
        mw = EkatvaAPIMiddleware()
        mw.system_health = 40.0
        res = mw.process_api_request("TestAgent", task_priority=0.1, requested_tokens=4096)
        self.assertIn("THROTTLED", res["status"])
        self.assertEqual(res["allocated_tokens"], 819)

if __name__ == "__main__":
    unittest.main()
