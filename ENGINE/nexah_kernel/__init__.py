"""
NEXAH Kernel Package
====================

Core navigation kernel for the NEXAH framework.

This package provides the minimal system navigation engine
used to analyze and intervene in complex dynamical systems.

Main components:

Models
    Core data structures used by the kernel.

Meso
    Regime landscape construction.

Navigation
    Path and trajectory evaluation.

MEVA
    Structural intervention simulation.

NexahKernel
    Main kernel interface combining the system analysis pipeline.
"""

from .models import (
    SystemArchitecture,
    StructuralGraph,
    RegimeLandscape,
    NavigationResult,
)

from .meso import build_regime_landscape

from .navigation import NavigationEngine

from .meva import ActionEngine

from .nexah_kernel import NexahKernel


__all__ = [
    "SystemArchitecture",
    "StructuralGraph",
    "RegimeLandscape",
    "NavigationResult",
    "build_regime_landscape",
    "NavigationEngine",
    "ActionEngine",
    "NexahKernel",
]
