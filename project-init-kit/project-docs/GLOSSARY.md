---
created: 2026-09-08T17:38:40Z
updated: 2026-09-11T14:49:25Z
---

# GLOSSARY.md — [Project Name]

**Answers:** What does this term mean? — consult whenever a word is ambiguous, once filled in.
**Depends on:** nothing for the "Workstream, Epic, and Milestone" section (generic, already here); on `PRD.md`, and especially `PLAN.md`, for everything else.

> **Status: starter structure — the last document to finalize, not the first.** Counter-intuitively, this isn't where you start: without knowing yet what product this is, you don't know which vocabulary deserves an entry. Real order: `PRD.md` → `NFR.md` → `SOLUTION_DESIGN.md` → `PLAN.md` → **here, last**. This file can start filling in as soon as a first PRD draft exists (the first terms emerge), but it only **finalizes** once `PLAN.md` is done — that's when there's enough material to actually know what product this is. Each section carries the reflection questions to ask yourself before writing — don't ask the agent to invent the answers.

---

## Actors and Roles

*Who or what interacts with this system, in a distinct capacity.*

> **Questions to ask:**
> 1. Who or what touches this system, and does each one need different capabilities, access, or trust level?
> 2. Is there a word (like "user" or "agent") that could mean two different things depending on context here? Does it need splitting into two terms?
> 3. Are there distinct modes or intents the same actor can be in, worth naming separately?

*(To be written)*

---

## System Components

*The pieces that run or deploy independently.*

> **Questions to ask:**
> 1. What are the independently-run or independently-deployable pieces of this system?
> 2. Do any two components have similar names that could be confused? What distinguishes each in one sentence?
> 3. Is there a natural split worth naming as a category (public vs. private, always-on vs. on-demand)?

*(To be written — probably short here if this is a single backend/single frontend project)*

---

## Data Stores

*Where information actually persists.*

> **Questions to ask:**
> 1. Where does information actually persist, and how many distinct stores are there?
> 2. Does any one store hold more than one kind of data that should be named separately?
> 3. Which store, if lost, would be the most damaging?

*(To be written)*

---

## Domain Vocabulary

*Process or content terms an outsider might misread.*

> **Questions to ask:**
> 1. What recurring nouns or process names would an outsider misinterpret without a definition?
> 2. Which terms get said constantly in conversation about this project that aren't obvious from the word alone?
> 3. Is there a term borrowed from a wider field that means something narrower here?

*(To be written)*

---

## Workstream, Epic, and Milestone

*Generic — reuse as-is.*

- **Workstream** = *which functional area*. Never finishes. Can be revisited by a later Epic. Identifier: `WS-NN` (two digits).
- **Epic** = *when, how much at once*. Sequential, time-boxed build stage. Identifier: `epic-NNN-name` (three-digit folder).
- **Milestone** = *what ships*. The GitHub representation of an Epic — not a fourth, separate concept.

> **Question to ask:** does this project genuinely need all three axes, or is it small enough that two collapse into one? What are this project's actual Workstreams, independent of the order they'll be built in?

---

## Project Documents

*Generic — pointer only.*

The canonical document listing every other project document: see `PRD.md` § Related Documents.

---

*GLOSSARY.md — [Project Name] — starter structure from `project-init-kit/`.*
