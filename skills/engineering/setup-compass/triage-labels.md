---
type: Template
title: "Triage Labels"
generated: { by: compass-port/0.1.0, at: 2026-09-10T19:44:27Z }
sources:
  - id: upstream
    resource: /NOTICE.md
    title: Upstream skills repository (see NOTICE.md)
---
<!-- Target-repo frontmatter: keep the block below (fill `at`) when writing this file into docs/agents/ -->
```yaml
---
type: Agent Config
title: "Triage Labels"
generated: { by: compass/setup-compass, at: <ISO 8601 UTC> }
---
```

# Triage Labels

The skills speak in terms of five canonical triage roles. This file maps those roles to the actual label strings used in this repo's issue tracker.

| Label in Compass | Label in our tracker | Meaning                                  |
| -------------------------- | -------------------- | ---------------------------------------- |
| `needs-triage`             | `needs-triage`       | Maintainer needs to evaluate this issue  |
| `needs-info`               | `needs-info`         | Waiting on reporter for more information |
| `ready-for-agent`          | `ready-for-agent`    | Fully specified, ready for an AFK agent  |
| `ready-for-human`          | `ready-for-human`    | Requires human implementation            |
| `wontfix`                  | `wontfix`            | Will not be actioned                     |

When a skill mentions a role (e.g. "apply the AFK-ready triage label"), use the corresponding label string from this table.

Edit the right-hand column to match whatever vocabulary you actually use.
