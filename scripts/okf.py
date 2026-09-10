#!/usr/bin/env python3
"""OKF v0.2 tooling for the Compass bundle. Standard library only.

  scripts/okf.py check [DIR] [--strict]
                          validate conformance of this repo, or of DIR (a
                          target repo Compass has written into); --strict
                          also checks footnote labels resolve to sources ids,
                          generated/verified actor syntax, and ADR status pairs
  scripts/okf.py index    (re)generate index.md files from frontmatter
  scripts/okf.py stamp    add missing frontmatter using the type map below

Conformance (SPEC §11): every non-reserved .md has parseable frontmatter
with a non-empty `type`; index.md carries no frontmatter (bundle root may
carry only okf_version); log.md uses ISO date headings.
"""
import os, re, sys, datetime

ARGS = [a for a in sys.argv[2:] if not a.startswith("--")]
FLAGS = {a for a in sys.argv[2:] if a.startswith("--")}
ROOT = os.path.abspath(ARGS[0]) if ARGS else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESERVED = {"index.md", "log.md"}
SKIP_DIRS = {".git", "node_modules"}
PRODUCER = "compass-port/0.1.0"
UPSTREAM = "https://github.com/mattpocock/skills"

def walk():
    for d, dirs, files in os.walk(ROOT):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
        for f in files:
            if f.endswith(".md"):
                yield os.path.join(d, f)

def rel(p): return os.path.relpath(p, ROOT)

FM_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.S)

def split(text):
    m = FM_RE.match(text)
    if not m: return None, text
    return m.group(1), text[m.end():]

def fm_get(fm, key):
    m = re.search(rf"^{re.escape(key)}:[ \t]*(.*)$", fm, re.M)
    return m.group(1).strip() if m else None

# ---- type map -------------------------------------------------------------
def type_for(p):
    r = rel(p); parts = r.split(os.sep); base = parts[-1]
    if r == "README.md": return "Reference"
    if r == "CONTEXT.md": return "Glossary"
    if r == "CLAUDE.md": return "Agent Instructions"
    if parts[0] == ".agents":
        return "ADR" if len(parts) > 1 and parts[1] == "adr" else "Reference"
    if parts[0] == "docs": return "Skill Doc"
    if parts[0] == "skills":
        if base == "SKILL.md": return "Skill"
        if base == "README.md": return "Reference"
        if len(parts) >= 3 and parts[2] == "setup-compass" and base != "SKILL.md": return "Template"
        return "Reference"
    return "Reference"

def title_for(p):
    _, body = split(open(p, encoding="utf-8").read())
    m = re.search(r"^# (.+)$", body, re.M)
    if m: return m.group(1).strip()
    r = rel(p)
    if os.path.basename(r) == "SKILL.md": return os.path.basename(os.path.dirname(r))
    return os.path.splitext(os.path.basename(r))[0]

def is_upstream_derived(p):
    r = rel(p)
    return r.startswith(("skills/", "docs/")) or r in {".agents/writing-docs.md", ".agents/invocation.md", ".agents/adr/0001-explicit-setup-pointer-only-for-hard-dependencies.md"}

# ---- stamp ----------------------------------------------------------------
def stamp():
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    n = 0
    for p in walk():
        if os.path.basename(p) in RESERVED: continue
        text = open(p, encoding="utf-8").read()
        fm, body = split(text)
        t = type_for(p)
        if fm is not None:
            if fm_get(fm, "type"): continue
            new_fm = f"type: {t}\n" + fm
            if not fm_get(fm, "generated"):
                new_fm += f"\ngenerated: {{ by: {PRODUCER}, at: {now} }}"
            if is_upstream_derived(p) and not fm_get(fm, "sources"):
                new_fm += f"\nsources:\n  - id: upstream\n    resource: {UPSTREAM}\n    title: mattpocock/skills v1.2.3"
            open(p, "w", encoding="utf-8").write(f"---\n{new_fm}\n---\n{body}")
        else:
            title = title_for(p).replace('"', "'")
            lines = [f"type: {t}", f'title: "{title}"',
                     f"generated: {{ by: {PRODUCER}, at: {now} }}"]
            if is_upstream_derived(p):
                lines += ["sources:", "  - id: upstream", f"    resource: {UPSTREAM}", "    title: mattpocock/skills v1.2.3"]
            open(p, "w", encoding="utf-8").write("---\n" + "\n".join(lines) + "\n---\n" + body)
        n += 1
    print(f"stamped {n} file(s)")

# ---- index ----------------------------------------------------------------
INDEX_DIRS = ["", "skills", "skills/engineering", "skills/productivity", "skills/misc", "skills/in-progress", "docs", "docs/engineering", "docs/productivity", ".agents", ".agents/adr"]

def desc_of(p):
    fm, body = split(open(p, encoding="utf-8").read())
    d = fm_get(fm or "", "description")
    if d: return d.strip('"').strip("'")
    for line in body.splitlines():
        s = line.strip()
        if s and not s.startswith(("#", "|", "```", "-", "*", "<", "[")):
            return (s[:117] + "...") if len(s) > 120 else s
    return ""

def index():
    for d in INDEX_DIRS:
        absd = os.path.join(ROOT, d)
        if not os.path.isdir(absd): continue
        entries, subdirs = [], []
        for name in sorted(os.listdir(absd)):
            full = os.path.join(absd, name)
            if name in SKIP_DIRS or name.startswith(".") and d == "" and name != ".agents": continue
            if os.path.isdir(full):
                skill = os.path.join(full, "SKILL.md")
                if os.path.isfile(skill):
                    entries.append((name, f"{name}/SKILL.md", desc_of(skill)))
                elif any(f.endswith(".md") for _, _, fs in os.walk(full) for f in fs):
                    subdirs.append((name, f"{name}/"))
            elif name.endswith(".md") and name not in RESERVED:
                fm, _ = split(open(full, encoding="utf-8").read())
                t = fm_get(fm or "", "title") or os.path.splitext(name)[0]
                entries.append((t.strip('"'), name, desc_of(full)))
        out = []
        if d == "": out.append('---\nokf_version: "0.2"\n---\n')
        out.append(f"# {d or 'Compass'}\n")
        if entries:
            out.append("\n# Documents\n")
            out += [f"* [{t}]({u}) - {desc}" if desc else f"* [{t}]({u})" for t, u, desc in entries]
        if subdirs:
            out.append("\n# Subdirectories\n")
            out += [f"* [{n}]({u})" for n, u in subdirs]
        open(os.path.join(absd, "index.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")
        print(f"wrote {os.path.join(d, 'index.md') if d else 'index.md'}")

# ---- check ----------------------------------------------------------------
def check():
    errors = []
    for p in walk():
        r = rel(p); base = os.path.basename(p)
        text = open(p, encoding="utf-8").read()
        fm, body = split(text)
        if base == "index.md":
            if fm is not None:
                keys = [l.split(":")[0].strip() for l in fm.splitlines() if l.strip()]
                if r != "index.md" or keys != ["okf_version"]:
                    errors.append(f"{r}: index.md may not carry frontmatter (root may carry only okf_version)")
            continue
        if base == "log.md":
            if fm is not None: errors.append(f"{r}: log.md may not carry frontmatter")
            for l in text.splitlines():
                if l.startswith("## ") and not re.fullmatch(r"## \d{4}-\d{2}-\d{2}", l.strip()):
                    errors.append(f"{r}: log heading not ISO date: {l.strip()}")
            continue
        if fm is None:
            errors.append(f"{r}: missing frontmatter"); continue
        if not fm_get(fm, "type"):
            errors.append(f"{r}: missing or empty `type`")
        if "--strict" in FLAGS:
            errors += strict(r, fm, body)
    if errors:
        print("\n".join(errors)); print(f"\n{len(errors)} problem(s)"); sys.exit(1)
    print("OKF v0.2 conformance: OK")

ACTOR = re.compile(r"^(human:[\w.-]+|process:[\w.-]+|[\w.-]+/[\w.@-]+)$")
ADR_MAP = {"proposed": "draft", "accepted": "stable", "deprecated": "deprecated", "superseded": "deprecated"}

def strict(r, fm, body):
    errs = []
    for m in re.finditer(r"(?<![\w_])by:\s*([^,}\n]+)", fm):
        if not ACTOR.match(m.group(1).strip()):
            errs.append(f"{r}: actor not in OKF convention: {m.group(1).strip()}")
    for m in re.finditer(r"\bat:\s*([^,}\n]+)", fm):
        v = m.group(1).strip()
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(Z|[+-]\d{2}:\d{2})", v):
            errs.append(f"{r}: timestamp not ISO 8601 with offset: {v}")
    st = fm_get(fm, "status")
    if st and st not in ("draft", "stable", "deprecated"):
        errs.append(f"{r}: status must be draft|stable|deprecated, got {st}")
    adr = fm_get(fm, "adr_status")
    if adr:
        if adr not in ADR_MAP: errs.append(f"{r}: unknown adr_status {adr}")
        elif (st or "stable") != ADR_MAP[adr]: errs.append(f"{r}: adr_status {adr} requires status {ADR_MAP[adr]}")
        if adr == "superseded" and not fm_get(fm, "superseded_by"): errs.append(f"{r}: superseded ADR needs superseded_by")
    ids = set(re.findall(r"^\s*-\s*id:\s*(\S+)", fm, re.M))
    prose = re.sub(r"```.*?```", "", body, flags=re.S); prose = re.sub(r"`[^`\n]*`", "", prose)
    labels = set(re.findall(r"\[\^([^\]]+)\]", prose))
    if "sources" in fm or labels:
        for l in labels - ids: errs.append(f"{r}: footnote [^{l}] has no sources[].id")
        for i in ids - labels:
            if fm_get(fm, "type") == "Research": errs.append(f"{r}: source id {i} is never cited")
    return errs

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    {"check": check, "index": index, "stamp": stamp}.get(cmd, lambda: sys.exit(__doc__))()
