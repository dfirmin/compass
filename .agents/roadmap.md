---
type: Reference
title: "Roadmap"
description: "Planned order of work: port (done), diagrams, company-skill integration."
generated: { by: compass-port/0.1.0, at: 2026-09-10T19:44:27Z }
---
# Roadmap

Planned order, agreed before the port. Step 1 is done; 2 and 3 are open.

1. **Port and rename** (done). Followed by OKF v0.2 (done): Compass itself is a bundle, and every document the skills write into a target repo carries OKF frontmatter (`setup-compass/okf.md`, `scripts/okf.py`, `scripts/test.sh`). Adapted from mattpocock/skills. Renames: `ask-matt` → `ask-compass`, `setup-matt-pocock-skills` → `setup-compass`, `grilling` → `probing`, `grill-me` → `probe-me`, `grill-with-docs` → `probe-with-docs`, `wayfinder` → `scout`. Everything else keeps its name. Plugin and `npx` packaging removed in favour of `scripts/install.sh`. Plain-language question line added to `probing` and written into target repos by `setup-compass`.

2. **Diagrams as a required artifact.** Architectural diagrams (Mermaid in-repo, so they diff and review like code) become a first-class output next to `CONTEXT.md`, `AGENTS.md`, and ADRs. In OKF terms a diagram is a concept with `type: Diagram` (already reserved in the type table) and a `resource` pointing at the `.mmd` file. Open questions: which skills produce them (`probe-with-docs`, `to-spec`, `implement`?), where they live (`docs/diagrams/`? beside the ADR they support?), and what `domain-modeling`'s "update inline" rule means for a diagram.

3. **Company-skill integration.** Workflows that pull in our internal API, Engineering Security, and AWS standards skills when relevant. Likely shape: `setup-compass` asks which company skill sets apply to this repo and records pointers in `docs/agents/`, and `ask-compass` / `implement` / `code-review` consult those pointers. Must stay generic: no per-platform skill folders.
