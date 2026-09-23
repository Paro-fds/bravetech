---
created: 2026-09-08T17:38:40Z
updated: 2026-09-16T20:11:50Z
---

# Project Init Kit

A documentation-first starting structure for a new software project, built with **Specification-Driven Development (SDD)**: you document context *before* you code, rather than improvising it mid-conversation with an agent.

> **This folder is self-contained.** Everything needed to understand and use this structure is included inside it — nothing to fetch from elsewhere. Copy it as-is into your own new project's workspace.

## Install it, in four commands

```bash
# from inside your new, empty project directory
cp -r /path/to/project-init-kit/. .      # the trailing /. is what copies .claude and .githooks
git init                                  # if you have not already
git config core.hooksPath .githooks       # stamps `updated:` on every markdown commit
rm -rf project-init-kit                   # if you copied the folder rather than its contents
```

**The trailing `/.` is the whole trick, and getting it wrong is the most common way this goes silently wrong.** `cp -r project-init-kit/ .` skips the dotted folders on most systems, so you lose `.claude/` (every skill) and `.githooks/` (the timestamp stamping) — and nothing announces it. On Windows, copying in Explorer needs *Show hidden files* turned on first.

**Check it worked:** `ls -a` should show `.claude` and `.githooks`. In Claude Code, `/help` should list the skills below.

Then read `project-docs/_ARCHITECTURE_EXPLAINED.md`, and paste `STARTER_PROMPT.md` into your agent.

## Why this exists

Most agent-assisted projects drift because the agent is given the whole product in one conversation, re-derived from scratch every session. This kit is the opposite bet: a small, ordered set of documents that give an agent the right context at the right time, so a session can start productive instead of re-explaining the product every time.

It also captures a real architectural pattern (layered backend structure — see `project-docs/learnings/03-backend-layered-architecture-template.md`) worth reusing on any new backend service, not just documented once and forgotten.

## What's in this kit

```text
project-init-kit/
├── README.md                        <- this file
├── STARTER_PROMPT.md                <- the prompt to paste into your agent to begin
├── AGENTS.md / CLAUDE.md            <- built last, a derived summary of everything below
├── project-docs/                    <- EVERY document about building the project
│   ├── _ARCHITECTURE_EXPLAINED.md   <- 0. READ first — how the code is split, and why
│   ├── PRD.md                       <- 1. fill in first
│   ├── NFR.md                       <- 2.
│   ├── SOLUTION_DESIGN.md           <- 3.
│   ├── PLAN.md                      <- 4.
│   ├── GLOSSARY.md                  <- 5. finalized last
│   ├── PROJECT_WORKFLOW.md          <- 6. which document to touch, and when
│   ├── templates/user-story.md      <- copy this for every story
│   ├── execution/
│   │   ├── EPIC_EXECUTION.md        <- tracker, fills itself in as work happens
│   │   └── epic-NNN-slug/           <- one folder per Epic, holding its US-NNN.md files
│   ├── functional-specs/README.md   <- no fixed template, written once real behaviour ships
│   ├── technical-specs/README.md    <- same, implementation side
│   ├── reviews/README.md            <- what you believed that turned out false
│   ├── learnings/README.md          <- practice that transfers to your next project
│   │   └── 01-, 02-, 03-*.md        <- three worked examples, shipped; yours start at 04
│   └── exploration/                 <- raw research, kept as-is, never cited as decided
├── .githooks/                       <- pre-commit, stamps `updated:` on staged markdown
│                                       enable once: git config core.hooksPath .githooks
└── .claude/skills/                  <- executable Claude Code skills, see below
    ├── bootstrap-project-docs/      <- the starter prompt, as a skill
    ├── user-story/                  <- create/refine/update/delete a user story
    ├── epic/                        <- create/refine/close an Epic
    ├── get-work-status/             <- read-only "where are we" status readout
    ├── check-project-docs/          <- audits the foundational docs for drift
    ├── document-learning/           <- writes a project-docs/learnings/ file
    ├── prepare-compact/             <- makes the committed files a sufficient handoff
    ├── scaffold-backend-service/    <- scaffolds a new backend service (+ 12 template files)
    └── scaffold-frontend-app/       <- scaffolds a React + TypeScript frontend
```

## The one rule the layout enforces

**`project-docs/` holds every document about *building* the project, and nothing that *is* the product.** The repository root keeps only what a first session must read without being told: `README.md`, `AGENTS.md`, `CLAUDE.md`.

That split is worth more than it looks, and it was installed on the source project only after the absence of it caused a real failure: product docs, process docs, teaching material, review records, tooling and this kit all shared a root and one catch-all folder with no rule about which was which. A session then asked what closing an Epic involved, found nothing, and **proposed inventing a procedure that already existed** two folders away. That is not a lookup failure, it is a structural one — and it is the kind that gets worse silently, because everything still works, it just cannot be found.

**`project-docs/` is the name the source project uses too, and keeping it is worth more than it looks.** That project had named the folder after itself — a word from its author's own language — for exactly the reason you might want to do the same: a folder named after the project reads as a signature, and a folder named `docs` reads as ignorable.

It was renamed anyway, and the reason is worth one paragraph before you decide. A name that has to be explained cannot do a folder's first job, which is telling a stranger what is inside. And the moment the kit and the project it came from share a name, **every path in every document transfers between them unchanged** — there is nothing to translate, and so nothing to drift. That mattered here: an earlier version of this kit shipped one folder layout while the skills bundled inside it assumed another, and the half that was wrong was the half a student reads first.

So rename it if you have a reason. If you do, grep once for `project-docs/` and fix the pointers — a few dozen, all in markdown — and know that you are taking on the translation the shared name removes.

**No leading dot**, whatever you call it. `.project-docs` would be hidden by `ls`, by Explorer, by most editor trees and by many search tools. `.claude/` is dotted because a machine owns it; these documents are for a human.

## The skills, and what each is for

These are [Claude Code skills](https://code.claude.com/docs/en/skills) — they load automatically when their description matches what's being asked, or can be invoked by name. All nine assume this kit's document/story conventions.

They were extracted from a real project's working setup and then genericized: project-specific vocabulary, precedents and findings taken out, and `[OWNER]/[REPO]`-style placeholders left anywhere they touch GitHub. **What survives is the procedure and the reason for it** — where a skill says *this is the step that fails most often*, that is a real failure someone had, not a hypothetical.

| Skill | Use it to... |
|---|---|
| `bootstrap-project-docs` | Interview you section by section to fill in `PRD.md` → `NFR.md` → `SOLUTION_DESIGN.md` → `PLAN.md` → `GLOSSARY.md` → `PROJECT_WORKFLOW.md`. Same job as `STARTER_PROMPT.md`, loads automatically. |
| `user-story` | Create a new `US-NNN.md` (+ GitHub issue), **refine** one before building it, update one, or delete one — the day-to-day unit of work. |
| `epic` | Create a new Epic, Refine one before its stories are written, or Close one (consolidation: closeout doc, functional+technical spec pair, staleness check, Milestone close). |
| `get-work-status` | A read-only "where are we" readout: current Epic, last Done story, next story to build, unresolved items from the last session. |
| `check-project-docs` | Audit `PRD.md`/`NFR.md`/`SOLUTION_DESIGN.md`/`CLAUDE.md`/`GLOSSARY.md` against what's actually been built, and for retired terms creeping back in. Reports only, never auto-edits. |
| `document-learning` | Write or update a `project-docs/learnings/` file the right way — checking first that it *is* a learning rather than a review, and including the real failures rather than only the clean outcome. |
| `prepare-compact` | Push the session's real work into the story/tracker/review files, then check the documented resume path still names the next action — so the committed tree *is* the handoff. Writes no handoff file of its own, and doesn't run `/compact`. |
| `scaffold-backend-service` | Lay down a new FastAPI + SQLAlchemy service's folder structure and boilerplate, using the Clean Architecture layering from `_ARCHITECTURE_EXPLAINED.md` Part 1. Requires the project's documents to already exist. |
| `scaffold-frontend-app` | Lay down a React + TypeScript + Vite frontend on Feature-Sliced Design, with Tailwind, React Router, TanStack Query, Zustand, the Steiger architecture linter and Vitest wired up — and the linter *proven* to fail on a violation before it reports success. Same precondition. |

**Two of the nine scaffold code rather than documents** — `scaffold-backend-service` and `scaffold-frontend-app` — and both refuse to run until the documents exist. That refusal is the point: scaffolding first means choosing your layers before you know your domain.

**One-time setup**: `user-story` and `epic` reference `[OWNER]/[REPO]` and, if you use a GitHub Project board, `[TRACKER_PROJECT_NUMBER]`/`[Tracker Project Name]` — open those two files once and fill in your actual values (or adapt the GitHub-specific steps to whatever tracker you're using, per `project-docs/PROJECT_WORKFLOW.md` § Work Tracking).

**Why the *documentation* has this shape**: `project-docs/learnings/01-documentation-structure-template.md` (full methodology, naming conventions) and its annex `02-document-section-reflection-questions.md` (the section-by-section reflection questions, the same ones already embedded in each document above).

**Why the *code* has this shape**: `project-docs/_ARCHITECTURE_EXPLAINED.md` — **Clean Architecture** on the backend and **Feature-Sliced Design** on the frontend, the one rule behind each, the naming conventions, the recommended stack for both halves, and a checked reading list for going further. `03-backend-layered-architecture-template.md` carries the backend's longer reasoning.

Those three learnings ship as **worked examples of the form**, which is why they are numbered `01`–`03` and your own start at `04`.

## The order you fill things in — not alphabetical order

```text
PRD.md                   <- what, for whom, why — THE FIRST document, depends on nothing
       ↓
NFR.md                   <- what quality bar (can move in parallel with the PRD)
       ↓
SOLUTION_DESIGN.md        <- how it's built, in what Workstreams
       ↓
PLAN.md                   <- in what order, grouped into what Epics
       ↓
GLOSSARY.md               <- the vocabulary — starts as soon as a first PRD exists, FINALIZED last
       ↓
project-docs/PROJECT_WORKFLOW.md  <- which document to touch, and when
```

`_ARCHITECTURE_EXPLAINED.md` is not in that sequence because **you do not fill it in — you read it, then decide.** It already contains answers. What it asks of you is that you accept or replace each one deliberately, and record what you chose in `SOLUTION_DESIGN.md` §5 where the rest of your architecture lives.

**Why the Glossary isn't first, despite the intuition**: without knowing yet what the product is, you don't know which vocabulary deserves an entry. The Glossary can start filling in as soon as a first PRD draft exists, but it only gets finalized once `PLAN.md` is done — that's when there's enough material to actually know what the product is. Its "Workstream, Epic, and Milestone" section is the exception: generic, product-independent, already filled in from day one.

`AGENTS.md` / `CLAUDE.md` and everything under `project-docs/execution/`, `functional-specs/`, `technical-specs/` and `reviews/` **don't get filled in now**: `AGENTS.md`/`CLAUDE.md` are the *derived* summary of everything else, built last; the rest fills in once there is real work to record, not before.

## Try the PRD without an agent first

**For `PRD.md` specifically**: before opening an agent at all, take the time to answer the reflection questions yourself — on paper, in a draft, or directly in the file. This isn't a formality: it's the point of the exercise. An agent can help *formalize* an answer you already have in mind, but if you ask it to supply the answer instead, you skip the actual skill this document is meant to build: your own capacity to think through and plan the thing you're building.

Once the PRD is genuinely your own thinking, lean on the agent more for the documents that follow (`NFR.md`, `SOLUTION_DESIGN.md`, `PLAN.md`...) — that help is more legitimate once the foundational thinking is already done, on the document that defines what you're building.

## Filling in the documents with an agent

Copy the prompt from **`STARTER_PROMPT.md`** into your agent (works with any tool — Claude Code, or any other agentic coding tool). It walks the agent through asking each document's questions, one section at a time, in the right order, without ever inventing an answer for you. If you're using Claude Code, the skill `.claude/skills/bootstrap-project-docs/SKILL.md` does the same thing and loads automatically.

**Rule to watch for**: if the agent starts drafting several documents at once without asking you anything, stop it and paste the prompt again — the goal isn't speed, it's that the content is genuinely yours. And even when it does ask instead of inventing, the real goal is that **you** already thought through the answer, not that you improvised it in front of the agent.

## Once the documents are filled in

Move into the Explore → Plan → Implement → Commit cycle: use `PLAN.md`'s Epic sequencing to pick the first Epic, `project-docs/templates/user-story.md` to write its first story, and build from there.

**Scaffold the code at this point, and not before** — `scaffold-backend-service`, then `scaffold-frontend-app`. Scaffolding first means choosing your layers before you know your domain, and the layer you get wrong is the one you will not notice for a month. `project-docs/execution/EPIC_EXECUTION.md` starts tracking status the moment the first story exists; `project-docs/functional-specs/` and `project-docs/technical-specs/` start once the first story actually ships.
