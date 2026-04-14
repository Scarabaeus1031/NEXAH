import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter, label, center_of_mass
from scipy.spatial.distance import cdist

# ============================================================
# NEXAH v8.1 — Gap Detection + Grey Node Graph
# Lorenz-derived RGB + Grey field with explicit passage analysis
# ============================================================

# ------------------------------------------------------------
# LORENZ SYSTEM
# ------------------------------------------------------------
def lorenz_step(x, y, z, sigma=10.0, rho=28.0, beta=8.0/3.0, dt=0.005):
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z

    x_new = x + dx * dt
    y_new = y + dy * dt
    z_new = z + dz * dt
    return x_new, y_new, z_new


def simulate_lorenz(steps=18000, burn=3000, dt=0.005):
    x, y, z = 0.1, 1.0, 1.05

    xs, ys, zs = [], [], []
    for _ in range(steps + burn):
        x, y, z = lorenz_step(x, y, z, dt=dt)
        if _ >= burn:
            xs.append(x)
            ys.append(y)
            zs.append(z)

    return np.array(xs), np.array(ys), np.array(zs)


# ------------------------------------------------------------
# SEMANTIC RGB + GREY REGIONS
# ------------------------------------------------------------
def classify_regions(x, y, z):
    """
    blue  = lower / memory side
    red   = upper / expansion side
    green = central transition band
    grey  = narrow channel around transition axis
    """
    # transition axis: roughly along x+y balance in projected plane
    axis_val = x - y
    center_val = np.abs(axis_val)

    # grey channel
    if center_val < 0.45 and 5.0 < z < 32.0:
        return "grey"

    # green transfer
    if center_val < 2.5 and 2.0 < z < 30.0:
        return "green"

    # lobe colors
    if x + y >= 0:
        return "red"
    return "blue"


# ------------------------------------------------------------
# GRID ACCUMULATION
# ------------------------------------------------------------
def make_grid(xs, ys, bins=420, padding=1.0):
    xmin, xmax = xs.min() - padding, xs.max() + padding
    ymin, ymax = ys.min() - padding, ys.max() + padding
    return xmin, xmax, ymin, ymax, bins


def points_to_image(xp, yp, values, xmin, xmax, ymin, ymax, bins):
    img = np.zeros((bins, bins), dtype=float)

    ix = ((xp - xmin) / (xmax - xmin) * (bins - 1)).astype(int)
    iy = ((yp - ymin) / (ymax - ymin) * (bins - 1)).astype(int)

    valid = (ix >= 0) & (ix < bins) & (iy >= 0) & (iy < bins)
    ix = ix[valid]
    iy = iy[valid]
    vals = values[valid]

    for xg, yg, v in zip(ix, iy, vals):
        img[bins - 1 - yg, xg] += v

    return img


def project_to_grid_points(xp, yp, xmin, xmax, ymin, ymax, bins):
    ix = ((xp - xmin) / (xmax - xmin) * (bins - 1)).astype(int)
    iy = ((yp - ymin) / (ymax - ymin) * (bins - 1)).astype(int)
    valid = (ix >= 0) & (ix < bins) & (iy >= 0) & (iy < bins)
    return ix[valid], iy[valid], valid


# ------------------------------------------------------------
# GAP DETECTION
# ------------------------------------------------------------
def detect_channel_and_gaps(density_img):
    """
    Detect bright channel and internal low-density gaps.
    """
    smooth = gaussian_filter(density_img, sigma=2.0)

    # normalize
    if smooth.max() > 0:
        smooth_n = smooth / smooth.max()
    else:
        smooth_n = smooth.copy()

    # channel = dense narrow band
    channel_mask = smooth_n > 0.18

    # inner gaps = holes / low-density islands inside channel neighborhood
    inner_low = smooth_n < 0.07

    # restrict to central passage zone
    bins = density_img.shape[0]
    yy, xx = np.mgrid[0:bins, 0:bins]
    cx = bins / 2
    cy = bins / 2

    rx = (xx - cx) / (0.20 * bins)
    ry = (yy - cy) / (0.10 * bins)
    central_window = (rx**2 + ry**2) < 1.0

    gap_mask = inner_low & central_window

    lab, nlab = label(gap_mask)
    centers = []

    for k in range(1, nlab + 1):
        comp = (lab == k)
        area = comp.sum()
        if 20 <= area <= 2500:
            cyx = center_of_mass(comp)
            centers.append((cyx[1], cyx[0], area))  # x, y, area

    # sort by x position
    centers = sorted(centers, key=lambda t: t[0])

    return smooth_n, channel_mask, gap_mask, centers


# ------------------------------------------------------------
# GREY NODE DETECTION
# ------------------------------------------------------------
def detect_grey_nodes(xp, yp, xmin, xmax, ymin, ymax, bins):
    """
    Grey nodes = local density peaks along grey channel.
    """
    ones = np.ones_like(xp, dtype=float)
    grey_density = points_to_image(xp, yp, ones, xmin, xmax, ymin, ymax, bins)
    grey_smooth = gaussian_filter(grey_density, sigma=2.2)

    if grey_smooth.max() > 0:
        g = grey_smooth / grey_smooth.max()
    else:
        g = grey_smooth

    # local peak heuristic
    bins_y, bins_x = g.shape
    peaks = []
    for j in range(2, bins_y - 2):
        for i in range(2, bins_x - 2):
            val = g[j, i]
            if val < 0.22:
                continue
            patch = g[j-2:j+3, i-2:i+3]
            if val >= patch.max():
                peaks.append((i, j, val))

    # non-maximum suppression by distance
    kept = []
    min_dist = 18
    for p in sorted(peaks, key=lambda t: -t[2]):
        if all((p[0] - q[0])**2 + (p[1] - q[1])**2 >= min_dist**2 for q in kept):
            kept.append(p)

    # keep only strongest nodes
    kept = kept[:12]
    kept = sorted(kept, key=lambda t: t[0])

    return grey_density, grey_smooth, kept


# ------------------------------------------------------------
# NODE GRAPH
# ------------------------------------------------------------
def build_node_graph(nodes, max_neighbors=3):
    if len(nodes) == 0:
        return []

    pts = np.array([[n[0], n[1]] for n in nodes], dtype=float)
    D = cdist(pts, pts)

    edges = set()
    for i in range(len(nodes)):
        nbrs = np.argsort(D[i])[1:max_neighbors+1]
        for j in nbrs:
            a, b = min(i, j), max(i, j)
            edges.add((a, b))

    return sorted(edges)


# ------------------------------------------------------------
# PLOTS
# ------------------------------------------------------------
def plot_full_field(xs, ys, regions, grey_pts, gap_centers):
    fig, ax = plt.subplots(figsize=(9, 9))

    colors = {
        "blue": "#1f77b4",
        "green": "#2ca02c",
        "red": "#d62728",
    }

    # plot main field
    for reg in ["blue", "green", "red"]:
        mask = (regions == reg)
        ax.scatter(xs[mask], ys[mask], s=1, c=colors[reg], label=reg, alpha=0.9)

    # grey channel
    ax.scatter(grey_pts[:, 0], grey_pts[:, 1], s=2, c="black", label="grey", alpha=0.9)

    # gap centers
    for k, (gx, gy, area) in enumerate(gap_centers[:6]):
        ax.scatter([gx], [gy], s=90, facecolors="none", edgecolors="gold", linewidths=2)
        ax.text(gx + 0.4, gy + 0.4, f"gap {k+1}", color="gold", fontsize=9)

    ax.set_title("NEXAH v8.1 — Full Field + Grey Channel + Gaps")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.legend(loc="upper left")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()


def plot_gap_maps(smooth_n, channel_mask, gap_mask, gap_centers):
    fig, axs = plt.subplots(1, 3, figsize=(16, 5))

    axs[0].imshow(smooth_n, cmap="magma", origin="upper")
    axs[0].set_title("Smoothed Grey Density")

    axs[1].imshow(channel_mask, cmap="gray", origin="upper")
    axs[1].set_title("Detected Channel")

    axs[2].imshow(gap_mask, cmap="inferno", origin="upper")
    axs[2].set_title("Gap Mask")
    for k, (gx, gy, area) in enumerate(gap_centers[:10]):
        axs[2].scatter([gx], [gy], s=60, facecolors="none", edgecolors="cyan")
        axs[2].text(gx + 3, gy + 3, str(k+1), color="cyan", fontsize=8)

    for ax in axs:
        ax.set_xticks([])
        ax.set_yticks([])

    plt.tight_layout()


def plot_node_graph(grey_smooth, nodes, edges):
    fig, ax = plt.subplots(figsize=(8, 8))

    ax.imshow(grey_smooth, cmap="Blues", origin="upper")

    for i, (x, y, val) in enumerate(nodes):
        ax.scatter([x], [y], s=80, c="black")
        ax.text(x + 4, y + 4, f"v{i}", color="black", fontsize=9)

    for i, j in edges:
        x1, y1, _ = nodes[i]
        x2, y2, _ = nodes[j]
        ax.plot([x1, x2], [y1, y2], color="gray", alpha=0.7, linewidth=1)

    ax.set_title("Grey Star Nodes — Mycel Network Graph")
    ax.set_xticks([])
    ax.set_yticks([])
    plt.tight_layout()


def plot_rt_proxy(xs, ys):
    """
    Simple R/T-style proxy from radial oscillation around the channel center.
    """
    cx = np.mean(xs[np.abs(xs) < 2.0])
    cy = np.mean(ys[np.abs(xs) < 2.0])

    r = np.sqrt((xs - cx)**2 + (ys - cy)**2)
    r = (r - r.min()) / (r.max() - r.min() + 1e-9)

    fig, ax = plt.subplots(figsize=(14, 4))
    ax.plot(r, linewidth=1.2)
    ax.set_title("R/T Field Dynamics")
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return r


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------
def main():
    xs, ys, zs = simulate_lorenz()

    # semantic classes
    regions = np.array([classify_regions(x, y, z) for x, y, z in zip(xs, ys, zs)])

    blue_mask = regions == "blue"
    green_mask = regions == "green"
    red_mask = regions == "red"
    grey_mask = regions == "grey"

    xmin, xmax, ymin, ymax, bins = make_grid(xs, ys, bins=420, padding=1.0)

    # gap detection uses only grey points
    grey_x = xs[grey_mask]
    grey_y = ys[grey_mask]
    grey_pts = np.column_stack([grey_x, grey_y])

    grey_density, grey_smooth, nodes = detect_grey_nodes(
        grey_x, grey_y, xmin, xmax, ymin, ymax, bins
    )

    smooth_n, channel_mask, gap_mask, gap_centers = detect_channel_and_gaps(grey_density)
    edges = build_node_graph(nodes, max_neighbors=3)

    # plots
    plot_full_field(xs, ys, regions, grey_pts, gap_centers)
    plot_gap_maps(smooth_n, channel_mask, gap_mask, gap_centers)
    plot_node_graph(grey_smooth, nodes, edges)
    rt = plot_rt_proxy(xs, ys)

    plt.show()

    # summary
    print("\n=== NEXAH v8.1 Summary ===")
    unique, counts = np.unique(regions, return_counts=True)
    total = len(regions)
    for u, c in zip(unique, counts):
        print(f"{u}: {c} ({c/total:.3f})")

    print(f"\nGrey nodes detected: {len(nodes)}")
    print(f"Gaps detected: {len(gap_centers)}")
    if len(gap_centers) > 0:
        print("Gap centers (xpix, ypix, area):")
        for g in gap_centers[:8]:
            print(" ", tuple(round(v, 2) for v in g))

    print(f"Node graph edges: {len(edges)}")
    print(f"R/T proxy min/max/mean: {rt.min():.4f} {rt.max():.4f} {rt.mean():.4f}")


if __name__ == "__main__":
    main()
