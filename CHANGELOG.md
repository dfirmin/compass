# Changelog

## 0.1.0

Initial port from [mattpocock/skills](https://github.com/mattpocock/skills) v1.2.3 (MIT).

- Renamed: `ask-matt` → `ask-compass`, `setup-matt-pocock-skills` → `setup-compass`, `grilling` → `probing`, `grill-me` → `probe-me`, `grill-with-docs` → `probe-with-docs`, `wayfinder` → `scout`. Labels follow: `scout:map`, `scout:<type>`.
- Removed Claude Code plugin manifest, changesets, and `npx skills` install route. Added `scripts/install.sh` (symlink or copy; user or project scope; Claude Code, Codex, Cursor).
- `probing`: every question now carries an **In plain terms** restatement for non-technical stakeholders.
- `setup-compass`: writes `docs/agents/plain-language.md` and a `### Plain-language questions` sub-block into the target repo's `CLAUDE.md`/`AGENTS.md`.
- Docs pages: links made repo-relative; upstream attribution generalised.
