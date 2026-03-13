"""
NEXAH Adapter Demo Runner

This script demonstrates how external system adapters can be connected
to the NEXAH framework.

It loads several example adapters and prints their structural state graphs.
"""

from examples.lorenz_adapter import LorenzAdapter
from examples.kuramoto_adapter import KuramotoAdapter
from examples.powergrid_adapter import PowerGridAdapter
from examples.supply_chain_adapter import SupplyChainAdapter
from examples.traffic_adapter import TrafficAdapter


def run_adapter(adapter):

    print("\n==============================")
    print("SYSTEM:", adapter.metadata().get("system", "Unknown"))
    print("==============================")

    graph = adapter.to_state_graph()

    print("\nStates:")
    for s in graph["states"]:
        print(" ", s)

    print("\nTransitions:")
    for k, v in graph["transitions"].items():
        print(" ", k, "→", v)

    if graph["regimes"]:
        print("\nRegimes:")
        for k, v in graph["regimes"].items():
            print(" ", k, ":", v)

    if graph["risk_targets"]:
        print("\nRisk Targets:", graph["risk_targets"])

    if graph["actions"]:
        print("\nPossible Actions:", graph["actions"])

    print("\nMetadata:")
    print(graph["metadata"])


def main():

    adapters = [
        LorenzAdapter(),
        KuramotoAdapter(),
        PowerGridAdapter(),
        SupplyChainAdapter(),
        TrafficAdapter(),
    ]

    for adapter in adapters:
        run_adapter(adapter)


if __name__ == "__main__":
    main()
