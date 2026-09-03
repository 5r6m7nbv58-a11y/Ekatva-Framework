import json

def analyze():
    try:
        with open("simulation_results.json", "r") as f:
            data = json.load(f)
        
        steps = len(data)
        avg_health = sum(d["health"] for d in data) / steps
        total_taxes = sum(d["tax_interventions"] for d in data)
        max_taxes_in_step = max(d["tax_interventions"] for d in data)
        
        print("\n=== SIMULATION TELEMETRY SUMMARY ===")
        print(f"Total Steps Evaluated : {steps}")
        print(f"Average Ecosystem Health: {avg_health:.2f}%")
        print(f"Total Tax Interventions : {total_taxes}")
        print(f"Peak Tax Interventions  : {max_taxes_in_step} agents/step")
        print(f"Final Health State      : {data[-1]['health']}%\n")
    except FileNotFoundError:
        print("Error: simulation_results.json not found. Run multi_agent_enforced.py first.")

if __name__ == "__main__":
    analyze()
