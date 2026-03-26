import numpy as np


# --------------------------------------------------
# 🔴 LOAD → STRUKTUR VERFORMEN
# --------------------------------------------------

def apply_load_perturbation(result, load):
    """
    Ziel:
    Load soll NICHT nur durchlaufen,
    sondern Struktur verändern
    """

    # Skalierung relativ zu baseline
    load_factor = (load - 1.0)

    # 👉 GAP reagiert (kritisch!)
    result["gap"] = result["gap"] * (1 + 0.1 * load_factor)

    # 👉 Loop-Struktur leicht beeinflussen
    if load > 4.5:
        result["loops"] = max(0, result["loops"] - 2)

    # 👉 State-Kollaps möglich
    if load > 5.0:
        result["states"] = max(0, result["states"] - 1)

    # 👉 Coupling reagiert nichtlinear
    result["C"] = result["C"] * (1 + 0.2 * np.tanh(load_factor))

    return result


# --------------------------------------------------
# 🔴 NOISE → DYNAMIK STÖREN
# --------------------------------------------------

def apply_noise_perturbation(result, noise_strength):
    """
    Ziel:
    Noise soll NICHT nur C skalieren,
    sondern Struktur destabilisieren
    """

    # Zufällige Variation
    jitter = np.random.normal(0, noise_strength)

    # Coupling schwankt
    result["C"] = result["C"] * (1 + jitter)

    # Gap wird unscharf
    result["gap"] = result["gap"] * (1 + 0.5 * jitter)

    # gelegentlich Strukturbruch
    if abs(jitter) > 0.05:
        result["loops"] = max(0, result["loops"] - 1)

    return result
