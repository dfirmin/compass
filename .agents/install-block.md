---
type: Reference
title: "Canonical install block"
description: "The one install wording, copied verbatim into README."
generated: { by: compass-port/0.1.0, at: 2026-09-10T19:44:27Z }
---
# The canonical install block

One install story, one wording. `README.md` and every page under `docs/` that mentions installation must say **this** and nothing else. Change it here first, then propagate.

Compass is **not** distributed as a Claude Code plugin and **not** via `npx skills`. Both routes are unavailable in our environment. The single supported route is a clone plus `scripts/install.sh`, which places every promoted skill into the directories the harnesses read.

<canonical-block name="install">

```bash
git clone https://github.com/dfirmin/compass.git ~/compass
cd /path/to/your-repo
~/compass/scripts/install.sh
```

That installs **per project**: the skills are copied into `./.agents/skills/` (which Codex and Cursor read) and `./.claude/skills/` is symlinked to it (which Claude Code reads), so there is one copy on disk and it travels with the repo. Commit `.agents/skills/` so teammates and CI get the same set; re-run the script after `git pull` in `~/compass` to refresh. Use `--user` for a machine-wide install into `~/.claude/skills/` and `~/.agents/skills/` instead (symlinks, so they track the checkout).

</canonical-block>

Then, once per repo, run `/setup-compass` inside your agent.

## Not the install story

`scripts/list-skills.sh` prints every skill path and is a maintainer aid, not an installer.
