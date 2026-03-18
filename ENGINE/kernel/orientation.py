class ObservationFrame:
    """
    Defines the observation frame for the discovery engine.
    Determines how architectures are interpreted.
    """

    def __init__(self, dimensions=None, metrics=None):

        self.dimensions = dimensions or []
        self.metrics = metrics or []

    def describe(self):

        return {
            "dimensions": self.dimensions,
            "metrics": self.metrics,
        }
