# ENGINE/runtime/simulation_engine.py

from FRAMEWORK.MESO.risk_geometry import compute_risk
from FRAMEWORK.ARCHY.regime_mapper import detect_regime
from FRAMEWORK.NEXAH.navigation_policy import select_actions
from FRAMEWORK.MEVA.execution_engine import execute_actions


class NexahSimulationEngine:

    def __init__(self, system, policy=None):

        self.system = system
        self.policy = policy

        self.state = system.initial_state()
        self.history = []

    def step(self):

        # 1 risk geometry
        risk = compute_risk(self.system, self.state)

        # 2 regime detection
        regime = detect_regime(self.system, self.state, risk)

        # 3 policy decision
        if self.policy:
            actions = self.policy(self.system, self.state, risk, regime)
        else:
            actions = select_actions(self.system, self.state, risk, regime)

        # 4 execute actions
        new_state = execute_actions(self.system, self.state, actions)

        # 5 update state
        self.state = new_state

        # 6 log trace
        self.history.append({
            "state": self.state,
            "risk": risk,
            "regime": regime,
            "actions": actions
        })

        return self.state, regime

    def run(self, steps=20):

        results = []

        for step in range(steps):

            state, regime = self.step()

            results.append({
                "step": step,
                "state": state,
                "regime": regime
            })

            if regime == "collapse":
                break

        return results

    def reset(self):

        self.state = self.system.initial_state()
        self.history = []
