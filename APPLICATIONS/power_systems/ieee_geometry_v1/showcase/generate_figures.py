"""Generate the four canonical Phase V showcase figures from JSON artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt


CASE_DIR = Path(__file__).parents[1]
DEFAULT_OUTPUT_DIR = Path(__file__).parent / "figures"
NAVY = "#17365d"
BLUE = "#2d6cdf"
ORANGE = "#d97706"
GREEN = "#26834a"
RED = "#b42318"
GRAY = "#667085"


def _load(name: str) -> dict[str, Any]:
    value = json.loads((CASE_DIR / name).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"canonical artifact must be an object: {name}")
    return value


def _feature_series(
    frames: dict[str, Any], feature_name: str
) -> tuple[list[float], list[float]]:
    x: list[float] = []
    y: list[float] = []
    for frame in frames["frames"]:
        features = frame["system_features"]
        if frame["status"] != "converged" or features is None:
            continue
        position = features["feature_names"].index(feature_name)
        x.append(frame["load_scale"])
        y.append(features["values"][position])
    return x, y


def _available_step_series(
    geometry: dict[str, Any], field: str
) -> tuple[list[float], list[float]]:
    x: list[float] = []
    y: list[float] = []
    for step in geometry["analysis"]["steps"]:
        value = step[field]
        if step["status"] == "available" and value is not None:
            x.append(step["target_load_scale"])
            y.append(value)
    return x, y


def _available_turn_series(
    geometry: dict[str, Any], frames: dict[str, Any], field: str
) -> tuple[list[float], list[float]]:
    x: list[float] = []
    y: list[float] = []
    load_scales = [frame["load_scale"] for frame in frames["frames"]]
    for turn in geometry["analysis"]["turns"]:
        value = turn[field]
        if turn["status"] == "available" and value is not None:
            x.append(load_scales[turn["center_index"]])
            y.append(value)
    return x, y


def _style_axis(axis: Any, *, xlabel: bool = True) -> None:
    axis.grid(True, color="#d0d5dd", linewidth=0.7, alpha=0.7)
    axis.spines[["top", "right"]].set_visible(False)
    axis.tick_params(colors=NAVY)
    if xlabel:
        axis.set_xlabel("Declared load scale λ (not time)", color=NAVY)


def _save(figure: Any, path: Path) -> None:
    figure.savefig(
        path,
        dpi=180,
        bbox_inches="tight",
        facecolor="white",
        metadata={"Software": "NEXAH Phase V canonical figure generator"},
    )
    plt.close(figure)


def physical_campaign_figure(
    development_frames: dict[str, Any],
    evaluation_frames: dict[str, Any],
    path: Path,
) -> None:
    figure, axes = plt.subplots(2, 1, figsize=(10.5, 7.0), sharex=True)
    series = (
        (development_frames, "IEEE-9 development", ORANGE),
        (evaluation_frames, "IEEE-14 evaluation", BLUE),
    )
    for frames, label, color in series:
        x, y = _feature_series(frames, "minimum_bus_voltage")
        axes[0].plot(x, y, marker="o", markersize=4, linewidth=2, label=label, color=color)
        x, y = _feature_series(frames, "maximum_line_loading")
        axes[1].plot(x, y, marker="o", markersize=4, linewidth=2, label=label, color=color)
    axes[0].set_title("Physical benchmark summaries along the frozen campaign", color=NAVY)
    axes[0].set_ylabel("Minimum bus voltage (pu)", color=NAVY)
    axes[1].set_ylabel("Maximum line loading (%)", color=NAVY)
    for axis in axes:
        _style_axis(axis, xlabel=axis is axes[1])
        axis.legend(frameon=False)
    figure.suptitle("IEEE-9 DEVELOPMENT vs IEEE-14 LOCKED EVALUATION", color=NAVY, fontweight="bold")
    figure.tight_layout()
    _save(figure, path)


def path_geometry_figure(
    development_geometry: dict[str, Any],
    evaluation_geometry: dict[str, Any],
    path: Path,
) -> None:
    figure, axes = plt.subplots(2, 1, figsize=(10.5, 7.0), sharex=True)
    series = (
        (development_geometry, "IEEE-9 development", ORANGE),
        (evaluation_geometry, "IEEE-14 evaluation", BLUE),
    )
    for geometry, label, color in series:
        x, y = _available_step_series(geometry, "normalized_local_drift")
        axes[0].plot(x, y, marker="o", markersize=4, linewidth=2, label=label, color=color)
        x, y = _available_step_series(geometry, "cumulative_path_length")
        axes[1].plot(x, y, marker="o", markersize=4, linewidth=2, label=label, color=color)
    axes[0].set_title("Frozen standardized system-summary geometry", color=NAVY)
    axes[0].set_ylabel("Normalized local drift", color=NAVY)
    axes[1].set_ylabel("Cumulative path length", color=NAVY)
    for axis in axes:
        _style_axis(axis, xlabel=axis is axes[1])
        axis.legend(frameon=False)
    figure.suptitle("LOCAL CHANGE AND ACCUMULATED PATH", color=NAVY, fontweight="bold")
    figure.tight_layout()
    _save(figure, path)


def turning_geometry_figure(
    development_geometry: dict[str, Any],
    evaluation_geometry: dict[str, Any],
    development_frames: dict[str, Any],
    evaluation_frames: dict[str, Any],
    path: Path,
) -> None:
    figure, axes = plt.subplots(2, 1, figsize=(10.5, 7.0), sharex=True)
    series = (
        (development_geometry, development_frames, "IEEE-9 development", ORANGE),
        (evaluation_geometry, evaluation_frames, "IEEE-14 evaluation", BLUE),
    )
    for geometry, frames, label, color in series:
        x, y = _available_turn_series(geometry, frames, "direction_change_radians")
        axes[0].plot(x, y, marker="o", markersize=4, linewidth=2, label=label, color=color)
        x, y = _available_turn_series(geometry, frames, "discrete_curvature")
        axes[1].plot(x, y, marker="o", markersize=4, linewidth=2, label=label, color=color)
    axes[0].set_title("Centered three-frame measurements", color=NAVY)
    axes[0].set_ylabel("Direction change (radians)", color=NAVY)
    axes[1].set_ylabel("Discrete curvature", color=NAVY)
    for axis in axes:
        _style_axis(axis, xlabel=axis is axes[1])
        axis.legend(frameon=False)
    figure.suptitle("DIRECTION CHANGE AND LOCAL CURVATURE", color=NAVY, fontweight="bold")
    figure.tight_layout()
    _save(figure, path)


def evidence_boundary_figure(
    development_frames: dict[str, Any],
    evaluation_frames: dict[str, Any],
    path: Path,
) -> None:
    figure, axis = plt.subplots(figsize=(10.5, 4.8))
    rows = (
        (development_frames, 1.0, "IEEE-9 development"),
        (evaluation_frames, 0.0, "IEEE-14 evaluation"),
    )
    for frames, row, label in rows:
        for frame in frames["frames"]:
            converged = frame["status"] == "converged"
            axis.scatter(
                frame["load_scale"],
                row,
                s=78,
                color=GREEN if converged else RED,
                marker="o" if converged else "X",
                zorder=3,
            )
        axis.plot(
            [frames["frames"][0]["load_scale"], frames["frames"][-1]["load_scale"]],
            [row, row],
            color="#d0d5dd",
            linewidth=2,
            zorder=1,
        )
    axis.axvspan(2.25, 2.45, color=RED, alpha=0.07)
    axis.annotate(
        "IEEE-9: solver evidence stops after λ=2.2",
        xy=(2.3, 1.0),
        xytext=(1.55, 1.37),
        arrowprops={"arrowstyle": "->", "color": RED},
        color=NAVY,
    )
    axis.text(
        0.6,
        -0.48,
        "IEEE-14: no sampled solver boundary on the frozen grid — no extrapolation",
        color=NAVY,
    )
    axis.text(
        0.6,
        -0.66,
        "Benchmark computation only · observed outcome: none · episodic memory: closed",
        color=GRAY,
    )
    axis.set_yticks([0.0, 1.0], ["IEEE-14 evaluation", "IEEE-9 development"])
    axis.set_ylim(-0.78, 1.58)
    axis.set_xlim(0.55, 2.45)
    axis.set_xlabel("Declared load scale λ (not time)", color=NAVY)
    axis.set_title("EVIDENCE AVAILABILITY AND ITS BOUNDARY", color=NAVY, fontweight="bold")
    _style_axis(axis, xlabel=False)
    axis.scatter([], [], color=GREEN, marker="o", label="converged physical frame")
    axis.scatter([], [], color=RED, marker="X", label="explicit failed frame")
    axis.legend(frameon=False, loc="upper left")
    figure.tight_layout()
    _save(figure, path)


def generate_all(output_dir: Path = DEFAULT_OUTPUT_DIR) -> tuple[Path, ...]:
    output_dir.mkdir(parents=True, exist_ok=True)
    development_frames = _load("development_frames.json")
    evaluation_frames = _load("evaluation_frames.json")
    development_geometry = _load("development_geometry.json")
    evaluation_geometry = _load("evaluation_geometry.json")
    paths = (
        output_dir / "01-physical-campaign.png",
        output_dir / "02-path-geometry.png",
        output_dir / "03-turning-geometry.png",
        output_dir / "04-evidence-boundary.png",
    )
    physical_campaign_figure(development_frames, evaluation_frames, paths[0])
    path_geometry_figure(development_geometry, evaluation_geometry, paths[1])
    turning_geometry_figure(
        development_geometry,
        evaluation_geometry,
        development_frames,
        evaluation_frames,
        paths[2],
    )
    evidence_boundary_figure(development_frames, evaluation_frames, paths[3])
    return paths


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    for path in generate_all(args.out_dir):
        print(path)


if __name__ == "__main__":
    main()
