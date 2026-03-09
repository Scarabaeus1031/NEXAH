from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class DeltaResult:
    """
    Result container for ARCHY Delta Operator calculations.
    """

    base_orientation: float
    architectural_delta: float
    environmental_delta: float
    total_orientation: float
    drift_magnitude: float
    interpretation: str

    def as_dict(self) -> Dict[str, float | str]:
        return {
            "base_orientation": self.base_orientation,
            "architectural_delta": self.architectural_delta,
            "environmental_delta": self.environmental_delta,
            "total_orientation": self.total_orientation,
            "drift_magnitude": self.drift_magnitude,
            "interpretation": self.interpretation,
        }


def compute_delta_orientation(
    base_orientation: float,
    architectural_delta: float = 0.0,
    environmental_delta: float = 0.0,
) -> DeltaResult:
    """
    Compute ARCHY Delta orientation.

    Formula:

        O = S + Δa + Δr

    where

        S   = base axial orientation
        Δa  = architectural correction
        Δr  = environmental drift
    """

    total_orientation = base_orientation + architectural_delta + environmental_delta

    drift = abs(architectural_delta + environmental_delta)

    interpretation = classify_drift(drift)

    return DeltaResult(
        base_orientation=base_orientation,
        architectural_delta=architectural_delta,
        environmental_delta=environmental_delta,
        total_orientation=total_orientation,
        drift_magnitude=drift,
        interpretation=interpretation,
    )


def classify_drift(drift: float) -> str:
    """
    Classify orientation drift magnitude.
    """

    if drift < 0.05:
        return "stable orientation"

    if drift < 0.2:
        return "minor drift"

    if drift < 0.5:
        return "significant drift"

    return "critical misalignment"


def normalize_angle(angle: float) -> float:
    """
    Normalize orientation angle to 0–360 degrees.
    """

    return angle % 360


def example_stonehenge_case() -> DeltaResult:
    """
    Example case inspired by ancient orientation systems.
    """

    base_orientation = 90.0  # east alignment

    architectural_delta = -1.5  # architectural correction

    environmental_delta = 0.7  # environmental drift

    result = compute_delta_orientation(
        base_orientation=base_orientation,
        architectural_delta=architectural_delta,
        environmental_delta=environmental_delta,
    )

    result.total_orientation = normalize_angle(result.total_orientation)

    return result


def pretty_print(result: DeltaResult) -> str:

    lines = []
    lines.append("ARCHY Δ Orientation Result")
    lines.append("-" * 32)

    lines.append(f"base_orientation     : {result.base_orientation:.2f}")
    lines.append(f"architectural_delta  : {result.architectural_delta:.2f}")
    lines.append(f"environmental_delta  : {result.environmental_delta:.2f}")

    lines.append("-" * 32)

    lines.append(f"total_orientation    : {result.total_orientation:.2f}")
    lines.append(f"drift_magnitude      : {result.drift_magnitude:.3f}")

    lines.append(f"classification       : {result.interpretation}")

    return "\n".join(lines)


if __name__ == "__main__":

    result = example_stonehenge_case()

    print(pretty_print(result))
