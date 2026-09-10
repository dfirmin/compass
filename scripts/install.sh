#!/usr/bin/env bash
set -euo pipefail

# Compass installer. No plugin marketplace, no npx: this script is the
# supported install path.
#
# Default is a per-project install into the repo you run it from:
#
#   ./.agents/skills   copied   (Codex, Cursor; committed with the repo so
#                               teammates and CI get the same skills)
#   ./.claude/skills   symlink -> ./.agents/skills (Claude Code; one copy on disk)
#
# Usage:
#   scripts/install.sh              per-project, from the current directory (default)
#   scripts/install.sh --user       into ~/.claude/skills and ~/.agents/skills
#                                   instead (symlinks into this checkout)
#   scripts/install.sh --copy       force copies everywhere
#   scripts/install.sh --link       force symlinks everywhere
#   scripts/install.sh --uninstall  remove whatever a previous run installed
#
# Re-run after `git pull` in the Compass checkout to refresh a project install.

REPO="$(cd "$(dirname "$0")/.." && pwd)"
MODE=""
SCOPE="project"
ACTION="install"

for arg in "$@"; do
  case "$arg" in
    --copy) MODE="copy" ;;
    --link) MODE="link" ;;
    --project) SCOPE="project" ;;
    --user) SCOPE="user" ;;
    --uninstall) ACTION="uninstall" ;;
    -h|--help) sed -n '3,22p' "$0"; exit 0 ;;
    *) echo "unknown argument: $arg" >&2; exit 2 ;;
  esac
done

if [ "$SCOPE" = "user" ]; then
  DESTS=("$HOME/.claude/skills" "$HOME/.agents/skills")
  [ -z "$MODE" ] && MODE="link"
else
  DESTS=("$PWD/.agents/skills")
  [ -z "$MODE" ] && MODE="copy"
fi

# deprecated/ is retired and misc/ is unpromoted; neither is installed.
names=()
srcs=()
while IFS= read -r -d '' skill_md; do
  src="$(dirname "$skill_md")"
  names+=("$(basename "$src")")
  srcs+=("$src")
done < <(find "$REPO/skills" -name SKILL.md -not -path '*/node_modules/*' -not -path '*/deprecated/*' -not -path '*/misc/*' -print0)

for DEST in "${DESTS[@]}"; do
  if [ -L "$DEST" ]; then
    resolved="$(readlink -f "$DEST")"
    case "$resolved" in
      "$REPO"|"$REPO"/*)
        echo "error: $DEST is a symlink into this repo ($resolved)." >&2
        echo "Remove it (rm \"$DEST\") and re-run; the script will recreate it as a real dir." >&2
        exit 1
        ;;
    esac
  fi

  mkdir -p "$DEST"

  for i in "${!names[@]}"; do
    name="${names[$i]}"
    src="${srcs[$i]}"
    target="$DEST/$name"

    if [ "$ACTION" = "uninstall" ]; then
      if [ -e "$target" ] || [ -L "$target" ]; then
        rm -rf "$target"
        echo "removed $target"
      fi
      continue
    fi

    # replace whatever is there, link or dir
    if [ -e "$target" ] || [ -L "$target" ]; then
      rm -rf "$target"
    fi

    if [ "$MODE" = "copy" ]; then
      cp -R "$src" "$target"
      echo "copied $name -> $target"
    else
      ln -sfn "$src" "$target"
      echo "linked $name -> $target"
    fi
  done
done

# Project scope: Claude Code reads .claude/skills; point it at the same files.
if [ "$SCOPE" = "project" ]; then
  mkdir -p "$PWD/.claude"
  if [ "$ACTION" = "uninstall" ]; then
    [ -L "$PWD/.claude/skills" ] && rm "$PWD/.claude/skills" && echo "removed $PWD/.claude/skills"
  else
    if [ -e "$PWD/.claude/skills" ] && [ ! -L "$PWD/.claude/skills" ]; then
      echo "note: $PWD/.claude/skills exists as a real directory; leaving it alone. Symlink it to .agents/skills yourself if you want one copy." >&2
    else
      ln -sfn "../.agents/skills" "$PWD/.claude/skills"
      echo "linked .claude/skills -> ../.agents/skills"
    fi
  fi
fi

if [ "$ACTION" = "install" ]; then
  echo
  echo "Installed ${#names[@]} skills. Restart your agent session, then run /setup-compass once per repo."
fi
