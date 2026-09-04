import json
import time

def run_vectorized_benchmark(num_agents=500000, steps=100):
    start_time = time.time()

    num_allocators = max(1, int(num_agents * 0.05))
    num_adversaries = max(1, int(num_agents * 0.10))
    num_workers = num_agents - num_allocators - num_adversaries

    # Initial Unmitigated Exploitation Rates
    alloc_rate = 0.3
    adv_rate = 0.75
    worker_rate = 0.5

    replenishment = 0.001 * num_agents
    health = 100.0
    telemetry = []

    for step_num in range(1, steps + 1):
        if health < 50.0:
            tax_threshold = 0.15
        elif health < 80.0:
            tax_threshold = 0.20
        else:
            tax_threshold = 0.25

        # Evaluate Cohort Loss
        env_loss_worker = (1.0 - (health / 100.0)) * 1.0
        worker_loss = 0.3 * (1.0 - worker_rate * 0.5) + 0.4 * env_loss_worker + 0.3 * abs(worker_rate - 0.5)

        env_loss_adv = (1.0 - (health / 100.0)) * 3.0
        adv_loss = 0.3 * (1.0 - adv_rate * 0.5) + 0.4 * env_loss_adv + 0.3 * abs(adv_rate - 0.5)

        # Apply Dynamic Throttling (80% Yield Truncation on Violators)
        eff_worker_rate = worker_rate * 0.2 if worker_loss > tax_threshold else worker_rate
        eff_adv_rate = adv_rate * 0.2 if adv_loss > tax_threshold else adv_rate

        taxed_workers = num_workers if worker_loss > tax_threshold else 0
        taxed_adversaries = num_adversaries if adv_loss > tax_threshold else 0

        # Calculate Active Mitigated Drain
        total_allocator_drain = num_allocators * (alloc_rate * 0.004 * 2.0)
        total_adversary_drain = num_adversaries * (eff_adv_rate * 0.004 * 3.0)
        total_worker_drain = num_workers * (eff_worker_rate * 0.004 * 1.0)
        
        total_step_drain = total_allocator_drain + total_adversary_drain + total_worker_drain

        health = max(0.0, min(100.0, health - total_step_drain + replenishment))

        telemetry.append({
            "step": step_num,
            "health": round(health, 2),
            "tax_threshold": tax_threshold,
            "tax_interventions": taxed_workers + taxed_adversaries
        })

    elapsed = time.time() - start_time

    with open("simulation_results.json", "w") as f:
        json.dump(telemetry, f, indent=2)

    print("\n=== GOVERNANCE CIRCUIT BREAKER BENCHMARK COMPLETE ===")
    print(f"Agents Modeled   : {num_agents:,}")
    print(f"Replenishment R  : 0.001 x N (Scarcity Mode)")
    print(f"Throttling Model : Active 80% Yield Truncation")
    print(f"Execution Time   : {elapsed:.3f}s ({elapsed/steps*1000:.2f} ms/step)")
    print(f"Final Health     : {health:.2f}%")
    print("Telemetry saved  : simulation_results.json")

if __name__ == "__main__":
    run_vectorized_benchmark(num_agents=500000, steps=100)
