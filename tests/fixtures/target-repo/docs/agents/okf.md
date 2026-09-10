---
type: Agent Config
title: "OKF frontmatter for documents Compass writes"
generated: { by: compass/setup-compass, at: 2026-09-10T20:10:00Z }
---
# OKF frontmatter for documents Compass writes

Every markdown document a Compass skill creates or updates in this repo is an [Open Knowledge Format](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) v0.2 concept: YAML frontmatter with a `type`, then the body. This makes the repo's knowledge ingestible by any OKF consumer without a migration later.

## The block

```yaml
---
type: <Type>                                   # required; vocabulary below
title: <display name>                          # recommended
description: <one sentence>                    # recommended
generated: { by: compass/<skill>, at: <ISO 8601 UTC> }   # who wrote the current content
verified: { by: human:<id>, at: <ISO 8601 UTC> }         # only after the user confirms it
status: stable                                 # draft | stable | deprecated; omit means stable
sources:                                       # only when the content derives from something
  - id: <short-key>
    resource: <URL or bundle-relative path>
    title: <label>
---
```

Rules:

- `generated.by` is `compass/<skill-name>` (for example `compass/probe-with-docs`). `generated.at` is the time of the last meaningful content change; update it on every edit, never on reformatting.
- `verified` is added only when the user has read and confirmed the content in the session. Use their actor id, `human:dfirmin`. Never mark something verified on the user's behalf.
- On updating an existing document, preserve every frontmatter key you don't understand.
- Cite claims from a `sources` entry with a footnote whose label is that entry's `id`: `... sharded daily.[^ga4-schema]`. Footnote labels must match a `sources[].id`.
- `index.md` and `log.md` are reserved OKF names; never use them for a concept document.
- Bundle-relative links start at the repo root (`/docs/adr/0003-...md`) and are preferred over `../` paths.

## Type vocabulary

| Document | `type` |
| --- | --- |
| `CONTEXT.md` | `Glossary` |
| `CONTEXT-MAP.md` | `Context Map` |
| `docs/adr/NNNN-*.md` | `ADR` |
| `docs/agents/*.md` (these files) | `Agent Config` |
| Research findings file | `Research` |
| Handoff document | `Handoff` |
| `to-questionnaire-*.md` | `Questionnaire` |
| `.out-of-scope/*.md` | `Out of Scope` |
| Local tracker `spec.md` / `issues/NN-*.md` / `map.md` | `Spec` / `Issue` / `Scout Map` |
| Architecture diagram document | `Diagram` |

Anything not listed: pick a short, self-explanatory `type` and add it to this table.

## ADR status

OKF `status` is `draft | stable | deprecated`. The ADR lifecycle is finer, so an ADR carries both:

| `adr_status` | `status` |
| --- | --- |
| `proposed` | `draft` |
| `accepted` | `stable` |
| `deprecated` | `deprecated` |
| `superseded` | `deprecated`, plus `superseded_by: /docs/adr/NNNN-slug.md` |
