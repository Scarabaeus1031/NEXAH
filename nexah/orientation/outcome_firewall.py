"""Typed evidence records and an explicit gate for episodic-memory updates."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Mapping, TypeAlias

from .base import ContractModel, require_aware_datetime, require_text
from .evidence import Provenance, Uncertainty
from .memory import Episode, EpisodeStore, EpisodeStoreError


class EvidenceRecordType(str, Enum):
    SCENARIO = "scenario"
    COMPUTATION_RESULT = "computation_result"
    OBSERVED_OUTCOME = "observed_outcome"


class ComputationStatus(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    INDETERMINATE = "indeterminate"


class OutcomeSourceRelation(str, Enum):
    INDEPENDENT = "independent"
    TESTED_METHOD_OUTPUT = "tested_method_output"
    UNKNOWN = "unknown"


class MethodSelectionRelation(str, Enum):
    NOT_USED = "not_used"
    USED = "used"
    UNKNOWN = "unknown"


class FirewallCheckStatus(str, Enum):
    PASS = "pass"
    FAIL = "fail"
    UNKNOWN = "unknown"
    NOT_APPLICABLE = "not_applicable"


class FirewallDisposition(str, Enum):
    ACCEPTED_BENCHMARK_RECORD = "accepted_benchmark_record"
    ACCEPTED_OBSERVATION_ONLY = "accepted_observation_only"
    ACCEPTED_OUTCOME_LINKED_CASE = "accepted_outcome_linked_case"
    REJECTED = "rejected"
    INDETERMINATE = "indeterminate"


OUTCOME_FIREWALL_CHECK_IDS = (
    "record-type",
    "temporal-order",
    "source-independence",
    "scope-compatibility",
    "evidence-cutoff",
    "method-selection-leakage",
)


@dataclass(frozen=True, slots=True, kw_only=True)
class OrientationEvidenceEnvelope(ContractModel):
    """Evidence state that was available when an orientation was produced."""

    orientation_id: str
    scope: str
    orientation_timestamp: datetime
    report_evidence_ids: tuple[str, ...]
    available_evidence_ids: tuple[str, ...]
    provenance: Provenance
    schema_version: str = "1.0"

    def __post_init__(self) -> None:
        require_text(self.orientation_id, "orientation_id")
        require_text(self.scope, "scope")
        require_text(self.schema_version, "schema_version")
        require_aware_datetime(self.orientation_timestamp, "orientation_timestamp")
        _require_unique(self.report_evidence_ids, "report evidence IDs")
        _require_unique(self.available_evidence_ids, "available evidence IDs")


@dataclass(frozen=True, slots=True, kw_only=True)
class ScenarioRecord(ContractModel):
    """An authored change for inquiry; explicitly not an observation."""

    record_id: str
    scope: str
    declared_at: datetime
    baseline_reference: str
    change: str
    reason: str
    provenance: Provenance
    record_type: EvidenceRecordType = EvidenceRecordType.SCENARIO
    schema_version: str = "1.0"

    def __post_init__(self) -> None:
        for value, name in (
            (self.record_id, "record_id"),
            (self.scope, "scope"),
            (self.baseline_reference, "baseline_reference"),
            (self.change, "change"),
            (self.reason, "reason"),
            (self.schema_version, "schema_version"),
        ):
            require_text(value, name)
        require_aware_datetime(self.declared_at, "declared_at")
        if self.record_type is not EvidenceRecordType.SCENARIO:
            raise ValueError("ScenarioRecord must retain scenario record_type")


@dataclass(frozen=True, slots=True, kw_only=True)
class ComputationResultRecord(ContractModel):
    """A reproducible software result; never an independently observed outcome."""

    record_id: str
    scope: str
    computed_at: datetime
    input_references: tuple[str, ...]
    configuration_reference: str
    status: ComputationStatus
    output_checksums: dict[str, str]
    numerical_warnings: tuple[str, ...]
    uncertainty: Uncertainty
    provenance: Provenance
    deterministic_seed: int | None = None
    record_type: EvidenceRecordType = EvidenceRecordType.COMPUTATION_RESULT
    schema_version: str = "1.0"

    def __post_init__(self) -> None:
        for value, name in (
            (self.record_id, "record_id"),
            (self.scope, "scope"),
            (self.configuration_reference, "configuration_reference"),
            (self.schema_version, "schema_version"),
        ):
            require_text(value, name)
        require_aware_datetime(self.computed_at, "computed_at")
        if not self.input_references:
            raise ValueError("computation result requires input references")
        _require_unique(self.input_references, "computation input references")
        if not self.output_checksums:
            raise ValueError("computation result requires output checksums")
        for name, checksum in self.output_checksums.items():
            require_text(name, "output checksum name")
            require_text(checksum, "output checksum")
        if self.record_type is not EvidenceRecordType.COMPUTATION_RESULT:
            raise ValueError(
                "ComputationResultRecord must retain computation_result record_type"
            )


@dataclass(frozen=True, slots=True, kw_only=True)
class ObservedOutcomeRecord(ContractModel):
    """A later outcome with explicit source and method-selection relationships."""

    record_id: str
    orientation_id: str
    scope: str
    observed_at: datetime
    description: str
    source_relation: OutcomeSourceRelation
    source_relation_basis: str | None
    method_selection_relation: MethodSelectionRelation
    method_selection_basis: str | None
    uncertainty: Uncertainty
    provenance: Provenance
    record_type: EvidenceRecordType = EvidenceRecordType.OBSERVED_OUTCOME
    schema_version: str = "1.0"

    def __post_init__(self) -> None:
        for value, name in (
            (self.record_id, "record_id"),
            (self.orientation_id, "orientation_id"),
            (self.scope, "scope"),
            (self.description, "description"),
            (self.schema_version, "schema_version"),
        ):
            require_text(value, name)
        require_aware_datetime(self.observed_at, "observed_at")
        if self.source_relation is not OutcomeSourceRelation.UNKNOWN:
            if self.source_relation_basis is None:
                raise ValueError("known source relation requires a basis")
            require_text(self.source_relation_basis, "source_relation_basis")
        if self.method_selection_relation is not MethodSelectionRelation.UNKNOWN:
            if self.method_selection_basis is None:
                raise ValueError("known method-selection relation requires a basis")
            require_text(self.method_selection_basis, "method_selection_basis")
        if self.record_type is not EvidenceRecordType.OBSERVED_OUTCOME:
            raise ValueError(
                "ObservedOutcomeRecord must retain observed_outcome record_type"
            )


EvidenceRecord: TypeAlias = (
    ScenarioRecord | ComputationResultRecord | ObservedOutcomeRecord
)


@dataclass(frozen=True, slots=True, kw_only=True)
class FirewallCheck(ContractModel):
    check_id: str
    status: FirewallCheckStatus
    statement: str

    def __post_init__(self) -> None:
        require_text(self.check_id, "check_id")
        require_text(self.statement, "statement")


@dataclass(frozen=True, slots=True, kw_only=True)
class OutcomeFirewallResult(ContractModel):
    orientation_id: str
    orientation_scope: str
    record_id: str
    record_type: EvidenceRecordType
    disposition: FirewallDisposition
    checks: tuple[FirewallCheck, ...]
    episode_update_allowed: bool
    evaluated_at: datetime
    provenance: Provenance
    schema_version: str = "1.0"

    def __post_init__(self) -> None:
        require_text(self.orientation_id, "orientation_id")
        require_text(self.orientation_scope, "orientation_scope")
        require_text(self.record_id, "record_id")
        require_text(self.schema_version, "schema_version")
        require_aware_datetime(self.evaluated_at, "evaluated_at")
        if len(self.checks) != 6:
            raise ValueError("outcome firewall requires exactly six checks")
        check_ids = tuple(check.check_id for check in self.checks)
        _require_unique(check_ids, "check IDs")
        if check_ids != OUTCOME_FIREWALL_CHECK_IDS:
            raise ValueError("outcome firewall checks must use the normative order")
        if self.episode_update_allowed:
            if (
                self.record_type is not EvidenceRecordType.OBSERVED_OUTCOME
                or self.disposition
                is not FirewallDisposition.ACCEPTED_OUTCOME_LINKED_CASE
                or any(check.status is not FirewallCheckStatus.PASS for check in self.checks)
            ):
                raise ValueError(
                    "episode update requires an accepted observed outcome and all checks"
                )
        elif self.disposition is FirewallDisposition.ACCEPTED_OUTCOME_LINKED_CASE:
            raise ValueError(
                "accepted outcome-linked case must authorize the episode update"
            )


def evidence_record_from_dict(data: Mapping[str, object]) -> EvidenceRecord:
    """Decode a strict evidence record from its explicit discriminator."""

    try:
        record_type = EvidenceRecordType(data["record_type"])
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError("evidence record requires a known record_type") from error
    if record_type is EvidenceRecordType.SCENARIO:
        return ScenarioRecord.from_dict(data)
    if record_type is EvidenceRecordType.COMPUTATION_RESULT:
        return ComputationResultRecord.from_dict(data)
    return ObservedOutcomeRecord.from_dict(data)


def evaluate_outcome_firewall(
    envelope: OrientationEvidenceEnvelope,
    record: EvidenceRecord,
    *,
    evaluated_at: datetime,
) -> OutcomeFirewallResult:
    """Evaluate memory eligibility without upgrading any evidence class."""

    require_aware_datetime(evaluated_at, "evaluated_at")
    if isinstance(record, (ScenarioRecord, ComputationResultRecord)):
        checks = _non_outcome_checks(record.record_type)
        disposition = FirewallDisposition.ACCEPTED_BENCHMARK_RECORD
        allowed = False
    else:
        checks = _observed_outcome_checks(envelope, record)
        statuses = {check.status for check in checks}
        if FirewallCheckStatus.FAIL in statuses:
            disposition = FirewallDisposition.REJECTED
        elif FirewallCheckStatus.UNKNOWN in statuses:
            disposition = FirewallDisposition.INDETERMINATE
        else:
            disposition = FirewallDisposition.ACCEPTED_OUTCOME_LINKED_CASE
        allowed = disposition is FirewallDisposition.ACCEPTED_OUTCOME_LINKED_CASE
    return OutcomeFirewallResult(
        orientation_id=envelope.orientation_id,
        orientation_scope=envelope.scope,
        record_id=record.record_id,
        record_type=record.record_type,
        disposition=disposition,
        checks=checks,
        episode_update_allowed=allowed,
        evaluated_at=evaluated_at,
        provenance=Provenance(
            source=envelope.provenance.source,
            method="NEXAH outcome firewall v1",
            recorded_at=evaluated_at,
            record_id=f"{envelope.orientation_id}:{record.record_id}:firewall",
            metadata={
                "orientation_provenance_id": envelope.provenance.record_id,
                "candidate_provenance_id": record.provenance.record_id,
                "no_automatic_evidence_upgrade": True,
            },
        ),
    )


def put_episode_if_authorized(
    store: EpisodeStore,
    episode: Episode,
    authorization: OutcomeFirewallResult,
) -> None:
    """Write through the safe gateway only after a matching positive decision."""

    if not authorization.episode_update_allowed:
        raise EpisodeStoreError(
            "episodic-memory update rejected by the outcome firewall"
        )
    if authorization.record_type is not EvidenceRecordType.OBSERVED_OUTCOME:
        raise EpisodeStoreError("authorization is not linked to an observed outcome")
    if authorization.record_id != episode.outcome.outcome_id:
        raise EpisodeStoreError("authorization and episode outcome identities differ")
    if (
        authorization.orientation_scope
        != episode.state.representation.representation_id
    ):
        raise EpisodeStoreError("authorization and episode scopes differ")
    store.put(episode)


def _non_outcome_checks(
    record_type: EvidenceRecordType,
) -> tuple[FirewallCheck, ...]:
    label = record_type.value
    return (
        FirewallCheck(
            check_id="record-type",
            status=FirewallCheckStatus.FAIL,
            statement=f"{label} is a valid record but not an observed outcome.",
        ),
        *tuple(
            FirewallCheck(
                check_id=check_id,
                status=FirewallCheckStatus.NOT_APPLICABLE,
                statement="Check does not apply because the record is not an outcome.",
            )
            for check_id in OUTCOME_FIREWALL_CHECK_IDS[1:]
        ),
    )


def _observed_outcome_checks(
    envelope: OrientationEvidenceEnvelope,
    outcome: ObservedOutcomeRecord,
) -> tuple[FirewallCheck, ...]:
    unknown_evidence = tuple(
        sorted(set(envelope.report_evidence_ids) - set(envelope.available_evidence_ids))
    )
    if outcome.source_relation is OutcomeSourceRelation.INDEPENDENT:
        source_status = FirewallCheckStatus.PASS
        source_statement = "Outcome source is declared independent with a basis."
    elif outcome.source_relation is OutcomeSourceRelation.TESTED_METHOD_OUTPUT:
        source_status = FirewallCheckStatus.FAIL
        source_statement = "Outcome is output of the tested method."
    else:
        source_status = FirewallCheckStatus.UNKNOWN
        source_statement = "Independence of the outcome source is unknown."
    if outcome.method_selection_relation is MethodSelectionRelation.NOT_USED:
        selection_status = FirewallCheckStatus.PASS
        selection_statement = "Outcome was not used for method or parameter selection."
    elif outcome.method_selection_relation is MethodSelectionRelation.USED:
        selection_status = FirewallCheckStatus.FAIL
        selection_statement = "Outcome influenced method or parameter selection."
    else:
        selection_status = FirewallCheckStatus.UNKNOWN
        selection_statement = "Method-selection leakage status is unknown."
    return (
        FirewallCheck(
            check_id="record-type",
            status=FirewallCheckStatus.PASS,
            statement="Candidate is explicitly typed as an observed outcome.",
        ),
        FirewallCheck(
            check_id="temporal-order",
            status=(
                FirewallCheckStatus.PASS
                if outcome.observed_at > envelope.orientation_timestamp
                else FirewallCheckStatus.FAIL
            ),
            statement=(
                "Outcome follows the orientation timestamp."
                if outcome.observed_at > envelope.orientation_timestamp
                else "Outcome does not follow the orientation timestamp."
            ),
        ),
        FirewallCheck(
            check_id="source-independence",
            status=source_status,
            statement=source_statement,
        ),
        FirewallCheck(
            check_id="scope-compatibility",
            status=(
                FirewallCheckStatus.PASS
                if outcome.orientation_id == envelope.orientation_id
                and outcome.scope == envelope.scope
                else FirewallCheckStatus.FAIL
            ),
            statement=(
                "Outcome orientation identity and scope match."
                if outcome.orientation_id == envelope.orientation_id
                and outcome.scope == envelope.scope
                else "Outcome orientation identity or scope differs."
            ),
        ),
        FirewallCheck(
            check_id="evidence-cutoff",
            status=(
                FirewallCheckStatus.PASS
                if not unknown_evidence
                else FirewallCheckStatus.FAIL
            ),
            statement=(
                "All report evidence was available at orientation time."
                if not unknown_evidence
                else "Report references evidence absent at orientation time: "
                + ", ".join(unknown_evidence)
            ),
        ),
        FirewallCheck(
            check_id="method-selection-leakage",
            status=selection_status,
            statement=selection_statement,
        ),
    )


def _require_unique(values: tuple[str, ...], label: str) -> None:
    if len(values) != len(set(values)):
        raise ValueError(f"{label} must be unique")
