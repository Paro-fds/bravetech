---
created: 2026-09-08T17:38:40Z
updated: 2026-09-16T19:53:40Z
---

# AGENTS.md — [Project Name]

> **Status: build this last.** This file is the *derived* summary of every document above, filled in only after they exist, in this order: `PRD.md` → `NFR.md` → `SOLUTION_DESIGN.md` → `PLAN.md` → `GLOSSARY.md` (finalized once `PLAN.md` is done) → `project-docs/PROJECT_WORKFLOW.md`. Don't write it before those exist — there's nothing to summarize yet.
>
> **Why `AGENTS.md` and not just `CLAUDE.md`**: if this project is used with more than one agentic tool (e.g. Claude Code and something else), `AGENTS.md` is the open standard read natively by most of them. `CLAUDE.md` (see that file, right next to this one) stays a thin import of this file, plus any Claude-Code-specific instructions.

**While the documents above are still open questions**, don't write this file.

**To fill them in**: paste the prompt from `STARTER_PROMPT.md` into your agent — works with any tool. If you're using Claude Code, the skill `.claude/skills/bootstrap-project-docs/SKILL.md` does the same thing in more detail and loads automatically; other tools need the manual prompt, since automatic discovery of `.claude/skills/` isn't guaranteed outside Claude Code.

**Once ready to write it**, aim for under ~300 lines, and for every line ask: *"would removing this line cause a wrong action?"* If not, cut it or turn it into a pointer.

Expected content, once built:
1. What this project is (2-3 sentences) — a pointer to `PRD.md`, not a copy
2. Folder map
3. Pointer to the tech stack (`SOLUTION_DESIGN.md` §5), not a restated table
4. Conventions specific to this project, including naming conventions (see below)
5. Confidentiality constraints, if any
6. Reading order for a first session (quick-resume path vs. full orientation)
7. Pointers section — which document is canonical for what, never its content re-injected here, **and where a rule goes when a piece of work produces one** (see below)
8. Reading order for a first session (quick-resume path vs. full orientation)

## Where a rule lives — the section most projects are missing

This is the one below that was added after it went wrong on the source project, and it is worth writing into your `AGENTS.md` on day one rather than after.

**A rule never lives only in a review, and a review is never required reading for doing the work.** A review is the *account*: what was believed, the evidence it was false, what changed. The **rule** that came out of it belongs in whichever document owns rules of that kind, moved there before the work that produced it is called done. The review keeps the reasoning and may be pointed at from the rule's new home. Nothing points the other way.

Write the outbound table into your own pointers section — the left column is the kind of thing a finding turns out to be, the right column is the document you have already decided owns it:

```markdown
| what the finding turned out to be | where the rule goes |
|---|---|
| what the product is, or who it is for            | PRD.md |
| a quality bar, a risk, a dependency              | NFR.md |
| an architecture decision or constraint           | SOLUTION_DESIGN.md, as an ADR |
| how we work, or what Done means                  | PROJECT_WORKFLOW.md |
| how one Workstream behaves / is built            | its func / tech spec pair |
| what a word means                                | GLOSSARY.md |
| something no session may get wrong               | this file |
| practice that transfers to another project       | learnings/ |
| nothing beyond the correction itself             | it stays in the review, which is then complete |
```

**Allow exactly one exception, and bound it**: work in flight. While an Epic is open its rules and open questions live in one file — `project-docs/execution/epic-NNN-*/epic-NNN-refinement.md` — **named from `EPIC_EXECUTION.md`, so there is one place to look rather than a folder to search.** At close they move, and an Epic that closes leaving rules in that file has not closed.

**The failure this prevents**, from the source project, because the abstract version does not land: a constraint recorded as a `###` subsection of a review was cited six times in one session as the basis for changing four source files. The Project Owner went looking for it — PRD, workflow, solution design, NFR, plan, execution tracker — and it was in none of them. The agent was applying a rule the human could not audit. That is not a lookup failure; it is a structural one, and the fix is a table like the one above plus the discipline of running it when work ends.

## Two document conventions worth adopting verbatim

**Number the folders whose files are a history: `NN-<name>.md`.** `reviews/` and `learnings/` both are. The number is the order the file was written, **assigned once and never reassigned** — a later insertion takes the next number, because a citation in an old commit message has to keep pointing at the same document. Sorting a record of how understanding changed by subject tells you nothing.

**Put `created` and `updated` in YAML frontmatter on every markdown file, in UTC:**

```yaml
---
created: 2026-09-08T20:21:51Z
updated: 2026-09-11T14:31:03Z
---
```

Full ISO-8601 with `Z`, never a local offset. **Do not maintain `updated` by hand** — `.githooks/pre-commit` in this kit stamps it on every staged markdown file, enabled once per clone with `git config core.hooksPath .githooks`. A hand-kept date is a second copy of something git already owns, and it goes stale the first week you are busy. The hook refuses to stamp a file with unstaged changes rather than sweep them into your commit.

## Naming conventions — the part of "Conventions" worth calling out on its own

Every project ends up with real naming rules — how components/files are cased, how booleans are named, which timezone convention applies to timestamps, how service folders are named. These are genuinely project- and language-specific, so what belongs in *this* file is the short version plus a pointer.

**If you are using the kit's recommended stack, the tables are already written**: `project-docs/_ARCHITECTURE_EXPLAINED.md` Part 4 carries them for Python and for TypeScript/React, along with the timestamp rule and the document-naming rules. Copy the rows that apply, or point here at that document — do not maintain two copies.

**If you are not**, or the moment your project needs a rule that document does not have, here is the **process** that produced a good table on the source project this kit was extracted from:

1. **State the baseline convention explicitly, per language/layer, the moment that language/layer exists** — don't leave it implicit or "whatever the first file happened to do." At minimum: casing for each identifier kind (files, components/classes, variables/functions, constants, booleans), and any project-wide non-negotiable (e.g. a timezone rule for every stored timestamp, a required prefix for boolean names).
2. **This is the confirmed baseline, not a speculative one** — write down conventions once they're actually decided/observed, not invented ahead of any real code needing them.
3. **Extend it here the moment a real correction happens, don't invent rules ahead of the code that would need them.** The first time a naming mistake is caught (a component named inconsistently, a timestamp stored in local time instead of UTC, a boolean without an `is`/`has`/`can` prefix), that becomes a new line in this section immediately — not a one-off fix left undocumented, and not generalized into a rule before it's actually been needed twice.
4. **Service/module folder naming** (once a project splits into more than one independently-run piece): pick one separator/casing convention (e.g. always-hyphenated `<actor>-<service>`, never concatenated, never nested under a shared parent) and state it here explicitly — see `project-docs/learnings/01-documentation-structure-template.md`'s own naming-convention section for the documentation-layer equivalent of this same idea (`WS-NN`, `epic-NNN-name`, `US-NNN`), which is already generic and doesn't need re-deriving.

A worked example of the *shape* this section should take (not values to copy — write your own per language actually in use):

```markdown
**Naming conventions:**
- **<Language/layer A>:** <file/class casing>; <variable/function casing>;
  booleans prefixed `is`/`has`/`can`/`should`; true constants `UPPER_SNAKE_CASE`.
- **<Language/layer B>:** <the language's own standard style guide, named
  explicitly>; any project-specific deviation from it stated here.
- **Service folders:** `<actor>-<service>`, always hyphenated, never
  concatenated, flat at repo root.

This is the confirmed baseline per language; extend it here the moment a
real correction happens, don't invent rules ahead of the code that would
need them.
```
