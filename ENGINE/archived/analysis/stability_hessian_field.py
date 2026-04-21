import numpy as np
import matplotlib.pyplot as plt


class StabilityHessianField:
    """
    Compute Hessian curvature of a stability landscape.

    Allows detection of:
    - peaks
    - valleys
    - saddle points
    """

    def __init__(self, X, Y, Z):

        self.X = X
        self.Y = Y
        self.Z = Z

    def compute(self):

        # first derivatives
        Zy, Zx = np.gradient(self.Z)

        # second derivatives
        Zyy, Zyx = np.gradient(Zy)
        Zxy, Zxx = np.gradient(Zx)

        return Zxx, Zyy, Zxy

    def hessian_determinant(self):

        Zxx, Zyy, Zxy = self.compute()

        detH = Zxx * Zyy - Zxy**2

        return detH

    def plot(self):

        detH = self.hessian_determinant()

        plt.figure(figsize=(9,7))

        plt.contourf(
            self.X,
            self.Y,
            detH,
            levels=40,
            cmap="coolwarm"
        )

        plt.colorbar(label="Hessian Determinant")

        plt.title("Stability Hessian Field")

        plt.xlabel("Axis X")
        plt.ylabel("Axis Y")

        plt.show()
