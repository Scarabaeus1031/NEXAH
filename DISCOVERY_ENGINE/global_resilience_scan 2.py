# tools/global_resilience_scan.py

import sys
import os
import json
import copy
import random
import tempfile

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

import matplotlib.pyplot as plt

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


def rebuild_edges(data):
    edges = []

    for source, targets in data["transitions"].items():
        for target in targets:
            edge = [source, target]
            if edge not in edges:
                edges.append(edge)

    data["edges"] = edges
    return data


def mutate_add_edge(data):
    nodes = data.get("nodes", [])
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
    data = rebuild_edges(data)

    return data, f"ADD edge {source} -> {target}"


def mutate_remove_edge(data):
    all_edges = []

    for source, targets in data["transitions"].items():
        for target in targets:
            all_edges.append((source, target))

    if not all_edges:
        return data, "NOOP remove_edge"

    source, target = random.choice(all_edges)

    if len(data["transitions"].get(source, [])) <= 1:
        return data, f"NOOP remove_edge {source}->{target}"

    data["transitions"][source] = [
        t for t in data["transitions"][source]
        if t != target
    ]

    data = rebuild_edges(data)

    return data, f"REMOVE edge {source} -> {target}"


def mutate_redirect_edge(data):
    nodes = data.get("nodes", [])
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

    data = rebuild_edges(data)

    return data, f"REDIRECT edge {source}: {old_target} -> {new_target}"


def mutate_system(base_data):
    data = copy.deepcopy(base_data)

    mutation_fn = random.choice([
        mutate_add_edge,
        mutate_remove_edge,
        mutate_redirect_edge
    ])

    mutated, description = mutation_fn(data)

    return mutated, description


def run_scan(system_path, num_variants=500):
    base_data = load_json(system_path)
    base_data = normalize_transitions(base_data)
    base_data = rebuild_edges(base_data)

    base_score, base_report = score_system(copy.deepcopy(base_data))

    results = []
    best_score = base_score
    best_report = base_report
    best_data = copy.deepcopy(base_data)
    best_action = "BASE SYSTEM"

    results.append({
        "score": base_score,
        "action": "BASE SYSTEM"
    })

    for i in range(num_variants):
        candidate_data, action = mutate_system(copy.deepcopy(base_data))

        try:
            candidate_score, candidate_report = score_system(candidate_data)
        except Exception:
            continue

        results.append({
            "score": candidate_score,
            "action": action
        })

        if candidate_score > best_score:
            best_score = candidate_score
            best_report = candidate_report
            best_data = copy.deepcopy(candidate_data)
            best_action = action

        if (i + 1) % 50 == 0:
            print(f"scanned={i + 1} best_score={best_score:.3f}")

    best_data = denormalize_transitions(best_data)
    best_data = rebuild_edges(best_data)

    return {
        "base_score": base_score,
        "best_score": best_score,
        "best_action": best_action,
        "best_report": best_report,
        "best_data": best_data,
        "results": results,
    }


def visualize(scan_result):
    scores = [r["score"] for r in scan_result["results"]]
    best_score = scan_result["best_score"]
    base_score = scan_result["base_score"]

    plt.figure(figsize=(9, 6))

    plt.hist(scores, bins=25)

    plt.axvline(base_score, linestyle="--", label=f"Base score = {base_score:.3f}")
    plt.axvline(best_score, linestyle="-", label=f"Best score = {best_score:.3f}")

    plt.xlabel("Resilience Score")
    plt.ylabel("Number of Variants")
    plt.title("Global Resilience Scan")

    plt.legend()
    plt.show()


def print_summary(scan_result):
    print("\nNEXAH Global Resilience Scan")
    print("-" * 40)
    print("Base score:", round(scan_result["base_score"], 3))
    print("Best score:", round(scan_result["best_score"], 3))
    print("Best action:", scan_result["best_action"])

    delta = scan_result["best_score"] - scan_result["base_score"]
    print("Improvement:", round(delta, 3))

    print("\nBest safe states:")
    for s in scan_result["best_report"]["safe_states"]:
        print(" -", s)

    print("\nBest critical states:")
    for s in scan_result["best_report"]["critical_states"]:
        print(" -", s)

    print("\nBest collapse states:")
    for s in scan_result["best_report"]["collapse_states"]:
        print(" -", s)


def save_best_system(scan_result, output_path):
    with open(output_path, "w") as f:
        json.dump(scan_result["best_data"], f, indent=2)


if __name__ == "__main__":
    scan_result = run_scan(SYSTEM_PATH, num_variants=800)

    print_summary(scan_result)

    output_path = "APPLICATIONS/examples/energy_grid_global_best.json"
    save_best_system(scan_result, output_path)

    print("\nSaved best system to:")
    print(output_path)

    visualize(scan_result)
