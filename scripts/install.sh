#!/usr/bin/env bash
set -euo pipefail

# Compass installer. No plugin marketplace, no npx: this script is the
# supported install path.
#
# It puts every promoted skill (engineering/, productivity/, plus in-progress/)
# into the skill directories the agent harnesses read:
#
#   ~/.claude/skills   Claude Code
#   ~/.agents/skills   Codex, Cursor, and other Agent Skills harnesses
#                      (Cursor also reads ~/.claude/skills, so both are covered)
#
# Usage:
#   scripts/install.sh              symlink into the user-level dirs (default)
#   scripts/install.sh --copy       copy instead of symlink (Windows, locked-down
#                                   machines, or when you want a frozen snapshot)
#   scripts/install.sh --project    install into ./.claude/skills and
#                                   ./.agents/skills of the current working
#                                   directory instead of the home dirs
#   scripts/install.sh --uninstall  remove whatever a previous run installed
#
# Symlinks track this checkout: `git pull` updates every installed skill.
# Copies don't: re-run with --copy to refresh.

REPO="$(cd "$(dirname "$0")/.." && pwd)"
MODE="link"
SCOPE="user"
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
else
  DESTS=("$PWD/.claude/skills" "$PWD/.agents/skills")
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

if [ "$ACTION" = "install" ]; then
  echo
  echo "Installed ${#names[@]} skills. Restart your agent session, then run /setup-compass once per repo."
fi
