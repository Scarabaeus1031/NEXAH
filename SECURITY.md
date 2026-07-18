# Security Policy

NEXAH is a research repository and is not presented as a production control,
decision, or autonomous execution system. Security reports are nevertheless
welcome for the maintained Python package, CLI, Editorial Writer safeguards,
and repository workflows.

## Supported surface

Security review is directed at the latest state of the default branch. Archived,
experimental, and historical artifacts are preserved for research traceability
and are not maintained as supported production software.

## Reporting

Do not open a public issue containing credentials, tokens, personal data, or
working exploit details. Use GitHub's private vulnerability-reporting mechanism
when available, or contact the repository maintainer privately through the
maintainer's GitHub profile.

Include:

- the affected path and revision;
- the conditions required to reproduce the issue;
- the likely impact and boundary of that impact;
- a minimal reproduction if it can be shared safely; and
- whether secrets or personal data may already have been exposed.

Never include an Are.na token or other secret in repository files, logs,
screenshots, issue text, or test fixtures.

## Scope boundary

A successful test, simulation, or conformance check is not a security guarantee.
NEXAH does not currently claim operational hardening, safety certification,
calibrated risk, or authorization for deployment in sensitive environments.
