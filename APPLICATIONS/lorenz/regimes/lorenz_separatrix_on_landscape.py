"""
Overlay fractal separatrix on Lorenz potential landscape
"""

import numpy as np
import matplotlib.pyplot as plt
import os

# files
POTENTIAL_FILE = "APPLICATIONS/outputs/lorenz_resilience/lorenz_resilience_map.csv"
SEPARATRIX_FILE = "APPLICATIONS/outputs/lorenz_separatrix/separatrix_zoom.npy"

OUTPUT = "APPLICATIONS/outputs/lorenz_separatrix_overlay"
os.makedirs(OUTPUT, exist_ok=True)


# load potential
tau = np.loadtxt(POTENTIAL_FILE, delimiter=",")

rows, cols = tau.shape

xs = np.linspace(-4,4,cols)
zs = np.linspace(15,35,rows)

V = 1/(tau+1e-6)
V = (V-V.min())/(V.max()-V.min())


# load separatrix map
basin = np.load(SEPARATRIX_FILE)

# compute boundary
dz, dx = np.gradient(basin)
boundary = np.abs(dx)+np.abs(dz)

boundary = boundary>0


# zoom region coordinates
xs_zoom = np.linspace(-0.2,0.2,basin.shape[1])
zs_zoom = np.linspace(26,28,basin.shape[0])


# plot
X,Z = np.meshgrid(xs,zs)

fig = plt.figure(figsize=(10,8))
ax = fig.add_subplot(111,projection="3d")

ax.plot_surface(
    X,
    Z,
    V,
    cmap="magma",
    alpha=0.8,
    linewidth=0
)

# overlay fractal boundary
bx,bz = np.where(boundary)

bx = xs_zoom[bx]
bz = zs_zoom[bz]

bv = np.zeros_like(bx)+0.02

ax.scatter(
    bx,
    bz,
    bv,
    s=1,
    c="cyan"
)

ax.set_title("Fractal Separatrix on Lorenz Potential Landscape")

path = OUTPUT+"/separatrix_overlay.png"
plt.savefig(path,dpi=300)

print("saved:",path)

plt.show()
