---
created: 2026-09-08T17:38:40Z
updated: 2026-09-11T14:49:25Z
---

# functional-specs/

**Answers:** What does a delivered Workstream actually do, from a behavior standpoint?

**No fixed template.** Sections are decided per Workstream, once there's real behavior to document — never ahead of time. Writing a functional spec before a story in that Workstream has closed is speculation, not documentation.

**Filename convention:** `ws-func-NN-name.md`, where `NN` matches the Workstream's ID in `SOLUTION_DESIGN.md` § Workstreams exactly.

> **Questions to ask to decide whether a section is needed (not to fill in a fixed list):**
> 1. What does a user or calling system observe now that they couldn't observe before this Workstream existed?
> 2. What are the edge cases or refusal conditions someone building against this needs to know?
> 3. Is there a rule here that isn't obvious from reading the code — a business rule, a confidentiality boundary, an ordering requirement?
>
> **Governing question for all of it: has a story in this Workstream actually closed yet? If not, there's nothing real to document — wait.**
