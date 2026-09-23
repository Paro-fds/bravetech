---
created: 2026-09-08T17:38:40Z
updated: 2026-09-11T14:49:25Z
---

# _TEMPLATE_US.md — user story template

> **Vocabulary reminder**: a **User story** is the concrete unit of work inside an **Epic** (sequential build stage, see `PLAN.md`), touching one or more **Workstream** (functional area, see `SOLUTION_DESIGN.md`). See also `GLOSSARY.md` § Workstream, Epic, and Milestone.
>
> Copy this file to `epic-NNN-<name>/US-NNN.md` once the first Epic is named in `PLAN.md`. `US-NNN` numbering is sequential across **the whole project**, never reset per Epic, never reused.

```markdown
# US-NNN: [Short title]

**Status:** 🔲 Backlog / ✅ Done / etc.
**Milestone:** [Epic name]
**Depends on:** US-XXX (optional — only if there's a real dependency)

---

## As [role from GLOSSARY.md]
I want [feature or capability]
So that [outcome]

## Context
[What already exists. What state the codebase is in. Which files/components/
prior stories this builds on. What NOT to assume is already done.]

## Acceptance criteria
- [ ] [Specific and binary]
- [ ] [...]

## Out of scope
- [What NOT to build in this story]

## Tasks
- [ ] [Concrete implementation step]
- [ ] [...]

## Definition of done
- [ ] [Specific thing checked by eye or by testing]

## As-built notes
[Added once work starts or completes — what actually happened, deviations
from plan, decisions made along the way.]
```

> **Questions to ask before writing each section:**
>
> **As / I want / So that**
> 1. Who precisely wants this — which named role from the Glossary, not just "a user"?
> 2. What do they want to be able to do, in one sentence?
> 3. Why does that outcome matter to them, not just to you as the builder?
>
> **Context**
> 1. What already exists that this builds on?
> 2. What should explicitly NOT be assumed as already done?
>
> **Acceptance criteria**
> 1. What's the smallest testable statement that's unambiguously true or false once this is done?
> 2. Is there a criterion here that's actually a Task in disguise — an implementation step, not an observable outcome?
>
> **Out of scope**
> 1. What's adjacent to this story that a reader might assume is included, but isn't?
>
> **Tasks**
> 1. What's the next concrete action, in an order that could actually be followed start to finish?
>
> **Definition of done**
> 1. What does the person who requested this actually check, with their own eyes, to accept it?
>
> **As-built notes**
> 1. What changed between what was planned and what was actually built, and why?
