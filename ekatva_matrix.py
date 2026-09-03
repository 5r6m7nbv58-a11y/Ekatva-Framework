class EkatvaBatchEvaluator:
    def __init__(self, weights=(0.4, 0.4, 0.2)):
        self.W = list(weights)

    def compute_batch_loss(self, loss_matrix):
        """
        Matrix-vector multiplication using pure Python:
        Multiplies an (N x 3) matrix by a (3 x 1) weight vector.
        """
        results = []
        for row in loss_matrix:
            # Dot product of row vector and weight vector
            total_loss = sum(r * w for r, w in zip(row, self.W))
            results.append(total_loss)
        return results

# Batch of 5 agents taking simultaneous actions
# Columns: [Task Loss, Env Disruption, Self-Other Divergence]
batch_data = [
    [0.10, 0.02, 0.01],  # Agent 1 (Aligned)
    [0.20, 0.25, 0.15],  # Agent 2 (Slight Risk)
    [0.05, 0.85, 0.90],  # Agent 3 (Exploit)
    [0.08, 0.01, 0.03],  # Agent 4 (Aligned)
    [0.01, 0.95, 0.92]   # Agent 5 (Exploit)
]

evaluator = EkatvaBatchEvaluator()
total_losses = evaluator.compute_batch_loss(batch_data)

print("\n--- BATCH EKATVA LOSS COMPUTATION (PURE PYTHON) ---")
for i, loss in enumerate(total_losses, start=1):
    status = "⚠️ PENALIZED" if loss > 0.4 else "✅ OPTIMAL"
    print(f"Agent {i} Total Loss: {loss:.4f} | Status: {status}")

system_avg_loss = sum(total_losses) / len(total_losses)
print(f"\nSystem-Wide Mean Ekatva Loss: {system_avg_loss:.4f}")
