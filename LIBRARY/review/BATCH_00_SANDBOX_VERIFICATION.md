# NEXAH Library — Batch 00 Sandbox Verification

## Result

**PASS**

- Sandbox Channel: `NEXAH API SANDBOX`
- Are.na Channel ID: `5446798`
- Visibility: `private`
- Production mutations: `0`
- Public Library Channels modified: `0`
- Test material remaining in Sandbox: `0`
- Reusable orphan Blocks created by the two test attempts: `2`
- Known first-attempt Block ID: `47957216`

## Verified operations

1. Create Text Block — passed
2. Verify Text Block — passed
3. Remove the test Block from the Sandbox by destroying its Connection — passed
4. Create Channel Connection — passed
5. Move Connection to the visual top — passed
6. Verify order — passed
7. Remove test Channel Connection — passed

Are.na V3 models removal of a reusable Block from a Channel as removal of its
Connection. A direct `DELETE /v3/blocks/{id}` attempt returned HTTP 405 during
the first isolated run. The test Connection was immediately removed, the
Sandbox was verified empty, and the harness was corrected to use the supported
Connection-removal semantics. The disconnected Blocks may remain as private
orphan objects because V3 exposes no global Block-delete operation. No public
Channel was involved. Future Sandbox journals record both Block and Connection
IDs explicitly.

## Aftercare

- New Source Snapshot: `arena-2026-07-15T224634+0000`
- Public Channels: `71`
- Registered Entities: `10`
- Visible Channel Connections: `50`
- Health: `pass_with_editorial_warnings`
- Release Check: `pass_with_editorial_warnings`
- Errors: `0`

The private Sandbox and its test artifacts are intentionally absent from the
public Source Snapshot.

## Editorial Diff against the prior baseline

- Records checked: `71`
- No change: `64`
- Metadata changes: `6`
- Link changes: `1`
- Content-count changes: `0`
- Sequence changes: `0`
- Availability changes: `0`

The observed differences predate or are independent of Batch 0. Batch 0 touched
only the private Sandbox. The apparent START link change is not a topology
change: connected Channel `5345108` remained at position `70`; only a trailing
space in its title changed.

Metadata review candidates:

- `5345108` — title whitespace and `updated_at`
- `5391199` — `updated_at`
- `5397157` — description and `updated_at`
- `5404597` — title and `updated_at`
- `5404615` — description and `updated_at`
- `5442781` — title whitespace and `updated_at`

These observations do not authorize Registry, Queue, or Are.na changes.

## Existing editorial warnings

- 14 curated transitions are not directly clickable
- 5 Series remain editorially unresolved
- 16 manual cleanup Actions remain open

## Governance conclusion

Batch 0 proves that the Writer can create, move, verify, and remove temporary
editorial Connections inside a private Channel while leaving the public Library
unchanged. Batch 1 remains blocked until its four Queue Actions are explicitly
changed from `pending` to `accepted` through a separate human-reviewed
repository edit.
