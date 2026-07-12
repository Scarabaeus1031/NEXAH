"""Generate the canonical Lorenz sheet-transition Demonstrator artifacts."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import NDArray


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR.parent / "visuals" / "structure"
FloatArray = NDArray[np.float64]
IntArray = NDArray[np.int64]


def lorenz(
    x: float,
    y: float,
    z: float,
    s: float = 10.0,
    r: float = 28.0,
    b: float = 2.667,
) -> tuple[float, float, float]:
    return s * (y - x), x * (r - z) - y, x * y - b * z


def simulate(steps: int = 8000, dt: float = 0.01) -> tuple[FloatArray, ...]:
    """Run the deterministic Euler-integrated Lorenz reference trajectory."""

    xs = np.zeros(steps, dtype=np.float64)
    ys = np.zeros(steps, dtype=np.float64)
    zs = np.zeros(steps, dtype=np.float64)
    xs[0], ys[0], zs[0] = (0.1, 0.0, 0.0)

    for index in range(steps - 1):
        dx, dy, dz = lorenz(xs[index], ys[index], zs[index])
        xs[index + 1] = xs[index] + dx * dt
        ys[index + 1] = ys[index] + dy * dt
        zs[index + 1] = zs[index] + dz * dt

    return xs, ys, zs


def compute_sheets(xs: FloatArray, ys: FloatArray, num_sheets: int = 6) -> IntArray:
    """Return the historical radial-bin sheet labels used by the Demonstrator."""

    radius = np.sqrt(xs**2 + ys**2)
    bins = np.linspace(radius.min(), radius.max(), num_sheets + 1)
    return np.asarray(np.digitize(radius, bins) - 1, dtype=np.int64)


def compute_transition_matrix(sheets: IntArray) -> tuple[FloatArray, FloatArray]:
    n_states = len(np.unique(sheets))
    counts = np.zeros((n_states, n_states), dtype=np.float64)

    for index in range(1, len(sheets)):
        source = int(sheets[index - 1])
        target = int(sheets[index])
        counts[source, target] += 1

    probabilities = counts / (counts.sum(axis=1, keepdims=True) + 1e-9)
    return counts, probabilities


def generate_transition_data(
    *,
    steps: int = 8000,
    dt: float = 0.01,
    num_sheets: int = 6,
) -> dict[str, Any]:
    """Create the canonical in-memory reference used by plots and validation."""

    xs, ys, zs = simulate(steps=steps, dt=dt)
    trajectory = np.column_stack((xs, ys, zs))
    sheets = compute_sheets(xs, ys, num_sheets=num_sheets)
    transition_events = np.zeros(len(sheets), dtype=bool)
    transition_events[1:] = sheets[1:] != sheets[:-1]
    counts, probabilities = compute_transition_matrix(sheets)
    return {
        "trajectory": trajectory,
        "sheets": sheets,
        "transition_events": transition_events,
        "transition_matrix": counts,
        "transition_matrix_prob": probabilities,
        "config": {"steps": steps, "dt": dt, "num_sheets_requested": num_sheets},
    }


def save_transition_outputs(
    data: dict[str, Any], output_dir: Path = OUTPUT_DIR
) -> None:
    """Write the historical plots and arrays plus the raw reference trajectory."""

    import matplotlib.pyplot as plt

    output_dir.mkdir(parents=True, exist_ok=True)
    trajectory = data["trajectory"]
    sheets = data["sheets"]
    transition_events = data["transition_events"]
    probabilities = data["transition_matrix_prob"]

    plt.figure(figsize=(16, 4))
    plt.plot(sheets, label="sheet index", alpha=0.7)
    plt.scatter(
        np.where(transition_events)[0],
        sheets[transition_events],
        color="red",
        s=10,
        label="transitions",
    )
    plt.title("Transition Structure — Sheet Dynamics")
    plt.xlabel("time")
    plt.ylabel("sheet")
    plt.legend()
    plt.tight_layout()
    path = output_dir / "transition_structure_timeseries.png"
    plt.savefig(path, dpi=200)
    plt.close()
    print(f"✅ Saved: {path}")

    plt.figure(figsize=(6, 5))
    plt.imshow(probabilities, cmap="viridis")
    plt.colorbar(label="P(i → j)")
    plt.title("Transition Matrix (Sheet Structure)")
    plt.xlabel("to state")
    plt.ylabel("from state")
    plt.tight_layout()
    path = output_dir / "transition_structure_matrix.png"
    plt.savefig(path, dpi=200)
    plt.close()
    print(f"✅ Saved: {path}")

    plt.figure(figsize=(6, 6))
    scatter = plt.scatter(
        trajectory[:, 0],
        trajectory[:, 1],
        c=sheets,
        cmap="tab10",
        s=2,
    )
    plt.colorbar(scatter, label="sheet index")
    plt.title("Phase Space Partition (Sheets)")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.tight_layout()
    path = output_dir / "transition_structure_phase.png"
    plt.savefig(path, dpi=200)
    plt.close()
    print(f"✅ Saved: {path}")

    np.save(output_dir / "transition_trajectory.npy", trajectory)
    np.save(output_dir / "transition_sheets.npy", sheets)
    np.save(output_dir / "transition_matrix.npy", data["transition_matrix"])
    np.save(output_dir / "transition_matrix_prob.npy", probabilities)
    print("💾 Saved data")


def main() -> None:
    print(f"📁 Output directory: {OUTPUT_DIR}")
    print("Running Transition Structure Analysis")
    data = generate_transition_data()
    sheets = data["sheets"]
    print("\n--- Transition Structure ---")
    print(f"Total transitions: {int(np.sum(data['transition_events']))}")
    print(f"Number of states: {len(np.unique(sheets))}")
    print("\nTransition Matrix (probabilities):")
    print(data["transition_matrix_prob"])
    save_transition_outputs(data)
    print("\n✅ Transition Structure complete")


if __name__ == "__main__":
    main()
