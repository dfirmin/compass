---
type: Skill Doc
title: "scout (docs)"
description: "Plan a huge chunk of work (more than one agent session can hold) as a shared map of decision tickets on your issue tracker, and resolve them one at a time until the way to the destination is clear."
generated: { by: compass-port/0.1.0, at: 2026-09-10T19:44:27Z }
sources:
  - id: upstream
    resource: /NOTICE.md
    title: Upstream skills repository (see NOTICE.md)
---
## What it does

`scout` takes an effort too big for one agent [session](https://www.aihero.dev/ai-coding-dictionary/session): an idea whose **destination** you can name but whose route you cannot yet see, and charts it as a shared **map** of **decision tickets** on your issue tracker, then resolves them one at a time until the way is clear.

It plans, it does not do. Every ticket holds a question whose resolution is a decision, not a slice of a build to execute, and the map is finished when nothing is left to decide before someone goes and builds the thing. That one rule is what separates a scout ticket from an ordinary implementation [ticket](https://www.aihero.dev/ai-coding-dictionary/ticket), and it is the rule agents break most often. When the map clears, scout hands off; it does not carry on into code.

## When to reach for it

You invoke this by typing `/scout`; the [agent](https://www.aihero.dev/ai-coding-dictionary/agent) won't reach for it on its own.

It is the heaviest, densest flow in the set, so the trigger is narrow: the effort has to be genuinely larger than one agent session can hold, and the route to the destination has to be foggy. The split is a clean one: `/probe-with-docs` for single-session planning, `/scout` for multi-session planning.

| What you have in front of you | What to run |
| --- | --- |
| A well-scoped feature you can settle in one sitting | [probe-me](../../skills/productivity/probe-me/SKILL.md), or [probe-with-docs](../../skills/engineering/probe-with-docs/SKILL.md) when there is a codebase |
| A greenfield project, or a build spanning many sessions, with the route still unclear | `/scout` |
| A thread where the deciding is already done | [to-spec](../../skills/engineering/to-spec/SKILL.md): skip straight past the map |
| A cleared scout map | [to-spec](../../skills/engineering/to-spec/SKILL.md), then [to-tickets](../../skills/engineering/to-tickets/SKILL.md) and [implement](../../skills/engineering/implement/SKILL.md) |
| An existing session that has already grown too big | say "hand off to `/scout`" ([handoff](../../skills/productivity/handoff/SKILL.md) bridges into a map as well as out of one) |

Greenfield is not a requirement. Scout is used routinely on legacy and half-built codebases, and it is arguably sharper there, because a lot of the fog is "what is already true here" rather than "what should we do".

## Prerequisites

The map and its tickets live on the repo's issue tracker, so scout needs the tracker wiring that [setup-compass](../../skills/engineering/setup-compass/SKILL.md) lays down. That step writes a "Scouting operations" section describing how the map, its child tickets, blocking edges, and frontier queries are expressed for GitHub, GitLab, or local markdown. Scout resolves that doc through the pointer in your `CLAUDE.md` / `AGENTS.md` rather than a fixed path; with no tracker configured at all it falls back to local markdown files.

The tracker is not decoration. Blocking is what renders the frontier visually in the tracker's own UI, and a tracker without native dependency links (a self-hosted Gitea, say) degrades scout to inferring blockers from the map text, which works but needs closer supervision.

## The map, the fog, and the frontier

The **map** is a single issue labelled `scout:map`; its tickets are its child issues. It is an **index, not a store**: a decision lives in exactly one place, its ticket, and the map only gists it and links. A session loads the map at low resolution and zooms into individual tickets on demand, which is what lets a map keep growing without every session paying for its whole history.

Four things live on it:

- **Destination**: what reaching the end of this map looks like. Naming it is the first act of charting, before any ticket exists, because the destination fixes the scope every ticket is measured against.
- **Decisions so far**: one line per closed ticket, each linking to where the detail actually lives.
- **Not yet specified**: the **fog of war**. Decisions you can tell are coming but cannot yet phrase sharply. The test for fog versus ticket is whether you can state the question precisely *now*, not whether you can answer it. Resolving a ticket clears the fog ahead of it and graduates whatever is now specifiable into fresh tickets.
- **Out of scope**: work ruled beyond the destination. Fog only ever gathers *toward* the destination, so out-of-scope work is closed and never graduates.

The **frontier** is the open, unblocked, unclaimed tickets (the edge of the known). A session claims a ticket by assigning it to itself before doing any work, so the assignee *is* the claim and concurrent sessions skip it. Tickets are referred to by name throughout, never by a bare `#42`; a wall of issue numbers is illegible in narration.

## The four decision-ticket types

Every ticket carries a `scout:<type>` label, and is either **[HITL](https://www.aihero.dev/ai-coding-dictionary/human-in-the-loop)** (worked with a human who speaks for themselves) or **[AFK](https://www.aihero.dev/ai-coding-dictionary/afk)**, driven by the agent alone. A HITL ticket only resolves through the live exchange; an agent that answers its own [probing](https://www.aihero.dev/ai-coding-dictionary/probing) questions has broken it.

| Type | Mode | Reach for it when | Resolved by |
| --- | --- | --- | --- |
| `probing` | HITL | The default. The question can be settled by talking it through. | [probing](../../skills/productivity/probing/SKILL.md) plus [domain-modeling](../../skills/engineering/domain-modeling/SKILL.md), in a fresh session |
| `prototype` | HITL | "How should this look" or "how should this behave": a question talking cannot settle. | [prototype](../../skills/engineering/prototype/SKILL.md), with the built artifact linked from the ticket as an asset |
| `research` | AFK | A fact outside the working directory is blocking a decision. | A [research](../../skills/engineering/research/SKILL.md) [subagent](https://www.aihero.dev/ai-coding-dictionary/subagent), fired at charting time and burned down in parallel on a `research/<name>` branch |
| `task` | Either | Nothing to decide, but manual work blocks a decision, such as provisioning access, signing up for a service, or moving data so its shape can be seen. | The agent alone where it can, otherwise a precise checklist for the human |

`task` is the only type that *does* rather than decides, and it earns its place by unblocking a decision, never by delivering a piece of the destination. This is the type that goes wrong most often in practice: agents interpret it as an implementation step and start writing product code inside the map.

Research is the only exception to *one ticket per session*.

## Common questions

**How is this different from `/probe-with-docs`? Which should I start with?**
Session count, not project size. `/probe-with-docs` is single-session planning; scout is multi-session planning. If you can hold the whole thing in one conversation, probing is the cheaper and better tool, and scout is genuinely slower and denser for that case. The community shorthand that has settled on it: scout only makes sense if the work doesn't fit into a single session. This is by a distance the most-asked scout question, and it keeps being asked because the descriptions do not tell you where your own task sits on that line. You have to judge the session count yourself.

**When it asks for the "destination", does it mean the end of this session or the end of everything?**
The whole map. That means the destination of the entire map, not just the initial session. The question reads ambiguously because scout is by definition a multi-session tool, so a session-scoped answer never makes sense. Typical destinations are a [spec](https://www.aihero.dev/ai-coding-dictionary/spec) to hand off, a decision to lock before planning starts, a proof of concept, or a change made in place like a data migration.

**The map is cleared. Didn't scout already write the spec and make the tickets? Why do I still need `/to-spec` and `/to-tickets`?**
No. Scout's tickets are decision tickets, and by the time the map closes they are all closed too. What is left is a map full of linked decisions, which is not a build plan. [to-spec](../../skills/engineering/to-spec/SKILL.md) collapses those linked decisions into one spec (`/to-spec #<map_issue>`) and [to-tickets](../../skills/engineering/to-tickets/SKILL.md) slices that into tracer-bullet implementation tickets. Looping the map straight into [implement](../../skills/engineering/implement/SKILL.md) skips the collapse and throws the linked detail away. Go straight to implementation only when the effort turned out genuinely small. People do run the abbreviated pipeline and report it working; the two extra steps buy you an explicit spec artifact that a reviewer or a colleague can read, which matters more the less solo you are.

**My agent started writing production code in the middle of a scout session.**
The most-reported failure with this skill, and there is a real hole behind it. Scout's "plan, don't do" default can be overridden in the map's **Notes**, but the Notes are written by the agent, so the constraint and its exemption live in the same file the constrained party owns. One user watched an agent write "this map carries execution" into its own Notes and then read it back in later sessions as its own licence, building on a live server. There is no hard in-skill stop for "I meant the default." Until there is: read the Notes on any map you didn't chart yourself, keep implementation in its own sessions, and treat any `scout:task` that looks like a slice of the build as mis-typed.

**I charted 27 tickets, and by the time I got to the thirteenth, the rest no longer made sense.**
A real and repeatedly-reported outcome, verbatim from a field report. Scout's default instinct is to plan comprehensively, and a map whose later tickets rest on assumptions the earlier ones invalidate is exactly the waterfall trap the skill is accused of. Two things push back on it. Scope the map to a bounded destination rather than to the whole product. Practitioners consistently report that maps scoped to one defined epic behave better than a sprawling "implement V1", and planning something very big is not the goal in the first place: shipping small increments is. And [prototype](https://www.aihero.dev/ai-coding-dictionary/prototyping) aggressively: the whole reason the route stays current is that uncertainty is flushed out by cheap concrete artifacts before implementation depends on it. Scout is "prototypemaxxing", not "planmaxxing".

**Can I work several tickets in parallel?**
The frontier is built to show you what is takeable, and blocking edges are there so parallel work is safe on paper. In practice one-at-a-time is the safer default. Users working two probing tickets at once get asked in one session a question they just answered in the other, because the sessions share no [context](https://www.aihero.dev/ai-coding-dictionary/context). There is also a known gap on prototype tickets: an agent has been reported building three UI variations, choosing one itself, and closing the ticket. The selection is yours to make, and the skill does not currently say so loudly enough. If you do run in parallel, review the dependency graph yourself first.

**Do I have to use GitHub Issues?**
No. Any issue tracker works. GitHub is the best-supported path because its native sub-issues and blocking relationships are what make the frontier visible without opening the map; GitLab, Linear, Jira and local markdown all get used. Two honest caveats. A tracker with no native blocking means the dependency graph is inferred from text and needs manual correction. And local markdown puts the artifacts in your repo, which is not recommended: storing this material in the repo tends to lead to accidental persistence. Open-source maintainers hit the opposite problem (public trackers filling with agent-generated planning tickets) and tend to choose local markdown anyway.

**The probing is exhausting. Every question is three paragraphs long.**
This is the sharpest live complaint about scout and it is not resolved. The decomposition one user gave: the verbosity itself causes decision exhaustion, and the length strips out *why* a question is being asked, so you lose the chain from decision to decision as the map gets longer. The verbosity looks like a property of the current set of [models](https://www.aihero.dev/ai-coding-dictionary/model) rather than of the skill, and no fix has landed. Practitioner mitigations in circulation: run a lower [reasoning effort](https://www.aihero.dev/ai-coding-dictionary/effort), and put a plain-language instruction in your global `CLAUDE.md`. Expect to spend real thought here regardless, since the amount of thinking scout demands from you is not a defect but most of what it is for.

**A decision I already closed turned out to be wrong. Do I edit the old ticket or make a new one?**
There is no official guidance, and the agent's instinct is unhelpful: it tends to design around the bad decision rather than challenge it, so you have to steer manually. What does work is telling scout plainly what changed; it updates the map, revises the affected tickets, and comments on already-closed ones. Scope changes mid-map are recoverable. A map you *designed* to change is a scoping smell.

**Where did `decision-mapping` go?**
It is this skill, renamed to `scout` in v1.1 and invoked as `/scout`. "Decision map" was jargon and was also inaccurate, since only one of the four ticket types is really a decision by itself. The reframe gave the skill one coherent vocabulary (destination, fog of war, frontier, the map) instead of an invented term layered on top. The unit kept the "decision" word, though: a **decision ticket** is what a scout ticket is called, precisely to stop people reading it as an implementation ticket.

## It's working if

- The destination is written down and agreed before a single ticket exists.
- Every open ticket reads as a question. Any ticket that reads "build the X" is either mis-typed or belongs downstream of the map.
- You can look at your tracker and see which tickets are takeable without opening the map, since that is the frontier rendering itself through native blocking.
- A session resolves one ticket, posts the answer as a resolution comment, closes it, and leaves one line on the map's *Decisions so far*. Then it stops.
- **Not yet specified** shrinks over time. A patch of fog that graduates into a ticket disappears from that section rather than living in both places.
- When the opening breadth-first probe turns up no fog at all, the skill stops and tells you the effort is small enough to skip the map.
- The session that finishes the map hands you toward a spec, not a pull request.

## Where it fits

`scout` is a **situational on-ramp**, not the default front door. The probe-led idea → ship chain is still where most work starts; scout is what you climb onto when the idea is too big to hold in one session, and it merges back onto that chain at [to-spec](../../skills/engineering/to-spec/SKILL.md), because a cleared map hands off rather than builds.

Underneath, it is mostly other skills wearing scout's scheduling: [probing](../../skills/productivity/probing/SKILL.md) and [domain-modeling](../../skills/engineering/domain-modeling/SKILL.md) resolve the default ticket type, [prototype](../../skills/engineering/prototype/SKILL.md) resolves the tickets that talking cannot, and [research](../../skills/engineering/research/SKILL.md) runs as a subagent so its reading never lands in your session. [handoff](../../skills/productivity/handoff/SKILL.md) is the bridge in and out: into a map from a conversation that outgrew itself, out of one when a side quest appears mid-session. For anything else, [ask-compass](../../skills/engineering/ask-compass/SKILL.md) routes over the whole set.
