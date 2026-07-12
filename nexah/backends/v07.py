"""Typed adapter for the frozen NEXAH v0.7 computational baseline."""

from __future__ import annotations

from datetime import datetime
import random
from typing import Any, Mapping, Protocol, Sequence, cast

import numpy as np
from numpy.typing import ArrayLike, NDArray

from nexah.core import NEXAH
from nexah.orientation import (
    Constraint,
    Context,
    Evidence,
    EvidenceKind,
    Goal,
    MapRef,
    MapScope,
    Observation,
    OrientationState,
    Provenance,
    ReferenceFrame,
    Regime,
    RepresentationRef,
    ScopedIdentifier,
    StateRef,
    Transition,
    Uncertainty,
    UncertaintyKind,
)
from nexah.orientation.base import require_aware_datetime, require_text

from .base import BackendAdapterError, BackendResult, EmbeddingAlignment


FloatArray = NDArray[np.float64]


class _V07Engine(Protocol):
    def analyze(
        self, trajectory: FloatArray, target_state: int | None = None
    ) -> dict[str, Any]:
        ...


class V07BackendAdapter:
    """Run v0.7 and translate its local analysis into current contracts."""

    def __init__(
        self,
        *,
        n_clusters: int = 4,
        window: int = 5,
        random_state: int = 42,
        normalize: bool = True,
    ) -> None:
        if n_clusters < 1:
            raise BackendAdapterError("n_clusters must be at least 1")
        if window < 1:
            raise BackendAdapterError("window must be at least 1")
        self.n_clusters = n_clusters
        self.window = window
        self.random_state = random_state
        self.normalize = normalize

    @property
    def backend_id(self) -> str:
        return "nexah-v07"

    def adapt(
        self,
        trajectory: ArrayLike,
        *,
        analysis_id: str,
        provenance: Provenance,
        context: Context,
        timestamps: Sequence[datetime] | None = None,
        reference_frame: ReferenceFrame | None = None,
        goals: tuple[Goal, ...] = (),
        constraints: tuple[Constraint, ...] = (),
    ) -> BackendResult:
        """Analyze a trajectory and preserve the scope of every v0.7 claim."""

        require_text(analysis_id, "analysis_id")
        values = self._validate_trajectory(trajectory)
        observation_times = self._validate_timestamps(
            timestamps, values.shape[0], provenance.recorded_at
        )

        embedded_samples = values.shape[0] - self.window
        if embedded_samples < self.n_clusters:
            raise BackendAdapterError(
                "trajectory produces fewer embedded samples than n_clusters "
                f"({embedded_samples} < {self.n_clusters})"
            )

        alignment = EmbeddingAlignment(
            input_samples=int(values.shape[0]),
            embedded_samples=int(embedded_samples),
            window=self.window,
            final_source_sample_used=int(values.shape[0] - 2),
        )

        raw_result = self._run_baseline(values)
        representation_id = f"{analysis_id}:v07-local-fit"
        evidence_id = f"{analysis_id}:v07-analysis"
        uncertainty = Uncertainty(
            kind=UncertaintyKind.UNKNOWN,
            value=None,
            basis=(
                "v0.7 does not estimate calibrated uncertainty; outputs are "
                "locally fitted descriptive heuristics"
            ),
        )

        observations = tuple(
            self._observation(
                value=value,
                index=index,
                observed_at=observation_times[index],
                analysis_id=analysis_id,
                provenance=provenance,
            )
            for index, value in enumerate(values)
        )

        representation = RepresentationRef(
            backend=self.backend_id,
            method="sliding-window-kmeans-empirical-transition",
            scope=MapScope.LOCAL_FIT,
            representation_id=representation_id,
            parameters={
                **raw_result["config"],
                "embedded_samples": alignment.embedded_samples,
                "alignment_anchor": alignment.anchor,
                "final_source_sample_used": alignment.final_source_sample_used,
                "timestamps_provided": timestamps is not None,
            },
        )
        map_ref = MapRef(
            map_id=f"{analysis_id}:transition-map",
            scope=MapScope.LOCAL_FIT,
            representation_id=representation_id,
            description="Empirical transition map fitted only to this v0.7 analysis",
        )
        location = StateRef(
            identifier=ScopedIdentifier(
                value=str(raw_result["current_state"]),
                scope=representation_id,
            ),
            label="v0.7 current local cluster",
        )

        analysis_evidence = Evidence(
            evidence_id=evidence_id,
            claim=(
                "The frozen v0.7 backend produced a locally fitted state-space "
                "and empirical transition analysis for this trajectory."
            ),
            kind=EvidenceKind.COMPUTATION,
            provenance=provenance,
            uncertainty=uncertainty,
            payload={
                "config": _json_safe(raw_result["config"]),
                "signature": _json_safe(raw_result["signature"]),
                "regime_shifts_embedded": _json_safe(raw_result["regime_shifts"]),
                "regime_zones_embedded": _json_safe(raw_result["regime_zones"]),
                "limitations": [
                    "cluster identifiers are local to this fit",
                    "embedded windows overlap",
                    "regime indices refer to embedded positions",
                    "stability and navigation outputs are heuristic",
                ],
            },
        )

        state = OrientationState(
            observations=observations,
            representation=representation,
            reference_frame=reference_frame
            or ReferenceFrame(
                frame_id=f"{analysis_id}:source-sample-index",
                description=(
                    "Source sample indices; v0.7 embedded states are anchored "
                    "to the end of each represented window"
                ),
                scale="sample",
            ),
            context=context,
            uncertainty=uncertainty,
            timestamp=provenance.recorded_at,
            provenance=provenance,
            location=location,
            goals=goals,
            constraints=constraints,
            map=map_ref,
            evidence=(analysis_evidence,),
        )

        transitions = self._transitions(
            cast(dict[int, dict[int, float]], raw_result["transitions"]),
            representation_id,
            evidence_id,
        )

        # v0.7 regime zones are temporal embedded-index ranges, not collections
        # of stable state identities. They remain in evidence/raw output rather
        # than being mislabeled as Regime contracts.
        return BackendResult(
            state=state,
            transitions=transitions,
            regimes=tuple(),
            alignment=alignment,
            raw_output=raw_result,
        )

    def _validate_trajectory(self, trajectory: ArrayLike) -> FloatArray:
        try:
            values = np.asarray(trajectory, dtype=np.float64)
        except (TypeError, ValueError) as error:
            raise BackendAdapterError("trajectory must contain numeric values") from error

        if values.ndim not in (1, 2):
            raise BackendAdapterError("trajectory must be one- or two-dimensional")
        if values.shape[0] <= self.window:
            raise BackendAdapterError("trajectory length must be greater than window")
        if values.ndim == 2 and values.shape[1] == 0:
            raise BackendAdapterError("trajectory must contain at least one variable")
        if not np.all(np.isfinite(values)):
            raise BackendAdapterError("trajectory must contain only finite values")
        return values

    def _validate_timestamps(
        self,
        timestamps: Sequence[datetime] | None,
        count: int,
        fallback: datetime,
    ) -> tuple[datetime, ...]:
        if timestamps is None:
            return tuple(fallback for _ in range(count))
        if len(timestamps) != count:
            raise BackendAdapterError("timestamps length must match trajectory length")
        for index, value in enumerate(timestamps):
            try:
                require_aware_datetime(value, f"timestamps[{index}]")
            except ValueError as error:
                raise BackendAdapterError(str(error)) from error
        return tuple(timestamps)

    def _run_baseline(self, values: FloatArray) -> dict[str, Any]:
        python_random_state = random.getstate()
        numpy_random_state = np.random.get_state()
        try:
            engine = cast(
                _V07Engine,
                NEXAH(  # type: ignore[no-untyped-call]
                    n_clusters=self.n_clusters,
                    window=self.window,
                    random_state=self.random_state,
                    normalize=self.normalize,
                ),
            )
            return engine.analyze(values)
        except Exception as error:
            raise BackendAdapterError(f"v0.7 analysis failed: {error}") from error
        finally:
            random.setstate(python_random_state)
            np.random.set_state(numpy_random_state)

    def _observation(
        self,
        *,
        value: Any,
        index: int,
        observed_at: datetime,
        analysis_id: str,
        provenance: Provenance,
    ) -> Observation:
        encoded = float(value) if np.ndim(value) == 0 else np.asarray(value).tolist()
        return Observation(
            observation_id=f"{analysis_id}:sample:{index}",
            value=encoded,
            variable="trajectory",
            observed_at=observed_at,
            provenance=provenance,
        )

    def _transitions(
        self,
        transitions: dict[int, dict[int, float]],
        scope: str,
        evidence_id: str,
    ) -> tuple[Transition, ...]:
        converted = []
        for source in sorted(transitions):
            for target in sorted(transitions[source]):
                converted.append(
                    Transition(
                        source=StateRef(
                            identifier=ScopedIdentifier(value=str(source), scope=scope)
                        ),
                        target=StateRef(
                            identifier=ScopedIdentifier(value=str(target), scope=scope)
                        ),
                        probability=float(transitions[source][target]),
                        evidence_ids=(evidence_id,),
                    )
                )
        return tuple(converted)


def _json_safe(value: Any) -> Any:
    """Normalize backend values before they enter a public contract payload."""

    if isinstance(value, np.ndarray):
        return [_json_safe(item) for item in value.tolist()]
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    if isinstance(value, Mapping):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_json_safe(item) for item in value]
    return value
