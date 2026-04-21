import numpy as np
import matplotlib.pyplot as plt

# Defining the primes within a given range
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]
# Let's map each prime to a unique RGB color
rgb_map = {
    41: (1, 0, 0),  # Red
    137: (0, 1, 0), # Green
    29: (0, 0, 1)   # Blue
}

# Create a grid of size 20x20
grid_size = 20
grid = np.zeros((grid_size, grid_size))

# Fill the grid with primes
for i in range(grid_size):
    for j in range(grid_size):
        prime_idx = (i * grid_size + j) % len(primes)
        grid[i, j] = primes[prime_idx]

# Create RGB colors for each prime
rgb_grid = np.zeros((grid_size, grid_size, 3))

# Applying color mapping
for i in range(grid_size):
    for j in range(grid_size):
        prime_value = grid[i, j]
        if prime_value in rgb_map:
            rgb_grid[i, j] = rgb_map[prime_value]
        else:
            rgb_grid[i, j] = (0.5, 0.5, 0.5)  # Default color for non-specified primes

# Plotting the grid
plt.imshow(rgb_grid, interpolation='nearest')
plt.title("Prime Number Grid with RGB Colors")
plt.colorbar()
plt.show()
