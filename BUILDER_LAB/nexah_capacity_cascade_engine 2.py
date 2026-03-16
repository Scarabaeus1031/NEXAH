# ==========================================================
# NEXAH CAPACITY CASCADE ENGINE (v3)
# Realistic load/capacity/stress cascade simulation
# ==========================================================

import os
import json
import argparse
import random
from typing import Dict, Any, List, Tuple


# ----------------------------------------------------------
# PATHS
# ----------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


# ----------------------------------------------------------
# NETWORK FILE FORMAT (planetary_network.json)
# ----------------------------------------------------------
# {
#   "nodes": {
#     "SAT_GNSS": {"layer":"SPACE","capacity":100,"base_load":20,"shock_load":0,"fail_threshold":1.0,"fail_prob_above":0.35},
#     "IXP_NYC":  {"layer":"DIGITAL","capacity":100,"base_load":40},
#     ...
#   },
#   "edges": [
#     {"src":"SAT_GNSS","tgt":"IXP_NYC","transfer":0.45},
#     {"src":"IXP_NYC","tgt":"FIN_NYC","transfer":0.35},
#     ...
#   ]
# }
#
# Minimal defaults:
# - capacity default: 100
# - base_load default: 30
# - shock_load default: 0
# - fail_threshold default: 1.0
# - fail_prob_above default: 0.25
# - transfer default: 0.25


# ----------------------------------------------------------
# LOAD NETWORK
# ----------------------------------------------------------

def load_network(path: str) -> Dict[str, Any]:

    if not os.path.exists(path):
        raise FileNotFoundError(f"Network JSON not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if "nodes" not in data or "edges" not in data:
        raise ValueError("Network JSON must contain 'nodes' and 'edges'.")

    # ---- HANDLE LIST FORMAT ----

    if isinstance(data["nodes"], list):

        node_dict = {}

        for n in data["nodes"]:
            node_id = n.get("id")

            if not node_id:
                raise ValueError("Node missing 'id' field")

            node_dict[node_id] = n

        data["nodes"] = node_dict

    # ---- DEFAULTS ----

    for node_id, nd in data["nodes"].items():

        nd.setdefault("layer", "GENERIC")
        nd.setdefault("capacity", 100.0)
        nd.setdefault("base_load", 30.0)
        nd.setdefault("shock_load", 0.0)
        nd.setdefault("fail_threshold", 1.0)
        nd.setdefault("fail_prob_above", 0.25)
        nd.setdefault("recovery_rate", 0.0)

    for e in data["edges"]:
        e.setdefault("transfer", 0.25)

    return data


# ----------------------------------------------------------
# HELPERS
# ----------------------------------------------------------

def incoming_edges(edges: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    inc: Dict[str, List[Dict[str, Any]]] = {}
    for e in edges:
        tgt = e["tgt"]
        inc.setdefault(tgt, []).append(e)
    return inc

def outgoing_edges(edges: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    out: Dict[str, List[Dict[str, Any]]] = {}
    for e in edges:
        src = e["src"]
        out.setdefault(src, []).append(e)
    return out


# ----------------------------------------------------------
# SIMULATION CORE
# ----------------------------------------------------------

def simulate_capacity_cascade(
    network: Dict[str, Any],
    start: str,
    steps: int = 8,
    seed: int = 42,
    shock: float = 60.0,
    verbose: bool = True
) -> List[Dict[str, Any]]:
    """
    start fails at step 0 (forced), and its load is redistributed downstream.
    Each step:
      1) compute loads = base_load + propagated + shock_load
      2) compute stress = load / capacity
      3) fail nodes with stress >= threshold (or probabilistic above threshold)
      4) redistribute "lost capacity" (or load) via outgoing edges as extra load
    Returns timeline: list of step snapshots
    """

    random.seed(seed)

    nodes: Dict[str, Dict[str, Any]] = network["nodes"]
    edges: List[Dict[str, Any]] = network["edges"]

    out = outgoing_edges(edges)

    # State tracking
    failed: Dict[str, bool] = {nid: False for nid in nodes.keys()}

    # Per-step load contributions (propagated load)
    propagated_load: Dict[str, float] = {nid: 0.0 for nid in nodes.keys()}

    # Optional per-node shock accumulator
    shock_load: Dict[str, float] = {nid: float(nodes[nid].get("shock_load", 0.0)) for nid in nodes.keys()}

    # Force initial failure
    if start not in nodes:
        raise ValueError(f"Start node not in network: {start}")

    failed[start] = True
    shock_load[start] += shock  # make it "heavily stressed" for record-keeping

    timeline: List[Dict[str, Any]] = []

    for step in range(steps + 1):
        # --- compute total load + stress
        snapshot_nodes: Dict[str, Dict[str, Any]] = {}

        for nid, nd in nodes.items():
            cap = float(nd.get("capacity", 100.0))
            base = float(nd.get("base_load", 30.0))
            total = base + propagated_load[nid] + shock_load[nid]

            stress = total / cap if cap > 0 else 999.0

            snapshot_nodes[nid] = {
                "layer": nd.get("layer", "GENERIC"),
                "capacity": cap,
                "base_load": base,
                "propagated_load": propagated_load[nid],
                "shock_load": shock_load[nid],
                "total_load": total,
                "stress": stress,
                "failed": bool(failed[nid]),
            }

        # --- determine new failures for this step
        newly_failed: List[str] = []

        for nid, nd in nodes.items():
            if failed[nid]:
                continue

            stress = snapshot_nodes[nid]["stress"]
            threshold = float(nd.get("fail_threshold", 1.0))
            prob_above = float(nd.get("fail_prob_above", 0.25))

            if stress >= threshold:
                # if stress is far above threshold, force failure
                if stress >= threshold * 1.15:
                    failed[nid] = True
                    newly_failed.append(nid)
                else:
                    # probabilistic failure close to threshold
                    if random.random() < prob_above:
                        failed[nid] = True
                        newly_failed.append(nid)

        # --- propagate from failed nodes
        # Idea: a failed node "dumps" a fraction of its total load to its targets
        # (you can interpret this as demand shifting / rerouting / dependency shock)
        new_propagated: Dict[str, float] = {nid: 0.0 for nid in nodes.keys()}

        for nid, is_failed in failed.items():
            if not is_failed:
                continue

            dumped = snapshot_nodes[nid]["total_load"]

            for e in out.get(nid, []):
                tgt = e["tgt"]
                transfer = float(e.get("transfer", 0.25))

                # If target already failed, still add load (optional). We add anyway for trace.
                new_propagated[tgt] += dumped * transfer

        # --- optional recovery (very simple)
        # recovery_rate reduces propagated load & shock load gradually
        for nid, nd in nodes.items():
            rr = float(nd.get("recovery_rate", 0.0))
            if rr > 0 and not failed[nid]:
                shock_load[nid] = max(0.0, shock_load[nid] * (1.0 - rr))
                propagated_load[nid] = max(0.0, propagated_load[nid] * (1.0 - rr))

        # Next step loads add (accumulate) or replace?
        # We choose ACCUMULATE for realistic cascade pressure:
        for nid in nodes.keys():
            propagated_load[nid] += new_propagated[nid]

        snapshot = {
            "step": step,
            "start": start,
            "failed_nodes": sorted([nid for nid in nodes.keys() if failed[nid]]),
            "newly_failed": newly_failed,
            "nodes": snapshot_nodes,
        }
        timeline.append(snapshot)

        if verbose:
            failed_set = set(snapshot["failed_nodes"])
            print(f"\nSTEP {step}")
            print("FAILED:", snapshot["failed_nodes"])
            if newly_failed:
                print("NEW FAILURES:", newly_failed)

        # If nothing changes anymore, we can stop early
        if step > 0 and not newly_failed and all(v == 0.0 for v in new_propagated.values()):
            if verbose:
                print("\nNo further propagation/new failures — stopping early.")
            break

    return timeline


# ----------------------------------------------------------
# CLI
# ----------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="NEXAH Capacity Cascade Engine (v3)")
    parser.add_argument("--network", default=os.path.join(DATA_DIR, "planetary_network.json"),
                        help="Path to network JSON")
    parser.add_argument("--start", required=True, help="Node ID to fail at step 0")
    parser.add_argument("--steps", type=int, default=8)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--shock", type=float, default=60.0, help="Extra shock_load added to start node")
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument("--save_timeline", default="",
                        help="If set, writes timeline JSON to this path (e.g. BUILDER_LAB/data/last_run_timeline.json)")
    args = parser.parse_args()

    network = load_network(args.network)

    timeline = simulate_capacity_cascade(
        network=network,
        start=args.start,
        steps=args.steps,
        seed=args.seed,
        shock=args.shock,
        verbose=(not args.quiet),
    )

    if args.save_timeline:
        out_path = args.save_timeline
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(timeline, f, indent=2)
        print("\nSaved timeline:", out_path)


if __name__ == "__main__":
    main()
