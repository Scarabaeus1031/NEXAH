"""
Navigation Layer for the NEXAH Kernel.

This module exposes the navigation components responsible for
exploring regime graphs and planning structural interventions.
"""

from .navigator import Navigator
from .intervention_planner import InterventionPlanner

# Kernel-level alias
NavigationEngine = Navigator

__all__ = [
    "Navigator",
    "InterventionPlanner",
    "NavigationEngine",
]
