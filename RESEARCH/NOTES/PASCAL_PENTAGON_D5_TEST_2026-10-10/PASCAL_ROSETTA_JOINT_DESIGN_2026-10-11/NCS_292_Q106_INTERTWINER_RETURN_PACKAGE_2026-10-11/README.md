# NCS-292 · Q106 Intertwiner & Return Package

Reused identity: `SCC-003 / A0OE:PASCAL_PENTAGON_D5_TEST`  
Related backlog: `A0-BL-023`, `A0-BL-051`  
Status: `PASS_WITH_OPEN_INTERTWINER` — formal design replay, not a new Study

## Result

The original five modules and six new typed validation gates now live in one
bounded package:

1. **NCS operator recovery.** The old animation contains a common planar
   translation of four points with identity label action. It does not contain
   a hidden four-package permutation.
2. **Q106 interface search.** Exhaustive D5 orbit-union search finds one unique
   connected `5+5+5` interface of size 15 and one unique connected
   `5+5+5+5` interface of size 20. No connected eight-5-orbit interface of
   size 40 exists.
3. **ABC/123 residual.** Q106 has one unique connected invariant six-node
   residual — apex plus first seam ring — and a connected invariant 100-node
   complement. The six-label alphabet `ABC x {+,-}` is defined, and the
   `P1/P2/P3 + H7` labels exist as an observer mask; their node map into the
   six-node Q106 residual is not defined. The stronger `5 x 20` block system
   also remains open.
4. **Janus return.** Both the commuting and dihedral Janus laws are internally
   valid. The sources do not select one. The Möbius seam returns in the
   20-class quotient after one turn and exactly after two.
5. **Interactive instrument.**
   [Open the explorer](NCS_292_Q106_INTERTWINER_RETURN_EXPLORER.html) to inspect
   translation, orbit interfaces, residual and return laws.
6. **Exact D20 decoder.** `n=400z+20y+x` round-trips all five recovered
   samples: 1729, 417, 1836, 378 and 718.
7. **Lossy P20 view.** `(z,y,x)->(x+y/2,z)` reproduces the historical plots,
   but is provably non-injective. This is now reported as
   `INFORMATION_LOST_AS_EXPECTED`, not as a decoder failure.
8. **Namespace boundary.** The five-state alphabet `V5={-2,-1,0,+1,+2}` and
   the residue carrier `C20=Z/20Z` remain distinct typed objects.
9. **Address bus.** `C30->C6` has six fibres of five and wraps phase `29->0`.
   It exposes an address; it does not choose a seam.
10. **β/Janus stop gate.** All `6!=720` seam-pin assignments remain candidates,
    while both Janus laws remain algebraically valid and historically
    unselected.
11. **Fibonacci rail.** The closed `A0-BL-045` results are hash-bound and
    replayed: `Q^5=[[8,5],[5,3]]`, `det=-1`, `tr=11`, and
    `Q^10=[[89,55],[55,34]]`. `Q^10` is not an identity return; determinant
    `-1` does not select Möbius topology. The signed reciprocal bridge keeps
    exact return and anti-return separate, while transport to D20/C20/X20/X40
    or Q106 remains open.

## Documentary explorer integration — 2026-10-15

The interactive explorer now displays the current parent result `44/44` and
adds two source-bounded comparator views. They do not modify `RESULT.json`, add
checks or reopen the frozen formal design:

- The factor view shows the stored nested pure-five-orbit examples
  `I15=3*5` and `I20=4*5`, with `I15` contained in `I20` by the addition of
  one five-node orbit.
- It separates three typed uses of `105`: `106-1=105=5*21=3*5*7` is Q106
  cardinality arithmetic; the C12/D30 branch audit records
  `105 L + 105 R = 210` incidences; and the existing Ghostgrid/Q840 audit
  records `840-735=105` as a `35`-only residue tick in `Z/840Z`. Equal integer
  value does not identify these carriers, and no 105-node Q106 interface is
  inferred.
- It marks `ABC x {+,-}` and `P1/P2/P3 + H7` as available label layers while
  keeping the actual label-to-Q106 node map null.
- The drift comparator places the recovered NCS translation
  `d(f)=0.224*sin(0.16f)`, the historical marker `1/112` and
  `zeta(-1)=-1/12` on one number line while retaining three different semantic
  types. The finite Ihara/Hashimoto `5 -> 10` primitive-cycle change is a cycle
  signature, not a drift; no Riemann-to-NCS or Riemann-to-Q106 map is claimed.

Ghostgrid source: [Q840 archaeology addendum](<../../../../../../../00 EXECUTIVE/NEXAH-Mission-Control/INTAKE/NEXAH_ROOT7_EULER_MIRROR_CONCORDANCE_INTAKE_2026-09-28/06_GHOSTGRID_Q840_ARCHAEOLOGY_ADDENDUM.md>).

The revised verifier passes `44/44` checks with classification
`RECOVERED_LAYERED_PIPELINE_WITH_OPEN_FIBONACCI_TRANSPORT_BETA_JANUS`. The package therefore
sharpens the bridge substantially, but deliberately keeps the actual
adjacency-preserving `X20 -> Q106` intertwiner, canonical β binding and
historical Janus selection — plus Fibonacci cross-carrier transport — open.

## Owner-authorized Euler-41 residual-switch follow-up

The bounded follow-up
[`EULER41_RESIDUAL_SWITCH_AUDIT_2026-10-11`](EULER41_RESIDUAL_SWITCH_AUDIT_2026-10-11/README.md)
passes `60/60` checks with classification
`PASS_EXACT_CONTROLLER_ARCHITECTURE_WITH_OPEN_SEAM_BINDING`.

It adds no identity. It verifies the exact `29=p_10`, `41=p_13`, base-13
mirror and Euler `40 -> 41` boundary; types the `+1` as an external controller;
and derives a canonical D5-invariant apex-versus-ring binary readout from the
unique Q106 residual. It also proves that this bit does not canonically select
one of the six compatible added seam orbits or one of the two Janus laws.

The recovered semantics are now promoted into independent parent-level gates;
the follow-up remains a downstream replay rather than a cyclic frozen input.
The refined circuit verifies two distinct ingress routes meeting at
the value 29, the C30-to-C6 six-address quotient, the 720 unresolved seam-pin
assignments, the synchronization cover 120, and the exact arithmetic joint
`206^2-204^2=820=41*20`. Forty-seven unique owner-supplied views are
hash-bound as visual archaeology, and the expanded ledger
crucially binds the base-20/frame family to recovered Thread-V, Codex
Resonantia, Observer-Atlas, UCRT and prior Science-Lab forensic sources outside
Photos. The exact decoder `n=400z+20y+x` replays all five source samples; its
`x+y/2` plot coordinate is explicitly retained as a lossy view.

## Owner-supplied Q106 prime-index binding

The bounded
[`JANUS_PN_HANDLE_VM_TRANSFER_AUDIT_2026-10-11`](JANUS_PN_HANDLE_VM_TRANSFER_AUDIT_2026-10-11/README.md)
passes `71/71` checks and binds Q106 to the standard one-based prime-index
map without creating another NCS or Q106 identity:

```text
p_(2^3) = p_8  = 19
p_(2^4) = p_16 = 53
Q106    = 2 * p_16 = 2 * p_(2^4)
```

The already source-bound
[`Q106_PRIME_INDEX_RADIX_ROOT_GROWTH_AUDIT_2026-10-11`](Q106_PRIME_INDEX_RADIX_ROOT_GROWTH_AUDIT_2026-10-11/README.md)
also supports the following exact C-closure, retained here as a working
navigation label rather than a new operator:

```text
p_(4^2) = p_16 = 53
53 + 4*p_5 = 53 + 44 = 97 = p_25 = p_(5^2)
97 + 3^2 = 97 + 9 = 106
4*p_5 + 3^2 = 44 + 9 = 53 = p_16
therefore 106 = p_16 + p_16 = 2*p_16
```

Thus `x4` belongs to `p_5=11`, while the outer Q106 closure uses `x2` on
`p_16=53`. The intermediate split is `106=53+44+9`, or equivalently
`106=53+(44+9)=53+53`.

The first line and second line form an index-power ladder (`8 -> 16`); they do
not assert that doubling the prime value `19` produces `53`. The separate
boundary `p_19=67` prevents reversal of prime value and prime index. In the
first-four-prime radix grammar the same Q106 is recovered independently as
`2*C_10(5,3)=2*53=106`, while `C_10(7,2)+C_10(3,5)=72+35=107=p_28`.

This is exact arithmetic evidence inside the existing
`SCC-003 / A0OE:PASCAL_PENTAGON_D5_TEST` source lineage. The thematic lens
remains an unbound NN / NEXAH Navigator candidate; the evidence location does
not identify the lens with A0. The Triple-19/57 visual extension remains
deferred rather than being silently folded into NCS.

The subsequently Owner-authorized
[`Q106_SQUARE_INDEX_PRIME_READOUT_AUDIT_2026-10-11`](Q106_PRIME_INDEX_RADIX_ROOT_GROWTH_AUDIT_2026-10-11/Q106_SQUARE_INDEX_PRIME_READOUT_AUDIT_2026-10-11/README.md)
passes `17/17`, with byte-identical Primary/Replay and an independent `13/13`
verifier. It types the Q106 readout as

```text
(F,O,L) = (9,16,25) = (3^2,4^2,5^2),
P_square(3,4,5) = (p9,p16,p25) = (23,53,97).
```

The Pythagorean equality belongs to the index layer, not to the prime values.
The exact C-closure survives, while no D5-invariant 53-node subcarrier exists.
The result is therefore a prime-index lens over Q106 rather than a geometric
53-node half or a new Prime Pascal Pyramid identity.

The subsequent bounded
[`46/106/194 contrast`](Q106_PRIME_INDEX_RADIX_ROOT_GROWTH_AUDIT_2026-10-11/Q106_SQUARE_INDEX_PRIME_READOUT_AUDIT_2026-10-11/Q106_46_106_194_CONTRAST_AUDIT_2026-10-11/README.md)
passes `16/16` with byte-identical replay and independent `16/16`
verification. The common arithmetic carrier grammar
`C_k=2*p_(k^2)` gives `46,106,194` for `k=3,4,5`, but only `k=4` satisfies
`C_k-p_((k+1)^2)=(k-1)^2`; it is also the sole hit in the declared finite
scan `2<=k<=1000`. This strengthens bounded selectivity without defining
`R(Q46)` or `R(Q194)` and without creating a new Pascal identity.

## Replay

From the NEXAH repository root:

```bash
python3 RESEARCH/NOTES/PASCAL_PENTAGON_D5_TEST_2026-10-10/PASCAL_ROSETTA_JOINT_DESIGN_2026-10-11/NCS_292_Q106_INTERTWINER_RETURN_PACKAGE_2026-10-11/verify_intertwiner_return.py
```

Use `--write` to refresh `RESULT.json` after intentional source changes.

## Files

- `CONTRACT.json` — frozen inputs, modules, outcomes and claim ceiling
- `FORMAL_CONTRACT.md` — mathematical statement and stop boundary
- `verify_intertwiner_return.py` — deterministic exhaustive replay
- `RESULT.json` — current machine-readable result
- `NCS_292_Q106_INTERTWINER_RETURN_EXPLORER.html` — source-bound instrument

## What this does not claim

The package creates no new Navigator identity, no `PENT-08`, no admitted Lab
run and no publication state. Matching cardinalities and D5 orbit profiles do
not by themselves identify carriers, historical mechanisms or physical
systems.

## X20 adjacency-intertwiner follow-up

The Owner-authorized bounded follow-up
[`NCS_X20_Q106_ADJACENCY_INTERTWINER_AUDIT_2026-10-11`](NCS_X20_Q106_ADJACENCY_INTERTWINER_AUDIT_2026-10-11/README.md)
passes `22/22` contract and finite-structure checks. It extracts the unique
twenty-node Q106 interface and counts `15000` rotation-equivariant and `24`
D5-equivariant target charts.

The audit also localizes the remaining blocker: the frozen source defines
`X20=C5 x P4` as a state set with rotation but supplies no adjacency or edge
types. The correct classification is therefore
`UNDEFINED_CONTRACT_ADJACENCY_MISSING`; `typed_intertwiner_to_q106` remains
`null`. No Q106 edge rule is pulled back into X20, no chart is selected, and
Triple-19 Pc/Pd compatibility remains open until an independent X20 graph and
typed carrier map exist.

## X20 source-contract and Triple-19 follow-up

The next closed-gate package
[`NCS_X20_TYPED_CARRIER_PCPD_Q106_INTERTWINER_AUDIT_2026-10-11`](NCS_X20_TYPED_CARRIER_PCPD_Q106_INTERTWINER_AUDIT_2026-10-11/README.md)
passes `60/60` source, type and gate checks and returns
`SOURCE_CONTRACT_UNRECOVERED`.

It confirms that `P4` is the four-role set `carrier / frame_cut /
transform_view / return_record`, not a declared path graph. No frozen NCS,
MRB, ACR-44 or OIL/RIS source supplies `E_X` or X20 edge types. It also
corrects the Triple-19 typing: `P_c` and `P_d` construct oriented states;
`A(r,c_r,sigma)=(6-r,c_r,-sigma)` is the involution. The Triple-19 carrier has
fourteen oriented states and no typed map to X20 or Q106.

All `24` inherited D5 charts remain enumerated but blocked before target fit.
No adjacency or Pc/Pd compatibility test is executed and no chart is ranked or
selected.

## Triple-19 / X40 orientation-factor follow-up

The bounded factor audit
[`TRIPLE19_X40_C2_ORIENTATION_FACTOR_AUDIT_2026-10-11`](TRIPLE19_X40_C2_ORIENTATION_FACTOR_AUDIT_2026-10-11/README.md)
passes `50/50` checks. It establishes an exact shared `C2` orientation factor:
the Triple-19 antipode and both X40 Janus candidates induce the same bit flip.

The result does not choose between the commuting and dihedral Janus laws. The
declared quotient `q:X40→X20` collapses the two orientation values in every one
of its twenty fibres, so no `rho:X20→C2` can reconstruct that factor. Moreover,
`Hom(C7,C5)` is trivial. The full Triple-19-to-X20 carrier map, X20 adjacency,
Q106 intertwiner and historical Janus selection therefore remain null.

