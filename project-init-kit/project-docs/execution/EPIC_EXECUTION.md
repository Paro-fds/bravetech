---
created: 2026-09-26T13:09:00Z
updated: 2026-09-26T13:09:00Z
---

# EPIC_EXECUTION.md — FDS Portail

**Répond à :** Quel est l'état de chaque story, en ce moment ?
**Dépend de :** `PLAN.md` pour les noms d'Epics.

> Cette table est la source de vérité du statut en temps réel. Mise à jour à chaque changement de statut d'une story — pas à la fin d'un Epic.

---

## Epic 1 — Socle & Portail public

**Workstream :** WS-01 Portail public
**Status :** 🟡 In progress

Établit le socle technique complet (CI/CD, déploiement Railway + Vercel, base de données PostgreSQL provisionnée, tests d'architecture verts) et livre la première page publique réelle avec données en base. Voir `execution/epic-001-socle/epic-001-refinement.md` pour les questions ouvertes et l'ordre de build.

| Story | Titre | Statut | Spec |
|---|---|---|---|
| US-001 | Consulter la liste des cursus depuis l'accueil | 🔲 Backlog | [US-001.md](epic-001-socle/US-001.md) |
| US-002 | Voir la fiche détaillée d'un cursus | 🔲 Backlog | [US-002.md](epic-001-socle/US-002.md) |
| US-003 | Tests d'architecture en CI avant tout merge | 🟡 In progress | [US-003.md](epic-001-socle/US-003.md) |
| US-004 | Déploiement en environnement accessible | 🔲 Backlog | [US-004.md](epic-001-socle/US-004.md) |

---

## Epic 2 — Candidature & Suivi

**Workstream :** WS-02, WS-03, WS-05
**Status :** ⏳ Not started

*(Démarrera une fois epic-001 ✅ Done)*

---

## Epic 3 — Administration & Audit

**Workstream :** WS-04, WS-05
**Status :** ⏳ Not started

*(Démarrera une fois epic-002 ✅ Done)*

---

*EPIC_EXECUTION.md — FDS Portail — Bravetech · GL-EN3-2026*
