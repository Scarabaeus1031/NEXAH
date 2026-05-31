"""

ATLAS NAVIGATION CONTROLLER V1

Historical prototype developed prior to

EXP_29–EXP_36 Atlas Operations.

Implements a risk-driven state machine based on:

- risk

- residual

- distance to separatrix

The controller predates:

- Basin Discovery

- Recovery Corridors

- Recovery Anchors

- Atlas-Guided Control

and serves as the conceptual precursor

to future atlas-native controllers.

"""

from enum import Enum, auto
from dataclasses import dataclass


class NexahState(Enum):
    NEXIT = auto()
    ENGAGE = auto()
    LOCK = auto()
    RELEASE = auto()


@dataclass
class NexahMetrics:
    risk: float
    risk_slope: float
    d2c: float
    residual: float
    distance_to_sep: float


@dataclass
class NexahThresholds:
    d_engage: float = 4.0
    d_lock: float = 1.8
    d_release: float = 4.5

    r_engage: float = 0.18
    r_release: float = 0.12

    c_lock: float = 0.08
    res_lock: float = 0.25


class NexahStateMachineController:
    def __init__(self, thresholds: NexahThresholds):
        self.thresholds = thresholds
        self.state = NexahState.NEXIT

    def transition(self, m: NexahMetrics) -> NexahState:
        t = self.thresholds

        if self.state == NexahState.NEXIT:
            if (
                m.distance_to_sep < t.d_engage
                and m.risk > t.r_engage
                and m.risk_slope > 0
            ):
                self.state = NexahState.ENGAGE

        elif self.state == NexahState.ENGAGE:
            if (
                m.distance_to_sep < t.d_lock
                and (m.d2c > t.c_lock or m.residual > t.res_lock)
            ):
                self.state = NexahState.LOCK
            elif m.distance_to_sep > t.d_release and m.risk < t.r_release:
                self.state = NexahState.NEXIT

        elif self.state == NexahState.LOCK:
            if m.risk_slope <= 0 or m.distance_to_sep > t.d_lock:
                self.state = NexahState.RELEASE

        elif self.state == NexahState.RELEASE:
            if m.distance_to_sep > t.d_release and m.risk < t.r_release:
                self.state = NexahState.NEXIT
            elif m.distance_to_sep < t.d_lock:
                self.state = NexahState.LOCK

        return self.state

    def action(self, m: NexahMetrics) -> str:
        state = self.transition(m)

        if state == NexahState.NEXIT:
            return "MONITOR"

        if state == NexahState.ENGAGE:
            return "PREEMPTIVE_STABILIZE"

        if state == NexahState.LOCK:
            if m.residual > self.thresholds.res_lock:
                return "REDUCE_LOAD + REACTIVE_SUPPORT"
            return "STRONG_INTERVENTION"

        if state == NexahState.RELEASE:
            return "DAMPEN + SMOOTH_RECOVERY"

        return "MONITOR"
