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

To (re)install every promoted skill into the local harness directories, run `scripts/install.sh`; re-run it after adding, removing, or renaming a skill.

No em-dashes anywhere in this repo's prose. Where a sentence reaches for one, rewrite it with a comma, colon, period, parentheses, or a conjunction.
