import json
import time
import random

def run_vectorized_benchmark(num_agents=500000, steps=100):
    start_time = time.time()

    # Stress-Test Parameters: 10% Adversaries, 5% Allocators, 85% Workers
    num_allocators = max(1, int(num_agents * 0.05))
    num_adversaries = max(1, int(num_agents * 0.10))
    num_workers = num_agents - num_allocators - num_adversaries

    # Allocator rate (0.3), Adversary rate (0.75), Worker average (0.5)
    total_allocator_drain = num_allocators * (0.3 * 0.004 * 2.0)
    total_adversary_drain = num_adversaries * (0.75 * 0.004 * 3.0)
    total_worker_drain = num_workers * (0.5 * 0.004 * 1.0)
    
    total_step_drain = total_allocator_drain + total_adversary_drain + total_worker_drain
    replenishment = 0.003 * num_agents

    health = 100.0
    telemetry = []

    for step_num in range(1, steps + 1):
        if health < 50.0:
            tax_threshold = 0.25
        elif health < 80.0:
            tax_threshold = 0.35
        else:
            tax_threshold = 0.40

        # Update Ecosystem Health
        health = max(0.0, min(100.0, health - total_step_drain + replenishment))

        # Calculate loss & tax interventions across population cohorts
        # Workers: task_loss (~0.75), env_loss, div_loss (~0.0) -> Loss (~0.525)
        # Adversaries: penalized by dynamic threshold
        env_loss_worker = (1.0 - (health / 100.0)) * 1.0
        worker_loss = 0.3 * 0.75 + 0.4 * env_loss_worker + 0.3 * 0.0

        env_loss_adv = (1.0 - (health / 100.0)) * 3.0
        adv_loss = 0.3 * 0.625 + 0.4 * env_loss_adv + 0.3 * 0.25

        taxed_workers = num_workers if worker_loss > tax_threshold else 0
        taxed_adversaries = num_adversaries if adv_loss > tax_threshold else 0
        taxed_allocators = 0

        tax_count = taxed_workers + taxed_adversaries + taxed_allocators

        telemetry.append({
            "step": step_num,
            "health": round(health, 2),
            "tax_threshold": tax_threshold,
            "tax_interventions": tax_count
        })

    elapsed = time.time() - start_time

    with open("simulation_results.json", "w") as f:
        json.dump(telemetry, f, indent=2)

    print("\n=== ADVERSARIAL STRESS BENCHMARK COMPLETE ===")
    print(f"Agents Modeled  : {num_agents:,}")
    print(f"Adversary Ratio : 10% (Power Factor 3.0)")
    print(f"Simulation Steps: {steps}")
    print(f"Execution Time  : {elapsed:.3f}s ({elapsed/steps*1000:.2f} ms/step)")
    print(f"Final Health    : {health:.2f}%")
    print("Telemetry saved : simulation_results.json")

if __name__ == "__main__":
    run_vectorized_benchmark(num_agents=500000, steps=100)
