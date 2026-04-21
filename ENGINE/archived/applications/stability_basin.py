class StabilityBasin:
    """
    Computes basin structure based on distance to stable states.

    Uses RiskGeometry distance values to classify system regimes.
    """

    def __init__(self, distance_map):
        self.distance_map = distance_map

    def classify(self):
        """
        Classify nodes into stability regimes.
        """

        regimes = {
            "stable": [],
            "stress": [],
            "failure": [],
        }

        for state, dist in self.distance_map.items():

            if dist == 0:
                regimes["stable"].append(state)

            elif dist <= 2:
                regimes["stress"].append(state)

            else:
                regimes["failure"].append(state)

        return regimes
