---
created: 2026-09-08T17:38:40Z
updated: 2026-09-11T17:10:20Z
---

# PROJECT_WORKFLOW.md — [Project Name]

**Answers:** How does work actually flow, and which document do I touch when?
**Depends on:** everything before it — this is the connective tissue.

> **Status: starter structure.**

---

## Which document to update, and when

*Generic — reuse this table as-is, only adjusting document names if they change.*

| Document | Grain | Updated when |
|---|---|---|
| `project-docs/execution/EPIC_EXECUTION.md` | Per story | Continuously — every time a story's status changes |
| `project-docs/functional-specs/`, `project-docs/technical-specs/` | Per Workstream | Incrementally, as a story ships |
| `project-docs/reviews/` | **Per finding** | **The moment a belief turns out to be false** — not at the end of the work. See that folder's README; this is the row most often ignored, and the only one whose cost rises the longer you wait |
| `project-docs/PLAN.md` | Per Epic | Only when a whole Epic starts or finishes |
| `project-docs/PRD.md` | Per decision | Only when a real product/scope decision changes |
| `project-docs/SOLUTION_DESIGN.md` (§ ADR) | Per architecture decision | When a real architecture choice is made or changes |
| `project-docs/NFR.md` | Per requirement | When a quality requirement, risk, or dependency appears/changes |
| `project-docs/GLOSSARY.md` | Per term | Before a new or ambiguous term gets used elsewhere |
| `project-docs/learnings/` | Per reusable practice | When a review turns out to be true beyond this codebase. Written afterwards, deliberately — unlike a review |
| `project-docs/PROJECT_WORKFLOW.md` | Per convention | When a process convention changes |
| `CLAUDE.md` / `AGENTS.md` | Session-critical facts | When a fact every session needs to know changes |
| `project-docs/execution/epic-NNN-*/epic-NNN-refinement.md` | Per Epic | Written at Refine before any story exists, updated while the Epic is open. **The one place an in-flight rule may live** — emptied into the documents above when the Epic closes |
| `project-docs/exploration/` | Never updated | Written once, kept as it arrived, never tidied and never cited as a decision |

> **Questions to ask:**
> 1. For each document, what real-world event should trigger its update?
> 2. Is a document being updated on a schedule instead of when its underlying fact actually changes — a sign it might not be the right owner of that fact?
> 3. Which row here has never once fired? An untouched `reviews/` after real work does not mean nothing was learned; it means the findings went into a conversation that no longer exists.
> 4. Take the last rule you applied. Which row above owns it, and is it actually written there — or is it only in a review, a commit message, or an agent's head? A rule the team cannot look up is a rule only one of you is following.

---

## Work Tracking (Tracker)

*To generalize based on the tool actually used — GitHub Issues/Projects, or something simpler.*

> **Questions to ask:**
> 1. What tool will actually track work — a board, a spreadsheet, just issues?
> 2. What states does work move through, and who moves it?
> 3. Are custom fields actually needed, or does the story format's own Status line already cover it?

*(To be written)*

---

## User Story Format

See `project-docs/templates/user-story.md` — copy of the same format, don't duplicate it here.

---

## Definition of Done (Project Level)

> 1. What's the universal bar every story must clear before Done, independent of that story's own Definition of Done?

*(To be written)*

---

## Vocabulary Reference

Every term used in specs, this document, and in conversation must resolve in `GLOSSARY.md`.

> **Question:** is every term used in the specs traceable to a Glossary entry?

---

## Tracker Bootstrap Steps

*To generalize once the tool above is chosen.*

> **Question:** what are the one-time setup steps, in order, someone starting this fresh needs before the first story can be created?

**One step is fixed whatever the tracker turns out to be:**

```bash
git config core.hooksPath .githooks
```

One command, once per clone. It enables `.githooks/pre-commit`, which stamps `updated:` on every staged markdown file in UTC. Skip it and the dates silently stop moving, which is worse than not having them — a date that is present and wrong is read as true.

*(The rest to be written once the tracker is chosen)*

---

*PROJECT_WORKFLOW.md — [Project Name] — starter structure from `project-init-kit/`.*
