# APPLICATIONS/base_adapter.py

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class NexahAdapter(ABC):
    """
    Base interface for connecting external dynamical systems to NEXAH.

    Each adapter must translate a system state into the NEXAH regime landscape.
    """

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}

    # ------------------------------------------------------------------
    # Simulation control
    # ------------------------------------------------------------------

    @abstractmethod
    def reset(self) -> Any:
        """
        Reset the simulation and return the initial observation.
        """
        pass

    @abstractmethod
    def step(self, action: Any) -> Any:
        """
        Apply an action to the system and advance simulation one step.
        Returns new observation.
        """
        pass

    # ------------------------------------------------------------------
    # Observation
    # ------------------------------------------------------------------

    @abstractmethod
    def get_observation(self) -> Dict[str, Any]:
        """
        Return the current system state representation.

        Example:
        {
            "state_vector": [...],
            "graph": ...,
            "metadata": ...
        }
        """
        pass

    # ------------------------------------------------------------------
    # Regime detection
    # ------------------------------------------------------------------

    @abstractmethod
    def identify_regime(self, observation: Dict[str, Any]) -> Dict[str, Any]:
        """
        Identify the current regime within the regime landscape.

        Example:
        {
            "regime": "stable_left",
            "confidence": 0.92,
            "embedding": [...]
        }
        """
        pass

    # ------------------------------------------------------------------
    # Risk estimation
    # ------------------------------------------------------------------

    @abstractmethod
    def compute_risk(
        self,
        observation: Dict[str, Any],
        regime: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Estimate risk of transition to unstable regimes.

        Example:
        {
            "risk_score": 0.35,
            "collapse_probability": 0.02,
            "boundary_distance": 1.3
        }
        """
        pass

    # ------------------------------------------------------------------
    # Action interface
    # ------------------------------------------------------------------

    @abstractmethod
    def get_feasible_actions(self, observation: Dict[str, Any]) -> List[Any]:
        """
        Return list of feasible actions/interventions.
        """
        pass

    # ------------------------------------------------------------------
    # Reward / evaluation
    # ------------------------------------------------------------------

    @abstractmethod
    def compute_reward(
        self,
        prev_obs: Dict[str, Any],
        action: Any,
        new_obs: Dict[str, Any]
    ) -> float:
        """
        Evaluate navigation performance.

        Higher reward = better navigation.
        """
        pass
