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

# ====================== URF Axial Space (v9.1) ======================
# 3D coordinate system + Matroschka mapping + Switch Grid integration

from .urf_axial_space.urf_axial_space_kernel import URFAxialSpaceKernel
from .urf_axial_space.switch_grid_mapper import SwitchGridMapper

# Add to public API
__all__.extend([
    "URFAxialSpaceKernel",
    "SwitchGridMapper",
])
# ====================== URF Axial Space Layer (v9.1) ======================
# 3D coordinate system for Matroschka, Spiral Coupling and Switch Grid

from .urf_axial_space.urf_axial_space_kernel import URFAxialSpaceKernel
from .urf_axial_space.switch_grid_mapper import SwitchGridMapper

# Add to public API
__all__.extend([
    "URFAxialSpaceKernel",
    "SwitchGridMapper",
])
