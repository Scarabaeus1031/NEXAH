"""
EXP_44N
ATLAS COMPRESSION VALIDATION

Goal
--------------------------------------------------
Validate whether the coherent-domain compression
from the Atlas State Graph into the Domain
Supergraph preserves large-scale structure.

Pipeline

State Graph
 ->
Coherent Domains
 ->
Domain Supergraph
 ->
Compression Validation

Author
--------------------------------------------------
NEXAH / FIELD NAVIGATION VALIDATION
"""

from pathlib import Path

import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# PATH DISCOVERY
# ============================================================

CURRENT = Path(__file__).resolve()

POWER_ROOT = next(
    p for p in CURRENT.parents
    if p.name == "power_systems"
)

STATE_GRAPH_PATH = (
    POWER_ROOT
    / "FIELD_NAVIGATION_VALIDATION"
    / "outputs"
    / "EXP_44D_ATLAS_STATE_GRAPH_RECONSTRUCTION"
)

SUPERGRAPH_PATH = (
    POWER_ROOT
    / "FIELD_NAVIGATION_VALIDATION"
    / "outputs"
    / "EXP_44L_DOMAIN_SUPERGRAPH_CONSTRUCTION"
    / "exp44l_domain_supergraph.graphml"
)

DOMAIN_TABLE_PATH = (
    POWER_ROOT
    / "FIELD_NAVIGATION_VALIDATION"
    / "outputs"
    / "EXP_44H2_COHERENT_DOMAIN_EXTRACTION"
    / "exp44h2_domain_table.csv"
)

OUTDIR = (
    POWER_ROOT
    / "FIELD_NAVIGATION_VALIDATION"
    / "outputs"
    / "EXP_44N_ATLAS_COMPRESSION_VALIDATION"
)

OUTDIR.mkdir(
    parents=True,
    exist_ok=True
)

print()
print("POWER_ROOT ->", POWER_ROOT)
print()


# ============================================================
# FIND STATE GRAPH
# ============================================================

graphml_files = list(
    STATE_GRAPH_PATH.glob("*.graphml")
)

if len(graphml_files) == 0:
    raise FileNotFoundError(
        "No graphml file found in EXP_44D output."
    )

STATE_GRAPH_FILE = graphml_files[0]

print("State Graph ->", STATE_GRAPH_FILE)
print("Exists      ->", STATE_GRAPH_FILE.exists())
print()

print("Supergraph  ->", SUPERGRAPH_PATH)
print("Exists      ->", SUPERGRAPH_PATH.exists())
print()

print("Domains     ->", DOMAIN_TABLE_PATH)
print("Exists      ->", DOMAIN_TABLE_PATH.exists())
print()


# ============================================================
# LOAD
# ============================================================

G_state = nx.read_graphml(
    STATE_GRAPH_FILE
)

G_super = nx.read_graphml(
    SUPERGRAPH_PATH
)

domains = pd.read_csv(
    DOMAIN_TABLE_PATH
)

print("State Nodes :", G_state.number_of_nodes())
print("State Edges :", G_state.number_of_edges())
print()

print("Super Nodes :", G_super.number_of_nodes())
print("Super Edges :", G_super.number_of_edges())
print()


# ============================================================
# BASIC METRICS
# ============================================================

state_nodes = G_state.number_of_nodes()
super_nodes = G_super.number_of_nodes()

state_edges = G_state.number_of_edges()
super_edges = G_super.number_of_edges()

compression_ratio = (
    state_nodes / super_nodes
)

edge_ratio = (
    state_edges / super_edges
)

state_density = nx.density(G_state)
super_density = nx.density(G_super)

state_components = nx.number_connected_components(
    G_state.to_undirected()
)

super_components = nx.number_connected_components(
    G_super.to_undirected()
)

avg_degree_state = np.mean(
    [d for _, d in G_state.degree()]
)

avg_degree_super = np.mean(
    [d for _, d in G_super.degree()]
)


# ============================================================
# DOMAIN METRICS
# ============================================================

largest_domain = domains["nodes"].max()

coherent_nodes = domains["nodes"].sum()

largest_share = (
    largest_domain /
    coherent_nodes
)

domain_count = len(domains)


# ============================================================
# SPECTRAL COMPARISON
# ============================================================

A_state = nx.to_numpy_array(
    G_state
)

A_super = nx.to_numpy_array(
    G_super,
    weight="weight"
)

eig_state = np.linalg.eigvals(A_state)
eig_super = np.linalg.eigvals(A_super)

spectral_radius_state = np.max(
    np.abs(eig_state)
)

spectral_radius_super = np.max(
    np.abs(eig_super)
)


# ============================================================
# SAVE METRICS
# ============================================================

metrics = pd.DataFrame([{
    "state_nodes": state_nodes,
    "super_nodes": super_nodes,
    "compression_ratio": compression_ratio,
    "state_edges": state_edges,
    "super_edges": super_edges,
    "edge_ratio": edge_ratio,
    "state_density": state_density,
    "super_density": super_density,
    "state_components": state_components,
    "super_components": super_components,
    "avg_degree_state": avg_degree_state,
    "avg_degree_super": avg_degree_super,
    "largest_domain": largest_domain,
    "largest_share": largest_share,
    "spectral_radius_state": spectral_radius_state,
    "spectral_radius_super": spectral_radius_super
}])

metrics.to_csv(
    OUTDIR / "exp44n_compression_metrics.csv",
    index=False
)


# ============================================================
# VISUAL 1
# ============================================================

plt.figure(figsize=(8,6))

plt.bar(
    ["State Graph", "Domain Supergraph"],
    [state_nodes, super_nodes]
)

plt.ylabel("Nodes")

plt.title(
    "EXP_44N Compression Summary"
)

plt.tight_layout()

plt.savefig(
    OUTDIR / "exp44n_compression_summary.png",
    dpi=300
)

plt.close()


# ============================================================
# VISUAL 2
# ============================================================

plt.figure(figsize=(8,6))

plt.hist(
    [d for _, d in G_state.degree()],
    bins=30,
    alpha=0.7,
    label="State Graph"
)

plt.hist(
    [d for _, d in G_super.degree()],
    bins=15,
    alpha=0.7,
    label="Supergraph"
)

plt.legend()

plt.title(
    "EXP_44N Degree Distribution Comparison"
)

plt.tight_layout()

plt.savefig(
    OUTDIR / "exp44n_degree_distribution_comparison.png",
    dpi=300
)

plt.close()


# ============================================================
# VISUAL 3
# ============================================================

plt.figure(figsize=(8,6))

plt.plot(
    np.sort(np.abs(eig_state))[::-1][:50],
    label="State Graph"
)

plt.plot(
    np.sort(np.abs(eig_super))[::-1],
    label="Supergraph"
)

plt.legend()

plt.title(
    "EXP_44N Spectral Comparison"
)

plt.tight_layout()

plt.savefig(
    OUTDIR / "exp44n_spectral_comparison.png",
    dpi=300
)

plt.close()


# ============================================================
# VISUAL 4
# ============================================================

plt.figure(figsize=(8,6))

plt.bar(
    domains["domain_id"].astype(str),
    domains["nodes"]
)

plt.title(
    "EXP_44N Domain Size Distribution"
)

plt.xlabel("Domain")
plt.ylabel("Nodes")

plt.tight_layout()

plt.savefig(
    OUTDIR / "exp44n_domain_size_distribution.png",
    dpi=300
)

plt.close()


# ============================================================
# REPORT
# ============================================================

report = f"""
EXP_44N ATLAS COMPRESSION VALIDATION
==================================================

State Nodes
-----------
{state_nodes}

Supergraph Nodes
----------------
{super_nodes}

Compression Ratio
-----------------
{compression_ratio:.2f}

State Edges
-----------
{state_edges}

Supergraph Edges
----------------
{super_edges}

Edge Compression Ratio
----------------------
{edge_ratio:.2f}

State Density
-------------
{state_density:.6f}

Supergraph Density
------------------
{super_density:.6f}

Largest Domain
--------------
{largest_domain}

Largest Domain Share
--------------------
{largest_share:.4f}

State Components
----------------
{state_components}

Supergraph Components
---------------------
{super_components}

Interpretation
--------------
This experiment evaluates whether
coherent-domain compression preserves
large-scale Atlas structure.

The Atlas was compressed from
{state_nodes} states into
{super_nodes} coherent domains.

Pipeline

State Graph
 ->
Coherent Domains
 ->
Domain Supergraph
 ->
Compression Validation
"""

print(report)

with open(
    OUTDIR / "exp44n_report.txt",
    "w"
) as f:
    f.write(report)

print()
print("EXP_44N complete.")
print()
