# NEXAH Library

`LIBRARY/` is the canonical bridge between the visual NEXAH Library on Are.na
and the implementation, research, and validation layers in this repository.

It contains:

- ten pilot Entity records;
- seventeen controlled Core Operator records;
- the frozen Library Architecture v1.0;
- stable identity and curated classification used by read-only queries.

The executable loader, Are.na comparison client, and query layer live in
`nexah/library/`. Tests live in `tests/library/`.

## Commands

From the repository root:

```bash
python -m nexah.library validate
python -m nexah.library compare --all
python -m nexah.library reading-path --audience newcomer
python -m nexah.library operators --operator NX-OP-0005
python -m nexah.library graph --format mermaid
python -m nexah.library recommend NX-000004 --limit 5
```

An Are.na token is optional for material that is not publicly readable:

```bash
export ARENA_TOKEN="..."
```

The Are.na connector is strictly read-only. It can fetch and compare current
metadata, but it contains no create, update, connect, sort, or delete method.

## Structure

```text
LIBRARY/
├── README.md
├── architecture/
│   └── LIBRARY_ARCHITECTURE_V1.md
└── registry/
    ├── registry.yaml
    ├── entities/
    └── concepts/
```

Are.na remains authoritative for visual content and sequence. Registry YAML
remains authoritative for stable NEXAH identity and curated classification.
