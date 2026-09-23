---
created: 2026-09-08T17:38:40Z
updated: 2026-09-16T19:53:40Z
---

> **First learned:** 2026-08-11 18:23:37
> **Last updated:** 2026-08-13 18:10:19

## Context

This file is the extractable, reusable version of a document taxonomy that emerged after two full sessions of restructuring, auditing, and cross-reference cleanup on a real multi-service product. It exists so that starting a *new* project doesn't require re-deriving this structure from scratch. This file is the "what," ready to copy; the project it was extracted from has its own longer history of *why* each document earned its scope.

A second annex, [`02-document-section-reflection-questions.md`](02-document-section-reflection-questions.md), breaks every document in the table below into its actual sections and gives 3-5 brainstorming questions per section — use it when actually starting a new project and filling these documents in, not when just learning the shape.

## How this was learned

**Trigger:** After a full file-by-file audit pass on a live project, the owner asked to "log the final map" so the same structure could be rebuilt for a future project "more or less" from this template rather than from memory.

**Addendum trigger:** A request followed to also cover the layer *below* `CLAUDE.md` that the original pass didn't touch: the distinction between `CLAUDE.md` and the open `AGENTS.md` standard, how nested/per-folder `CLAUDE.md` files work, and a full representation of what can live inside `.claude/` (rules, skills, commands, agents, workflows, hooks, MCP, plugins, worktrees) — because the plan was to reuse this exact document structure for a second, smaller project, and the extension layer needed documenting up front rather than rediscovered. Researched against the current official Claude Code docs at the time rather than assumed, since this layer changes frequently between versions. A later ask in the same session pulled the project's own physical folder tree into this file directly, so the naming-convention rules that were already here as prose sit next to a real worked example instead of staying abstract — then asked for that tree to be anonymized: project name genericized to `<project-root>/`, Epic/story names reduced to their `epic-NNN-<name>`/`US-NNN` pattern, and every folder specific to *what* that particular project builds (service folders, its data layer) removed, so what remains is the minimal, truly generic documentation-layer shape rather than a snapshot of one product.

**The path:** The structure below is not what the source project started with. It went through a real Phase→Epic rename, two folder reorganisations, a PRD/NFR split, a Workstream-vs-Epic disentanglement, a restructure of the execution tracking (a flat `EPIC_EXECUTION.md`, split `functional-specs/` and `technical-specs/`, zero-padded Epic and Workstream folders), and a final file-by-file consistency audit that caught real drift: duplicated tables, stale section-number cross-references, inconsistent status vocabulary, mismatched persona tags, and a document (`GLOSSARY.md`) that stated its own table was canonical elsewhere while still containing a full copy of it two lines below.

**Things to be aware of:** every one of these documents earned its scope the hard way, by first having the wrong scope and being caught overlapping with something else. Copying the *shape* below into a new project on day one is fine. Copying content into the wrong document, or skipping the "does this already say that" check before writing, will reproduce the exact drift this cleanup was needed for in the first place.

## The Rule

### The document set, in dependency order

| # | Document | Answers | Depends on |
|---|---|---|---|
| 1 | `GLOSSARY.md` | What does this term mean? | Nothing — read first when a term is ambiguous |
| 2 | `PRD.md` | What are we building, for whom, why? | Glossary for vocabulary |
| 3 | `NFR.md` | What quality bar must it meet? | PRD (companion, not a subset) |
| 4 | `SOLUTION_DESIGN.md` | How is it built? What Workstreams does it decompose into? | PRD + NFR |
| 5 | `PLAN.md` | In what order, grouped into what Epics? | SOLUTION_DESIGN for Workstream IDs |
| 6 | `project-docs/execution/EPIC_EXECUTION.md` | What's the status of each story, right now? | PLAN for Epic names |
| 7 | `project-docs/functional-specs/`, `project-docs/technical-specs/` | What does a delivered Workstream actually do / how is it actually built? | Written incrementally as stories close, never upfront |
| 8 | `project-docs/execution/epic-NNN-*/US-NNN.md` | What, specifically, was asked for and accepted for one unit of work? | Nothing — the atomic unit everything else summarizes |
| 9 | `project-docs/PROJECT_WORKFLOW.md` | How does work actually flow through the system, and which doc do I touch when? | Everything above, it's the connective tissue |
| 10 | `.claude/skills/<name>/SKILL.md` | The executable version of #9, for one recurring task | PROJECT_WORKFLOW (self-contained copy, doesn't re-read it at runtime) |
| 11 | `CLAUDE.md` | What does every session need before touching anything? | Everything above — this is the *derived* summary, built last, not first |

Each row answers exactly one question. If a piece of content could answer two rows' questions, it belongs in whichever row is more specific, and every other row gets a pointer instead of a copy.

**Deliberately missing from this table: a testing-strategy document.** Which test framework(s) to use and how testing will actually work isn't decided upfront in this template — that decision is left to emerge once there's real code to test against, rather than speculated on before a first line of code exists. If a project reaches the point of actually needing this decided, it would most naturally land as a new row in this table, or fold into `NFR.md`'s existing Maintainability section (which already asks whether a test suite exists and what it covers) — not invented before there's a first line of code to write tests for.

### Non-negotiable naming conventions

- **Workstream** (functional area, not time-bound): `WS-NN`, two-digit zero-padded (`WS-00`… `WS-06`). Two digits because a project won't realistically exceed 99 functional areas — Epics and stories are a different, faster-growing count and get their own padding.
- **Epic** (sequential, time-bound build stage, one active at a time): `epic-NNN-name`, three-digit zero-padded folders (`epic-000-...`, `epic-001-...`).
- **User story**: `US-NNN`, sequential across the *whole project*, never reset per Epic, never reused.
- **Functional/technical spec files**: `ws-func-NN-name.md` / `ws-tech-NN-name.md`, matching the Workstream's own two-digit ID exactly.
- **Service folders** (once a project splits into multiple backend/frontend services): `<actor>-<service>` (e.g. `user-backend` / `admin-backend`, or whatever the actor split is), always hyphenated, flat at repo root, never concatenated, never nested under a shared parent folder.

### The physical folder tree, generic template

Copy this shape as-is into a new project; only the content of each file changes:

```
<project-root>/
├── README.md                     <- how a stranger runs it
├── AGENTS.md                     <- row 11: derived summary, built last, stays lean
├── CLAUDE.md                     <- a thin import of AGENTS.md, plus Claude-Code-only notes
├── .claude/
│   ├── settings.json             <- committed: permissions/hooks config
│   ├── settings.local.json       <- gitignored: personal overrides
│   └── skills/
│       └── <skill-name>/SKILL.md <- row 10: executable version of PROJECT_WORKFLOW.md, one recurring task
├── .githooks/pre-commit          <- stamps `updated:` on staged markdown
│
├── project-docs/                 <- EVERY document about building the project
│   ├── PRD.md                    <- row 2: what, for whom, why
│   ├── NFR.md                    <- row 3: the quality bar, companion to PRD not a subset
│   ├── SOLUTION_DESIGN.md        <- row 4: architecture, Workstreams (WS-NN), ADRs
│   ├── PLAN.md                   <- row 5: Epic sequencing, keyed to Workstream IDs
│   ├── GLOSSARY.md               <- row 1: vocabulary, read first when a term is ambiguous
│   ├── PROJECT_WORKFLOW.md       <- row 9: which document to touch, and when
│   ├── _ARCHITECTURE_EXPLAINED.md         <- how the code is split, and why
│   ├── execution/
│   │   ├── EPIC_EXECUTION.md              <- row 6: continuous, per-story status
│   │   ├── epic-000-<name>/               <- three-digit zero-padded Epic folder
│   │   └── epic-001-<name>/US-NNN.md      <- row 8: sequential project-wide, never reset per Epic
│   ├── functional-specs/ws-func-NN-*.md   <- row 7: two-digit, matches the Workstream's WS-NN exactly
│   ├── technical-specs/ws-tech-NN-*.md    <- row 7: same pairing, implementation side
│   ├── reviews/NN-<name>.md      <- what was believed here that turned out false
│   ├── learnings/NN-<name>.md    <- this file lives here
│   ├── templates/user-story.md   <- copied once per story
│   └── exploration/              <- raw research, kept as-is, never cited as decided
│
└── <the product's own source>    <- frontend/, backend/, whatever the thing actually is
```

**One rule governs that layout: `project-docs/` holds every document about *building* the project, and nothing that *is* the product.** The root keeps only what a first session must read without being told.

**And no leading dot on it.** A dotted folder is a contract with tooling meaning *machine-owned*: `ls` omits it, Explorer hides it, and most search tools skip it without a flag — so documents behind one are invisible to every staleness check that works by grepping. `.claude/` is dotted because nothing searches for it and every agent is handed that path literally. These documents are for a human.

Wherever the project's own source code and service folders live (frontend, backend, a data layer, whatever the product actually is) is out of scope for this template by design — that's product-specific, not part of the reusable documentation shape. This file standardizes the documentation layer sitting above the code; **`project-docs/_ARCHITECTURE_EXPLAINED.md` is its counterpart for the code itself**, and the project's own `AGENTS.md` folder map records the real, concrete layout.

### The three build-tracking axes, kept deliberately separate

- **Workstream** = *what area*. Doesn't complete. Can be revisited by a later Epic.
- **Epic** = *when, how much at once*. Whether a project runs Epics sequentially (one finished before the next starts) or allows some parallelism is a project-specific constraint — state it explicitly, it's not a universal property of "Epic."
- **Milestone** = *what ships*. The GitHub-native representation of an Epic, not a fourth concept.

### Which document to update, and when (the part that prevents drift)

The full table lives in `project-docs/PROJECT_WORKFLOW.md` § Which document to update, and when — copy that table verbatim into a new project's `PROJECT_WORKFLOW.md`, then adjust document names only. The one-line version: **story detail is continuous, Epic detail is per-Epic, product decisions are per-decision, architecture decisions get an ADR entry in place, everything else updates only when the fact it states actually changes.** Never update on a schedule, never update speculatively.

### Architecture Decision Records live inside the solution design doc

Not a separate file, not a separate folder. One table, at the end of `SOLUTION_DESIGN.md`, entries never deleted, only marked `Deprecated` with a date and reason. This keeps "current architecture" and "why it's not the other thing" in the same document, which is where someone actually needs both at once.

### `CLAUDE.md` is built last, and stays lean

Every other document above is a source; `CLAUDE.md` is the derived, always-loaded summary. Concretely: a folder map, a tech-stack pointer (not a restated tech-stack table), the confidentiality/behavioral constraints unique to this project, a first-session reading order (quick-resume path + full-orientation path), and a pointers section that names which doc is canonical for what, never inlining that doc's content. Target under ~300 lines. For each line, the test is: would removing this cause a wrong action? If not, cut it or turn it into a pointer.

### `CLAUDE.md` vs `AGENTS.md`

`AGENTS.md` is an open, tool-agnostic standard (Linux Foundation-stewarded, tens of thousands of repos as of late 2025): plain markdown, no required fields, read natively by Codex, Cursor, Copilot, Gemini CLI, Aider, Windsurf, and 20+ other tools. **Claude Code does not read `AGENTS.md` natively.** If a repo needs both (multiple AI tools in play), the supported pattern is a thin `CLAUDE.md` that imports it and adds Claude-specific instructions below:

```markdown
@AGENTS.md

## Claude Code
Use plan mode for changes under src/billing/.
```

A symlink (`ln -s AGENTS.md CLAUDE.md`) also works if there's nothing Claude-specific to add, but requires admin rights on Windows, so the `@`-import is the more portable default.

**When to use which:** a single-tool project (only Claude Code touches the repo) needs `CLAUDE.md` alone — adding `AGENTS.md` on top is pure duplication with nothing reading it a second way. `AGENTS.md` earns its place the moment a second AI coding tool joins the project; at that point it becomes the shared source of truth and `CLAUDE.md` shrinks to an import plus a short Claude-specific addendum.

### Nested `CLAUDE.md` and `.claude/rules/`

Two different mechanisms for scoping instructions below the project root, both real and both worth knowing before defaulting to "everything goes in the root `CLAUDE.md`":

- **Nested `CLAUDE.md`** (or `CLAUDE.local.md`): a `CLAUDE.md` inside a subdirectory of the working directory is discovered automatically but loads **on demand**, only when Claude actually reads a file in that subtree — not at session launch. Ancestor `CLAUDE.md` files (cwd walking up to the filesystem root) load in full at launch instead, ordered root-first so the most specific file is read last. Use this for a subtree with a genuinely different context — a service folder with its own Python-specific detail that's irrelevant while working on an unrelated frontend, for instance.
- **`.claude/rules/*.md`**: the sibling mechanism, scoped by file-glob instead of by directory. A rule with `paths:` frontmatter (e.g. `src/api/**/*.ts`) loads only when Claude reads a matching file; a rule without `paths:` loads at launch, same priority as `.claude/CLAUDE.md`. Reach for this when the split is by *file type or convention* cutting across the whole tree (e.g. "testing conventions," "API design rules") rather than by *directory*.

Official guidance: split out of the root `CLAUDE.md` once it approaches ~200 lines — long files still load in full but reduce instruction adherence.

### The `.claude/` folder

Everything Claude Code reads that's specific to one project:

```
.claude/
├── settings.json         committed   — permissions, hooks, model, env, statusLine
├── settings.local.json   gitignored  — personal overrides, same schema as above
├── CLAUDE.md              committed   — alternative to root CLAUDE.md, same effect
├── rules/*.md             committed   — topic-scoped instructions, optional paths:
├── skills/<name>/SKILL.md committed   — executable procedures for recurring tasks
├── commands/<name>.md     committed   — legacy single-file /command; skills supersede
├── agents/<name>.md       committed   — "subagents": isolated context, own tool access
├── workflows/<name>.js    committed   — multi-subagent orchestration scripts
├── output-styles/         committed   — only if the team shares a custom style
└── agent-memory/<agent>/  Claude-written — only for subagents with memory
```

Plus two things that live at the project root, not inside `.claude/`: `.mcp.json` (committed, team-shared MCP servers Claude Code itself connects to) and `CLAUDE.local.md` (gitignored, personal project notes, sibling to a gitignored `settings.local.json`).

**Naming collision worth flagging in any project that defines its own domain "agent" vocabulary**: `.claude/agents/` is a distinct Claude Code platform mechanism ("subagents" — an isolated-context-window helper Claude delegates to, e.g. a code-reviewer subagent). If a project's own product already has an "Agent" concept (a user-facing AI agent, say), say so explicitly in conversation and in the file itself, since "the agent" would otherwise be an overloaded term.

### Advanced extension points, documented but not always adopted

Four more pieces of the `.claude/` ecosystem, real and current, not necessarily needed by every project. Documenting the decision to skip one, when that's the choice, makes it a decision rather than a gap:

| Mechanism | What it is | Where it lives | Adopt when... |
|---|---|---|---|
| **Hooks** | Deterministic shell commands Claude Code runs at lifecycle events (`PreToolUse` can block a tool call outright, `PostToolUse` runs after one succeeds, `SessionStart` fires on launch/resume/compact). Unlike `CLAUDE.md`, these are enforced regardless of what Claude decides — settings rules are enforced by the client, not by Claude's judgment. | `hooks` key inside `settings.json` (project, user, or local scope) — not a separate folder | A `CLAUDE.md` rule keeps being described but not reliably followed (e.g. "always run the linter before committing") — that's the signal to promote it from advisory instruction to an enforced `PreToolUse`/`PostToolUse` hook instead of writing the sentence a third time |
| **MCP (`.mcp.json`)** | Claude Code's *own* config for connecting itself, as a coding tool, to external MCP servers (GitHub, a database, a design tool) during a session. **Naming collision to flag explicitly**: this is unrelated to a project's own planned MCP-server product architecture, if it has one — those would be services the project builds as part of its product, not something Claude Code the CLI reads to extend itself | `.mcp.json` at the project root, committed, team-shared | The team wants Claude Code itself (not the product) to read from an external system mid-session — e.g. querying a live issue tracker instead of pasting ticket text into chat |
| **Plugins** | A self-contained, distributable bundle of skills + agents + hooks + MCP servers (+ LSP servers), either installed from a marketplace or auto-discovered with zero install step via a `.claude-plugin/plugin.json` manifest | A plugin directory, installed at user or project scope | **The direct answer to reusing one project's structure in a sibling project without copy-paste drift**: once a skill or a rule set is meant to be shared and stay in sync across repos rather than duplicated by hand, package it as one plugin and enable it in both, instead of maintaining two independent copies |
| **Worktrees** | Isolated parallel git checkouts (`--worktree`/`-w` flag, `.claude/worktrees/<name>/`, `.worktreeinclude` for copying gitignored files like `.env` into each one, subagent `isolation: worktree`) so multiple sessions edit without colliding | `.claude/worktrees/` (add to `.gitignore`), `.worktreeinclude` at project root | Useful the moment a project's own working model allows multiple parallel sessions. **Not applicable** if a project's stated working model is explicitly sequential — one agent, one story at a time, no parallel work — worktrees exist specifically to run parallel isolated sessions, the opposite of that constraint |

### Reading order for a fresh session

**Quick resume:** `project-docs/execution/EPIC_EXECUTION.md`, then `PLAN.md` § Immediate Next Steps, then — if an Epic is open — that Epic's `epic-NNN-refinement.md`, which `EPIC_EXECUTION.md` names.

**The handoff is the committed files, not a separate handoff note.** An earlier version of this template sent a resuming session to gitignored scratch files. Tracked documents beat scratch notes for the reason version control exists: they are reviewed, they are shared, and they cannot quietly be the stale copy.

**Full orientation:** `PRD.md` → `NFR.md` → `SOLUTION_DESIGN.md` → `PLAN.md` → `project-docs/execution/EPIC_EXECUTION.md` → `project-docs/functional-specs/` + `project-docs/technical-specs/` → `project-docs/PROJECT_WORKFLOW.md` + the relevant skill. `GLOSSARY.md` is a standing reference outside this sequence, consulted on demand.

## Common mistakes table

| Mistake | Why it happens | The fix |
|---|---|---|
| Restating a table in a second document "for convenience" | Feels helpful in the moment | One canonical location per fact, always. Every other mention is a pointer, even if that means an extra click |
| Renumbering a section and stopping once the headers look right | The obvious fix (headers) is visible; the cross-references are not | After any renumber, grep the *whole repo* for `Section N` / `§N` patterns, not just the file you edited, and not just files that seem like "obvious candidates" |
| Inventing a new formatting convention instead of finding the one already in use | Faster than searching | Grep for how the same kind of thing is already written elsewhere before formatting something new |
| Treating a reflective "what do you think" question as an instruction to execute | Eagerness to be useful | If the message is framed as a question, answer the question first. Wait for an explicit go-ahead before writing anything |
| Adding a status/progress dimension to a document meant to be timeless (e.g. a glossary) | Status feels like useful context | A definition answers "what is this," not "is this built yet." Keep a separate, explicit `Status` field if genuinely needed, never bury delivery status inside the definition prose |
| Leaving a document's own text un-updated after moving what it describes | The move itself feels like the whole task | If a document says "the canonical version of X is here," and X moves, that sentence has to move or be rewritten too, it's part of the content, not incidental |
| Assuming an agentic tool reads `AGENTS.md` automatically because it exists in the repo | The two files look interchangeable and both describe "instructions for AI agents" | Claude Code only reads `CLAUDE.md`. An `AGENTS.md` with nothing importing it via `@AGENTS.md` is invisible to Claude Code no matter how complete it is |
| Building the same reusable skill/hook/rule set by hand a second time in a sibling project instead of packaging it once | Copy-pasting a folder is faster in the moment than setting up a plugin | Once a piece of `.claude/` is meant to be shared across repos, package it as a plugin so both projects read one source instead of drifting apart silently |

### Sources

Researched against official Claude Code documentation (all under `code.claude.com`, which `docs.anthropic.com/en/docs/claude-code/*` now redirects to):

- [How Claude remembers your project](https://code.claude.com/docs/en/memory) — `CLAUDE.md` hierarchy and load order, `AGENTS.md` interop, `.claude/rules/`
- [Explore the `.claude` directory](https://code.claude.com/docs/en/claude-directory) — full file/folder reference for project- and user-level `.claude/`
- [Plugins reference](https://code.claude.com/docs/en/plugins-reference) — plugin components, installation scopes, skills-directory (manifest-only) plugins
- [Automate actions with hooks](https://code.claude.com/docs/en/hooks-guide) — hook lifecycle events, enforcement vs. `CLAUDE.md` guidance, example use cases
- [Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp) — `.mcp.json` project scope vs. `~/.claude.json` local/user scope
- [Run parallel sessions with worktrees](https://code.claude.com/docs/en/worktrees) — `--worktree`, `.worktreeinclude`, subagent `isolation: worktree`
- [AGENTS.md](https://agents.md/) — the open standard's own spec page
