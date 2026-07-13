"""D–E pipeline: orient an IEEE load campaign and attribute its changes."""

from __future__ import annotations

from dataclasses import dataclass, replace

from nexah.backends import BackendResult, V07BackendAdapter
from nexah.orientation import (
    Context,
    OrientationReport,
    Provenance,
    ReferenceFrame,
    generate_orientation_report,
)
from nexah.orientation.base import require_text
from nexah.sources import IEEECoupledCampaign, IEEEPhysicalSnapshot, SourceBatch


@dataclass(frozen=True, slots=True, kw_only=True)
class EntityDelta:
    """Observed change for one physical entity and one declared feature."""

    entity_id: str
    feature: str
    unit: str | None
    previous: float
    current: float
    delta: float


@dataclass(frozen=True, slots=True, kw_only=True)
class IEEEAttributionEvent:
    """Spatial co-change aligned to one v0.7 representation event."""

    embedded_index: int
    campaign_index: int
    previous_scenario_id: str
    scenario_id: str
    previous_load_scale: float
    load_scale: float
    bus_deltas: tuple[EntityDelta, ...]
    line_deltas: tuple[EntityDelta, ...]
    interpretation: str = (
        "Ranked physical co-changes at an aligned representation event; "
        "co-occurrence does not establish causal contribution."
    )


@dataclass(frozen=True, slots=True, kw_only=True)
class IEEEOrientationRun:
    """Coupled source, scoped v0.7 result, report, and entity attribution."""

    campaign: IEEECoupledCampaign
    backend_result: BackendResult
    report: OrientationReport
    attributions: tuple[IEEEAttributionEvent, ...]


def orient_ieee_campaign(
    campaign: IEEECoupledCampaign,
    *,
    analysis_id: str,
    n_clusters: int = 4,
    window: int = 5,
    random_state: int = 42,
    top_entities_per_feature: int = 3,
) -> IEEEOrientationRun:
    """Run v0.7 on the ordered load view and align events to entity snapshots."""

    require_text(analysis_id, "analysis_id")
    if top_entities_per_feature < 1:
        raise ValueError("top_entities_per_feature must be at least 1")
    batch = campaign.campaign_batch
    context = Context(
        domain=batch.context.domain,
        values={
            **batch.context.values,
            "source_batch_id": batch.batch_id,
            "source_row_axis": batch.row_axis.value,
            "ordered_parameter": "load_scale",
            "independent_steady_state_solutions": True,
            "case_id": campaign.case_id,
        },
    )
    result = V07BackendAdapter(
        n_clusters=n_clusters,
        window=window,
        random_state=random_state,
    ).adapt(
        batch.to_numpy(),
        analysis_id=analysis_id,
        provenance=batch.provenance,
        context=context,
        reference_frame=ReferenceFrame(
            frame_id=f"{analysis_id}:load-scale-order",
            description=(
                "Independent pandapower steady-state solutions ordered by "
                "increasing load scale; this frame is not physical time"
            ),
            scale="load-scale order",
        ),
    )
    generic = generate_orientation_report(result)
    report = _scope_report(generic, campaign=campaign, analysis_id=analysis_id)
    attributions = attribute_ieee_changes(
        campaign,
        result,
        top_entities_per_feature=top_entities_per_feature,
    )
    return IEEEOrientationRun(
        campaign=campaign,
        backend_result=result,
        report=report,
        attributions=attributions,
    )


def attribute_ieee_changes(
    campaign: IEEECoupledCampaign,
    result: BackendResult,
    *,
    top_entities_per_feature: int = 3,
) -> tuple[IEEEAttributionEvent, ...]:
    """Align v0.7 label changes with ranked bus and line co-changes."""

    if top_entities_per_feature < 1:
        raise ValueError("top_entities_per_feature must be at least 1")
    snapshot_by_id = {snapshot.scenario_id: snapshot for snapshot in campaign.snapshots}
    ordered = tuple(snapshot_by_id[row_id] for row_id in campaign.campaign_batch.row_ids)
    events = []
    for raw_index in result.raw_output.get("regime_shifts", []):
        embedded_index = int(raw_index)
        campaign_index = result.alignment.raw_anchor(embedded_index)
        if not 0 < campaign_index < len(ordered):
            continue
        previous = ordered[campaign_index - 1]
        current = ordered[campaign_index]
        events.append(
            IEEEAttributionEvent(
                embedded_index=embedded_index,
                campaign_index=campaign_index,
                previous_scenario_id=previous.scenario_id,
                scenario_id=current.scenario_id,
                previous_load_scale=previous.load_scale,
                load_scale=current.load_scale,
                bus_deltas=_rank_entity_deltas(
                    previous.bus_batch,
                    current.bus_batch,
                    limit=top_entities_per_feature,
                ),
                line_deltas=_rank_entity_deltas(
                    previous.line_batch,
                    current.line_batch,
                    limit=top_entities_per_feature,
                ),
            )
        )
    return tuple(events)


def _rank_entity_deltas(
    previous: SourceBatch | None,
    current: SourceBatch | None,
    *,
    limit: int,
) -> tuple[EntityDelta, ...]:
    if previous is None or current is None:
        raise ValueError("entity attribution requires converged physical batches")
    if previous.row_ids != current.row_ids:
        raise ValueError("entity IDs differ between aligned snapshots")
    if previous.features != current.features:
        raise ValueError("entity features differ between aligned snapshots")
    left = previous.to_numpy()
    right = current.to_numpy()
    ranked: list[EntityDelta] = []
    for column, feature in enumerate(current.features):
        candidates = [
            EntityDelta(
                entity_id=entity_id,
                feature=feature.name,
                unit=feature.unit,
                previous=float(left[row, column]),
                current=float(right[row, column]),
                delta=float(right[row, column] - left[row, column]),
            )
            for row, entity_id in enumerate(current.row_ids)
        ]
        candidates.sort(key=lambda item: (-abs(item.delta), item.entity_id))
        ranked.extend(candidates[:limit])
    return tuple(ranked)


def _scope_report(
    report: OrientationReport,
    *,
    campaign: IEEECoupledCampaign,
    analysis_id: str,
) -> OrientationReport:
    generic_order_assumption = (
        "Observation order is represented by source sample index because "
        "acquisition timestamps were not supplied."
    )
    assumptions = tuple(
        assumption
        for assumption in report.assumptions
        if assumption != generic_order_assumption
    ) + (
        "Rows are independent pandapower steady-state solutions ordered by "
        "increasing load scale; they are not timestamps or dynamic evolution.",
        "Entity attribution reports aligned co-change and does not establish causality.",
    )
    missing = tuple(
        item
        for item in report.missing_information
        if item != "Source observation timestamps"
    ) + ("Dynamic trajectories between independently solved load cases",)
    provenance = Provenance(
        source=report.provenance.source,
        method="ieee-load-campaign-orientation-v1",
        recorded_at=report.timestamp,
        record_id=f"{analysis_id}:ieee-orientation-report",
        metadata={
            **report.provenance.metadata,
            "case_id": campaign.case_id,
            "campaign_id": campaign.campaign_id,
            "ordered_parameter": "load_scale",
            "base_generator": report.provenance.method,
        },
    )
    return replace(
        report,
        assumptions=assumptions,
        missing_information=missing,
        explanation=(
            report.explanation
            + " The represented sequence is an ordered load-scale campaign of "
            "independent steady-state solutions, not a time trajectory."
        ),
        provenance=provenance,
    )
