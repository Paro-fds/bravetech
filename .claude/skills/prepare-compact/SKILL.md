---
name: prepare-compact
description: Prepares a session for compaction by making the project's own committed files a sufficient handoff — pushing this session's real work into the story/tracker/review files, then verifying the documented resume path names the actual next action. Does NOT run the compact (that is a separate, user-triggered /compact). Use when asked to prepare for a compact, wrap up a session, or write a handoff.
created: 2026-09-08T17:38:40Z
updated: 2026-09-30T16:04:08Z
---

# Prepare Compact Skill

**The handoff is the committed files, not a separate handoff document.** A compact writes its own summary of the conversation; what it cannot do is make the *repository* honest. So this skill's job is to leave the tree in a state where a session that has lost every word of this conversation can resume from `AGENTS.md`'s reading order alone.

> **Why no handoff file.** An earlier version of this skill wrote two git-ignored notes into a scratch folder. When a real compact arrived, the useful move turned out to be different: push the session's work into the tracked files, point `PLAN.md § Immediate Next Steps` at the actual next action, and compact. That resumed cleanly, which is the only test that matters — and unlike a scratch note, it is versioned and it is read by everyone. **If your project does keep a handoff folder, substitute your own write-the-file step for Step 4 below;** the rest applies unchanged.

## Procedure

**Step 1 — Push this session's real work into the durable record, before anything else.** This is the whole point of the skill. The tracking documents are supposed to be updated as work happens (`project-docs/PROJECT_WORKFLOW.md` § "Which document to update, and when"), and a compact is not a place to store what should have been written down. Check each:

- **A story worked on this session whose `## As-built notes` do not yet reflect it.** Real progress and decisions belong in the spec file even when the story is not ready to be Done — `user-story`'s Update procedure. Only the Project Owner marks a story Done.
- **`project-docs/execution/EPIC_EXECUTION.md`** — a status or build-order note that changed mid-session.
- **`project-docs/PLAN.md`** — an Epic status line, or a resolved open question.
- **A correction that belongs in `project-docs/reviews/`** — something believed at the start of this session that turned out false. `reviews/README.md`'s rule is that these are written *at the moment of the finding*, and the reason is arithmetic: it costs almost nothing while fresh and is close to impossible to reconstruct later. **A compact that is about to discard the conversation is the last moment.**
- **Transferable practice that belongs in `project-docs/learnings/`** — a habit that would help on any project, not just this one. `document-learning`.

If any of these are outstanding, **do them now.** Do not leave them as a "resume here" item unless the Project Owner says to defer. Ask if it is unclear whether something rises to this level.

**Step 2 — Get the real date from the shell's clock.** Never from conversation context; a session can span real elapsed time.

**Step 3 — Check the tree, and say what you find.** `git status --short` and `git log --oneline -1`. Uncommitted work is not automatically wrong, but a fresh session needs to know whether the tree is clean, deliberately dirty, or dirty by accident. **Also check `git stash list`** — a forgotten stash survives a compact and is invisible to a session that does not think to look.

**Step 4 — Verify the resume path actually lands somewhere useful.** Read what `AGENTS.md`'s reading-order section sends a fresh session to, in order, and confirm each still says something true:

- `project-docs/execution/EPIC_EXECUTION.md` — is the story table true *right now*?
- `project-docs/PLAN.md § Immediate Next Steps` — **does item 1 name the next action, or the one just completed?** This is the step that fails most often and the one that matters most: a resume path whose first item is already done sends the next session to re-derive what to do.
- the most recently changed file in `project-docs/reviews/`.

Fix whatever is stale. This is the substitute for a handoff document, and it is a better one because it is committed and versioned.

**Step 5 — Report** what Step 1 saved, the tree state from Step 3, and where Step 4 leaves a fresh session. Then stop. **Do not run `/compact`** — that is the Project Owner's action, and this skill only prepares for it.
