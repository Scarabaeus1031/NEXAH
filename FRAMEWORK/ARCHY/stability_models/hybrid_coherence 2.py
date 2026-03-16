from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class HybridCoherenceResult:
    """
    Result container for ARCHY Hybrid Coherence Factor calculations.
    """

    stability_index: float
    coupling_factor: float
    hybrid_coherence: float
    interpretation: str

    def as_dict(self) -> Dict[str, float | str]:
        return {
            "stability_index": self.stability_index,
            "coupling_factor": self.coupling_factor,
            "hybrid_coherence": self.hybrid_coherence,
            "interpretation": self.interpretation,
        }


def compute_hybrid_coherence(
    stability_index: float,
    coupling_factor: float,
) -> HybridCoherenceResult:
    """
    Compute Hybrid Coherence Factor.

    Formula:

        HCF = SI_total * C

    Where:

        SI_total = total stabilization score
        C = coupling factor between stabilization elements

    Interpretation:

        0.0 – 0.3  weak structure
        0.3 – 0.6  moderate stabilization
        0.6 – 0.8  robust hybrid stabilization
        0.8 – 1.0  highly coherent stabilization system
    """

    if not 0 <= stability_index <= 1:
        raise ValueError("stability_index must be between 0 and 1")

    if not 0 <= coupling_factor <= 1:
        raise ValueError("coupling_factor must be between 0 and 1")

    hcf = stability_index * coupling_factor

    interpretation = classify_hcf(hcf)

    return HybridCoherenceResult(
        stability_index=stability_index,
        coupling_factor=coupling_factor,
        hybrid_coherence=hcf,
        interpretation=interpretation,
    )


def classify_hcf(hcf: float) -> str:
    """
    Classify Hybrid Coherence value.
    """

    if hcf < 0.3:
        return "weak stabilization"

    if hcf < 0.6:
        return "moderate stabilization"

    if hcf < 0.8:
        return "robust hybrid stabilization"

    return "highly coherent stabilization system"


def estimate_coupling_from_elements(
    active_elements: int,
    total_elements: int = 10,
) -> float:
    """
    Estimate coupling factor based on number of active stabilization elements.

    ARCHY defines 10 stabilization elements:

        mass
        medium
        geometry
        location
        layering
        orientation
        motion
        frame
        membrane
        urban form
    """

    if total_elements <= 0:
        raise ValueError("total_elements must be positive")

    if active_elements < 0:
        raise ValueError("active_elements cannot be negative")

    if active_elements > total_elements:
        active_elements = total_elements

    return active_elements / total_elements


def example_architecture_case() -> HybridCoherenceResult:
    """
    Example case: traditional stone building.
    """

    stability_index = 0.72

    # example: 7 out of 10 ARCHY elements active
    coupling = estimate_coupling_from_elements(
        active_elements=7
    )

    return compute_hybrid_coherence(
        stability_index=stability_index,
        coupling_factor=coupling,
    )


def pretty_print(result: HybridCoherenceResult) -> str:
    lines = []
    lines.append("ARCHY Hybrid Coherence Result")
    lines.append("-" * 34)
    lines.append(f"stability_index : {result.stability_index:.3f}")
    lines.append(f"coupling_factor : {result.coupling_factor:.3f}")
    lines.append(f"HCF             : {result.hybrid_coherence:.3f}")
    lines.append(f"classification  : {result.interpretation}")
    return "\n".join(lines)


if __name__ == "__main__":
    result = example_architecture_case()
    print(pretty_print(result))
