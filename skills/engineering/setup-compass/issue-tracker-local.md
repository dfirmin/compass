---
type: Template
title: "Issue tracker: Local Markdown"
generated: { by: compass-port/0.1.0, at: 2026-09-10T19:44:27Z }
sources:
  - id: upstream
    resource: /NOTICE.md
    title: Upstream skills repository (see NOTICE.md)
---
<!-- Target-repo frontmatter: keep the block below (fill `at`) when writing this file into docs/agents/ -->
```yaml
---
type: Agent Config
title: "Issue tracker: Local Markdown"
generated: { by: compass/setup-compass, at: <ISO 8601 UTC> }
---
```

# Issue tracker: Local Markdown

Issues and specs for this repo live as markdown files in `.scratch/`.

## Conventions

- One feature per directory: `.scratch/<feature-slug>/`
- The spec is `.scratch/<feature-slug>/spec.md`
- Implementation issues are one file per ticket at `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01`, never a single combined tickets file
- Triage state is recorded as a `Status:` line near the top of each issue file (see `triage-labels.md` for the role strings)
- Comments and conversation history append to the bottom of the file under a `## Comments` heading
- Every file carries OKF frontmatter (`docs/agents/okf.md`): `type: Spec` for `spec.md`, `type: Issue` for tickets, `type: Scout Map` for a scout map, with `title` and `generated: { by: compass/<skill>, at: ... }`. The `Status:` / `Type:` / `Blocked by:` body lines stay as they are; they are the tracker's state, not OKF's

## When a skill says "publish to the issue tracker"

Create a new file under `.scratch/<feature-slug>/` (creating the directory if needed).

## When a skill says "fetch the relevant ticket"

Read the file at the referenced path. The user will normally pass the path or the issue number directly.

## Scouting operations

Used by `/scout`. The **map** is a file with one **child** file per ticket.

- **Map**: `.scratch/<effort>/map.md` (the Notes / Decisions-so-far / Fog body).
- **Child ticket**: `.scratch/<effort>/issues/NN-<slug>.md`, numbered from `01`, with the question in the body. A `Type:` line records the ticket type (`research`/`prototype`/`probing`/`task`); a `Status:` line records `claimed`/`resolved`.
- **Blocking**: a `Blocked by: NN, NN` line near the top. A ticket is unblocked when every file it lists is `resolved`.
- **Frontier**: scan `.scratch/<effort>/issues/` for files that are open, unblocked, and unclaimed; first by number wins.
- **Claim**: set `Status: claimed` and save before any work.
- **Resolve**: append the answer under an `## Answer` heading, set `Status: resolved`, then append a context pointer (gist + link) to the map's Decisions-so-far in `map.md`.
