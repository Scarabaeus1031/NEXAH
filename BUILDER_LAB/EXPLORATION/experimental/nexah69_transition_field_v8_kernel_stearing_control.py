import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from pathlib import Path

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

BASE_PATH = Path("APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs")
CASE = "ieee118"

GRID_RES = 45
BINS = 28

FPS = 25
FRAME_SKIP = 2
MAX_FRAMES = 700
PRED_STEPS = 40

ALPHA_LEARNED = 0.7
ALPHA_RETURN = 0.1
ALPHA_GATE = 0.7
ALPHA_PHASE = 0.5
ALPHA_CONTROL = 1.2   # 🔥 neu

# --------------------------------------------------
# LOAD
# --------------------------------------------------

def load_dataset(case):
    return pd.read_csv(BASE_PATH / f"{case}_v43_dataset.csv").dropna()

def load_off_field(case):
    return pd.read_csv(BASE_PATH / f"{case}_v68_off_manifold_cloud.csv").dropna()

# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def normalize_safe(x):
    x = np.asarray(x, dtype=float)
    m = np.max(np.abs(x))
    return x if m == 0 else x / m

def nearest_traj_point(px, py, traj):
    diff = traj - np.array([px, py])
    idx = np.argmin(np.sum(diff**2, axis=1))
    return idx, traj[idx]

def local_tangent(traj, idx):
    if idx <= 0:
        v = traj[1] - traj[0]
    elif idx >= len(traj) - 1:
        v = traj[-1] - traj[-2]
    else:
        v = traj[idx + 1] - traj[idx - 1]

    n = np.linalg.norm(v)
    return v / n if n > 0 else np.zeros(2)

def estimate_phase(traj):
    return np.unwrap(np.arctan2(traj[:, 1], traj[:, 0]))

def compute_phase_velocity(theta):
    return np.gradient(theta)

def estimate_density(px, py, traj, k=25):
    diff = traj - np.array([px, py])
    dist = np.sqrt(np.sum(diff**2, axis=1))
    k = min(k, len(dist))
    return np.exp(-np.mean(np.sort(dist)[:k]))

# --------------------------------------------------
# LEARNED FIELD
# --------------------------------------------------

def build_transition_model(traj):
    x = traj[:, 0]
    y = traj[:, 1]

    x_bins = np.linspace(x.min(), x.max(), BINS)
    y_bins = np.linspace(y.min(), y.max(), BINS)

    dx = np.gradient(x)
    dy = np.gradient(y)

    model = {}

    for t in range(len(traj) - 1):
        xi = np.digitize(x[t], x_bins)
        yi = np.digitize(y[t], y_bins)

        v = np.array([dx[t], dy[t]])
        n = np.linalg.norm(v)
        if n == 0:
            continue

        key = (xi, yi)
        model.setdefault(key, []).append(v / n)

    learned = {}
    for key, values in model.items():
        m = np.mean(values, axis=0)
        n = np.linalg.norm(m)
        learned[key] = m / n if n > 0 else np.zeros(2)

    return learned, x_bins, y_bins

def learned_vector(px, py, model, xb, yb):
    xi = np.digitize(px, xb)
    yi = np.digitize(py, yb)
    return model.get((xi, yi), np.zeros(2))

# --------------------------------------------------
# HYBRID + CONTROL VECTOR
# --------------------------------------------------

def hybrid_control_vector(px, py, traj, theta, omega, model, xb, yb, target):

    idx, nearest = nearest_traj_point(px, py, traj)
    tangent = local_tangent(traj, idx)

    learned = learned_vector(px, py, model, xb, yb)
    return_vec = nearest - np.array([px, py])

    density = estimate_density(px, py, traj)
    gate = 1.0 - density

    mean_omega = np.mean(omega)
    mismatch = abs(omega[idx] - mean_omega)

    perp = np.array([-tangent[1], tangent[0]])

    gate_vec = gate * perp
    phase_vec = mismatch * perp

    # 🎯 CONTROL TERM
    control_vec = target - np.array([px, py])

    vec = (
        ALPHA_LEARNED * learned
        + ALPHA_RETURN * return_vec
        + ALPHA_GATE * gate_vec
        + ALPHA_PHASE * phase_vec
        + ALPHA_CONTROL * control_vec
    )

    n = np.linalg.norm(vec)
    return vec / n if n > 0 else vec

# --------------------------------------------------
# SIMULATION
# --------------------------------------------------

def simulate_control(start, traj, theta, omega, model, xb, yb, target):
    p = start.copy()
    path = [p.copy()]

    for _ in range(PRED_STEPS):
        v = hybrid_control_vector(p[0], p[1], traj, theta, omega, model, xb, yb, target)
        p = p + 0.03 * v
        path.append(p.copy())

    return np.array(path)

# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    print("🚀 NEXAH V8 — CONTROL KERNEL")

    df = load_dataset(CASE)
    cloud = load_off_field(CASE)

    c = normalize_safe(df["c"].values)
    dc = normalize_safe(df["dc"].values)

    traj = np.column_stack([c, dc])

    theta = estimate_phase(traj)
    omega = compute_phase_velocity(theta)

    model, xb, yb = build_transition_model(traj)

    xmin, xmax = cloud["c"].min(), cloud["c"].max()
    ymin, ymax = cloud["dc"].min(), cloud["dc"].max()

    xs = np.linspace(xmin, xmax, GRID_RES)
    ys = np.linspace(ymin, ymax, GRID_RES)
    X, Y = np.meshgrid(xs, ys)

    # 🎯 Target (frei wählbar!)
    target = np.array([0.5*(xmin+xmax), 0.5*(ymin+ymax)])

    fig, ax = plt.subplots(figsize=(7,7))
    ax.set_facecolor("black")
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_xticks([]); ax.set_yticks([])

    trail, = ax.plot([], [], color="white", lw=2)
    control_path, = ax.plot([], [], color="cyan", lw=2)
    point = ax.scatter([], [], color="white", s=40)
    target_plot = ax.scatter(*target, color="red", s=80)

    title = ax.text(0.5, 1.02, "", transform=ax.transAxes,
                    ha="center", color="white")

    def update(frame):
        idx = min(frame * FRAME_SKIP + 20, len(traj)-1)
        sub = traj[:idx]

        sub_theta = estimate_phase(sub)
        sub_omega = compute_phase_velocity(sub_theta)

        sub_model, xb2, yb2 = build_transition_model(sub)

        trail.set_data(sub[:,0], sub[:,1])

        current = sub[-1]
        future = simulate_control(current, sub, sub_theta, sub_omega, sub_model, xb2, yb2, target)

        control_path.set_data(future[:,0], future[:,1])
        point.set_offsets([current])

        title.set_text(f"NEXAH V8 Control — t={idx}")

        return trail, control_path, point, title

    frames = min(len(traj)//FRAME_SKIP, MAX_FRAMES)

    anim = FuncAnimation(fig, update, frames=frames, interval=40)

    out = BASE_PATH / f"{CASE}_v8_control_kernel.gif"
    anim.save(out, writer="pillow", fps=FPS)

    print(f"[OK] saved → {out}")

if __name__ == "__main__":
    main()
