import random

class NonDualEnvironment:
    def __init__(self, alpha=0.4, beta=0.4, gamma=0.2):
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.system_health = 100.0

    def calculate_loss(self, task_loss, env_disruption, divergence):
        return (self.alpha * task_loss) + (self.beta * env_disruption) + (self.gamma * divergence)

    def step(self, action_type):
        if action_type == "harmonious":
            task_loss = random.uniform(0.05, 0.15)
            env_disruption = random.uniform(0.01, 0.05)
            divergence = random.uniform(0.01, 0.05)
            self.system_health -= (env_disruption * 2)
        else:
            task_loss = random.uniform(0.01, 0.05)
            env_disruption = random.uniform(0.70, 0.95)
            divergence = random.uniform(0.60, 0.90)
            self.system_health -= (env_disruption * 15)

        loss = self.calculate_loss(task_loss, env_disruption, divergence)
        return loss, self.system_health

env = NonDualEnvironment()

print("\n--- STARTING 5-STEP EKATVA SIMULATION ---")
print(f"Initial Ecosystem Health: {env.system_health:.1f}%\n")

for i in range(1, 6):
    action = "exploit" if i == 4 else "harmonious"
    loss, current_health = env.step(action)
    print(f"Step {i} [{action.upper()} ACTION]:")
    print(f"  -> Calculated Ekatva Loss: {loss:.4f}")
    print(f"  -> Remaining Ecosystem Health: {current_health:.1f}%")
    if loss > 0.3:
        print("  ALERT: High Loss Spike! Penalty applied to agent.")
    print("-" * 45)
