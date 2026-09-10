---
type: Skill
name: handoff
description: Compact the current conversation into a handoff document for another agent to pick up.
argument-hint: "What will the next session be used for?"
disable-model-invocation: true
generated: { by: compass-port/0.1.0, at: 2026-09-10T19:44:27Z }
sources:
  - id: upstream
    resource: /NOTICE.md
    title: Upstream skills repository (see NOTICE.md)
---

Write a handoff document summarising the current conversation so a fresh agent can continue the work. Save to the temporary directory of the user's OS - not the current workspace. Start it with OKF frontmatter: `type: Handoff`, `title`, `description` (the one-line goal of the next session), `generated: { by: compass/handoff, at: <ISO 8601 UTC> }`, and `sources` listing the artifacts it references (specs, ADRs, issues) by path or URL.

Include a "suggested skills" section in the document, naming which skills the next agent should call the Skill tool for.

Do not duplicate content already captured in other artifacts (specs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.
