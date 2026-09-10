---
type: Reference
title: "Compass README"
description: "Agent skills for ETL, AWS, and app work; install and orientation."
generated: { by: compass-port/0.1.0, at: 2026-09-10T19:44:27Z }
---
# Compass

Agent skills for real engineering work on our data platform and the apps around it. Compass is adapted from [mattpocock/skills](https://github.com/mattpocock/skills) (MIT, see `LICENSE`): same small, composable, model-agnostic skills, extended toward ETL generation across warehouses (Teradata, Databricks, Snowflake, Oracle), AWS infrastructure, and the front-end/TypeScript codebases we still own.

Two things Compass adds on top of the upstream shape:

- **Plain-language questions.** Every decision question a skill asks you comes with an **In plain terms** restatement a non-technical stakeholder can answer. Product owners and analysts can sit in a probing session without a translator.
- **Repo config over per-platform skills.** There is no `etl-databricks` or `web-typescript` skill. Skills generalize; what's specific to a repo (platform, dialect, deployment target, which company standards apply) lives in `docs/agents/*.md`, written once by `/setup-compass`.

Planned next: architectural diagrams as a required artifact alongside `CONTEXT.md` and ADRs, and pulling our internal API, Engineering Security, and AWS standards skills into the flows. See [.agents/roadmap.md](./.agents/roadmap.md).

## Installation

No plugin marketplace, no `npx`: neither works in our environment. Clone and run the installer.

```bash
git clone https://github.com/dfirmin/compass.git ~/compass
cd /path/to/your-repo
~/compass/scripts/install.sh
```

That installs **per project**: the skills are copied into `./.agents/skills/` (which Codex and Cursor read) and `./.claude/skills/` is symlinked to it (which Claude Code reads), so there is one copy on disk and it travels with the repo. Commit `.agents/skills/` so teammates and CI get the same set; re-run the script after `git pull` in `~/compass` to refresh. Use `--user` for a machine-wide install into `~/.claude/skills/` and `~/.agents/skills/` instead (symlinks, so they track the checkout).

Then restart your agent session and run **`/setup-compass`** once per repo. It will:

- Ask which issue tracker this repo uses (GitHub, GitLab, or local markdown; anything else described in a paragraph)
- Ask whether to keep the default triage labels (`/triage` uses labels)
- Detect single- vs multi-context domain docs
- Write the plain-language question rule into the repo's `AGENTS.md` / `CLAUDE.md`

Not sure which skill fits? Run **`/ask-compass`**.

## The main flow

1. **`/probe-with-docs`**: sharpen the idea by interview. It's stateful: what it learns lands in `CONTEXT.md` and ADRs. Outside a repo, `/probe-me` runs the same interview statelessly.
2. Need a runnable answer to a design question? Detour through **`/prototype`**, bridged by **`/handoff`**.
3. Multi-session build? **`/to-spec`** then **`/to-tickets`**, then **`/implement`** per ticket. Small enough for one session? **`/implement`** right here.

`/implement` drives **`/tdd`** internally and closes out with **`/code-review`**. Bugs and requests piling up go through **`/triage`**; something broken goes through **`/diagnosing-bugs`**; an effort too big and foggy for one session gets charted with **`/scout`**. Full routing, including when to `/clear`, `/compact`, or `/handoff`, is in [`ask-compass`](./skills/engineering/ask-compass/SKILL.md).

## Reference

These split on one axis: who can invoke them. **User-invoked** skills are reachable only when you type them (e.g. `/probe-me`); their job is to orchestrate. **Model-invoked** skills can be invoked by you _or_ reached for automatically by the agent when the task fits; they hold the reusable discipline. A user-invoked skill may invoke model-invoked skills, but never another user-invoked one.

### Engineering

Skills for daily code work.

**User-invoked**

- **[ask-compass](./skills/engineering/ask-compass/SKILL.md)**: Ask which skill or flow fits your situation. A router over the user-invoked skills in this repo.
- **[probe-with-docs](./skills/engineering/probe-with-docs/SKILL.md)**: Probing session that also builds your project's domain model, sharpening terminology and updating `CONTEXT.md` and ADRs inline.
- **[triage](./skills/engineering/triage/SKILL.md)**: Move issues through a state machine of triage roles.
- **[improve-codebase-architecture](./skills/engineering/improve-codebase-architecture/SKILL.md)**: Scan a codebase for deepening opportunities, present them as a visual HTML report, then probe through whichever one you pick.
- **[setup-compass](./skills/engineering/setup-compass/SKILL.md)**: Configure this repo for the engineering skills (issue tracker, triage labels, domain doc layout). Run once per repo before using the other engineering skills.
- **[to-spec](./skills/engineering/to-spec/SKILL.md)**: Turn the current conversation into a spec and publish it to the issue tracker. No interview, just synthesizes what you've already discussed.
- **[to-tickets](./skills/engineering/to-tickets/SKILL.md)**: Break any plan, spec, or conversation into a set of tracer-bullet tickets, each declaring its blocking edges, written as text in a local file, or as native blocking links on a real tracker.
- **[implement](./skills/engineering/implement/SKILL.md)**: Build the work described by a spec or set of tickets, driving `/tdd` at pre-agreed seams and closing out with `/code-review` before committing.
- **[scout](./skills/engineering/scout/SKILL.md)**: Plan a huge chunk of work, more than one agent session can hold, as a shared map of decision tickets on the issue tracker, and resolve them one at a time until the way to the destination is clear.

**Model-invoked**

- **[prototype](./skills/engineering/prototype/SKILL.md)**: Build a throwaway prototype to answer a design question, either a single shareable HTML file for state/logic questions, or several radically different UI variations toggleable from one route.
- **[diagnosing-bugs](./skills/engineering/diagnosing-bugs/SKILL.md)**: Disciplined diagnosis loop for hard bugs and performance regressions: build a feedback loop that goes red on this bug → minimise → hypothesise → instrument → fix → regression-test.
- **[research](./skills/engineering/research/SKILL.md)**: Investigate a question against high-trust primary sources and capture the findings as a cited Markdown file in the repo, run as a background agent.
- **[tdd](./skills/engineering/tdd/SKILL.md)**: Test-driven development with a red-green-refactor loop. Builds features or fixes bugs one vertical slice at a time.
- **[domain-modeling](./skills/engineering/domain-modeling/SKILL.md)**: Actively build and sharpen a project's domain model: challenge terms against the glossary, stress-test with edge-case scenarios, and update `CONTEXT.md` and ADRs inline.
- **[codebase-design](./skills/engineering/codebase-design/SKILL.md)**: Shared discipline and vocabulary for designing deep modules: a lot of behaviour behind a small interface, placed at a clean seam, testable through that interface.
- **[code-review](./skills/engineering/code-review/SKILL.md)**: Two-axis review of the diff since a fixed point: **Standards** (does it follow the repo's coding standards, plus a Fowler smell baseline?) and **Spec** (does it faithfully implement the originating issue/spec?), run as parallel sub-agents so neither pollutes the other.
- **[resolving-merge-conflicts](./skills/engineering/resolving-merge-conflicts/SKILL.md)**: Work through an in-progress git merge or rebase conflict hunk by hunk, resolving by intent traced to each side's primary source, then finish the operation (never `--abort`).
- **[wizard](./skills/engineering/wizard/SKILL.md)**: Generate an interactive bash wizard that walks a human through steps only they can perform: provisioning infrastructure, setting up credentials or CI secrets, walking an unfamiliar third-party dashboard, or running a one-off migration or cutover.

### Productivity

General workflow tools, not code-specific.

**User-invoked**

- **[probe-me](./skills/productivity/probe-me/SKILL.md)**: Get relentlessly interviewed about a plan or design until every branch of the design tree is resolved.
- **[handoff](./skills/productivity/handoff/SKILL.md)**: Compact the current conversation into a handoff document so another agent can continue the work.
- **[teach](./skills/productivity/teach/SKILL.md)**: Teach the user a new skill or concept over multiple sessions, using the current directory as a stateful teaching workspace.
- **[to-questionnaire](./skills/productivity/to-questionnaire/SKILL.md)**: Turn a decision you can't answer alone into a Markdown questionnaire for the one person who can, filled in async, or together over a meeting. It probes you about the send (who it's for, what you need back), not the subject.
- **[wait-what](./skills/productivity/wait-what/SKILL.md)**: Fire this the moment a message doesn't land. The agent re-pitches it with the context you're missing, in plain English, using your `CONTEXT.md` vocabulary.

**Model-invoked**

- **[probing](./skills/productivity/probing/SKILL.md)**: Interview the user relentlessly about a plan, decision, or idea until every branch of the design tree is resolved. The reusable interview primitive behind `probe-me`, `probe-with-docs`, `triage`, `scout` and `improve-codebase-architecture`.
- **[writing-for-agents](./skills/productivity/writing-for-agents/SKILL.md)**: Writing documents for agents: skills, AGENTS.md/CLAUDE.md, and any doc an agent reaches by a pointer.
