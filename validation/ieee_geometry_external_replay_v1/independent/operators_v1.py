"""Independent manifest-derived IEEE Geometry V1 operator implementation.

This module intentionally uses only the Python standard library.  It does not
import the NEXAH package or any production geometry/operator implementation.
"""

from __future__ import annotations

import math
from typing import Any


FAILED_FRAME_REASON = "failed frame contains no fabricated physical feature vector"
PARAMETER_SEMANTICS = "ordered_load_scale_not_time"


def _is_finite_number(value: Any) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(float(value))
    )


def _euclidean(values: list[float]) -> float:
    return math.sqrt(sum(value * value for value in values))


def _projection_definition(manifest: dict[str, Any]) -> dict[str, Any]:
    matches = [
        item
        for item in manifest["projections"]
        if item["projection_id"] == "system-summary-standardized-v1"
    ]
    if len(matches) != 1:
        raise ValueError("manifest must define exactly one system summary projection")
    return matches[0]


def fit_ieee9_standardization(
    manifest: dict[str, Any], development_frames: dict[str, Any]
) -> dict[str, Any]:
    """Fit the manifest-declared population model on converged IEEE-9 rows."""

    if development_frames["case_id"] != "ieee9":
        raise ValueError("standardization fit is restricted to IEEE-9")
    if development_frames["case_role"] != "method_development":
        raise ValueError("IEEE-9 case role must remain method_development")

    projection = _projection_definition(manifest)
    feature_names = list(projection["inputs"])
    rows: list[list[float]] = []
    for frame in development_frames["frames"]:
        if frame["status"] != "converged":
            continue
        features = frame.get("system_features")
        if not isinstance(features, dict):
            raise ValueError("converged frame lacks system_features")
        names = features.get("feature_names")
        values = features.get("values")
        if names != feature_names:
            raise ValueError("system feature names do not match manifest projection")
        if not isinstance(values, list) or len(values) != len(feature_names):
            raise ValueError("system feature vector has invalid length")
        if not all(_is_finite_number(value) for value in values):
            raise ValueError("system feature vector contains non-finite value")
        rows.append([float(value) for value in values])

    if not rows:
        raise ValueError("IEEE-9 has no converged rows for standardization")

    count = len(rows)
    means = [
        sum(row[column] for row in rows) / count
        for column in range(len(feature_names))
    ]
    population_stddevs = [
        math.sqrt(
            sum((row[column] - means[column]) ** 2 for row in rows) / count
        )
        for column in range(len(feature_names))
    ]
    zero_variance_features = [
        name
        for name, stddev in zip(feature_names, population_stddevs)
        if stddev == 0.0
    ]
    status = "insufficient" if zero_variance_features else "available"
    reason = (
        "zero-variance projection feature"
        if zero_variance_features
        else None
    )
    return {
        "manifest_id": manifest["manifest_id"],
        "projection_id": projection["projection_id"],
        "fit_campaign_id": development_frames["campaign_id"],
        "fit_case_id": development_frames["case_id"],
        "feature_names": feature_names,
        "means": means,
        "population_stddevs": population_stddevs,
        "status": status,
        "zero_variance_features": zero_variance_features,
        "reason": reason,
    }


def _project_frames(
    frames_document: dict[str, Any], model: dict[str, Any]
) -> list[dict[str, Any]]:
    projected: list[dict[str, Any]] = []
    expected_index = 0
    previous_scale: float | None = None

    for frame in frames_document["frames"]:
        index = frame["campaign_index"]
        scale = frame["load_scale"]
        if index != expected_index:
            raise ValueError("campaign indices must be contiguous and ordered")
        if not _is_finite_number(scale):
            raise ValueError("load scale must be finite")
        if previous_scale is not None and float(scale) <= previous_scale:
            raise ValueError("load scales must be strictly increasing")
        expected_index += 1
        previous_scale = float(scale)

        record = {
            "frame_id": frame["frame_id"],
            "campaign_index": index,
            "load_scale": scale,
            "status": "insufficient",
            "values": None,
            "reason": FAILED_FRAME_REASON,
        }
        if frame["status"] == "converged":
            features = frame.get("system_features")
            if not isinstance(features, dict):
                raise ValueError("converged frame lacks system_features")
            if features.get("feature_names") != model["feature_names"]:
                raise ValueError("frame feature order differs from fitted model")
            values = features.get("values")
            if not isinstance(values, list) or len(values) != len(model["means"]):
                raise ValueError("invalid system feature vector")
            if not all(_is_finite_number(value) for value in values):
                raise ValueError("non-finite system feature value")
            if model["status"] != "available":
                record["reason"] = model["reason"]
            else:
                record.update(
                    {
                        "status": "available",
                        "values": [
                            (float(value) - mean) / stddev
                            for value, mean, stddev in zip(
                                values,
                                model["means"],
                                model["population_stddevs"],
                            )
                        ],
                        "reason": None,
                    }
                )
        elif frame["status"] != "failed":
            raise ValueError(f"unsupported frame status: {frame['status']!r}")
        projected.append(record)
    return projected


def _build_steps(
    projected_frames: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], float, str | None]:
    steps: list[dict[str, Any]] = []
    cumulative = 0.0
    terminal_frame_id: str | None = None

    for source, target in zip(projected_frames, projected_frames[1:]):
        delta_scale = target["load_scale"] - source["load_scale"]
        record = {
            "source_frame_id": source["frame_id"],
            "target_frame_id": target["frame_id"],
            "source_index": source["campaign_index"],
            "target_index": target["campaign_index"],
            "source_load_scale": source["load_scale"],
            "target_load_scale": target["load_scale"],
            "delta_load_scale": delta_scale,
            "status": "insufficient",
            "delta_vector": None,
            "displacement": None,
            "normalized_local_drift": None,
            "cumulative_path_length": None,
            "reason": None,
            "parameter_semantics": PARAMETER_SEMANTICS,
        }
        if terminal_frame_id is not None:
            record["reason"] = (
                f"sampled path already terminated at {terminal_frame_id}"
            )
        elif source["status"] != "available" or target["status"] != "available":
            unavailable = (
                source if source["status"] != "available" else target
            )
            record["reason"] = unavailable["reason"]
            terminal_frame_id = unavailable["frame_id"]
        elif delta_scale <= 0.0:
            record["reason"] = "non-positive campaign-axis spacing"
            terminal_frame_id = target["frame_id"]
        else:
            delta = [
                target_value - source_value
                for source_value, target_value in zip(
                    source["values"], target["values"]
                )
            ]
            displacement = _euclidean(delta)
            cumulative += displacement
            record.update(
                {
                    "status": "available",
                    "delta_vector": delta,
                    "displacement": displacement,
                    "normalized_local_drift": displacement / delta_scale,
                    "cumulative_path_length": cumulative,
                    "reason": None,
                }
            )
        steps.append(record)
    return steps, cumulative, terminal_frame_id


def _build_turns(
    projected_frames: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    turns: list[dict[str, Any]] = []
    for previous, center, following in zip(
        projected_frames,
        projected_frames[1:],
        projected_frames[2:],
    ):
        record = {
            "previous_frame_id": previous["frame_id"],
            "center_frame_id": center["frame_id"],
            "next_frame_id": following["frame_id"],
            "center_index": center["campaign_index"],
            "status": "insufficient",
            "direction_change_radians": None,
            "discrete_curvature": None,
            "reason": None,
        }
        unavailable = next(
            (
                item
                for item in (previous, center, following)
                if item["status"] != "available"
            ),
            None,
        )
        if unavailable is not None:
            record["reason"] = unavailable["reason"]
        else:
            delta_previous = [
                center_value - previous_value
                for previous_value, center_value in zip(
                    previous["values"], center["values"]
                )
            ]
            delta_next = [
                following_value - center_value
                for center_value, following_value in zip(
                    center["values"], following["values"]
                )
            ]
            norm_previous = _euclidean(delta_previous)
            norm_next = _euclidean(delta_next)
            if norm_previous == 0.0 or norm_next == 0.0:
                record["reason"] = "zero displacement norm"
            else:
                cosine = sum(
                    left * right
                    for left, right in zip(delta_previous, delta_next)
                ) / (norm_previous * norm_next)
                direction_change = math.acos(max(-1.0, min(1.0, cosine)))
                local_arc = 0.5 * (norm_previous + norm_next)
                if local_arc == 0.0:
                    record["reason"] = "zero local arc-length denominator"
                else:
                    record.update(
                        {
                            "status": "available",
                            "direction_change_radians": direction_change,
                            "discrete_curvature": direction_change / local_arc,
                            "reason": None,
                        }
                    )
        turns.append(record)
    return turns


def _build_solver_boundaries(
    frames_document: dict[str, Any],
) -> list[dict[str, Any]]:
    boundaries: list[dict[str, Any]] = []
    last_converged: dict[str, Any] | None = None
    for frame in frames_document["frames"]:
        if frame["status"] == "converged":
            last_converged = frame
            continue
        if frame["status"] != "failed":
            raise ValueError(f"unsupported frame status: {frame['status']!r}")
        if last_converged is None:
            boundaries.append(
                {
                    "failed_frame_id": frame["frame_id"],
                    "failed_index": frame["campaign_index"],
                    "failed_load_scale": frame["load_scale"],
                    "last_converged_frame_id": None,
                    "last_converged_load_scale": None,
                    "status": "insufficient",
                    "distance_load_scale": None,
                    "solver_failure": frame.get("failure"),
                    "reason": "no prior converged frame",
                    "boundary_type": "solver_non_convergence",
                }
            )
            continue
        boundaries.append(
            {
                "failed_frame_id": frame["frame_id"],
                "failed_index": frame["campaign_index"],
                "failed_load_scale": frame["load_scale"],
                "last_converged_frame_id": last_converged["frame_id"],
                "last_converged_load_scale": last_converged["load_scale"],
                "status": "available",
                "distance_load_scale": (
                    frame["load_scale"] - last_converged["load_scale"]
                ),
                "solver_failure": frame.get("failure"),
                "reason": None,
                "boundary_type": "solver_non_convergence",
            }
        )
    return boundaries


def build_independent_geometry(
    manifest: dict[str, Any],
    frames_document: dict[str, Any],
    standardization_model: dict[str, Any],
) -> dict[str, Any]:
    """Build the six frozen operator records without production imports."""

    if frames_document["manifest_id"] != manifest["manifest_id"]:
        raise ValueError("frame manifest identity mismatch")
    projected_frames = _project_frames(frames_document, standardization_model)
    steps, total_path_length, terminal_frame_id = _build_steps(projected_frames)
    turns = _build_turns(projected_frames)
    boundaries = _build_solver_boundaries(frames_document)

    contiguous: list[str] = []
    for frame in projected_frames:
        if frame["status"] != "available":
            break
        contiguous.append(frame["frame_id"])

    operator_ids = [item["operator_id"] for item in manifest["operators"]]
    return {
        "standardization_model": dict(standardization_model),
        "analysis": {
            "manifest_id": manifest["manifest_id"],
            "campaign_id": frames_document["campaign_id"],
            "case_id": frames_document["case_id"],
            "case_role": frames_document["case_role"],
            "projection_model": dict(standardization_model),
            "projected_frames": projected_frames,
            "steps": steps,
            "turns": turns,
            "solver_boundaries": boundaries,
            "contiguous_converged_frame_ids": contiguous,
            "total_path_length": total_path_length,
            "terminal_frame_id": terminal_frame_id,
            "operator_ids": operator_ids,
        },
    }

