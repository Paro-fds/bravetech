---
created: 2026-09-08T17:38:40Z
updated: 2026-09-16T19:53:40Z
---

> **First learned:** 2026-09-08 15:30:00
> **Last updated:** 2026-09-08 15:30:00

## Context

A real multi-service backend went through several rounds of critique before its internal layering settled into something worth reusing as-is on the *next* backend service, rather than re-derived (and re-making the same corrected mistakes) from scratch each time. This file is the generalized, project-agnostic version of that settled structure — pulled out of one project's own internal learning notes and its companion scaffolding skill, so a new project can start a backend service already at the "settled" shape instead of at the "first attempt, about to get critiqued" shape.

This complements `01-documentation-structure-template.md`: that file is about the *documentation* layer sitting above a project; this file is about the *internal code* layer sitting inside one backend service. Use it once `SOLUTION_DESIGN.md` §4/§6 has decided a service needs a real internal structure (not a single-file script), before writing the first line of that service's source.

## How this was learned

**Trigger:** A second backend service in the same project needed to share a database table with the first one. Deciding *how* forced a real, researched architectural question — duplicate the data-access mapping in each service, or extract a shared package — which in turn required the layering itself to already be principled enough to reason about cleanly. That pressure-test is what surfaced most of the rules below; they weren't designed upfront, they were corrected into shape.

**The path:** The first backend service did not start with this structure — it went through real critique rounds that caught: business logic accidentally depending on a framework-specific ORM type instead of a plain domain object; an exception hierarchy split across layers that made it unclear which layer was allowed to decide an HTTP status code; and a "just add the field to the model" instinct that leaked a persistence-layer concern (a database column) into code that should only ever see a domain concept. Each of these got corrected once, then written down as a rule so the correction didn't have to happen again on the next service. When a second service needed the same database, the choice between "duplicate the mapping" and "share a package" was resolved by weighing a concrete tradeoff (schema-drift risk of duplication vs. tooling-convention conflict of a shared package) rather than picked by default — see the Decision Log for how that specific case was reasoned through.

**Things to be aware of:**
- This structure earns its cost on a service with real business logic and more than a couple of entities. A single-endpoint utility service does not need four layers — don't impose this on something that doesn't have the complexity to justify it.
- The one-way dependency rule (below) is easy to state and easy to accidentally violate the first time a "just this once" shortcut feels convenient — e.g. importing an ORM model directly into a route handler to save a conversion step. Every one of those shortcuts, taken once, becomes very hard to find and undo later, once a dozen more routes have copied the same shortcut.
- Deciding whether to duplicate a data-access mapping or share it as a package across services is a real, non-obvious tradeoff, not a default — see the Rule's "Sharing data access across services" subsection.

## The Rule

### The four layers, and the one-way dependency

```
Entities  ←  Data Access Layer (DAL)  ←  Business Logic Layer (BLL)  ←  API layer
```

Dependencies point **one way only**, left to right is never allowed:

- **Entities** — plain domain objects (a dataclass, a Pydantic model used as a domain type, or equivalent in your language). No framework imports, no ORM base class, no knowledge that a database exists at all. This is what every other layer actually thinks about.
- **Data Access Layer (DAL)** — the *only* layer allowed to import the ORM/database library. It maps between the framework's persistence representation (e.g. a SQLAlchemy mapped class) and a plain Entity, and exposes functions/methods that take and return Entities only — never the ORM row type. Keep the real mapped class module-private (e.g. prefix it `_UserRow` or equivalent) so nothing outside this layer is even tempted to import it directly.
- **Business Logic Layer (BLL)** — all business rules, validation, and orchestration across DAL calls. Takes Entities in, returns Entities out — never a DTO, never an ORM type. This is where "can this action happen" gets decided, not in the API layer and not in the DAL.
- **API layer** — request/response handling only. Converts an incoming request into whatever the BLL needs, calls the BLL, converts the BLL's Entity result into a response shape (a DTO). Contains no business rules of its own.

**Why one-way, not a shortcut "just this once":** the moment a route handler imports an ORM model directly, or the BLL starts returning a database row, the whole point of the boundary is gone — the layer that was supposed to be swappable/testable in isolation now silently depends on the thing it was insulated from. This is the single most common way this structure erodes; treat any exception request to it as a signal to look harder for the correct layer, not as a pragmatic one-off.

### DTOs live at the edge, not in the middle

A DTO (Data Transfer Object — the shape of a request body or response payload) belongs to the API layer only. It exists to define the *wire contract*, which is allowed to differ from the internal Entity shape (different field names, a subset of fields, a computed field). Never let a DTO leak into the BLL or DAL — those layers only ever see Entities.

### Exceptions: one flat file, named semantically, mapped in exactly one place

- Keep exception classes in a single flat file (e.g. `core/exceptions.py`), not split per-layer or per-feature. Name them for the business meaning of the failure (`InvalidCredentialsError`, `DuplicateEmailError`), never for which layer raised them (`DAL_NotFoundError`) — a caller shouldn't need to know which layer failed to understand what went wrong.
- Map each exception to an HTTP status (or equivalent transport-level response) in exactly one place (e.g. `core/exception_handlers.py`). No other file should ever decide a status code from an exception type — that decision belongs in one place so it can't drift into two different answers for the same exception.
- It's fine, and often correct, for one exception to cover more than one underlying cause when the caller shouldn't be able to distinguish them (e.g. a single generic "invalid credentials" exception covering both "wrong password" and "expired token," so a caller can't use error specificity to enumerate which part of an auth check failed).

### Sharing data access across services

The moment two independent services need to read/write the same underlying data store, there's a real choice, not a default:

| Option | When it's right | The real cost |
|---|---|---|
| **Duplicate the data-access mapping** in each service (each service defines its own DAL-layer model for the shared table) | Services are meant to stay independently deployable, each with its own dependency/environment setup, and the shared table's schema changes rarely and predictably (owned by exactly one service's migration history) | Risk of schema drift if the duplicated mappings aren't kept in sync — mitigate with a clear single owner of the actual schema/migrations, and a code comment in every duplicate pointing at that owner |
| **Extract a shared package** (a shared library both services depend on) | Services already share a dependency-management setup (a monorepo-style workspace, a shared virtual environment/lockfile), or the shared schema changes often enough that duplication would drift immediately | Usually means collapsing both services onto one shared environment/lockfile — a real cost if your project's convention is one independent environment per service |

Whichever is chosen, write the decision down as an ADR entry in `SOLUTION_DESIGN.md` §14 — this is exactly the kind of choice that looks arbitrary in hindsight if the tradeoff that was weighed isn't recorded.

### A minimal folder shape for one backend service

```
<service>/
├── app/
│   ├── main.py                 <- app entry point / server bootstrap
│   ├── core/
│   │   ├── config.py           <- settings/env loading
│   │   ├── exceptions.py       <- flat file, one class per business failure
│   │   └── exception_handlers.py  <- the one place exceptions map to a response status
│   ├── entities/                <- plain domain objects, no framework imports
│   ├── dal/                     <- the only layer allowed to import the ORM/DB library
│   ├── bll/                     <- business rules, takes/returns Entities only
│   └── api/
│       └── v1/
│           └── dto/             <- request/response shapes, API layer only
└── <dependency manifest, migrations folder, etc. per your stack>
```

A freshly scaffolded service should have working infrastructure (`core/`, the DAL's database connection setup, an empty API router) but **no** `entities/`, `dal/`, `bll/`, or `dto/` file yet — those are real feature work, added per unit of work (per user story), not part of scaffolding. Building them ahead of a real need produces dead code that has to be maintained without ever being exercised.

### A concurrency gotcha worth checking the moment a second writer appears

If more than one process/service will write to the same lightweight file-based database (e.g. SQLite), don't assume a documented concurrency setting (e.g. "we use WAL mode") is actually in effect — verify it directly (query the actual runtime setting) rather than trusting a comment or a tech-stack table. A single-writer setup never surfaces the gap; it only becomes a real correctness risk the moment a second writer joins, which is exactly when it's easiest to miss because nothing about adding the second service *looks* like a database change.

### A cross-origin gotcha worth checking the moment a second, separate-origin frontend appears

If a browser-based frontend calls this backend from a different origin (different port or domain), backend-only verification (a command-line HTTP client) will not catch a missing CORS configuration — CORS preflight and enforcement are purely browser-side, invisible to any non-browser client. The only reliable check is a real browser-based test (a headless-browser script or manual click-through) driving the actual frontend against the actual backend.

## Common mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Importing the ORM-mapped class directly in a route handler "just to save a conversion step" | Feels like unnecessary boilerplate in the moment | Always convert to/from the Entity at the DAL boundary, even when it feels redundant for a trivial field set — the boilerplate is what keeps the boundary real |
| Letting a DTO field name or shape leak into the BLL's own logic (e.g. branching on a DTO's optional field instead of the Entity's) | The DTO is already in scope in the API handler, feels convenient to pass through | Convert DTO → Entity before calling into the BLL, always, even for a single-field request |
| Splitting exception classes by layer (`DAL_NotFoundError`, `BLL_NotFoundError`) | Feels like it mirrors the architecture cleanly | Name exceptions for the business meaning of the failure, not the layer — a flat file, one meaning per class |
| Assuming a documented concurrency or CORS setting is actually implemented, because it's written down in a config/architecture doc | Documentation describes intent, and intent is easy to mistake for verified fact | Verify runtime behavior directly (query the actual setting, run the actual browser-based check) the moment a second service or a second origin joins, don't trust the doc alone |

## Decision Log — Sequence of Changes

1. **First backend service built** — the four-layer split (Entities/DAL/BLL/API) and the flat-exceptions-file convention adopted after real critique caught boundary violations in an earlier draft.
2. **Second backend service needed to share a table with the first** — resolved via the "Sharing data access across services" tradeoff above: duplicated the DAL-layer mapping rather than extracting a shared package, specifically because the project's convention was one independent dependency environment per service, and a shared package would have required collapsing both onto one environment.
3. **Second service's build surfaced two real gaps, not decisions**: a documented-but-not-implemented database concurrency setting, and a missing CORS configuration only caught by an actual browser-based test after a command-line check had passed cleanly — both generalized into this file's two gotcha subsections above.
