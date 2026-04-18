"""
NEXAH Core Package

Lightweight navigation + field layer for system dynamics.
"""

# Optional: expose navigator
from .navigation.navigator import NexahNavigator

__all__ = [
    "NexahNavigator",
]

__version__ = "2.0"
