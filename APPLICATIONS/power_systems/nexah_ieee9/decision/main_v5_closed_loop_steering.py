# APPLICATIONS/power_systems/nexah_ieee9/decision/main_v5_closed_loop_steering.py

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
RUN_ID = datetime.now().strftime("run_v5_closed_loop_steering_%Y%m%d_%H%M%S")
OUT_DIR = RESULTS_ROOT / RUN_ID


@dataclass
class ClosedLoopConfig:
    n_steps: int = 120
    lambda0: float = 0.50
    lambda_step_base: float = 0.015

    # base control
    preemptive_step_scale: float = 0.45
    strong_lambda_drop: float = 0.040
    steer_out_lambda_drop: float = 0.070
    recover_step_scale: float = 0.20

    # v5 steering
    target_distance: float = 0.45
    k_steer: float = 0.18
    steer_clip: float = 0.06

    # plant
    noise_scale: float = 0.004
    collapse_center: float = 2.05
    collapse_sharpness: float = 9.0


# ============================================================
# HELPERS
# ============================================================

def ensure_out_dir() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)


def sigmoid(z: np.ndarray | float) -> np.ndarray | float:
    return 1.0 / (1.0 + np.exp(-z))


# ============================================================
# PLANT
# ============================================================

class NexahClosedLoopPlant:
    def __init__(self, cfg: ClosedLoopConfig):
        self.cfg = cfg

    def step(self, lam: float, control_bias: float, t: int) -> dict[str, float]:
        lam_eff = max(0.0, lam - control_bias)

        risk = float(sigmoid((lam_eff - self.cfg.collapse_center) * self.cfg.collapse_sharpness))

        d2c = float(
            self.cfg.collapse_sharpness
            * risk
            * (1.0 - risk)
            * (1.0 - 2.0 * risk)
        )

        residual = float(0.15 * lam_eff + 0.7 * risk + 0.2 * abs(d2c))
        distance = float(max(0.0, 1.15 - 1.05 * risk - 0.18 * lam_eff))

        return {
            "risk": risk,
            "d2c": d2c,
            "residual": residual,
            "distance": distance,
            "lambda_eff": lam_eff,
        }


# ============================================================
# ACTION → CONTROL
# ============================================================

def action_to_control(action: str, cfg: ClosedLoopConfig) -> tuple[float, float]:
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

    if action == "REDUCE_LOAD + REACTIVE_SUPPORT":
        return 0.030, 0.10

    return 0.0, 1.0


def steering_term(distance: float, action: str, cfg: ClosedLoopConfig) -> float:
    """
    Steering tries to keep the trajectory away from very small distance values.
    If distance < target_distance, term becomes negative and pushes lambda down.
    """
    raw = cfg.k_steer * (distance - cfg.target_distance)
    raw = float(np.clip(raw, -cfg.steer_clip, cfg.steer_clip))

    # only steer meaningfully when action implies intervention
    if action in {
        "PREEMPTIVE_STABILIZE",
        "STRONG_INTERVENTION",
        "STRONG_INTERVENTION + STEER_OUT",
        "REDUCE_LOAD + REACTIVE_SUPPORT",
        "DAMPEN + SMOOTH_RECOVERY",
    }:
        return raw

    return 0.0


# ============================================================
# CLOSED LOOP
# ============================================================

def run_closed_loop(cfg: ClosedLoopConfig):
    rng = np.random.default_rng(42)

    controller = NexahStateMachineController(NexahThresholds())
    plant = NexahClosedLoopPlant(cfg)

    lam = cfg.lambda0

    lambda_history = []
    lambda_eff_history = []
    control_bias_history = []
    steer_history = []

    risk_history = []
    slope_history = []
    d2c_history = []
    residual_history = []
    distance_history = []

    state_history = []
    action_history = []
    log_lines = []

    prev_risk = None
    prev_distance = None

    last_action = "MONITOR"

    for t in range(cfg.n_steps):
        control_bias, step_scale = action_to_control(last_action, cfg)

        obs = plant.step(lam=lam, control_bias=control_bias, t=t)

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

        steer = steering_term(distance, action, cfg)

        control_bias_next, step_scale_next = action_to_control(action, cfg)

        lam = max(
            0.0,
            lam + cfg.lambda_step_base * step_scale_next - control_bias_next + steer
        )

        lambda_history.append(lam)
        lambda_eff_history.append(obs["lambda_eff"])
        control_bias_history.append(control_bias_next)
        steer_history.append(steer)

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
            f"control_bias={control_bias_next:.4f} "
            f"steer={steer:.4f} "
            f"action={action}"
        )

        last_action = action
        prev_distance = distance

    return {
        "lambda": np.array(lambda_history),
        "lambda_eff": np.array(lambda_eff_history),
        "control_bias": np.array(control_bias_history),
        "steer": np.array(steer_history),
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
                "mode": "closed_loop_v5_steering",
                "n_steps": cfg.n_steps,
                "lambda0": cfg.lambda0,
                "lambda_step_base": cfg.lambda_step_base,
                "target_distance": cfg.target_distance,
                "k_steer": cfg.k_steer,
                "steer_clip": cfg.steer_clip,
            },
            f,
            indent=2,
        )

    np.save(OUT_DIR / "lambda.npy", data["lambda"])
    np.save(OUT_DIR / "lambda_eff.npy", data["lambda_eff"])
    np.save(OUT_DIR / "control_bias.npy", data["control_bias"])
    np.save(OUT_DIR / "steer.npy", data["steer"])
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
    ax.plot(data["lambda"], label="Lambda", alpha=0.85)
    ax.plot(data["steer"], label="Steer Term", alpha=0.85)
    ax.set_title("Closed-loop IEEE9 with NEXAH Steering (v5)")
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
    ax.plot(data["risk"], data["distance"], alpha=0.45)
    ax.axhline(cfg.target_distance, linestyle="--", alpha=0.7, label="target_distance")
    ax.set_title("Closed-loop NEXAH Trajectory on Field (v5)")
    ax.set_xlabel("Risk")
    ax.set_ylabel("Distance to Separatrix")
    ax.grid(True)
    ax.legend()
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
    print(f"Saved closed-loop v5 steering results to: {OUT_DIR}")
