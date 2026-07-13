"""Deterministic validation trajectories matching established NEXAH examples."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


FloatArray = NDArray[np.float64]


def lorenz(
    *,
    rho: float = 28.0,
    samples: int = 2500,
    initial: tuple[float, float, float] = (0.1, 0.0, 0.0),
) -> FloatArray:
    steps = samples + 1000
    dt = 0.01
    trajectory = np.zeros((steps, 3), dtype=np.float64)
    trajectory[0] = initial
    sigma, beta = 10.0, 2.667
    for index in range(steps - 1):
        x, y, z = trajectory[index]
        derivative = np.array(
            [sigma * (y - x), x * (rho - z) - y, x * y - beta * z]
        )
        trajectory[index + 1] = trajectory[index] + dt * derivative
    return trajectory[-samples:]


def rossler(
    *,
    c: float = 5.7,
    samples: int = 2500,
    initial: tuple[float, float, float] = (0.1, 0.0, 0.0),
) -> FloatArray:
    steps = samples + 1000
    dt = 0.01
    trajectory = np.zeros((steps, 3), dtype=np.float64)
    trajectory[0] = initial
    a, b = 0.2, 0.2
    for index in range(steps - 1):
        x, y, z = trajectory[index]
        derivative = np.array([-y - z, x + a * y, b + z * (x - c)])
        trajectory[index + 1] = trajectory[index] + dt * derivative
    return trajectory[-samples:]


def kuramoto(
    *,
    coupling: float = 2.2,
    samples: int = 2500,
    seed: int = 7,
) -> FloatArray:
    burn_in = 500
    steps = samples + burn_in
    dt = 0.04
    agents = 64
    rng = np.random.default_rng(seed)
    theta = rng.uniform(0.0, 2.0 * np.pi, agents)
    omega = rng.normal(0.0, 0.55, agents)
    order_values = np.zeros(steps, dtype=np.float64)

    for index in range(steps):
        order = np.mean(np.exp(1j * theta))
        magnitude = float(np.abs(order))
        phase = float(np.angle(order))
        order_values[index] = magnitude
        theta_dot = omega + coupling * magnitude * np.sin(phase - theta)
        theta = np.mod(theta + dt * theta_dot, 2.0 * np.pi)

    order_values = order_values[burn_in:]
    derivative = np.gradient(order_values) / dt
    return np.column_stack((order_values, derivative))


def add_relative_noise(
    trajectory: FloatArray,
    *,
    fraction: float,
    seed: int,
) -> FloatArray:
    if fraction < 0.0:
        raise ValueError("noise fraction must be non-negative")
    rng = np.random.default_rng(seed)
    scale = np.std(trajectory, axis=0)
    safe_scale = np.where(scale > 0.0, scale, 1.0)
    noise = rng.normal(0.0, fraction, trajectory.shape) * safe_scale
    return np.asarray(trajectory + noise, dtype=np.float64)
