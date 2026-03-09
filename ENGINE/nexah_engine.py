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

# ------------------------------------------------
# Kernel Layers
# ------------------------------------------------

from ENGINE.nexah_kernel.orientation import ObservationFrame
from ENGINE.nexah_kernel.archy import build_structural_graph
from ENGINE.nexah_kernel.meso import build_regime_landscape
from ENGINE.nexah_kernel.navigation import NavigationEngine

# ------------------------------------------------
# Tools
# ------------------------------------------------

from tools.system_designer import generate_architecture
from tools.resilience_analyzer import analyze_resilience
from tools.resilience_landscape import compute_landscape
from tools.resilience_phase_transition_detector import detect_transitions


class NexahEngine:

    def __init__(self, config=None):
        self.config = config or {}

    def run(self):

        print("\nStarting NEXAH Discovery Engine\n")

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

        try:
            landscape = compute_landscape(graph)
        except Exception:
            landscape = {
                "nodes": list(graph.nodes()),
                "edges": list(graph.edges()),
                "landscape_type": "graph_fallback"
            }

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

        print("Navigation analysis complete\n")

        return {
            "architecture": architecture,
            "graph": graph,
            "resilience": resilience_metrics,
            "landscape": regime_landscape,
            "transitions": transitions,
            "navigation": navigation_results,
        }


# ------------------------------------------------
# Runner
# ------------------------------------------------

def run_engine():

    engine = NexahEngine()
    results = engine.run()

    print("NEXAH Engine finished\n")

    return results


if __name__ == "__main__":
    run_engine()        # Some landscape tools expect JSON path instead of graph.
        # If that fails, build a minimal landscape directly from graph.

        try:
            landscape = compute_landscape(graph)

        except Exception:

            # fallback landscape
            landscape = {
                "nodes": list(graph.nodes()),
                "edges": list(graph.edges()),
                "landscape_type": "graph_fallback"
            }

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

        print("Navigation analysis complete\n")

        return {
            "architecture": architecture,
            "graph": graph,
            "resilience": resilience_metrics,
            "landscape": regime_landscape,
            "transitions": transitions,
            "navigation": navigation_results,
        }


# ------------------------------------------------
# Runner
# ------------------------------------------------

def run_engine():

    engine = NexahEngine()

    results = engine.run()

    print("NEXAH Engine finished\n")

    return results


if __name__ == "__main__":

    run_engine()        # Adapter logic:
        # some landscape tools expect system_path instead of graph

        try:
            landscape = compute_landscape(graph)
        except TypeError:
            if isinstance(architecture, dict) and "system" in architecture:
                system = architecture["system"]

                if hasattr(system, "metadata") and "source_path" in system.metadata:
                    landscape = compute_landscape(system.metadata["source_path"])
                else:
                    raise
            else:
                raise

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

        print("Navigation analysis complete\n")

        return {
            "architecture": architecture,
            "graph": graph,
            "resilience": resilience_metrics,
            "landscape": regime_landscape,
            "transitions": transitions,
            "navigation": navigation_results,
        }


# ------------------------------------------------
# Runner
# ------------------------------------------------

def run_engine():

    engine = NexahEngine()

    results = engine.run()

    print("NEXAH Engine finished\n")

    return results


if __name__ == "__main__":

    run_engine()
