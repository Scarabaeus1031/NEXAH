import numpy as np
import matplotlib.pyplot as plt


class StabilityInformationGeometry:
    """
    Information geometry of the stability landscape.

    Uses the Hessian of the stability field to derive
    curvature-based geometric measures.
    """

    def __init__(self, X, Y, Z):

        self.X = X
        self.Y = Y
        self.Z = Z

    # --------------------------------------------------
    # derivatives
    # --------------------------------------------------

    def compute_hessian(self):

        dZ_dy, dZ_dx = np.gradient(self.Z)

        d2Z_dx2 = np.gradient(dZ_dx, axis=1)
        d2Z_dy2 = np.gradient(dZ_dy, axis=0)

        d2Z_dxdy = np.gradient(dZ_dx, axis=0)

        return d2Z_dx2, d2Z_dy2, d2Z_dxdy

    # --------------------------------------------------
    # geometric quantities
    # --------------------------------------------------

    def compute_geometry(self):

        dxx, dyy, dxy = self.compute_hessian()

        # Hessian determinant
        detH = dxx * dyy - dxy**2

        # Hessian trace (Laplacian)
        traceH = dxx + dyy

        # curvature magnitude
        curvature = np.sqrt(dxx**2 + dyy**2 + 2*dxy**2)

        return detH, traceH, curvature

    # --------------------------------------------------
    # plotting
    # --------------------------------------------------

    def plot(self):

        detH, traceH, curvature = self.compute_geometry()

        fig, axes = plt.subplots(1, 3, figsize=(18,5))

        # Hessian determinant
        im0 = axes[0].contourf(self.X, self.Y, detH, levels=30, cmap="coolwarm")
        axes[0].set_title("Hessian Determinant")
        axes[0].set_xlabel("Axis X")
        axes[0].set_ylabel("Axis Y")
        fig.colorbar(im0, ax=axes[0])

        # trace
        im1 = axes[1].contourf(self.X, self.Y, traceH, levels=30, cmap="viridis")
        axes[1].set_title("Trace(Hessian)")
        axes[1].set_xlabel("Axis X")
        axes[1].set_ylabel("Axis Y")
        fig.colorbar(im1, ax=axes[1])

        # curvature magnitude
        im2 = axes[2].contourf(self.X, self.Y, curvature, levels=30, cmap="magma")
        axes[2].set_title("Curvature Magnitude")
        axes[2].set_xlabel("Axis X")
        axes[2].set_ylabel("Axis Y")
        fig.colorbar(im2, ax=axes[2])

        plt.suptitle("Stability Information Geometry")

        plt.tight_layout()

        plt.show()
