---
type: Skill
name: research
description: Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo. Use when the user wants a topic researched, docs or API facts gathered, or reading legwork delegated to a background agent.
generated: { by: compass-port/0.1.0, at: 2026-09-10T19:44:27Z }
sources:
  - id: upstream
    resource: https://github.com/mattpocock/skills
    title: mattpocock/skills v1.2.3
---

Spin up a **background agent** to do the research, so you keep working while it reads.

Its job:

1. Investigate the question against **primary sources** (official docs, source code, specs, first-party APIs), not a secondary write-up of them. Follow every claim back to the source that owns it.
2. Write the findings to a single Markdown file with OKF frontmatter (`type: Research`, `generated: { by: compass/research, at: ... }`; see `docs/agents/okf.md` if present). List every source consulted under `sources:` with a stable `id`, `resource` (the URL or path), `title`, and `last_modified` when the source shows one. Cite each claim with a footnote whose label is that source's `id` (`...limit is 10 MB.[^s3-docs]`); every footnote label must match a `sources[].id` and vice versa.
3. Save it where the repo already keeps such notes; match the existing convention, and if there is none, put it somewhere sensible and say where.
