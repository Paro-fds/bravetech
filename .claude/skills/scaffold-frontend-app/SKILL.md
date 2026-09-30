---
name: scaffold-frontend-app
description: Scaffold a new React + TypeScript + Vite frontend using Feature-Sliced Design, with Tailwind, React Router, TanStack Query, Zustand, Steiger and Vitest wired up. Use once the project's documents exist and it is time to lay down the frontend's actual folder structure. The counterpart to scaffold-backend-service.
created: 2026-09-16T20:15:00Z
updated: 2026-09-30T16:04:08Z
---

# Scaffold Frontend App Skill

## Why this exists

Read `project-docs/_ARCHITECTURE_EXPLAINED.md` **Part 3** first if the *why* behind any piece here is unclear — the layers, the import rule, the public-API convention and where each library lives are all explained there. This skill covers the *how*.

It exists so a frontend starts at the settled shape rather than at *"one `components/` folder, and we will sort it out later"* — which is the shape every frontend starts at and none of them sorts out later.

## Hard precondition — do not skip

**No source file gets created before scope is agreed.** Before running this skill:

- `project-docs/PRD.md`, `NFR.md`, `SOLUTION_DESIGN.md` and `PLAN.md` must already exist and be filled in.
- `SOLUTION_DESIGN.md` §5 must record that this stack was **chosen**, not defaulted into. `_ARCHITECTURE_EXPLAINED.md` is a proposal; a project that has not accepted it should not be scaffolded from it.

If either is missing, **stop and say so.** Scaffold nothing, and say that scope needs to be agreed first.

**One more check that is specific to this skill:** confirm the project actually needs a separate frontend application. A backend that renders its own templates does not, and a project with three static pages does not. Six layers imposed on a brochure site is worse than no structure at all.

## What this skill does *not* do

It builds **infrastructure only**: the Vite app, the layer folders, the providers, the router, the linting and the test setup.

It creates **no entity, no feature and no widget.** Those are real work, added per user story, exactly as the backend scaffold creates no `dal_*.py`. A freshly scaffolded frontend renders one nearly-empty page.

**It also does not create `entities/`, `features/` or `widgets/` as empty folders.** This is deliberate and it is the non-obvious part: Steiger reports on slices that are empty, insignificant or sidestepped, so pre-creating three empty layers hands a student a red linter on a project where they have written nothing. **A layer is created by the first story that needs it.** FSD's own guidance is that you do not have to use all the layers — only that their names are fixed when you do.

## Procedure

```
Scaffold Progress:
- [ ] Step 1: Confirm the precondition
- [ ] Step 2: Create the Vite app
- [ ] Step 3: Install the stack
- [ ] Step 4: Wire Tailwind
- [ ] Step 5: Create the FSD skeleton
- [ ] Step 6: Wire the providers and the router
- [ ] Step 7: Install Steiger, and prove it bites
- [ ] Step 8: Wire Vitest, and prove it runs
- [ ] Step 9: Verify it boots
- [ ] Step 10: Report
```

---

**Step 1 — Confirm the precondition.** See above. Stop here if anything is missing.

**Step 2 — Create the Vite app.**

```bash
npm create vite@latest <app-folder> -- --template react-ts
cd <app-folder>
npm install
```

`<app-folder>` is usually `frontend/`. Whatever it is, it is **flat at the repository root**, beside the backend — not nested inside it.

**Step 3 — Install the stack.**

```bash
npm i react-router-dom @tanstack/react-query zustand
npm i -D tailwindcss @tailwindcss/vite
npm i -D vitest jsdom @testing-library/react @testing-library/jest-dom @testing-library/user-event
npm i -D steiger @feature-sliced/steiger-plugin
```

**Do not add a library the documents did not ask for.** If `SOLUTION_DESIGN.md` says nothing about global client state, install Zustand anyway — it is in the accepted stack — but do not add a form library, a date library, a component library or an icon set on your own initiative. Those are per-story decisions.

**Step 4 — Wire Tailwind.** Two edits, and the CSS import is the one people forget.

`vite.config.ts`:

```ts
/// <reference types="vitest" />
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: './src/shared/config/test-setup.ts',
  },
})
```

`src/app/styles/index.css` — replace the whole file Vite generated:

```css
@import "tailwindcss";
```

**Tailwind 4 has no `tailwind.config.js` and no PostCSS step.** If you find yourself running `npx tailwindcss init`, you are following a guide for version 3. Delete the generated `src/App.css` and `src/index.css`.

**Step 5 — Create the FSD skeleton.** Only the layers a scaffold can honestly fill:

```
src/
  app/
    index.tsx            <- providers, composed
    router.tsx           <- route table
    styles/index.css     <- the Tailwind import
  pages/
    home/
      index.ts           <- public API: export { HomePage } from './ui/HomePage'
      ui/HomePage.tsx
  shared/
    api/index.ts         <- the HTTP client, and nothing else yet
    config/index.ts      <- env reading
    config/test-setup.ts
    lib/index.ts
    ui/index.ts
  main.tsx
```

Then **delete** `src/App.tsx`, `src/assets/` and anything else the Vite template left at `src/` root. A file at `src/` root belongs to no layer, and the first one that survives teaches everyone that the rule is optional.

**`shared/api/index.ts` is where the wire boundary lives.** One thin client, and per-resource modules added by the stories that need them. The rule from Part 3 that matters most here: **a server DTO type is declared in an `api` segment and mapped to your own type before it leaves.** Name them apart — `UserDto` and `User` — and never export the `Dto`.

**Step 6 — Wire the providers and the router.**

`src/app/index.tsx`:

```tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { RouterProvider } from 'react-router-dom'
import { router } from './router'
import './styles/index.css'

const queryClient = new QueryClient()

export function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  )
}
```

`src/app/router.tsx` holds the route table and imports from `pages/` — **the only layer that may.**

`src/main.tsx` mounts `<App />` and does nothing else.

**Step 7 — Install Steiger, and prove it bites.** This is the step that makes the architecture real, and skipping the proof is how a project ends up with a linter that was never actually enforcing anything.

`steiger.config.js` at the app root:

```js
import { defineConfig } from 'steiger'
import fsd from '@feature-sliced/steiger-plugin'

export default defineConfig([
  ...fsd.configs.recommended,
])
```

Add to `package.json` scripts: `"lint:arch": "steiger ./src"`.

Run `npx steiger ./src` — it should pass.

**Now prove it fails.** Add a deliberate upward import to a lower layer — in `src/shared/lib/index.ts`, write `import { HomePage } from '../../pages/home'`. Run it again. **It must report `fsd/forbidden-imports`.** If it passes, the linter is not wired to your source and every guarantee in Part 3 is decoration. Remove the line and confirm it goes green again.

Do not move on until you have watched it go red and then green.

**Step 8 — Wire Vitest, and prove it runs.**

`src/shared/config/test-setup.ts`:

```ts
import '@testing-library/jest-dom/vitest'
```

Add to `package.json` scripts: `"test": "vitest run"`.

**Split the tests the way the source is split**, in `tests/` beside `src/`:

- `tests/pure/` — no DOM, no React. **A test here that imports React is a bug in the test, and it is worth adding a check that fails on it.** This is where `shared/lib` and any mapping logic gets tested, and those tests run in milliseconds.
- `tests/rendered/` — anything that renders, using Testing Library.

Write **one** trivial test in each so the split exists from the first commit rather than being retrofitted, and run `npm test` to watch them pass. A test directory created empty is a test directory nobody puts the first test in.

**Step 9 — Verify it boots.** Do not assume the scaffold is correct — prove it:

1. `npm run dev`, in the background or another terminal.
2. Open the served URL. The home page renders, with Tailwind styling visibly applied — **check an actual Tailwind class has an effect**, because a missing `@import "tailwindcss"` fails silently and looks like unstyled HTML rather than an error.
3. The browser console is clean — no provider errors, no router warnings.
4. `npm run build` completes with no TypeScript errors.
5. Stop the server.

**Step 10 — Report.** Confirm every file created, that it boots, that `npm run build` is clean, **that Steiger was seen to fail on a deliberate violation and then pass**, and that `npm test` runs both test folders.

Then say what comes next: the first real story, via `user-story` Create — which is what will add the first `entities/`, `features/` or `widgets/` slice, and with it the first layer this scaffold deliberately did not create.

## The two mistakes this skill exists to prevent

**Putting a file at `src/` root.** There is always a reason for the first one. Every file after it cites the first one as precedent, and within a month the layers describe half the codebase.

**Letting a server DTO travel.** Fetch returns the server's shape; the tempting move is to pass it straight to a component. Once three components read `user.first_name` because that is what the API happens to call it, your wire format is your UI contract and the backend can no longer rename a field. Map at the boundary, in an `api` segment, every time — even when the two shapes are identical today. **Especially then**, because that is when it feels most pointless and when the coupling is cheapest to prevent.
