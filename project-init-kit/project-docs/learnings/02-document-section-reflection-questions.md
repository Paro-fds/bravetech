---
created: 2026-09-08T17:38:40Z
updated: 2026-09-16T19:53:40Z
---

> **First learned:** 2026-08-13 18:04:50
> **Last updated:** 2026-08-13 18:10:19

## Context

Annex to `01-documentation-structure-template.md`: that file teaches the shape (which document answers which question, in what order, physically laid out how); this file breaks each of those documents into its actual sections and gives 3-5 brainstorming questions per section, for whoever is starting a new project to reflect on — alone or talking it through with an agent — before or while drafting that section.

The intended use: a person starting a new project reads a section's questions, thinks or talks them through with an agent, and arrives at the session with enough clarity to fill that section in well, instead of staring at an empty template or asking an agent to invent the content for them. The questions are the scaffold; the answers have to be the person's own.

`.claude/skills/*/SKILL.md` is deliberately excluded: a skill is a procedure (how a recurring task gets executed), not something to reflect your way into the content of.

Also deliberately absent: reflection questions for a testing-strategy document, because no such document exists in `08`'s table to break down — which test framework(s) to use and how testing will actually work is left to emerge once there's real code to test, not decided speculatively upfront. See `01-documentation-structure-template.md`'s matching note for where that decision would land if a project reaches the point of needing it written down.

## How this was learned

**Trigger:** After `08` had a generic physical folder tree, the next layer down was requested: for each document in `08`'s dependency table, list its actual sections, sort each into "generic — reuse as-is" vs. "specific to this project — here's the generalized version," and attach 3-5 reflection questions per section. Extra care was asked for on `PRD.md` specifically, since it tends to have the most sections that only make sense for one particular kind of product.

**The path:** Extracted the real section headers from every live document of a working project (`GLOSSARY.md`, `PRD.md`, `NFR.md`, `SOLUTION_DESIGN.md`, `PLAN.md`, `project-docs/execution/EPIC_EXECUTION.md`, `project-docs/functional-specs/`, `project-docs/technical-specs/`, a `US-NNN.md` story, `project-docs/PROJECT_WORKFLOW.md`, `CLAUDE.md`) rather than reconstructing them from memory, since a stale section list here would be worse than no list.

**Things to be aware of:**
- Two documents don't fit the "list of fixed sections" shape at all, and are treated differently below rather than forced into it: `project-docs/execution/EPIC_EXECUTION.md` is a derived tracker, not authored via reflection — it's populated automatically as `PLAN.md`'s Epics get worked. `project-docs/functional-specs/` and `project-docs/technical-specs/` have no fixed template — their own README stubs confirm this — sections are decided per Workstream based on what actually needs documenting once real behavior/implementation exists, created incrementally, never upfront.
- Some sections are genuinely conditional, not just "generalizable" — `PRD.md`'s Voice and Persona section, for instance, only applies if the product has a conversational or brand-voice component at all. Marking a section "N/A, skip" is itself a useful category, distinct from "generic, keep" and "specific, generalize."
- `NFR.md` needed almost no generalization — ISO 25010 is already a project-agnostic quality model. That asymmetry (NFR barely changes, PRD changes a lot) is itself worth noticing: the more a document describes *what this specific product is*, the less portable its exact sections are; the more it describes *a quality bar or a process*, the more portable it is.

## The Rule

Each entry below: the document, its purpose (from `08`'s table), its sections marked **Generic** (reuse the heading as-is), **Generalize** (a heading too specific to one product — a reusable version is given), or **Conditional** (only include if it applies to your product at all) — followed by reflection questions per generic/generalized section.

---

### 1. `GLOSSARY.md` — what does this term mean?

A glossary's category headers are shaped by whatever product it describes — don't copy category *names* from one product to another, copy the underlying pattern:

| Category (generalized) | Example instantiation |
|---|---|
| **Actors and roles** — who or what interacts with the system in a distinct capacity | Agents, visitor profiles, operating modes |
| **System components** — the independently-run or independently-deployable pieces | Frontends, backend services |
| **Data stores** — where information actually persists | Databases, caches, file stores |
| **Domain vocabulary** — process/content terms an outsider would misread | Content types, processes, auth/access terms |
| **Workstream, Epic, and Milestone** — Generic, reuse verbatim | same |
| **Project Documents** — Generic, pointer-only pattern | same |

**Actors and roles**
1. Who or what touches this system, and does each one need different capabilities, access, or trust level?
2. Is there a word (like "user" or "agent") that could mean two different things depending on context here? Does it need splitting into two terms?
3. Are there distinct modes or intents the same actor can be in, worth naming separately?

**System components**
1. What are the independently-run or independently-deployable pieces of this system?
2. Do any two components have similar names that could be confused? What distinguishes each in one sentence?
3. Is there a natural split worth naming as a category (public vs. private, always-on vs. on-demand)?

**Data stores**
1. Where does information actually persist, and how many distinct stores are there?
2. Does any one store hold more than one kind of data that should be named separately?
3. Which store, if lost, would be the most damaging?

**Domain vocabulary**
1. What recurring nouns or process names would an outsider misinterpret without a definition?
2. Which terms get said constantly in conversation about this project that aren't obvious from the word alone?
3. Is there a term borrowed from a wider field (e.g. "epic," "token") that means something narrower here?

**Workstream, Epic, and Milestone**
1. Does this project genuinely need all three axes — functional area / time-boxed sequential stage / shippable checkpoint — or is it small enough that two collapse into one?
2. What are this project's actual Workstreams (functional areas), independent of when each will be worked?

**Project Documents**
1. Which single document is the canonical map of every other document, so this stays a pointer and never a second copy?

---

### 2. `PRD.md` — what are we building, for whom, why?

The section most worth rethinking per-project. A conversational-agent product, a data-tracking app, and a CRUD dashboard need different subsets — generalize or flag conditional accordingly:

| Section | Treatment |
|---|---|
| 1. Product Statement | Generic |
| 2. Audience | Generic |
| 3. Ideal End-to-End Scenario | Generic |
| 4. Jobs to Be Done | Generic |
| 5. Layered Product Experience | Generic (however many access/capability tiers actually exist — could be one, could be several) |
| 6. What the Product Can Do | Generic |
| 7. What the Product Must Never Do | Generic — valuable for any product with automated or sensitive-data components |
| 8. Voice and Persona | **Conditional** — only if there's a conversational or brand-voice component at all; skip entirely otherwise |
| 9. Access Model | Generic |
| 10. Observability | Generic |
| 11. Success Criteria | Generic |
| 12. Failure Criteria / Go-Live Blockers | Generic |
| 13. Out of Scope — V1 | Generic |
| 14. Related Documents | Generic |

**Product Statement**
1. In one or two sentences, what does this product actually do, and who is it for?
2. What real problem does this solve? Is it solving more than one distinct problem for more than one distinct audience?
3. Why does this need to exist now, for this person, rather than being solved another way?

**Audience**
1. Who will actually use or encounter this, in every distinct capacity, not just the "main" user?
2. Is there a philosophy behind who gets access and who doesn't?
3. Which audience matters most if their needs conflict with another audience's?

**Ideal End-to-End Scenario**
1. Walk through, step by step, the best possible experience a real person has, from first contact to the outcome they wanted.
2. What has to be true at each step for that scenario to actually happen?
3. Where in that walkthrough would the experience break down today if nothing further got built?

**Jobs to Be Done**
1. What is the user trying to accomplish, independent of any feature you might build?
2. For each job, what does the user do today without this product?
3. Which job, if left unsolved, makes the whole product pointless?

**Layered Product Experience**
1. Does this product have more than one tier of access or capability? How many, concretely?
2. What can each tier see or do that the tier below it cannot?
3. Is a tier boundary here about trust and security, or just about feature richness?

**What the Product Can Do**
1. List the concrete capabilities a user can invoke, one per line, in plain verbs.
2. For each capability, what triggers it, and what's the actual output?
3. Is there a capability everyone will assume exists that isn't actually planned? Worth stating as explicitly out of scope now.

**What the Product Must Never Do**
1. What would be actively harmful, embarrassing, or unsafe if this product did it, even once?
2. Are there topics, data, or actions that must always redirect to a human instead of being handled automatically?
3. What's the worst plausible misuse, and does this document say what happens when someone tries it?

**Voice and Persona** *(skip if not applicable)*
1. Does this product "speak" to anyone directly — chat, notifications, generated copy? If not, this section doesn't apply.
2. If it does, whose voice is it: a company's, a persona's, the founder's own?
3. What tone would feel wrong for this product even if factually accurate?

**Access Model**
1. How does someone go from "no access" to "has access"? Who approves it, if anyone?
2. What's stored about who has access, and who can revoke it?
3. Is there a difference between "logged in" and "trusted enough to see everything"?

**Observability**
1. Once this is live, what's the first question you'll want answered about how it's actually being used?
2. What would you need to notice quickly if something started going wrong?
3. Who looks at this data, and how often?

**Success Criteria**
1. How will you know, concretely, that this product is working as intended?
2. Is success measured by usage, by an outcome for the user, or by your own judgment?
3. What's the smallest version of "success" that would still make this worth having shipped?

**Failure Criteria / Go-Live Blockers**
1. What must be true before this is allowed to go live, non-negotiably?
2. What would make you pull this back down after launch?
3. Is there a difference here between "not perfect yet" and "actually blocking"?

**Out of Scope — V1**
1. What are you deliberately not building yet, even though it's related?
2. What would you say to someone who asks "why doesn't it do X" about each excluded item?
3. Is anything excluded here likely to be assumed as included by a first-time reader?

**Related Documents**
1. What other documents does a new reader need, and in what order?
2. Is there a single canonical map of every project document, or does this list risk becoming a second copy that drifts?

---

### 3. `NFR.md` — what quality bar must it meet?

All Generic — ISO 25010 is a project-agnostic quality model. The only per-project edit is which regulatory regime actually applies in Compliance/Legal.

**Performance**
1. What response time would feel broken to a real user?
2. Is there a known peak-load moment (a launch, a specific hour)?
3. What's actually being measured — page load, API latency, something else?

**Reliability / Availability**
1. What does "down" mean for this product, precisely?
2. Is any downtime acceptable, and when?
3. What's the plan if a dependency this relies on goes down?

**Scalability**
1. What happens if usage grows 10x overnight?
2. Which resource runs out first?
3. Is scale a real near-term risk here, or a hypothetical for V1?

**Security**
1. What's the most sensitive thing this system holds?
2. Who should never be able to access it?
3. What's the worst-case breach scenario, and is it survivable?

**Usability / Accessibility**
1. Who might struggle to use this as designed — device, language, ability?
2. Is there a minimum accessibility standard being targeted?
3. What's the simplest task a first-time user must be able to complete unaided?

**Compatibility**
1. What environments (browsers, devices, OS) must this actually work on?
2. Is there an environment explicitly not supported?
3. Does it need to interoperate with any existing system?

**Compliance / Legal**
1. What regulation applies to this data or this audience?
2. What consent or disclosure is legally required before collecting data?
3. Who is liable if this goes wrong?

**Maintainability**
1. How easy is it for a future person, including future-you, to change this safely?
2. What's the plan for keeping documentation in sync with code?
3. Is there a test suite, and what does it actually cover?

**Portability**
1. Could this move to a different host or provider without a full rewrite?
2. Is anything hard-coded to one vendor that shouldn't be?

**Observability / Monitoring**
1. What would you want alerted on immediately if it broke?
2. What's logged today versus what should be?
3. Who's actually watching this?

**Disaster Recovery / Backup**
1. What's the worst data-loss scenario, and how would you recover from it?
2. How often is data backed up, and has restore ever actually been tested?
3. What's the acceptable amount of data loss (RPO) and downtime (RTO)?

**Risks and Mitigations**
1. What's most likely to go wrong before this ships?
2. For each risk, what's the plan if it happens anyway?
3. Which risk, if realized, would be hardest to recover from?

**Dependencies**
1. What external services, libraries, or people does this rely on to function?
2. What happens if one becomes unavailable or changes its API?
3. Is there a single point of failure among these?

---

### 4. `SOLUTION_DESIGN.md` — how is it built, and what Workstreams does it decompose into?

| Section | Treatment |
|---|---|
| 1. Purpose and Scope | Generic |
| 2. Workstreams | Generic — the canonical Workstream-ID definition |
| 3. System Overview | Generic |
| 4. Component Map (services/ports, diagram, tool list) | Generic pattern; the specific contents are always product-specific |
| 5. Tech Stack | Generic |
| 6. Data Layer | Generic pattern; the specific store breakdown is product-specific |
| 7. Authentication and Authorization Flow | **Conditional** — only if the product has access control at all |
| 8. Real-Time / Interactive Architecture | **Conditional** — only if there's a live or streaming layer |
| 9-10. Automated Update or Feedback Loop | **Conditional** — only if content/behavior updates automatically rather than by manual edit |
| 11. Deployment Overview | Generic |
| 12. Assumptions | Generic |
| 13. Out of Scope | Generic |
| 14. Architecture Decision Records | Generic — reuse the ADR table pattern verbatim |
| 15. Open Questions | Generic |

**Purpose and Scope**
1. What is this document responsible for deciding that no other document decides?
2. What's explicitly out of this document's authority (e.g. product decisions belong in the PRD)?

**Workstreams**
1. What are the independent functional areas of this system, regardless of build order?
2. Could two Workstreams ever be worked by different people at the same time without stepping on each other?
3. Is there a Workstream hiding inside another one that deserves its own ID?

**System Overview**
1. In a few sentences, how do the major pieces fit together end to end?
2. What's the one diagram or flow that would explain this fastest to a new engineer?

**Component Map**
1. What are the actual runnable/deployable components, and what does each one own?
2. What ports, URLs, or entry points does each expose?
3. Is there a component here that's really two components pretending to be one?

**Tech Stack**
1. What's the stack for each major part of the system, and why that choice specifically?
2. Is there a piece of the stack that's a placeholder/guess rather than a real decision yet?

**Data Layer**
1. Where does each kind of data actually live, and in what shape?
2. Which store is the source of truth if two stores could disagree?
3. What's the schema or contract, precisely enough that two implementations wouldn't drift?

**Authentication and Authorization Flow** *(skip if no access control)*
1. Step by step, how does someone go from anonymous to authenticated to authorized for a specific action?
2. What's issued (a token, a session, a key), and what does it actually prove?

**Real-time / interactive architecture** *(skip if nothing is live/streaming)*
1. What has to happen in real time versus what can be request/response?
2. What's the fallback if the real-time channel drops mid-interaction?

**Automated update or feedback loop** *(skip if content only changes by manual edit)*
1. Does anything about this system update itself based on usage or new data? What triggers it?
2. Who reviews an automated change before it goes live, if anyone?
3. What's the worst thing an automated update loop could do if left unchecked?

**Deployment Overview**
1. Where does this actually run today, and where will it run at launch?
2. What's the path from a local change to it being live?
3. Is there a CI/CD step, and what does it actually gate?

**Assumptions**
1. What is this design assuming is true that hasn't actually been verified yet?
2. Which assumption, if wrong, would force a redesign rather than a patch?

**Out of Scope**
1. What's architecturally excluded from this version, and why?
2. Is there anything excluded here that a later Workstream will need to revisit?

**Architecture Decision Records**
1. What was decided that could plausibly have gone the other way?
2. Why was the other option rejected, specifically enough that someone won't propose it again without knowing?
3. Is this decision still current, or does it need a `Deprecated` entry with a reason?

**Open Questions**
1. What's genuinely unresolved right now that shouldn't block starting, but shouldn't be forgotten either?
2. Who or what would resolve each open question, and when?

---

### 5. `PLAN.md` — in what order, grouped into what Epics?

All sections Generic (sequencing/prioritization patterns, not product-specific content).

**Epic Overview**
1. In what order will functional areas actually get worked, and why that order?
2. Is any Epic blocked on another finishing first?
3. Could two Epics genuinely run in parallel, or is sequential truly required here — and why?

**Jobs to Be Done — Reference**
1. Does every Job to Be Done map to exactly one Epic, or does one job span several?
2. Is this table still just a pointer to the PRD's real JTD definitions, or has content started duplicating there?

**MoSCoW Prioritization**
1. For each Job to Be Done, what's truly Must-have versus Should/Could/Won't for V1?
2. What's the cost of being wrong about something marked Must-have that turns out not to be needed?
3. Is anything marked Won't-have likely to get asked about anyway — worth stating explicitly rather than silently dropping?

**Per-Epic detail sections**
1. What does this Epic deliver that the previous one didn't?
2. What Workstream(s) does it primarily touch?
3. What's the one-sentence goal a stakeholder could repeat back correctly?

**Immediate Next Steps**
1. What's the very next concrete action, not a restatement of the whole roadmap?
2. Is this section likely to go stale quickly — should day-to-day status live in a dedicated tracker instead?

---

### 6. `project-docs/execution/EPIC_EXECUTION.md` — what's the status of each story, right now?

Not authored via reflection — this is a derived tracker, populated automatically as `PLAN.md`'s Epics get worked and stories close. No content to brainstorm; only a process check:

1. Is this table still true right now, or has a story's status changed without this file being updated?
2. Does every Epic in `PLAN.md` have a matching section here, in the same order?

---

### 7. `project-docs/functional-specs/` and `project-docs/technical-specs/` — what does a delivered Workstream actually do / how is it actually built?

No fixed section template exists for either — confirmed by each folder's own README stub. Sections are decided per Workstream, incrementally, once real behavior or implementation exists to document; writing them upfront would be speculation. Use these questions to decide *whether a section is needed at all*, not to fill in a fixed list:

**Functional spec (behavior)**
1. What does a user or calling system observe now that they couldn't observe before this Workstream existed?
2. What are the edge cases or refusal conditions someone building against this needs to know?
3. Is there a rule here that isn't obvious from reading the code — a business rule, a confidentiality boundary, an ordering requirement?

**Technical spec (implementation)**
1. What would a new engineer need to know to modify this safely without breaking an invariant?
2. What's the exact data contract, schema, or naming rule, precisely enough that two implementations wouldn't drift apart?
3. What decision here was non-obvious enough that someone might "fix" it back to the wrong thing later?

**Governing question for both:** has a story in this Workstream actually closed yet? If not, there's nothing real to document — wait.

---

### 8. `project-docs/execution/epic-NNN-*/US-NNN.md` — what, specifically, was asked for and accepted for one unit of work?

Already fully generic (the shared user-story format) — the only per-project tie is that "role" should be a real one from *your* Glossary, not an example project's.

**As / I want / So that**
1. Who specifically wants this — which named role from the Glossary, not just "a user"?
2. What do they want to be able to do, in one sentence?
3. Why does that outcome matter to them, not just to you as the builder?

**Context**
1. What already exists that this builds on?
2. What should explicitly *not* be assumed as already done?

**Acceptance criteria**
1. What's the smallest testable statement that's unambiguously true or false once this is done?
2. Is there an AC here that's actually a Task in disguise — an implementation step, not an observable outcome?

**Out of scope**
1. What's adjacent to this story that a reader might assume is included, but isn't?

**Tasks**
1. What's the concrete next action, in an order that could actually be followed start to finish?

**Definition of done**
1. What does the person who requested this actually check, with their own eyes, to accept it?

**As-built notes**
1. What changed between what was planned and what was actually built, and why?

---

### 9. `project-docs/PROJECT_WORKFLOW.md` — how does work actually flow, and which doc do I touch when?

| Section | Treatment |
|---|---|
| Which document to update, and when | Generic — the connective-tissue table |
| Work Tracking | Generic pattern, conditional on which tool is actually used |
| User Story Format | Generic — pointer to the shared template, see §8 above |
| Definition of Done | Generic |
| Vocabulary Reference | Generic |
| Tracker Bootstrap Steps | Generic pattern |

**Which document to update, and when**
1. For each document, what real-world event should trigger updating it?
2. Is any document being updated on a schedule instead of when its underlying fact actually changes — a sign it's the wrong owner for that fact?

**Work Tracking**
1. What tool will actually track work — a board, a spreadsheet, just issues?
2. What are the states work moves through, and who moves them?
3. Are custom fields actually needed, or does the story format's own Status line already cover it?

**Definition of Done (project-level)**
1. What's the universal bar every story must clear before Done, independent of that story's own DoD checklist?

**Vocabulary Reference**
1. Is every term used across specs traceable to a Glossary entry?

**Tracker bootstrap steps**
1. What are the one-time setup steps someone starting this fresh needs to do, in order, before the first story can be created?

---

### 10. `CLAUDE.md` — what does every session need before touching anything?

All Generic — this is what `08`'s own "CLAUDE.md is built last" section already teaches; these questions are how to actually populate it.

**What this project is**
1. In 2-3 sentences, what is this and who is it for?
2. What's the one architectural fact a fresh session absolutely must know before touching any file?

**Folder map**
1. What are the top-level folders, and what's the one-line reason each exists?
2. Is there a naming convention that needs stating explicitly so it's never guessed at?

**Tech stack**
1. What's the stack per major part of the system?
2. Where's the canonical detail already documented, so this section stays a pointer instead of a restatement?

**Conventions**
1. What's a mistake that's already happened once, that this section exists specifically to prevent?
2. What naming or formatting rule would a new contributor get wrong without being told directly? For each language/layer actually in use: what's the casing rule for files, classes/components, variables/functions, booleans, and constants — stated explicitly, not left to be inferred from the first file that happened to set a precedent? (See `AGENTS.md`'s own "Naming conventions" section in this kit for the shape this should take.)
3. Is there a service/module folder naming convention (once the project has more than one independently-run piece), and is it stated here rather than left implicit?

**Confidentiality constraints**
1. What must never be revealed, said, or invented, and what should happen instead when someone asks anyway?
2. Is there anything cleared for use that used to be restricted — is the table actually current?

**First-session checklist**
1. What's the fastest path to being useful for someone who already knows this project, versus someone starting fresh?
2. In what order should the core documents be read?

**Pointers**
1. For the handful of things that come up constantly mid-session, which single document is canonical for each?

## Common mistakes table

| Mistake | Why it happens | The fix |
|---|---|---|
| Copying a document's exact section headings into a new project instead of the underlying pattern | The heading already exists, feels safe to reuse verbatim | Ask "generic, generalize, or conditional?" for every heading before reusing it — see the PRD entry above for what that looks like done properly |
| Forcing a fixed section list onto a document type that's meant to be incremental (functional/technical specs) | Consistency feels like it should apply everywhere | Some documents are deliberately shaped by what's real yet, not by a template — writing sections before a story closes is speculation, not documentation |
| Answering these reflection questions generically instead of with the actual project's specifics | Faster to write something plausible-sounding than to think it through | The questions are the scaffold, not the content — an answer that would fit any project didn't actually answer the question |
| Treating a Conditional section as mandatory because it's in the list | The list looks complete, so skipping something in it feels like an omission | "Skip if not applicable" is itself the correct answer for a Conditional section on a project where it doesn't apply — don't force content into it |
