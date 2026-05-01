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
# Instability field
# ============================

def estimate_instability_field(data, grid_size=40):

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

    vel_list = [[[] for _ in range(grid_size)] for _ in range(grid_size)]

    for i in range(len(x)):
        ix = np.searchsorted(gx, x[i]) - 1
        iy = np.searchsorted(gy, y[i]) - 1

        if 0 <= ix < grid_size and 0 <= iy < grid_size:
            vel_list[iy][ix].append([vx[i], vy[i]])

    instability = np.zeros((grid_size, grid_size))

    for i in range(grid_size):
        for j in range(grid_size):
            v = np.array(vel_list[i][j])
            if len(v) > 1:
                instability[i,j] = np.var(v)
            else:
                instability[i,j] = 0

    return gx, gy, instability

# ============================
# Main
# ============================

def main():

    print("⚡ NEXAH — Instability Field Estimation")

    data = simulate_lorenz()

    gx, gy, inst = estimate_instability_field(data)

    plt.figure(figsize=(8,6))
    plt.imshow(inst, cmap="inferno", origin="lower")
    plt.colorbar(label="instability")
    plt.title("Instability Field (Lorenz)")
    plt.savefig("RESEARCH/validation/lorenz/results/instability_field.png")
    plt.close()

    print("✅ Saved: instability_field.png")


if __name__ == "__main__":
    main()
