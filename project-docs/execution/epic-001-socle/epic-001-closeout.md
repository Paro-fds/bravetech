---
created: 2026-09-30T16:04:08Z
updated: 2026-09-30T16:04:08Z
---

# Epic 001 Closeout — Socle & Portail public

**Workstream :** WS-01 Portail public  
**Status :** ✅ Done — closed 2026-09-26  
**Goal :** Le portail est en ligne, les cursus sont visibles, et l'infrastructure de développement et de déploiement est opérationnelle.

Frozen record of what this Epic delivered. Full story-by-story detail lives
in project-docs/execution/EPIC_EXECUTION.md and each story's own spec file — not duplicated
here. Behavior and implementation, consolidated across all 4 stories, are
extracted into project-docs/functional-specs/ws-func-01-portail-public.md and
project-docs/technical-specs/ws-tech-01-portail-public.md.

## Stories Delivered

| Story | Titre | Spec |
|---|---|---|
| US-001 | Consulter la liste des cursus depuis l'accueil | [US-001.md](US-001.md) |
| US-002 | Voir la fiche détaillée d'un cursus | [US-002.md](US-002.md) |
| US-003 | Tests d'architecture en CI avant tout merge | [US-003.md](US-003.md) |
| US-004 | Déploiement en environnement accessible | [US-004.md](US-004.md) |

All 4 stories ✅ Done.

## Decisions & Architecture Deliberations

1. **Clean Architecture 4-layers respectée** : Couche `entities/` strictement isolée sans dépendances externes (ni FastAPI, ni SQLAlchemy). Validée par les tests d'architecture en CI (`tests/unit/test_architecture.py`).
2. **Données de référence réelles FDS** : Source de vérité dans les fichiers officiels `cursus/*.json` (Génie Civil, Génie Électromécanique, Génie Électronique, MPC, Architecture). Injection idempotente dans la table `cursus` et `documents_requis` via `cursus_loader.py`.
3. **Frontend FSD + Tailwind CSS 4** : React 19 + TypeScript + Vite 8 avec intégration `@tailwindcss/vite` et design responsive accessible (360px mobile ready).
4. **ADR-006 (Déploiement Proxmox / Docker)** : Option 2 retenue — conteneurisation Docker complète (`backend/Dockerfile`, `frontend/Dockerfile` multi-stage avec Nginx, `docker-compose.yml` multi-services avec PostgreSQL 15) pour hébergement souverain sur machine virtuelle Linux hébergée sur Proxmox à la Faculté des Sciences.

## Split to Unscheduled

None. All scheduled stories for Epic 1 were completed.

## Tracking

Milestone `Epic 1 — Socle & Portail public` closed 2026-09-26, 4/4 issues closed (#1, #2, #3, #4).

---

*epic-001-closeout.md — FDS Portail — Bravetech · GL-EN3-2026*
