import numpy as np
import matplotlib.pyplot as plt
import os

WINDOW = 50


def detect_events(defect_matrix):
    """
    Detect start times of defect segments.
    """
    events = []

    for ring in range(defect_matrix.shape[0]):

        active = False

        for t in range(defect_matrix.shape[1]):

            val = defect_matrix[ring, t]

            if val and not active:
                events.append((ring, t))
                active = True

            if not val:
                active = False

    return events


def load_defects():

    required = [
        "output/inner_shell_defects.npy",
        "output/middle_shell_defects.npy",
        "output/outer_shell_defects.npy",
    ]

    for f in required:
        if not os.path.exists(f):
            raise RuntimeError(
                f"Missing {f}\nRun three_layer_counterrotation_longrun.py first."
            )

    inner = np.load(required[0])
    middle = np.load(required[1])
    outer = np.load(required[2])

    return inner, middle, outer


def cross_layer_correlations(inner, middle, outer):

    inner_events = detect_events(inner)
    middle_events = detect_events(middle)
    outer_events = detect_events(outer)

    correlations = []

    for ring, t in middle_events:

        for r2, t2 in inner_events:

            if abs(t2 - t) < WINDOW:
                correlations.append(("middle→inner", t, t2))

        for r2, t2 in outer_events:

            if abs(t2 - t) < WINDOW:
                correlations.append(("middle→outer", t, t2))

    return correlations


def plot_event_hist(correlations):

    deltas = []

    for c in correlations:
        _, t1, t2 = c
        deltas.append(t2 - t1)

    plt.figure()
    plt.hist(deltas, bins=50)
    plt.xlabel("time offset (t₂ − t₁)")
    plt.ylabel("count")
    plt.title("Cross-layer defect propagation")
    plt.show()


def main():

    inner, middle, outer = load_defects()

    correlations = cross_layer_correlations(inner, middle, outer)

    print("Total correlated events:", len(correlations))

    plot_event_hist(correlations)


if __name__ == "__main__":
    main()
