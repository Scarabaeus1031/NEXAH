import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def boxcount(Z, k):

    S = np.add.reduceat(
        np.add.reduceat(Z, np.arange(0, Z.shape[0], k), axis=0),
        np.arange(0, Z.shape[1], k),
        axis=1
    )

    return len(np.where((S > 0) & (S < k*k))[0])


def fractal_dimension(Z):

    Z = Z < 255

    sizes = 2**np.arange(2, 8)

    counts = []

    for size in sizes:
        counts.append(boxcount(Z, size))

    coeffs = np.polyfit(np.log(sizes), np.log(counts), 1)

    return -coeffs[0], sizes, counts


img = Image.open("APPLICATIONS/outputs/lorenz_separatrix/separatrix_zoom.png").convert("L")

data = np.array(img)

D, sizes, counts = fractal_dimension(data)

print("Estimated fractal dimension:", D)

plt.plot(np.log(sizes), np.log(counts), "o-")
plt.xlabel("log(box size)")
plt.ylabel("log(box count)")
plt.title(f"Box counting dimension ≈ {D:.3f}")
plt.show()
