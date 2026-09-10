# skills/engineering


# Documents

* [Engineering](README.md) - Skills for daily code work.
* [ask-compass](ask-compass/SKILL.md) - Ask which skill or flow fits your situation. A router over the skills in this repo.
* [code-review](code-review/SKILL.md) - Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes: Standards (does the code follow this repo's documented coding standards?) and Spec (does the code match what the originating issue/spec asked for?). Runs both reviews in parallel sub-agents and reports them side by side. Use when the user wants to review a branch, a PR, work-in-progress changes, or asks to \"review since X\".
* [codebase-design](codebase-design/SKILL.md) - Shared vocabulary for designing deep modules. Use when the user wants to design or improve a module's interface, find deepening opportunities, decide where a seam goes, make code more testable or AI-navigable, or when another skill needs the deep-module vocabulary.
* [diagnosing-bugs](diagnosing-bugs/SKILL.md) - Diagnosis loop for hard bugs and performance regressions. Use when the user says "diagnose"/"debug this", or reports something broken/throwing/failing/slow.
* [domain-modeling](domain-modeling/SKILL.md) - Build and sharpen a project's domain model. Use when discussing codebase terminology, writing or editing a CONTEXT.md, or recording or editing an ADR.
* [implement](implement/SKILL.md) - Implement a piece of work based on a spec or set of tickets.
* [improve-codebase-architecture](improve-codebase-architecture/SKILL.md) - Scan a codebase for deepening opportunities, present them as a visual HTML report, then probe through whichever one you pick.
* [probe-with-docs](probe-with-docs/SKILL.md) - A relentless interview to sharpen a plan or design, which also creates docs (ADR's and glossary) as we go.
* [prototype](prototype/SKILL.md) - Build a throwaway prototype to answer a design question. Use when the user wants to sanity-check whether a state model or logic feels right, or explore what a UI should look like.
* [research](research/SKILL.md) - Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo. Use when the user wants a topic researched, docs or API facts gathered, or reading legwork delegated to a background agent.
* [resolving-merge-conflicts](resolving-merge-conflicts/SKILL.md) - Use when you need to resolve an in-progress git merge/rebase conflict.
* [scout](scout/SKILL.md) - Plan a huge chunk of work (more than one agent session can hold) as a shared map of decision tickets on your issue tracker, and resolve them one at a time until the way to the destination is clear.
* [setup-compass](setup-compass/SKILL.md) - Configure this repo for the engineering skills: set up its issue tracker, triage label vocabulary, and domain doc layout. Run once before first use of the other engineering skills.
* [tdd](tdd/SKILL.md) - Test-driven development. Use when the user wants to build features or fix bugs test-first, mentions "red-green-refactor", or wants integration tests.
* [to-spec](to-spec/SKILL.md) - Turn the current conversation into a spec and publish it to the project issue tracker: no interview, just synthesis of what you've already discussed.
* [to-tickets](to-tickets/SKILL.md) - Break a plan, spec, or the current conversation into a set of tracer-bullet tickets, each declaring its blocking edges, published to the configured tracker (edges as text in one file per ticket locally, or native blocking links on a real tracker).
* [triage](triage/SKILL.md) - Move issues and external PRs through a state machine of triage roles, categorise, verify, probe if needed, and write agent-ready briefs.
* [wizard](wizard/SKILL.md) - Generate an interactive bash wizard that walks a human through steps only they can perform. Use when provisioning infrastructure, setting up credentials or CI secrets, walking an unfamiliar third-party dashboard, or running a one-off migration or cutover. Don't invoke this for steps the agent can perform itself.
