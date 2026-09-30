---
name: scaffold-backend-service
description: Scaffold a new FastAPI + SQLAlchemy backend service using this kit's layered architecture pattern (Entities/DAL/BLL/DTO). Use once a new service's PRD/CLAUDE.md/README already exist and it's time to lay down its actual folder structure.
created: 2026-09-08T17:38:40Z
updated: 2026-09-30T16:04:08Z
---

# Scaffold Backend Service Skill

## Why this exists

Read `project-docs/_ARCHITECTURE_EXPLAINED.md` first if the *why* behind any piece here is unclear — Part 1 explains the layers, Part 5 the stack, and `project-docs/learnings/03-backend-layered-architecture-template.md` carries the long reasoning. This skill covers the *how*, not the *why*. It exists so every backend service in this project starts from the same settled structure directly, instead of re-deriving it (and re-making the same corrected mistakes) from scratch each time.

## Hard precondition — do not skip

Per this kit's "New sub-project workflow" (see `CLAUDE.md`/`AGENTS.md` once written): **no source file gets created before scope is agreed.** Before running this skill, `<service>/PRD.md`, `<service>/CLAUDE.md`, and `<service>/README.md` must already exist. If any are missing, **stop and say so** — scaffold nothing, and point out that scope needs to be agreed (brainstorm → PRD → CLAUDE.md → README) first. This skill only ever runs *after* that gate, never instead of it.

## What this skill does *not* do

It builds infrastructure only — `core/`, `dal/database.py`, the `api/v1/` router aggregator, `main.py`, Alembic wiring, `pyproject.toml`. It does **not** create any `entities/ent_*.py`, `dal/dal_*.py`, `bll/bll_*.py`, or `api/v1/dto/dto_*.py` file — those are real feature work, built per-story via `user-story`, not scaffolding. A freshly scaffolded service has an empty (but working) `api/v1/` with nothing mounted yet.

## Procedure

```
Scaffold Progress:
- [ ] Step 1: Confirm the precondition (PRD/CLAUDE/README exist)
- [ ] Step 2: Create the folder structure
- [ ] Step 3: Copy and adapt the template files
- [ ] Step 4: Install dependencies
- [ ] Step 5: Alembic init
- [ ] Step 6: Verify it actually boots
- [ ] Step 7: Report
```

**Step 1 — Confirm the precondition.** Check `<service>/PRD.md`, `<service>/CLAUDE.md`, `<service>/README.md` all exist. Stop here if any are missing (see above).

**Step 2 — Create the folder structure** inside `<service>/`:
```
app/{__init__.py, main.py}
app/core/__init__.py
app/entities/__init__.py
app/dal/__init__.py
app/bll/__init__.py
app/api/__init__.py
app/api/v1/__init__.py
app/api/v1/dto/__init__.py
database/.gitkeep
```

**Step 3 — Copy and adapt the template files** from this skill's `templates/` folder (paths below are relative to that folder → relative to `<service>/`):

| Template | Destination | Adapt |
|---|---|---|
| `pyproject.toml` | `pyproject.toml` | Replace `{{SERVICE_NAME}}` with the service's folder name. Add any service-specific dependency named in its own `CLAUDE.md` tech stack table. |
| `core_config.py` | `app/core/config.py` | Add the service's own `Settings` fields, per its `README.md`'s Environment variables table — secrets get no default (see the comment already in the template). |
| `core_logging.py` | `app/core/logging.py` | Copy verbatim, no changes needed. |
| `core_middleware.py` | `app/core/middleware.py` | Copy verbatim, no changes needed. |
| `core_exceptions.py` | `app/core/exceptions.py` | Copy verbatim — starts with just `AppError`/`NotFoundError`/`DuplicateKeyError`; business exceptions get added per-story. |
| `core_exception_handlers.py` | `app/core/exception_handlers.py` | Copy verbatim — starts empty; handlers get added per-story alongside the business exceptions above. |
| `dal_database.py` | `app/dal/database.py` | Copy verbatim, no changes needed. |
| `main.py` | `app/main.py` | Replace `{{SERVICE_TITLE}}` with the service's display name. |
| `api_v1_init.py` | `app/api/v1/__init__.py` | Copy verbatim — router include lines get uncommented/added per-story. |
| `alembic_env.py` | *(used in Step 5, not copied directly yet)* | — |
| `env.example` | `.env.example` **and** `.env` | Add the service's own vars from its `README.md`. |
| `gitignore` | `.gitignore` | Copy verbatim, no changes needed. |

**Step 4 — Install dependencies.** With `uv`: `uv sync` from `<service>/` (creates `.venv`, installs pinned deps, installs the service itself editable, so `import app` works everywhere, including Alembic, with no `sys.path` hack). With plain `pip`: create a `.venv`, `pip install -e .`.

**Step 5 — Alembic init:**
1. `alembic init alembic` (via `uv run alembic init alembic` if using `uv`).
2. Replace the generated `alembic/env.py` with this skill's `templates/alembic_env.py` (the generated one has default un-wired boilerplate; this one is already correctly pointed at `app.core.config.settings` and `app.dal.database.Base`).
3. No migration to generate yet — there are no DAL models until the first story adds one.

**Step 6 — Verify it actually boots.** Don't just assume the scaffold is correct — prove it:
1. `uvicorn app.main:app --port 8000` in the background (or your chosen port).
2. Check the log output shows clean structlog-formatted startup lines (`Started server process`, `Application startup complete`) with no traceback.
3. `curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8000/docs` → expect `200`.
4. Stop the server.

**Step 7 — Report.** Confirm every file created, that it boots clean, and that the next step is the first real story (via `user-story` Create, or `epic` Refine first if this service's own story batch hasn't been planned yet) — which is what will add the first `entities/`/`dal/`/`bll/`/`api/v1/dto/` files.
