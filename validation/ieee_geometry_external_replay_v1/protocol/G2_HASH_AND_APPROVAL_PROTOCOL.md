# G2 Hash and Approval Protocol

Status: **mechanism proposed; approval record not yet created**

## Candidate bytes

The complete machine-readable comparator and analysis contract is
`protocol/g2_protocol_candidate.json`.

Its canonical byte convention is:

- UTF-8 without BOM;
- JSON object with keys sorted recursively by the serializer;
- two-space indentation;
- Unix LF line endings;
- exactly one trailing LF;
- no non-finite JSON numbers.

The review digest is recorded in
`protocol/g2_protocol_candidate.sha256` using the conventional
`<lowercase-hex><two spaces><relative-path>` format.

## Approval binding

G2 approval must identify the candidate digest explicitly. After approval, the
candidate bytes are copied unchanged to `g2_protocol_approved.json` and a
separate `g2_approval_record.json` records:

- protocol ID and version;
- exact approved relative path;
- SHA-256 digest;
- approver;
- approval timestamp;
- status `approved`;
- statement that approval preceded all new IEEE-14 comparator output.

The approved JSON bytes must hash to the recorded value. Renaming the file does
not change the digest; any byte edit invalidates approval and returns the work
to G2.

## Future command separation

No comparator command is implemented at G2. G3/G4 remain closed. Any later
implementation must provide two technically separate entry points:

- development: accepts only the literal case `ieee9` and reads only the frozen
  IEEE-9 development-frame path;
- evaluation: accepts only the literal case `ieee14`, requires the approved
  protocol and approval record, verifies their SHA-256 binding before loading
  any IEEE-14 frame, and fails closed on absence or mismatch.

The development module must not import, infer, glob, enumerate, preload, or
display the IEEE-14 path or results. The evaluation entry point must be invoked
explicitly after G2 approval. No shared command may automatically run both.

