---
name: document-learning
description: Write or update a file in project-docs/learnings/ capturing practice that transfers to a project unrelated to this one. Checks first that it is a learning at all rather than a review or a lesson, since two other folders have a stronger claim on most findings. Use whenever a piece of work produced a non-obvious, reusable habit worth persisting beyond this session.
created: 2026-09-08T17:38:40Z
updated: 2026-09-30T16:04:08Z
---

# Document Learning Skill

Automates `project-docs/PROJECT_WORKFLOW.md`'s learning-file convention so the structure is consistent every time, rather than reconstructed from memory of the last one.

## Step 0 — is this a learning at all?

**Two other folders have a stronger claim on most findings, and this is the step that was missing.** `project-docs/learnings/README.md` is canonical; ask in this order and stop at the first yes:

| Question | Destination | Not this skill |
|---|---|---|
| Is it content that *is* the product — material a user or reader consumes? | wherever your product's content lives | ✓ |
| Is it a correction to what we believed about *this* code? | `project-docs/reviews/` | ✓ |
| Is it practice that would help on a project unrelated to this one? | `project-docs/learnings/` | **this skill** |

**Say which one it is and why, before writing anything.** A finding that fails the third question is not a small learning — it belongs somewhere else, and filing it here makes this folder a dumping ground whose files nobody trusts to be reusable. The honest test: *strip out every name specific to this project. Is anything left worth reading?*

**A review is the usual source.** Most learnings start as a `reviews/` entry and get extracted later by asking "is any of this true beyond this codebase?" — and **the review stays where it is.** Extracting does not move or delete it; the review is still the better document about this project's own code.

## The non-negotiable rule

**"How this was learned" must include real failures and corrections, not just the clean final outcome.** This is the single most important thing this skill enforces. A learning file that only describes what the final answer turned out to be is not what this convention is for — the wrong turns, the things that got corrected, and why, are the actual reusable value. If a piece of work had no real corrections along the way, that itself is worth a one-line note rather than padding the section with a narrative that implies more drama than there was.

## Procedure

1. **Get the real current date/time**: your shell's real clock (e.g. PowerShell `Get-Date -Format "yyyy-MM-dd HH:mm:ss"`, or `date "+%Y-%m-%d %H:%M:%S"`). Never assume today's date from conversation context — sessions can span real elapsed time, and an assumed date can silently be wrong.
2. **Check whether this is a new topic or an update to an existing one.** Scan `project-docs/learnings/` for a file already covering this subject. If one exists, this is an **update**, not a new file — go to step 3a. Otherwise, it's **new** — go to step 3b.

3a. **Updating an existing file:**
   - Bump `**Last updated:**` to the real timestamp from step 1 (leave `**First learned:**` untouched).
   - Add new content to the relevant sections — append to "Things to be aware of," add rows to "Common mistakes," append a new dated entry to "Decision Log — Sequence of Changes" if the file has one. Don't rewrite sections that are still accurate.
   - Skip to step 6.

3b. **New file — take the next number in the sequence.** `NN-kebab-case-name.md`: `04-trusting-a-new-tool.md`, not `trusting_a_new_tool.md`. Name it for the **practice**, not for the incident that produced it.

   **The number is the order the file was written, assigned once and never reassigned.** A later insertion takes the next free number rather than the one its subject suggests — a citation in an old commit message has to keep pointing at the same document. Sorting a record of how understanding changed by subject tells you nothing.

4. **Write the metadata block and title:**
```markdown
> **First learned:** YYYY-MM-DD HH:MM:SS
> **Last updated:** YYYY-MM-DD HH:MM:SS

# Title — named for the practice, not for the story that produced it
```

5. **Write the body, in this order:**
   - **`## Context`** — what this documents and, importantly, *why it's worth capturing as reusable knowledge* — not just what happened, but what future sessions/services would otherwise have to re-derive.
   - **`## How this was learned`** — three required parts:
     - **Trigger:** what prompted this (a direct request, a critique, a bug hit in the wild).
     - **The path:** what actually happened, in enough detail that a wrong turn is visible as a wrong turn — not smoothed into "we decided X" when the real sequence was "tried Y, it broke because Z, corrected to X."
     - **Things to be aware of:** concrete gotchas — specific enough that someone hitting the same situation recognizes it immediately, not generic advice.
   - **`## The Rule`** — the actual reusable guidance, generalized beyond the one instance that produced it (use placeholder names/terms where the original was specific to one story/service, so the rule reads as applicable elsewhere).
   - **`## Common mistakes`** — a table (`Mistake | Why it happened | Fix`) of *real* corrections that happened, not hypothetical ones. Leave a placeholder note if the work is still in progress and mistakes haven't happened yet — don't pre-populate with imagined ones.
   - **`## Decision Log — Sequence of Changes`** *(optional — include for multi-step work with enough discrete decisions to be worth a timeline; skip for a short, single-decision learning)* — append-only, dated entries, in the order things actually happened.

6. **Report** the file path (and, for an update, what was added vs. left unchanged).
7. **Ask whether the structure itself should change too.** A learning that says *"set a project up differently next time"* has a second home: the scaffolding that sets projects up — these skills, `project-docs/_ARCHITECTURE_EXPLAINED.md`, the document templates. Prose and scaffold are meant to be refreshed in the same pass, and they drift silently when they are not: a scaffold that still lays down the shape a learning just rejected will be believed, because it *runs*. Say so in the report; do not silently edit the scaffolding as a side effect of writing a learning.
