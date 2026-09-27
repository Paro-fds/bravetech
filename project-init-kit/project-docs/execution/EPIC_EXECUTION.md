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

**Workstream :** WS-02 Candidature, WS-03 Suivi de dossier, WS-05 Notifications
**Status :** 🟡 In progress — [refinement](epic-002-candidature/epic-002-refinement.md)

Walking Skeleton complet côté candidat : formulaire multi-étapes avec saisie des informations personnelles, réponse à la question de déplacement physique, simulation de paiement MonCash/NatCash, téléversement sécurisé des pièces jointes, attribution de la référence `CAN-2026-XXXX`, email de confirmation et page de suivi du dossier.

| Story | Titre | Statut | Spec |
|---|---|---|---|
| US-005 | Formulaire d'inscription & question `deplacement_physique` | 🔲 Backlog | [US-005.md](epic-002-candidature/US-005.md) |
| US-006 | Simulation de paiement MonCash / NatCash | 🔲 Backlog | [US-006.md](epic-002-candidature/US-006.md) |
| US-007 | Téléversement sécurisé des pièces requises | 🔲 Backlog | [US-007.md](epic-002-candidature/US-007.md) |
| US-008 | Finalisation de candidature & notification de confirmation | 🔲 Backlog | [US-008.md](epic-002-candidature/US-008.md) |
| US-009 | Consultation et suivi de dossier par référence | 🔲 Backlog | [US-009.md](epic-002-candidature/US-009.md) |

---

## Epic 3 — Administration & Audit

**Workstream :** WS-04, WS-05
**Status :** ⏳ Not started

*(Démarrera une fois epic-002 ✅ Done)*

---

*EPIC_EXECUTION.md — FDS Portail — Bravetech · GL-EN3-2026*
