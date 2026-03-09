"""
NEXAH Discovery Engine Runner

Orchestrates the NEXAH discovery pipeline.

Architecture Generation
→ Evolution
→ Resilience Analysis
→ Landscape Mapping
→ Phase Transition Detection
→ Law Discovery
→ Validation
→ Navigation
"""

from nexah_kernel.orientation import ObservationFrame
from nexah_kernel.archy import build_structural_graph
from nexah_kernel.meso import build_regime_landscape
from nexah_kernel.navigation import NavigationEngine

# tools
from tools.system_designer import generate_architecture
from tools.resilience_analyzer import analyze_resilience
from tools.resilience_landscape import compute_landscape
from tools.resilience_phase_transition_detector import detect_transitions


class NexahEngine:

    def __init__(self, config=None):
        self.config = config or {}

    def run(self):

        print("Starting NEXAH Discovery Engine")

        # ------------------------------------------------
        # 1 Architecture Generation
        # ------------------------------------------------

        architecture = generate_architecture()

        print("Architecture generated")

        # ------------------------------------------------
        # 2 Structural Graph
        # ------------------------------------------------

        graph = build_structural_graph(architecture)

        print("Structural graph built")

        # ------------------------------------------------
        # 3 Resilience Analysis
        # ------------------------------------------------

        resilience_metrics = analyze_resilience(graph)

        print("Resilience analysis complete")

        # ------------------------------------------------
        # 4 Landscape Mapping
        # ------------------------------------------------

        landscape = compute_landscape(graph)

        regime_landscape = build_regime_landscape(landscape)

        print("Regime landscape constructed")

        # ------------------------------------------------
        # 5 Phase Transitions
        # ------------------------------------------------

        transitions = detect_transitions(landscape)

        print("Phase transitions detected")

        # ------------------------------------------------
        # 6 Navigation
        # ------------------------------------------------

        navigator = NavigationEngine(graph, regime_landscape)

        navigation_results = navigator.evaluate_paths()

        print("Navigation analysis complete")

        return {
            "architecture": architecture,
            "graph": graph,
            "resilience": resilience_metrics,
            "landscape": regime_landscape,
            "transitions": transitions,
            "navigation": navigation_results,
        }


def run_engine():

    engine = NexahEngine()

    results = engine.run()

    print("NEXAH Engine finished")

    return results


if __name__ == "__main__":

    run_engine()
