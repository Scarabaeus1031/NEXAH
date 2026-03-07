import numpy as np
import matplotlib.pyplot as plt
import networkx as nx


class BasinTransitionGraph:
    """
    Build a transition graph between attraction basins.

    Two basins are connected if they touch along the segmentation boundary.
    """

    def __init__(self, basin_map, maxima):
        self.basin_map = basin_map
        self.maxima = maxima

    def compute(self):
        """
        Detect adjacency between basins.
        """

        ny, nx_ = self.basin_map.shape
        edges = set()

        for i in range(ny - 1):
            for j in range(nx_ - 1):

                a = self.basin_map[i, j]
                b = self.basin_map[i + 1, j]
                c
