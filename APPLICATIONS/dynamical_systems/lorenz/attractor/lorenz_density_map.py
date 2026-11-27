"""
NEXAH Lorenz Density Map

Computes a density map of the Lorenz attractor by projecting
trajectory points into a 2D histogram (X-Z plane).

Outputs:

APPLICATIONS/outputs/lorenz_density/

Files:
- lorenz_density_map.png
- lorenz_density.csv
- lorenz_density_record.npz
"""

import argparse
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
from matplotlib.patches import Rectangle
from matplotlib.ticker import MaxNLocator
from scipy.integrate import odeint


# ---------------------------------------------------
# Output folder
# ---------------------------------------------------

OUTPUT_DIR = "APPLICATIONS/outputs/lorenz_density"


# ---------------------------------------------------
# Lorenz system
# ---------------------------------------------------

def lorenz(state, t, sigma=10.0, rho=28.0, beta=8/3):
    x, y, z = state
    return [
        sigma * (y - x),
        x * (rho - z) - y,
        x * y - beta * z
    ]


# ---------------------------------------------------
# Generate trajectory
# ---------------------------------------------------

def generate_trajectory(steps=60000):  # leicht reduziert für schnellere Demo
    print("→ Generating trajectory...")

    t = np.linspace(0, 60, steps)

    traj = odeint(
        lorenz,
        [1.0, 1.0, 1.0],
        t
    )

    return traj


# ---------------------------------------------------
# Density calculation
# ---------------------------------------------------

def compute_density(traj, bins=300):  # etwas weniger bins = schneller + cleaner
    print("→ Computing density map...")

    x = traj[:, 0]
    z = traj[:, 2]

    density, xedges, zedges = np.histogram2d(
        x,
        z,
        bins=bins
    )

    # kleine Stabilisierung für spätere Field-Nutzung
    density = density.astype(float)

    return density.T, xedges, zedges


# ---------------------------------------------------
# Save density CSV
# ---------------------------------------------------

def save_density_csv(density):
    path = os.path.join(OUTPUT_DIR, "lorenz_density.csv")

    np.savetxt(path, density, delimiter=",")

    print("Saved:", path)


# ---------------------------------------------------
# Plot density
# ---------------------------------------------------

def draw_density(ax, density, xedges, zedges):
    image = ax.pcolormesh(
        xedges,
        zedges,
        density,
        cmap="inferno",
        shading="flat",
    )
    ax.figure.colorbar(image, ax=ax, label="Density")
    ax.set(xlabel="X", ylabel="Z", title="Lorenz Attractor Density Map")


def plot_density(density, xedges, zedges):
    print("→ Rendering density map...")
    fig, ax = plt.subplots(figsize=(8, 8))
    draw_density(ax, density, xedges, zedges)
    path = os.path.join(OUTPUT_DIR, "lorenz_density_map.png")
    fig.savefig(path, dpi=300)
    plt.close(fig)
    print("Saved:", path)


def bin_index(values, edges):
    """Assign in-range values using histogram2d's inclusive final edge."""
    index = np.searchsorted(edges, values, side="right") - 1
    return np.minimum(index, len(edges) - 2)


def black_egg_view(traj, density, xedges, zedges, *, initial_sample=None):
    x_bins = bin_index(traj[:, 0], xedges)
    z_bins = bin_index(traj[:, 2], zedges)
    samples = np.empty(0, dtype=int)
    selected = 0

    fig = plt.figure(figsize=(12, 7))
    fig.suptitle("Black Egg U-Turn")
    fig.subplots_adjust(left=0.07, right=0.97, bottom=0.09, top=0.87, wspace=0.30, hspace=0.38)
    grid = fig.add_gridspec(2, 2, width_ratios=[1.15, 1], height_ratios=[2, 1])
    map_ax = fig.add_subplot(grid[:, 0])
    record_ax = fig.add_subplot(grid[0, 1], projection="3d")
    order_ax = fig.add_subplot(grid[1, 1])

    draw_density(map_ax, density, xedges, zedges)
    cell = Rectangle(
        (0, 0), 0, 0, fill=False, edgecolor="cyan", linewidth=1.8, visible=False
    )
    map_ax.add_patch(cell)
    map_ax.set_title("X–Z density · click a cell")
    record_ax.set(xlabel="X", ylabel="Y", zlabel="Z", title="3D record · select a cell")
    record_ax.plot(*traj.T, color="0.7", alpha=0.4, linewidth=0.4)
    (cell_points,) = record_ax.plot([], [], [], ".", color="tab:blue")
    (record_point,) = record_ax.plot([], [], [], "o", color="tab:orange")
    order_ax.set(xlabel="Sample number in run", ylabel="Y")
    order_ax.set_title("Click a point · ↑ earlier · ↓ later")
    order_ax.xaxis.set_major_locator(MaxNLocator(nbins=6, integer=True))
    order_ax.ticklabel_format(axis="x", useOffset=False, style="plain")
    (order_points,) = order_ax.plot([], [], ".", color="tab:blue", pickradius=6)
    (order_point,) = order_ax.plot([], [], "o", color="tab:orange")

    def show_sample(index):
        nonlocal selected
        selected = index
        sample = samples[selected]
        x, y, z = traj[sample]
        record_point.set_data_3d([x], [y], [z])
        order_point.set_data([sample + 1], [y])
        record_ax.set_title(
            f"3D record · sample {sample + 1} · {selected + 1}/{len(samples)} in cell\n"
            f"X {x:.6f}   Y {y:.6f}   Z {z:.6f}"
        )
        fig.canvas.draw_idle()

    def select_cell(x, z):
        nonlocal samples
        column, row = bin_index(x, xedges), bin_index(z, zedges)
        left, right = xedges[column:column + 2]
        bottom, top = zedges[row:row + 2]
        cell.set_bounds(left, bottom, right - left, top - bottom)
        cell.set_visible(True)
        samples = np.flatnonzero((x_bins == column) & (z_bins == row))
        cell_points.set_data_3d(*traj[samples].T)
        order_points.set_data(samples + 1, traj[samples, 1])
        order_point.set_data([], [])
        record_point.set_data_3d([], [], [])
        order_ax.relim()
        order_ax.autoscale_view()
        if len(samples):
            show_sample(0)
        else:
            record_ax.set_title("3D record · 0 samples in this cell")
            fig.canvas.draw_idle()

    def on_click(event):
        toolbar = fig.canvas.toolbar
        if event.button != MouseButton.LEFT or (toolbar and toolbar.mode):
            return
        if event.inaxes is map_ax:
            x, z = event.xdata, event.ydata
            if xedges[0] <= x <= xedges[-1] and zedges[0] <= z <= zedges[-1]:
                select_cell(x, z)
        elif event.inaxes is order_ax:
            hit, details = order_points.contains(event)
            if hit:
                candidates = details["ind"]
                positions = order_ax.transData.transform(
                    np.column_stack((samples[candidates] + 1, traj[samples[candidates], 1]))
                )
                distances = np.sum((positions - [event.x, event.y]) ** 2, axis=1)
                show_sample(candidates[distances.argmin()])

    def on_key(event):
        if len(samples) and event.key in ("up", "down"):
            step = 1 if event.key == "down" else -1
            show_sample(np.clip(selected + step, 0, len(samples) - 1))

    fig.canvas.mpl_connect("button_press_event", on_click)
    fig.canvas.mpl_connect("key_press_event", on_key)
    if initial_sample is not None:
        x, _, z = traj[initial_sample]
        select_cell(x, z)
    return fig


# ---------------------------------------------------
# OPTIONAL: Minimal Field Layer (Preview)
# ---------------------------------------------------

def compute_field(density):
    print("→ Deriving simple field from density...")

    # einfache Normalisierung
    field = density / (np.max(density) + 1e-9)

    return field


# ---------------------------------------------------
# Main
# ---------------------------------------------------

def main(*, show_example=False):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("\n🧠 Generating Lorenz Density Map\n")

    traj = generate_trajectory()

    density, xedges, zedges = compute_density(traj)

    save_density_csv(density)
    plot_density(density, xedges, zedges)
    record_path = os.path.join(OUTPUT_DIR, "lorenz_density_record.npz")
    np.savez_compressed(
        record_path, trajectory=traj, density=density, x_edges=xedges, z_edges=zedges
    )
    print("Saved:", record_path)
    # The example cell contains sample 574 (one-based) from the density run.
    initial_sample = 573 if show_example else None
    black_egg_view(traj, density, xedges, zedges, initial_sample=initial_sample)
    plt.show()

    print("\n✅ Density map finished.\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Explore the Lorenz density and 3D record.")
    parser.add_argument("--example", action="store_true", help="Open with an example cell selected.")
    main(show_example=parser.parse_args().example)
