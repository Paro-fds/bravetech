---
created: 2026-09-10T19:30:13Z
updated: 2026-09-11T17:10:20Z
---

# `learnings/` — practice that transfers to your next project

A learning is **transferable practice**: something worth doing on any project, learned by doing it on this one. It is written for someone who will never read this codebase — including you, eighteen months from now, starting something else.

## Which folder does this go in?

Three destinations, one question each. Ask them in order and stop at the first yes.

| Question | Destination |
|---|---|
| Is it content the product itself teaches or ships? | wherever your product content lives — not here |
| Is it a correction to what you believed about *this* code? | **`../reviews/`** — dated, tied to a file, written at the moment of the finding |
| Is it practice that would help on a project unrelated to this one? | **here** |

**Ask the second question honestly, because most findings belong there.** A learning that cannot survive having every project-specific name stripped out of it is a review that was filed in the wrong folder. The test: *remove every name specific to this project. Is anything left worth reading?*

**A review is where a learning comes from.** Later, a pass over `../reviews/` asks *is any of this true beyond this codebase?* — and when the answer is yes, it becomes a file here while **the review stays exactly where it is.** Extracting is not moving.

## Naming

`NN-<descriptive-kebab-case>.md`: `04-trusting-a-new-tool.md`, not `trusting_a_new_tool.md`. The number records **the order the learning entered this folder**, assigned once and never reassigned — not a reading order and not a priority, since these are looked up by subject. Same convention as `reviews/`, for the same reason. Files imported from another project get renumbered into your sequence rather than keeping that project's, which says nothing true here.

## Structure

Whatever shape serves it, but these four sections earn their place, and one is non-negotiable:

- **`## Context`** — what this is, and why it is worth keeping rather than re-deriving.
- **`## How this was learned`** — the trigger, then **the path**, then the gotchas. **The path must show the wrong turns as wrong turns.** "Tried Y, it broke because Z, corrected to X" — not smoothed into "we decided X". This is the whole value; a file that only records the clean final answer is not a learning, it is documentation.
- **`## The Rule`** — the reusable guidance, generalised past the one incident that produced it.
- **`## Common mistakes`** — a table of *real* corrections that happened. Never hypothetical ones.

If a piece of work genuinely had no wrong turns, write that in one line rather than manufacturing drama the work did not have.

---

*Maintainer note, for whoever exports this kit:* the example learning files ship from the source project's own `learnings/` folder and are copied in at export time, so that there is one live copy rather than two that drift. The rules above are the part a student needs; the examples are illustration.
