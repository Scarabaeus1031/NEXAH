import numpy as np

# ============================================================
# GLOBAL CONFIG
# ============================================================

DEFAULT_N = 200
SEED = 42


# ============================================================
# CORE DATA GENERATOR
# ============================================================

def get_phase_data():
    return theta_values, c_values, loop_values, gh_mask

def generate_phase_data(N=DEFAULT_N, seed=SEED):
    """
    Central data generator for all phase-based analysis.

    Returns:
        theta_values
        c_values
        loop_values
    """

    np.random.seed(seed)

    theta = np.linspace(0, 2*np.pi, N)

    # --- CORE STRUCTURE ---
    # Diese Struktur ist bewusst so gewählt, dass:
    # - mehrere Frequenzen überlagert werden
    # - GH-Korridor entsteht
    # - HEX / 60° sichtbar bleibt

    c = (
        0.02
        + 0.008 * np.sin(2 * theta)     # global mode
        + 0.004 * np.sin(6 * theta)     # hex symmetry
        + 0.002 * np.random.randn(N)    # noise
    )

    loops = (
        3
        + 1.5 * np.cos(3 * theta)       # triadic modulation
        + 1.0 * np.cos(6 * theta)       # hex coupling
        + 0.5 * np.random.randn(N)
    )

    return theta, c, loops


# ============================================================
# NORMALIZATION UTILS
# ============================================================

def normalize(x):
    return (x - np.min(x)) / (np.max(x) - np.min(x) + 1e-8)


# ============================================================
# METRICS
# ============================================================

def compute_metrics(theta, c, loops):
    """
    Computes system-level metrics (Entry 19 logic)
    """

    c_norm = normalize(c)
    l_norm = normalize(loops)

    # Flow persistence proxy (smoothness)
    P = 1 - np.mean(np.abs(np.diff(c_norm)))

    # Recurrence proxy (variance)
    R = np.var(c_norm)

    # Loop density
    L = np.mean(loops > np.mean(loops))

    # Coupling
    C = P * R * L

    return {
        "P": P,
        "R": R,
        "L": L,
        "C": C
    }


# ============================================================
# GH CORRIDOR
# ============================================================

def compute_gh_score(c, loops):
    c_norm = normalize(c)
    l_norm = normalize(loops)

    gh = (1 - np.abs(c_norm - 0.5)*2) * (1 - np.abs(l_norm - 0.5)*2)

    return gh


def detect_gh_corridor(theta, c, loops, percentile=75):

    gh = compute_gh_score(c, loops)

    threshold = np.percentile(gh, percentile)
    mask = gh > threshold

    return {
        "gh_score": gh,
        "mask": mask,
        "theta_corridor": theta[mask],
        "c_corridor": c[mask],
        "loops_corridor": loops[mask]
    }


# ============================================================
# LOAD FUNCTION (ENTRY POINT)
# ============================================================

def load_phase_data(N=DEFAULT_N):
    """
    Standard interface for ALL modules
    """

    theta, c, loops = generate_phase_data(N=N)

    return theta, c, loops


# ============================================================
# DEBUG / TEST
# ============================================================

if __name__ == "__main__":

    theta, c, loops = load_phase_data()

    metrics = compute_metrics(theta, c, loops)
    gh = detect_gh_corridor(theta, c, loops)

    print("\n--- PIPELINE TEST ---")
    print(f"C (coupling): {metrics['C']:.6f}")
    print(f"P: {metrics['P']:.4f}, R: {metrics['R']:.4f}, L: {metrics['L']:.4f}")
    print(f"GH points: {len(gh['theta_corridor'])}")
