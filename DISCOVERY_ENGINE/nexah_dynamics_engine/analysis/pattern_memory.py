# DISCOVERY_ENGINE/nexah_dynamics_engine/analysis/pattern_memory.py

import json
import os
import numpy as np


# --------------------------------------------------
# CONFIG
# --------------------------------------------------

MEMORY_FILE = "pattern_memory.json"
SIMILARITY_THRESHOLD = 0.90


# --------------------------------------------------
# CORE MEMORY CLASS
# --------------------------------------------------

class PatternMemory:
    def __init__(self, filepath=MEMORY_FILE):
        self.filepath = filepath
        self.memory = []
        self.load()

    def load(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, "r") as f:
                self.memory = json.load(f)
        else:
            self.memory = []

    def save(self):
        with open(self.filepath, "w") as f:
            json.dump(self.memory, f, indent=2)

    def add_pattern(self, signature, classification, label=None):
        entry = {
            "signature": signature,
            "type": classification["type"],
            "confidence": classification["confidence"],
            "label": label
        }
        self.memory.append(entry)
        self.save()

    def list_patterns(self):
        for i, p in enumerate(self.memory):
            print(f"[{i}] {p['type']} (conf={p['confidence']:.3f}) label={p['label']}")


# --------------------------------------------------
# SIGNATURE VECTOR (same as before!)
# --------------------------------------------------

def signature_to_vector(signature):
    vec = []

    for k in sorted(signature["degree_dist"].keys()):
        vec.append(signature["degree_dist"][k])

    vec.append(signature["avg_loop"])
    vec.append(signature["std_loop"])
    vec.append(signature["avg_channel"])
    vec.append(signature["std_channel"])

    for k in sorted(signature["angle_profile"].keys()):
        vec.append(signature["angle_profile"][k])

    return np.array(vec)


# --------------------------------------------------
# SIMILARITY
# --------------------------------------------------

def cosine_similarity(sig1, sig2):
    v1 = signature_to_vector(sig1)
    v2 = signature_to_vector(sig2)

    v1 = v1 / (np.linalg.norm(v1) + 1e-8)
    v2 = v2 / (np.linalg.norm(v2) + 1e-8)

    return float(np.dot(v1, v2))


# --------------------------------------------------
# SEARCH / MATCH
# --------------------------------------------------

def find_similar(memory, new_signature, threshold=SIMILARITY_THRESHOLD):
    results = []

    for i, entry in enumerate(memory):
        sim = cosine_similarity(new_signature, entry["signature"])

        if sim >= threshold:
            results.append({
                "index": i,
                "similarity": sim,
                "type": entry["type"],
                "label": entry.get("label")
            })

    return sorted(results, key=lambda x: -x["similarity"])


def best_match(memory, new_signature):
    best = None
    best_sim = -1

    for i, entry in enumerate(memory):
        sim = cosine_similarity(new_signature, entry["signature"])

        if sim > best_sim:
            best_sim = sim
            best = {
                "index": i,
                "similarity": sim,
                "type": entry["type"],
                "label": entry.get("label")
            }

    return best


# --------------------------------------------------
# INTERFACE FUNCTIONS
# --------------------------------------------------

def store_pattern(memory, signature, classification, label=None):
    memory.add_pattern(signature, classification, label)


def query_pattern(memory, signature):
    match = best_match(memory.memory, signature)

    print("\n--- BEST MATCH ---")
    if match:
        print(f"Type: {match['type']}")
        print(f"Similarity: {match['similarity']:.4f}")
        print(f"Label: {match['label']}")
    else:
        print("No match found")

    return match


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":
    print("Pattern Memory Ready")
