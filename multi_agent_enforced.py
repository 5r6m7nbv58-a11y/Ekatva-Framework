import json
import random
import time

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
            if loss < current_tax_threshold:
                yield_val = test_rate * 0.5
                if yield_val > best_yield:
                    best_yield = yield_val
                    best_rate = test_rate

        self.exploitation_rate = best_rate

class EnforcedEcosystem:
    def __init__(self, num_agents=1000):
        self.health = 100.0
        self.num_agents = num_agents
        
        num_allocators = max(1, int(num_agents * 0.05))
        num_adversaries = max(1, int(num_agents * 0.05))
        num_workers = num_agents - num_allocators - num_adversaries

        self.agents = (
            [Agent(f"Allocator_{i+1}", 0.3, role="allocator") for i in range(num_allocators)] +
            [AdversarialAgent(f"Adversary_{i+1}") for i in range(num_adversaries)] +
            [Agent(f"Worker_{i+1}", round(random.uniform(0.1, 0.9), 2), role="worker") for i in range(num_workers)]
        )
        self.telemetry = []

    def get_dynamic_threshold(self):
        if self.health < 50.0:
            return 0.25
        elif self.health < 80.0:
            return 0.35
        return 0.40

    def step(self, step_num):
        tax_threshold = self.get_dynamic_threshold()

        total_drain = sum(a.exploitation_rate * 0.004 * a.power_factor for a in self.agents)
        
        # Adaptive environment recovery scaled to population size N
        replenishment = 0.003 * self.num_agents
        self.health = max(0.0, min(100.0, self.health - total_drain + replenishment))

        tax_count = 0
        for agent in self.agents:
            if isinstance(agent, AdversarialAgent):
                agent.adapt_rate(self.health, tax_threshold)

            loss = agent.compute_loss(self.health)
            raw_yield = agent.exploitation_rate * 0.5
            
            if loss > tax_threshold:
                actual_yield = raw_yield * 0.20
                tax_count += 1
            else:
                actual_yield = raw_yield

            agent.yield_harvested += actual_yield

        self.telemetry.append({
            "step": step_num,
            "health": round(self.health, 2),
            "tax_threshold": tax_threshold,
            "tax_interventions": tax_count
        })

    def run_simulation(self, steps=100):
        start_time = time.time()
        for s in range(1, steps + 1):
            self.step(s)
        elapsed = time.time() - start_time
            
        with open("simulation_results.json", "w") as f:
            json.dump(self.telemetry, f, indent=2)

        return elapsed

if __name__ == "__main__":
    num_agents = 1000
    steps = 100
    eco = EnforcedEcosystem(num_agents=num_agents)
    elapsed = eco.run_simulation(steps=steps)
    
    print("\n=== HIGH-SCALE BALANCED BENCHMARK COMPLETE ===")
    print(f"Agents Modeled  : {num_agents}")
    print(f"Simulation Steps: {steps}")
    print(f"Execution Time  : {elapsed:.3f}s ({elapsed/steps*1000:.2f} ms/step)")
    print(f"Final Health    : {eco.health:.2f}%")
    print("Telemetry saved : sim
ulation_results.json")
