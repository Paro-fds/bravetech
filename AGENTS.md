---
created: 2026-09-26T12:52:00Z
updated: 2026-11-06T03:03:27Z
---

# AGENTS.md — FDS Portail

## Ce qu'est ce projet

FDS Portail est la vitrine publique officielle de la Faculté des Sciences (FDS-UEH) et sa plateforme de candidature dématérialisée. Un candidat peut s'informer sur les cursus, soumettre son dossier et suivre son traitement intégralement depuis son smartphone, sans se déplacer. Voir `PRD.md` pour le périmètre complet, les personas et les critères de succès.

**Problème central résolu :** un candidat hors de Port-au-Prince devait se déplacer physiquement pour candidater. FDS Portail supprime cette contrainte.

---

## Carte des dossiers

```
bravetech/                          # racine du dépôt
├── AGENTS.md  CLAUDE.md  README.md
├── cahier_des_charges.md           # Livrable 1 : référence métier
├── project-docs/
│   ├── PRD.md  NFR.md  SOLUTION_DESIGN.md  PLAN.md  GLOSSARY.md  PROJECT_WORKFLOW.md
│   ├── _ARCHITECTURE_EXPLAINED.md  # Référence architecture (ne jamais modifier)
│   ├── execution/                  # EPIC_EXECUTION.md + epic-NNN-*/US-NNN.md
│   ├── functional-specs/  technical-specs/   # Une spec par Workstream (ws-func-NN, ws-tech-NN)
│   ├── reviews/                    # Croyances invalidées — écrire au moment de la découverte
│   ├── learnings/                  # Pratiques transférables à un autre projet
│   ├── exploration/                # Notes exploratoires — jamais citées comme décision
│   └── templates/                  # Gabarit de user story
├── backend/
│   ├── entities/                   # Domain — dataclasses pures, zéro dépendance externe
│   ├── ports/                      # Interfaces abstraites (ICandidatureRepository, IStockageFichiers, IEmailSender…)
│   ├── bll/                        # Application — cas d'utilisation (*UseCase)
│   ├── dal/                        # Infrastructure — SQLAlchemy, migrations Alembic (dal/migrations/), stockage local, Resend, JWT
│   ├── api/v1/                     # Presentation — routers FastAPI, DTOs Pydantic (api/v1/dto/)
│   └── scripts/                    # migrer.py (lancé au démarrage), seed_admin.py
├── frontend/src/                   # FSD : app/ pages/ features/ entities/ shared/ (steiger en CI)
├── cursus/                         # Offre académique en JSON (source de vérité des cursus)
├── tests/
│   ├── unit/test_architecture.py   # ← Gardien de la Clean Architecture (CI)
│   ├── unit/                       # Entités et cas d'utilisation, sans base
│   └── integration/                # Routes FastAPI sur SQLite en mémoire, migrations
├── tools/crap.py                   # Score CRAP (CI : échec au-dessus de 30)
├── deploy/deploy.sh                # Déploiement et retour arrière sur la VM (ADR-009)
├── docker-compose.yml              # Développement ; docker-compose.prod.yml : production (images GHCR)
├── .github/workflows/              # ci.yml (contrôles), deploy.yml (déploiement continu)
└── .claude/skills/                 # Skills du kit (user-story, epic, get-work-status…)
```

---

## Stack technique

Voir `SOLUTION_DESIGN.md §5` — ne pas recopier ici. En résumé :
- **Backend :** FastAPI + SQLAlchemy + Alembic + PostgreSQL
- **Frontend :** React 19 + Vite + TypeScript + FSD
- **Hébergement :** Docker Compose sur la VM Proxmox de la FDS ; déploiement continu GitHub Actions → GHCR → SSH (ADR-006, ADR-009)
- **Services :** volume Docker de la VM pour les pièces (ADR-007, pas Cloudinary), Resend pour les emails
- **Auth :** JWT HS256 + bcrypt

---

## Règle de dépendance — non négociable

La Clean Architecture impose une direction d'import stricte :

```
entities/ ← bll/ ← dal/
               ↑
           api/v1/
```

**`tests/unit/test_architecture.py` fait échouer le build si cette règle est violée.** Ce test tourne à chaque CI. Ne jamais merger une PR avec ce test rouge.

Règle complémentaire : **jamais de logique métier dans `dal/`, jamais d'import SQLAlchemy dans `entities/`.**

---

## Conventions de nommage

**Python (backend) :**
- Fichiers : `snake_case.py`
- Classes/Entités : `PascalCase` (ex. `SqlCandidatureRepository`, `DocumentSoumis`)
- Variables/fonctions : `snake_case`
- Booléens : préfixés `est_` (ex. `est_actif`, `est_admission`, `est_obligatoire`)
- Constantes : `UPPER_SNAKE_CASE`
- Interfaces (ports) : préfixées `I` (ex. `ICandidatureRepository`, `IEmailSender`)

**TypeScript/React (frontend) :**
- Composants : `PascalCase.tsx`
- Fichiers non-composants : `camelCase.ts`
- Variables/fonctions : `camelCase`
- Booléens : préfixés `est` ou `is` (ex. `estKreyol`, `isLoading`)
- Types/Interfaces : `PascalCase`

**Horodatages :** toujours UTC, format ISO-8601 avec `Z` (`2026-09-26T12:52:00Z`). Jamais d'heure locale stockée.

**Identifiants de structure :**
- Workstreams : `WS-NN` (ex. `WS-02`)
- Epics : `epic-NNN-nom` (ex. `epic-002-candidature`)
- User Stories : `US-NNN` séquentiel sur tout le projet (ex. `US-005`)
- Références dossier : `CAN-YYYY-NNNN` (ex. `CAN-2026-0089`)

**Fichiers numérotés (`reviews/`, `learnings/`) :** `NN-nom-court.md` — numéro attribué une fois, jamais réattribué.

---

## Où va une règle quand le travail en produit une

| Ce que le résultat s'avère être | Où va la règle |
|---|---|
| Ce qu'est le produit, ou pour qui il est | `PRD.md` |
| Un niveau de qualité, un risque, une dépendance | `NFR.md` |
| Une décision ou contrainte d'architecture | `SOLUTION_DESIGN.md §14` (ADR) |
| Comment on travaille, ou ce que Fini signifie | `PROJECT_WORKFLOW.md` |
| Comment un Workstream se comporte / est construit | Sa spec fonc ou tech dans `functional-specs/` ou `technical-specs/` |
| Ce que signifie un mot | `GLOSSARY.md` |
| Quelque chose qu'aucune session ne peut se tromper | Ce fichier (`AGENTS.md`) |
| Pratique transférable à un autre projet | `learnings/` |
| Règle en cours pendant un Epic ouvert | `execution/epic-NNN-*/epic-NNN-refinement.md` — **vidé à la clôture** |
| Rien au-delà de la correction elle-même | Reste dans `reviews/` — la review est alors complète |

**Une règle ne vit jamais uniquement dans une review.** Une review documente ce qui était cru et pourquoi c'était faux. La règle qui en est issue se déplace dans le document propriétaire avant que le travail soit déclaré terminé.

---

## Pointeurs canoniques

| Question | Document de référence |
|---|---|
| Qu'est-ce qu'on construit ? | `PRD.md` |
| Pour qui, et quel problème ? | `PRD.md §2-4` |
| Quelle barre de qualité ? | `NFR.md` |
| Comment c'est architecturé ? | `SOLUTION_DESIGN.md` + `_ARCHITECTURE_EXPLAINED.md` |
| Dans quel ordre on construit ? | `PLAN.md` |
| Qu'est-ce que ce terme veut dire ? | `GLOSSARY.md` |
| Comment le travail circule ? | `PROJECT_WORKFLOW.md` |
| Quel est le statut d'un Epic en cours ? | `execution/EPIC_EXECUTION.md` |
| Quelles décisions ont été prises et pourquoi ? | `SOLUTION_DESIGN.md §14` (ADRs) |
| Quels risques connus ? | `NFR.md §Risques` |
| Quelles hypothèses ? | `SOLUTION_DESIGN.md §12` |

---

## Faits critiques à ne pas se tromper

1. **PostgreSQL est la seule source de vérité.** Les fichiers stockés et les statuts email sont des effets de bord — jamais des états.

2. **L'email est non bloquant.** Une erreur Resend ne doit jamais annuler une candidature ou une validation. La référence dossier s'affiche à l'écran même si l'email échoue.

3. **`deplacement_physique`** est un champ obligatoire sur chaque candidature — c'est la métrique principale du MVP (cible : ≥ 70 % à `false`).

4. **`(candidat_id, document_requis_id)` est une contrainte UNIQUE.** Le remplacement d'un document rejeté est un upsert — jamais une insertion qui créerait un doublon.

5. **Toute action admin est auditée** — `valide_par` + `date_validation` sont immuables une fois écrits.

6. **Les fichiers sont validés côté serveur** — magic bytes (`filetype`), extension, taille ≤ 5 Mo — avant tout stockage.

7. **Les routes `/api/v1/admin/` sont protégées par JWT** — `get_current_admin` est posé sur le routeur admin (toute nouvelle route en hérite) ; `get_current_admin_complet` pour ce qui est réservé au rôle `admin`.

8. **La simulation de paiement doit être visuellement claire** — le candidat ne doit pas croire qu'il paye réellement (risque de recours).

9. **L'admission est unique : Premier cycle MPC.** Aucun champ « cursus » ni « filière » dans la candidature : le candidat choisit sa branche (Génie Civil, Électromécanique, Électronique, Architecture) après le MPC, hors du portail. Parcours total : 2 + 3 = 5 ans. Les pièces requises sont une liste unique de 5 (acte de naissance, Bac II, relevé de notes, deux photos d'identité, CIN) — ni bonne vie et mœurs, ni certificat médical. Voir ADR-008.

---

## Ordre de lecture pour une session

**Reprise rapide (agent déjà orienté) :**
1. Ce fichier (`AGENTS.md`)
2. `execution/EPIC_EXECUTION.md` — statut de l'Epic en cours

**Orientation complète (première session ou après une longue pause) :**
1. `PRD.md` — quoi, pour qui, critères de succès
2. `SOLUTION_DESIGN.md` — architecture, Workstreams, ADRs
3. `PLAN.md` — Epics et User Stories
4. `_ARCHITECTURE_EXPLAINED.md` Partie 1 — Règle de Dépendance et structure des couches
5. `tests/unit/test_architecture.py` — comprendre ce que le CI vérifie automatiquement

---

*AGENTS.md — FDS Portail — Bravetech · GL-EN3-2026*

