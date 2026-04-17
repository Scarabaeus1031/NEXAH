from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List, Optional, Tuple

import numpy as np


Array = np.ndarray
FieldFunction = Callable[[float, float], Array]
ControlFunction = Callable[[Array, Array, float, float], Array]


@dataclass
class StepResult:
    state: Array
    field: Array
    coherence: float
    risk: float
    control: Array


@dataclass
class SimulationResult:
    states: Array
    fields: Array
    coherences: Array
    risks: Array
    controls: Array


def default_field(x: float, y: float) -> Array:
    """
    Stable damped spiral field.
    """
    return np.array([y, -x - 0.3 * y], dtype=float)


def coherence(state: Array, velocity: Array, field_vec: Optional[Array] = None) -> float:
    """
    Compute coherence as alignment between actual motion and field dynamics.

    C(x) = <x_dot, F(x)> / (||x_dot|| ||F(x)||)
    """
    if field_vec is None:
        field_vec = velocity

    denom = np.linalg.norm(velocity) * np.linalg.norm(field_vec)
    if denom < 1e-12:
        return 1.0

    return float(np.dot(velocity, field_vec) / denom)


def risk_from_coherence(c: float, mode: str = "one_minus_c") -> float:
    """
    Map coherence to risk.

    Supported modes:
    - 'one_minus_c' : R = 1 - C
    - 'negative_only': R = max(0, -C)
    """
    if mode == "one_minus_c":
        return float(1.0 - c)
    if mode == "negative_only":
        return float(max(0.0, -c))
    raise ValueError(f"Unknown risk mode: {mode}")


def default_control(state: Array, field_vec: Array, c: float, r: float) -> Array:
    """
    Simple field-aware control:
    if coherence is low, apply an upward correction.
    """
    if c < 0.3:
        return np.array([0.0, 0.6], dtype=float)
    return np.zeros(2, dtype=float)


class FieldController:
    """
    Minimal NEXAH-style controller operating on:
    - field dynamics
    - coherence
    - risk
    - simple control law
    """

    def __init__(
        self,
        field_fn: FieldFunction = default_field,
        control_fn: ControlFunction = default_control,
        risk_mode: str = "one_minus_c",
        dt: float = 0.05,
    ) -> None:
        self.field_fn = field_fn
        self.control_fn = control_fn
        self.risk_mode = risk_mode
        self.dt = dt

    def field(self, state: Array) -> Array:
        return self.field_fn(float(state[0]), float(state[1]))

    def step(self, state: Array) -> StepResult:
        field_vec = self.field(state)

        # In this minimal version, observed velocity starts as field velocity
        velocity = field_vec.copy()

        c = coherence(state, velocity, field_vec)
        r = risk_from_coherence(c, mode=self.risk_mode)
        u = self.control_fn(state, field_vec, c, r)

        next_state = state + self.dt * (field_vec + u)

        return StepResult(
            state=next_state,
            field=field_vec,
            coherence=c,
            risk=r,
            control=u,
        )

    def simulate(self, x0: Array, steps: int = 200) -> SimulationResult:
        state = np.array(x0, dtype=float)

        states: List[Array] = []
        fields: List[Array] = []
        coherences: List[float] = []
        risks: List[float] = []
        controls: List[Array] = []

        for _ in range(steps):
            states.append(state.copy())

            result = self.step(state)

            fields.append(result.field.copy())
            coherences.append(result.coherence)
            risks.append(result.risk)
            controls.append(result.control.copy())

            state = result.state

        return SimulationResult(
            states=np.array(states),
            fields=np.array(fields),
            coherences=np.array(coherences),
            risks=np.array(risks),
            controls=np.array(controls),
        )


if __name__ == "__main__":
    controller = FieldController()
    result = controller.simulate(x0=np.array([-2.0, -1.5]), steps=120)

    print("Simulation complete")
    print("Final state:", result.states[-1])
    print("Mean coherence:", np.mean(result.coherences))
    print("Mean risk:", np.mean(result.risks))
    print("Number of interventions:", np.sum(np.linalg.norm(result.controls, axis=1) > 0))
