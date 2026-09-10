---
type: Skill
name: probing
description: Probe the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'probe' trigger phrases.
generated: { by: compass-port/0.1.0, at: 2026-09-10T19:44:27Z }
sources:
  - id: upstream
    resource: https://github.com/mattpocock/skills
    title: mattpocock/skills v1.2.3
---

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask the whole frontier in one round: number each question and give your recommended answer. Then wait for the user's answers before the next round.

Format a round like so:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

💬 **In plain terms**: <the same question in one or two sentences a non-technical stakeholder could answer: no jargon, no code, no acronyms; say what is being decided and why it matters>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

💬 **In plain terms**: <...>

➡️ <your recommended answer>
```

The **In plain terms** line is not optional and not a summary of the title. It restates the decision for someone who doesn't know the codebase, the platform, or the vocabulary: a product owner, an analyst, a manager. If the technical body asks "should the dedupe key be `(policy_id, effective_ts)` or a surrogate hash?", the plain line asks "when two records describe the same policy at the same moment, do we treat them as duplicates or keep both?". A technical reader skips it; a non-technical reader answers from it alone.

Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), dispatch a sub-agent to find it; don't ask the user for anything you could look up yourself. Don't block on it: a running exploration is an unsettled prerequisite, so only the questions downstream of it wait for the sub-agent to report; ask the rest of the frontier now. The _decisions_ are the user's: put each to them and wait.

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Do not act on it until the user confirms you have reached a shared understanding.
