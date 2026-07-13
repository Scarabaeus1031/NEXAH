"""Coupled physical views for pandapower IEEE benchmark networks."""

from __future__ import annotations

from dataclasses import dataclass
import importlib
from math import isfinite
from typing import Any, Sequence

import numpy as np

from nexah.orientation import Context, Provenance
from nexah.orientation.base import ContractModel, require_text

from .array import ArraySourceAdapter
from .base import (
    SourceAdapterError,
    SourceAxis,
    SourceBatch,
    SourceFeature,
    SourceQuality,
)


class IEEESourceAdapterError(SourceAdapterError):
    """Raised when an IEEE source campaign cannot be represented honestly."""


@dataclass(frozen=True, slots=True, kw_only=True)
class IEEEPhysicalSnapshot(ContractModel):
    """One load case with separate bus and line entity views."""

    scenario_id: str
    case_id: str
    load_scale: float
    converged: bool
    bus_batch: SourceBatch | None
    line_batch: SourceBatch | None
    failure: str | None = None

    def __post_init__(self) -> None:
        require_text(self.scenario_id, "scenario_id")
        require_text(self.case_id, "case_id")
        if not isfinite(self.load_scale) or self.load_scale <= 0.0:
            raise ValueError("load_scale must be finite and positive")
        if self.converged:
            if self.bus_batch is None or self.line_batch is None:
                raise ValueError("converged snapshots require bus and line batches")
            if self.failure is not None:
                raise ValueError("converged snapshots cannot contain a failure")
            if self.bus_batch.row_axis is not SourceAxis.ENTITY:
                raise ValueError("bus snapshot must use the entity row axis")
            if self.line_batch.row_axis is not SourceAxis.ENTITY:
                raise ValueError("line snapshot must use the entity row axis")
        else:
            if self.bus_batch is not None or self.line_batch is not None:
                raise ValueError("failed snapshots cannot contain physical batches")
            if self.failure is None:
                raise ValueError("failed snapshots require a failure description")


@dataclass(frozen=True, slots=True, kw_only=True)
class IEEECoupledCampaign(ContractModel):
    """Spatial entity snapshots coupled to one ordered system campaign."""

    campaign_id: str
    case_id: str
    snapshots: tuple[IEEEPhysicalSnapshot, ...]
    campaign_batch: SourceBatch
    provenance: Provenance
    context: Context

    def __post_init__(self) -> None:
        require_text(self.campaign_id, "campaign_id")
        require_text(self.case_id, "case_id")
        if not self.snapshots:
            raise ValueError("IEEE campaign requires snapshots")
        if self.campaign_batch.row_axis is not SourceAxis.ORDERED_SAMPLE:
            raise ValueError("IEEE load campaign must use the ordered-sample axis")
        if self.campaign_batch.provenance != self.provenance:
            raise ValueError("campaign batch must preserve root provenance")
        if self.campaign_batch.context != self.context:
            raise ValueError("campaign batch must preserve root context")


class IEEEPandapowerAdapter:
    """Extract physical IEEE observations without assigning NEXAH regimes."""

    _CASE_LOADERS = {
        "ieee9": "case9",
        "ieee14": "case14",
        "ieee30": "case30",
        "ieee57": "case57",
        "ieee118": "case118",
    }

    def __init__(self, *, case_id: str = "ieee14") -> None:
        if case_id not in self._CASE_LOADERS:
            supported = ", ".join(self._CASE_LOADERS)
            raise IEEESourceAdapterError(
                f"unsupported IEEE case {case_id!r}; choose one of: {supported}"
            )
        self.case_id = case_id

    @property
    def adapter_id(self) -> str:
        return "pandapower-ieee-coupled-source-v1"

    def run_campaign(
        self,
        load_scales: Sequence[float],
        *,
        campaign_id: str,
        provenance: Provenance,
        context: Context,
    ) -> IEEECoupledCampaign:
        require_text(campaign_id, "campaign_id")
        scales = tuple(float(value) for value in load_scales)
        if len(scales) < 2:
            raise IEEESourceAdapterError("campaign requires at least two load scales")
        if any(not isfinite(value) or value <= 0.0 for value in scales):
            raise IEEESourceAdapterError("load scales must be finite and positive")
        if any(current <= previous for previous, current in zip(scales, scales[1:])):
            raise IEEESourceAdapterError("load scales must be strictly increasing")

        snapshots = tuple(
            self._run_snapshot(
                load_scale=load_scale,
                scenario_id=f"{campaign_id}:load-{index:03d}",
                provenance=provenance,
                context=context,
            )
            for index, load_scale in enumerate(scales)
        )
        converged = tuple(snapshot for snapshot in snapshots if snapshot.converged)
        if not converged:
            raise IEEESourceAdapterError("no campaign scenario converged")

        rows = tuple(self._summary_row(snapshot) for snapshot in converged)
        row_ids = tuple(snapshot.scenario_id for snapshot in converged)
        failed = len(snapshots) - len(converged)
        campaign_batch = SourceBatch(
            batch_id=f"{campaign_id}:campaign",
            values=rows,
            features=_CAMPAIGN_FEATURES,
            context=context,
            provenance=provenance,
            quality=SourceQuality(
                input_rows=len(snapshots),
                output_rows=len(converged),
                missing_values=0,
                non_finite_values=0,
                transformations=(
                    f"excluded {failed} non-converged scenarios from numeric campaign",
                )
                if failed
                else (),
            ),
            row_axis=SourceAxis.ORDERED_SAMPLE,
            row_ids=row_ids,
        )
        return IEEECoupledCampaign(
            campaign_id=campaign_id,
            case_id=self.case_id,
            snapshots=snapshots,
            campaign_batch=campaign_batch,
            provenance=provenance,
            context=context,
        )

    def _run_snapshot(
        self,
        *,
        load_scale: float,
        scenario_id: str,
        provenance: Provenance,
        context: Context,
    ) -> IEEEPhysicalSnapshot:
        pp, networks = _pandapower_modules()
        loader = getattr(networks, self._CASE_LOADERS[self.case_id])
        net = loader()
        net.load.loc[:, "p_mw"] *= load_scale
        net.load.loc[:, "q_mvar"] *= load_scale
        try:
            pp.runpp(
                net,
                algorithm="nr",
                max_iteration=30,
                tolerance_mva=1e-6,
                init="auto",
            )
        except Exception as error:
            return IEEEPhysicalSnapshot(
                scenario_id=scenario_id,
                case_id=self.case_id,
                load_scale=load_scale,
                converged=False,
                bus_batch=None,
                line_batch=None,
                failure=f"{type(error).__name__}: {error}",
            )

        bus_values = net.res_bus.loc[
            :, ["vm_pu", "va_degree", "p_mw", "q_mvar"]
        ].to_numpy(dtype=np.float64)
        bus_ids = tuple(f"bus:{index}" for index in net.res_bus.index)
        bus_batch = ArraySourceAdapter().adapt(
            bus_values,
            batch_id=f"{scenario_id}:buses",
            provenance=provenance,
            context=context,
            feature_names=("vm_pu", "va_degree", "p_mw", "q_mvar"),
            units=("pu", "degree", "MW", "MVAr"),
            row_axis=SourceAxis.ENTITY,
            row_ids=bus_ids,
        )

        line_values = net.res_line.loc[
            :, ["loading_percent", "p_from_mw", "q_from_mvar"]
        ].to_numpy(dtype=np.float64)
        line_ids = tuple(
            f"line:{index}:{int(net.line.at[index, 'from_bus'])}-{int(net.line.at[index, 'to_bus'])}"
            for index in net.res_line.index
        )
        line_batch = ArraySourceAdapter().adapt(
            line_values,
            batch_id=f"{scenario_id}:lines",
            provenance=provenance,
            context=context,
            feature_names=("loading_percent", "p_from_mw", "q_from_mvar"),
            units=("percent", "MW", "MVAr"),
            row_axis=SourceAxis.ENTITY,
            row_ids=line_ids,
        )
        return IEEEPhysicalSnapshot(
            scenario_id=scenario_id,
            case_id=self.case_id,
            load_scale=load_scale,
            converged=True,
            bus_batch=bus_batch,
            line_batch=line_batch,
        )

    def _summary_row(self, snapshot: IEEEPhysicalSnapshot) -> tuple[float, ...]:
        if snapshot.bus_batch is None or snapshot.line_batch is None:
            raise IEEESourceAdapterError("cannot summarize a failed snapshot")
        buses = snapshot.bus_batch.to_numpy()
        lines = snapshot.line_batch.to_numpy()
        return (
            snapshot.load_scale,
            float(np.min(buses[:, 0])),
            float(np.mean(buses[:, 0])),
            float(np.std(buses[:, 0])),
            float(np.max(buses[:, 1]) - np.min(buses[:, 1])),
            float(np.max(lines[:, 0])),
            float(np.sum(np.clip(buses[:, 2], 0.0, None))),
            float(np.sum(np.clip(buses[:, 3], 0.0, None))),
        )


_CAMPAIGN_FEATURES = (
    SourceFeature(name="load_scale", unit="ratio"),
    SourceFeature(name="minimum_bus_voltage", unit="pu"),
    SourceFeature(name="mean_bus_voltage", unit="pu"),
    SourceFeature(name="bus_voltage_std", unit="pu"),
    SourceFeature(name="bus_angle_range", unit="degree"),
    SourceFeature(name="maximum_line_loading", unit="percent"),
    SourceFeature(name="total_bus_consumption_p", unit="MW"),
    SourceFeature(name="total_bus_consumption_q", unit="MVAr"),
)


def _pandapower_modules() -> tuple[Any, Any]:
    try:
        return (
            importlib.import_module("pandapower"),
            importlib.import_module("pandapower.networks"),
        )
    except ImportError as error:
        raise IEEESourceAdapterError(
            "pandapower is required for the IEEE source adapter"
        ) from error
