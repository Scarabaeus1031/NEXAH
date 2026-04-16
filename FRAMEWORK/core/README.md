# nexah/core — The NEXAH Kernel

This directory contains the **minimal core** of the NEXAH framework.

It defines the central abstractions used by all higher layers:

- System representation (`NexahSystem`)
- Schema validation
- Loading of system definitions from JSON
- Core data structures for nodes, edges, regimes, transitions, risk targets, etc.

## Purpose

This is the **heart** of NEXAH — everything else (geometry, navigation, applications) builds on top of these definitions.

## Current Structure

- `system/` — System schema, validation and loader
- `__init__.py` — Package initialization

## Usage Example

```python
from nexah.core.system.loader import load_system

system = load_system("path/to/system_definition.json")
print(system.nodes)
print(system.regimes)
