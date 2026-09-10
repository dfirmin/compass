# Compass Update Log

## 2026-09-10
* **Update**: Skills now write OKF: `setup-compass` emits `docs/agents/okf.md` (frontmatter block, type vocabulary, actor id) and every template a skill writes (`CONTEXT.md`, ADRs, research, handoff, questionnaire, out-of-scope, local tracker, `teach` formats) starts with OKF frontmatter. `scripts/okf.py check DIR --strict` validates a target repo; `scripts/test.sh` runs it against `tests/fixtures/target-repo/`.
* **Update**: Made the repo an OKF v0.2 bundle: frontmatter with `type` on every document, generated `index.md` files, this `log.md`, and `scripts/okf.py` to check and regenerate.
* **Update**: `scripts/install.sh` now defaults to per-project install (copy into `.agents/skills/`, symlink `.claude/skills/`); `--user` keeps the home-directory behaviour.
* **Initialization**: Initial port from [mattpocock/skills](https://github.com/mattpocock/skills) v1.2.3 (MIT). Renamed `ask-matt` → `ask-compass`, `setup-matt-pocock-skills` → `setup-compass`, `grilling` → `probing`, `grill-me` → `probe-me`, `grill-with-docs` → `probe-with-docs`, `wayfinder` → `scout`. Removed plugin and `npx` packaging in favour of `scripts/install.sh`. Added the **In plain terms** line to `probing` and `docs/agents/plain-language.md` to `setup-compass`.
