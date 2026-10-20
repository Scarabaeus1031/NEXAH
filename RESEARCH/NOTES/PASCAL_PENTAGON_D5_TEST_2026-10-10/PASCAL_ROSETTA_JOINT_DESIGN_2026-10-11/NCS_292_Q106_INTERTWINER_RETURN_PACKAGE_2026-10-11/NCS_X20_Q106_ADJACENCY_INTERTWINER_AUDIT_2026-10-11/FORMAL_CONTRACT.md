# NCS X20 → Q106 adjacency intertwiner audit

Date: `2026-10-11`  
Parent: `A0-BL-023:NCS_292_Q106_INTERTWINER_RETURN_PACKAGE:V1`  
Class: bounded formal audit; extension of the existing SCC-003/Q106 identity

## Objects

The parent defines the quotient state set

```text
X20 = C5 × P4 = {(s,p): 0≤s<5, 0≤p<4}
r_X(s,p) = (s+1 mod 5,p).
```

It does not define an edge set on `X20`, an adjacency on `P4`, or edge types.
In particular, the letter `P` is used for four package labels and cannot be
silently promoted to the path graph `P4`.

The target is the unique connected Q106 union of four five-node D5 orbits.
Its graph is the induced undirected support of the frozen Q106 edge table.

## Necessary map classes

Any rotation-equivariant bijection must send the four free C5 orbits of X20
to the four target C5 orbits. There are

```text
4! × 5^4 = 15000
```

such bijections: choose an orbit permutation and one cyclic phase per orbit.

If the candidate reflection

```text
j_X(s,p)=(-s mod 5,p)
```

and the frozen Q106 reflection `m` are both required, every orbit phase is
fixed by its reflection anchor. The remaining D5-equivariant bijections number

```text
4! = 24.
```

Neither count supplies adjacency preservation or a canonical map.

## Intertwiner gate

A typed graph intertwiner requires

```text
{x,y} in E_X  iff  {iota(x),iota(y)} in E_Q
iota r_X = r_Q iota
iota j_X = m_Q iota
```

with any directed or typed edge conditions stated separately. Since `E_X` is
not present in the frozen sources, the first equation is undefined. Pulling
`E_Q` back through a selected chart would manufacture the desired result and
is prohibited.

## Comparator boundary

The verifier records three common completions only as controls:

- the empty graph on 20 states;
- four disjoint five-cycles;
- the Cartesian product graph `C5 □ P4`.

Their edge or degree profiles differ from the target interface. This does not
prove that no source graph can work; it proves that these undeclared defaults
must not be substituted for a missing source contract.

## Return and Triple-19 boundary

The quotient return and two-turn exact return established by the parent remain
valid. They do not create `E_X`. The Triple-19 Pc/Pd involution remains a
related representation bridge. Its commutation with Q106 cannot be tested
until both `iota` and a typed Pc/Pd-to-X20-or-Q106 map exist.

## Expected disposition

If all frozen inputs and finite counts replay, while `E_X` remains null, the
correct result is:

```text
PASS / UNDEFINED_CONTRACT_ADJACENCY_MISSING
typed_intertwiner_to_q106 = null
```

This is a localized formal result, not a failed search and not permission to
select one of the remaining charts.
