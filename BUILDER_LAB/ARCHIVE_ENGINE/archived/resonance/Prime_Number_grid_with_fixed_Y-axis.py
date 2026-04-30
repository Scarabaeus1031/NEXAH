import numpy as np
import matplotlib.pyplot as plt
from sympy import primerange

# Set constants for the primes' colors
constant_41 = 41
constant_13 = 13
constant_29 = 29

# Define number of primes to be visualized
num_primes = 1000
primes = list(primerange(1, 8000))[:num_primes]  # Get first 'num_primes' primes

# Create a function to apply color-coding based on constants
def color_based_on_prime(n):
    if n % constant_41 == 0:
        return 'g'  # Green for +41
    elif n % constant_13 == 0:
        return 'b'  # Blue for +13
    elif n % constant_29 == 0:
        return 'r'  # Red for +29
    else:
        return 'gray'  # Default color for non-special primes

# Plot the prime numbers in a grid
fig, ax = plt.subplots(figsize=(10, 6))

# Create x and y values for the prime positions (here we are using a 1D arrangement)
x_values = np.arange(len(primes))
y_values = np.zeros_like(x_values)  # Fixed y-values for simplicity

# Apply the color scheme for each prime
colors = [color_based_on_prime(p) for p in primes]

# Scatter plot with color-coding
scatter = ax.scatter(x_values, y_values, c=colors, cmap='viridis', s=20)

# Set titles and labels
ax.set_title("Prime Number Grid with RGB Colors (First 1000 Primes)")
ax.set_xlabel("Prime Numbers")
ax.set_ylabel("Y axis (Fixed for simplicity)")

# Display color bar for reference
plt.colorbar(scatter, ax=ax, label="Prime Color Map")

# Save and show the plot
plt.tight_layout()
plt.savefig('output/prime_number_grid_1000.png')
plt.show()
