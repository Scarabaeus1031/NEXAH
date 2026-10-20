# Janus · PN · Handle · VM Transfer Audit — Formal Contract

Status: **formal design validation; not an admitted Study**  
Identity: reuses `A0OE:PASCAL_PENTAGON_D5_TEST`; creates none.

## M1 — Prime six-step translation

Use one-based prime indices. Test

`p_25=97`, `p_27=103`, `p_29=109`

and the translated year row

`1836 + (97,103,109) = (1933,1939,1945)`.

Both rows must have constant first difference `+6`. The translation is exact;
it does not establish historical causation.

## M2 — Nested Janus centers and the 7/6 handle

Declare additive involutions `J_s(x)=s-x`.

- `J_206` exchanges `97` and `109` and fixes `103`.
- `J_3878` exchanges `1933` and `1945` and fixes `1939`.
- `tau(t)=t-1836` must intertwine them:
  `tau(J_3878(t))=J_206(tau(t))`.
- `J_212` exchanges `103` and `109` and fixes `106`.

Thus `103` is the center of the full prime triad, while `106` is the center
of its right half-interval. It is not a prime member of that triad.

For the proposed handle, test `7+6=13=p_6` and `7*6=42`. Addition and
multiplication remain distinct. Also test that `42` is bracketed by
`p_13=41` and `p_14=43`; this is an exact neighbor fact, not a selector law.
The standard one-based indexing boundary is explicit: `53=p_16`,
`106=2p_16`, and `p_19=67`.

The stronger prime-lattice form is also tested:

- `(p_4,p_6,p_8)=(7,13,19)`;
- `(p_25,p_27,p_29)=(97,103,109)`;
- `(p_742,p_744,p_746)=(5647,5653,5659)`.

All three have index steps `+2,+2` and value steps `+6,+6`. A bounded scan
through starts `k=1..1000` counts all such double chains; recurrence is
reported rather than uniqueness claimed.

## M3 — Dual-carrier residuals

Against carrier `1729`, test

`(1933,1939,1945)-1729 = (204,210,216)`.

Required factorizations are `204=12*17`, `210=2*3*5*7`, and `216=6^3`.
Against carrier `1836`, the residuals are the prime row `(97,103,109)`.
The carrier gap is `1836-1729=107=p_28`.

The two-by-three residual matrix must have zero mixed second difference.
Therefore the raw carrier/year table is additive and supplies no nonlinear
interaction term.

## M4 — Suffix prime-index transfer

For the suffix row `(29,33,45)`, apply `P(k)=p_k`:

`(29,33,45) -> (109,137,197)`.

Input intervals are `(4,12)` and output intervals `(28,60)`, giving local
gains `(7,5)`. The decrease `7 -> 5` is a two-interval observation only.
It is not sufficient to identify a damping function.

The final two outputs satisfy `137=20*6+17` and `197=20*9+17`. A finite
control scans all starts `a=1..100` with index pattern `(a,a+4,a+16)`.

Also test the typed bridge `1929=1000+929` and
`P(1929 mod 100)=p_29=109=1945-1836`.

## M5 — 1461/5653 handle

Keep three operations separate:

- decimal reversal `R_4(3565)=5653`;
- additive Janus map `J_3565(x)=3565-x`, which exchanges `1729` and `1836`;
- split-coordinate proposal
  `F(100a+p_k)=100(4a)+p_(k-2)`.

Test `1461=100*14+p_18`, `14=2*7`, `18=2*3^2`, and
`F(1461)=100*56+p_16=5653`, with `56=7*8`, `p_16=53`, and
`5653=p_744`. Its role as the center of `(p_742,p_744,p_746)` is a separate
prime-lattice fact. A permutation control counts all distinct decimal
permutations of `3565` that are prime.

## M6 — VM alias boundary

The supplied sources use VM/vm for several roles: a vertical axis, a
contraction branch, a Vorstellungs-Medium, and a label in a time-ring visual.
These roles are recorded as distinct source-typed aliases. No equality or
operator correspondence is inferred from spelling alone.

## M7 — First-four-prime radix grammar

Freeze `(p_1,p_2,p_3,p_4)=(2,3,5,7)` and define the ordered radix join
`C_b(a,c)=ba+c` for `b>=8`. The declared pairing is outer `(2,7)` and inner
`(3,5)`, giving the decimal views `27,72,35,53` at `b=10`.

The structural identities are

`2*5=3+7=10`, `2*3=6`, and `2+5=7`.

Therefore, for every declared radix,

`A_b=2*C_b(5,3)=10b+6`,

`B_b=C_b(7,2)+C_b(3,5)=10b+7`,

so `B_b-A_b=1`. At `b=10`, `(A_10,B_10)=(106,107)`. This is the
base-independent algebraic core; the decimal factorizations remain
base-specific.

Test the decimal views:

- `27=3^3`;
- `72=6*12=8*9`;
- `35=5*7`;
- `53=p_16`;
- `gcd(27,72)=9`, `lcm(27,72)=216=6^3`;
- `53-35=18=2*9=3*6`;
- `72*6=432=27*16=2^4*3^3`;
- with `L=216`, `432=2L`, `1729=8L+1`, `1945=9L+1`, and
  `27*72=9L=1944=1945-1`;
- `40=2^3*5`, `41=p_13`, `42=6*7`, with `J_82` fixing `41`.

The 6/9 coupling is typed as `6=2*3`, `9=3^2`, `9/6=3/2`,
`9-6=3`, `9+6=15=3*5`, and `lcm(6,9)=18`. The visual resemblance `5/S`
is an added cartographic mnemonic, not a numerical equality.

The `L=216` contact with the historical carrier and endpoint is recorded as a
post-hoc exact coordinate relation, not as evidence of historical causation.

All three pair partitions and both orientations are enumerated as a control.
The value `107` must not be called unique merely because the selected pairing
produces it.

## Outcome rule

Return `PASS_EXACT_JANUS_PN_SIX_STEP_INTERTWINER_WITH_RADIX_GRAMMAR_AND_DAMPING_OPEN` only
when every exact arithmetic and source-integrity check passes while the
damping law and VM unification remain explicitly open.
