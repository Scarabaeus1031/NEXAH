import matplotlib.pyplot as plt
import numpy as np

# Prime numbers up to 1000 for visualization
prime_numbers = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
    73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157,
    163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241,
    251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347,
    349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439,
    443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547,
    557, 563, 569, 571, 577, 587, 593, 599, 607, 613, 617, 619, 631, 641, 643, 647,
    653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757,
    761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863,
    877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983,
    991, 997
]

# Create an empty grid (fixed Y-axis)
grid_size = len(prime_numbers)
y_axis = np.zeros(grid_size)

# Color map: normalize the values between 0 and 1 for color assignment
colors = plt.cm.viridis(np.linspace(0, 1, grid_size))

# Create the plot
fig, ax = plt.subplots(figsize=(12, 6))

# Plot each prime with corresponding RGB color
for i, prime in enumerate(prime_numbers):
    ax.scatter(prime, y_axis[i], color=colors[i], s=100)  # Adjust point size as needed

# Add color bar and associate with the axis
sm = plt.cm.ScalarMappable(cmap="viridis", norm=plt.Normalize(vmin=min(prime_numbers), vmax=max(prime_numbers)))
sm.set_array([])  # Empty array to make color bar work
cbar = plt.colorbar(sm, ax=ax, label="Prime Color Map")  # Added `ax=ax` argument

# Add labels and title
ax.set_xlabel("Prime Numbers")
ax.set_ylabel("Y axis (Fixed for Simplicity)")
ax.set_title("Prime Number Grid with RGB Colors (First 1000 Primes)")

# Show the plot
plt.show()
