# ============================================================
# 🔥 NEW: Mean Shape + Variance
# ============================================================

def plot_mean_shapes(all_shapes):
    plt.figure(figsize=(8, 5))

    for label, shapes in all_shapes.items():
        if len(shapes) == 0:
            continue

        # resample to same length
        resampled = []
        for t_norm, seg_norm in shapes:
            target_t = np.linspace(0, 1, 50)
            seg_interp = np.interp(target_t, t_norm, seg_norm)
            resampled.append(seg_interp)

        resampled = np.array(resampled)

        mean_shape = np.mean(resampled, axis=0)
        std_shape = np.std(resampled, axis=0)

        plt.plot(target_t, mean_shape, label=f"{label} mean")
        plt.fill_between(
            target_t,
            mean_shape - std_shape,
            mean_shape + std_shape,
            alpha=0.2
        )

    plt.title("Mean Event Shape + Variance")
    plt.xlabel("Normalized Time")
    plt.ylabel("Normalized Curvature")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()


# ============================================================
# 🔥 NEW: Shape Derivative
# ============================================================

def plot_shape_derivatives(all_shapes):
    plt.figure(figsize=(8, 5))

    for label, shapes in all_shapes.items():
        for t_norm, seg_norm in shapes:
            d = np.gradient(seg_norm)
            plt.plot(t_norm, d, alpha=0.3, label=label)

    handles, labels = plt.gca().get_legend_handles_labels()
    unique = dict(zip(labels, handles))
    plt.legend(unique.values(), unique.keys())

    plt.title("Event Shape Derivatives (d/dt)")
    plt.xlabel("Normalized Time")
    plt.ylabel("d(curvature)/dt")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()


# ============================================================
# 🔥 NEW: Area to Mean (your key idea)
# ============================================================

def compute_area_to_mean(all_shapes):
    area_results = {}

    for label, shapes in all_shapes.items():
        if len(shapes) == 0:
            continue

        resampled = []
        for t_norm, seg_norm in shapes:
            target_t = np.linspace(0, 1, 50)
            seg_interp = np.interp(target_t, t_norm, seg_norm)
            resampled.append(seg_interp)

        resampled = np.array(resampled)
        mean_shape = np.mean(resampled, axis=0)

        areas = []
        for s in resampled:
            area = np.mean(np.abs(s - mean_shape))
            areas.append(area)

        area_results[label] = {
            "mean_area": float(np.mean(areas)),
            "std_area": float(np.std(areas))
        }

    return area_results


# ============================================================
# 🔥 PRINT AREA RESULTS
# ============================================================

def print_area_results(area_results):
    print("\n=== AREA TO MEAN (FIELD ALIGNMENT) ===\n")

    header = f"{'Scenario':<12} {'MeanArea':<12} {'StdArea':<12}"
    print(header)
    print("-" * len(header))

    for k, v in area_results.items():
        print(
            f"{k:<12} "
            f"{v['mean_area']:<12.4f} "
            f"{v['std_area']:<12.4f}"
        )
