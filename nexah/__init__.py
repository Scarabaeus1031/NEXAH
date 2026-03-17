"""
NEXAH Public API

This module exposes the core structural components of the NEXAH Engine
for external users.

Example:

    import nexah

    engine = nexah.Engine()
    poset = engine.create_poset(elements, order)
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
    """
    High-level interface for the NEXAH framework.

    Provides simplified access to the core structural
    components of the NEXAH Engine.
    """

    def __init__(self):
        self.Poset = Poset
        self.Lattice = Lattice

    def create_poset(self, elements, order):
        """
        Create a finite poset structure.
        """
        return self.Poset(elements, order)

    def create_lattice(self, elements, order):
        """
        Create a lattice structure.
        """
        return self.Lattice(elements, order)


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
]
