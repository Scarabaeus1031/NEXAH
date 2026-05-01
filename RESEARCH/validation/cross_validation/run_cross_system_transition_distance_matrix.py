import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# ============================
# Systems
# ============================

def lorenz(x, y, z, s=10, r=28, b=8/3):
    return s*(y-x), x*(r-z)-y, x*y - b*z

def rossler(x, y, z, a=0.2, b=0.2, c=5.7):
    return -y - z, x + a*y, b + z*(x - c)

def duffing(x, v, t, delta=0.2, alpha=-1, beta=1, gamma=0.3, omega=1.2):
    dx = v
    dv = -delta*v - alpha*x - beta*x**3 + gamma*np.cos(omega*t)
    return dx, dv

# ============================
# Simulators
# ============================

def simulate_lorenz(steps=5000, dt=0.01):
    xs = np.zeros((steps,3))
    xs[0] = [0.0, 1.0, 1.05]
    for i in range(steps-1):
        dx = lorenz(*xs[i])
        xs[i+1] = xs[i] + dt*np.array(dx)
    return xs

def simulate_rossler(steps=5000, dt=0.01):
    xs = np.zeros((steps,3))
    xs[0] = [0.0, 1.0, 0.0]
    for i in range(steps-1):
        dx = rossler(*xs[i])
        xs[i+1] = xs[i] + dt*np.array(dx)
    return xs

def simulate_duffing(steps=5000, dt=0.01):
    xs = np.zeros((steps,2))
    xs[0] = [0.0, 1.0]
    t = 0
    for i in range(steps-1):
        dx = duffing(xs[i,0], xs[i,1], t)
        xs[i+1] = xs[i] + dt*np.array(dx)
        t += dt
    return xs

# ============================
# Transition matrix
# ============================

def compute_transition_matrix(labels, k):
    T = np.zeros((k,k))
    for i in range(len(labels)-1):
        T[labels[i], labels[i+1]] += 1
    T /= T.sum(axis=1, keepdims=True) + 1e-8
    return T

# ============================
# Main
# ============================

def run():

    k = 6

    systems = {
        "Lorenz": simulate_lorenz()[:,:2],
        "Rössler": simulate_rossler()[:,:2],
        "Duffing": simulate_duffing()
    }

    matrices = {}

    for name, data in systems.items():
        km = KMeans(n_clusters=k, n_init=10)
        labels = km.fit_predict(data)
        T = compute_transition_matrix(labels, k)
        matrices[name] = T

    # Plot
    plt.figure(figsize=(12,4))
    for i, (name, T) in enumerate(matrices.items()):
        plt.subplot(1,3,i+1)
        plt.imshow(T, cmap="viridis")
        plt.title(name)
    plt.tight_layout()
    plt.savefig("RESEARCH/validation/cross_system_transition_matrices.png")
    plt.close()

    print("✅ Saved: cross_system_transition_matrices.png")

    return matrices


if __name__ == "__main__":
    run()
