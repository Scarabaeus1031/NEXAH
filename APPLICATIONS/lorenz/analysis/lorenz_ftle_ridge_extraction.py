import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
from datetime import datetime
import os

# ---------------------------------------------------
# Synthetic FTLE example (can be replaced by real FTLE)
# ---------------------------------------------------

def generate_ftle_field(n=200):

    x = np.linspace(-20,20,n)
    y = np.linspace(-20,20,n)

    X,Y = np.meshgrid(x,y)

    Z = np.sin(X/3)*np.cos(Y/3)
    Z += 0.3*np.sin(X*Y/40)

    Z = gaussian_filter(Z,2)

    return X,Y,Z


# ---------------------------------------------------
# Ridge detection (simple gradient method)
# ---------------------------------------------------

def detect_ridges(Z, threshold=0.4):

    gx,gy = np.gradient(Z)

    grad_mag = np.sqrt(gx**2 + gy**2)

    ridges = grad_mag > threshold*np.max(grad_mag)

    return ridges


# ---------------------------------------------------
# Plot result
# ---------------------------------------------------

def plot_ridges(X,Y,Z,ridges):

    plt.figure(figsize=(10,6))

    plt.imshow(
        Z,
        extent=[X.min(),X.max(),Y.min(),Y.max()],
        origin="lower",
        cmap="inferno"
    )

    plt.contour(
        ridges,
        levels=[0.5],
        colors="cyan",
        linewidths=1
    )

    plt.title("FTLE Ridge Skeleton")

    outdir = "../../outputs/lorenz_navigation"
    os.makedirs(outdir,exist_ok=True)

    name = f"lorenz_ftle_ridges_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    path = os.path.join(outdir,name)

    plt.savefig(path,dpi=300)
    print("saved:",path)

    plt.show()


# ---------------------------------------------------

if __name__ == "__main__":

    X,Y,Z = generate_ftle_field()

    ridges = detect_ridges(Z)

    plot_ridges(X,Y,Z,ridges)
