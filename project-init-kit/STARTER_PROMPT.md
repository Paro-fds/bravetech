---
created: 2026-09-08T17:38:40Z
updated: 2026-09-16T20:11:50Z
---

# Prompt de démarrage — colle ceci tel quel dans ton agent

**Utilise ceci une fois que tu as copié la structure `project-init-kit/` dans ton propre projet.** Ce prompt fonctionne avec n'importe quel agent (Claude Code ou tout autre outil de codage agentique) — il ne dépend d'aucun mécanisme spécifique à un outil.

```text
Ce projet contient une structure de documentation à remplir. Chaque document
se trouve dans project-docs/, et ils sont remplis dans l'ordre suivant :

  project-docs/PRD.md
  project-docs/NFR.md
  project-docs/SOLUTION_DESIGN.md
  project-docs/PLAN.md
  project-docs/GLOSSARY.md          (finaliser en dernier, une fois que nous saurons de quoi il s'agit)
  project-docs/PROJECT_WORKFLOW.md  (dernier de tous)

Chaque section contient des questions de réflexion (entre guillemets avec ">"). Guide-moi
à travers ces documents, dans cet ordre, une section à la fois : pose-moi
les questions de cette section, attends ma réponse, et n'invente rien à ma place.
Une fois que j'ai répondu, rédige la section à partir de ma réponse et montre-la-moi
avant de passer à la suivante.

Ne touche pas encore à AGENTS.md ou CLAUDE.md, et ne crée rien dans
project-docs/execution/, functional-specs/, technical-specs/, reviews/ ou
learnings/. Ces éléments arrivent plus tard : AGENTS.md et CLAUDE.md sont des résumés
de tout ce qui précède et sont rédigés en dernier, et le reste n'est rempli qu'une fois
qu'il y a un travail réel à enregistrer.
```

**Avant de le coller**, lis `project-docs/_ARCHITECTURE_EXPLAINED.md` une fois. C'est le seul document du kit qui répond au lieu de questionner, et `SOLUTION_DESIGN.md` ira plus vite si tu sais déjà laquelle de ses recommandations tu prends.

**Une fois les six documents remplis**, rédige `AGENTS.md` et `CLAUDE.md` à partir de ces documents, puis planifie ton premier Epic (`epic`) et sa première histoire (`user-story`) — et seulement ensuite scaffold le code (`scaffold-backend-service`, puis `scaffold-frontend-app`).

**Ce qui doit se passer ensuite** : l'agent doit te poser une question à la fois, attendre ta réponse, puis rédiger — sans te livrer d'un coup les six documents déjà remplis. Si l'agent commence à rédiger tout cela sans te poser aucune question, arrête-le et colle à nouveau le prompt : c'est exactement le comportement que ce dispositif vise à empêcher.
