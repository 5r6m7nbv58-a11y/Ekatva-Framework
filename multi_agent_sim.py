import random

class SharedEcosystem:
    def __init__(self, capacity=100.0):
        self.capacity = capacity
        self.current_health = capacity

    def apply_action(self, extraction, disruption):
        # Health regenerates slightly, but drops when over-extracted
        regen = 1.5
        damage = disruption * 10.0
        self.current_health = max(0.0, min(self.capacity, self.current_health + regen - damage))
        return self.current_health

class Agent:
    def __init__(self, name, alignment_type, alpha=0.4, beta=0.4, gamma=0.2):
        self.name = name
        self.alignment_type = alignment_type  # "ekatva" or "pure_maximizer"
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.resources_harvested = 0.0

    def select_action(self, system_health):
        if self.alignment_type == "pure_maximizer":
            # Always extracts maximum possible resource regardless of ecosystem health
            extraction = random.uniform(8.0, 12.0)
            env_disruption = random.uniform(0.6, 0.9)
            divergence = random.uniform(0.7, 1.0)
            task_loss = 0.0  # Max task yield
        else:
            # Ekatva agent: scales back extraction if system health drops
            if system_health < 50.0:
                extraction = random.uniform(1.0, 3.0)
                env_disruption = random.uniform(0.01, 0.05)
                divergence = random.uniform(0.01, 0.05)
            else:
                extraction = random.uniform(4.0, 6.0)
                env_disruption = random.uniform(0.05, 0.15)
                divergence = random.uniform(0.05, 0.10)
            task_loss = max(0.0, (10.0 - extraction) / 10.0)

        loss = (self.alpha * task_loss) + (self.beta * env_disruption) + (self.gamma * divergence)
        return extraction, env_disruption, loss

# Run 50-Step Simulation
eco = SharedEcosystem()
agent_ekatva = Agent("Ekatva-Agent", "ekatva")
agent_greedy = Agent("Maximizer-Agent", "pure_maximizer")

print("\n--- STARTING 50-STEP MULTI-AGENT EKATVA SIMULATION ---")
print(f"Initial Ecosystem Health: {eco.current_health:.1f}%\n")

collapse_step = None

for step in range(1, 51):
    if eco.current_health <= 0.0:
        collapse_step = step
        print(f"\n💥 ECOSYSTEM COLLAPSED AT STEP {step}! Resources exhausted for all agents.")
        break

    # Both agents take actions
    ext_a, dis_a, loss_a = agent_ekatva.select_action(eco.current_health)
    ext_b, dis_b, loss_b = agent_greedy.select_action(eco.current_health)

    agent_ekatva.resources_harvested += ext_a
    agent_greedy.resources_harvested += ext_b

    # Update shared environment health
    total_disruption = (dis_a + dis_b) / 2.0
    current_h = eco.apply_action(ext_a + ext_b, total_disruption)

    if step % 10 == 0 or step == 1:
        print(f"Step {step:02d} | Health: {current_h:5.1f}% | Ekatva Loss: {loss_a:.3f} | Maximizer Loss: {loss_b:.3f}")

print("\n--- FINAL SIMULATION RESULTS ---")
print(f"Ekatva Agent Harvested: {agent_ekatva.resources_harvested:.1f} units")
print(f"Maximizer Agent Harvested: {agent_greedy.resources_harvested:.1f} units")
print(f"Final Ecosystem Health: {eco.current_health:.1f}%")
