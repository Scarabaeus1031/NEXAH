# dominant_cycle_detector.py

import numpy as np
import matplotlib.pyplot as plt
from sympy import primerange
import networkx as nx
import os

# =========================
# CONFIG
# =========================

MODS = [7, 11, 13, 17, 19, 23, 29, 31]
N_PRIMES = 20000
TOP_K = 3
THRESHOLD = 0.03

OUTPUT_PATH = "output/plots"
os.makedirs(OUTPUT_PATH, exist_ok=True)

# =========================
# PRIME GENERATOR
# =========================

def generate_primes(n):
    primes = list(primerange(2, 300000))
    return np.array(primes[:n])

# =========================
# TRANSITION MATRIX
# =========================

def transition_matrix(sequence, mod):
    residues = sequence % mod
    T = np.zeros((mod, mod))

    for i in range(len(residues) - 1):
        a = residues[i]
        b = residues[i + 1]
        T[a, b] += 1

    row_sums = T.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1
    return T / row_sums

# =========================
#
