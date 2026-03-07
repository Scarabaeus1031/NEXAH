import numpy as np
import matplotlib.pyplot as plt


class StabilityPersistenceHomology:
    """
    Lightweight persistence-style analysis for stability landscapes.

    This module approximates 0-dimensional persistence behavior by
    tracking local maxima and their prominence above surrounding terrain.

    It is not a full persistent homology implementation, but it provides
    a useful topological summary of:
        - how many dominant peaks exist
        - how strong / persistent they are
        - which peaks are likely structural vs noise
    """

    def __init__(self, X, Y, Z):
        self.X = X
        self.Y = Y
        self.Z = Z

    def find_local_maxima(self):
        """
        Detect local maxima using 8-neighborhood comparison.
        """

        maxima = []

        ny, nx = self.Z.shape

        for i in range(1, ny - 1):
            for j in range(1, nx - 1):

                value = self.Z[i, j]
                neighborhood = self.Z[i - 1:i + 2, j - 1:j + 2]

                if value == np.max(neighborhood):
                    if np.sum(neighborhood == value) == 1:
                        maxima.append((i, j, value))

        return maxima

    def estimate_birth_death(self, maxima, window=6):
        """
        Approximate persistence of each maximum.

        birth = peak value
        death = lowest surrounding "barrier" estimate in local window
        persistence = birth - death

        This is a heuristic prominence-style estimate.
        """

        ny, nx = self.Z.shape
        features = []

        for i, j, birth in maxima:

            i0 = max(0, i - window)
            i1 = min(ny, i + window + 1)
            j0 = max(0, j - window)
            j1 = min(nx, j + window + 1)

            patch = self.Z[i0:i1, j0:j1]

            # exclude the peak itself when possible
            flat = patch.flatten()
            if len(flat) > 1:
                death = np.percentile(flat, 20)
            else:
                death = birth

            persistence = birth - death

            features.append({
                "grid_index": (i, j),
                "position": (self.X[i, j], self.Y[i, j]),
                "birth": float(birth),
                "death": float(death),
                "persistence": float(persistence),
            })

        features.sort(key=lambda d: d["persistence"], reverse=True)

        return features

    def compute(self):
        """
        Full lightweight persistence-style pipeline.
        """

        maxima = self.find_local_maxima()
        features = self.estimate_birth_death(maxima)

        return features

    def print_report(self, features, top_k=15):
        """
        Print strongest persistent features.
        """

        print("\nSTABILITY PERSISTENCE HOMOLOGY (LIGHTWEIGHT)\n")
        print("-" * 60)

        for k, feat in enumerate(features[:top_k], start=1):
            x, y = feat["position"]
            print(
                f"{k:02d} | "
                f"pos=({x:.3f}, {y:.3f}) | "
                f"birth={feat['birth']:.3f} | "
                f"death={feat['death']:.3f} | "
                f"persistence={feat['persistence']:.3f}"
            )

    def plot_persistence_diagram(self, features):
        """
        Plot persistence diagram: birth vs death.
        """

        births = [f["birth"] for f in features]
        deaths = [f["death"] for f in features]

        plt.figure(figsize=(7, 7))

        plt.scatter(births, deaths, color="darkred", s=50)

        if births and deaths:
            lo = min(deaths)
            hi = max(births)
            plt.plot([lo, hi], [lo, hi], linestyle="--", color="black", alpha=0.6)

        plt.xlabel("Birth")
        plt.ylabel("Death")
        plt.title("Stability Persistence Diagram")

        plt.show()

    def plot_persistence_barcodes(self, features, top_k=20):
        """
        Plot barcode-style persistence intervals.
        """

        plt.figure(figsize=(10, 6))

        selected = features[:top_k]

        for idx, feat in enumerate(selected):
            plt.hlines(
                y=idx,
                xmin=feat["death"],
                xmax=feat["birth"],
                color="navy",
                linewidth=2.5
            )

        plt.xlabel("Stability Level")
        plt.ylabel("Feature Index")
        plt.title("Stability Persistence Barcodes")

        plt.show()

    def plot_landscape_features(self, features, top_k=15):
        """
        Overlay strongest persistent features on the contour landscape.
        """

        plt.figure(figsize=(9, 7))

        plt.contourf(
            self.X,
            self.Y,
            self.Z,
            levels=40,
            cmap="viridis"
        )

        selected = features[:top_k]

        xs = [f["position"][0] for f in selected]
        ys = [f["position"][1] for f in selected]
        ps = [f["persistence"] for f in selected]

        sizes = [40 + 30 * p for p in ps]

        plt.scatter(
            xs,
            ys,
            color="red",
            s=sizes,
            edgecolor="white",
            linewidth=0.8,
            label="Persistent Features"
        )

        for idx, feat in enumerate(selected):
            x, y = feat["position"]
            plt.text(x, y, f"P{idx}", color="white", fontsize=8, ha="center", va="center")

        plt.xlabel("Axis X")
        plt.ylabel("Axis Y")
        plt.title("Persistent Stability Features")
        plt.legend()
        plt.colorbar(label="Stability")

        plt.show()
