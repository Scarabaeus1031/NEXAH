# D30 extension contract

Status: `FORMAL_DESIGN_VALIDATION / NON-EXECUTED-SCIENCE BOUNDARY`

## 1. Reused source

The source is the frozen depth-six, five-face SCC-003 incidence carrier

```text
X = C5 x {(n,k) | 0 <= k <= n <= 6}.
```

No new graph or canonical identity is introduced.

The five existing face addresses are exposed as registers

```text
Dj <-> f=j-1,  j in {1,2,3,4,5}.
```

`D1..D5` denotes this address view. `D5` without an index remains the
order-ten dihedral symmetry group; the two uses are not identities.

## 2. D30 phase compiler

Define

```text
p30(f,n,k) = 2k-n mod 30
F30(f,n,k) = (f, f+k mod 5, n mod 6, p30).
```

For the raw branch maps

```text
tL(f,n,k) = (f,n+1,k)
tR(f,n,k) = (f,n+1,k+1)
```

define

```text
TL(a,b,d,p) = (a,b,  d+1,p-1)
TR(a,b,d,p) = (a,b+1,d+1,p+1).
```

Then `F30 o tL = TL o F30` and `F30 o tR = TR o F30` on all 210 frozen
face-edge incidences.

## 3. Reflection compiler

On the 30-phase circle let

```text
S0(theta) = -theta
F6(theta) = 12deg-theta.
```

The ordered products satisfy

```text
S0 o F6 = rotation -12deg = TL
F6 o S0 = rotation +12deg = TR.
```

The raw reflection `m(f,n,k)=(-f,n,n-k)` is compiled as `p -> -p`.
On the D-registers it fixes `D1`, exchanges `D2<->D5` and exchanges
`D3<->D4`. Rotation sends `Dj` to `D(j mod 5)+1`.

## 4. D-register phase cover

The register-phase view is

```text
VD(f,n,k) = (D(f+1), p30(f,n,k)) in C5_D x C30_P.
```

It has capacity `150`, of which `65` positions occur at frozen depth six.
Each register contains `28` raw incidences and `127` branch words, but only
`13` phase values. `VD` is therefore not injective. The refined view

```text
VD+(f,n,k) = (D(f+1), n, p30(f,n,k))
```

is injective on all 140 frozen incidences.

## 5. Word semantics

For a word `w` over `{L,R}` with length `n` and `k=#R(w)`, the endpoint and
phase are

```text
endpoint(w) = (n,k)
phase(w) = #R(w)-#L(w) = 2k-n mod 30.
```

The endpoint multiplicity is `binomial(n,k)`. Word order is provenance that
the Pascal lattice intentionally forgets; the endpoint is not a claim of a
unique history.

## 6. Non-factorization through the C12 gear

For the old carrier `G=C5^2 x C6 x C12`, every homomorphism to `C30` has the
form

```text
chi(a,b,d,q) = xa+yb+zd+wq mod 30,
```

where `x,y` are multiples of six and `z,w` are multiples of five. Therefore
the left increment `z-w` is always divisible by five and cannot equal `-1`.
No such character realizes the signed unit branch schedule.

## 7. Separate 30-point carriers

The following equal cardinalities do not establish identity:

- `C30_P`: one directed 30-phase coordinate cycle;
- H3 root carrier: 30 vertices with a three-cycle Coxeter decomposition
  `10+10+10`;
- E8 Coxeter coordinates: eight oriented 30-cycles.

An E8 coordinate adapter is parameterized by `(lane, origin, orientation)`.
There are 480 such charts and no declared selector. H3 remains a separate
geometry carrier.

## 8. Return and claim ceiling

`F30` is injective on the 140 raw incidences, so exact raw return is available
on its image. Passing this audit establishes only the stated finite algebraic
contract. It does not establish a unique E8 adapter, H3/E8/Pascal identity,
physical gear, calendar law, resonance, new Family, `PENT-08`, admitted Study,
publication status or behavior beyond depth six.
