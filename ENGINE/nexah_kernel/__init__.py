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

Navigation
    Trajectory and path evaluation.

MEVA
    Structural intervention simulation.

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

# Navigation and intervention engines
from .navigation import NavigationEngine
from .meva import ActionEngine

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

    # Engines
    "NavigationEngine",
    "ActionEngine",

    # Kernel interface
    "NexahKernel",
]
