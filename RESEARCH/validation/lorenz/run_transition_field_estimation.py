import numpy as np
import matplotlib.pyplot as plt

# ============================
# Lorenz system
# ============================

def lorenz(x, y, z, s=10, r=28, b=8/3):
    return s*(y-x), x*(r-z)-y, x*y - b*z

def simulate_lorenz(steps=5000, dt=0.01):
    xs = np.zeros((steps,3))
    xs[0] = [0.0, 1.0, 1.05]
    for i in range(steps-1):
        dx = lorenz(*xs[i])
        xs[i+1] = xs[i] + dt*np.array(dx)
    return xs

# ============================
# Field estimation
# ============================

def estimate_field(data, grid_size=40):

    x = data[:,0]
    y = data[:,1]

    vx = np.diff(x)
    vy = np.diff(y)

    x = x[:-1]
    y = y[:-1]

    xmin, xmax = x.min(), x.max()
    ymin, ymax = y.min(), y.max()

    gx = np.linspace(xmin, xmax, grid_size)
    gy = np.linspace(ymin, ymax, grid_size)

    field_x = np.zeros((grid_size, grid_size))
    field_y = np.zeros((grid_size, grid_size))
    counts = np.zeros((grid_size, grid_size))

    for i in range(len(x)):
        ix = np.searchsorted(gx, x[i]) - 1
        iy = np.searchsorted(gy, y[i]) - 1

        if 0 <= ix < grid_size and 0 <= iy < grid_size:
            field_x[iy, ix] += vx[i]
            field_y[iy, ix] += vy[i]
            counts[iy, ix] += 1

    mask = counts > 0
    field_x[mask] /= counts[mask]
    field_y[mask] /= counts[mask]

    return gx, gy, field_x, field_y

# ============================
# Main
# ============================

def main():

    print("⚡ NEXAH — Transition Field Estimation")

    data = simulate_lorenz()

    gx, gy, fx, fy = estimate_field(data)

    X, Y = np.meshgrid(gx, gy)

    plt.figure(figsize=(8,6))
    plt.quiver(X, Y, fx, fy)
    plt.title("Estimated Flow Field (Lorenz)")
    plt.savefig("RESEARCH/validation/lorenz/results/transition_field.png")
    plt.close()

    print("✅ Saved: transition_field.png")


if __name__ == "__main__":
    main()
