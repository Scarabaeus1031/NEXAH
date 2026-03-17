class Engine:
    """
    High-level interface for the NEXAH framework.

    Provides simplified access to the core structural
    analysis components.
    """

    def __init__(self):
        from ENGINE.core.poset import FinitePoset
        from ENGINE.core.lattice import LatticeOps

        self.Poset = FinitePoset
        self.Lattice = LatticeOps

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
