---
created: 2026-09-08T17:38:40Z
updated: 2026-09-11T14:49:25Z
---

# PRD.md — [Project Name]

**Answers:** What are we building, for whom, why?
**Depends on:** nothing — **this is the first document to fill in.** The vocabulary (`GLOSSARY.md`) gets built from what's decided here, not the other way around.

> **Status: starter structure.** Answer the reflection questions yourself before asking an agent to draft. Sections marked **Conditional** are guesses about whether they apply — confirm explicitly rather than silently accepting or skipping them.
>
> **Try it without an agent first.** This document in particular deserves to be thought through by you before opening an agent — on paper or in a draft. An agent can help formalize an answer you already have; if it supplies the answer instead, the exercise doesn't build the skill it's meant to target: your own capacity to think and plan.

*(Fill in before drafting: what is this product, in one line? What stack, if already decided? Is this for real end users, an internal tool, or a learning/demo project?)*

---

## 1. Product Statement

> 1. In one or two sentences, what does this product actually do, and who is it for?
> 2. What real problem does it solve? Does it solve more than one distinct problem for more than one distinct audience?
> 3. Why does it need to exist now, for this person, rather than being solved another way?

*(To be written)*

## 2. Audience

> 1. Who will actually use or encounter this, in every distinct capacity — not just the "main" user?
> 2. Is there a logic behind who gets access and who doesn't?
> 3. Which audience matters most if their needs conflict with another's?

*(To be written)*

## 3. Ideal End-to-End Scenario

> 1. Describe, step by step, the best possible experience a real person has, from first contact to the outcome they wanted.
> 2. What has to be true at each step for that scenario to actually happen?
> 3. Where in that journey would the experience break down today if nothing more got built?

*(To be written)*

## 4. Jobs to Be Done

> 1. What is the user trying to accomplish, independent of any feature you might build?
> 2. For each job, what does the user do today without this product?
> 3. Which job, if left unsolved, makes the whole product pointless?

*(To be written)*

## 5. Layered Product Experience *(Conditional — skip if there's only one tier of access/capability)*

> 1. Does this product have more than one tier of access or capability? How many, concretely?
> 2. What can each tier see or do that the tier below it cannot?
> 3. Is a tier boundary here about trust/security, or just feature richness?

*(To confirm: how many tiers, if any)*

## 6. What the Product Can Do

> 1. List the concrete capabilities a user can invoke, one per line, in plain verbs.
> 2. For each capability, what triggers it, and what's the actual output?
> 3. Is there a capability everyone will assume exists but isn't actually planned? State it explicitly as out of scope now.

*(To be written)*

## 7. What the Product Must Never Do

> 1. What would be actively harmful, embarrassing, or unsafe if this product did it, even once?
> 2. Are there topics, data, or actions that must always redirect to a human instead of being handled automatically?
> 3. What's the worst plausible misuse, and does this document say what happens if someone tries it?

*(To be written)*

## 8. Voice and Persona *(Conditional — skip if there's no conversational or brand-voice component)*

> 1. Does this product "speak" to anyone directly — chat, notifications, generated copy? If not, this section doesn't apply.
> 2. If it does, whose voice is it: a company's, a persona's, your own?
> 3. What tone would feel wrong for this product even if factually accurate?

*(To confirm: applicable or skip)*

## 9. Access Model

> 1. How does someone go from "no access" to "has access"? Who approves it, if anyone?
> 2. What's stored about who has access, and who can revoke it?
> 3. Is there a difference between "logged in" and "trusted enough to see everything"?

*(To be written)*

## 10. Observability

> 1. Once this is live, what's the first question you'll want answered about real usage?
> 2. What would you need to be alerted about quickly if something started going wrong?
> 3. Who looks at this data, and how often?

*(To be written)*

## 11. Success Criteria

> 1. How will you know, concretely, that this product is working as intended?
> 2. Is success measured by usage, by an outcome for the user, or by your own judgment?
> 3. What's the smallest version of "success" that would still be worth having shipped?

*(To be written)*

## 12. Failure Criteria / Go-Live Blockers

> 1. What must be true before this is allowed to go live, non-negotiably?
> 2. What would make you pull this back down after launch?
> 3. Is there a difference here between "not perfect yet" and "actually blocking"?

*(To be written)*

## 13. Out of Scope — V1

> 1. What are you deliberately not building yet, even though it's related?
> 2. What would you say to someone who asks "why doesn't it do X" for each excluded item?
> 3. Is anything here likely to be assumed as included by a first-time reader?

*(To be written)*

## 14. Related Documents

> 1. What other documents does a new reader need, and in what order?
> 2. Is there a single canonical map of every project document, or does this list risk becoming a second copy that drifts?

See `GLOSSARY.md`, `NFR.md`, `SOLUTION_DESIGN.md`, `PLAN.md`, `project-docs/execution/`, `project-docs/PROJECT_WORKFLOW.md`, `AGENTS.md`.

---

*PRD.md — [Project Name] — starter structure from `project-init-kit/`.*
