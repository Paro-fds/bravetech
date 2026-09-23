---
created: 2026-09-08T17:38:40Z
updated: 2026-09-11T14:49:25Z
---

# technical-specs/

**Answers:** How is a delivered Workstream actually built, from an implementation standpoint?

**No fixed template**, same logic as `functional-specs/` — sections decided per Workstream, incrementally, once there's a real implementation to document.

**Filename convention:** `ws-tech-NN-name.md`, same pairing as the functional side, matching the Workstream's ID.

> **Questions to ask to decide whether a section is needed:**
> 1. What would a new engineer need to know to modify this safely without breaking an invariant?
> 2. What's the exact data contract, schema, or naming rule, precise enough that two implementations wouldn't drift?
> 3. What decision here was non-obvious enough that someone might "fix" it back to the wrong thing later?
>
> **Governing question for all of it: has a story in this Workstream actually closed yet? If not, wait.**
