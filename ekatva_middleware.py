import time

class EkatvaAPIMiddleware:
    def __init__(self, base_token_limit=4096):
        self.base_token_limit = base_token_limit
        self.system_health = 100.0  # Shared cluster capacity pool

    def compute_request_loss(self, task_priority, tokens_requested):
        l_task = max(0.0, 1.0 - task_priority)
        l_env = 1.0 - (self.system_health / 100.0)
        l_div = min(1.0, tokens_requested / self.base_token_limit)
        return 0.3 * l_task + 0.4 * l_env + 0.3 * l_div

    def process_api_request(self, agent_id, task_priority, requested_tokens):
        loss = self.compute_request_loss(task_priority, requested_tokens)
        
        # Dynamic tax threshold scaling
        threshold = 0.25 if self.system_health < 50.0 else 0.40

        if loss > threshold:
            allocated_tokens = int(requested_tokens * 0.20)  # 80% token restriction
            delay = round((loss - threshold) * 2.0, 2)
            time.sleep(delay)
            status = f"THROTTLED ({delay}s latency penalty, 80% token tax)"
        else:
            allocated_tokens = requested_tokens
            status = "APPROVED"

        # Simulate system load decay
        self.system_health = max(0.0, self.system_health - (requested_tokens / self.base_token_limit) * 0.5)

        return {
            "agent_id": agent_id,
            "loss": round(loss, 4),
            "allocated_tokens": allocated_tokens,
            "status": status,
            "remaining_health": round(self.system_health, 2)
        }

if __name__ == "__main__":
    mw = EkatvaAPIMiddleware()
    print("--- SIMULATING LIVE LLM API REQUEST ROUTER ---")
    res1 = mw.process_api_request("Agent_A", task_priority=0.9, requested_tokens=1024)
    print(f"Req 1 (Normal)   : {res1}")
    
    # Degrade health artificial simulation
    mw.system_health = 45.0
    res2 = mw.process_api_request("Adversary_Agent", task_priority=0.2, requested_tokens=4096)
    print(f"Req 2 (Throttled): {res2}")
