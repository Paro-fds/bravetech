---
created: 2026-09-08T17:38:40Z
updated: 2026-09-11T14:49:25Z
---

# PLAN.md — [Project Name]

**Answers:** In what order, grouped into what Epics?
**Depends on:** `SOLUTION_DESIGN.md` for Workstream IDs.

> **Status: starter structure.** All sections are generic (sequencing/prioritization patterns, no product-specific content yet).

> **Vocabulary reminder (generic — see also `GLOSSARY.md` § Workstream, Epic, and Milestone):**
> - **Epic** = *when, how much at once*. Sequential, time-boxed build stage, grouping one or more Workstreams (defined in `SOLUTION_DESIGN.md`). Identifier `epic-NNN-name` (three-digit folder).
> - **User story** = the concrete unit of work inside an Epic. Identifier `US-NNN`, sequential across the whole project, never reset per Epic.
> - **Milestone** = what ships — the GitHub representation of an Epic, once a tracker is in use.

---

## Epic Overview

> 1. In what order will functional areas actually get worked, and why that order?
> 2. Is any Epic blocked on another finishing first?
> 3. Could two Epics genuinely run in parallel, or is sequential truly required here — and why?

*(To be written — state explicitly whether this project works Epics sequentially, one at a time, or allows parallel work)*

## Jobs to Be Done — Reference

*Pointer to `PRD.md` § Jobs to Be Done, not a second copy.*

> 1. Does every Job to Be Done map to exactly one Epic, or does one job span several?

## MoSCoW Prioritization

> 1. For each Job to Be Done, what's truly Must-have versus Should/Could/Won't for V1?
> 2. What's the cost of being wrong about something marked Must-have that turns out not to be needed?
> 3. Is anything marked Won't-have likely to get asked about anyway — worth stating explicitly rather than silently dropping?

*(To be written)*

## Per-Epic Detail

*One section per Epic, once the Epics above are identified.*

> **Questions to ask, per Epic:**
> 1. What does this Epic deliver that the previous one didn't?
> 2. What Workstream(s) does it primarily touch?
> 3. What's the one-sentence goal a stakeholder could repeat back correctly?

*(To be written)*

## Immediate Next Steps

> 1. What's the very next concrete action — not a restatement of the whole roadmap?
> 2. Is this section likely to go stale quickly — should day-to-day status live in a dedicated tracker instead (`project-docs/execution/EPIC_EXECUTION.md`)?

*(To be written)*

---

*PLAN.md — [Project Name] — starter structure from `project-init-kit/`.*
