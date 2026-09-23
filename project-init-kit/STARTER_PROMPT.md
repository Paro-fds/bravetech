---
created: 2026-09-08T17:38:40Z
updated: 2026-09-16T20:11:50Z
---

# Starter prompt — copy this as-is into your agent

**Use this once you've copied the `project-init-kit/` structure into your own project.** This prompt works with any agent (Claude Code, or any other agentic coding tool) — it doesn't depend on a tool-specific mechanism.

```text
This project contains a documentation structure to fill in. Every document
is under project-docs/, and they are filled in in this order:

  project-docs/PRD.md
  project-docs/NFR.md
  project-docs/SOLUTION_DESIGN.md
  project-docs/PLAN.md
  project-docs/GLOSSARY.md          (finalize last, once we know what this is)
  project-docs/PROJECT_WORKFLOW.md  (last of all)

Each section contains reflection questions (quoted with ">"). Guide me
through these documents, in this order, one section at a time: ask me
that section's questions, wait for my answer, don't invent anything on
my behalf. Once I've answered, write the section from my answer and show
it to me before moving to the next one.

Don't touch AGENTS.md or CLAUDE.md yet, and don't create anything under
project-docs/execution/, functional-specs/, technical-specs/, reviews/ or
learnings/. Those come later: AGENTS.md and CLAUDE.md are summaries of
everything above and are written last, and the rest only fill in once
there is real work to record.
```

**Before you paste it**, read `project-docs/_ARCHITECTURE_EXPLAINED.md` once. It is the one document in the kit that answers instead of asking, and `SOLUTION_DESIGN.md` will go faster if you already know which of its recommendations you are taking.

**After the six documents are filled in**, write `AGENTS.md` and `CLAUDE.md` from them, then plan your first Epic (`epic` skill) and its first story (`user-story` skill) — and only then scaffold the code (`scaffold-backend-service`, then `scaffold-frontend-app`).

**What should happen next**: the agent should ask you one question at a time, wait for your answer, then draft — not hand you all six documents filled in at once. If the agent starts drafting everything without asking you anything, stop it and paste the prompt again: that's exactly the behavior this is meant to prevent.
