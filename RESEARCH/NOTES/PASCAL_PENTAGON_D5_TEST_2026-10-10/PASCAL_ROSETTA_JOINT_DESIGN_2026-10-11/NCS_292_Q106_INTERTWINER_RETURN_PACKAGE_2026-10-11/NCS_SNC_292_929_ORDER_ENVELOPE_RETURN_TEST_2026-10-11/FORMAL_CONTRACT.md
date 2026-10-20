# NCS–SNC 292/929 Order, Envelope & Return — formal contract

Date: `2026-10-11`  
Identity: reuse `SCC-003 / A0OE:PASCAL_PENTAGON_D5_TEST`  
Class: bounded formal design validation; not an admitted Study

## Declared finite operators

The parent package already validates the following maps on

```text
X40 = C5 x P4 x C2.
```

This extension gives them short candidate names:

```text
N(s,p,e) = ( s+1 mod 5, p, e)       navigation / rotation
S(s,p,e) = (-s   mod 5, p, 1-e)     dihedral mirror
C(s,p,e) = ( s,        p, 1-e)      commuting closure flip
```

Words execute from left to right. For example, `NCS(x)` means first `N`, then
`C`, then `S`.

This naming is a declared test convention. The historical animation recovers
only a common planar translation with identity label action. It does not
decompose the letters `NCS` into these three maps.

## S3 order scan

The complete order family is

```text
NCS, NSC, CNS, CSN, SNC, SCN.
```

Every word is compiled as a permutation of all 40 states. Equality is exact,
not visual. The test records the number of distinct maps and the multiplicity
of every order class.

## ALGO / OLGO / OKO measurement stack

The three names are used as typed measurement roles:

- **ALGO / ratios:** fixed-state ratio, moved-state ratio, package-preservation
  ratio, layer-preservation ratio and the exact reciprocal digit ratios of the
  `292 <-> 929` address pair.
- **OLGO / mirror:** orientation sign, reflection axis and the exact conjugacy
  relation `f N f = N^-1`.
- **OKO / topology:** cycle profile, permutation order, one-pass fixed set and
  exact two-pass return.

The **Envelope** is the finite set of distinct measurement signatures across
all six words. It is not a fourth operator.

**Operator 16** is the combined ALGO–OLGO–OKO record. The ordinal label does
not imply sixteen component operators. A separate `2^4` sixteen-state carrier
may be compared later, but no source map to it is declared here.

## Typed 292/929 registers

The test keeps four registers separate:

```text
929                 integer prime address
0.929               normalized metric candidate
1069/365 ~= 2.929   ratio target candidate
2929 = 29 * 101     exact integer joint
```

`292` and `929` are complementary decimal palindromes. `2929` is not a
palindrome; its decimal reversal is `9292`. Equal digits across unlike
registers are correspondence labels, not mathematical identities.

## W20 correction

The frozen Q106 table is searched directly for weight `20`. The candidate is
accepted only if the selected nodes form one complete D5 orbit. Node count and
weight are reported independently:

```text
5 nodes x weight 20 = weighted subtotal 100
```

This is not a decomposition into five 20-node blocks.

## Decision boundary

The package may report exact arithmetic, exact finite permutation classes,
the W20 orbit and one-/two-pass return inside the declared model. It must stop
before claiming a historical N/S/C decomposition, a 292/929-to-X40 address
map, a canonical ALGO/OLGO/OKO Operator registry entry, an action on the
separate sixteen-state carrier, or any physical mechanism.
