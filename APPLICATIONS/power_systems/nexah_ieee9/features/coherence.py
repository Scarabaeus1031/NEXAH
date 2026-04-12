import numpy as np

def compute_coherence(theta):
    return abs(np.mean(np.exp(1j * theta)))
