import json
import time
import numpy as np

def run_vectorized_benchmark(num_agents=500000, steps=100):
    start_time = time.time()

    num_allocators = max(1, int(num_agents * 0.05))
    num_adversaries = max(1, int(num_agents * 0.05))
    num_workers = num_agents - num_allocators - num_adversaries

    power_factors = np.ones(num_agents, dtype=np.float32)
    power_factors[:num_allocators] = 2.0

    exploitation_rates = np.empty(num_agents, dtype=np.float32)
    exploitation_rates[:num_allocators] = 0.3
    exploitation_rates[num_allocators:num_allocators + num_adversaries] = 0.5
    exploitation_rates[num_allocators + num_adversaries:] = np.random.uniform(0.1, 0.9, num_workers)

    is_adversary = np.zeros(num_agents, dtype=bool)
    is_adversary[num_allocators:num_allocators + num_adversaries] = True

    health = 100.0
    telemetry = []
    test_rates = np.linspace(0.05, 0.95, 19, dtype=np.float32)

    for step_num in range(1, steps + 1):
        if health < 50.0:
            tax_threshold = 0.25
        elif health < 80.0:
            tax_threshold = 0.35
        else:
            tax_threshold = 0.40

        total_drain = np.sum(exploitation_rates * 0.004 * power_factors)
        replenishment = 0.003 * num_agents
        health = float(np.clip(health - total_drain + replenishment, 0.0, 100.0))

        if np.any(is_adversary):
            task_loss_cand = np.maximum(0.0, 1.0 - (test_rates[:, None] * 0.5))
            env_loss_cand = (1.0 - (health / 100.0)) * 1.0
            div_loss_cand = np.abs(test_rates[:, None] - 0.5)
            loss_cand = 0.3 * task_loss_cand + 0.4 * env_loss_cand + 0.3 * div_loss_cand

            yield_cand = test_rates[:, None] * 0.5
            valid_mask = loss_cand < tax_threshold
            masked_yields = np.where(valid_mask, yield_cand, -1.0)
            
            best_rate_idx = np.argmax(masked_yields, axis=0)
            exploitation_rates[is_adversary] = test_rates[best_rate_idx]

        task_loss = np.maximum(0.0, 1.0 - (exploitation_rates * 0.5))
        env_loss = (1.0 - (health / 100.0)) * power_factors
        div_loss = np.abs(exploitation_rates - 0.5)
        loss = 0.3 * task_loss + 0.4 * env_loss + 0.3 * div_loss

        taxed_mask = loss > tax_threshold
        tax_count = int(np.sum(taxed_mask))

        telemetry.append({
            "step": step_num,
            "health": round(health, 2),
            "tax_threshold": tax_threshold,
            "tax_interventions": tax_count
        })

    elapsed = time.time() - start_time

    with open("simulation_results.json", "w") as f:
        json.dump(telemetry, f, indent=2)

    print("\n=== MASSIVE SCALE BENCHMARK COMPLETE ===")
    print(f"Agents Modeled  : {num_agents:,}")
    print(f"Simulation Steps: {steps}")
    print(f"Execution Time  : {elapsed:.3f}s ({elapsed/steps*1000:.2f} ms/step)")
    print(f"Final Health    : {health:.2f}%")
    print("Telemetry saved : simulation_results.json")

if __name__ == "__main__":
    run_vectorized_benchmark(num_agents=500000, steps=100)
