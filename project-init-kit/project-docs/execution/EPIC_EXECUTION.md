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
**Status :** ✅ Done — closed 2026-09-26, voir [epic-001-closeout.md](epic-001-socle/epic-001-closeout.md)

Socle technique complet établi (Clean Architecture, CI GitHub Actions avec tests d'architecture, déploiement Docker Compose sur VM Linux Proxmox, catalogue officiel des cursus FDS en base de données PostgreSQL). Spécifications consolidées dans `functional-specs/ws-func-01-portail-public.md` et `technical-specs/ws-tech-01-portail-public.md`.

| Story | Titre | Statut | Spec |
|---|---|---|---|
| US-001 | Consulter la liste des cursus depuis l'accueil | ✅ Done | [US-001.md](epic-001-socle/US-001.md) |
| US-002 | Voir la fiche détaillée d'un cursus | ✅ Done | [US-002.md](epic-001-socle/US-002.md) |
| US-003 | Tests d'architecture en CI avant tout merge | ✅ Done | [US-003.md](epic-001-socle/US-003.md) |
| US-004 | Déploiement en environnement accessible | ✅ Done | [US-004.md](epic-001-socle/US-004.md) |

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
