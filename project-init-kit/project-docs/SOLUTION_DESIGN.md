---
created: 2026-09-08T17:38:40Z
updated: 2026-09-16T19:53:40Z
---

# SOLUTION_DESIGN.md — [Project Name]

**Answers:** How is this built? What Workstreams does it decompose into?
**Depends on:** `PRD.md` + `NFR.md`.

> **Status: starter structure.** Sections marked **Conditional** are guesses about applicability — confirm explicitly.

*(Fill in before drafting: is the stack already decided? Single service or multiple? Any hard constraint already fixed?)*

---

## 1. Purpose and Scope

> 1. What is this document responsible for deciding that no other document decides?
> 2. What's explicitly outside this document's authority (e.g. product decisions belong in the PRD)?

*(To be written)*

## 2. Workstreams — canonical definition of `WS-NN`

> **Vocabulary reminder (generic, product-independent — see also `GLOSSARY.md` § Workstream, Epic, and Milestone):**
> - **Workstream** = *which functional area*. Never finishes, can be revisited by a later Epic. Identifier: `WS-NN` (two digits).
> - **Epic** = *when, how much at once*. Sequential, time-boxed build stage. Identifier: `epic-NNN-name`.
> - **Milestone** = *what ships*. The GitHub-native representation of an Epic, not a separate concept.
>
> Workstreams get defined here; Epics (which group Workstreams over time) get defined next, in `PLAN.md`.

> 1. What are the independent functional areas of this system, regardless of build order?
> 2. Could two Workstreams be worked by different people at the same time without stepping on each other?
> 3. Is there a Workstream hiding inside another one that deserves its own ID?

*(To be written)*

## 3. System Overview

> 1. In a few sentences, how do the major pieces fit together end to end?
> 2. What's the one diagram or flow that would explain this fastest to a new engineer?

*(To be written)*

## 4. Component Map

> 1. What are the actual runnable/deployable components, and what does each one own?
> 2. What ports, URLs, or entry points does each expose?
> 3. Is there a component here that's really two components pretending to be one?

*(To be written)*

**Before answering this section, read `project-docs/_ARCHITECTURE_EXPLAINED.md`.** It proposes a settled internal structure for both halves of a project — a layered backend (entities / dal / bll / api, with DTOs and versioning at the edge) and a Feature-Sliced frontend — together with the naming conventions and a recommended stack, each with the reasoning and the cost stated.

**Treat it as a proposal to accept or replace deliberately, not a default to apply silently.** A single-endpoint utility service does not need four layers, and forcing it into them is its own mistake. Whatever you decide, **record the decision here** — that is what this section is for, and "we used the kit's" is a perfectly good answer as long as it is written down.

`project-docs/learnings/03-backend-layered-architecture-template.md` carries the backend pattern's longer reasoning, including the tradeoff when two services need the same table.

## 5. Tech Stack

> 1. What's the stack for each major part of the system, and why that choice specifically?
> 2. Is there a piece of the stack that's a placeholder/guess rather than a real decision yet?

*(To be written)*

## 6. Data Layer

> 1. Where does each kind of data actually live, and in what shape?
> 2. Which store is the source of truth if two stores could disagree?
> 3. What's the schema or contract, precisely enough that two implementations wouldn't drift?

*(To be written)*

## 7. Authentication and Authorization Flow *(Conditional — skip if there's no access control at all)*

> 1. Step by step, how does someone go from anonymous to authenticated to authorized for a specific action?
> 2. What's issued (a token, a session, a key), and what does it actually prove?

*(To confirm: applicable or skip)*

## 8. Real-Time / Interactive Architecture *(Conditional — skip if nothing is live/streaming)*

> 1. What has to happen in real time versus what can be request/response?
> 2. What's the fallback if the real-time channel drops mid-interaction?

*(To confirm: applicable or skip)*

## 9-10. Automated Update or Feedback Loop *(Conditional — skip if content/behavior only changes by manual edit)*

> 1. Does anything in this system update itself based on usage or new data? What triggers it?
> 2. Who reviews an automated change before it goes live, if anyone?
> 3. What's the worst thing an automated update loop could do if left unchecked?

*(To confirm: applicable or skip)*

## 11. Deployment Overview

> 1. Where does this actually run today, and where will it run at launch?
> 2. What's the path from a local change to it being live?
> 3. Is there a CI/CD step, and what does it actually gate?

*(To be written)*

## 12. Assumptions

> 1. What is this design assuming is true that hasn't actually been verified?
> 2. Which assumption, if wrong, would force a redesign rather than a patch?

*(To be written)*

## 13. Out of Scope

> 1. What's architecturally excluded from this version, and why?
> 2. Is there anything excluded here that a later Workstream will need to revisit?

*(To be written)*

## 14. Architecture Decision Records (ADR)

*Generic — reuse the table as-is. Entries are never deleted, only marked `Deprecated` with a date and reason.*

| # | Decision | Rejected alternative | Reason | Status |
|---|---|---|---|---|
| | | | | |

> **Questions to ask, for every new entry:**
> 1. What was decided that could plausibly have gone the other way?
> 2. Why was the other option rejected, specifically enough that someone won't propose it again without knowing?

## 15. Open Questions

> 1. What's genuinely unresolved right now, without blocking the start, but also not forgotten?
> 2. Who or what would resolve each open question, and when?

*(To be written as they come up)*

---

*SOLUTION_DESIGN.md — [Project Name] — starter structure from `project-init-kit/`.*
