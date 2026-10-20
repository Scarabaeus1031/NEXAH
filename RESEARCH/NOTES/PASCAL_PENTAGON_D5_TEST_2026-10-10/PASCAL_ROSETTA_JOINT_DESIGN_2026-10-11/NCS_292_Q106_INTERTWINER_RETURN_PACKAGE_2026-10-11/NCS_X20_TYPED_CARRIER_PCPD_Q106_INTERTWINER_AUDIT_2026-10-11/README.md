# NCS X20 typed carrier · Pc/Pd · Q106 intertwiner audit

This package executes the next closed-gate step beneath
`A0-BL-023:NCS_292_Q106_INTERTWINER_RETURN_PACKAGE:V1`.

## Result

The source review is complete and returns:

```text
PASS_SOURCE_AUDIT_WITH_UNRECOVERED_CONTRACT
classification = SOURCE_CONTRACT_UNRECOVERED
x20_edge_set = null
x20_edge_types = null
triple19_to_x20_map = null
typed_intertwiner_to_q106 = null
```

The result localizes the missing object. The NCS sources define X20 as a
twenty-state set with C5 rotation, but not as a graph. Triple-19 defines the
constructors `P_c`, `P_d` and the antipode involution `A` on a separate
fourteen-state oriented carrier, but no map into X20.

The 24 inherited D5-equivariant charts are retained in
`X20_CHART_GATE.csv`. All remain blocked before target comparison; none is
ranked or selected.

## Files

- `CONTRACT.json` — frozen question, gates, outcomes and authority boundary;
- `SOURCE_LEDGER.json` — hash-bound source typing and null-map ledger;
- `FORMAL_CONTRACT.md` — mathematical contract and interpretation;
- `verify_x20_typed_carrier_pcpd_q106.py` — deterministic verifier;
- `X20_SOURCE_STATES.csv` — the twenty declared state coordinates;
- `X20_CHART_GATE.csv` — the twenty-four blocked D5 chart candidates;
- `RESULT.json` — machine-readable result.

## Replay

```bash
python3 verify_x20_typed_carrier_pcpd_q106.py
```

This is formal design validation during Structure Freeze. It changes no
canonical counts, lifecycle, evidence authority or publication state.
