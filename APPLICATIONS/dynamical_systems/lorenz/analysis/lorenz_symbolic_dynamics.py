import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

# -------------------------------
# Lorenz parameters
# -------------------------------

sigma = 10
rho = 28
beta = 8/3

dt = 0.01
steps = 200000

# -------------------------------
# Lorenz system
# -------------------------------

def lorenz(x, y, z):

    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z

    return dx, dy, dz


# -------------------------------
# integrate trajectory
# -------------------------------

x = np.zeros(steps)
y = np.zeros(steps)
z = np.zeros(steps)

x[0], y[0], z[0] = 1, 1, 1

for i in range(steps-1):

    dx, dy, dz = lorenz(x[i], y[i], z[i])

    x[i+1] = x[i] + dx * dt
    y[i+1] = y[i] + dy * dt
    z[i+1] = z[i] + dz * dt


# -------------------------------
# L / R symbolic sequence
# -------------------------------

symbols = []

for xi in x:

    if xi > 0:
        symbols.append("R")
    else:
        symbols.append("L")


# remove transient
symbols = symbols[5000:]


# -------------------------------
# pattern detection
# -------------------------------

pattern_length = 3
patterns = []

for i in range(len(symbols)-pattern_length):

    p = "".join(symbols[i:i+pattern_length])
    patterns.append(p)


counter = Counter(patterns)

print("\nPattern counts (length 3):\n")

for k,v in counter.most_common():

    print(k, v)


# -------------------------------
# histogram plot
# -------------------------------

labels = list(counter.keys())
values = list(counter.values())

plt.figure(figsize=(10,5))

plt.bar(labels, values)

plt.title("Lorenz Symbolic Dynamics (3-pattern frequency)")
plt.xlabel("Pattern")
plt.ylabel("Occurrences")

plt.tight_layout()

plt.show()


# -------------------------------
# transition matrix
# -------------------------------

transitions = Counter()

for i in range(len(symbols)-1):

    pair = symbols[i] + symbols[i+1]
    transitions[pair] += 1


print("\nTransition counts:\n")

for k,v in transitions.items():

    print(k, v)
