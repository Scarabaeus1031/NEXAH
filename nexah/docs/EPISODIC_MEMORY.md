# Episodic Memory

Status: initial transparent implementation

The episodic layer records complete, immutable links between:

```text
OrientationState
→ OrientationReport
→ observed Outcome
→ Episode
```

It does not train or mutate the v0.7 backend. Retrieved episodes are attached to
a new `OrientationState` as explicit context, and the original state remains
unchanged.

## Episode contract

An `Episode` contains:

- stable episode ID
- original Orientation State
- generated Orientation Report
- subsequently observed Outcome
- creation timestamp and provenance
- optional tags

The Outcome cannot precede the State, report position scope must match the State,
and Report evidence references must exist in the stored State.

## Storage model

`JsonlEpisodeStore` is a deliberately simple single-writer, append-only store.
Every line is one operation:

```json
{"operation":"put","recorded_at":"...","episode":{}}
{"operation":"delete","recorded_at":"...","episode_id":"...","reason":"..."}
{"operation":"restore","recorded_at":"...","reason":"...","episode":{}}
```

Deletion appends a tombstone; it does not erase history. Restoration appends the
full immutable Episode again. `history()` exposes every operation for audit.

This first implementation favors transparency over storage efficiency. Full
Orientation States can be large; deduplicated object storage or SQLite is later
engineering work and must preserve the same audit semantics.

## Similarity semantics

For two v0.7 states, `v07-signature-permutation-invariant-v1` compares:

| Component | Weight |
|---|---:|
| Context domain match | 0.10 |
| Number of observed states | 0.10 |
| Sorted occupancy distribution | 0.30 |
| Sorted self-transition distribution | 0.25 |
| Sorted transition-entropy distribution | 0.25 |

Distribution values are sorted before comparison, so local KMeans label numbers
are never treated as persistent identities. Each distribution score is
`1 / (1 + mean absolute distance)`. The resulting score is a retrieval heuristic,
not a probability, calibrated confidence, causal similarity, or proof that two
systems occupy the same regime.

Different backends receive similarity `0`. If compatible backend signatures are
absent, a documented backend/context fallback is used.

## Minimal flow

```python
store = JsonlEpisodeStore("episodes.jsonl")
store.put(episode)

references = store.retrieve_similar(new_state, limit=3)
enriched_state = attach_similar_episodes(new_state, references)
```

Generating a report from `enriched_state` carries those references into
`OrientationReport.similar_episodes`.

## Boundaries

- Outcomes must be supplied by an observer or external workflow.
- Similarity does not determine which action should be selected.
- Retrieval does not alter backend parameters or learned maps.
- JSONL is not currently a concurrent multi-writer database.
- No forgetting, consolidation, or automatic policy learning is implemented.

## Validation

The first multi-system benchmark is documented under
**[validation/memory_generalization/](../../validation/memory_generalization/)**.
Across Lorenz, Rössler, and Kuramoto it retrieves the expected family for 11 of
12 clean, noisy, and parameter-shifted queries. The parameter-shifted Kuramoto
case is misclassified as Lorenz and remains an explicit failure case.

The versioned follow-up is documented under
**[validation/memory_generalization_v2/](../../validation/memory_generalization_v2/)**.
It stores five references per family and uses separate validation and held-out
test queries. Its selected method retrieves all six held-out families, but the
minimum margin is only 0.003172. V2 therefore closes the synthetic multi-episode
fixture, not the questions of semantic Outcome relevance or real-world memory.
