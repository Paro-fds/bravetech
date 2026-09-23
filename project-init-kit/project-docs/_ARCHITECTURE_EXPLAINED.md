---
created: 2026-09-16T19:40:29Z
updated: 2026-09-16T20:11:50Z
---

# Architecture, explained

**Answers:** how is the code split, why that way, and what is each file allowed to import?
**Read this:** once, before you write the first source file of either half. Then keep it open while you write the next ten.

This is the one document in the kit that hands you answers instead of questions.
Everything else under `project-docs/` asks you to think — `PRD.md` asks what you are building, `SOLUTION_DESIGN.md` asks how.
This file says: *here is a structure that works, here is why it works, and here is what it costs.*

**You may replace any of it.** What you may not do is leave it implicit.
An architecture nobody wrote down is not a simpler architecture; it is the same number of decisions, made once each by whoever touched the file first, and never written where the next person can find them.

---

## Part 0 — The one idea

Most of what follows is a consequence of a single rule.
Robert C. Martin calls it the **Dependency Rule**, and states it in one sentence:

> Source code dependencies must only point inward.
> Nothing in an inner circle can know anything at all about something in an outer circle.

Alistair Cockburn arrived at the same place from a different direction, and his framing is the one that makes it click:

> The asymmetry to exploit is not that between *left* and *right* sides of the application but between *inside* and *outside*.

His point is that the user interface and the database are **the same kind of thing**: both are external, both are replaceable, and both will try to smear themselves through your business rules if you let them.
A web framework and a Postgres driver are not opposites — they are two adapters on two ports of the same machine.

### What the rule buys you

- **You can test the middle without starting anything.** No server, no database, no browser. If your business rules need a running Postgres to be exercised, they are not isolated from Postgres.
- **You can replace an edge.** Swapping SQLite for Postgres, or REST for a queue consumer, touches one layer.
- **A bug has an address.** When output is wrong you can ask *which layer is allowed to know this?* and go there.

### The test that actually matters

Do not measure your architecture by its folder diagram. Measure it by this question:

> **Pick any file at random. Can you say, without looking, exactly which folders it is allowed to import from?**

If yes, you have an architecture. If it depends on the file, you have a folder layout.

### And a rule nobody checks is a preference

This is the part most projects skip, and it is the part that decides whether the structure survives contact with a deadline.

**Both halves of this kit enforce their dependency rule with a machine.**
The backend does it with a test that parses every import and fails the build (`tests/unit/test_architecture.py`).
The frontend does it with an architectural linter (Steiger).
Neither relies on anyone remembering.

The first time someone imports the ORM model directly into a route handler "just to save a conversion step", the boundary is gone — and it will be gone silently, because everything still works. Ten routes later it is unrecoverable. A check is what turns that from a judgement call into a red build.

---

## Part 1 — The backend: four layers, one direction

```
entities  ←  dal  ←  bll  ←  api
   ↑                          ↑
   └──────── core/ ───────────┘   (config, logging, exceptions: available to all)
```

Arrows are **"is imported by"**. Dependencies run right to left, and never left to right.

**This shape has a name — Clean Architecture — and Part 2 explains where it comes from.** Read Part 1 for what each folder does, then Part 2 for why the rule points the way it does.

If you want the one-paragraph version of the whole thing: **the things that change slowly go in the middle, the things that change fast go at the edge, and nothing in the middle is allowed to name anything at the edge.**

### `entities/` — plain domain objects

The things your product is *about*: a `User`, an `Order`, an `Invoice`.

- A dataclass, or a Pydantic model used as a domain type. Nothing more.
- **No framework imports. No ORM base class. No knowledge that a database exists.**
- This is what every other layer passes around and thinks in.

If `entities/` imports SQLAlchemy, the innermost circle now depends on the outermost one, and every benefit above is gone at once.

### `dal/` — the Data Access Layer

**The only layer in the entire codebase allowed to import the ORM.**

- It maps between the persistence representation (a SQLAlchemy mapped class) and a plain entity.
- Its functions **take entities and return entities** — never a mapped row.
- Keep the mapped class module-private: name it `_UserRow`, so nothing outside is even tempted.

This is the Repository pattern, and its purpose has a name: **persistence ignorance**. The rest of the application does not know *how* a thing is stored, only that it can be got and put.

### `bll/` — the Business Logic Layer

Every rule, every validation, every piece of orchestration across more than one `dal/` call.

- Takes entities in, returns entities out. **Never a DTO. Never an ORM type.**
- This is where *"is this allowed?"* is decided — not in the route, and not in the DAL.
- If you find yourself asking where a piece of logic goes, and the answer is "well, the route already has the data", the answer is still here.

### `api/` — the edge

Request in, response out. Nothing else.

- Convert the incoming request body (a DTO) into what the BLL needs.
- Call the BLL.
- Convert the entity the BLL returns into a response DTO.
- **No business rules.** A route that contains an `if` about your domain is a route that has stolen the BLL's job.

### DTOs live at the edge and nowhere else

A **DTO** (Data Transfer Object) is the shape of a request body or a response payload. It is your **wire contract** — the promise you make to whoever calls you.

It is deliberately allowed to differ from your entity: different field names, a subset of fields, a computed field, a flattened relationship. That freedom *is the point*. Your internal model should be free to change without breaking every client.

**A DTO must never reach the BLL or the DAL.** The moment business logic branches on a DTO's optional field, your wire format has become your domain model, and you can no longer change either one alone.

### Why `api/v1/`, and what the `v1` actually promises

The scaffold puts routes under `app/api/v1/`, with DTOs at `app/api/v1/dto/`. This is not decoration.

**A version number is a promise that a client written today keeps working tomorrow.** Once something else consumes your API — a frontend you also own, a mobile app, another team — you no longer control when callers update. Versioning gives you somewhere to put a change that would otherwise break them: `v2` appears, `v1` keeps working, clients migrate on their own schedule.

What counts as breaking, and therefore needs a new version: removing a field, renaming one, narrowing a type, making an optional field required, changing what a status code means. What does not: **adding** an optional field, adding an endpoint, adding an enum value clients are told to ignore when unknown.

**The structural reason it lives in the folder name**: because `dto/` sits *inside* `v1/`, a v2 DTO is a different file rather than an edit to a shared one. Two versions can disagree without a single `if version == 1` anywhere in your code. That is what keeps versioning from rotting into a pile of conditionals.

**Start with `v1` even alone.** It costs one folder today. Adding versioning to an API that never had it costs a migration of every caller you did not know you had.

### Exceptions: one flat file, business names, mapped in one place

- Keep exception classes in **one flat file** (`core/exceptions.py`) — not split per layer, not per feature.
- Name them for **what failed in business terms**: `InvalidCredentialsError`, `DuplicateEmailError`. Never `DalNotFoundError`. A caller should not have to know which layer broke in order to understand what went wrong.
- Map each exception to an HTTP status in **exactly one place** (`core/exception_handlers.py`). No other file decides a status code from an exception type — otherwise the same failure gets two different answers in two different routes, and nobody notices for months.
- One exception covering several causes is often *correct*: a single `InvalidCredentialsError` for both "wrong password" and "expired token" is deliberate, because a caller who can tell them apart can enumerate your auth check.

### Enforcement

Write the test before you need it:

```python
# tests/unit/test_architecture.py — walks every import in app/ and asserts direction
FORBIDDEN = {
    "entities": ("dal", "bll", "api", "sqlalchemy", "fastapi"),
    "dal":      ("bll", "api"),
    "bll":      ("api", "sqlalchemy"),
}
```

Parse each module's imports with `ast`, look up its layer from its path, fail on any hit.
It is roughly forty lines and it is the difference between an architecture and an intention.

The full reasoning behind this layering, including the tradeoff of sharing a DAL across two services, is `project-docs/learnings/03-backend-layered-architecture-template.md`. The *how* — the folders, the boilerplate, the commands — is the `scaffold-backend-service` skill.

---

## Part 2 — What this is called: Clean Architecture

**The structure in Part 1 has a name, and the name is Clean Architecture.**
Use it. It is what you should write in `SOLUTION_DESIGN.md`, what you should say in a review, and what you should search for when you want to read more.

### One idea, four names, twenty years

The same architecture was arrived at independently several times, and each arrival gave it a different name. They are not competing approaches, and you do not have to choose between them:

| Year | Name | Who | What it added |
|---|---|---|---|
| 2005 | **Hexagonal Architecture**, later **Ports & Adapters** | Alistair Cockburn | the insight that the UI and the database are the same kind of thing — both outside |
| 2008 | **Onion Architecture** | Jeffrey Palermo | the concentric picture, and the argument from *churn*: data-access technology changes every few years, so it must not be at the centre |
| 2012 | **Clean Architecture** | Robert C. Martin | the consolidation, and the Dependency Rule as a single quotable sentence |

Palermo's framing is the one worth carrying, because it explains *why* the rule points the way it does: **put the things that change slowly at the centre, and the things that change fast at the edge.** Your business rules outlive your database, your web framework and probably your language. Structure the code so that is possible.

That is also why `entities/` sits innermost. Not because it is important in some abstract sense — because it is the part you least want to rewrite when everything around it is replaced.

### The one thing that makes it work, and that a diagram cannot show

**Dependency inversion.** It is the mechanism, and it is the part most people miss when they copy the folder diagram.

Here is the problem it solves. At **runtime**, control flows *outward*: the BLL needs a user, so the DAL runs a query, so the database driver opens a socket. That is unavoidable — the business logic really does need the database.

But if the BLL *imports* the DAL to do that, the dependency points outward and the rule is broken. So you split the two apart:

- The **inner** layer declares what it needs, as an interface it owns: `UserRepository`, with a `find_by_email` that takes and returns entities.
- The **outer** layer implements it: `DalUser` satisfies that interface using SQLAlchemy.
- Something at the very edge — the **composition root**, usually where your app starts up — hands the concrete one in.

The BLL now names an interface it owns and never names SQLAlchemy. Control still flows outward at runtime; the source dependency points inward. **Compile-time dependency and runtime call direction are different things, and inverting one without the other is the whole trick.**

In Python this is lighter than it sounds: the interface can be a `Protocol`, or in a small project simply a constructor parameter that is type-hinted and passed in at startup. What matters is that the BLL does not `import` from `dal/`, and that a test can hand it a fake.

**The test that tells you whether you actually did it:** can you unit-test `bll/` with no database running? If yes, you inverted the dependency. If you had to spin up SQLite to test a business rule, you drew the diagram but did not build the architecture.

### The anemic-model objection, and what to do about it

One criticism is worth facing head-on, because it is fair.

Your `entities/` are dataclasses — data with no behaviour — and all the logic lives in `bll/`. Martin Fowler named this the **anemic domain model** and considers it an anti-pattern:

> There is hardly any behavior on these objects, making them little more than bags of getters and setters.

And the charge that stings:

> They incur all of the costs of a domain model, without yielding any of the benefits.

**Two honest responses. Know which one you are giving.**

1. **For most applications this trade is fine, and you should take it knowingly.** If your rules are mostly validation, authorization and orchestration across several stored things, they genuinely do not belong on one object, and a rich model buys ceremony rather than clarity. This is the common case, and choosing it deliberately is not the same as drifting into it.

2. **Where behaviour clearly belongs to one entity, put it on the entity.** Nothing in this architecture forbids it — a method that uses only the object's own fields imports nothing and breaks no rule. `order.total()`, `invoice.is_overdue()`, `booking.overlaps(other)` belong on the object. Moving those into a service is how a model becomes anemic: not by design, but one convenience at a time.

**The rule of thumb: if the logic needs only this object's own data, it goes on the object. If it needs the database, another entity, or the outside world, it goes in `bll/`.**

### A note on Domain-Driven Design, so you do not confuse the two

You will meet DDD in almost everything written about Clean Architecture, so it is worth one short section to keep the two apart.

**This is not Domain-Driven Design, and you should not call it that.**

DDD is a different discipline, about *how you arrive at a model* through conversation with domain experts. Its centre of gravity is strategic — bounded contexts, subdomains, context mapping — and none of that is here. What this architecture shares with DDD is two of its smaller tactical patterns: the **repository** (your `dal/`) and **persistence ignorance** (your `entities/`). Sharing two patterns with a discipline does not make you a practitioner of it.

Evans himself has said he **over-emphasized those tactical building blocks**, and that the strategic half is the part that matters and the part people skip. So a codebase that adopts repositories and calls itself DDD has adopted precisely the half its author thinks is over-weighted. Say "Clean Architecture", which is accurate, and leave DDD to mean what it means.

**Reach for real DDD when the business rules are the hard part** — insurance, logistics, finance, healthcare billing — when domain experts argue about what a word means and different parts of the business need different models of the same noun. For a CRUD application with a permissions model, it produces DDD-shaped folders with none of DDD's benefits.

**One DDD idea is worth stealing regardless, and you already have it.** `GLOSSARY.md` — the rule that the words domain experts use, the words in your conversations and the identifiers in your source code must be **one vocabulary** — is DDD's *Ubiquitous Language*, and it is arguably the most valuable idea in the book. The kit enforces it structurally: the glossary is written before the code, every story's terms must resolve to an entry, and `check-project-docs` greps for words you have retired. Keep doing that. It costs almost nothing and it is where DDD's real leverage was all along.

---

## Part 3 — The frontend: Feature-Sliced Design

The frontend uses **Feature-Sliced Design (FSD)**: an explicit, externally documented methodology with its own specification, linter and vocabulary.

### The layers

```
src/
  app/        providers, router, global styles, entry point
  pages/      one slice per route — composes widgets and features
  widgets/    self-contained composite blocks (a header, a sidebar, a feed)
  features/   things a user *does* — an action with its UI and its logic
  entities/   business nouns — the user, the order, the comment
  shared/     ui/ api/ lib/ config/ — reusable, business-agnostic
```

You do not have to use all six. **Their names are fixed, though** — that is what makes the structure legible to anyone who knows FSD. A small app may begin with only `app/`, `pages/`, `entities/` and `shared/`, and grow `features/` and `widgets/` when it needs them.

### Slices and segments

Inside every layer except `app/` and `shared/`, code is divided into **slices** named for the business domain — `entities/user/`, `features/add-to-cart/`.

Inside every slice, code is divided into **segments** named for technical purpose:

| Segment | Holds |
|---|---|
| `ui/` | components, styling, anything visual |
| `api/` | requests to the backend, and the types of what comes back |
| `model/` | state stores, schemas, business logic |
| `lib/` | helpers this slice needs |
| `config/` | constants, feature flags |

### The import rule, and the public API

Two rules do the real work.

**1. A module may only import from layers strictly below it.** `pages/` may use `features/`; `features/` may never use `pages/`. Cycles become structurally impossible.

**2. A slice may not import a sibling slice on its own layer.** `features/add-to-cart/` may not reach into `features/checkout/`. If two features need the same thing, that thing belongs one layer down — usually in `entities/` or `shared/`.

Each slice exposes a **public API** through an `index.ts` at its root, and that is the only legal entrypoint. Reaching past it into `features/checkout/ui/Button.tsx` is a violation even from a layer that is otherwise allowed to import it. The public API is what lets you reorganise a slice's insides without touching anything else.

### Enforcement

```bash
npm i -D steiger @feature-sliced/steiger-plugin
```

Configure `steiger.config.ts` and run it in CI. The rules that matter: `fsd/forbidden-imports` (upward imports and cross-slice imports), `fsd/no-public-api-sidestep` (reaching past an `index.ts`), `fsd/no-layer-public-api`.

This is the frontend's answer to `test_architecture.py`. Same job, different machine.

### How this differs from the backend, stated plainly

**The two halves of this kit do not use the same structuring principle, and you should know that rather than discover it.**

| | backend | frontend (FSD) |
|---|---|---|
| Rule | one-way imports | one-way imports |
| Direction | **inward**, toward `entities/` — the most abstract, most stable code | **downward**, toward `shared/` — the most reusable, least business-specific code |
| Organised by | technical layer | business slice, *then* technical segment |
| Dependency inversion | yes — the point of the rule | **no**, by design; direct downward imports are allowed |
| Enforced by | a pytest test | a linter (Steiger) |

The directions are genuinely opposite: the backend points at business policy, FSD points at generic utilities. FSD has been described as two development flows pointing at each other — the backend built bottom-up from the domain, the frontend built top-down from the page.

**Why that is acceptable.** The two halves have different pressures. A backend's hard part is business rules that must stay correct while infrastructure changes around them, and the Dependency Rule protects exactly that. A frontend's hard part is that features multiply, teams work in parallel, and *"where does this file go"* is asked twenty times a day. FSD answers that question directly, which the Dependency Rule does not.

**What the two do share, and it is the thing worth learning:** every file has a declared set of folders it may import from, that set is written down, and a machine checks it. That is the transferable idea. The layer names are the local dialect.

### The stack, and where each piece lives

| Concern | Choice | Lives in |
|---|---|---|
| Routing | React Router | `app/` |
| Server state | TanStack Query | the `api/` segment of a slice; query hooks beside the requests they wrap |
| Client state | Zustand | the `model/` segment of the slice that owns it |
| Local UI state | `useState` | inside the component |
| Config / providers | React Context | `app/` |

**Server state and client state are different things and the distinction is the whole reason there are two libraries.**
Data that lives on the server and is *cached* in the browser — a list, a record, anything fetched — is TanStack Query's job: loading, errors, retries, invalidation and refetching are all one concern and they are solved. Data that only ever exists in the browser — a filter panel's open state, a multi-step form in progress, a selected item — is Zustand's.

The most common beginner mistake is putting server data in a global store and hand-writing the cache invalidation. The second most common is reaching for a global store for something one component owns. Use `useState` until two unrelated components need the same value.

**Context is for configuration, not for state that changes often.** Every consumer re-renders on every change, so a theme or a current user is fine and a live-updating value is not.

### TypeScript

The frontend is TypeScript, and the reason is the boundary.

The `api/` segment is where server DTOs exist. With types, "a DTO must not reach the UI" stops being a convention and becomes a compile error: declare the wire type in `api/`, map it to your own type at the boundary, and never export the wire type. That is a stronger guarantee than any linter path rule — and it is the same guarantee the backend gets from `entities/` having no ORM import.

Name the two shapes differently and never let them merge: `UserDto` for what the server sent, `User` for what your application thinks in.

### What `scaffold-frontend-app` lays down

The skill is at `.claude/skills/scaffold-frontend-app/`, and this is its job:

1. `npm create vite@latest -- --template react-ts`, then Tailwind.
2. Create `src/{app,pages,widgets,features,entities,shared}`, with `shared/{ui,api,lib,config}` and an `index.ts` in each slice it creates.
3. Install React Router, TanStack Query, Zustand; wire the router and the `QueryClientProvider` in `app/`.
4. Install and configure `steiger` + `@feature-sliced/steiger-plugin`, and **prove it fails on a deliberate upward import** before declaring success — a linter nobody has seen go red is a claim, not a guarantee.
5. Set up Vitest + Testing Library, with tests split `pure/` (no DOM, and a test importing React fails) and `rendered/`.
6. Create **no** feature, entity or widget — those are story work, exactly as the backend scaffold creates no `dal_*.py`. It does not even create those three folders empty: Steiger reports on empty and insignificant slices, so pre-creating them hands you a red linter on a project where you have written nothing. **A layer is created by the first story that needs it.**
7. Verify it boots, then report.

**Same hard precondition as the backend scaffold**: nothing is scaffolded before scope is agreed and the documents exist.

---

## Part 4 — Naming conventions

State these the moment a language enters your project, and extend them the first time a real mistake is caught — not before.

### Python

| Kind | Convention | Example |
|---|---|---|
| Module | `snake_case`, prefixed with its layer | `dal_user.py`, `bll_billing.py`, `ent_invoice.py` |
| Class | `PascalCase`, carrying the same prefix | `DalUser`, `BllBilling`, `EntInvoice` |
| Private ORM row | leading underscore | `_UserRow` |
| Function, variable | `snake_case` | `find_by_email` |
| Constant | `UPPER_SNAKE_CASE` | `MAX_RETRIES` |
| Boolean | prefixed `is_` / `has_` / `can_` | `is_active`, `has_paid` |
| Package folder | lowercase, no underscores | `entities/`, `dal/`, `bll/` |

**The layer prefix is worth the ugliness.** `dal_user.py` next to `bll_user.py` tells you which is which in a file tab, a stack trace, a search result and a code review — every place a bare `user.py` would not. The cost is real and the payoff is bigger.

**One hard rule that comes with it:** a layer prefix must never appear in anything a user reads on a screen. It is an internal navigation aid, not vocabulary.

### TypeScript / React

| Kind | Convention | Example |
|---|---|---|
| Component file | `PascalCase.tsx`, named for its single export | `UserCard.tsx` |
| Hook | `camelCase.ts`, prefixed `use` | `useCurrentUser.ts` |
| Pure module | `camelCase.ts` | `formatDate.ts` |
| Type / interface | `PascalCase`, no `I` prefix | `User`, not `IUser` |
| Wire type | `PascalCase` + `Dto` | `UserDto` |
| Folder (slice, segment) | `kebab-case` | `features/add-to-cart/` |
| Constant | `UPPER_SNAKE_CASE` | `PAGE_SIZE` |
| Boolean | `is` / `has` / `can` / `should` | `isLoading`, `canEdit` |
| Event handler | `handleX` where defined, `onX` as a prop | `onSubmit={handleSubmit}` |
| Public API | `index.ts` at each slice root | `features/add-to-cart/index.ts` |

One component per file, named the same as its file. A file exporting three components is three files that have not been separated yet.

### Timestamps, everywhere

**Store and transmit UTC. Always.** ISO-8601 with `Z`. Convert to local time in the UI and nowhere else.
This is worth stating on day one because the cost of getting it wrong is not a bug you fix — it is stored data that is now ambiguous.

### Documents and folders

- `SCREAMING_SNAKE.md` for the canonical documents there is exactly one of: `PRD.md`, `PLAN.md`, `GLOSSARY.md`.
- `hyphenated-lowercase.md` for everything you have many of, and for every folder.
- **Folders whose files are a history number them `NN-name.md`** — `reviews/`, `learnings/`. The number is the order the file was written, **assigned once and never reassigned**, because a citation in an old commit has to keep resolving.
- Every markdown file opens with `created` and `updated` in YAML frontmatter, UTC, and `updated` is stamped by `.githooks/pre-commit` rather than maintained by hand.

### Extending this section

Add a line here **the first time a real naming mistake is caught** — a component named inconsistently, a timestamp stored local, a boolean without a prefix.
Do not invent rules ahead of code that would need them. A convention list written speculatively is a list nobody believes.

---

## Part 5 — The recommended stack

This is what the kit's scaffolds produce. **It is a starting point, not a requirement.**

### Backend

| Part | Choice | Why this specifically |
|---|---|---|
| Language | **Python 3.12+** | typing that is now genuinely good, and the largest library surface for whatever your domain needs |
| Framework | **FastAPI** | native async, automatic OpenAPI docs from your DTOs, and Pydantic validation at the edge where it belongs |
| ORM | **SQLAlchemy 2.x**, typed declarative | real columns and real relationships, so your schema is a schema rather than a JSON blob |
| Migrations | **Alembic** | the schema will change; the only question is whether the change is recorded |
| Database | **SQLite** to start, **PostgreSQL** when you need concurrent writers | SQLite is zero setup and one file; the DAL is what makes the swap cheap |
| Dependencies | **`uv`** | one lockfile, fast enough to run on every start, installs your package editable so imports work everywhere |
| Validation | **Pydantic v2** | DTOs that validate themselves at the edge |
| Tests | **pytest** | with `pytest-asyncio` in auto mode |

### Frontend

| Part | Choice | Why this specifically |
|---|---|---|
| Language | **TypeScript** | it is what makes the DTO boundary enforceable rather than aspirational |
| Framework | **React 19** | the largest ecosystem, and FSD's documentation and tooling assume it |
| Build | **Vite** | instant dev server, and the thing every current guide assumes |
| Styling | **Tailwind CSS 4** | a token vocabulary instead of a component library you will fight |
| Routing | **React Router** | the default; file-based routing is a framework decision, not a library one |
| Server state | **TanStack Query** | caching, retries and invalidation are one solved problem, and hand-rolling them is the most repeated frontend mistake |
| Client state | **Zustand** | small, unopinionated, no provider ceremony. Redux Toolkit only for a large team with a large app |
| Tests | **Vitest + Testing Library + jsdom** | same config as Vite, no second build pipeline |
| Architecture lint | **Steiger** | the rule, checked |

### What swapping costs

- **A different database** — nearly free, if `dal/` is honest. This is the layering paying for itself.
- **A different Python framework** — a rewrite of `api/`, nothing else. Also the layering paying for itself.
- **A different frontend framework** — FSD is framework-agnostic; the layers and the rule survive. The components do not.
- **Dropping TypeScript** — the `api/` boundary becomes convention again, enforced only by the linter and by you.
- **Dropping the architecture checks** — free today, and you will not be able to tell when it stops being free. That is the one on this list not to take.

---

## Part 6 — Where this sits in your path

```
1. Copy the kit into your empty project            (README.md § Install)
2. Run the starter prompt                          STARTER_PROMPT.md
       ↓  fills, one section at a time, with your answers:
   PRD → NFR → SOLUTION_DESIGN → PLAN → GLOSSARY → PROJECT_WORKFLOW
3. Write AGENTS.md / CLAUDE.md                     (derived, last)
4. Plan the first Epic and its stories             skills: epic, user-story
5. Scaffold the backend                            skill: scaffold-backend-service
6. Scaffold the frontend                           skill: scaffold-frontend-app
7. Build, one story at a time
```

**Steps 5 and 6 come after step 2, and that ordering is the kit's central claim.**
Scaffolding first means choosing your layers before you know your domain, and the layer you get wrong is the one you will not notice for a month.

Read `project-docs/learnings/03-backend-layered-architecture-template.md` for the long reasoning behind Part 1, and `project-docs/learnings/01-documentation-structure-template.md` for why the documents are ordered the way they are.

---

## Part 7 — Where to read more

**Everything below was opened and checked.** Start at the top of each list; they are ordered, not alphabetical.

### Clean Architecture — start here

**1. [The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)** — Robert C. Martin, ~10 min.
The original post, and still the shortest complete statement. If you read one thing, read this. It is where the Dependency Rule sentence in Part 0 comes from, and where the concentric-circles diagram everyone redraws was first drawn.

**2. [Common web application architectures](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures)** — Microsoft Learn, ~20 min.
**The best free explanation with real diagrams**, and the one that will make Part 1 click. Read *"What are layers"*, *"Traditional N-Layer architecture"* and *"Clean architecture"*, and stop at *"Monolithic applications and containers"* — the rest is Azure and Docker you do not need.

It is written in C#, and that does not matter: the section that teaches the most is the one explaining why traditional N-Layer puts your business logic on top of your database, and how inverting one dependency fixes it. That argument is language-independent, and their `UI / BLL / DAL` is exactly your `api / bll / dal`.

**3. [The Onion Architecture](https://jeffreypalermo.com/2008/07/the-onion-architecture-part-1/)** — Jeffrey Palermo, ~8 min.
Read this for the *reason*, which Part 2 borrows: data-access technology changes every few years, so it must not be the thing everything else is built on. Short, and the argument is the clearest of the three.

**4. [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/)** — Alistair Cockburn, ~15 min.
The oldest of the four names and the most quotable. Worth reading once for one idea: *"the asymmetry to exploit is not that between left and right sides of the application but between inside and outside."* Once the UI and the database look like the same kind of thing to you, the rest of this document is obvious.

### When you want to go deeper

**[Anemic Domain Model](https://martinfowler.com/bliki/AnemicDomainModel.html)** — Martin Fowler, ~6 min.
The objection Part 2 answers. Read it so you can decide deliberately, rather than being told later that you built an anti-pattern.

**[Explicit Architecture: how I put it all together](https://herbertograca.com/2017/11/16/explicit-architecture-01-ddd-hexagonal-onion-clean-cqrs-how-i-put-it-all-together/)** — Herberto Graça, ~17 min. **Advanced.**
The single best piece on how Hexagonal, Onion and Clean relate to one another. **A caution, since it is exactly the confusion Part 2 warns about**: it folds DDD and CQRS in alongside them, which is legitimate for its purpose and is *not* what you are building. Read it for the relationships between the architecture styles; treat the DDD and CQRS material as further reading about something else.

*Books, if you want them: Martin's* Clean Architecture *(2017) is the long version of link 1. Evans'* Domain-Driven Design *(2003) is a different subject — read it when your domain is genuinely hard, not to understand this layout.*

### Feature-Sliced Design — the frontend

**1. [Overview](https://feature-sliced.design/docs/get-started/overview)** — ~10 min. Layers, slices, segments and the import rule. The whole methodology in one page.

**2. [Tutorial](https://feature-sliced.design/docs/get-started/tutorial)** — a hands-on walkthrough building a Medium clone, in two halves: decide the structure *on paper* first, then write it. Assumes React and TypeScript. **The on-paper half is the valuable one** — deciding which layer something belongs to before writing it is the actual skill.

**3. [Public API](https://feature-sliced.design/docs/reference/public-api)** — ~5 min. The `index.ts` convention, and why reaching past it is a violation even from a layer allowed to import you.

**4. [Steiger](https://github.com/feature-sliced/steiger)** — the linter. Install it on day one, not after the structure has already drifted.

### Alternatives worth knowing exist

**[Bulletproof React](https://github.com/alan2207/bulletproof-react/blob/master/docs/project-structure.md)** — the main feature-based alternative to FSD: fewer concepts, less ceremony, a looser rule. Read its ESLint `import/no-restricted-paths` section even if you use FSD — it is the clearest short example of enforcing a boundary in JavaScript tooling.

### The stack's own documentation

[FastAPI](https://fastapi.tiangolo.com/tutorial/bigger-applications/) (*Bigger Applications* is the routing structure you want) · [SQLAlchemy 2.0 ORM](https://docs.sqlalchemy.org/en/20/orm/quickstart.html) · [Alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html) · [uv](https://docs.astral.sh/uv/) · [Pydantic](https://docs.pydantic.dev/latest/) · [Vite](https://vite.dev/guide/) · [TanStack Query](https://tanstack.com/query/latest/docs/framework/react/overview) · [Zustand](https://zustand.docs.pmnd.rs/) · [React Router](https://reactrouter.com/) · [Tailwind](https://tailwindcss.com/docs) · [Vitest](https://vitest.dev/) · [Testing Library](https://testing-library.com/docs/react-testing-library/intro/)

---

*If a link above is dead by the time you read this, the search terms that will find its replacement are: "clean architecture dependency rule", "onion architecture Palermo", "hexagonal architecture ports adapters", "feature-sliced design layers".*
