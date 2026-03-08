# tools/system_evolver.py

import sys
import os
import json
import copy
import random
import tempfile

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from tools.resilience_analyzer import analyze_system


SYSTEM_PATH = "APPLICATIONS/examples/energy_grid_control.json"


def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


def write_temp_system(data):
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
    json.dump(data, tmp, indent=2)
    tmp.close()
    return tmp.name


def score_system(data):
    temp_path = write_temp_system(data)
    try:
        report = analyze_system(temp_path)
        return report["resilience_score"], report
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def normalize_transitions(data):
    transitions = data.get("transitions", {})
    normalized = {}

    for state, targets in transitions.items():
        if isinstance(targets, list):
            normalized[state] = list(targets)
        else:
            normalized[state] = [targets]

    data["transitions"] = normalized
    return data


def denormalize_transitions(data):
    transitions = data.get("transitions", {})
    result = {}

    for state, targets in transitions.items():
        if len(targets) == 1:
            result[state] = targets[0]
        else:
            result[state] = targets

    data["transitions"] = result
    return data


def ensure_edge_list_consistency(data):
    edges = []

    for source, targets in data["transitions"].items():
        for target in targets:
            edge = [source, target]
            if edge not in edges:
                edges.append(edge)

    data["edges"] = edges
    return data


def mutate_add_edge(data):
    nodes = list(data.get("nodes", []))
    if len(nodes) < 2:
        return data, "NOOP add_edge"

    source = random.choice(nodes)
    target = random.choice(nodes)

    if source == target:
        return data, "NOOP add_edge"

    current_targets = set(data["transitions"].get(source, []))
    if target in current_targets:
        return data, f"NOOP add_edge {source}->{target}"

    data["transitions"].setdefault(source, []).append(target)
    data = ensure_edge_list_consistency(data)

    return data, f"ADD edge {source} -> {target}"


def mutate_remove_edge(data):
    all_edges = []
    for source, targets in data["transitions"].items():
        for target in targets:
            all_edges.append((source, target))

    if not all_edges:
        return data, "NOOP remove_edge"

    source, target = random.choice(all_edges)

    # avoid removing the last outgoing edge of a node
    if len(data["transitions"].get(source, [])) <= 1:
        return data, f"NOOP remove_edge {source}->{target}"

    data["transitions"][source] = [
        t for t in data["transitions"][source]
        if t != target
    ]

    data = ensure_edge_list_consistency(data)

    return data, f"REMOVE edge {source} -> {target}"


def mutate_redirect_edge(data):
    nodes = list(data.get("nodes", []))
    all_edges = []

    for source, targets in data["transitions"].items():
        for target in targets:
            all_edges.append((source, target))

    if not all_edges or len(nodes) < 2:
        return data, "NOOP redirect_edge"

    source, old_target = random.choice(all_edges)
    new_target = random.choice(nodes)

    if new_target == source:
        return data, "NOOP redirect_edge"

    if new_target in data["transitions"].get(source, []):
        return data, f"NOOP redirect_edge {source}->{new_target}"

    if len(data["transitions"].get(source, [])) <= 1:
        data["transitions"][source] = [new_target]
    else:
        replaced = False
        new_targets = []
        for t in data["transitions"][source]:
            if t == old_target and not replaced:
                new_targets.append(new_target)
                replaced = True
            else:
                new_targets.append(t)
        data["transitions"][source] = new_targets

    data = ensure_edge_list_consistency(data)

    return data, f"REDIRECT edge {source}: {old_target} -> {new_target}"


def mutate_system(base_data):
    data = copy.deepcopy(base_data)

    mutation_fn = random.choice([
        mutate_add_edge,
        mutate_remove_edge,
        mutate_redirect_edge,
    ])

    mutated, description = mutation_fn(data)

    return mutated, description


def evolve_system(system_path, generations=200):
    base_data = load_json(system_path)
    base_data = normalize_transitions(base_data)
    base_data = ensure_edge_list_consistency(base_data)

    best_data = copy.deepcopy(base_data)
    best_score, best_report = score_system(best_data)
    best_action = "INITIAL SYSTEM"

    history = [(0, best_score, best_action)]

    for generation in range(1, generations + 1):
        candidate_data, action = mutate_system(best_data)

        try:
            candidate_score, candidate_report = score_system(candidate_data)
        except Exception:
            continue

        if candidate_score > best_score:
            best_data = copy.deepcopy(candidate_data)
            best_score = candidate_score
            best_report = candidate_report
            best_action = action
            history.append((generation, best_score, best_action))
            print(
                f"generation={generation} score={best_score:.3f} action={best_action}"
            )

    best_data = denormalize_transitions(best_data)
    best_data = ensure_edge_list_consistency(best_data)

    return {
        "best_data": best_data,
        "best_score": best_score,
        "best_report": best_report,
        "best_action": best_action,
        "history": history,
    }


def save_system(data, output_path):
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)


def print_summary(result):
    print("\nNEXAH System Evolver")
    print("-" * 40)
    print("Best score:", round(result["best_score"], 3))
    print("Best action:", result["best_action"])

    print("\nSafe states:")
    for s in result["best_report"]["safe_states"]:
        print(" -", s)

    print("\nCritical states:")
    for s in result["best_report"]["critical_states"]:
        print(" -", s)

    print("\nCollapse states:")
    for s in result["best_report"]["collapse_states"]:
        print(" -", s)


if __name__ == "__main__":
    result = evolve_system(SYSTEM_PATH, generations=300)

    print_summary(result)

    output_path = "APPLICATIONS/examples/energy_grid_evolved.json"
    save_system(result["best_data"], output_path)

    print("\nSaved evolved system to:")
    print(output_path)
