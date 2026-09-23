---
name: get-work-status
description: Reports current project status — the current Epic, the last story marked Done, any story in progress, the next story to build per dependency order, and what PLAN.md's Immediate Next Steps carries forward. Read-only, makes no edits. Use at the start of a session to resume quickly, or whenever asked "where are we," "what's next," or "what's the status."
created: 2026-09-08T17:38:40Z
updated: 2026-09-16T19:53:40Z
---

# Get Work Status Skill

Read-only, and makes no edits — if it finds drift it reports it. Automates the **Quick resume** reading order in your `AGENTS.md`, so it does not have to be run by hand and its steps stay the same every time. That section is canonical for the order; if this skill and it ever disagree, `AGENTS.md` wins and this file is what gets fixed.

> **The handoff is the committed files, not a handoff document.** This skill reads the tracker, the plan and the newest review, because those are what a session that was not here can actually trust. See `prepare-compact`, whose whole job is keeping them sufficient.

## Procedure

1. **Read `project-docs/execution/EPIC_EXECUTION.md`** — find the current Epic: the one marked `🟡 In progress`, and its story table.
   - **If no Epic is `🟡 In progress`, the project is *between* Epics** and there is no current story. Say that plainly rather than reporting the last closed Epic as if it were current, and go straight to step 4 — between Epics, `PLAN.md` § Immediate Next Steps is the only thing that knows what happens next. This is a normal state, not an error; it is the state immediately after any Epic closes.
2. **Read `PLAN.md`'s Epic Overview table** — cross-check the Epic status matches; if it doesn't, flag the mismatch (this is exactly the kind of drift `check-project-docs` looks for, but a status mismatch found here is worth surfacing immediately, not deferred).
3. **From the current Epic's story table**, identify:
   - The **last story marked `✅ Done`**.
   - Any story **`🟡 In progress`** — there should be **at most one**, and two is a finding worth reporting on its own. Any story **`⛔ Blocked`**, with the reason it carries. Those four states are the whole list (`PROJECT_WORKFLOW.md` § Story states); **`✅ Accepted` is not a state** and a story carrying it is drift.
   - The **next story to build**, per the Epic's documented dependency-respecting build order (stated in its `EPIC_EXECUTION.md` section, e.g. "US-001 → US-004 → US-002 → ...") rather than raw story-ID order, if such an order is documented. If no explicit build order exists, use the first `🔲 Backlog` story by ID.
4. **Read `project-docs/PLAN.md` § Immediate Next Steps.** This is the project's carry-forward instruction — what a previous session deliberately left for the next one, which the story tables alone do not show. **Check whether item 1 names something already done**; a resume path whose first item is complete is the most common form of drift here, and reporting it is more useful than following it.
5. **Read the most recently changed file in `project-docs/reviews/`** — `ls -t` rather than by filename, since these are named by subject and not by date. It carries what was believed recently and turned out false, which is the context least likely to survive a compact.
6. **Report**, in this order:
   - Current Epic (number, name, status).
   - Last Done story (ID + title).
   - In-progress story, if any.
   - Next story to build (ID + title), and whether it needs Refine (per the `user-story` skill) before building.
   - **Immediate Next Steps item 1**, verbatim or lightly condensed — don't drop specifics like "the schema is settled, don't reopen it" — and say if it looks already done.
   - The newest review's subject, one line, so its corrections are not re-derived.
   - Anything from step 2's Epic-status cross-check that didn't match.

Keep the report itself short — this is a status readout, not a re-derivation of the whole project. Point to the source files rather than re-explaining their full content.
