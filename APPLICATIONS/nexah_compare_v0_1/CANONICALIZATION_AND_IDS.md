# Canonicalization and Stable IDs

Profile: `NEXAH_COMPARE_CANONICAL_JSON_0_1`

## Canonical JSON

1. Input is UTF-8 JSON.
2. Duplicate object keys are rejected.
3. `NaN`, positive or negative infinity and non-finite runtime values are
   rejected.
4. Object keys are serialized in Unicode code-point order.
5. Array order and JSON value types are preserved.
6. Serialization uses no insignificant whitespace and emits Unicode directly.
7. Exactly one terminal LF is emitted.
8. No implicit timestamp, random value, locale value or machine path is added.
9. Canonicalization never changes the input file in place.
10. SHA-256 is calculated over the exact canonical bytes.

This profile adopts the sealed THE EYE policy mechanics. It does not claim RFC
8785 or cross-language equivalence. Decimal quantities are strings so display
and binary floating-point behavior cannot silently change identity.

## Stable IDs

IDs are ASCII, explicit and stable across replays:

| Object | Form |
|---|---|
| Case | `CASE-<SLUG>` |
| Analysis | `AN-<CASE-SLUG>-<SOURCE-SLUG>` |
| Evidence | `EVD-<CASE-SLUG>-NNNN` |
| Claim | `CLM-<ANALYSIS-SLUG>-NNNN` |
| Relation group | `REL-<CASE-SLUG>-NNNN` |
| Residual | `RES-<CASE-SLUG>-NNNN` |
| Comparison | `CMP-<CASE-SLUG>-<PROFILE-SLUG>` |
| Return | `RET-<COMPARISON-SLUG>-NNNN` |

An ID identifies a declared record or unit; it is not inferred from a label.
Renaming display text does not change the ID. Material content changes produce
a new content hash and, when identity changes, a new ID. IDs are never reused
for a semantically different object.

## Record hashes

Every admitted evidence file carries its byte SHA-256. WP3 calculates the
SHA-256 of the exact canonical ComparisonRecord bytes and returns it in the CLI
success summary. The frozen `ComparisonRecord` schema has no self-hash field,
so the runtime does not silently add one. WP4 may bind this external digest in
a receipt and the existing `ReturnRecord.comparison_sha256`; adding an embedded
self-hash would require an explicit versioned contract amendment.

## Paths and time

Evidence paths are relative to the future Case package root and may not be
absolute or contain a `..` segment. Time values use RFC 3339. Business periods
use explicit `start`, `end`, `basis` and `timezone`; a month and a year are not
silently comparable.
