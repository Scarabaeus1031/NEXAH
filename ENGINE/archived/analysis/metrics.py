import numpy as np

def compute_metrics(field, memory=None):

    field = field / (np.max(field) + 1e-9)

    entropy = -np.sum(field * np.log(field + 1e-9))
    peak = np.max(field)
    spread = np.std(field)

    metrics = {
        "entropy": float(entropy),
        "peak": float(peak),
        "spread": float(spread)
    }

    if memory is not None:
        memory_strength = np.sum(memory)
        metrics["memory"] = float(memory_strength)

    return metrics
