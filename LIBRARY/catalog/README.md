# NEXAH Website Catalog

This directory is a read-only, non-canonical catalog overlay for the public
NEXAH Library on Are.na.

It exists to support a future human-facing website. It does not allocate
Registry identities, promote Proposals, define Series, modify Operators, or
write to Are.na.

## What is captured

Each public Work receives one source-keyed record under `works/` containing:

- its stable public Are.na Channel identity and URL;
- live title and Channel description;
- current editorial classification from the Library review;
- a cover reference without copying the image into the repository;
- the ordered public Blocks and their source titles;
- structural signals for Foreword, Index, Parts, Chapters, Appendices, and closing pages;
- explicit evidence boundaries for everything not yet reviewed.

`website_catalog.yaml` is the compact website index. The detailed Work records
remain separate so that the catalog can grow without turning into one enormous
file.

## Evidence boundary

Are.na exposes image metadata and Block titles, but it does not expose text
rendered inside an uploaded image. Therefore:

- Channel descriptions and Block titles are source evidence;
- page roles are conservative machine-assisted structural observations;
- text inside Foreword, Index, or content pages is **not extracted**;
- semantic summaries are **not generated** by this pass.

A later human or visual review may enrich selected research books, atlases,
reports, and whiteboards. Journey Works remain bibliographic and dramaturgic
unless explicitly reviewed.

## Editorial shelves

`catalog_overrides.yaml` records website-only shelves and corrections supplied
by the human editor. A shelf is a discovery surface, not canonical identity. A
Work may appear on more than one shelf.

## Refresh

```bash
python -m nexah.library website-catalog
```

The command is GET-only. It reads the existing classification and public
Are.na state, then rebuilds the catalog records. It never reads a write token.
