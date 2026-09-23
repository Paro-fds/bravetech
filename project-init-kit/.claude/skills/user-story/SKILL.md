---
name: user-story
description: Create, refine, update, or delete a user story for this project. Create writes the spec file and tracker row. Refine is pre-build scoping of an existing Backlog story — read the source, resolve open questions, record the decisions — before any code is written. Use whenever asked to write a new story, scope one out before building it, change an existing story's scope/status/tasks, or remove one.
created: 2026-09-08T17:38:40Z
updated: 2026-09-16T19:53:40Z
---

# User Story Skill

> **Setup, once, before first use:** replace `[OWNER]/[REPO]` below with your actual GitHub `owner/repo`, and `[TRACKER_PROJECT_NUMBER]`/`[Tracker Project Name]` with your GitHub Project (v2) board's number and name, if you're using one. If you're not using GitHub Issues/Projects at all, adapt §3 and the Create/Update/Delete procedures to whatever tracker `project-docs/PROJECT_WORKFLOW.md` § Work Tracking names instead.

## 1. Overview

Self-contained: this skill carries its own copy of the format and conventions below so it doesn't need to open `project-docs/PROJECT_WORKFLOW.md` to run. That file is the human-readable version of the same material — if the two ever disagree, treat the real `US-*.md` files in `project-docs/execution/` as the tiebreaker, then fix whichever doc is stale.

Vocabulary used below (Workstream, Epic, Milestone) is defined in `GLOSSARY.md` § Workstream, Epic, and Milestone. Short version: Workstream = functional area (not time-bound). Epic = a scoped, sequential build stage, worked one at a time — canonical in `PLAN.md`. Milestone = a deliverable checkpoint inside an Epic, effectively a release, represented on GitHub by a Milestone object.

---

## 2. User Story Format

```markdown
# US-NNN: [Short title]

**Status:** 🔲 Backlog / ✅ Done / etc.
**Milestone:** [exact GitHub Milestone title, e.g. "Epic 1 — <Name>"]
**GitHub Issue:** [#N](https://github.com/[OWNER]/[REPO]/issues/N)
**Depends on:** US-XXX (optional — only if there's a real dependency)

---

## As [role from GLOSSARY.md]
I want [feature or capability]
So that [outcome]

## Context
[What already exists. What state the codebase is in. Which files, components,
or prior stories this builds on. What NOT to assume is already done.]

## Acceptance criteria
- [ ] [Specific and binary]
- [ ] [...]

(Group AC under `### ` subheadings for a story with several distinct areas.)

## Out of scope
- [What NOT to build in this story]

## Tasks
- [ ] [Concrete implementation step]
- [ ] [...]

## Definition of done
- [ ] [Specific thing checked in the browser or app]
- [ ] [Project Owner] validates → story moved to Done

## As-built notes
[Only present once work starts or completes — what actually happened,
deviations from plan, decisions made along the way.]
```

**Story ID:** `US-001`, `US-002`, ... sequential across the whole project — never reused, never reset per Epic, never gapped.

**Tasks vs. Acceptance criteria:** AC = what must be true when done (testable outcomes). Tasks = the steps to get there (implementation actions).

**Role:** always a name from `GLOSSARY.md` § Actors and Roles. The project owner is "As [Project Owner] (Owner)".

**GitHub issue body** (per `project-docs/PROJECT_WORKFLOW.md`) contains ONLY: the "As / I want / So that" statement, a Context paragraph, and a `**Spec:** project-docs/execution/<epic-folder>/US-NNN.md` line. Never acceptance criteria, tasks, or Definition of Done — those live in the spec file only.

## 3. GitHub Projects context

If a GitHub Project (v2, board) is in use: **"[Tracker Project Name]"**, project number `[TRACKER_PROJECT_NUMBER]`, owner `[OWNER]` — `https://github.com/users/[OWNER]/projects/[TRACKER_PROJECT_NUMBER]`. Its `Status` single-select field typically has options like Backlog, To Do, In Progress, Review, Done. Every issue created via this skill's Create procedure (§ below) must be added to this project. Never set or change the `Status` field, and never move an issue between any board state — the project owner does that manually. This skill only ever creates issues, adds them to the project (leaving `Status` at whatever default the project applies), and edits the body/title; it does not touch board position or close issues except during an explicit delete (§ Delete below).

## 4. Definition of Done

A story is Done only when: (1) any tests it specifies pass; (2) the project owner performs the specific check listed in the story's Definition of Done and finds no issues; (3) the project owner gives joint validation. This skill never marks a story Done on its own — only the project owner does, in conversation.

## 5. Vocabulary Reference

Every term used in a story must resolve to a definition in `GLOSSARY.md` (Actors and Roles, System Components, Data Stores, Domain Vocabulary, Workstream/Epic/Milestone). If a term is ambiguous or missing, resolve/add it to `GLOSSARY.md` before writing the story.

---

## Procedure: Create a new user story

1. **Determine the next ID.** Scan `project-docs/execution/**/US-*.md`, take the highest `NNN`, use `NNN+1`. Never reuse or renumber existing stories.
2. **Determine the Epic folder and Milestone.** Check `PLAN.md`'s Epic Overview for the currently active Epic (only one is ever active — Epics are sequential, never parallel, unless this project's `PLAN.md` explicitly says otherwise). If the story could plausibly serve more than one Epic, ask rather than guessing. Confirm the exact Milestone title against GitHub: `gh api repos/[OWNER]/[REPO]/milestones --jq '.[] | {number, title}'`. If no matching milestone exists yet, stop and ask — don't invent one. Note which Workstream(s) the story primarily touches (from `SOLUTION_DESIGN.md` §2's Workstreams table) — mention it in the story's Context if it's not obvious from the Epic alone.
3. **Write the spec file** at `project-docs/execution/<epic-folder>/US-NNN.md` using the format in §2. Status starts at `🔲 Backlog`. No `As-built notes` section yet. Leave the GitHub Issue line as a placeholder until step 5 returns a real number.
4. **Draft the issue body** (title: `US-NNN: [Short title]`; body: story statement + Context + `**Spec:** project-docs/execution/<epic-folder>/US-NNN.md`, per §2's GitHub issue body convention).
5. **Create the GitHub issue:**
   ```
   gh issue create --repo [OWNER]/[REPO] --title "US-NNN: [Short title]" --body-file <tmp-file> --milestone "<exact milestone title>"
   ```
   Capture the returned issue URL/number.
6. **Add the issue to the tracker project** (§3, if in use): `gh project item-add [TRACKER_PROJECT_NUMBER] --owner [OWNER] --url "<issue-url>"`. Do not set or touch the `Status` field — the project owner manages board position manually.
7. **Fill in the GitHub Issue line** in the spec file with the real link.
8. **Add a row to `project-docs/execution/EPIC_EXECUTION.md`** in the matching Epic's table, status `🔲 Backlog`, linking to the new spec file.
9. **Report** the new story number, spec file path, and issue URL, and confirm the issue was added to the project. Do not move or set the project's `Status` field for the new item.

## Procedure: Refine a user story

Pre-build analysis for an existing Backlog story — the step between Create and actually implementing it. Analogous to `epic`'s Refine procedure, one level down. Never touches Status, and never marks a story ready or Done — only the Project Owner does that (§4).

1. **Read the source, not only the documents.** The story and everything it references (linked functional/technical specs, schema docs, stories named in `Depends on`) *and* the actual code the story will change. **This step is ordered first because skipping it has a measured cost.** On the project this procedure came from, an Epic's `PLAN.md` section made three claims about the code; reading a single source file falsified all three. A plan is written from the roadmap; a story has to be written from the source. **The most expensive kind of story is one whose premise was true when the roadmap was written** — it reads as correct at every review, and only the build discovers otherwise.
2. **Find the genuine open questions** — ambiguous requirements, unresolved technical choices, decisions the current Context does not already answer. A question the source answers is not an open question; resolve it by reading.
3. **Research before asking**, when the answer depends on external best practice rather than project-specific preference (a library choice, a protocol convention) — state findings and sources before presenting options.
4. **Ask the Project Owner** with concrete options and a recommendation where one exists, not open-ended questions.
5. **Record every decision** as dated additions to the story's `## Context` (`**Refined YYYY-MM-DD, ahead of build:**`), and update `## Acceptance criteria` and `## Tasks` in the same pass so they *reflect* the decisions rather than narrating them in prose nearby.
6. **Correct a false claim in place; do not quietly delete it.** Where refinement disproves something the story or `PLAN.md` already asserted, write the correction next to the claim it replaces. A section that does this is usually the half still worth reading a year later — an edited-away wrong premise teaches nobody why the story changed shape.
7. **Fix any stale cross-reference** noticed while reading — a link to a renamed file, a section number that moved. Don't leave it for `check-project-docs` to find later.
8. **Report** what was refined and every decision made. Do not proceed to implementation unless the Project Owner explicitly says to.

**What a good refinement looks like:** the story that comes out of it should be buildable without asking another question, and its `## Context` should record at least one thing that reading the source *changed*. A refinement that confirms every assumption it started with usually means the source was not actually read — step 1 exists because that is the common failure, not a hypothetical one.

## Procedure: Update an existing user story

1. **Locate** the spec file: `project-docs/execution/**/US-NNN.md`.
2. **Apply the requested change** (tasks, acceptance criteria, status, as-built notes, etc.) directly in the spec file.
3. **If status changed**, update the matching row in `project-docs/execution/EPIC_EXECUTION.md` to match.
4. **Only touch the GitHub issue** if the story statement, title, or Context itself changed — acceptance criteria, tasks, and Definition of Done checkbox changes never go to GitHub (§2). Use `gh issue edit <N> --title "..."` / `--body-file <tmp-file>` as needed.
5. **Never mark the story Done or close the issue** as part of an update — that only happens via explicit project-owner validation (§4).
6. **Report** exactly what changed and in which files.

## Procedure: Delete a user story

Destructive and touches shared GitHub state — before doing anything, list every file and reference that will change and confirm with the project owner.

1. **Search for cross-references first:** `grep -rn "US-NNN" project-docs/ *.md` (and any other doc types in use). A story can be referenced by other stories' `**Depends on:**` field, by `EPIC_EXECUTION.md`, by compacts/learnings, or by root docs. List every hit before touching anything.
2. **Remove the spec file**: `project-docs/execution/<epic-folder>/US-NNN.md`.
3. **Remove the row** from `project-docs/execution/EPIC_EXECUTION.md`.
4. **Fix every cross-reference found in step 1** — e.g. another story's `**Depends on:** US-NNN` needs updating or removing, not left dangling.
5. **Close (never delete) the GitHub issue** with a comment explaining why: `gh issue close <N> --comment "..."`. Issues are historical record — actually deleting one via `gh issue delete` is a separate, harder-to-reverse action and is not something this skill does automatically; if the project owner explicitly wants the issue gone rather than closed, that's a distinct, explicit request each time.
6. **Report** every file changed and the issue closed, so nothing was missed.
