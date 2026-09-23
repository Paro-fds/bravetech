---
name: bootstrap-project-docs
description: Interview the user section by section to fill in this project's foundational documents (PRD.md, NFR.md, SOLUTION_DESIGN.md, PLAN.md, GLOSSARY.md, project-docs/PROJECT_WORKFLOW.md), using the reflection questions already embedded in each file. Use when a document still contains "(To be written)" placeholders and questions instead of real content.
created: 2026-09-08T17:38:40Z
updated: 2026-09-16T19:53:40Z
---

# Bootstrap project docs

## What this does

Walks the user through each foundational document of this project, one section at a time, using the reflection questions already written inside each file (marked with `>` blockquotes). The goal is that the user answers the questions and the content stays theirs — not a plausible-sounding paragraph the agent invented on their behalf.

## Order to follow

Documents depend on each other — don't jump ahead. Note that `GLOSSARY.md` is deliberately **not first**: without knowing what the product is yet, there's no way to know which terms deserve an entry.

1. `PRD.md` — what, for whom, why. **The first document**, depends on nothing.
2. `NFR.md` — the quality bar (can happen in parallel with PRD, not before it)
3. `SOLUTION_DESIGN.md` — how it's built, needs PRD + NFR to exist first
4. `PLAN.md` — sequencing, needs Workstream IDs from SOLUTION_DESIGN.md
5. `GLOSSARY.md` — can start as soon as a first PRD draft exists (early terms emerge), but only **finalize** it once `PLAN.md` is done — that's when there's enough material to know what vocabulary actually matters. Its "Workstream, Epic, Milestone" section is generic and already filled in from day one; the rest is product-specific and comes last.
6. `project-docs/PROJECT_WORKFLOW.md` — the connective tissue, needs everything above

`AGENTS.md` / `CLAUDE.md` are **not** part of this walk — they're built last, once the documents above are real, as a derived summary. Don't attempt to draft them during this interview.

`project-docs/execution/EPIC_EXECUTION.md`, `project-docs/functional-specs/`, `project-docs/technical-specs/`, and `project-docs/execution/*` are **not** authored via reflection either — they get filled in later, incrementally, once real work exists. Don't try to pre-fill them now.

When `SOLUTION_DESIGN.md` §4/§5/§6 (Component Map / Tech Stack / Data Layer) comes up, point at **`project-docs/_ARCHITECTURE_EXPLAINED.md`** — it carries a settled layered backend structure, a frontend architecture, the naming conventions and a recommended stack, each with its reasoning and its cost. It is a starting point to accept or reject deliberately, **not a default to apply silently**, and a single-endpoint utility service should not be forced into it. `project-docs/learnings/03-backend-layered-architecture-template.md` has the longer reasoning behind the backend half.

## Rules

1. **One section at a time.** Don't paste every question from every document in one message — the user can't answer that. Pick the next unanswered section, ask its questions, stop, wait.
2. **Never invent an answer on the user's behalf**, even a plausible one. If they seem stuck, offer to talk it through by asking a narrower follow-up question — not by proposing finished prose for them to approve.
3. **Draft only after they've answered.** Once the user has actually answered a section's questions, write the section's content from their answers, show it to them, and ask if it's accurate before moving to the next section.
4. **Conditional sections**: several sections in `PRD.md` and `SOLUTION_DESIGN.md` are marked *Conditional* with a pre-filled guess. Confirm that guess explicitly with the user rather than silently accepting or silently overriding it. "Skip, not applicable" is a valid, complete answer for a Conditional section — don't push for content that doesn't apply.
5. **Don't force genuinely incremental documents into this process.** `project-docs/functional-specs/` and `project-docs/technical-specs/` have no fixed template on purpose — see their own `README.md`. If asked to bootstrap those now, point out that nothing has shipped yet, so there's nothing real to document.
6. **Stop and ask before creating any file not already scaffolded** in this repository — don't invent new documents outside this kit's structure without checking first.
7. **If the user gives an answer that contradicts something already written** in an earlier document (e.g. a PRD decision that changes what GLOSSARY.md said), flag the conflict explicitly rather than silently editing the earlier file.

## Where the structure itself is explained

If the user asks *why* the structure is shaped this way (dependency order, naming conventions, the `.claude/` layer, `CLAUDE.md` vs `AGENTS.md`), don't re-derive it — point to `project-docs/learnings/01-documentation-structure-template.md` (the full methodology) and its annex `project-docs/learnings/02-document-section-reflection-questions.md` (the section-by-section reflection questions, self-contained).

For **code** structure — backend layers, frontend architecture, naming conventions, the recommended stack — point to `project-docs/_ARCHITECTURE_EXPLAINED.md`, and to `project-docs/learnings/03-backend-layered-architecture-template.md` for the backend's longer reasoning.
