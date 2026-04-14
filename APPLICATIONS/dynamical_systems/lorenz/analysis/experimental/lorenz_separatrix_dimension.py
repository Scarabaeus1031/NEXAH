import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy.ndimage import sobel


img = Image.open(
    "APPLICATIONS/outputs/lorenz_separatrix/separatrix_zoom.png"
)

img = img.convert("L")

data = np.array(img)


# Edge detection
dx = sobel(data, axis=0)
dy = sobel(data, axis=1)

edges = np.hypot(dx, dy)

edges = edges > np.percentile(edges, 95)


def boxcount(Z, k):

    S = np.add.reduceat(
        np.add.reduceat(Z, np.arange(0, Z.shape[0], k), axis=0),
        np.arange(0, Z.shape[1], k),
        axis=1,
    )

    return len(np.where(S > 0)[0])


sizes = 2 ** np.arange(1, 7)

counts = []

for size in sizes:
    counts.append(boxcount(edges, size))


coeffs = np.polyfit(np.log(sizes), np.log(counts), 1)

D = -coeffs[0]

print("Fractal dimension (boundary):", D)


plt.figure(figsize=(6, 6))
plt.imshow(edges, cmap="gray")
plt.title("Extracted Basin Boundary")
plt.axis("off")

plt.figure()
plt.plot(np.log(sizes), np.log(counts), "o-")
plt.xlabel("log(box size)")
plt.ylabel("log(box count)")
plt.title(f"Fractal dimension ≈ {D:.3f}")
plt.show()
