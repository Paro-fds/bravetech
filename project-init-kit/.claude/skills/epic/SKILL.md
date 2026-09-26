---
name: epic
description: Create, refine, or close an Epic for this project — the Epic-level counterpart to the user-story skill. Create scaffolds a new Epic (folder, PLAN.md, EPIC_EXECUTION.md, GitHub Milestone, Workstream confirmation). Refine does pre-build scoping/analysis across an Epic's whole story batch before stories are created. Close runs the full end-of-Epic consolidation: closeout doc, functional+technical spec pair, PRD.md/SOLUTION_DESIGN.md staleness check, GitHub Milestone close. Use whenever asked to start a new Epic, scope out an Epic's stories before creating them, or close/finish an Epic.
created: 2026-09-08T17:38:40Z
updated: 2026-09-16T19:53:40Z
---

# Epic Skill

> **Setup, once, before first use:** replace `Paro-fds/bravetech` below with your actual GitHub `owner/repo`. If you're not using GitHub Milestones, adapt the Create/Close procedures' GitHub steps to whatever tracker `project-docs/PROJECT_WORKFLOW.md` § Work Tracking names instead.

## 1. Overview

Self-contained, same spirit as `user-story`: carries its own copy of the relevant format so it doesn't need `project-docs/PROJECT_WORKFLOW.md` open to run. If this file and `PLAN.md`/`EPIC_EXECUTION.md`'s actual content ever disagree, treat the real files as the tiebreaker and fix whichever is stale.

Vocabulary: `GLOSSARY.md` § Workstream, Epic, and Milestone. Whether Epics run strictly sequentially (one at a time, never in parallel) is a project-specific convention — check `PLAN.md`'s own stated rule rather than assuming. Epics mostly map 1:1 to Workstreams (`SOLUTION_DESIGN.md` §2 is canonical for Workstream IDs/names); an Epic touching a second Workstream's corner is the documented exception, not the default — don't assume it without checking.

## 2. PLAN.md formats

**Epic Overview table row** (`PLAN.md`, top of file):
```
| **Epic N** | Name — short description | WS-NN | <status emoji + text> |
```
Status values in use: `⏳ Not started`, `🟡 In progress — ...`, `✅ Done — closed YYYY-MM-DD, see project-docs/execution/EPIC_EXECUTION.md`.

**Epic detail section** (`PLAN.md`, one per Epic, in Epic order):
```markdown
## Epic N — Name

**Workstream:** WS-NN Name
**Goal:** [one or two sentences — what's true once this Epic is done]

[1-2 paragraphs: why this Epic exists / what it covers, pointing to
project-docs/functional-specs/ws-func-NN-*.md and project-docs/technical-specs/ws-tech-NN-*.md
for behavior/implementation detail rather than repeating it here]

---
```

## 3. EPIC_EXECUTION.md format

One section per Epic, in Epic order:
```markdown
## Epic N — Name

**Workstream:** WS-NN Name
**Status:** [emoji + text, mirrors PLAN.md's Epic Overview row]

[1 paragraph: scope, pointing to the func/tech spec pair]

[Optional: dependency-respecting build order note, if story IDs don't
match the order they need to be built in]

| Story | Title | Status | Spec |
|---|---|---|---|
| US-NNN | ... | 🔲 Backlog | [US-NNN.md](epic-NNN-slug/US-NNN.md) |

---
```

## 4. Epic closeout doc format

`project-docs/execution/epic-NNN-slug/epic-NNN-closeout.md`.

**Once you have written one, it becomes the precedent — read the previous Epic's closeout before writing the next.** The template below leaves several things open on purpose (how to record an Epic that grew mid-flight, how to record an item left outstanding by decision rather than by omission), and the answer to each is easier to copy than to re-derive.
```markdown
# Epic NNN Closeout — Name

**Workstream:** WS-NN Name
**Status:** ✅ Done — closed YYYY-MM-DD
**Goal:** [same goal line as PLAN.md's detail section]

Frozen record of what this Epic delivered. Full story-by-story detail lives
in project-docs/execution/EPIC_EXECUTION.md and each story's own spec file — not duplicated
here. Behavior and implementation, consolidated across all N stories, are
extracted into project-docs/functional-specs/ws-func-NN-*.md and
project-docs/technical-specs/ws-tech-NN-*.md.

## Stories Delivered

| Story | Title | Spec |
|---|---|---|
| US-NNN | ... | [US-NNN.md](US-NNN.md) |

All N stories ✅ Done.

## Split to Unscheduled

[Table of any stories deliberately split out without a Milestone so the
Epic could close without them, if any — omit this section if none.]

## Tracking

[If the project uses Milestones: `Milestone "Epic N — Name" closed YYYY-MM-DD,
N/N issues closed`, plus any reconciliation needed. **If it tracks work as files
(as this one does), say so and say that Steps 2 and 7 were skipped rather than
forgotten** — a closeout that is simply silent about two of eight steps reads as
an incomplete close a year later.]
```

---

## Procedure: Create a new Epic

1. **Confirm this is actually the next Epic.** Check `PLAN.md`'s Epic Overview — if Epics in this project run sequentially, the immediately-prior Epic should be `✅ Done`. If it isn't, stop and ask before creating a new one.
2. **Determine the Workstream.** Check `SOLUTION_DESIGN.md` §2's Workstreams table. If this Epic maps to an existing, not-yet-delivered Workstream, use it. If it needs a genuinely new Workstream, add a row there first (next sequential `WS-NN`) — don't invent an Epic-Workstream mapping without updating the canonical table.
3. **Create the folder**: `project-docs/execution/epic-NNN-slug/` (slug matches the Epic name, kebab-case).
4. **Add the Epic Overview row and detail section to `PLAN.md`** (§2 above), status `⏳ Not started` or `🟡 In progress` if stories are being drafted immediately after.
5. **Add the Epic section to `project-docs/execution/EPIC_EXECUTION.md`** (§3 above), with an empty story table (or populated, if Refine already ran and stories exist).
6. **Create the GitHub Milestone**: `gh api repos/Paro-fds/bravetech/milestones -f title="Epic N — Name"`. Confirm the exact title matches what's in `PLAN.md`/`EPIC_EXECUTION.md` verbatim — the `user-story` skill's Create procedure matches on this exact string.
7. **Report** the new Epic number, folder, Milestone, and Workstream, and whether Refine (stories not yet drafted) or `user-story` Create (stories ready) should run next.

## Procedure: Refine an Epic

Epic-level scoping before any of its stories get created — analogous to `user-story`'s Refine, one level up: open questions resolved, a story batch planned, dependencies mapped, before a single `US-NNN.md` file exists.

1. **Establish scope**: what capability does this Epic deliver, end to end? Ask if it isn't already clear from the Epic's one-line description in `PLAN.md`.
2. **Resolve build-blocking open questions** — technical choices (libraries, schema, protocols) the Epic's stories can't be written without. Research external best practice where relevant (state findings + sources before asking); ask for project-specific preference. Record resolutions in `SOLUTION_DESIGN.md` (§15 Open Questions, or §14 as an ADR if it's architecture-level) or the Workstream's technical spec, whichever already exists.
3. **Plan the story batch**: draft a list of stories (title + one-line scope each) covering the Epic's full scope, without creating spec files yet. Identify real dependencies between them.
4. **Determine build order**: if dependencies mean story-ID order isn't build order, work out the actual sequence — this becomes the "dependency-respecting build order" note in `EPIC_EXECUTION.md` (§3 above).
5. **Write it down in `project-docs/execution/epic-NNN-slug/epic-NNN-refinement.md`, then report it.** The report is for the Project Owner to answer; the file is so that the answers, the findings and the open questions survive a compact and are findable by a session that was not here. **Name that file from `EPIC_EXECUTION.md`'s Epic section**, because your `AGENTS.md` reading-order section sends a resuming session to it and nothing else will say what it is called.

   It carries: the findings from reading the source (numbered `E<N>-<n>`, with a status column), any disagreement with what `PLAN.md` or a review predicted for this Epic, the open questions with a recommendation for each, and the story batch in build order. **While the Epic is open this file is where its rules live** — the one bounded exception in `AGENTS.md`'s "where a rule lives" table — which is the whole reason it is a file and not a message.

6. **Report the plan** (story list + build order + resolved open questions) and confirm before creating any stories.
7. **Create the stories**, one by one, via the `user-story` skill's Create procedure, once confirmed.

## Procedure: Close an Epic

The consolidation backstop — required whenever an Epic completes, per `project-docs/PROJECT_WORKFLOW.md`'s "Which document to update, and when." Every step below is real, not optional; skipping the spec-pair consolidation or the PRD/SOLUTION_DESIGN check is exactly the kind of drift `check-project-docs` exists to catch later, so do it now instead.

```
Epic Close Progress:
- [ ] Step 1: Confirm every story is actually Done
- [ ] Step 2: Reconcile GitHub issue/Milestone state
- [ ] Step 3: Write the closeout doc
- [ ] Step 4: Consolidate the functional + technical spec pair, and relocate every rule out of epic-NNN-refinement.md
- [ ] Step 5: Check PRD.md and SOLUTION_DESIGN.md for staleness
- [ ] Step 6: Update EPIC_EXECUTION.md and PLAN.md
- [ ] Step 7: Close the GitHub Milestone
- [ ] Step 8: Report
```

**Step 1 — Confirm every story is actually Done.** Every row in this Epic's `EPIC_EXECUTION.md` table should be `✅ Done`. If any aren't, and the project owner still wants to close (e.g. splitting a straggler to Unscheduled), confirm explicitly which stories are being split out and why before proceeding.

**Step 2 — Reconcile GitHub issue/Milestone state.** `gh api repos/Paro-fds/bravetech/milestones/<N>` and check `open_issues == 0`. A story marked Done in the spec but whose issue is still open (can happen with PR-based merges that don't auto-close) needs reconciling: `gh issue close <N> --comment "..."` explaining the bookkeeping gap.

**Step 3 — Write the closeout doc** (§4 above) at `project-docs/execution/epic-NNN-slug/epic-NNN-closeout.md`.

**Step 4 — Consolidate the functional + technical spec pair.** Read back across every story's As-built notes and decisions (not just the closeout doc's summary table — the real substance is in each story's own file). Write or update `project-docs/functional-specs/ws-func-NN-*.md` (behavior only, what a user/visitor/admin experiences) and `project-docs/technical-specs/ws-tech-NN-*.md` (implementation only, cross-referencing the functional spec rather than repeating it). If either file already has partial content from incremental updates during the Epic, reconcile rather than overwrite blindly — check for drift between what stories actually built and what got written down mid-Epic.

**Empty the refinement file of its rules, and say where each one went.** `epic-NNN-refinement.md` held this Epic's rules while it was open, which is the bounded exception in `AGENTS.md`'s "where a rule lives" table. Closing is when the exception ends: every rule in it moves to the document that owns rules of its kind — usually this spec pair, sometimes `SOLUTION_DESIGN.md` as an ADR, sometimes `AGENTS.md`. **An Epic that closes leaving a rule only in its refinement file has not closed.** What stays behind is the account: the findings, what was believed, what reading the source falsified. Mark the file's status closed and leave it as the Epic's history beside its closeout.

**How many pairs, when the Epic touched several Workstreams.** Write a pair for the Workstream the Epic **declared**, plus any other whose contribution is a *coherent whole subject* rather than a corner — and record the remaining Workstreams' contributions as a paragraph each in the closeout instead.

The reason is that **an existing spec is read as the account of its whole area, so a thin one is worse than an absent one.** An Epic that touched one corner of another Workstream would produce a spec describing that corner while saying nothing about the rest — and the next person to open it has no way to know it is partial. A paragraph in the closeout makes no such claim. `project-docs/functional-specs/README.md` carries the rule.

**Say where each spec starts.** A Workstream whose core was built before the story convention existed has no As-built notes to consolidate from, so its spec covers only what the closing Epic delivered into it and must say so in a header — otherwise it silently claims to be that Workstream's whole history.

**Step 5 — Check PRD.md and SOLUTION_DESIGN.md for staleness.** This is explicitly separate from Step 4 — the Workstream spec pair documents *behavior and implementation*; PRD.md and SOLUTION_DESIGN.md make *product and architecture* claims that can go stale independently (a scope statement, a component diagram, an access-model description). Re-read the sections of each that this Epic's domain touches and ask: does anything here still describe the pre-Epic state, or contradict what actually got built? Report findings and get confirmation before editing either — both are `Per-decision`/`Per-architecture-decision` grain documents (`PROJECT_WORKFLOW.md`'s table), not routinely-edited ones.

**Read two things beyond this Epic's domain, because scoping the check to the domain is how the worst finding gets missed.** The findings you expect are inside the domain: a delivered prerequisite still described as pending, a superseded rule, an enforced claim still hedged. The expensive one is not. On the project this procedure came from, the worst finding at an Epic close was a section of `PRD.md` asserting that most of the documents it listed did not exist yet — **false for two whole Epics**, nowhere near that Epic's subject, and something nothing would ever have re-read except a procedure that says to. So also check:

- **Any section that makes an inventory or existence claim** — "only X and Y exist today", "not yet built", "planned for", a related-documents list. These go stale by the project simply continuing, with no edit anywhere near them, which is why no story ever catches them.
- **Anything the Epic *delivered* that a document still describes as a prerequisite, a risk, or future work.** An Epic that unblocks something almost always leaves a sentence somewhere still waiting for it.

**Step 6 — Update `EPIC_EXECUTION.md` and `PLAN.md`.** Status line → `✅ Done — closed YYYY-MM-DD`, with a pointer to the closeout doc. `PLAN.md`'s Epic Overview row and detail section get the same treatment (detail section becomes a closed pointer).

**Step 7 — Close the GitHub Milestone**: `gh api -X PATCH repos/Paro-fds/bravetech/milestones/<N> -f state=closed`, only once Step 2 confirms `open_issues == 0`.

**Step 8 — Report.** Confirm every step above, explicitly call out whether Step 5 found anything in PRD.md/SOLUTION_DESIGN.md needing a follow-up edit (even if the answer is "checked, nothing stale"), **list every rule moved out of `epic-NNN-refinement.md` and the document each one landed in** — or say the file held none — and name the next Epic per `PLAN.md`'s Epic Overview. Don't start it; that's a separate, explicit instruction.
