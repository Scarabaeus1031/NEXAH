# nexah_state_machine_replay.py

from __future__ import annotations

import json
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# STATE MACHINE
# ============================================================

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
    d_engage: float = 0.65
    d_lock: float = 0.08
    d_release: float = 0.20

    r_engage: float = 0.18
    r_release: float = 0.10

    c_lock: float = 0.02
    res_lock: float = 0.12


class StableNexahController:
    def __init__(self, thresholds: NexahThresholds):
        self.thresholds = thresholds
        self.state = NexahState.NEXIT
        self.cooldown = 0
        self.min_hold_steps = 3
        self.last_state_change = -999

    def transition(self, m: NexahMetrics, step: int) -> NexahState:
        prev_state = self.state
        t = self.thresholds

        if self.cooldown > 0:
            self.cooldown -= 1
            return self.state

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
            if m.risk_slope <= 0:
                self.state = NexahState.RELEASE

        elif self.state == NexahState.RELEASE:
            if m.distance_to_sep > t.d_release and m.risk < t.r_release:
                self.state = NexahState.NEXIT
            elif m.distance_to_sep < t.d_lock and m.risk > t.r_release:
                self.state = NexahState.LOCK

        # hysteresis
        if self.state != prev_state:
            if step - self.last_state_change < self.min_hold_steps:
                self.state = prev_state
            else:
                self.cooldown = 2
                self.last_state_change = step

        return self.state

    def action(self, m: NexahMetrics, step: int) -> str:
        state = self.transition(m, step)

        if state == NexahState.NEXIT:
            return "MONITOR"

        if state == NexahState.ENGAGE:
            return "PREEMPTIVE_STABILIZE"

        if state == NexahState.LOCK:
            if m.distance_to_sep < 0.05:
                return "STRONG_INTERVENTION + STEER_OUT"
            if m.residual > self.thresholds.res_lock:
                return "REDUCE_LOAD + REACTIVE_SUPPORT"
            return "STRONG_INTERVENTION"

        if state == NexahState.RELEASE:
            return "DAMPEN + RECOVER"

        return "MONITOR"


# ============================================================
# IO
# ============================================================

RESULTS_ROOT = Path("APPLICATIONS/power_systems/nexah_ieee9/results")
OUT_ROOT = RESULTS_ROOT / "controller_runs"


def find_latest_run(results_root: Path) -> Path:
    candidates = [p for p in results_root.iterdir() if p.is_dir() and p.name.startswith("run_")]
    if not candidates:
        raise FileNotFoundError(f"No run_* directories found in {results_root}")
    return sorted(candidates)[-1]


def load_array(run_dir: Path, name: str, required: bool = True) -> np.ndarray | None:
    path = run_dir / name
    if path.exists():
        return np.load(path)
    if required:
        raise FileNotFoundError(f"Missing required file: {path}")
    return None


def smooth(x: np.ndarray, window: int = 5) -> np.ndarray:
    if window <= 1 or len(x) < window:
        return x.copy()
    kernel = np.ones(window) / window
    return np.convolve(x, kernel, mode="same")


# ============================================================
# BUILD METRICS
# ============================================================

def build_metrics_series(run_dir: Path) -> dict[str, np.ndarray]:
    risk = load_array(run_dir, "risk.npy")
    distance = load_array(run_dir, "distance.npy")
    residual = load_array(run_dir, "residual.npy")
    d2c = load_array(run_dir, "d2c.npy", required=False)

    if d2c is None:
        d2c = np.zeros_like(risk)

    # optional smoothing
    risk_s = smooth(risk, window=5)
    distance_s = smooth(distance, window=5)
    residual_s = smooth(residual, window=5)
    d2c_s = smooth(d2c, window=5)

    risk_slope = np.gradient(risk_s)

    return {
        "risk": risk_s,
        "distance": distance_s,
        "residual": residual_s,
        "d2c": d2c_s,
        "risk_slope": risk_slope,
    }


# ============================================================
# REPLAY
# ============================================================

def replay_controller(metrics: dict[str, np.ndarray], thresholds: NexahThresholds):
    controller = StableNexahController(thresholds)

    n = len(metrics["risk"])
    states = []
    actions = []
    logs = []

    for i in range(n):
        m = NexahMetrics(
            risk=float(metrics["risk"][i]),
            risk_slope=float(metrics["risk_slope"][i]),
            d2c=float(metrics["d2c"][i]),
            residual=float(metrics["residual"][i]),
            distance_to_sep=float(metrics["distance"][i]),
        )
        prev_state = controller.state
        action = controller.action(m, i)
        state = controller.state

        if state != prev_state:
            logs.append(f"[STATE CHANGE] step={i} {prev_state.name} -> {state.name}")

        logs.append(
            f"[STEP {i}] state={state.name} "
            f"risk={m.risk:.4f} "
            f"slope={m.risk_slope:.4f} "
            f"d2c={m.d2c:.4f} "
            f"res={m.residual:.4f} "
            f"dist={m.distance_to_sep:.4f} "
            f"action={action}"
        )

        states.append(state.value)
        actions.append(action)

    return np.array(states), actions, logs


# ============================================================
# SAVE
# ============================================================

def save_outputs(
    source_run: Path,
    metrics: dict[str, np.ndarray],
    states: np.ndarray,
    actions: list[str],
    logs: list[str],
):
    OUT_ROOT.mkdir(parents=True, exist_ok=True)

    run_id = datetime.now().strftime("controller_replay_%Y%m%d_%H%M%S")
    out_dir = OUT_ROOT / run_id
    out_dir.mkdir(parents=True, exist_ok=True)

    # save metadata
    meta = {
        "source_run": str(source_run),
        "n_steps": int(len(states)),
    }
    with open(out_dir / "meta.json", "w") as f:
        json.dump(meta, f, indent=2)

    np.save(out_dir / "risk.npy", metrics["risk"])
    np.save(out_dir / "distance.npy", metrics["distance"])
    np.save(out_dir / "residual.npy", metrics["residual"])
    np.save(out_dir / "d2c.npy", metrics["d2c"])
    np.save(out_dir / "risk_slope.npy", metrics["risk_slope"])
    np.save(out_dir / "controller_states.npy", states)

    with open(out_dir / "controller_actions.txt", "w") as f:
        for a in actions:
            f.write(f"{a}\n")

    with open(out_dir / "controller_log.txt", "w") as f:
        f.write("\n".join(logs))

    # plot 1: timeseries
    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(111)
    ax.plot(metrics["risk"], label="Risk")
    ax.plot(metrics["distance"], label="Distance to Separatrix")
    ax.plot(states, "--", label="Controller State")
    ax.set_title("IEEE9 + NEXAH State Machine Replay")
    ax.set_xlabel("Time Step")
    ax.grid(True)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_dir / "timeseries.png", dpi=200)
    plt.close(fig)

    # plot 2: 2D field
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111)
    sc = ax.scatter(metrics["risk"], metrics["distance"], c=states, s=28)
    ax.set_title("NEXAH Controller on IEEE9 Field")
    ax.set_xlabel("Risk")
    ax.set_ylabel("Distance to Separatrix")
    ax.grid(True)
    fig.colorbar(sc, ax=ax, label="State")
    fig.tight_layout()
    fig.savefig(out_dir / "field_overlay.png", dpi=200)
    plt.close(fig)

    return out_dir


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    source_run = find_latest_run(RESULTS_ROOT)
    print(f"\nUsing source run: {source_run}\n")

    metrics = build_metrics_series(source_run)
    thresholds = NexahThresholds()

    states, actions, logs = replay_controller(metrics, thresholds)
    out_dir = save_outputs(source_run, metrics, states, actions, logs)

    print(f"Saved replay outputs to: {out_dir}")
