---
created: 2026-09-26T13:09:00Z
updated: 2026-11-06T18:36:28Z
---

# EPIC_EXECUTION.md — FDS Portail

**Répond à :** Quel est l'état de chaque story, en ce moment ?
**Dépend de :** `PLAN.md` pour les noms d'Epics.

> Cette table est la source de vérité du statut en temps réel. Mise à jour à chaque changement de statut d'une story — pas à la fin d'un Epic.

## Où en est le projet (2026-11-06)

- **En production** sur https://dorfilus.ueh.edu.ht (VM Proxmox de la FDS, déploiement continu : US-026). 26 stories sur 28 sont livrées. Epics 1, 2 et 3 clôturés.
- **`US-016` — Notifications SMS : construite en simulation** (comme le paiement, faute de fournisseur SMS), en attente de validation par le Project Owner. Tout le périmètre contractuel (Must, Should, Could) est livré.
- **Prochaine story à construire : `US-027` — sauvegardes hors site** (Epic 5) : hors contrat, mais aucune copie de la base ni des pièces n'existe hors de la VM (`NFR.md`, Récupération après sinistre).
- **Ajoutée le 2026-11-05 à la demande du Project Owner : `US-028` — calendrier d'admission réglable par l'administration** (Epic 4) : fusionnée, déployée (PR #60, #63) et validée par le Project Owner le 2026-11-06.
- **Epics 2 et 3 clôturés le 2026-11-06** (closeouts, specs WS-02 à WS-05). Issues et Milestones GitHub fermés le 2026-11-06.
- **Emails** : en production, réception confirmée le 2026-11-06 (`reviews/03`, F2).

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
**Status :** ✅ Done — closed 2026-11-06, voir [epic-002-closeout.md](epic-002-candidature/epic-002-closeout.md)

Règle d'admission (2026-10-31) : l'admission est unique (Premier cycle MPC), sans choix de cursus ; liste unique de 5 pièces — voir [epic-002-refinement.md](epic-002-candidature/epic-002-refinement.md) (E2-6, E2-7, R5, R6) et ADR-008.

Walking Skeleton complet côté candidat : formulaire multi-étapes, question `deplacement_physique`, simulation de paiement MonCash/NatCash, téléversement sécurisé des pièces, attribution de la référence `CAN-2026-XXXX`, email de confirmation, page de suivi du dossier et remplacement d'un document rejeté.

| Story | Titre | Statut | Spec |
|---|---|---|---|
| US-005 | Formulaire d'inscription & question `deplacement_physique` | ✅ Done | [US-005.md](epic-002-candidature/US-005.md) |
| US-006 | Simulation de paiement MonCash / NatCash | ✅ Done | [US-006.md](epic-002-candidature/US-006.md) |
| US-007 | Téléversement sécurisé des pièces requises | ✅ Done | [US-007.md](epic-002-candidature/US-007.md) |
| US-008 | Finalisation de candidature & notification de confirmation | ✅ Done | [US-008.md](epic-002-candidature/US-008.md) |
| US-009 | Consultation et suivi de dossier par référence | ✅ Done | [US-009.md](epic-002-candidature/US-009.md) |
| US-010 | Remplacement d'un document rejeté depuis la page de suivi | ✅ Done | [US-010.md](epic-002-candidature/US-010.md) |
| US-018 | Aligner le portail public sur l'admission unique au MPC | ✅ Done | [US-018.md](epic-002-candidature/US-018.md) |

---

## Epic 3 — Administration & Audit

**Workstream :** WS-04 Administration
**Status :** ✅ Done — closed 2026-11-06, voir [epic-003-closeout.md](epic-003-administration/epic-003-closeout.md)

Interface d'administration sécurisée : authentification JWT + RBAC, tableau de bord des candidatures, validation/rejet de documents avec traçabilité complète (`valide_par`, `date_validation`), et notifications email déclenchées par les décisions admin.

| Story | Titre | Statut | Spec |
|---|---|---|---|
| US-011 | Authentification de l'administrateur (JWT + RBAC) | ✅ Done | [US-011.md](epic-003-administration/US-011.md) |
| US-012 | Dashboard admin — liste et consultation des candidatures | ✅ Done | [US-012.md](epic-003-administration/US-012.md) |
| US-013 | Validation ou rejet d'un document avec audit | ✅ Done | [US-013.md](epic-003-administration/US-013.md) |
| US-014 | Notification email déclenchée par une décision admin | ✅ Done | [US-014.md](epic-003-administration/US-014.md) |

---

## Epic 4 — Could Have & Should Have

**Workstream :** WS-05 Notifications, WS-04 Admin (exports)
**Status :** 🟡 In progress — reste `US-016` (SMS, Should Have) — [refinement](epic-004-could-have/epic-004-refinement.md)

Fonctionnalités de confort et d'efficacité opérationnelle : SMS en complément des emails, export CSV/PDF des dossiers pour commissions hors ligne, et mode sombre.

| Story | Titre | MoSCoW | Statut | Spec |
|---|---|---|---|---|
| US-015 | Export CSV/PDF filtré des dossiers validés | 🔵 Could | ✅ Done | [US-015.md](epic-004-could-have/US-015.md) |
| US-016 | Notifications SMS en complément de l'email (simulées) | 🟡 Should | 🔲 Backlog | [US-016.md](epic-004-could-have/US-016.md) |
| US-017 | Mode sombre interface admin et formulaire candidat | 🔵 Could | ✅ Done | [US-017.md](epic-004-could-have/US-017.md) |
| US-019 | Pages Histoire et Contact | 🟡 Should | ✅ Done | [US-019.md](epic-004-could-have/US-019.md) |
| US-020 | Interface en Kreyòl (sélecteur FR / KR) | 🟡 Should | ✅ Done | [US-020.md](epic-004-could-have/US-020.md) |
| US-021 | Refonte visuelle de l'accueil et des fiches de cursus | 🔵 Could | ✅ Done | [US-021.md](epic-004-could-have/US-021.md) |
| US-022 | Finition de la refonte visuelle (menu mobile, accueil et fiche MPC sur ordinateur, suivi) | 🔵 Could | ✅ Done | [US-022.md](epic-004-could-have/US-022.md) |
| US-028 | Calendrier d'admission réglable par l'administration | 🟡 Should | ✅ Done | [US-028.md](epic-004-could-have/US-028.md) |
| US-029 | Gestion des accès du personnel depuis l'espace admin | 🔵 Could | 🔲 Backlog | [US-029.md](epic-004-could-have/US-029.md) |

---

## Epic 5 — Mise en production

**Workstream :** transverse (déploiement, CI/CD, exploitation)
**Status :** 🟡 In progress — reste `US-027` (sauvegardes) — [refinement](epic-005-mise-en-production/epic-005-refinement.md)

Mise en ligne du portail sur la VM Proxmox de la FDS (Docker Compose, HTTPS assuré par l'Apache de l'UEH) : migrations versionnées, adresse réelle du visiteur derrière les proxys, CI frontend, déploiement continu par images GHCR, sauvegardes hors site avec restauration testée. Ordre de build : US-023 → US-024 → US-025 → US-026 → US-027.

| Story | Titre | Statut | Spec |
|---|---|---|---|
| US-023 | Migrations de base de données avec Alembic | ✅ Done | [US-023.md](epic-005-mise-en-production/US-023.md) |
| US-024 | Adresse réelle du visiteur derrière les proxys | ✅ Done | [US-024.md](epic-005-mise-en-production/US-024.md) |
| US-025 | Vérifications du frontend en CI | ✅ Done | [US-025.md](epic-005-mise-en-production/US-025.md) |
| US-026 | Déploiement continu vers la VM de la FDS | ✅ Done | [US-026.md](epic-005-mise-en-production/US-026.md) |
| US-027 | Sauvegardes hors site et procédure d'exploitation | 🔲 Backlog | [US-027.md](epic-005-mise-en-production/US-027.md) |

---

*EPIC_EXECUTION.md — FDS Portail — Bravetech · GL-EN3-2026*
