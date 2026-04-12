import numpy as np

def compute_structural_state(V, theta, lam, w=(1.0, 1.0, 0.5)):
    R = abs(np.mean(np.exp(1j * theta)))  # coherence
    voltage_spread = np.std(V)
    
    c = w[0] * (1 - R) + w[1] * voltage_spread + w[2] * lam
    
    return c, R, voltage_spread
