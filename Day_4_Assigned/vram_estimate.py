def estimate(parameters_b, context_k, bytes_per_param):
    weights_gb = parameters_b * bytes_per_param
    kv_cache_gb = parameters_b * context_k * 0.02
    total_gb = (weights_gb + kv_cache_gb) * 1.10

    return weights_gb, kv_cache_gb, total_gb


def verdict(total_gb, memory_budget_gb):
    if total_gb <= memory_budget_gb * 0.8:
        return "Fits comfortably"
    elif total_gb <= memory_budget_gb:
        return "Fits but tight"
    else:
        return "Does not fit"


def report(name, parameters_b, context_k, bytes_per_param, memory_budget_gb):
    weights, kv_cache, total = estimate(
        parameters_b,
        context_k,
        bytes_per_param
    )

    print(f"\nModel: {name}")
    print(f"Weights: {weights:.2f} GB")
    print(f"KV Cache: {kv_cache:.2f} GB")
    print(f"Total: {total:.2f} GB")
    print(f"Verdict: {verdict(total, memory_budget_gb)}")


if __name__ == "__main__":

    memory_budget = 8

    report(
        "1.5B Q4_K_M 8K",
        1.5,
        8,
        0.57,
        memory_budget
    )

    report(
        "8B Q4_K_M 8K",
        8,
        8,
        0.57,
        memory_budget
    )

    report(
        "8B FP16 8K",
        8,
        8,
        2.00,
        memory_budget
    )

    report(
        "30B Q4_K_M 8K",
        30,
        8,
        0.57,
        memory_budget
    )

print("\n--- Context Length Experiment ---")

contexts = [4, 8, 32, 128]

for context in contexts:
    weights, kv_cache, total = estimate(
        8,
        context,
        0.57
    )

    print(
        f"8B Q4_K_M | {context}K context "
        f"| Weights: {weights:.2f} GB "
        f"| KV Cache: {kv_cache:.2f} GB "
        f"| Total: {total:.2f} GB"
    )

print("\n--- Quantization Experiment ---")

quantizations = {
    "Q3_K_M": 0.43,
    "Q4_K_M": 0.57,
    "Q5_K_M": 0.68,
    "Q8_0": 1.00,
    "FP16": 2.00
}

for quantization, bytes_per_param in quantizations.items():
    weights, kv_cache, total = estimate(
        8,
        8,
        bytes_per_param
    )

    print(
        f"8B {quantization} | "
        f"Weights: {weights:.2f} GB | "
        f"KV Cache: {kv_cache:.2f} GB | "
        f"Total: {total:.2f} GB"
    )