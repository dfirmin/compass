#!/usr/bin/env bash
# Runs the OKF checks Compass promises: this repo is a conformant bundle, and a
# repo populated exactly as the skill templates instruct is conformant too
# (tests/fixtures/target-repo). Also proves the strict checks catch the
# mistakes an agent is most likely to make.
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
OKF="$REPO/scripts/okf.py"

python3 "$OKF" check --strict
python3 "$OKF" check "$REPO/tests/fixtures/target-repo" --strict

# index.md files must match what the generator produces from the working tree
snap="$(mktemp -d)"; cp -r "$REPO/." "$snap"; rm -rf "$snap/.git"
python3 "$snap/scripts/okf.py" index >/dev/null
if ! diff -rq "$REPO" "$snap" -x .git | grep -v '^$' | grep -q . ; then :; else
  diff -rq "$REPO" "$snap" -x .git | grep index.md && { echo "index.md files are stale; run scripts/okf.py index" >&2; rm -rf "$snap"; exit 1; }
fi
rm -rf "$snap"

# negative cases: copy the fixture, break it four ways, expect exactly those four errors
tmp="$(mktemp -d)"; cp -r "$REPO/tests/fixtures/target-repo/." "$tmp"
sed -i 's/adr_status: accepted/adr_status: proposed/' "$tmp/docs/adr/0002-dedupe-on-hash.md"
sed -i 's/\[\^sf-merge\]/[^sf-merg]/' "$tmp/research/snowflake-merge-limits.md"
sed -i 's#by: compass/to-spec#by: to-spec#' "$tmp/.scratch/etl-dedupe/spec.md"
out="$(python3 "$OKF" check "$tmp" --strict 2>&1 || true)"
for expect in "has no sources\[\].id" "is never cited" "actor not in OKF convention" "requires status draft"; do
  echo "$out" | grep -q "$expect" || { echo "strict check missed: $expect" >&2; echo "$out"; exit 1; }
done
echo "$out" | grep -q "^4 problem(s)" || { echo "expected exactly 4 problems" >&2; echo "$out"; exit 1; }
rm -rf "$tmp"
echo "all OKF tests passed"
