# Euler-41 / Q106 Residual Switch Audit

Reused identity: `A0OE:PASCAL_PENTAGON_D5_TEST`  
Parent: `A0-BL-023:NCS_292_Q106_INTERTWINER_RETURN_PACKAGE:V1`  
Authority: bounded Human Owner authorization, 2026-10-11  
Status: `PASS_WITH_OPEN_SEAM_BINDING` — formal design, no new Study or Run

## Short result

The proposed residual switching architecture is real at one precise level:

```text
X40 + external controller q
             |
             v
       41 = p_13
       41 = 32_13  --reverse-->  23_13 = 29 = p_10

Q106 = 100 + (1 + 5)
               |
               +-- canonical D5 quotient: apex=0, first ring=1
```

The audit passes all `60/60` deterministic checks. The unique six-node residual has a
canonical D5-invariant **binary readout**: apex versus five-node ring. That is
a legitimate off/on channel and makes the NCS residual interpretation much
stronger than a numerical coincidence.

The switch is not yet a canonical Möbius selector. Q106 has trivial intrinsic
`H1`; six added D5-compatible seam orbits remain. Because each seam choice is
itself D5 invariant, there is no D5-equivariant bijection from the moving
`1+5` residual nodes to those six fixed choices. The bit can activate a seam
channel, but it cannot determine which seam or whether `Jc` or `Jd` is used.

## Vigesimal circuit refinement

Two exact ingress routes can meet at the integer `29`:

```text
X28 disjoint-union {q29} -> 29
X40 disjoint-union {q41} -> 41 ->[base-13 digit reversal]-> 29
```

The integer is then inserted as `[29]_30` in the verified C30
Pascal–Lissajous clock. One unit step returns to `[0]_30`, and the canonical
projection `C30 -> C6` exposes six address classes with five phases each.

The process visuals also expose one exact arithmetic joint:

```text
206^2 - 204^2 = (206-204)(206+204) = 820 = 41*20.
```

This binds the factors 41 and 20, but it does not make the displayed 41° and
20° arcs equal or prove a torsion, resonance or physical bridge. The
architecture has an exact address bus, not yet an exact seam wire: a bijection
from the six C6 addresses to the six Q106 seam orbits has `6! = 720`
possibilities, and no source selects one.

The recovered Thread-V source also makes the former “400/20” vocabulary
precise. It is the ordinary base-20 decoder

```text
n = 400z + 20y + x
```

followed by the display projection `(z,y,x) -> (x+y/2,z)`. All five displayed
samples (1729, 417, 1836, 378, 718) replay. The projection is lossy, so the
three base-20 digits remain the actual state; the plot is a view, not a 3-D
spiral mechanism.

One vocabulary collision is now explicit: UCRT uses “vendissimal” for a
five-state alphabet, while Thread V uses it for base 20. Those are `V5` and
`C20`, not one carrier. This audit calls them **five-state** and
**base-20/vigesimal** respectively unless a typed map is supplied.

## What the new clues resolve

- `29` is the 10th prime; `41` is the 13th prime.
- The strongest exact 29/41 joint is radix-scoped:
  `41=32_base13`, whose digit reversal is `23_base13=29`.
- Euler's polynomial supplies the sharp boundary: prime values through step
  40, then the first failure at step 41 with `41^2`.
- `40+1` is well typed as `X40 disjoint-union {q}`. The `+1` is a controller,
  not a hidden payload state.
- A 13-step prime-index stair ending at 41 and a 13-weight Fibonacci rail can
  be drawn coherently. The blue rail / green-yellow stair palette is an owner
  display declaration, not a mathematical cause.
- The two 34 plates are valuable controls: Dürer and Khajuraho share magic sum
  34 and Q4 complement, yet implement it through different spatial operators.

## Important archaeology correction

LIFE06B already contains an Euler Stair / Fibonacci Rail instrument, but it
uses the first ten primes and its existing rail is yellow. The present
13-step/palette proposal is therefore an explicit extension/view, not a
historical property silently read back into LIFE06B.

## Files

- `FORMAL_CONTRACT.md` — typed model and proof boundary
- `CONTRACT.json` — frozen sources and machine contract
- `verify_euler41_residual_switch.py` — deterministic replay
- `RESULT.json` — machine-readable result
- `NN_REPO_ARCHAEOLOGY_CROSSWALK.md` — existing NN/repository route map
- `VISUAL_SOURCE_LEDGER.md` — forty-seven unique supplied views, hashes,
  recovered non-Photos module sources, custody and claim boundaries

## Replay

From this directory:

```bash
python3 verify_euler41_residual_switch.py
```

Use `--write` only after an intentional frozen-source update.

## Next unresolved object

The smallest remaining mathematical object is not another broad theory. It is
a typed selector

```text
sigma: controller/readout state -> {six seam orbits} x {Jc,Jd}
```

with an explicit source rule and an adjacency/operator-preserving transport to
Q106. Until that exists, the correct result is:

`PASS_EXACT_CONTROLLER_ARCHITECTURE_WITH_OPEN_SEAM_BINDING`.
