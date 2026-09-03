import sys
import subprocess

def main_menu():
    while True:
        print("\n==========================================")
        print("      EKATVA ALIGNMENT FRAMEWORK CLI      ")
        print("==========================================")
        print("1. Run Ecosystem Simulation (10 Agents)")
        print("2. Analyze Telemetry (simulation_results.json)")
        print("3. Launch Hyperparameter Tuner")
        print("4. Execute Unit Test Suite")
        print("5. Exit")
        print("------------------------------------------")
        
        choice = input("Select an option (1-5): ").strip()
        
        if choice == "1":
            subprocess.run(["python3", "multi_agent_enforced.py"])
        elif choice == "2":
            subprocess.run(["python3", "analyze_telemetry.py"])
        elif choice == "3":
            subprocess.run(["python3", "ekatva_tuner.py"])
        elif choice == "4":
            subprocess.run(["python3", "test_ekatva.py"])
        elif choice == "5":
            print("Exiting Ekatva CLI.")
            break
        else:
            print("Invalid choice. Please select 1-5.")

if __name__ == "__main__":
    main_menu()
