# NCS–SNC 292/929 Order, Envelope & Return Test

Reused identity: `SCC-003 / A0OE:PASCAL_PENTAGON_D5_TEST`  
Parent: `NCS-292 · Q106 Intertwiner & Return Package`  
Status: bounded formal design validation; no new Study or Navigator identity

## Question

Do the six orders of the parent package's finite rotation and Janus maps act
identically, or does operator order create a measurable ALGO/OLGO/OKO
Envelope?

## Contract boundary

For this test only, the already validated parent maps are named:

```text
N = five-sector rotation
S = dihedral Janus mirror
C = commuting Janus closure flip
```

This is a declared candidate algebra. It is not a recovered expansion of the
historical acronym `NCS`.

## Replay

From the NEXAH repository root:

```bash
python3 RESEARCH/NOTES/PASCAL_PENTAGON_D5_TEST_2026-10-10/PASCAL_ROSETTA_JOINT_DESIGN_2026-10-11/NCS_292_Q106_INTERTWINER_RETURN_PACKAGE_2026-10-11/NCS_SNC_292_929_ORDER_ENVELOPE_RETURN_TEST_2026-10-11/verify_order_envelope_return.py
```

## Result vocabulary

- **ALGO:** exact proportions and preservation ratios.
- **OLGO:** mirror axis, orientation reversal and conjugacy.
- **OKO:** cycle topology, closure order and exact return.
- **Envelope:** the set of distinct three-track signatures over all six orders.
- **Operator 16:** the combined three-track record, not sixteen component maps.

The separate `2^4` sixteen-state register is retained as an open carrier. No
map from X40 or W20 to that register is invented.

## Result

The verifier passes `21/21` checks and resolves the six words into exactly two
classes:

```text
Class A: CNS = NCS = NSC   -> reflection axis sector 2
Class B: CSN = SCN = SNC   -> reflection axis sector 3
```

`NCS` and `SNC` differ on all 40 states. The difference is nevertheless
sharply localized:

- **ALGO is invariant:** every word fixes `8/40 = 1/5`, moves `32/40 = 4/5`
  and preserves package and final layer coordinates.
- **OLGO separates the classes:** both are orientation reversing and satisfy
  `f N f = N^-1`, but their reflection axes lie in different sectors.
- **OKO is invariant:** every word has cycle profile `1^8 2^16`, changes some
  states after one pass and returns every state exactly after two passes.

Thus the declared model contains a real order effect, but it is a mirror-axis
shift rather than a new return topology.

The W20 correction also passes: Q106 contains five weight-20 nodes forming one
complete D5 orbit. They have no internal directed edges, receive two incoming
edges each and have no outgoing edges. `5 x weight 20 = 100` is a weighted
subtotal, not a 100-node block.

## Files

- `CONTRACT.json` — sources, definitions, outcomes and stop rules
- `FORMAL_CONTRACT.md` — exact finite model and claim boundary
- `verify_order_envelope_return.py` — deterministic exhaustive verifier
- `RESULT.json` — machine-readable replay result

## Nonclaims

This package does not establish a historical N/S/C decomposition, a physical
Möbius mechanism, a 292/929 address map, a universal role for `0.929` or
`2.929`, a canonical ALGO/OLGO/OKO Operator registry, or an action on the
separate sixteen-state carrier.
