---
created: 2026-09-10T19:30:13Z
updated: 2026-09-11T17:10:20Z
---

# `reviews/` — what you believed that turned out to be false

**This folder is empty and it is the most valuable one here.** Nothing goes in it on day one, and if it is still empty after your first Epic, something has gone wrong — not with the project, with the record-keeping.

A review is not a design doc and not a changelog. Its mode is exactly one thing:

> here is what I believed, here is the evidence it was false, here is the corrected claim.

## The rules that make it work

**One file per piece of work**, numbered and named for the subject: `01-architecture-review.md`, `02-frontend-test-review.md`. **The number is the order the review was written, not a priority and not a category** — this folder is a history, so chronological is the order to read it in, and `ls` alone would sort it by subject, which tells you nothing about how understanding changed. Assign the number once and never reassign it: a later review takes the next one, because a citation in an old commit message has to keep pointing at the same document. No date in the filename — the entries inside carry those, and so does the `updated:` frontmatter.

**Written at the moment of the finding, not at the end of the work.** This is the whole rule, and the reason is arithmetic: a correction costs almost nothing to write while it is fresh and is close to impossible to reconstruct a week later. A review written at the end of an Epic is a summary of what shipped, which is what the closeout doc is for.

**Number the findings** — `F1`, `F2`, or a table with a *status* column. A finding resolved later gets its resolution appended, never an edit that makes the original look as though it had been right all along.

**Keep the corrections, especially the embarrassing ones.** A review whose findings all turned out to be *"slightly more subtle than expected"* is a review nobody wrote honestly. The source project this kit came from has one recording that its own `README.md` claimed two modules were unit-tested when neither was — found by hitting a bug in one of them — and that paragraph is worth more than any of the clean architecture prose beside it.

## What does not live here: the rules

**A finding that becomes a rule must not stay only in this folder**, and this is the mistake worth pre-empting rather than discovering. A review is the *account* — what was believed, the evidence, the correction. Someone looking for a rule opens the document that owns rules of that kind; nobody thinks to read a history to find out what the rules are.

So when the work closes, each finding gets a destination: the PRD if it changed what the product is, `SOLUTION_DESIGN.md` if it changed the architecture, `PROJECT_WORKFLOW.md` if it changed how you work, the Workstream's spec pair if it is about one area, `AGENTS.md` if no session may get it wrong, `learnings/` if it transfers beyond this project — and **nowhere at all if it was only a correction**, in which case the review is already complete. Your `AGENTS.md` should carry that table; `project-init-kit/AGENTS.md` § *Where a rule lives* has the shape.

The review stays exactly where it is, and the rule's new home may link back to it for the full story. Nothing links the other way.

## Why this is separate from `learnings/`

| | |
|---|---|
| **a review** | contemporaneous, dated, tied to *this* code. Written before anyone knew how the story ended |
| **a learning** | distilled, reusable, written afterwards, meant to apply to your *next* project |

**A review is where a learning comes from.** Later, a pass over these files asks: *is any of this true beyond this codebase?* When the answer is yes it becomes a `learnings/` file — **and the review stays exactly where it is.** Extracting is not moving. Merging the two folders loses the thing that makes a review teachable, which is that it was written from inside the mistake.

## If you are handing this project to anyone

This folder is the part of your process that is also product. A reader learns more from how you were wrong than from the architecture you arrived at, and this is the only place that survives.
