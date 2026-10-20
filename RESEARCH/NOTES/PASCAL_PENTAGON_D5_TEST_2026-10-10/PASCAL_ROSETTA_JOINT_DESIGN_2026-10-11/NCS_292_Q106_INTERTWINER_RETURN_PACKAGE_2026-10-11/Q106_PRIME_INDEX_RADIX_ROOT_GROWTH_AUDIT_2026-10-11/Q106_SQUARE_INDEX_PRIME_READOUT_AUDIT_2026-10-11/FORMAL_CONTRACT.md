# Q106 square-index prime readout — formal contract

Status: **Owner-authorized bounded formal audit**  
Identity: reuses `SCC-003 / A0OE:PASCAL_PENTAGON_D5_TEST`; creates none.

## Typed maps

The frozen Q106 orbit record provides the readout

```text
R(Q106) = (F,O,L,N) = (9,16,25,106),
```

where `F` is the number of five-node orbits, `O` the total orbit count, `L`
the final level count and `N` the hemisphere carrier cardinality.

Define the square-root readout only on the first three coordinates:

```text
R_square(Q106) = (3^2,4^2,5^2).
```

Define the standard one-based square-index prime lift

```text
P_square(n) = p_(n^2).
```

Then the declared finite evaluation is

```text
P_square(3,4,5) = (p9,p16,p25) = (23,53,97).
```

`P_square(n)` is not `(p_n)^2`. The operator acts on the index before the
prime sequence is read.

## Exact relations under test

```text
9 + 16 = 25
3^2 + 4^2 = 5^2
16 = (2^2)^2 = 2^(2^2) = 4^2

p25 - p16 = 97 - 53 = 44 = 4*p5
106 - p25 = 106 - 97 = 9 = 3^2
44 + 9 = 53 = p16
106 = 2*p16
```

The inherited five-root ladder is checked separately:

```text
(p1,p4,p9,p16,p25) = (2,7,23,53,97)
adjacent sums          (9,30,76,150).
```

## Controls

1. **Type control:** `(p3)^2=25`, `(p4)^2=49`, `(p5)^2=121`; these are not
   `(p9,p16,p25)=(23,53,97)`.
2. **Value-triple control:** `23^2+53^2 != 97^2`. The Pythagorean equality
   belongs to indices `9,16,25`, not to the lifted prime values.
3. **Subcarrier control:** the frozen D5 orbit profile is one orbit of size
   `1`, nine of size `5` and six of size `10`. Every invariant union therefore
   has cardinality `0` or `1 mod 5`; `53 = 3 mod 5`, so no invariant 53-node
   subcarrier exists.
4. **Bounded uniqueness control:** scan positive consecutive roots through
   `a=10000`; only `a=3` satisfies
   `a^2+(a+1)^2=(a+2)^2`. This is also exact algebraically because the
   equation reduces to `(a-3)(a+1)=0`.

## Interpretation boundary

Passing establishes an exact finite **readout composition**:

```text
Q106 -> (9,16,25) -> (23,53,97) -> exact scalar closure.
```

It does not establish a 53-node half, a prime-labelled adjacency-preserving
embedding, a universal prime law or a new Pascal solid.
