---
type: Glossary
title: "Compass glossary"
description: "Shared vocabulary for the skills and their renamed terms."
generated: { by: compass-port/0.1.0, at: 2026-09-10T19:44:27Z }
---
# Compass

Our collection of agent skills (slash commands and behaviors) loaded by Claude Code, Codex, and Cursor. Skills are organized into buckets and consumed by per-repo configuration emitted by `/setup-compass`. Adapted from mattpocock/skills; the renamed terms below map back to that repo where noted.

## Language

**Probing**:
The relentless, round-by-round interview that drives a design tree to an empty frontier. The primitive is the `probing` skill; `probe-me` and `probe-with-docs` are its two named entry points. (Upstream: "grilling".)
_Avoid_: grilling, interviewing (as a term of art), Q&A

**In plain terms**:
The mandatory plain-language restatement attached to every decision question the agent asks, so a non-technical stakeholder can answer without the technical body. Carried by the `probing` template and by `docs/agents/plain-language.md` in each configured repo.

**Scout**:
The skill that charts a huge, foggy effort as a shared map of decision tickets on the issue tracker and works them one per session. Its labels are `scout:map` and `scout:<type>`. (Upstream: "wayfinder".)
_Avoid_: wayfinder, wayfinding

**Issue tracker**:
The tool that hosts a repo's issues: GitHub Issues, GitLab Issues, a local `.scratch/` markdown convention, or similar. Skills like `to-tickets`, `to-spec`, and `triage` read from and write to it.
_Avoid_: backlog manager, backlog backend, issue host

**Issue**:
A single tracked unit of work inside an **Issue tracker**: a bug, task, spec, or slice produced by `to-tickets`.
_Avoid_: ticket (use only when quoting external systems that call them tickets, or for a **Decision ticket**, see below)

**Decision ticket**:
A `scout` unit: a child **Issue** of a `scout:map` holding a *question* whose resolution is a decision, not a slice of a build to execute.

**Triage role**:
A canonical state-machine label applied to an **Issue** during triage (e.g. `needs-triage`, `ready-for-agent`). Each role maps to a real label string in the **Issue tracker** via `docs/agents/triage-labels.md`.

**Repo config**:
The `docs/agents/*.md` files `setup-compass` writes into a target repo (issue tracker, triage labels, domain docs, plain-language rule). Where repo-specific facts live, so the skills themselves stay platform-agnostic.

## Relationships

- An **Issue tracker** holds many **Issues**
- An **Issue** carries one **Triage role** at a time
- A **Decision ticket** is an **Issue** (a child of a `scout:map`)
- **Probing** is run directly by `probe-me`, `probe-with-docs`, and internally by `triage`, `scout`, and `improve-codebase-architecture`
- Every **Probing** question carries an **In plain terms** line

## Flagged ambiguities

- "backlog" previously meant both the *tool* and the *body of work*. Resolved: the tool is the **Issue tracker**; "backlog" is not a domain term.
- "grill"/"wayfinder" survive only in upstream links and this glossary's back-references; never in skill prose.
