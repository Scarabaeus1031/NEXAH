# tools/resilience_architecture_evolver.py

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


BASE_SYSTEM = "APPLICATIONS/examples/energy_grid_control.json"
OUTPUT_PATH = "APPLICATIONS/examples/energy_grid_architecture_evolved.json"


# --------------------------------------------------
# IO
# --------------------------------------------------

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def write_temp(data):
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
    json.dump(data, tmp, indent=2)
    tmp.close()
    return tmp.name


# --------------------------------------------------
# scoring
# --------------------------------------------------

def score_system(data):
    temp = write_temp(data)

    try:
        report = analyze_system(temp)
        return report["resilience_score"], report
    finally:
        if os.path.exists(temp):
            os.remove(temp)


# --------------------------------------------------
# graph helpers
# --------------------------------------------------

def normalize_transitions(data):
    normalized = {}

    for state, targets in data["transitions"].items():
        if isinstance(targets, list):
            normalized[state] = list(targets)
        else:
            normalized[state] = [targets]

    data["transitions"] = normalized
    return data


def denormalize_transitions(data):
    result = {}

    for state, targets in data["transitions"].items():
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


# --------------------------------------------------
# mutation operators
# --------------------------------------------------

def mutate_add_edge(data):
    nodes = data["nodes"]

    if len(nodes) < 2:
        return data, "NOOP add_edge"

    source = random.choice(nodes)
    target = random.choice(nodes)

    if source == target:
        return data, "NOOP add_edge"

    current = set(data["transitions"].get(source, []))
    if target in current:
        return data, f"NOOP add_edge {source}->{target}"

    data["transitions"].setdefault(source, []).append(target)
    data = rebuild_edges(data)

    return data, f"ADD {source}->{target}"


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

    return data, f"REMOVE {source}->{target}"


def mutate_redirect_edge(data):
    nodes = data["nodes"]
    all_edges = []

    for source, targets in data["transitions"].items():
        for target in targets:
            all_edges.append((source, target))

    if not all_edges:
        return data, "NOOP redirect_edge"

    source, old_target = random.choice(all_edges)
    new_target = random.choice(nodes)

    if new_target == source:
        return data, "NOOP redirect_edge"

    if new_target in data["transitions"].get(source, []):
        return data, f"NOOP redirect_edge {source}->{new_target}"

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

    return data, f"REDIRECT {source}:{old_target}->{new_target}"


def mutate_recovery_bias(data):
    regimes = data.get("regimes", {})

    stable_states = [
        s for s, r in regimes.items()
        if str(r).upper() == "STABLE"
    ]

    unstable_states = [
        s for s, r in regimes.items()
        if str(r).upper() != "STABLE"
    ]

    if not stable_states or not unstable_states:
        return data, "NOOP recovery_bias"

    source = random.choice(unstable_states)
    target = random.choice(stable_states)

    if source == target:
        return data, "NOOP recovery_bias"

    if target in data["transitions"].get(source, []):
        return data, f"NOOP recovery_bias {source}->{target}"

    data["transitions"].setdefault(source, []).append(target)
    data = rebuild_edges(data)

    return data, f"RECOVERY {source}->{target}"


def mutate(data):
    candidate = copy.deepcopy(data)

    op = random.choice([
        mutate_add_edge,
        mutate_remove_edge,
        mutate_redirect_edge,
        mutate_recovery_bias,
    ])

    return op(candidate)


# --------------------------------------------------
# crossover
# --------------------------------------------------

def crossover(parent_a, parent_b):
    child = copy.deepcopy(parent_a)
    child = normalize_transitions(child)

    pb = normalize_transitions(copy.deepcopy(parent_b))

    for state in child["transitions"]:
        if random.random() < 0.5 and state in pb["transitions"]:
            child["transitions"][state] = list(pb["transitions"][state])

    child = rebuild_edges(child)

    return child


# --------------------------------------------------
# population init
# --------------------------------------------------

def initialize_population(base_data, population_size):
    population = []

    for _ in range(population_size):
        candidate = copy.deepcopy(base_data)

        mutation_count = random.randint(1, 4)

        for _ in range(mutation_count):
            candidate, _ = mutate(candidate)

        population.append(candidate)

    return population


# --------------------------------------------------
# evolution engine
# --------------------------------------------------

def evolve_architectures(
    base_system_path,
    generations=40,
    population_size=24,
    elite_size=6,
    mutation_rate=0.7
):
    base_data = load_json(base_system_path)
    base_data = normalize_transitions(base_data)
    base_data = rebuild_edges(base_data)

    base_score, base_report = score_system(base_data)

    best_system = copy.deepcopy(base_data)
    best_score = base_score
    best_report = base_report
    best_origin = "BASE SYSTEM"

    population = initialize_population(base_data, population_size)

    history = [{
        "generation": 0,
        "best_score": round(best_score, 3),
        "origin": best_origin,
    }]

    print("\nResilience Architecture Evolver")
    print("--------------------------------")
    print(f"Base score: {base_score:.3f}")

    for generation in range(1, generations + 1):
        scored = []

        for system in population:
            try:
                score, report = score_system(system)
            except Exception:
                continue

            scored.append((score, system, report))

            if score > best_score:
                best_score = score
                best_system = copy.deepcopy(system)
                best_report = report
                best_origin = f"generation {generation}"

                print(
                    f"generation={generation} new_best={best_score:.3f}"
                )

        if not scored:
            print(f"generation={generation} produced no valid systems")
            continue

        scored.sort(key=lambda x: x[0], reverse=True)

        elites = [copy.deepcopy(item[1]) for item in scored[:elite_size]]

        generation_best = scored[0][0]
        history.append({
            "generation": generation,
            "best_score": round(generation_best, 3),
            "origin": f"generation {generation}",
        })

        next_population = elites.copy()

        while len(next_population) < population_size:
            parent_a = random.choice(elites)
            parent_b = random.choice(elites)

            child = crossover(parent_a, parent_b)

            if random.random() < mutation_rate:
                child, _ = mutate(child)

            next_population.append(child)

        population = next_population

        print(
            f"generation={generation} population_best={generation_best:.3f} global_best={best_score:.3f}"
        )

    best_system = denormalize_transitions(best_system)
    best_system = rebuild_edges(best_system)

    return {
        "base_score": base_score,
        "best_score": best_score,
        "best_report": best_report,
        "best_system": best_system,
        "history": history,
        "best_origin": best_origin,
    }


# --------------------------------------------------
# reporting
# --------------------------------------------------

def print_summary(result):
    print("\nEvolution Summary")
    print("-----------------")
    print(f"Base score: {result['base_score']:.3f}")
    print(f"Best score: {result['best_score']:.3f}")
    print(f"Improvement: {result['best_score'] - result['base_score']:.3f}")
    print(f"Best origin: {result['best_origin']}")

    print("\nBest safe states:")
    for s in result["best_report"]["safe_states"]:
        print(" -", s)

    print("\nBest critical states:")
    for s in result["best_report"]["critical_states"]:
        print(" -", s)

    print("\nBest collapse states:")
    for s in result["best_report"]["collapse_states"]:
        print(" -", s)

    print("\nHistory:")
    for row in result["history"]:
        print(
            f" generation={row['generation']} "
            f"best_score={row['best_score']:.3f}"
        )


# --------------------------------------------------
# main
# --------------------------------------------------

if __name__ == "__main__":
    result = evolve_architectures(
        BASE_SYSTEM,
        generations=50,
        population_size=30,
        elite_size=8,
        mutation_rate=0.75
    )

    save_json(OUTPUT_PATH, result["best_system"])

    print_summary(result)

    print("\nSaved evolved architecture to:")
    print(OUTPUT_PATH)
