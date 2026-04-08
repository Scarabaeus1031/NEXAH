# NEXAH Layer

This directory is the **conceptual and lightweight package layer** of
the NEXAH framework.

It does not replace the full `ENGINE/` or `FRAMEWORK/` directories.

Instead, it serves as a more focused layer where the central NEXAH ideas
become readable as:

-   package entry points
-   field abstractions
-   identity documents
-   navigation primitives
-   **channel and transport structures (v8)**
-   **switch and control dynamics (v9)**
-   operational transition notes
-   featured visuals

In that sense, `nexah/` is the place where the framework becomes more
directly legible as **NEXAH itself**.

------------------------------------------------------------------------

## What this directory is

The `nexah/` layer acts as a bridge between:

``` text
ENGINE
    → computational core

FRAMEWORK
    → architecture and stack logic

NEXAH
    → conceptual, operational, and navigational layer
```

This means the directory has a double role: 1. it provides a lightweight
public-facing package surface\
2. it gathers the emerging conceptual, geometric, and dynamical language
of NEXAH

------------------------------------------------------------------------

## Position in the repository

Within the larger repository, this layer sits between: - deep engine
implementation - formal framework architecture - applied system
modules - the emerging navigation language

A useful reading is:

``` text
simulation
    ↓
structure extraction
    ↓
field representation
    ↓
transition geometry
    ↓
channel formation (v8)
    ↓
switch dynamics (v9)
    ↓
navigation language
```

The `nexah/` directory primarily lives in the last four of these layers.

------------------------------------------------------------------------

## Internal structure

The current `nexah/` directory contains the following components.

### 1. `engine.py`

This provides a minimal high-level access point to core structural
functionality.

It exposes simplified entry points such as: - finite posets - lattice
construction

This makes `nexah/` a lightweight package layer rather than only a
documentation folder.

------------------------------------------------------------------------

### 2. `field_layer/`

The `field_layer/` is the geometric core of the `nexah/` package layer.

It translates evolving system states into a more continuous structural
representation.

This layer currently includes: - field construction - vector
approximation from state sequences - curvature estimation -
fragmentation metrics - flow strength metrics

Its central idea is:

> systems are not only sequences of states ---\
> they also generate local motion geometry.

The FIELD layer is therefore the bridge between: - dynamics - geometry -
channel formation - navigation

See: - [field_layer/core/README.md](./field_layer/core/README.md)

------------------------------------------------------------------------

### 3. `identity/`

This folder contains the identity documents of NEXAH.

These documents clarify: - what NEXAH is - what it is not - what its
strongest current layers are - how to distinguish core, emerging
extensions, and proto structures

This is where the framework's self-definition becomes explicit.

Current document: -
[identity/NEXAH_IDENTITY.md](./identity/NEXAH_IDENTITY.md)

------------------------------------------------------------------------

### 4. `navigation/`

This folder contains the currently emerging navigation language of
NEXAH.

These documents define the first explicit vocabulary for how movement
through structured fields may be understood.

They currently include: - navigation primitives - Zither-Gate logic - 3
plus 1 completion logic - split-interface-marker logic - channel-based
navigation concepts (v8) - switch-layer and regime transition logic (v9)

This is where the project begins to move from: - geometry as
description\
toward\
- geometry as passage\
→ and now further toward\
- geometry as controlled transition

Current documents: -
[navigation/NEXAH_NAVIGATION_PRIMITIVES.md](./navigation/NEXAH_NAVIGATION_PRIMITIVES.md) -
[navigation/NEXAH_ZITHER_GATE_MODEL.md](./navigation/NEXAH_ZITHER_GATE_MODEL.md) -
[navigation/NEXUS_3_PLUS_1_GATE_NOTE.md](./navigation/NEXUS_3_PLUS_1_GATE_NOTE.md) -
[navigation/SPLIT_INTERFACE_MARKERS_NOTE.md](./navigation/SPLIT_INTERFACE_MARKERS_NOTE.md)

------------------------------------------------------------------------

### 5. RATH / OLGO-JANUS Layer (neu 2026)

Die jüngste Erweiterung der Navigation-Sprache bildet die RATH
Phi-Lambda Resonance Bridge mit OLGO-JANUS Six-Sector Gate, v-bands
(Breathing Wave + Blinking Pulse) und der 432-440-444 Layer-Verwebung.

Siehe: - navigation/RATH_PHI_LAMBDA_RESONANCE_BRIDGE.md -
navigation/OLGO_JANUS_SIX_SECTOR_GATE.md -
navigation/V_BANDS_BREATHING_WAVE_BLINKING_PULSE.md

------------------------------------------------------------------------

### 6. `visuals/`

This folder contains the featured visual layer associated with the
current NEXAH concepts.

These visuals are not only decorative.

They serve as: - conceptual anchors - navigation diagrams - field
illustrations - channel structures - switch and transition references -
identity-layer highlights

The visual layer is especially important because much of NEXAH develops
through the interaction of: - computation - geometry - conceptual
notation - visual structure

A dedicated gallery should gradually curate the strongest visual pieces
from this layer.

------------------------------------------------------------------------

## Core idea of this directory

If `ENGINE/` is where NEXAH computes,\
and `FRAMEWORK/` is where NEXAH is architecturally described,

then `nexah/` is where NEXAH becomes: - readable - nameable -
geometric - navigable - dynamically controllable

Its main purpose is to gather the emerging layer in which:

structure becomes field\
field becomes geometry\
geometry becomes channel\
channel becomes switchable\
switch becomes navigation

------------------------------------------------------------------------

## Summary

The `nexah/` directory is the place where the NEXAH framework becomes
its own conceptual and operational layer.

It connects: - lightweight package access - field representation -
identity clarification - navigation grammar - channel dynamics (v8) -
switch dynamics (v9) - visual synthesis

In short:

`nexah/` is where NEXAH begins to speak, move, and decide in its own
language.
