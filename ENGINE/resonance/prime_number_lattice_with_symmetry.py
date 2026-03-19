import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------
SIZE = 5  # Grid size (5x5 grid)
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]  # List of first primes to place

# ---------------------------------------------------------
# FUNCTION TO GENERATE PRIME NUMBER LATTICE
# ---------------------------------------------------------
def generate_prime_lattice(size, primes):
    lattice = np.zeros((size, size))
    prime_idx = 0

    # Fill lattice with prime numbers in a specific pattern
    for i in range(size):
        for j in range(size):
            lattice[i, j] = primes[prime_idx % len(primes)]
            prime_idx += 1

    return lattice

# ---------------------------------------------------------
# PLOT PRIME NUMBER LATTICE
# ---------------------------------------------------------
lattice = generate_prime_lattice(SIZE, PRIMES)

plt.figure(figsize=(8,8))
plt.imshow(lattice, cmap='viridis', interpolation='nearest')
plt.title("Prime Number Lattice with Symmetry")
plt.xlabel("X Axis")
plt.ylabel("Y Axis")
plt.colorbar(label="Prime Value")
plt.tight_layout()
plt.savefig("Prime_Number_Lattice_with_Symmetry.png")
plt.show()
