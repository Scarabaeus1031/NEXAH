from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Tuple


DEFAULT_DOMAINS: Tuple[str, ...] = (
    "thermal",
    "pressure",
    "humidity",
    "acoustic",
    "light",
)


@dataclass(frozen=True)
class DomainMeasurement:
    """
    Represents one environmental stabilization domain.

    Example:
        thermal: outside amplitude 20, inside amplitude 5
        SI = 1 - (5 / 20) = 0.75
    """

    name: str
    outside: float
    inside: float
    weight: float = 1.0

    def validate(self) -> None:
        if self.outside <= 0:
            raise ValueError(
                f"Domain '{self.name}' must have outside > 0, got {self.outside}."
            )
        if self.inside < 0:
            raise ValueError(
                f"Domain '{self.name}' must have inside >= 0, got {self.inside}."
            )
        if self.weight < 0:
            raise ValueError(
                f"Domain '{self.name}' must have weight >= 0, got {self.weight}."
            )


@dataclass
class StabilityIndexResult:
    """
    Result container for ARCHY Stability Index calculations.
    """

    domain_scores: Dict[str, float]
    weighted_score: float
    unweighted_score: float
    total_weight: float
    valid_domains: List[str] = field(default_factory=list)

    def as_dict(self) -> Dict[str, object]:
        return {
            "domain_scores": self.domain_scores,
            "weighted_score": self.weighted_score,
            "unweighted_score": self.unweighted_score,
            "total_weight": self.total_weight,
            "valid_domains": self.valid_domains,
        }


def compute_domain_si(outside: float, inside: float) -> float:
    """
    ARCHY Stability Index per domain:

        SI = 1 - (inside / outside)

    Interpretation:
        SI = 0   -> no stabilization
        SI = 1   -> full stabilization
        SI < 0   -> inside variance exceeds outside variance
        SI > 1   -> mathematically possible only from inconsistent inputs

    We clamp the result into [0, 1] because ARCHY is intended as
    a bounded stabilization score.
    """
    if outside <= 0:
        raise ValueError(f"outside must be > 0, got {outside}")
    if inside < 0:
        raise ValueError(f"inside must be >= 0, got {inside}")

    raw = 1.0 - (inside / outside)
    return max(0.0, min(1.0, raw))


def compute_stability_index(
    measurements: Iterable[DomainMeasurement],
) -> StabilityIndexResult:
    """
    Compute weighted and unweighted ARCHY Stability Index across domains.
    """
    domain_scores: Dict[str, float] = {}
    weighted_sum = 0.0
    total_weight = 0.0
    unweighted_values: List[float] = []
    valid_domains: List[str] = []

    for m in measurements:
        m.validate()
        score = compute_domain_si(m.outside, m.inside)

        domain_scores[m.name] = score
        weighted_sum += score * m.weight
        total_weight += m.weight
        unweighted_values.append(score)
        valid_domains.append(m.name)

    if not valid_domains:
        raise ValueError("No measurements provided.")

    weighted_score = weighted_sum / total_weight if total_weight > 0 else 0.0
    unweighted_score = sum(unweighted_values) / len(unweighted_values)

    return StabilityIndexResult(
        domain_scores=domain_scores,
        weighted_score=weighted_score,
        unweighted_score=unweighted_score,
        total_weight=total_weight,
        valid_domains=valid_domains,
    )


def compute_archy_si_from_dict(
    outside: Dict[str, float],
    inside: Dict[str, float],
    weights: Optional[Dict[str, float]] = None,
    required_domains: Optional[Iterable[str]] = None,
) -> StabilityIndexResult:
    """
    Convenience interface using dictionaries.

    Example:
        outside = {"thermal": 20, "pressure": 1.0}
        inside  = {"thermal": 5,  "pressure": 0.1}
        weights = {"thermal": 1.5, "pressure": 1.0}
    """
    weights = weights or {}
    domains = tuple(required_domains) if required_domains is not None else tuple(outside.keys())

    measurements: List[DomainMeasurement] = []

    for domain in domains:
        if domain not in outside:
            raise KeyError(f"Missing outside value for domain '{domain}'.")
        if domain not in inside:
            raise KeyError(f"Missing inside value for domain '{domain}'.")

        measurements.append(
            DomainMeasurement(
                name=domain,
                outside=outside[domain],
                inside=inside[domain],
                weight=weights.get(domain, 1.0),
            )
        )

    return compute_stability_index(measurements)


def pretty_print_result(result: StabilityIndexResult) -> str:
    lines = []
    lines.append("ARCHY Stability Index Result")
    lines.append("-" * 32)

    for name, score in result.domain_scores.items():
        lines.append(f"{name:>10}: {score:.3f}")

    lines.append("-" * 32)
    lines.append(f"{'unweighted':>10}: {result.unweighted_score:.3f}")
    lines.append(f"{'weighted':>10}: {result.weighted_score:.3f}")
    lines.append(f"{'weight_sum':>10}: {result.total_weight:.3f}")
    return "\n".join(lines)


def example_cave_case() -> StabilityIndexResult:
    """
    Example based on a cave-like stabilization model.
    """
    outside = {
        "thermal": 20.0,
        "pressure": 1.0,
        "acoustic": 1.0,
        "humidity": 1.0,
    }
    inside = {
        "thermal": 5.0,
        "pressure": 0.1,
        "acoustic": 0.2,
        "humidity": 0.6,
    }
    weights = {
        "thermal": 1.0,
        "pressure": 1.0,
        "acoustic": 1.0,
        "humidity": 1.0,
    }

    return compute_archy_si_from_dict(
        outside=outside,
        inside=inside,
        weights=weights,
    )


if __name__ == "__main__":
    result = example_cave_case()
    print(pretty_print_result(result))
