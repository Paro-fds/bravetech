---
name: check-project-docs
description: Audits this project's foundational documents (PRD.md, NFR.md, SOLUTION_DESIGN.md, AGENTS.md, GLOSSARY.md) for staleness and drift against what's actually been built, and for retired terminology that's crept back in. Reports findings only — never edits these five files without explicit confirmation. Use when asked to check/audit/review the project docs for consistency, or periodically after an Epic closes.
created: 2026-09-08T17:38:40Z
updated: 2026-09-30T16:04:08Z
---

# Check Project Docs Skill

## Why this exists, and why it isn't just "re-read the docs and see if anything looks off"

Foundational docs (`PRD.md`, `SOLUTION_DESIGN.md`, etc.) drift because they describe *intent*, while `project-docs/execution/EPIC_EXECUTION.md` and `project-docs/technical-specs/`/`project-docs/functional-specs/` describe *what actually got built* — and only the second kind gets touched on every story delivery. A vague re-read pass mostly re-confirms what's already believed. This skill instead **compares the foundational docs against the as-built ground truth**, plus a maintained list of terms this project has explicitly retired — that's what actually surfaces drift, not a general sanity check.

**Report only. Never silently edit `PRD.md`, `NFR.md`, `SOLUTION_DESIGN.md`, `AGENTS.md`, or `GLOSSARY.md`.** All five are `Per-decision`/`Per-architecture-decision`/`Session-critical` grain documents (`project-docs/PROJECT_WORKFLOW.md`'s doc-update table) — any real discrepancy found in them should be surfaced and confirmed with the project owner before fixing, never auto-corrected.

## Retired-terms checklist

Maintain and extend this list as terms get retired in this project — don't let it go stale itself. **A rename or a deletion adds a row here in the same commit that performs it**, or this table becomes the stale thing it exists to catch.

**Read the "Legitimate uses" column before reporting a hit.** Most of these words have honest meanings elsewhere, and a grep that flags them is worse than no check: it trains a reader to skip the output.

| Term/pattern | Status | Legitimate uses — not a finding | Retired |
|---|---|---|---|
| *(empty — add a row the day you retire your first term)* | | | |

**Two worked examples of the shape, from the project this skill came from — delete these once you have real rows of your own:**

> | `level` (as a synonym for the product's teaching unit) | Retired — the word is **`lesson`**. `AGENTS.md` § conventions | a **zoom** level, an **ARIA heading** level, an **effort** level. All three are current vocabulary | 2026-09-08 |
> | `✅ Accepted` as a story state | Retired — **there is no fifth state.** Acceptance is what makes a story Done; write `✅ Done — accepted YYYY-MM-DD` | the word *accepted* inside that Done string, and prose about the Project Owner accepting | 2026-09-10 |

What makes those rows useful is the **third column**, and it is the one people leave out. Both retired words have honest meanings elsewhere; a grep that flags every occurrence produces mostly false hits, and a check whose output is mostly noise is a check nobody reads twice.

## Procedure

```
Docs Check Progress:
- [ ] Step 1: Read the five foundational docs
- [ ] Step 2: Read the ground truth (EPIC_EXECUTION.md + Workstream specs)
- [ ] Step 3: Grep for retired terms
- [ ] Step 4: Cross-check references and cross-doc consistency
- [ ] Step 5: Check for undocumented real decisions
- [ ] Step 6: Report
```

**Step 1 — Read the five foundational docs**: `project-docs/PRD.md`, `project-docs/NFR.md`, `project-docs/SOLUTION_DESIGN.md`, **`AGENTS.md`**, `project-docs/GLOSSARY.md`.

> **`AGENTS.md`, not `CLAUDE.md`.** In this kit's arrangement `CLAUDE.md` is a thin file that imports `AGENTS.md` and adds only Claude-Code-specific notes; **`AGENTS.md` holds the folder map, the damage rules and the conventions**, and it is the document loaded into every session, which makes a stale line in it the most expensive kind. Read `CLAUDE.md` too — it should be a few paragraphs — but audit `AGENTS.md`. An earlier version of this skill named `CLAUDE.md` here, and would have missed a folder map in `AGENTS.md` contradicting the commands section of the same file.

**Step 2 — Read the ground truth**: `project-docs/execution/EPIC_EXECUTION.md` (what's actually Done, per Epic) and every `project-docs/technical-specs/ws-tech-*.md` / `project-docs/functional-specs/ws-func-*.md` for a Workstream that's had any story delivered. This is what step 4 compares the foundational docs against — not each other.

**Step 3 — Grep for retired terms.** Use the checklist above, exact strings, across all five foundational docs (`Grep` with the term, scoped to those five files). Every hit is a candidate finding — confirm it's actually the retired usage (not, e.g., a historical note explicitly marked as superseded) before reporting it as live drift.

**Step 4 — Cross-check references and cross-doc consistency:**
- Does every file path, section number (`§N`), or Epic/Workstream ID cited in the five foundational docs still resolve? (A renamed spec file, a renumbered `§` after an edit, a retired Epic number.)
- Does `SOLUTION_DESIGN.md` §2's Workstream table match `PLAN.md`'s Epic Overview's Workstream column, and does `GLOSSARY.md`'s Epic/Workstream/Milestone definitions match how both are actually being used?
- Does anything in `PRD.md`/`SOLUTION_DESIGN.md` describe a component, flow, or schema that Step 2's ground truth shows was built differently? (E.g. an access-model description in `PRD.md` that predates a real schema decision recorded in a technical spec.)
- Does **`AGENTS.md` §2's folder map** still match the repo — every path, and every file named beside a path? This is the highest-yield single check in the skill: the map names files, files move, and nothing fails when a line goes stale. Verify each path resolves with `ls`, rather than reading the map and finding it plausible.
- **Does `AGENTS.md` contradict itself?** It is long enough to, and §2's map naming one path while §9's commands name another is a real defect that has happened. Cross-check any file mentioned in more than one section.

**Step 5 — Check for undocumented real decisions.** Look for decisions that read as `PRD.md`-grain (scope, product) or `SOLUTION_DESIGN.md`-grain (architecture) but were never written back into either file — the gap `epic`'s Close catches at an Epic boundary, caught here between them. **The ground truth is what is committed**, so read:

- `git log --oneline` since the last Epic close, reading the commit *bodies* — if your project writes reasoning there, a decision recorded nowhere else is usually visible in one.
- The newest files in `project-docs/reviews/`, which is where a correction lands at the moment it is found.
- `PLAN.md` § Immediate Next Steps, for a decision described as pending that has since been made.

A decision that exists only in a commit body or a review, and is `PRD.md`- or `SOLUTION_DESIGN.md`-grain, is the finding.

**Step 6 — Report.** One finding per row: file, what's stale/contradictory/retired-term-usage, what the ground truth actually says, and a suggested fix — but don't apply any of them without the project owner confirming which to act on. If nothing is found, say so plainly; don't manufacture findings to justify the pass.
