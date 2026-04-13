# APPLICATIONS/power_systems/nexah_ieee9/decision/main_v4_closed_loop.py

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

from nexah_ieee9.controller.nexah_state_machine import (
    NexahStateMachineController,
    NexahMetrics,
    NexahThresholds,
)


# ============================================================
# CONFIG
# ============================================================

RESULTS_ROOT = Path("APPLICATIONS/power_systems/nexah_ieee9/results")
RUN_ID = datetime.now().strftime("run_v4_closed_loop_%Y%m%d_%H%M%S")
OUT_DIR = RESULTS_ROOT / RUN_ID


@dataclass
class ClosedLoopConfig:
    n_steps: int = 120
    lambda0: float = 0.50
    lambda_step_base: float = 0.015

    # closed-loop gains
    preemptive_step_scale: float = 0.45
    strong_lambda_drop: float = 0.040
    steer_out_lambda_drop: float = 0.070
    recover_step_scale: float = 0.20

    # damping / smoothing
    smooth_window: int = 5

    # synthetic plant parameters for v4 prototype
    noise_scale: float = 0.004
    collapse_center: float = 2.05
    collapse_sharpness: float = 9.0


# ============================================================
# HELPERS
# ============================================================

def ensure_out_dir() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)


def smooth(x: np.ndarray, window: int = 5) -> np.ndarray:
    if window <= 1 or len(x) < window:
        return x.copy()
    kernel = np.ones(window) / window
    return np.convolve(x, kernel, mode="same")


def sigmoid(z: np.ndarray | float) -> np.ndarray | float:
    return 1.0 / (1.0 + np.exp(-z))


# ============================================================
# SYNTHETIC CLOSED-LOOP PLANT
# ------------------------------------------------------------
# This is the bridge step:
# first make the controller affect a plant,
# then later replace this with your actual IEEE9 solver call.
# ============================================================

class NexahClosedLoopPlant:
    def __init__(self, cfg: ClosedLoopConfig):
        self.cfg = cfg

    def step(self, lam: float, control_bias: float, t: int) -> dict[str, float]:
        """
        Prototype closed-loop plant.
        Later, replace this with:
            - actual IEEE9 solver call
            - feature extraction
            - manifold / residual / distance calculation
        """

        # Effective stress after control
        lam_eff = max(0.0, lam - control_bias)

        # Risk rises nonlinearly near collapse
        risk = float(sigmoid((lam_eff - self.cfg.collapse_center) * self.cfg.collapse_sharpness))

        # Curvature proxy: highest near transition
        d2c = float(
            self.cfg.collapse_sharpness
            * risk
            * (1.0 - risk)
            * (1.0 - 2.0 * risk)
        )

        # Residual proxy: grows around transition/collapse
        residual = float(0.15 * lam_eff + 0.7 * risk + 0.2 * abs(d2c))

        # Distance-to-separatrix proxy: decreases as risk rises
        distance = float(max(0.0, 1.15 - 1.05 * risk - 0.18 * lam_eff))

        # Coherence / fragmentation style proxies if needed later
        # not returned now because controller currently uses risk/distance/residual/d2c

        return {
            "risk": risk,
            "d2c": d2c,
            "residual": residual,
            "distance": distance,
            "lambda_eff": lam_eff,
        }


# ============================================================
# ACTION → PHYSICAL MODULATION
# ============================================================

def action_to_control(action: str, cfg: ClosedLoopConfig) -> tuple[float, float]:
    """
    Returns:
        control_bias: how much effective load/stress is reduced this step
        step_scale:   how much lambda is allowed to increase next
    """
    if action == "MONITOR":
        return 0.0, 1.0

    if action == "PREEMPTIVE_STABILIZE":
        return 0.015, cfg.preemptive_step_scale

    if action == "STRONG_INTERVENTION":
        return cfg.strong_lambda_drop, 0.15

    if action == "STRONG_INTERVENTION + STEER_OUT":
        return cfg.steer_out_lambda_drop, 0.05

    if action == "DAMPEN + SMOOTH_RECOVERY":
        return 0.020, cfg.recover_step_scale

    return 0.0, 1.0


# ============================================================
# CLOSED LOOP RUN
# ============================================================

def run_closed_loop(cfg: ClosedLoopConfig):
    rng = np.random.default_rng(42)

    controller = NexahStateMachineController(NexahThresholds())
    plant = NexahClosedLoopPlant(cfg)

    lam = cfg.lambda0
    lambda_history = []
    lambda_eff_history = []

    risk_history = []
    slope_history = []
    d2c_history = []
    residual_history = []
    distance_history = []

    state_history = []
    action_history = []
    log_lines = []

    prev_risk = None

    for t in range(cfg.n_steps):
        # Last action influences current plant via control_bias
        if t == 0:
            last_action = "MONITOR"
        else:
            last_action = action_history[-1]

        control_bias, step_scale = action_to_control(last_action, cfg)

        obs = plant.step(lam=lam, control_bias=control_bias, t=t)

        # add tiny noise so it doesn't look unrealistically perfect
        risk = max(0.0, obs["risk"] + rng.normal(0.0, cfg.noise_scale))
        distance = max(0.0, obs["distance"] + rng.normal(0.0, cfg.noise_scale))
        residual = obs["residual"] + rng.normal(0.0, cfg.noise_scale)
        d2c = obs["d2c"] + rng.normal(0.0, cfg.noise_scale)

        if prev_risk is None:
            risk_slope = 0.0
        else:
            risk_slope = risk - prev_risk
        prev_risk = risk

        metrics = NexahMetrics(
            risk=float(risk),
            risk_slope=float(risk_slope),
            d2c=float(d2c),
            residual=float(residual),
            distance_to_sep=float(distance),
        )

        prev_state = controller.state
        action = controller.action(metrics)
        state = controller.state

        # apply action to next lambda
        control_bias_next, step_scale_next = action_to_control(action, cfg)

        # lambda update
        lam = max(
            0.0,
            lam + cfg.lambda_step_base * step_scale_next - control_bias_next
        )

        lambda_history.append(lam)
        lambda_eff_history.append(obs["lambda_eff"])

        risk_history.append(risk)
        slope_history.append(risk_slope)
        d2c_history.append(d2c)
        residual_history.append(residual)
        distance_history.append(distance)

        state_history.append(state.value)
        action_history.append(action)

        if state != prev_state:
            log_lines.append(f"[STATE CHANGE] step={t} {prev_state.name} -> {state.name}")

        log_lines.append(
            f"[STEP {t}] "
            f"lambda={lam:.4f} "
            f"lambda_eff={obs['lambda_eff']:.4f} "
            f"state={state.name} "
            f"risk={risk:.4f} "
            f"slope={risk_slope:.4f} "
            f"d2c={d2c:.4f} "
            f"res={residual:.4f} "
            f"dist={distance:.4f} "
            f"action={action}"
        )

    return {
        "lambda": np.array(lambda_history),
        "lambda_eff": np.array(lambda_eff_history),
        "risk": np.array(risk_history),
        "risk_slope": np.array(slope_history),
        "d2c": np.array(d2c_history),
        "residual": np.array(residual_history),
        "distance": np.array(distance_history),
        "states": np.array(state_history),
        "actions": action_history,
        "log": log_lines,
    }


# ============================================================
# SAVE
# ============================================================

def save_results(data: dict[str, np.ndarray | list[str]], cfg: ClosedLoopConfig) -> None:
    ensure_out_dir()

    with open(OUT_DIR / "meta.json", "w") as f:
        json.dump(
            {
                "run_id": RUN_ID,
                "mode": "closed_loop_v4",
                "n_steps": cfg.n_steps,
                "lambda0": cfg.lambda0,
                "lambda_step_base": cfg.lambda_step_base,
            },
            f,
            indent=2,
        )

    np.save(OUT_DIR / "lambda.npy", data["lambda"])
    np.save(OUT_DIR / "lambda_eff.npy", data["lambda_eff"])
    np.save(OUT_DIR / "risk.npy", data["risk"])
    np.save(OUT_DIR / "risk_slope.npy", data["risk_slope"])
    np.save(OUT_DIR / "d2c.npy", data["d2c"])
    np.save(OUT_DIR / "residual.npy", data["residual"])
    np.save(OUT_DIR / "distance.npy", data["distance"])
    np.save(OUT_DIR / "controller_states.npy", data["states"])

    with open(OUT_DIR / "controller_actions.txt", "w") as f:
        for a in data["actions"]:
            f.write(f"{a}\n")

    with open(OUT_DIR / "controller_log.txt", "w") as f:
        f.write("\n".join(data["log"]))

    # plot 1
    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(111)
    ax.plot(data["risk"], label="Risk")
    ax.plot(data["distance"], label="Distance to Separatrix")
    ax.plot(data["states"], "--", label="Controller State")
    ax.plot(data["lambda"], label="Lambda", alpha=0.8)
    ax.set_title("Closed-loop IEEE9 with NEXAH Steering (v4)")
    ax.set_xlabel("Time Step")
    ax.grid(True)
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT_DIR / "closed_loop_timeseries.png", dpi=200)
    plt.close(fig)

    # plot 2
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111)
    sc = ax.scatter(data["risk"], data["distance"], c=data["states"], s=30)
    ax.plot(data["risk"], data["distance"], alpha=0.4)
    ax.set_title("Closed-loop NEXAH Trajectory on Field")
    ax.set_xlabel("Risk")
    ax.set_ylabel("Distance to Separatrix")
    ax.grid(True)
    fig.colorbar(sc, ax=ax, label="State")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "closed_loop_field.png", dpi=200)
    plt.close(fig)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    cfg = ClosedLoopConfig()
    data = run_closed_loop(cfg)
    save_results(data, cfg)
    print(f"Saved closed-loop v4 results to: {OUT_DIR}")
