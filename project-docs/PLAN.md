---
created: 2026-09-26T00:30:00Z
updated: 2026-10-28T14:18:55Z
---

# PLAN.md — FDS Portail

**Réponses :** Dans quel ordre, regroupé en quels Epics ?
**Dépend de :** `SOLUTION_DESIGN.md` (identifiants WS-01 à WS-05).

---

## Vue d'ensemble des Epics

Les Epics sont **séquentiels** — chaque Epic doit être livrable et testable avant que le suivant commence. L'équipe est < 5 personnes : le parallélisme augmente le risque d'intégration et le coût de context-switching.

| Epic | Nom | Workstreams | Bloqué par | Livrable clé |
|---|---|---|---|---|
| `epic-001-socle` | Socle & Portail public | WS-01 | — | ✅ Done — closed 2026-09-26, voir [epic-001-closeout.md](execution/epic-001-socle/epic-001-closeout.md) |
| `epic-002-candidature` | Candidature & Suivi | WS-02, WS-03, WS-05 | `epic-001` | 🟡 In progress — [suivi](execution/epic-002-candidature/epic-002-refinement.md) |
| `epic-003-administration` | Administration & Audit | WS-04, WS-05 | `epic-002` | Un admin valide/rejette des documents. Les emails de statut partent. Le candidat peut remplacer un document rejeté. |

**Pourquoi cet ordre ?**
- `epic-001` établit le socle technique (CI/CD, déploiement, base de données, auth basique) sur lequel tout repose.
- `epic-002` livre la tâche critique du MVP : permettre à un candidat de postuler sans se déplacer.
- `epic-003` ferme la boucle administrative sans laquelle les dossiers reçus restent bloqués.

**Parallélisme possible mais non recommandé :** WS-04 (admin) pourrait démarrer pendant WS-03 (suivi) car ils partagent peu de code. Le risque : contention sur le modèle de données `DocumentSoumis`. Décision : séquentiel, Epic-002 terminé avant Epic-003.

---

## Tâches à accomplir — référence

→ `PRD.md §4` — Jobs to Be Done.

Correspondance Epic ↔ JTBD :

| JTBD (PRD §4) | Epic |
|---|---|
| S'informer sur les cursus et prérequis | `epic-001` |
| Déposer une candidature en ligne | `epic-002` |
| Suivre l'avancement de son dossier | `epic-002` |
| Remplacer un document rejeté sans se déplacer | `epic-003` |

---

## Priorisation MoSCoW

Source : `PRD.md §6` (Must / Should / Won't). Consolidé ici pour le séquencement.

### Must Have — bloquant pour le lancement
| Fonctionnalité | Epic |
|---|---|
| Pages cursus avec dates clés et pièces requises | `epic-001` |
| Formulaire de candidature (infos + paiement simulé + upload) | `epic-002` |
| Génération de la référence `CAN-2026-X` | `epic-002` |
| Email de confirmation après soumission | `epic-002` |
| Suivi du dossier par référence + barre de progression | `epic-002` |
| Question `deplacement_physique` obligatoire + persistance | `epic-002` |
| Interface admin sécurisée (JWT) pour valider/rejeter un document | `epic-003` |
| Email de notification validation/rejet | `epic-003` |
| Remplacement d'un document rejeté depuis la page de suivi | `epic-003` |
| Simulation de paiement MonCash/NatCash + référence transactionnelle | `epic-002` |

### Should Have — important, non bloquant
| Fonctionnalité | Cible |
|---|---|
| Notifications SMS | Post-MVP (WS-05) |

### Won't Have — explicitement hors V1
| Fonctionnalité | Raison |
|---|---|
| Transactions monétaires réelles | Déléguées à FDS Pay |
| Espace étudiant complet (compte, historique) | Post-MVP |
| Plateforme de cours | FDS Akademi, hors périmètre |
| SSO institutionnel complet | Architecturalement préparé, non livré |
| Export CSV/PDF des dossiers | Post-MVP |

**Risque de confusion à nommer explicitement :** le candidat pourrait supposer qu'il paye réellement via MonCash. La simulation doit être visuellement claire (label "Simulation" dans l'UI) pour éviter les recours.

---

## Détail par Epic

### `epic-001` — Socle & Portail public

**Workstream :** WS-01  
**Statut :** ✅ Done — closed 2026-09-26  
**But en une phrase :** *"Le portail est en ligne, les cursus sont visibles, et l'infrastructure de développement et de déploiement est opérationnelle."*  
**Détail & Bilan :** Voir [epic-001-closeout.md](execution/epic-001-socle/epic-001-closeout.md).  
**Spécifications consolidées :** [ws-func-01-portail-public.md](functional-specs/ws-func-01-portail-public.md) et [ws-tech-01-portail-public.md](technical-specs/ws-tech-01-portail-public.md).

---

### `epic-002` — Candidature & Suivi

**Livrable :** le Walking Skeleton complet côté candidat — de la décision de postuler jusqu'à la réception de la référence et la consultation du statut.

**Workstreams :** WS-02, WS-03, WS-05

**But en une phrase :** *"Un candidat peut soumettre un dossier complet depuis son téléphone et suivre son avancement sans jamais se déplacer."*

**User stories principales :**
- `US-005` — Formulaire d'inscription & question `deplacement_physique` (infos personnelles, question obligatoire enregistrée en base).
- `US-006` — Simulation de paiement MonCash / NatCash avec référence transactionnelle.
- `US-007` — Téléversement sécurisé des pièces requises (PDF/JPG ≤ 5 Mo, vérification magic bytes).
- `US-008` — Finalisation de candidature & notification de confirmation (référence `CAN-2026-X` affichée, email asynchrone non bloquant).
- `US-009` — Consultation et suivi de dossier par référence (barre de progression).
- `US-010` — Remplacement d'un document rejeté depuis la page de suivi.

**Critère de sortie :** le Walking Skeleton du cahier des charges §5 s'exécute de bout en bout. `deplacement_physique` est enregistré. La référence est affichée et envoyée par email.

---

### `epic-003` — Administration & Audit

**Livrable :** le secrétariat peut traiter les dossiers. La boucle candidat/admin est fermée.

**Workstreams :** WS-04, WS-05

**But en une phrase :** *"Un administrateur authentifié peut valider ou rejeter chaque document — le candidat est notifié immédiatement et peut corriger sans se déplacer."*

**User stories principales :**
- `US-011` — Authentification de l'administrateur (email + mot de passe → JWT + RBAC).
- `US-012` — Dashboard admin : liste paginée et consultation des candidatures avec statuts et `deplacement_physique`.
- `US-013` — Validation ou rejet d'un document avec audit (`valide_par`, `date_validation` immuables).
- `US-014` — Notification email déclenchée par une décision admin (validation/rejet, non bloquant).

**Critère de sortie :** tous les scénarios du plan de tests fonctionnels (`cahier_des_charges.md §12.2`) passent. Les critères de succès du PRD §11 sont mesurables (≥ 20 candidatures, ≥ 70 % sans déplacement).

---

## Prochaines étapes immédiates

> `epic-001` est clôturé (socle, scaffold back/front, déploiement, US-001 à US-004). `epic-002` est ouvert, aucune story commencée.

1. **Refine `US-005`** (`epic-002`) — Formulaire d'inscription & question `deplacement_physique`. Passer par le skill `user-story` (Refine) : lever les questions ouvertes de la spec avant tout code. C'est la première story de l'Epic et il n'existe pas d'ordre de build explicite documenté.
2. **Construire `US-005`** — formulaire d'infos personnelles + question `deplacement_physique` obligatoire persistée en base (métrique principale du MVP, cible ≥ 70 % à `false`).
3. **Enchaîner `US-006` → `US-010`** dans l'ordre de l'Epic : simulation de paiement, téléversement sécurisé, finalisation + email, suivi par référence, remplacement d'un document rejeté.
4. **Documenter l'ordre de build** de l'Epic 2 dans sa section `EPIC_EXECUTION.md` si l'on dévie de l'ordre séquentiel par ID.

> Le statut quotidien (story en cours, bloquages) vit dans `project-docs/execution/` une fois le travail commencé — pas ici. Ce fichier ne change que si la séquence des Epics change.

---

*PLAN.md — FDS Portail — Bravetech · GL-EN3-2026*
