"""Transparent episodic memory for outcome-linked orientation history."""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime
import json
from pathlib import Path
from typing import Any, Protocol

from .base import ContractModel, require_aware_datetime, require_text
from .evidence import Provenance
from .primitives import EpisodeRef, Outcome, Similarity
from .report import OrientationReport
from .state import OrientationState


class EpisodeStoreError(ValueError):
    """Raised when an episode log is invalid or an operation is not permitted."""


@dataclass(frozen=True, slots=True, kw_only=True)
class Episode(ContractModel):
    """One immutable orientation → report → observed outcome record."""

    episode_id: str
    state: OrientationState
    report: OrientationReport
    outcome: Outcome
    created_at: datetime
    provenance: Provenance
    tags: tuple[str, ...] = ()
    schema_version: str = "1.0"

    def __post_init__(self) -> None:
        require_text(self.episode_id, "episode_id")
        require_text(self.schema_version, "schema_version")
        require_aware_datetime(self.created_at, "created_at")
        if self.outcome.observed_at < self.state.timestamp:
            raise ValueError("outcome cannot precede the orientation state")
        if self.created_at < self.outcome.observed_at:
            raise ValueError("episode cannot be created before its observed outcome")
        if self.report.timestamp < self.state.timestamp:
            raise ValueError("report cannot precede the orientation state")
        if self.report.position is not None:
            expected_scope = self.state.representation.representation_id
            if self.report.position.identifier.scope != expected_scope:
                raise ValueError("report position scope must match episode state")
        known_evidence = {item.evidence_id for item in self.state.evidence}
        unknown = set(self.report.evidence_references) - known_evidence
        if unknown:
            names = ", ".join(sorted(unknown))
            raise ValueError(f"report references evidence absent from state: {names}")


class EpisodeStore(Protocol):
    """Minimal store interface used by the Orientation Layer."""

    def put(self, episode: Episode) -> None:
        ...

    def get(self, episode_id: str) -> Episode | None:
        ...

    def all(self) -> tuple[Episode, ...]:
        ...

    def retrieve_similar(
        self,
        state: OrientationState,
        *,
        limit: int = 5,
        minimum_similarity: float = 0.0,
    ) -> tuple[EpisodeRef, ...]:
        ...


class JsonlEpisodeStore:
    """Single-writer append-only JSONL store with inspectable tombstones."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def put(self, episode: Episode) -> None:
        if self.get(episode.episode_id) is not None:
            raise EpisodeStoreError(f"episode already exists: {episode.episode_id}")
        self._append(
            {
                "operation": "put",
                "recorded_at": episode.created_at.isoformat(),
                "episode": episode.to_dict(),
            }
        )

    def get(self, episode_id: str) -> Episode | None:
        require_text(episode_id, "episode_id")
        return self._active().get(episode_id)

    def all(self) -> tuple[Episode, ...]:
        active = self._active()
        return tuple(active[key] for key in sorted(active))

    def delete(self, episode_id: str, *, recorded_at: datetime, reason: str) -> None:
        require_text(episode_id, "episode_id")
        require_text(reason, "reason")
        require_aware_datetime(recorded_at, "recorded_at")
        if self.get(episode_id) is None:
            raise EpisodeStoreError(f"active episode not found: {episode_id}")
        self._append(
            {
                "operation": "delete",
                "recorded_at": recorded_at.isoformat(),
                "episode_id": episode_id,
                "reason": reason,
            }
        )

    def restore(
        self,
        episode: Episode,
        *,
        recorded_at: datetime,
        reason: str,
    ) -> None:
        """Restore a deleted episode by appending its full immutable record."""

        require_aware_datetime(recorded_at, "recorded_at")
        require_text(reason, "reason")
        if self.get(episode.episode_id) is not None:
            raise EpisodeStoreError(f"episode is already active: {episode.episode_id}")
        self._append(
            {
                "operation": "restore",
                "recorded_at": recorded_at.isoformat(),
                "reason": reason,
                "episode": episode.to_dict(),
            }
        )

    def history(self) -> tuple[dict[str, Any], ...]:
        return tuple(self._records())

    def retrieve_similar(
        self,
        state: OrientationState,
        *,
        limit: int = 5,
        minimum_similarity: float = 0.0,
    ) -> tuple[EpisodeRef, ...]:
        if limit < 1:
            raise EpisodeStoreError("limit must be at least 1")
        if not 0.0 <= minimum_similarity <= 1.0:
            raise EpisodeStoreError("minimum_similarity must be in [0, 1]")

        scored: list[tuple[float, str, EpisodeRef]] = []
        for episode in self.all():
            similarity = orientation_similarity(state, episode.state, episode.episode_id)
            if similarity.value < minimum_similarity:
                continue
            reference = EpisodeRef(
                episode_id=episode.episode_id,
                summary=episode.outcome.description,
                similarity=similarity,
            )
            scored.append((-similarity.value, episode.episode_id, reference))
        scored.sort(key=lambda item: (item[0], item[1]))
        return tuple(item[2] for item in scored[:limit])

    def _append(self, record: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as handle:
            json.dump(record, handle, separators=(",", ":"))
            handle.write("\n")

    def _records(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        records: list[dict[str, Any]] = []
        with self.path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                if not line.strip():
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError as error:
                    raise EpisodeStoreError(
                        f"invalid JSONL record at line {line_number}: {error.msg}"
                    ) from error
                if not isinstance(record, dict):
                    raise EpisodeStoreError(
                        f"episode record at line {line_number} must be an object"
                    )
                records.append(record)
        return records

    def _active(self) -> dict[str, Episode]:
        active: dict[str, Episode] = {}
        for line_number, record in enumerate(self._records(), start=1):
            operation = record.get("operation")
            if operation in ("put", "restore"):
                try:
                    episode = Episode.from_dict(record["episode"])
                except (KeyError, TypeError, ValueError) as error:
                    raise EpisodeStoreError(
                        f"invalid put record at line {line_number}: {error}"
                    ) from error
                if episode.episode_id in active:
                    raise EpisodeStoreError(
                        f"duplicate active episode at line {line_number}: "
                        f"{episode.episode_id}"
                    )
                active[episode.episode_id] = episode
            elif operation == "delete":
                episode_id = record.get("episode_id")
                if not isinstance(episode_id, str):
                    raise EpisodeStoreError(
                        f"invalid delete record at line {line_number}"
                    )
                if episode_id not in active:
                    raise EpisodeStoreError(
                        f"delete references inactive episode at line {line_number}: "
                        f"{episode_id}"
                    )
                active.pop(episode_id)
            else:
                raise EpisodeStoreError(
                    f"unknown episode operation at line {line_number}: {operation}"
                )
        return active


def orientation_similarity(
    subject: OrientationState,
    reference: OrientationState,
    reference_episode_id: str,
) -> Similarity:
    """Permutation-invariant heuristic similarity for v0.7 signatures."""

    subject_id = subject.representation.representation_id
    if subject.representation.backend != reference.representation.backend:
        return Similarity(
            subject_id=subject_id,
            reference_id=reference_episode_id,
            value=0.0,
            method="incompatible-backend-v1",
        )

    subject_signature = _signature(subject)
    reference_signature = _signature(reference)
    if subject_signature is None or reference_signature is None:
        score = 0.7 if subject.context.domain == reference.context.domain else 0.3
        return Similarity(
            subject_id=subject_id,
            reference_id=reference_episode_id,
            value=score,
            method="backend-context-fallback-v1",
        )

    domain_score = 1.0 if subject.context.domain == reference.context.domain else 0.0
    state_score = 1.0 / (
        1.0
        + abs(
            float(subject_signature.get("n_states_observed", 0))
            - float(reference_signature.get("n_states_observed", 0))
        )
    )
    occupancy_score = _distribution_similarity(
        subject_signature.get("occupancy", {}),
        reference_signature.get("occupancy", {}),
    )
    persistence_score = _distribution_similarity(
        subject_signature.get("escape_difficulty", {}),
        reference_signature.get("escape_difficulty", {}),
    )
    entropy_score = _distribution_similarity(
        subject_signature.get("transition_entropy", {}),
        reference_signature.get("transition_entropy", {}),
    )
    score = (
        0.10 * domain_score
        + 0.10 * state_score
        + 0.30 * occupancy_score
        + 0.25 * persistence_score
        + 0.25 * entropy_score
    )
    return Similarity(
        subject_id=subject_id,
        reference_id=reference_episode_id,
        value=max(0.0, min(1.0, score)),
        method="v07-signature-permutation-invariant-v1",
    )


def attach_similar_episodes(
    state: OrientationState,
    references: tuple[EpisodeRef, ...],
) -> OrientationState:
    """Return a new state with retrieved context; never mutate the input state."""

    identifiers = [reference.episode_id for reference in references]
    if len(identifiers) != len(set(identifiers)):
        raise ValueError("retrieved episode IDs must be unique")
    return replace(state, episodes=references)


def _signature(state: OrientationState) -> dict[str, Any] | None:
    for evidence in state.evidence:
        signature = evidence.payload.get("signature")
        if isinstance(signature, dict):
            return signature
    return None


def _distribution_similarity(left: Any, right: Any) -> float:
    if not isinstance(left, dict) or not isinstance(right, dict):
        return 0.0
    left_values = sorted(float(value) for value in left.values())
    right_values = sorted(float(value) for value in right.values())
    width = max(len(left_values), len(right_values))
    if width == 0:
        return 1.0
    left_values.extend([0.0] * (width - len(left_values)))
    right_values.extend([0.0] * (width - len(right_values)))
    mean_distance = sum(
        abs(left_value - right_value)
        for left_value, right_value in zip(left_values, right_values)
    ) / width
    return 1.0 / (1.0 + mean_distance)
