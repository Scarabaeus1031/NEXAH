import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

# Parameters
N = 1000  # Number of iterations
width, height = 800, 800  # Image resolution
max_iter = 500  # Maximum number of iterations for Mandelbrot set
x_min, x_max, y_min, y_max = -2.0, 1.0, -1.5, 1.5  # Mandelbrot set bounds

# Mandelbrot function
def mandelbrot(c, max_iter):
    z = 0
    for n in range(max_iter):
        z = z*z + c
        if abs(z) > 2:
            return n
    return max_iter

# Generate Mandelbrot set
def generate_mandelbrot(x_min, x_max, y_min, y_max, width, height, max_iter):
    r1 = np.linspace(x_min, x_max, width)
    r2 = np.linspace(y_min, y_max, height)
    img = np.zeros((width, height))
    
    for i in range(width):
        for j in range(height):
            c = complex(r1[i], r2[j])
            img[i, j] = mandelbrot(c, max_iter)
    
    return img

# Generate Julia set
def generate_julia(c, x_min, x_max, y_min, y_max, width, height, max_iter):
    r1 = np.linspace(x_min, x_max, width)
    r2 = np.linspace(y_min, y_max, height)
    img = np.zeros((width, height))
    
    for i in range(width):
        for j in range(height):
            z = complex(r1[i], r2[j])
            n = 0
            while abs(z) <= 2 and n < max_iter:
                z = z*z + c
                n += 1
            img[i, j] = n
    
    return img

# Parameters for the Mandelbrot set and Julia set
c_julia = complex(-0.75, 0.1)  # Julia set parameter
mandelbrot_img = generate_mandelbrot(x_min, x_max, y_min, y_max, width, height, max_iter)
julia_img = generate_julia(c_julia, x_min, x_max, y_min, y_max, width, height, max_iter)

# Plot Mandelbrot and Julia sets
plt.figure(figsize=(12, 6))

# Mandelbrot set plot
plt.subplot(1, 2, 1)
plt.imshow(mandelbrot_img, cmap='hot', extent=(x_min, x_max, y_min, y_max), norm=LogNorm(vmin=1, vmax=max_iter))
plt.title("Mandelbrot Set")
plt.colorbar(label="Iterations")

# Julia set plot
plt.subplot(1, 2, 2)
plt.imshow(julia_img, cmap='hot', extent=(x_min, x_max, y_min, y_max), norm=LogNorm(vmin=1, vmax=max_iter))
plt.title(f"Julia Set: c = {c_julia}")
plt.colorbar(label="Iterations")

# Save the images
plt.tight_layout()
plt.savefig('EXP_09_mandelbrot_julia_transition.png', dpi=300)

plt.show()

# Additional analysis and visualization for the transitions could go here.
