"""
NEXAH Kernel Package
====================

Core navigation kernel for the NEXAH framework.

This package implements the minimal navigation engine used to analyze
and intervene in complex dynamical systems.

The kernel operates on structural graphs embedded in regime landscapes
and enables trajectory analysis and structural interventions.

Main components
---------------

Models
    Core data structures used by the kernel.

MESO
    Regime landscape construction.

State Dynamics
    Defines how system states evolve over time inside an observation frame.

Navigation
    Trajectory and path evaluation.

MEVA
    Structural intervention simulation.

Stability
    Spectral stability operators for architecture analysis.

Architecture
    Stability landscape construction and architecture navigation tools.

NexahKernel
    Main kernel interface combining the system analysis pipeline.
"""

# Core data structures
from .models import (
    SystemArchitecture,
    StructuralGraph,
    RegimeLandscape,
    NavigationResult,
)

# Landscape construction
from .meso import build_regime_landscape

# State dynamics
from .state_dynamics import (
    ObservationFrame,
    StateDynamics,
)

# Navigation and intervention engines
from .navigation import NavigationEngine
from .meva import ActionEngine

# Stability operators
from .stability.spectral_stability import (
    spectral_stability_score,
    resilience_estimate,
    graph_metrics,
)

# Architecture stability landscape
from .stability.architecture_landscape import (
    build_architecture_landscape,
)

# Architecture navigation tools
from .navigation.architecture_navigation import (
    find_local_maxima,
    stability_gradient,
    build_navigation_graph,
    best_architecture,
    gradient_ascent_architecture_search,
)

# Kernel interface
from .nexah_kernel import NexahKernel


__all__ = [

    # Data structures
    "SystemArchitecture",
    "StructuralGraph",
    "RegimeLandscape",
    "NavigationResult",

    # Landscape construction
    "build_regime_landscape",

    # State dynamics
    "ObservationFrame",
    "StateDynamics",

    # Engines
    "NavigationEngine",
    "ActionEngine",

    # Stability operators
    "spectral_stability_score",
    "resilience_estimate",
    "graph_metrics",

    # Architecture stability
    "build_architecture_landscape",

    # Architecture navigation
    "find_local_maxima",
    "stability_gradient",
    "build_navigation_graph",
    "best_architecture",
    "gradient_ascent_architecture_search",

    # Kernel interface
    "NexahKernel",
]
