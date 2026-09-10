---
type: Agent Instructions
title: "Compass maintainer instructions"
description: "Repo conventions every agent editing Compass must follow."
generated: { by: compass-port/0.1.0, at: 2026-09-10T19:44:27Z }
---
# Compass

Compass is our agent-skills repo, adapted from [mattpocock/skills](https://github.com/mattpocock/skills) (MIT). It keeps that repo's shape and discipline and extends it toward our work: ETL generation across warehouses, AWS infrastructure, and the front-end/TypeScript apps we still own. See `CONTEXT.md` for the vocabulary.

Skills are organized into bucket folders under `skills/`:

- `engineering/`: daily code work
- `productivity/`: daily non-code workflow tools
- `misc/`: kept around but rarely used, not promoted
- `in-progress/`: beta: try them, feedback wanted
- `deprecated/`: no longer used

Every skill in `engineering/` or `productivity/` (the **promoted** buckets) must have a reference in the top-level `README.md`. Skills in `misc/`, `in-progress/`, and `deprecated/` must not.

Install is a clone plus `scripts/install.sh`; the wording is copied verbatim from [.agents/install-block.md](./.agents/install-block.md). There is no plugin manifest and no `npx` route; don't add one.

Each skill entry in the top-level `README.md` must link the skill name to its `SKILL.md`.

Each bucket folder has a `README.md` that lists every skill in the bucket with a one-line description, with the skill name linked to its `SKILL.md`. The promoted buckets' `README.md`s and the top-level `README.md` group entries into **User-invoked** and **Model-invoked**; non-promoted bucket `README.md`s (`misc/`, `in-progress/`) use a flat list.

Skills in `engineering/` and `productivity/` also have a human-facing docs page at `docs/<bucket>/<skill-name>.md`. The docs tree mirrors those two bucket folders under `skills/`. When you add, rename, or change the behaviour of a promoted skill, create or re-sync its docs page following [.agents/writing-docs.md](./.agents/writing-docs.md). Skills in the non-promoted buckets get **no** docs page.

Every `SKILL.md` is either user-invoked (`disable-model-invocation: true` plus `policy.allow_implicit_invocation: false` in `agents/openai.yaml`, reachable only by the human) or model-invoked (model- or user-reachable). See [.agents/invocation.md](./.agents/invocation.md).

[`ask-compass`](./skills/engineering/ask-compass/SKILL.md) is the router that maps every user-reachable skill and how they relate. Whenever you add, rename, remove, or change how a user-reachable skill fits the flows, re-read `ask-compass`'s `SKILL.md` and update it so the map stays accurate: a new skill it never mentions, or a stale one it still routes to, is a router that lies.

## Compass-wide rules

- **Plain-language questions.** Every decision question a skill puts to the user carries an **In plain terms** restatement a non-technical stakeholder could answer. The `probing` template carries the line; `setup-compass` writes the rule into each target repo's `AGENTS.md`/`CLAUDE.md` via `docs/agents/plain-language.md`. A new skill that asks questions follows it.
- **No per-platform skills.** Don't add `etl-databricks`, `web-typescript`, or similar. Skills generalize; repo-specific facts (platform, dialect, deployment target, standards to pull in) live in the target repo's `docs/agents/*.md` written by `setup-compass`.
- **Diagrams as a required artifact** alongside `CONTEXT.md`, `AGENTS.md`, and ADRs: not yet implemented; see `.agents/roadmap.md`.
- **Company-skill integration** (API, Engineering Security, AWS standards): not yet implemented; see `.agents/roadmap.md`.

To (re)install every promoted skill, run `scripts/install.sh` from a target repo (per-project) or with `--user`; re-run it after adding, removing, or renaming a skill.

## OKF

This repo is an [Open Knowledge Format](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) v0.2 bundle. Every non-reserved `.md` carries frontmatter with a `type` (`Skill`, `Skill Doc`, `Reference`, `Template`, `ADR`, `Glossary`, `Agent Instructions`), a `generated: { by, at }` actor, and `sources` where the content derives from upstream. `index.md` files are generated, never hand-edited: run `scripts/okf.py index` after adding, removing, or renaming a document, and `scripts/okf.py check` before committing (CI runs both). `log.md` at the root is the update log, newest first under ISO date headings; `README.md` files stay as the human-facing narrative. New documents get their frontmatter from `scripts/okf.py stamp`.

The skills also **write** OKF: every template a skill emits into a target repo (`CONTEXT.md`, ADRs, `docs/agents/*.md`, research files, handoffs, questionnaires, out-of-scope notes, local tracker files, `teach` workspaces) starts with the block defined in `skills/engineering/setup-compass/okf.md`, which `setup-compass` copies into the target as `docs/agents/okf.md`. `generated.by` is `compass/<skill>`; `verified` is added only after the user confirms. A new skill that writes markdown follows the same seed and adds its `type` to that table. `tests/fixtures/target-repo/` is a repo populated exactly as the templates say; `scripts/test.sh` checks it (and this repo) with `okf.py check --strict`, run it before committing template changes.

No em-dashes anywhere in this repo's prose. Where a sentence reaches for one, rewrite it with a comma, colon, period, parentheses, or a conjunction.
