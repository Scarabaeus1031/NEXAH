"""Frozen, machine-readable protocol for the Phase V IEEE geometry case."""

from __future__ import annotations

from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError, version
from math import isfinite
from platform import python_version
from collections.abc import Mapping

from nexah.orientation.base import ContractModel, require_text
from nexah.sources.ieee import (
    IEEEPandapowerAdapter,
    PANDAPOWER_ALGORITHM,
    PANDAPOWER_INITIALIZATION,
    PANDAPOWER_MAX_ITERATION,
    PANDAPOWER_TOLERANCE_MVA,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class SoftwareLock(ContractModel):
    package: str
    exact_version: str

    def __post_init__(self) -> None:
        require_text(self.package, "package")
        require_text(self.exact_version, "exact_version")


@dataclass(frozen=True, slots=True, kw_only=True)
class IEEESolverProtocol(ContractModel):
    algorithm: str
    max_iteration: int
    tolerance_mva: float
    initialization: str
    independent_points: bool

    def __post_init__(self) -> None:
        require_text(self.algorithm, "algorithm")
        require_text(self.initialization, "initialization")
        if self.max_iteration < 1:
            raise ValueError("max_iteration must be positive")
        if not isfinite(self.tolerance_mva) or self.tolerance_mva <= 0.0:
            raise ValueError("tolerance_mva must be finite and positive")
        if not self.independent_points:
            raise ValueError("Phase V requires independently solved campaign points")


@dataclass(frozen=True, slots=True, kw_only=True)
class IEEECaseDefinition(ContractModel):
    case_id: str
    source_loader: str
    role: str
    load_scales: tuple[float, ...]
    historically_inspected: bool
    role_locked_before_geometry_results: bool
    selection_note: str

    def __post_init__(self) -> None:
        require_text(self.case_id, "case_id")
        require_text(self.source_loader, "source_loader")
        require_text(self.selection_note, "selection_note")
        if self.role not in {"method_development", "locked_evaluation"}:
            raise ValueError("case role must be method_development or locked_evaluation")
        if len(self.load_scales) < 3:
            raise ValueError("geometry campaigns require at least three load scales")
        if any(not isfinite(value) or value <= 0.0 for value in self.load_scales):
            raise ValueError("load scales must be finite and positive")
        if any(
            current <= previous
            for previous, current in zip(self.load_scales, self.load_scales[1:])
        ):
            raise ValueError("load scales must be strictly increasing")
        if not self.role_locked_before_geometry_results:
            raise ValueError("every Phase V case role must be locked before results")


@dataclass(frozen=True, slots=True, kw_only=True)
class IEEEVariableDefinition(ContractModel):
    name: str
    entity_scope: str
    unit: str
    source_field: str
    missing_policy: str

    def __post_init__(self) -> None:
        require_text(self.name, "name")
        require_text(self.entity_scope, "entity_scope")
        require_text(self.unit, "unit")
        require_text(self.source_field, "source_field")
        require_text(self.missing_policy, "missing_policy")


@dataclass(frozen=True, slots=True, kw_only=True)
class IEEEProjectionDefinition(ContractModel):
    projection_id: str
    inputs: tuple[str, ...]
    entity_alignment: str
    normalization: str
    fit_scope: str
    information_loss: str

    def __post_init__(self) -> None:
        require_text(self.projection_id, "projection_id")
        if not self.inputs:
            raise ValueError("projection requires at least one input")
        require_text(self.entity_alignment, "entity_alignment")
        require_text(self.normalization, "normalization")
        require_text(self.fit_scope, "fit_scope")
        require_text(self.information_loss, "information_loss")


@dataclass(frozen=True, slots=True, kw_only=True)
class IEEEGeometryOperatorDefinition(ContractModel):
    operator_id: str
    projection_id: str
    minimum_points: int
    formula: str
    insufficiency_policy: str

    def __post_init__(self) -> None:
        require_text(self.operator_id, "operator_id")
        require_text(self.projection_id, "projection_id")
        require_text(self.formula, "formula")
        require_text(self.insufficiency_policy, "insufficiency_policy")
        if self.minimum_points < 2:
            raise ValueError("geometry operator requires at least two points")


@dataclass(frozen=True, slots=True, kw_only=True)
class IEEEGeometryCaseManifest(ContractModel):
    manifest_id: str
    research_question: str
    evidence_class: str
    adapter_id: str
    campaign_axis: str
    axis_is_time: bool
    python_exact_version: str
    software_locks: tuple[SoftwareLock, ...]
    solver: IEEESolverProtocol
    cases: tuple[IEEECaseDefinition, ...]
    variables: tuple[IEEEVariableDefinition, ...]
    projections: tuple[IEEEProjectionDefinition, ...]
    operators: tuple[IEEEGeometryOperatorDefinition, ...]
    supported_claims: tuple[str, ...]
    prohibited_claims: tuple[str, ...]
    evaluation_rules: tuple[str, ...]
    outcome_status: str
    episode_update_allowed: bool
    schema_version: str = "1.0"

    def __post_init__(self) -> None:
        require_text(self.manifest_id, "manifest_id")
        require_text(self.research_question, "research_question")
        require_text(self.adapter_id, "adapter_id")
        require_text(self.campaign_axis, "campaign_axis")
        require_text(self.python_exact_version, "python_exact_version")
        require_text(self.schema_version, "schema_version")
        if self.evidence_class != "benchmark_model":
            raise ValueError("IEEE geometry manifest must remain benchmark_model evidence")
        if self.axis_is_time:
            raise ValueError("ordered load scale must not be represented as time")
        if self.outcome_status != "not_observed" or self.episode_update_allowed:
            raise ValueError("benchmark manifest cannot authorize episodic memory")
        roles = [case.role for case in self.cases]
        if roles.count("method_development") < 1 or roles.count("locked_evaluation") < 1:
            raise ValueError("manifest requires development and locked evaluation cases")
        case_ids = [case.case_id for case in self.cases]
        if len(case_ids) != len(set(case_ids)):
            raise ValueError("case IDs must be unique")
        campaign_grids = {case.load_scales for case in self.cases}
        if len(campaign_grids) != 1:
            raise ValueError("Phase V cases must share the frozen load-scale grid")
        packages = [lock.package for lock in self.software_locks]
        if len(packages) != len(set(packages)):
            raise ValueError("software lock packages must be unique")
        variable_names = [variable.name for variable in self.variables]
        if len(variable_names) != len(set(variable_names)):
            raise ValueError("variable names must be unique")
        projection_ids = [projection.projection_id for projection in self.projections]
        if len(projection_ids) != len(set(projection_ids)):
            raise ValueError("projection IDs must be unique")
        known_variables = set(variable_names)
        for projection in self.projections:
            unknown = set(projection.inputs) - known_variables
            if unknown:
                raise ValueError(
                    f"projection {projection.projection_id} has unknown inputs: "
                    + ", ".join(sorted(unknown))
                )
        known_projections = set(projection_ids)
        operator_ids = [operator.operator_id for operator in self.operators]
        if len(operator_ids) != len(set(operator_ids)):
            raise ValueError("geometry operator IDs must be unique")
        for operator in self.operators:
            if operator.projection_id not in known_projections:
                raise ValueError(
                    f"operator {operator.operator_id} references unknown projection"
                )
        if not self.supported_claims or not self.prohibited_claims:
            raise ValueError("manifest requires supported and prohibited claims")
        if not self.evaluation_rules:
            raise ValueError("manifest requires evaluation rules")


@dataclass(frozen=True, slots=True, kw_only=True)
class ManifestEnvironmentCheck(ContractModel):
    compatible: bool
    mismatches: tuple[str, ...]
    installed_versions: dict[str, str]


def check_manifest_environment(
    manifest: IEEEGeometryCaseManifest,
    *,
    installed_versions: Mapping[str, str] | None = None,
    installed_python: str | None = None,
) -> ManifestEnvironmentCheck:
    """Compare runtime versions with the frozen manifest without changing it."""

    observed = dict(installed_versions or _installed_versions(manifest.software_locks))
    runtime_python = installed_python or python_version()
    mismatches: list[str] = []
    if runtime_python != manifest.python_exact_version:
        mismatches.append(
            f"python: expected {manifest.python_exact_version}, found {runtime_python}"
        )
    for lock in manifest.software_locks:
        actual = observed.get(lock.package, "not-installed")
        if actual != lock.exact_version:
            mismatches.append(
                f"{lock.package}: expected {lock.exact_version}, found {actual}"
            )
    return ManifestEnvironmentCheck(
        compatible=not mismatches,
        mismatches=tuple(mismatches),
        installed_versions=observed,
    )


def check_manifest_adapter_protocol(
    manifest: IEEEGeometryCaseManifest,
) -> tuple[str, ...]:
    """Detect drift between a frozen manifest and the executable source adapter."""

    mismatches: list[str] = []
    if manifest.adapter_id != IEEEPandapowerAdapter().adapter_id:
        mismatches.append(
            f"adapter_id: expected {IEEEPandapowerAdapter().adapter_id}, "
            f"found {manifest.adapter_id}"
        )
    expected_solver = (
        PANDAPOWER_ALGORITHM,
        PANDAPOWER_MAX_ITERATION,
        PANDAPOWER_TOLERANCE_MVA,
        PANDAPOWER_INITIALIZATION,
    )
    actual_solver = (
        manifest.solver.algorithm,
        manifest.solver.max_iteration,
        manifest.solver.tolerance_mva,
        manifest.solver.initialization,
    )
    if actual_solver != expected_solver:
        mismatches.append("solver configuration differs from executable adapter")
    loaders = IEEEPandapowerAdapter.supported_case_loaders()
    for case in manifest.cases:
        expected_loader = loaders.get(case.case_id)
        actual_loader = case.source_loader.rsplit(".", 1)[-1]
        if expected_loader is None:
            mismatches.append(f"case {case.case_id} is unsupported by the adapter")
        elif actual_loader != expected_loader:
            mismatches.append(
                f"case {case.case_id}: expected loader {expected_loader}, "
                f"found {actual_loader}"
            )
    return tuple(mismatches)


def _installed_versions(locks: tuple[SoftwareLock, ...]) -> dict[str, str]:
    result: dict[str, str] = {}
    for lock in locks:
        try:
            result[lock.package] = version(lock.package)
        except PackageNotFoundError:
            result[lock.package] = "not-installed"
    return result
