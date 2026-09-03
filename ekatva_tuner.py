import sys
from multi_agent_enforced import EnforcedEcosystem, Agent

def run_tuner():
    print("=== EKATVA HYPERPARAMETER TUNER ===")
    try:
        alpha = float(input("Enter Task Weight (alpha) [default 0.3]: ") or 0.3)
        beta = float(input("Enter Env Weight (beta) [default 0.4]: ") or 0.4)
        gamma = float(input("Enter Div Weight (gamma) [default 0.3]: ") or 0.3)
    except ValueError:
        print("Invalid input. Using defaults.")
        alpha, beta, gamma = 0.3, 0.4, 0.3

    total = alpha + beta + gamma
    print(f"\nNormalized Weights -> alpha: {alpha/total:.2f}, beta: {beta/total:.2f}, gamma: {gamma/total:.2f}\n")

if __name__ == "__main__":
    run_tuner()
