from APPLICATIONS.adapters.base_adapter import NexahAdapter
from analysis.signature_to_graph import build_state_graph


class PhaseSpaceAdapter(NexahAdapter):

    def __init__(self, results):
        super().__init__()
        self.graph = build_state_graph(results)

    def states(self):
        return self.graph["states"]

    def transitions(self):
        return self.graph["transitions"]

    def regimes(self):
        return {s: s for s in self.graph["states"]}

    def metadata(self):
        return {
            "system": "phase_space_simulation",
            "type": "derived_from_nexah_engine"
        }
