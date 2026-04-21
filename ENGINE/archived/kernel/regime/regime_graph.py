class RegimeGraph:

    """
    Graph of regimes and transitions between them.
    """

    def __init__(self):

        self.regimes = set()
        self.transitions = {}


    def add_regime(self, regime):

        self.regimes.add(regime)


    def add_transition(self, from_regime, to_regime):

        if from_regime not in self.transitions:
            self.transitions[from_regime] = []

        self.transitions[from_regime].append(to_regime)


    def get_transitions(self, regime):

        return self.transitions.get(regime, [])
