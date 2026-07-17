# Cross-Reference Strategy

## Principle

Identity and authority are independent of repository path. Every durable reference uses stable identifiers and a compatible suite version; paths are resolvers and navigation aids.

## Reference forms

| Reference type | Required key | Optional convenience |
| --- | --- | --- |
| Normative clause | Document ID + Clause or Requirement ID + suite version | Relative link and visible clause title |
| Registry entry | Owning Document ID + Annex/registry ID + entry ID + suite version | Registry export path |
| Test | OLS-5 + Test ID + test registry version | Result-file link |
| Trace | Trace ID + owning clause + suite version | Research-source link |
| Informative explanation | OLS-I section + compatible suite release | Public URL |
| Research evidence | Persistent source identity, edition/date, and provenance | Repository path |
| Library reference | Work identity/edition plus cited OLS stable ID when language is discussed | Reader-facing link |
| Application mapping | Application identity/version plus OLS IDs used | Configuration path |
| Implementation mapping | Implementation identity/version plus Requirement/Test IDs claimed | Source or package link |

## Resolution chain

```text
Stable identifier
→ release manifest
→ canonical document and compatible revision
→ checksum-verified file
→ visible repository path
```

No consumer should reverse this chain and treat a path as semantic identity.

## Relative links

Relative links are appropriate for README navigation, images, and same-release convenience. They do not replace stable IDs in normative claims. A moved file may update navigational links without changing the referenced semantic identity.

## Old paths

The migration map records:

- old path;
- new path;
- stable identity;
- status;
- effective release;
- redirect availability;
- checksum.

If the hosting platform supports redirects, old public URLs should resolve to the new canonical path. Otherwise a small non-authoritative relocation notice may remain at the old path. It shall not duplicate the normative document body.

## Cross-domain rules

- Research cites OLS only when making a statement about the published language; research findings retain research status.
- Library material cites the controlling OLS element for semantic claims and labels explanation or metaphor accordingly.
- Applications list every active profile, operator, declaration, and derivation they rely on.
- Implementations map realized behavior to Requirement and Test IDs and disclose unsupported capability.
- OLS documents cite research only for traceability or rationale; research cannot override their published definitions.

## Validation

Migration validation checks stable-ID resolution, suite compatibility, broken links, duplicate canonical targets, checksum mismatch, and normative references that rely on path alone.

