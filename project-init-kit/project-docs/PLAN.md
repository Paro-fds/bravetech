---
created: 2026-09-26T00:30:00Z
updated: 2026-09-26T00:30:00Z
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
| `epic-002-candidature` | Candidature & Suivi | WS-02, WS-03, WS-05 | `epic-001` | Un candidat soumet un dossier complet et le suit via sa référence. |
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
- `US-005` — Formulaire multi-étapes (infos personnelles → paiement simulé → upload → soumission).
- `US-006` — Upload sécurisé d'un document PDF/JPG ≤ 5 Mo avec vérification magic bytes.
- `US-007` — Génération de la référence `CAN-2026-X` et affichage à l'écran.
- `US-008` — Email de confirmation asynchrone non bloquant.
- `US-009` — Page de suivi par référence avec barre de progression.
- `US-010` — Question `deplacement_physique` obligatoire enregistrée en base.
- `US-011` — Simulation paiement MonCash/NatCash avec référence transactionnelle.

**Critère de sortie :** le Walking Skeleton du cahier des charges §5 s'exécute de bout en bout. `deplacement_physique` est enregistré. La référence est affichée et envoyée par email.

---

### `epic-003` — Administration & Audit

**Livrable :** le secrétariat peut traiter les dossiers. La boucle candidat/admin est fermée.

**Workstreams :** WS-04, WS-05

**But en une phrase :** *"Un administrateur authentifié peut valider ou rejeter chaque document — le candidat est notifié immédiatement et peut corriger sans se déplacer."*

**User stories principales :**
- `US-012` — Authentification admin (email + mot de passe → JWT).
- `US-013` — Tableau de bord admin : liste paginée des candidatures avec statuts et `deplacement_physique`.
- `US-014` — Vue détaillée d'un dossier avec accès sécurisé aux documents via proxy.
- `US-015` — Validation / rejet d'un document avec audit (`valide_par`, `date_validation`).
- `US-016` — Email de notification validation/rejet au candidat (non bloquant).
- `US-017` — Remplacement d'un document rejeté depuis la page de suivi (upsert, statut → `en_attente`).
- `US-018` — Rate limiting sur `POST /api/v1/auth/token` (anti brute-force).

**Critère de sortie :** tous les scénarios du plan de tests fonctionnels (`cahier_des_charges.md §12.2`) passent. Les critères de succès du PRD §11 sont mesurables (≥ 20 candidatures, ≥ 70 % sans déplacement).

---

## Prochaines étapes immédiates

1. **Scaffold backend** (`epic-001`) — créer la structure `entities/`, `dal/`, `bll/`, `api/v1/`, `tests/`. Vérifier que `test_architecture.py` passe à vide.
2. **Scaffold frontend** (`epic-001`) — Vite + React + TypeScript + FSD + Steiger. Confirmer que le linter d'architecture échoue sur un import ascendant volontaire avant de déclarer le scaffold valide.
3. **Provisionner Railway + Vercel** — connecter GitHub, configurer les variables d'environnement, vérifier le premier déploiement automatique.
4. **Livrer US-001 et US-002** — première page cursus réelle, données en base, CI vert.

> Le statut quotidien (story en cours, bloquages) vit dans `project-docs/execution/` une fois le travail commencé — pas ici. Ce fichier ne change que si la séquence des Epics change.

---

*PLAN.md — FDS Portail — Bravetech · GL-EN3-2026*
