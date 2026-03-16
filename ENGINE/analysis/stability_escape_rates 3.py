import numpy as np
import matplotlib.pyplot as plt


class StabilityEscapeRates:
    """
    Estimate escape rates between attractors based on
    energy barriers along transition paths.

    Uses simplified Arrhenius / Kramers approximation:
        rate ~ exp(- barrier_height)
    """

    def __init__(self, X, Y, Z):

        self.X = X
        self.Y = Y
        self.Z = Z

    def _z_at(self, x, y):

        ix = np.argmin(np.abs(self.X[0] - x))
        iy = np.argmin(np.abs(self.Y[:,0] - y))

        return self.Z[iy, ix]

    def compute(self, attractors, paths):

        results = []

        for i, path in enumerate(paths):

            start = path[0]
            end = path[-1]

            zs = [self._z_at(x, y) for x, y in path]

            z_start = zs[0]
            z_end = zs[-1]

            barrier = max(zs)

            barrier_height = barrier - min(z_start, z_end)

            rate = np.exp(-barrier_height)

            results.append({
                "path": i,
                "start": start,
                "end": end,
                "barrier_height": barrier_height,
                "escape_rate": rate
            })

        return results

    def print_report(self, results):

        print("\nEscape Rate Analysis\n")

        for r in results:

            print(
                f"path {r['path']} | "
                f"barrier={r['barrier_height']:.3f} | "
                f"rate={r['escape_rate']:.5f}"
            )

    def plot(self, attractors, paths, results):

        plt.figure(figsize=(8,6))

        plt.contourf(self.X, self.Y, self.Z, 40, cmap="viridis")

        for path, res in zip(paths, results):

            rate = res["escape_rate"]

            width = 1 + 4*rate

            plt.plot(
                path[:,0],
                path[:,1],
                color="white",
                linewidth=width
            )

        plt.scatter(
            attractors[:,0],
            attractors[:,1],
            color="red",
            s=80
        )

        plt.title("Escape Rates Between Attractors")

        plt.colorbar()

        plt.show()
