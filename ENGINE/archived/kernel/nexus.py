"""
NEXUS — Multi-System Integration Layer

The NEXUS layer connects multiple architectures and
enables cross-system analysis.

It allows NEXAH to compare and combine systems
across different architecture spaces.
"""

class NexusLayer:

    def __init__(self):

        self.systems = []
        self.links = []
        self.shared_states = {}

    # --------------------------------------------------

    def add_system(self, system):

        """
        Register a system in the nexus.
        """

        self.systems.append(system)

    # --------------------------------------------------

    def connect_systems(self, system_a, system_b, relation):

        """
        Create a connection between systems.
        """

        link = {
            "system_a": system_a,
            "system_b": system_b,
            "relation": relation
        }

        self.links.append(link)

    # --------------------------------------------------

    def get_system_network(self):

        """
        Return the integrated system network.
        """

        return {
            "systems": self.systems,
            "links": self.links
        }

    # --------------------------------------------------

    def compare_systems(self):

        """
        Compare structural properties across systems.
        """

        comparison = []

        for system in self.systems:

            comparison.append({
                "nodes": len(system.get("nodes", [])),
                "edges": len(system.get("edges", []))
            })

        return comparison
