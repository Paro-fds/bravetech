---
created: 2026-09-26T13:09:00Z
updated: 2026-09-29T18:00:00Z
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

## Epic 2 — Candidature & Suivi (côté candidat)

**Workstream :** WS-02 Candidature, WS-03 Suivi de dossier
**Status :** 🟡 In progress — [refinement](epic-002-candidature/epic-002-refinement.md)

Walking Skeleton complet côté candidat : formulaire multi-étapes, question `deplacement_physique`, simulation de paiement MonCash/NatCash, téléversement sécurisé des pièces, attribution de la référence `CAN-2026-XXXX`, email de confirmation, page de suivi du dossier et remplacement d'un document rejeté.

| Story | Titre | Statut | Spec |
|---|---|---|---|
| US-005 | Formulaire d'inscription & question `deplacement_physique` | 🔲 Backlog | [US-005.md](epic-002-candidature/US-005.md) |
| US-006 | Simulation de paiement MonCash / NatCash | 🔲 Backlog | [US-006.md](epic-002-candidature/US-006.md) |
| US-007 | Téléversement sécurisé des pièces requises | 🔲 Backlog | [US-007.md](epic-002-candidature/US-007.md) |
| US-008 | Finalisation de candidature & notification de confirmation | 🔲 Backlog | [US-008.md](epic-002-candidature/US-008.md) |
| US-009 | Consultation et suivi de dossier par référence | 🔲 Backlog | [US-009.md](epic-002-candidature/US-009.md) |
| US-010 | Remplacement d'un document rejeté depuis la page de suivi | 🔲 Backlog | [US-010.md](epic-002-candidature/US-010.md) |

---

## Epic 3 — Administration & Audit

**Workstream :** WS-04 Administration
**Status :** ⏳ Not started — [refinement](epic-003-administration/epic-003-refinement.md)

*(Démarrera une fois epic-002 ✅ Done)*

Interface d'administration sécurisée : authentification JWT + RBAC, tableau de bord des candidatures, validation/rejet de documents avec traçabilité complète (`valide_par`, `date_validation`), et notifications email déclenchées par les décisions admin.

| Story | Titre | Statut | Spec |
|---|---|---|---|
| US-011 | Authentification de l'administrateur (JWT + RBAC) | 🔲 Backlog | [US-011.md](epic-003-administration/US-011.md) |
| US-012 | Dashboard admin — liste et consultation des candidatures | 🔲 Backlog | [US-012.md](epic-003-administration/US-012.md) |
| US-013 | Validation ou rejet d'un document avec audit | 🔲 Backlog | [US-013.md](epic-003-administration/US-013.md) |
| US-014 | Notification email déclenchée par une décision admin | 🔲 Backlog | [US-014.md](epic-003-administration/US-014.md) |

---

## Epic 4 — Could Have & Should Have

**Workstream :** WS-05 Notifications, WS-04 Admin (exports)
**Status :** ⏳ Not started — [refinement](epic-004-could-have/epic-004-refinement.md)

*(Démarrera une fois epic-003 ✅ Done)*

Fonctionnalités de confort et d'efficacité opérationnelle : SMS en complément des emails, export CSV/PDF des dossiers pour commissions hors ligne, et mode sombre.

| Story | Titre | MoSCoW | Statut | Spec |
|---|---|---|---|---|
| US-015 | Export CSV/PDF filtré des dossiers validés | 🔵 Could | 🔲 Backlog | [US-015.md](epic-004-could-have/US-015.md) |
| US-016 | Notifications SMS en complément de l'email | 🟡 Should | 🔲 Backlog | [US-016.md](epic-004-could-have/US-016.md) |
| US-017 | Mode sombre interface admin et formulaire candidat | 🔵 Could | 🔲 Backlog | [US-017.md](epic-004-could-have/US-017.md) |

---

*EPIC_EXECUTION.md — FDS Portail — Bravetech · GL-EN3-2026*
