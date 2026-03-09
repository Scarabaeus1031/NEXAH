from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .delta_operator import DeltaResult, compute_delta_orientation
from .hybrid_coherence import HybridCoherenceResult, compute_hybrid_coherence
from .stability_index import StabilityIndexResult, compute_archy_si_from_dict


DEFAULT_ELEMENT_KEYS = (
    "mass",
    "medium",
    "geometry",
    "location",
    "layering",
    "orientation",
    "motion",
    "frame",
    "membrane",
    "urban_form",
)


@dataclass
class ArchySystemInput:
    """
    Input model for a single ARCHY system analysis.
    """

    name: str
    outside: Dict[str, float]
    inside: Dict[str, float]
    domain_weights: Optional[Dict[str, float]] = None

    active_elements: Optional[Dict[str, float]] = None

    base_orientation: float = 0.0
    architectural_delta: float = 0.0
    environmental_delta: float = 0.0

    required_domains: Optional[List[str]] = None


@dataclass
class ArchySystemResult:
    """
    Full combined ARCHY analysis result.
    """

    name: str
    stability: StabilityIndexResult
    coherence: HybridCoherenceResult
    delta: DeltaResult

    archy_score: float
    regime_label: str
    notes: List[str] = field(default_factory=list)

    def as_dict(self) -> Dict[str, object]:
        return {
            "name": self.name,
            "stability": self.stability.as_dict(),
            "coherence": self.coherence.as_dict(),
            "delta": self.delta.as_dict(),
            "archy_score": self.archy_score,
            "regime_label": self.regime_label,
            "notes": self.notes,
        }


def normalize_element_weights(
    active_elements: Optional[Dict[str, float]] = None,
) -> Dict[str, float]:
    """
    Normalize ARCHY element activations to [0, 1].

    Missing keys are filled with 0.0.
    Values above 1.0 are clipped to 1.0.
    Values below 0.0 are clipped to 0.0.
    """
    active_elements = active_elements or {}
    normalized: Dict[str, float] = {}

    for key in DEFAULT_ELEMENT_KEYS:
        value = float(active_elements.get(key, 0.0))
        normalized[key] = max(0.0, min(1.0, value))

    return normalized


def compute_coupling_factor_from_elements(
    active_elements: Optional[Dict[str, float]] = None,
) -> float:
    """
    Estimate coupling factor C from ARCHY element activation.

       active_elements = normalize_element_weights(active_elements)

    total = sum(active_elements.values())
    max_total = len(DEFAULT_ELEMENT_KEYS)

    return total / max_total


def compute_archy_score(
    si: float,
    hcf: float,
    delta: float,
) -> float:
    """
    Combine SI, HCF and Δ into a single ARCHY system score.

    Δ acts as a penalty term (misalignment).

    ARCHY score model:

        score = (SI * 0.5 + HCF * 0.5) * (1 - drift_penalty)

    where drift_penalty = min(delta, 1.0)
    """

    drift_penalty = min(delta, 1.0)

    base = (si * 0.5) + (hcf * 0.5)

    return base * (1.0 - drift_penalty)


def classify_regime(score: float) -> str:
    """
    Classify ARCHY system regime.
    """

    if score < 0.3:
        return "unstable regime"

    if score < 0.5:
        return "fragile regime"

    if score < 0.7:
        return "moderate stability"

    if score < 0.85:
        return "robust structure"

    return "highly coherent system"


def analyze_archy_system(input_model: ArchySystemInput) -> ArchySystemResult:
    """
    Full ARCHY system analysis pipeline.
    """

    notes: List[str] = []

    # ---------- Stability Index ----------

    stability = compute_archy_si_from_dict(
        outside=input_model.outside,
        inside=input_model.inside,
        weights=input_model.domain_weights,
        required_domains=input_model.required_domains,
    )

    si_total = stability.weighted_score

    # ---------- Coupling Factor ----------

    coupling = compute_coupling_factor_from_elements(
        input_model.active_elements
    )

    coherence = compute_hybrid_coherence(
        stability_index=si_total,
        coupling_factor=coupling,
    )

    # ---------- Orientation Drift ----------

    delta = compute_delta_orientation(
        base_orientation=input_model.base_orientation,
        architectural_delta=input_model.architectural_delta,
        environmental_delta=input_model.environmental_delta,
    )

    # normalize orientation
    delta.total_orientation = delta.total_orientation % 360

    # ---------- Final ARCHY Score ----------

    archy_score = compute_archy_score(
        si=si_total,
        hcf=coherence.hybrid_coherence,
        delta=delta.drift_magnitude,
    )

    regime = classify_regime(archy_score)

    # ---------- Notes ----------

    if delta.drift_magnitude > 0.3:
        notes.append("orientation drift detected")

    if coherence.hybrid_coherence < 0.4:
        notes.append("weak hybrid coupling")

    if si_total < 0.5:
        notes.append("low stabilization performance")

    return ArchySystemResult(
        name=input_model.name,
        stability=stability,
        coherence=coherence,
        delta=delta,
        archy_score=archy_score,
        regime_label=regime,
        notes=notes,
    )


def example_cave_system() -> ArchySystemResult:
    """
    Example analysis: cave-like stabilization system.
    """

    input_model = ArchySystemInput(
        name="cave_system",

        outside={
            "thermal": 20,
            "pressure": 1,
            "acoustic": 1,
            "humidity": 1,
        },

        inside={
            "thermal": 5,
            "pressure": 0.1,
            "acoustic": 0.2,
            "humidity": 0.6,
        },

        domain_weights={
            "thermal": 1.2,
            "pressure": 1.0,
            "acoustic": 1.0,
            "humidity": 0.8,
        },

        active_elements={
            "mass": 1,
            "medium": 1,
            "geometry": 0.7,
            "location": 0.8,
            "layering": 0.6,
        },

        base_orientation=0,
        architectural_delta=0.05,
        environmental_delta=0.02,
    )

    return analyze_archy_system(input_model)


def pretty_print(result: ArchySystemResult) -> str:

    lines = []

    lines.append(f"ARCHY SYSTEM ANALYSIS : {result.name}")
    lines.append("=" * 40)

    lines.append(f"ARCHY SCORE : {result.archy_score:.3f}")
    lines.append(f"REGIME      : {result.regime_label}")

    lines.append("")

    lines.append("STABILITY INDEX")
    lines.append(f"  weighted SI : {result.stability.weighted_score:.3f}")

    lines.append("")

    lines.append("HYBRID COHERENCE")
    lines.append(f"  HCF : {result.coherence.hybrid_coherence:.3f}")

    lines.append("")

    lines.append("ORIENTATION")
    lines.append(f"  drift : {result.delta.drift_magnitude:.3f}")

    if result.notes:
        lines.append("")
        lines.append("NOTES")

        for n in result.notes:
            lines.append(f"  - {n}")

    return "\n".join(lines)


if __name__ == "__main__":

    result = example_cave_system()

    print(pretty_print(result))
