# Grid–Fold–Channel / Interface Assembly Update Return Audit

This package completes the formal-design checklist of `A0-BL-025` for a
finite two-branch channel model:

```text
carrier → fold → embedding → envelope → interface
        → assembly → update → Return
```

Run:

```sh
python3 verify_grid_fold_channel_contract.py
```

The verifier uses two non-identical controls: a one-dimensional path seam with
reflection and a two-dimensional square-boundary assembly with quarter-turn
update. It tests exact assembly fibres, minimal residual information, exact
Return, update compatibility and rejection of invalid interface updates.

Generated evidence:

- `RESULT.json`
- `CONTROL_FIBRE_PROFILE.csv`
- `TYPE_AND_FAILURE_LEDGER.csv`

Passing means the formal finite contract is complete. It does not admit a
Study, establish physical flow or stability, recover a historical visual
generator, create a Navigator identity, or authorize publication.
