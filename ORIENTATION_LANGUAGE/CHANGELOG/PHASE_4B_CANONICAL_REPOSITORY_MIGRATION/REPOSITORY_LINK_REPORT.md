# Repository Link Report

Scope: Markdown links below `ORIENTATION_LANGUAGE/`  
Date: 17 July 2026

## Method

Every local Markdown target was resolved relative to its containing document. HTTP, mail, and same-document anchor references were excluded from filesystem resolution.

## Result

| Metric | Result |
| --- | ---: |
| Local Markdown links checked | 85 |
| Broken local targets | 0 |
| Canonical OLS document entry links | 8 resolved |
| Manifest entry links | Resolved |
| Registry navigation links | Resolved |
| Migration record links | Resolved |

Released specification files were not edited to create path-based links. Repository navigation resolves to the immutable canonical targets; stable identifiers and the Release Manifest remain authoritative.
