"""
URF Axial Space – Public API

Provides 3D coordinate mapping for Matroschka structures,
Spiral Coupling and Switch Layer dynamics.
"""

# Korrigierter Import – Dateiname ist urf_axial_space_kernel.py
from .urf_axial_space_kernel import URFAxialSpaceKernel
from .switch_grid_mapper import SwitchGridMapper

__all__ = ["URFAxialSpaceKernel", "SwitchGridMapper"]

__version__ = "0.1"
