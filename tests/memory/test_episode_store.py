"""Tests for transparent, outcome-linked episodic memory."""

from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timedelta, timezone
import json

import numpy as np
import pytest

from nexah.backends import V07BackendAdapter
from nexah.orientation import (
    Context,
    Episode,
    EpisodeStoreError,
    JsonlEpisodeStore,
    Outcome,
    Provenance,
    attach_similar_episodes,
    generate_orientation_report,
    orientation_similarity,
)


NOW = datetime(2026, 7, 13, 10, 0, tzinfo=timezone.utc)


def make_state(signal: np.ndarray, *, analysis_id: str, clusters: int = 3):
    provenance = Provenance(
        source=f"{analysis_id}.csv",
        method="memory test fixture",
        recorded_at=NOW,
        record_id=analysis_id,
    )
    return V07BackendAdapter(
        n_clusters=clusters,
        window=8,
        random_state=7,
    ).adapt(
        signal,
        analysis_id=analysis_id,
        provenance=provenance,
        context=Context(domain="synthetic-memory-test"),
    ).state


def make_episode(
    signal: np.ndarray,
    *,
    episode_id: str,
    clusters: int = 3,
    outcome_description: str = "The observed trajectory remained bounded.",
) -> Episode:
    state = make_state(signal, analysis_id=f"analysis-{episode_id}", clusters=clusters)
    # Recreate the BackendResult only for report generation so the episode keeps
    # the exact state used by the report.
    adapted = V07BackendAdapter(
        n_clusters=clusters,
        window=8,
        random_state=7,
    ).adapt(
        signal,
        analysis_id=f"analysis-{episode_id}",
        provenance=state.provenance,
        context=state.context,
    )
    state = adapted.state
    report = generate_orientation_report(adapted)
    outcome_time = NOW + timedelta(minutes=1)
    outcome = Outcome(
        outcome_id=f"outcome-{episode_id}",
        description=outcome_description,
        observed_at=outcome_time,
        provenance=Provenance(
            source="memory test observation",
            method="fixture outcome",
            recorded_at=outcome_time,
            record_id=f"outcome-record-{episode_id}",
        ),
        uncertainty=state.uncertainty,
    )
    return Episode(
        episode_id=episode_id,
        state=state,
        report=report,
        outcome=outcome,
        created_at=outcome_time,
        provenance=outcome.provenance,
        tags=("fixture",),
    )


def sine_signal() -> np.ndarray:
    return np.sin(np.linspace(0.0, 8.0 * np.pi, 160))


def test_episode_round_trips_with_provenance_and_outcome() -> None:
    original = make_episode(sine_signal(), episode_id="episode-001")

    restored = Episode.from_dict(json.loads(json.dumps(original.to_dict())))

    assert restored == original
    assert restored.outcome.provenance.record_id == "outcome-record-episode-001"


def test_jsonl_store_survives_reopen(tmp_path) -> None:
    path = tmp_path / "episodes.jsonl"
    episode = make_episode(sine_signal(), episode_id="episode-001")

    JsonlEpisodeStore(path).put(episode)
    reopened = JsonlEpisodeStore(path)

    assert reopened.get("episode-001") == episode
    assert reopened.all() == (episode,)
    assert len(reopened.history()) == 1


def test_duplicate_active_episode_fails_visibly(tmp_path) -> None:
    store = JsonlEpisodeStore(tmp_path / "episodes.jsonl")
    episode = make_episode(sine_signal(), episode_id="episode-001")
    store.put(episode)

    with pytest.raises(EpisodeStoreError, match="already exists"):
        store.put(episode)


def test_delete_and_restore_preserve_append_only_history(tmp_path) -> None:
    store = JsonlEpisodeStore(tmp_path / "episodes.jsonl")
    episode = make_episode(sine_signal(), episode_id="episode-001")
    store.put(episode)

    store.delete(
        episode.episode_id,
        recorded_at=NOW + timedelta(minutes=2),
        reason="test reversible deletion",
    )
    assert store.get(episode.episode_id) is None
    assert [record["operation"] for record in store.history()] == ["put", "delete"]

    store.restore(
        episode,
        recorded_at=NOW + timedelta(minutes=3),
        reason="undo test deletion",
    )
    assert store.get(episode.episode_id) == episode
    assert [record["operation"] for record in store.history()] == [
        "put",
        "delete",
        "restore",
    ]


def test_similarity_retrieval_ranks_identical_signature_first(tmp_path) -> None:
    store = JsonlEpisodeStore(tmp_path / "episodes.jsonl")
    matching = make_episode(sine_signal(), episode_id="matching", clusters=3)
    different = make_episode(
        np.sign(np.sin(np.linspace(0.0, 24.0 * np.pi, 160))),
        episode_id="different",
        clusters=5,
    )
    store.put(different)
    store.put(matching)
    query = make_state(sine_signal(), analysis_id="query", clusters=3)

    references = store.retrieve_similar(query, limit=2)

    assert [reference.episode_id for reference in references] == [
        "matching",
        "different",
    ]
    assert references[0].similarity is not None
    assert references[0].similarity.value == pytest.approx(1.0)
    assert references[0].similarity.method == (
        "v07-signature-permutation-invariant-v1"
    )
    assert references[1].similarity is not None
    assert references[1].similarity.value < references[0].similarity.value


def test_retrieved_context_is_attached_without_mutating_state(tmp_path) -> None:
    store = JsonlEpisodeStore(tmp_path / "episodes.jsonl")
    store.put(make_episode(sine_signal(), episode_id="remembered"))
    state = make_state(sine_signal(), analysis_id="query")
    references = store.retrieve_similar(state)

    enriched = attach_similar_episodes(state, references)

    assert state.episodes == ()
    assert enriched is not state
    assert enriched.episodes == references
    assert enriched.representation == state.representation
    assert enriched.observations == state.observations


def test_incompatible_backends_have_zero_similarity() -> None:
    subject = make_state(sine_signal(), analysis_id="subject")
    reference = replace(
        subject,
        representation=replace(subject.representation, backend="other-backend"),
        map=None,
    )

    similarity = orientation_similarity(subject, reference, "episode-other")

    assert similarity.value == 0.0
    assert similarity.method == "incompatible-backend-v1"


def test_corrupt_log_fails_visibly(tmp_path) -> None:
    path = tmp_path / "episodes.jsonl"
    path.write_text("not-json\n", encoding="utf-8")

    with pytest.raises(EpisodeStoreError, match="line 1"):
        JsonlEpisodeStore(path).all()


def test_outcome_cannot_precede_orientation() -> None:
    episode = make_episode(sine_signal(), episode_id="episode-001")
    invalid_outcome = replace(
        episode.outcome,
        observed_at=episode.state.timestamp - timedelta(seconds=1),
    )

    with pytest.raises(ValueError, match="cannot precede"):
        replace(episode, outcome=invalid_outcome)


def test_episode_cannot_be_created_before_outcome() -> None:
    episode = make_episode(sine_signal(), episode_id="episode-001")

    with pytest.raises(ValueError, match="created before"):
        replace(
            episode,
            created_at=episode.outcome.observed_at - timedelta(seconds=1),
        )


def test_memory_context_flows_into_the_next_orientation_report(tmp_path) -> None:
    store = JsonlEpisodeStore(tmp_path / "episodes.jsonl")
    stored = make_episode(
        sine_signal(),
        episode_id="prior-bounded-run",
        outcome_description="The earlier trajectory remained bounded.",
    )
    store.put(stored)

    signal = sine_signal()
    adapted = V07BackendAdapter(n_clusters=3, window=8, random_state=7).adapt(
        signal,
        analysis_id="new-run",
        provenance=Provenance(
            source="new-run.csv",
            method="memory loop fixture",
            recorded_at=NOW + timedelta(hours=1),
            record_id="new-run",
        ),
        context=Context(domain="synthetic-memory-test"),
    )
    references = store.retrieve_similar(adapted.state, limit=1)
    enriched_state = attach_similar_episodes(adapted.state, references)
    enriched_result = replace(adapted, state=enriched_state)

    report = generate_orientation_report(enriched_result)

    assert report.similar_episodes == references
    assert report.similar_episodes[0].episode_id == "prior-bounded-run"
    assert report.similar_episodes[0].summary == (
        "The earlier trajectory remained bounded."
    )
