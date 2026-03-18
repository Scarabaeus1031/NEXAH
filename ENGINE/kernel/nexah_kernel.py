"""
NEXAH Kernel
============

Minimal system navigation kernel for exploring complex systems.

The NEXAH kernel integrates the core layers of the NEXAH framework:

    Orientation
    Architecture
    Regime Landscape
    Navigation
    Action / Intervention

It allows systems to be:

    analyzed
    navigated
    structurally modified
    and evaluated for resilience.

The kernel operates on structural graphs and regime landscapes.

Pipeline:

    System Graph
        ↓
    Regime Landscape
        ↓
    Navigation Analysis
        ↓
    Structural Intervention

This file acts as the primary entry point for the NEXAH system engine.
"""

from .meso import build_regime_landscape
from .navigation import NavigationEngine
from .meva import ActionEngine


class NexahKernel:

    def __init__(self, graph, landscape_data):
        """
        Initialize the NEXAH kernel.

        Parameters
        ----------
        graph : StructuralGraph
            Graph representation of the system.

        landscape_data : dict
            Data describing regime attractors, basins, and thresholds.
        """

        self.graph = graph

        # Build regime landscape
        self.landscape = build_regime_landscape(landscape_data)

        # Navigation analysis engine
        self.navigator = NavigationEngine(graph, self.landscape)

        # Action / intervention engine
        self.executor = ActionEngine(graph, self.landscape)

    # --------------------------------------------------

    def analyze_system(self):
        """
        Analyze system trajectories and leverage points.
        """

        return self.navigator.evaluate_paths()

    # --------------------------------------------------

    def simulate_action(self, action):
        """
        Simulate a structural modification of the system.
        """

        return self.executor.simulate_action(action)
