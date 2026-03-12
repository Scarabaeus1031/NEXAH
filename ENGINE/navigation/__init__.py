"""
NEXAH Navigation Module
=======================

Navigation utilities for exploring regime landscapes and architecture
stability fields.

This module contains tools for

• regime navigation
• architecture stability exploration
• stability gradient analysis
• architecture search in stability landscapes
"""

from .navigation_engine import NavigationEngine

# Architecture navigation tools
from .architecture_navigation import (
    find_local_maxima,
    stability_gradient,
    build_navigation_graph,
    best_architecture,
    gradient_ascent_architecture_search,
)

__all__ = [
    "NavigationEngine",
    "find_local_maxima",
    "stability_gradient",
    "build_navigation_graph",
    "best_architecture",
    "gradient_ascent_architecture_search",
]
