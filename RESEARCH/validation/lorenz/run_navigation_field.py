import numpy as np
import matplotlib.pyplot as plt

# ============================
# Lorenz system
# ============================

def lorenz(x, y, z, s=10, r=28, b=8/3):
    return s*(y-x), x*(r-z)-y, x*y - b*z

def simulate_lorenz(steps=8000, dt=0.01):
    xs = np.zeros((steps,3))
    xs[0] = [0.0, 1.0, 1.05]
    for i in range(steps-1):
        dx = lorenz(*xs[i])
        xs[i+1] = xs[i] + dt*np.array(dx)
    return xs

# ============================
# Combined Field Estimation
# ============================

def estimate_fields(data, grid_size=40):

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

    vel_list = [[[] for _ in range(grid_size)] for _ in range(grid_size)]

    for i in range(len(x)):
        ix = np.searchsorted(gx, x[i]) - 1
        iy = np.searchsorted(gy, y[i]) - 1

        if 0 <= ix < grid_size and 0 <= iy < grid_size:
            field_x[iy, ix] += vx[i]
            field_y[iy, ix] += vy[i]
            counts[iy, ix] += 1
            vel_list[iy][ix].append([vx[i], vy[i]])

    # Normalize flow
    mask = counts > 0
    field_x[mask] /= counts[mask]
    field_y[mask] /= counts[mask]

    # Instability
    instability = np.zeros((grid_size, grid_size))

    for i in range(grid_size):
        for j in range(grid_size):
            v = np.array(vel_list[i][j])
            if len(v) > 1:
                instability[i,j] = np.var(v)

    return gx, gy, field_x, field_y, instability

# ============================
# Main
# ============================

def main():

    print("⚡ NEXAH — Navigation Field")

    data = simulate_lorenz()

    gx, gy, fx, fy, inst = estimate_fields(data)

    X, Y = np.meshgrid(gx, gy)

    # Normalize arrows for visualization
    mag = np.sqrt(fx**2 + fy**2) + 1e-8
    fxn = fx / mag
    fyn = fy / mag

    plt.figure(figsize=(10,8))

    # Instability heatmap
    plt.imshow(inst, cmap="inferno", origin="lower",
               extent=[gx.min(), gx.max(), gy.min(), gy.max()],
               alpha=0.85)

    # Flow field
    plt.quiver(X, Y, fxn, fyn, color="white", scale=40)

    plt.title("NEXAH Navigation Field (Lorenz)")
    plt.colorbar(label="instability")

    plt.savefig("RESEARCH/validation/lorenz/results/navigation_field.png")
    plt.close()

    print("✅ Saved: navigation_field.png")


if __name__ == "__main__":
    main()
