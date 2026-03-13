import numpy as np
from ..base_adapter import NexahAdapter


class KuramotoAdapter(NexahAdapter):

    def __init__(self, oscillators=10):

        self.oscillators = oscillators

        self.states_list = [
            "desync",
            "partial_sync",
            "cluster_sync",
            "global_sync"
        ]

    def states(self):
        return self.states_list

    def transitions(self):

        return {
            "desync": ["partial_sync"],
            "partial_sync": ["cluster_sync", "desync"],
            "cluster_sync": ["global_sync", "partial_sync"],
            "global_sync": ["cluster_sync"]
        }

    def regimes(self):

        return {
            "desync": "UNSTABLE",
            "partial_sync": "TRANSITION",
            "cluster_sync": "COHERENT",
            "global_sync": "STABLE"
        }

    def initial_state(self):
        return "desync"

    def metadata(self):
        return {
            "system": "Kuramoto Oscillators",
            "oscillators": self.oscillators
        }
