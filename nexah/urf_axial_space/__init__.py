"""
NEXAH Public API

This module exposes the core structural components and the new URF Axial Space layer.
"""

# --- Core algebraic structures ---
from ENGINE.core.poset import FinitePoset as Poset
from ENGINE.core.lattice import LatticeOps as Lattice

# --- Operators ---
from ENGINE.core.closure_operator import ClosureOperator
from ENGINE.core.interior_operator import InteriorOperator
from ENGINE.core.monotone_operator import MonotoneOperator
from ENGINE.core.frame_operator import FrameOperator
from ENGINE.core.regime_operator import RegimeOperator

# --- High-level Engine Interface ---
class Engine:
    def __init__(self):
        self.Poset = Poset
        self.Lattice = Lattice

    def create_poset(self, elements, order):
        return self.Poset(elements, order)

    def create_lattice(self, elements, order):
        return self.Lattice(elements, order)


# ====================== URF Axial Space Layer (v9.1) ======================
# 3D coordinate system for Matroschka, Spiral Coupling and Switch Grid

from .urf_axial_space.urf_axial_space_kernel import URFAxialSpaceKernel
from .urf_axial_space.switch_grid_mapper import SwitchGridMapper


# --- Public API export list ---
__all__ = [
    "Poset",
    "Lattice",
    "ClosureOperator",
    "InteriorOperator",
    "MonotoneOperator",
    "FrameOperator",
    "RegimeOperator",
    "Engine",
    "URFAxialSpaceKernel",
    "SwitchGridMapper",
]

__version__ = "1.1"
