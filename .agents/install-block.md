# The canonical install block

One install story, one wording. `README.md` and every page under `docs/` that mentions installation must say **this** and nothing else. Change it here first, then propagate.

Compass is **not** distributed as a Claude Code plugin and **not** via `npx skills`. Both routes are unavailable in our environment. The single supported route is a clone plus `scripts/install.sh`, which places every promoted skill into the directories the harnesses read.

<canonical-block name="install">

```bash
git clone https://github.com/dfirmin/compass.git ~/compass
~/compass/scripts/install.sh
```

Symlinks into the checkout, so `git pull` in `~/compass` updates every installed skill. On Windows, or anywhere symlinks are awkward, add `--copy` (and re-run it to refresh). Add `--project` to install into the current repo's `.claude/skills/` and `.agents/skills/` instead of your home directory.

| Harness | Reads from |
| --- | --- |
| Claude Code | `~/.claude/skills/` (or `./.claude/skills/`) |
| Codex | `~/.agents/skills/` (or `./.agents/skills/`) |
| Cursor | `~/.agents/skills/` and `~/.claude/skills/` (both written by the script), plus its own `~/.cursor/skills/` |

</canonical-block>

Then, once per repo, run `/setup-compass` inside your agent.

## Not the install story

`scripts/list-skills.sh` prints every skill path and is a maintainer aid, not an installer.
