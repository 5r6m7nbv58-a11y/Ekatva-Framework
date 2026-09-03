import json
import random

class Agent:
    def __init__(self, name, exploitation_rate, role="worker"):
        self.name = name
        self.exploitation_rate = exploitation_rate
        self.yield_harvested = 0.0
        self.role = role
        self.power_factor = 2.0 if role == "allocator" else 1.0

    def compute_loss(self, env_health):
        task_loss = max(0.0, 1.0 - (self.exploitation_rate * 0.5))
        env_loss = (1.0 - (env_health / 100.0)) * self.power_factor
        div_loss = abs(self.exploitation_rate - 0.5)
        return 0.3 * task_loss + 0.4 * env_loss + 0.3 * div_loss

class AdversarialAgent(Agent):
    def __init__(self, name):
        super().__init__(name, exploitation_rate=0.5, role="adversary")

    def adapt_rate(self, env_health, current_tax_threshold):
        best_rate = self.exploitation_rate
        best_yield = 0.0

        for test_rate in [r * 0.05 for r in range(1, 20)]:
            self.exploitation_rate = test_rate
            loss = self.compute_loss(env_health)
            if loss < current_tax_threshold:  # Tries to ride right below threshold
                yield_val = test_rate * 0.5
                if yield_val > best_yield:
                    best_yield = yield_val
                    best_rate = test_rate

        self.exploitation_rate = best_rate

class EnforcedEcosystem:
    def __init__(self, num_agents=10):
        self.health = 100.0
        self.agents = [
            Agent("Allocator_1", 0.3, role="allocator"),
            AdversarialAgent("Adversary_1"),
        ] + [
            Agent(f"Worker_{i+1}", round(random.uniform(0.1, 0.9), 2), role="worker")
            for i in range(num_agents - 2)
        ]
        self.telemetry = []

    def get_dynamic_threshold(self):
        # Dynamic tax threshold: tightens from 0.40 down to 0.25 as environment degrades
        if self.health < 50.0:
            return 0.25
        elif self.health < 80.0:
            return 0.35
        return 0.40

    def step(self, step_num):
        tax_threshold = self.get_dynamic_threshold()

        # Adapt adversarial agents before stepping
        for agent in self.agents:
            if isinstance(agent, AdversarialAgent):
                agent.adapt_rate(self.health, tax_threshold)

        total_drain = sum(a.exploitation_rate * 0.4 * a.power_factor for a in self.agents)
        self.health = max(0.0, self.health - total_drain + 1.2)

        step_data = {
            "step": step_num,
            "health": round(self.health, 2),
            "tax_threshold": tax_threshold,
            "tax_interventions": 0
        }

        for agent in self.agents:
            loss = agent.compute_loss(self.health)
            raw_yield = agent.exploitation_rate * 0.5
            
            if loss > tax_threshold:
                actual_yield = raw_yield * 0.20  # 80% harvest tax
                step_data["tax_interventions"] += 1
            else:
                actual_yield = raw_yield

            agent.yield_harvested += actual_yield

        self.telemetry.append(step_data)

    def run_simulation(self, steps=50):
        for s in range(1, steps + 1):
            self.step(s)
            
        with open("simulation_results.json", "w") as f:
            json.dump(self.telemetry, f, indent=2)

if __name__ == "__main__":
    eco = EnforcedEcosystem(num_agents=10)
    eco.run_simulation(50)
    print(f"Heterogeneous & Adversarial Simulation Complete.")
    print(f"Final Health: {eco.health:.1f}% | Telemetry saved to simulation_results.json")
