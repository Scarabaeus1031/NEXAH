import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_gradient_magnitude

# ================================
# FIELD DEFINITION (same as v7.0 style)
# ================================

def field(x, y):
    # radial + rotation (dein Pattern)
    r = np.sqrt(x**2 + y**2) + 1e-6
    
    # radial push outward
    fx = x * (1 - r)
    fy = y * (1 - r)
    
    # rotation term
    fx += -y * 0.5
    fy += x * 0.5
    
    return fx, fy


# ================================
# TRAJECTORY SIMULATION
# ================================

def simulate(x0, y0, steps=200, dt=0.05):
    x, y = x0, y0
    traj = []
    
    for _ in range(steps):
        fx, fy = field(x, y)
        x += fx * dt
        y += fy * dt
        traj.append((x, y))
        
    return np.array(traj)


# ================================
# GRID SETUP
# ================================

N = 80
x_vals = np.linspace(-1.5, 1.5, N)
y_vals = np.linspace(-1.5, 1.5, N)

basin_map = np.zeros((N, N))
speed_map = np.zeros((N, N))
divergence = np.zeros((N, N))

# ================================
# BUILD MAPS
# ================================

for i, x in enumerate(x_vals):
    for j, y in enumerate(y_vals):
        
        traj = simulate(x, y)
        tail = traj[-50:]
        
        # attractor position
        cx, cy = np.mean(tail[:,0]), np.mean(tail[:,1])
        
        # encode as ID
        basin_map[j, i] = int((cx + 1.5) * 20) + int((cy + 1.5) * 20) * 100
        
        # speed
        dx = np.diff(traj[:,0])
        dy = np.diff(traj[:,1])
        speed_map[j, i] = np.mean(np.sqrt(dx**2 + dy**2))
        
        # divergence (finite difference approx)
        eps = 1e-3
        fx1, fy1 = field(x + eps, y)
        fx2, fy2 = field(x - eps, y)
        fx3, fy3 = field(x, y + eps)
        fx4, fy4 = field(x, y - eps)
        
        dfdx = (fx1 - fx2) / (2 * eps)
        dfdy = (fy3 - fy4) / (2 * eps)
        
        divergence[j, i] = dfdx + dfdy


# ================================
# SEPARATRIX DETECTION
# ================================

basin_grad = gaussian_gradient_magnitude(basin_map.astype(float), sigma=1.0)
div_grad   = gaussian_gradient_magnitude(divergence, sigma=1.0)
speed_grad = gaussian_gradient_magnitude(speed_map, sigma=1.0)

sep_strength = (
    0.5 * basin_grad +
    0.3 * div_grad +
    0.2 * speed_grad
)

# normalize
sep = (sep_strength - sep_strength.min()) / (sep_strength.max() - sep_strength.min())

# threshold
threshold = 0.4
sep_mask = sep > threshold


# ================================
# PLOTS
# ================================

plt.figure(figsize=(12,10))

# Basin Map
plt.subplot(2,2,1)
plt.imshow(basin_map, cmap='viridis')
plt.title("Basin Map")
plt.colorbar()

# Speed
plt.subplot(2,2,2)
plt.imshow(speed_map, cmap='magma')
plt.title("Speed (Blueshift)")
plt.colorbar()

# Divergence
plt.subplot(2,2,3)
plt.imshow(divergence, cmap='coolwarm')
plt.title("Divergence")
plt.colorbar()

# Separatrix
plt.subplot(2,2,4)
plt.imshow(sep, cmap='inferno')
plt.contour(sep_mask, colors='cyan', linewidths=0.5)
plt.title("Separatrix Map")

plt.tight_layout()
plt.show()


# ================================
# OVERLAY (KEY VISUAL)
# ================================

plt.figure(figsize=(6,6))
plt.imshow(basin_map, cmap='viridis')
plt.contour(sep_mask, colors='white', linewidths=1.0)
plt.title("Separatrix over Basin")
plt.show()
