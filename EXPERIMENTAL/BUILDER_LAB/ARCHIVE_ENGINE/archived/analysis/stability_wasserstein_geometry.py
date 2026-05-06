import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import wasserstein_distance


class StabilityWassersteinGeometry:

    def __init__(self, Z1, Z2):

        self.Z1 = Z1
        self.Z2 = Z2

    def compute(self):

        a = self.Z1.flatten()
        b = self.Z2.flatten()

        distance = wasserstein_distance(a, b)

        return distance

    def plot(self):

        plt.figure(figsize=(10,4))

        plt.subplot(1,2,1)
        plt.hist(self.Z1.flatten(), bins=40)
        plt.title("Landscape A")

        plt.subplot(1,2,2)
        plt.hist(self.Z2.flatten(), bins=40)
        plt.title("Landscape B")

        plt.tight_layout()

        plt.show()
