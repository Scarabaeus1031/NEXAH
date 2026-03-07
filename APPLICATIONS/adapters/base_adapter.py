
class NexahAdapter:
    """
    Base adapter interface for connecting external systems to the NEXAH framework.

    Implementations translate external simulator states into a NEXAH-compatible
    finite state graph representation.
    """

    def states(self):
        """
        Return the list or set of system states.
        """
        raise NotImplementedError("states() must be implemented by the adapter.")

    def transitions(self):
        """
        Return system transitions.

        Expected format:
        {
            "state_a": ["state_b", "state_c"],
            "state_b": ["state_c"]
        }
        """
        raise NotImplementedError("transitions() must be implemented by the adapter.")

    def regimes(self):
        """
        Optional regime classification for states.

        Example:
        {
            "stable": "STABLE",
            "stress": "STRESS",
            "failure": "FAILURE"
        }
        """
        return None

    def risk_targets(self):
        """
        Optional list of states representing failure or collapse conditions.
        """
        return []

    def actions(self):
        """
        Optional list of control actions that policies may apply.
        """
        return []

    def metadata(self):
        """
        Optional metadata about the system model.
        """
        return {}
