# HP-007 Package Structure

Status: `DESCRIPTIVE REVIEW AID — NO PHYSICAL SPLIT`

## Physical structure

```text
NEXAH Operator Orientation_culture/
├── .DS_Store
├── 23 root PNG files
└── THE OPERATORS OF ORIENTATION/
    ├── .DS_Store
    ├── PART 0/
    │   └── 7 PNG files
    ├── PART I/
    │   └── 5 PNG files
    └── PART_I_Index.png
```

| Property | Verified value |
|---|---:|
| Total files | 38 |
| Total bytes | 77943254 |
| PNG files | 36 |
| `.DS_Store` files | 2 |
| Root PNG files | 23 |
| Structured-draft PNG files | 13 |
| Unique SHA-256 hashes | 37 |
| Internal duplicate groups | 1 |
| Exact NEXAH/Control Desk repository matches | 0 |

## Descriptive strata

### Structured editorial draft

The nested 13-PNG stratum contains `PART 0`, `PART I`, a Part I index, overview
plates and developed plates for `OBSERVE` and `REFERENCE`. The index lists
additional operators, but no accepted evidence establishes their completion.

### Root visual and application material

The 23 root PNGs include process maps, operator tables, golf and movement
studies, boundary and biological plates, cultural orientation material and one
screenshot.

These strata are inspection aids only. They do not authorize a split and do not
create Works, Editions, supplements or source-master identities.

## Preserved unresolved elements

- INC-0040 and INC-0041 have identical bytes and different filenames.
- Both `.DS_Store` files are retained as physical package metadata.
- The screenshot remains included; its role is unresolved.
- UUID filenames do not establish page order.
- Page sequence and version lineage remain unknown.
- Scientific and operator claims in the visuals remain unvalidated historical
  source content.

## Preserved structure

```text
LIBRARY/review/HP-007/
├── README.md
├── PROVENANCE.md
├── SOURCE_MANIFEST.csv
├── PACKAGE_STRUCTURE.md
└── source_bundle/
    └── NEXAH Operator Orientation_culture/
        └── 38 unchanged files
```

## Copy-first verification

The owner-authorized preservation satisfied all required invariants:

1. the source remains 38 files and 77943254 bytes;
2. all 38 hashes match `SOURCE_MANIFEST.csv`;
3. the exact payload path was absent before copying;
4. all 38 files are copied without rename, edit, normalization, filtering,
   reordering, split or consolidation;
5. the duplicate pair, metadata files and screenshot remain present;
6. the source remains in Intake until a separate disposition decision;
7. destination paths, bytes and hashes pass full verification;
8. NX-000008, OLS, ORION, Registry, Experience, Are.na, publication and HP-008
   remained unchanged.

Verification result: `PASS`. The Intake source remains present. Any source
removal requires a separate Owner completion review and authorization.
