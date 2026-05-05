import numpy as np
import matplotlib.pyplot as plt

# --- Julia Set ---
def julia(c, size=200, iterations=100):
    x = np.linspace(-1.5, 1.5, size)
    y = np.linspace(-1.5, 1.5, size)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y

    mask = np.zeros(Z.shape, dtype=int)

    for i in range(iterations):
        Z = Z**2 + c
        mask += (np.abs(Z) < 2)

    return mask

# --- Kreis im Parameterraum ---
def generate_circle(center, radius, steps):
    angles = np.linspace(0, 2*np.pi, steps)
    return [center + radius * np.exp(1j * a) for a in angles]

# --- Δ berechnen ---
def compute_delta(j1, j2):
    return np.mean(np.abs(j1 - j2))

# --- Setup ---
center = -0.75 + 0j   # dein Bereich
radius = 0.3
steps = 100

circle = generate_circle(center, radius, steps)

# --- Δ entlang Kreis ---
deltas = []
prev = None

for c in circle:
    j = julia(c)

    if prev is not None:
        d = compute_delta(j, prev)
        deltas.append(d)
    else:
        deltas.append(0)

    prev = j

# --- Plot ---
plt.figure(figsize=(10,4))
plt.plot(deltas, color='red')
plt.title("Δ entlang Kreis im Parameterraum")
plt.xlabel("Position auf Kreis")
plt.ylabel("Δ")
plt.grid()
plt.show()
