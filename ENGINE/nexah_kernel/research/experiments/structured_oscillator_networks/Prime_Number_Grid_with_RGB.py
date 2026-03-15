import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

# Prime numbers up to 1000 for visualization
prime_numbers = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 
                 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 
                 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 
                 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317,
                 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419,
                 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503,
                 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 607, 613,
                 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709,
                 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821]

# Constants for the prime grid
constants = [41, 13, 29]  # Prime mod constants for visualization

# Initialize a 2D grid for storing prime colors
x_vals = np.arange(0, len(prime_numbers))
y_vals = np.zeros_like(x_vals)  # Fix y-axis for simplicity

# Normalize the color scale for visualization
norm = Normalize(vmin=0, vmax=1)

# Create a color map based on the prime constants and modulations
def get_prime_color(prime, constant):
    """
    Map prime number to a color based on its constant modulo.
    Blue for +41, Red for +29, and Green for +13.
    """
    if prime % constant == 0:
        if constant == 41:
            return 'green'  # Green for +41
        elif constant == 29:
            return 'red'  # Red for +29
        elif constant == 13:
            return 'blue'  # Blue for +13
    return 'gray'  # Default color for non-matching primes

# Set up the plot for the prime number grid visualization
plt.figure(figsize=(10, 6))
for idx, prime in enumerate(prime_numbers):
    color = get_prime_color(prime, 41)  # Choose +41 for simplicity (can be switched to others)
    plt.scatter(x_vals[idx], y_vals[idx], color=color, s=100)  # Plot prime point

# Title and labels
plt.title("Prime Number Grid with RGB Colors (First 1000 Primes)")
plt.xlabel("Prime Numbers")
plt.ylabel("y axis (Fixed for Simplicity)")

# Create a custom color map
sm = plt.cm.ScalarMappable(cmap='rainbow', norm=norm)
sm.set_array([])

# Add colorbar
plt.colorbar(sm, label="Prime Color Map")

plt.show()
