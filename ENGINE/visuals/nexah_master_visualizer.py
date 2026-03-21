import numpy as np
import matplotlib.pyplot as plt

from ENGINE.analysis.stability_landscape_generator import generate_stability_landscape

SIZE = 50

# --------------------------------------------------
# SIMPLE FLOW FIELD
# --------------------------------------------------

def compute_flow(field):
    gx, gy = np.gradient(field)
    return -gx, -gy

# --------------------------------------------------
# RECURRENCE MAP
# --------------------------------------------------

def compute_recurrence(paths):
    rec = np.zeros((SIZE, SIZE))

    for path in paths:
        start = path[0]
        for p in path[80:]:
            if np.linalg.norm(p - start) < 1.5:
                x, y = int(p[0]), int(p[1])
                rec[x % SIZE, y % SIZE] += 1

    return rec / (np.max(rec) + 1e-6)

# --------------------------------------------------
# DUMMY PATHS (for testing)
# --------------------------------------------------

def generate_dummy_paths(n=50):
    paths = []
    for _ in range(n):
        path = []
        pos = np.array([np.random.rand()*SIZE, np.random.rand()*SIZE])

        for _ in range(150):
            step = np.random.randn(2)
            pos = (pos + step) % SIZE
            path.append(pos.copy())

        paths.append(np.array(path))
    return paths

# --------------------------------------------------
# MAIN VISUAL
# --------------------------------------------------

def plot_master():

    field = generate_stability_landscape()
    field /= np.max(field)

    flow_x, flow_y = compute_flow(field)

    paths = generate_dummy_paths()
    rec = compute_recurrence(paths)

    plt.figure(figsize=(16,10))

    # ------------------------------------------
    # 1. FIELD
    # ------------------------------------------
    plt.subplot(2,2,1)
    plt.title("Base Field (Potential Landscape)")
    plt.imshow(field, origin="lower")
    plt.colorbar()
    plt.axis("off")

    # ------------------------------------------
    # 2. FLOW FIELD
    # ------------------------------------------
    plt.subplot(2,2,2)
    plt.title("Flow Field (Gradient Dynamics)")
    plt.imshow(field, origin="lower", alpha=0.6)

    step = 3
    X, Y = np.meshgrid(np.arange(0,SIZE,step), np.arange(0,SIZE,step))

    plt.quiver(
        Y, X,
        flow_y[::step, ::step],
        flow_x[::step, ::step],
        color='white',
        alpha=0.8
    )

    plt.axis("off")

    # ------------------------------------------
    # 3. TRAJECTORIES
    # ------------------------------------------
    plt.subplot(2,2,3)
    plt.title("Agent Trajectories")

    for path in paths[:40]:
        plt.plot(path[:,0], path[:,1], alpha=0.2)

    plt.xlim(0,SIZE)
    plt.ylim(0,SIZE)
    plt.axis("off")

    # ------------------------------------------
    # 4. RECURRENCE
    # ------------------------------------------
    plt.subplot(2,2,4)
    plt.title("Recurrence Map (Loop Density)")
    plt.imshow(rec, origin="lower", cmap="magma")
    plt.colorbar()
    plt.axis("off")

    plt.tight_layout()
    plt.show()

# --------------------------------------------------

if __name__ == "__main__":
    plot_master()
