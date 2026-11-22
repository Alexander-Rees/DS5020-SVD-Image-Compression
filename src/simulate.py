"""Reproduce the Iteration 2 low-rank signal and its noisy observation."""
import numpy as np


def simulate_low_rank(m=120, n=80, r=5, noise=0.01, seed=0):
    rng = np.random.default_rng(seed)
    L = rng.standard_normal((m, r))
    R = rng.standard_normal((r, n))
    Z = rng.standard_normal((m, n))
    B = L @ R
    return B + noise * Z, B
