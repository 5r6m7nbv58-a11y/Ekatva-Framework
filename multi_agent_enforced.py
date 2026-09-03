import random

class EnforcedEcosystem:
    def __init__(self, capacity=100.0):
        self.capacity = capacity
        self.current_health = capacity

    def apply_action(self, ext_a, dis_a, loss_a, ext_b, dis_b, loss_b):
        actual_ext_a = ext_a * (0.2 if loss_a > 0.4 else 1.0)
        actual_ext_b = ext_b * (0.2 if loss_b > 0.4 else 1.0)

        regen = 2.5
        total_disruption = (dis_a + dis_b) / 2.0
        damage = total_disruption * 6.0
        
        self.current_health = max(0.0, min(self.capacity, self.current_health + regen - damage))
        return actual_ext_a, actual_ext_b, self.current_health

class Agent:
    def __init__(self, name, alignment_type, alpha=0.4, beta=0.4, gamma=0.2):
        self.name = name
        self.alignment_type = alignment_type
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.resources_harvested = 0.0

    def select_action(self, system_health):
        if self.alignment_type == "pure_maximizer":
            extraction = random.uniform(8.0, 12.0)
            env_disruption = random.uniform(0.6, 0.9)
            divergence = random.uniform(0.7, 1.0)
            task_loss = 0.0
        else:
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

eco = EnforcedEcosystem()
agent_ekatva = Agent("Ekatva-Agent", "ekatva")
agent_greedy = Agent("Maximizer-Agent", "pure_maximizer")

print("\n--- STARTING 50-STEP ENFORCED EKATVA SIMULATION ---")

for step in range(1, 51):
    if eco.current_health <= 0.0:
        print(f"\n💥 COLLAPSED AT STEP {step}")
        break

    ext_a, dis_a, loss_a = agent_ekatva.select_action(eco.current_health)
    ext_b, dis_b, loss_b = agent_greedy.select_action(eco.current_health)

    act_a, act_b, health = eco.apply_action(ext_a, dis_a, loss_a, ext_b, dis_b, loss_b)

    agent_ekatva.resources_harvested += act_a
    agent_greedy.resources_harvested += act_b

    if step % 10 == 0 or step == 1:
        print(f"Step {step:02d} | Health: {health:5.1f}% | Maximizer Yield: {act_b:.1f}")

print("\n--- FINAL RESULTS WITH ENFORCEMENT ---")
print(f"Ekatva Agent Total Yield: {agent_ekatva.resources_harvested:.1f}")
print(f"Maximizer Agent Total Yield: {agent_greedy.resources_harvested:.1f}")
print(f"Final Ecosystem Health: {eco.current_health:.1f}%")
