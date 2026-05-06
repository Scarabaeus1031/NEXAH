# nexah/core — The NEXAH Kernel

This is the **minimal core** of the NEXAH framework.

It defines the central data structures and loading mechanisms used by all higher layers (geometry, navigation, applications).

## Current Structure

- `system/` — System schema, validation and loader
  - `schema.py` — `NexahSystem` dataclass and validation
  - `loader.py` — JSON loading with schema validation

## Purpose

- Provide a clean, typed representation of a NEXAH system (nodes, edges, regimes, transitions, risk_target, etc.)
- Ensure schema validation when loading system definitions
- Serve as the foundation for geometry mapping and control logic

## Usage Example

```python
from nexah.core.system.loader import load_system

system = load_system("path/to/my_system.json")

print(system.nodes)
print(system.regimes)
print(system.risk_target)
