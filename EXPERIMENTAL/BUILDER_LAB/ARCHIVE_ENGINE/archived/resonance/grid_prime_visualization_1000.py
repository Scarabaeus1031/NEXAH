import numpy as np
import matplotlib.pyplot as plt
from sympy import primerange

# ---------------------------------------------------------
# Prime numbers and their positions
# ---------------------------------------------------------

# Get first 1000 primes
primes = list(primerange(1, 8000))  # we go up to 8000 to get at least 1000 primes

# Prime positions and their RGB representation
positions = np.array(primes)  # x-axis
colors = np.zeros((len(positions), 3))  # RGB array

# Set RGB colors for each prime
for i, prime in enumerate(primes):
    if prime % 3 == 0:
        colors[i] = [0, 0, 1]  # Blue for multiples of 3
    elif prime % 5 == 0:
        colors[i] = [1, 0, 0]  # Red for multiples of 5
    else:
        colors[i] = [0, 1, 0]  # Green for others

# ---------------------------------------------------------
# Plot the Prime Grid with RGB colors
# ---------------------------------------------------------

# Set up the plot
plt.figure(figsize=(10, 10))
plt.scatter(positions, np.zeros(len(positions)), c=colors, s=100)

# Add labels
plt.title('Prime Number Grid with RGB Colors (First 1000 Primes)')
plt.xlabel('Prime Numbers')
plt.ylabel('Y axis (Fixed for simplicity)')
plt.colorbar()  # Color bar to show RGB scale

plt.tight_layout()
plt.show()
