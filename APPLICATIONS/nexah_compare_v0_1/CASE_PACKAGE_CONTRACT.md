# NEXAH Compare v0.1 — Local Case Package Contract

Status: `WP4_FROZEN_LOCAL_PACKAGE_PROFILE`

## Directory layout

```text
CASE_DIR/
  package.json
  inputs/
    case.json
    alignment.json                 # optional; exact auto-alignment otherwise
    analyses/
      analysis-a.json
      analysis-b.json              # two to four total
  evidence/
    ...                            # exactly the admitted CaseRecord paths
  outputs/
    comparison.json                # generated canonical record
    report.md                       # generated faithful projection
  manifest.json                    # hashes descriptor, inputs, evidence, outputs
  receipts/
    run-receipt.json               # binds manifest, comparison and report
  returns/
    return.json                    # optional, separate Human action
```

No undeclared file, absolute path, `..` segment or symlink is admitted. The
package root itself may not be a symlink. Missing and unavailable evidence has
no file; every `ADMITTED` evidence path must exist and match its CaseRecord
SHA-256.

## Descriptor

`package.json` validates against
`package_contract/case-package.schema.json`. Its output paths are fixed so a
package cannot redirect generated material outside its root. The privacy class
must equal the CaseRecord privacy class and remains limited to `SYNTHETIC` or
`LICENSED_DEIDENTIFIED`.

Example:

```json
{
  "schema_id": "nexah.compare.case-package",
  "schema_version": "0.1.0",
  "package_id": "PKG-MARKET-ENTRY-0001",
  "profile_id": "NC01-ADVISORY-0.1",
  "privacy_class": "SYNTHETIC",
  "case_path": "inputs/case.json",
  "analysis_paths": [
    "inputs/analyses/alpha.json",
    "inputs/analyses/beta.json"
  ],
  "alignment_path": "inputs/alignment.json",
  "reference_analysis_id": "AN-MARKET-ENTRY-ALPHA",
  "comparison_path": "outputs/comparison.json",
  "report_path": "outputs/report.md",
  "manifest_path": "manifest.json",
  "receipt_path": "receipts/run-receipt.json",
  "return_path": "returns/return.json"
}
```

## Run and replay

`run-package` validates inputs and evidence, executes WP3, writes canonical
comparison JSON, derives the Markdown report, builds the file manifest and
writes the deterministic receipt. `verify-package` revalidates every schema,
recomputes every hash, replays the comparison and regenerates the Markdown in
memory. Any mismatch rejects the package.

The receipt contains no implicit clock or machine path. Its command, runtime
version, engine identity, counts and hashes are derived and compared exactly.

## Markdown boundary

`outputs/report.md` is generated only from the schema-valid ComparisonRecord.
Every relation, calculation check, residual, abstention and the claim ceiling
is projected. Input text is HTML- and table-escaped. The report adds no truth
ranking, recommendation or conclusion. Byte inequality with a fresh projection
is `MARKDOWN_PROJECTION_MISMATCH`.

## Human Return

`create-return` requires an explicit Human action, actor, statement and RFC
3339 timestamp. The resulting ReturnRecord binds the exact comparison hash.
Selected residuals and amendment targets must exist in the comparison.
`AMEND` requires at least one amendment; other actions may not smuggle
amendments. A Return blocks rerunning the package so the reviewed result cannot
be silently replaced.
