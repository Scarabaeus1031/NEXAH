"""
NEXAH — Minimal Kernel Package (v0.7)

This package exposes the core NEXAH kernel:

- NEXAH (main class)
- CLI interface

All experimental modules have been moved to BUILDER_LAB.
"""

from .core import NEXAH

__all__ = ["NEXAH"]
