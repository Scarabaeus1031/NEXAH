import numpy as np
import matplotlib.pyplot as plt


def load_worldlines():

    worldlines = np.load("output/defect_worldlines.npy")

    return worldlines


def compute_phase_gradient(phases):

    grad = np.diff(phases)

    grad = (grad + np.pi) % (2 * np.pi) - np.pi

    return grad


def detect_vortex(phases):

    grad = compute_phase_gradient(phases)

    circulation = np.sum(grad)

    if abs(circulation) > np.pi:
        return True
    else:
        return False


def analyze_ring(phases):

    vortices = []

    for t in range(phases.shape[1]):

        p = phases[:, t]

        if detect_vortex(p):
            vortices.append(t)

    return vortices


def plot_vortex_times(vortex_times):

    plt.figure()

    plt.plot(vortex_times, np.ones(len(vortex_times)), "ro")

    plt.xlabel("time")
    plt.title("Detected vortex events")

    plt.show()


def main():

    phases = np.load("output/phase_history.npy")

    vortices = analyze_ring(phases)

    print("Detected vortex events:", len(vortices))

    plot_vortex_times(vortices)


if __name__ == "__main__":
    main()
