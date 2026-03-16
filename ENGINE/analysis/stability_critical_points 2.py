import numpy as np
import matplotlib.pyplot as plt


class StabilityCriticalPoints:
    """
    Detect critical points of a stability landscape.

    Critical points occur where gradient ≈ 0.

    Classification using Hessian determinant:
    det(H) > 0 and Zxx < 0  → local maximum
    det(H) > 0 and Zxx > 0  → local minimum
    det(H) < 0              → saddle
    """

    def __init__(self, X, Y, Z):

        self.X = X
        self.Y = Y
        self.Z = Z

    def compute(self, grad_threshold=0.02):

        Zy, Zx = np.gradient(self.Z)

        Zyy, Zyx = np.gradient(Zy)
        Zxy, Zxx = np.gradient(Zx)

        detH = Zxx * Zyy - Zxy**2

        maxima = []
        minima = []
        saddles = []

        ny, nx = self.Z.shape

        for i in range(1, ny-1):
            for j in range(1, nx-1):

                grad_mag = np.sqrt(Zx[i,j]**2 + Zy[i,j]**2)

                if grad_mag < grad_threshold:

                    d = detH[i,j]

                    x = self.X[i,j]
                    y = self.Y[i,j]

                    if d > 0:

                        if Zxx[i,j] < 0:
                            maxima.append((x,y))

                        else:
                            minima.append((x,y))

                    elif d < 0:
                        saddles.append((x,y))

        return maxima, minima, saddles

    def plot(self, maxima, minima, saddles):

        plt.figure(figsize=(9,7))

        plt.contourf(
            self.X,
            self.Y,
            self.Z,
            levels=40,
            cmap="viridis"
        )

        if maxima:
            m = np.array(maxima)
            plt.scatter(m[:,0], m[:,1], color="red", s=80, label="Maxima")

        if minima:
            m = np.array(minima)
            plt.scatter(m[:,0], m[:,1], color="blue", s=80, label="Minima")

        if saddles:
            s = np.array(saddles)
            plt.scatter(s[:,0], s[:,1], color="white", s=80, label="Saddles")

        plt.title("Stability Critical Points")

        plt.xlabel("Axis X")
        plt.ylabel("Axis Y")

        plt.legend()

        plt.colorbar(label="Stability")

        plt.show()
