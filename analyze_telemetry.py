import json

def analyze():
    try:
        with open("simulation_results.json", "r") as f:
            data = json.load(f)
        
        steps = len(data)
        avg_health = sum(d["health"] for d in data) / steps
        total_taxes = sum(d["tax_interventions"] for d in data)
        threshold_shifts = set(d["tax_threshold"] for d in data)
        
        print("\n=== ADVANCED EKATVA TELEMETRY SUMMARY ===")
        print(f"Total Steps Evaluated   : {steps}")
        print(f"Average Ecosystem Health: {avg_health:.2f}%")
        print(f"Final Health State      : {data[-1]['health']}%")
        print(f"Total Tax Interventions : {total_taxes}")
        print(f"Active Tax Thresholds   : {sorted(list(threshold_shifts))}\n")
    except FileNotFoundError:
        print("Error: simulation_results.json not found.")

if __name__ == "__main__":
    analyze()
