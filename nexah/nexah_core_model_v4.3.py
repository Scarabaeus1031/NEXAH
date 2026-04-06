import numpy as np
import matplotlib.pyplot as plt


# =========================
# HELPERS
# =========================

def moving_average(x, w):
    if w <= 1:
        return x
    return np.convolve(x, np.ones(w)/w, mode="same")


def classical_detection(voltage, t, threshold=0.7):
    idx = np.where(voltage < threshold)[0]
    return t[idx[0]] if len(idx) > 0 else None


def make_time(T=120.0, dt=0.1):
    return np.arange(0.0, T, dt)


# =========================
# SIGNALS
# =========================

def signal_collapse(t, seed=None):
    rng = np.random.default_rng(seed)
    v = 1.0 / (1.0 + np.exp(0.18 * (t - 73)))
    v += rng.normal(0, 0.002, len(t))
    return v


def signal_stable_flat(t, seed=None):
    rng = np.random.default_rng(seed)
    v = np.ones_like(t)
    v += rng.normal(0, 0.002, len(t))
    return v


def signal_random_walk(t, seed=None):
    rng = np.random.default_rng(seed)
    steps = rng.normal(0, 0.0015, len(t))
    v = 1 + np.cumsum(steps)
    v = np.clip(v, 0.75, 1.05)
    return v


def signal_noise_only(t, seed=None):
    rng = np.random.default_rng(seed)
    return 1 + rng.normal(0, 0.006, len(t))


# =========================
# NEXAH DETECTOR (parametric)
# =========================

def nexah_detect(t, v, deviation_th):

    dv = np.gradient(v, t)
    d2v = np.gradient(dv, t)

    v_s = moving_average(v, 7)
    dv_s = moving_average(dv, 7)
    d2v_s = moving_average(d2v, 7)

    X = np.column_stack([v_s, dv_s, d2v_s])

    base = t < 50
    mu = np.mean(X[base], axis=0)
    cov = np.cov(X[base].T) + 1e-6*np.eye(3)
    inv = np.linalg.inv(cov)

    diff = X - mu
    dist = np.sqrt(np.einsum("ij,jk,ik->i", diff, inv, diff))
    dist = moving_average(dist, 9)

    z = (dist - np.mean(dist[base])) / (np.std(dist[base]) + 1e-8)
    z = moving_average(z, 9)

    for i in range(len(t)):
        if t[i] < 10:
            continue

        if v[i] < 0.95 and z[i] > deviation_th:
            return t[i]

    return None


# =========================
# ROC TEST
# =========================

def evaluate_threshold(th, n_runs=20):

    t = make_time()

    # collapse → TP
    tp = 0
    for i in range(n_runs):
        v = signal_collapse(t, seed=100+i)
        if nexah_detect(t, v, th) is not None:
            tp += 1

    # non-collapse → FP
    fp = 0
    total_neg = 0

    generators = [
        signal_stable_flat,
        signal_noise_only,
        signal_random_walk
    ]

    for g in generators:
        for i in range(n_runs):
            v = g(t, seed=200+i)
            if nexah_detect(t, v, th) is not None:
                fp += 1
            total_neg += 1

    TPR = tp / n_runs
    FPR = fp / total_neg

    return TPR, FPR


# =========================
# MAIN
# =========================

if __name__ == "__main__":

    thresholds = np.linspace(2.0, 4.5, 12)

    TPRs = []
    FPRs = []

    print("\n=== NEXAH v4.3 ROC Sweep ===\n")

    for th in thresholds:
        TPR, FPR = evaluate_threshold(th)

        TPRs.append(TPR)
        FPRs.append(FPR)

        print(f"th={th:.2f} | TPR={TPR:.2f} | FPR={FPR:.2f}")

    # =========================
    # PLOT ROC
    # =========================

    plt.figure(figsize=(6,6))
    plt.plot(FPRs, TPRs, marker="o")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("NEXAH ROC Curve (v4.3)")
    plt.grid()
    plt.show()

    # =========================
    # PLOT THRESHOLD CURVE
    # =========================

    plt.figure(figsize=(8,4))
    plt.plot(thresholds, TPRs, label="TPR")
    plt.plot(thresholds, FPRs, label="FPR")
    plt.xlabel("deviation threshold")
    plt.ylabel("rate")
    plt.title("Threshold Sensitivity")
    plt.legend()
    plt.grid()
    plt.show()
