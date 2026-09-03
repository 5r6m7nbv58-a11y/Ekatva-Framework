import unittest
from multi_agent_enforced import Agent, EnforcedEcosystem

class TestEkatvaFramework(unittest.unittest.TestCase if hasattr(unittest, 'unittest') else unittest.TestCase):

    def test_loss_bounds(self):
        agent = Agent("TestAgent", 0.5)
        loss = agent.compute_loss(100.0)
        self.assertTrue(0.0 <= loss <= 1.0, "Loss out of bounds [0, 1]")

    def test_tax_enforcement_trigger(self):
        # Exploitative agent with rate 0.9 should yield total loss > 0.40 under degraded health
        greedy_agent = Agent("GreedyAgent", 0.9)
        loss = greedy_agent.compute_loss(50.0)
        self.assertGreater(loss, 0.40, "Expected loss to breach 0.40 threshold for tax trigger")

    def test_ecosystem_simulation_step(self):
        eco = EnforcedEcosystem(num_agents=5)
        initial_health = eco.health
        eco.step(1)
        self.assertNotEqual(initial_health, eco.health, "Ecosystem health should update after a step")
        self.assertEqual(len(eco.telemetry), 1, "Telemetry log should record step data")

if __name__ == "__main__":
    unittest.main()
