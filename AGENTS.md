---
created: 2026-09-26T12:52:00Z
updated: 2026-09-30T16:04:08Z
---

# AGENTS.md — FDS Portail

## Ce qu'est ce projet

FDS Portail est la vitrine publique officielle de la Faculté des Sciences (FDS-UEH) et sa plateforme de candidature dématérialisée. Un candidat peut s'informer sur les cursus, soumettre son dossier et suivre son traitement intégralement depuis son smartphone, sans se déplacer. Voir `PRD.md` pour le périmètre complet, les personas et les critères de succès.

**Problème central résolu :** un candidat hors de Port-au-Prince devait se déplacer physiquement pour candidater. FDS Portail supprime cette contrainte.

---

## Carte des dossiers

```
bravetech/
├── cahier_des_charges.md           # Référence métier francophone complète
├── tests/
│   ├── conftest.py
│   ├── unit/
│   │   ├── test_architecture.py   # ← Gardien de la Clean Architecture (run en CI)
│   │   └── entities/              # Tests des règles métier pures
│   └── integration/               # Tests des routes FastAPI (DB de test)
│
└── project-init-kit/
    ├── AGENTS.md                  # ← ce fichier
    ├── CLAUDE.md                  # import de ce fichier + instructions Claude Code
    ├── STARTER_PROMPT.md
    └── project-docs/
        ├── PRD.md                 # Quoi / pour qui / pourquoi
        ├── NFR.md                 # Barre de qualité (perf, sécu, dispo...)
        ├── SOLUTION_DESIGN.md     # Architecture, Workstreams, ADRs, stack
        ├── PLAN.md                # Epics, User Stories, MoSCoW
        ├── GLOSSARY.md            # Vocabulaire du domaine
        ├── PROJECT_WORKFLOW.md    # Tracker, définition de fini, init
        ├── _ARCHITECTURE_EXPLAINED.md  # Référence architecture (ne pas modifier)
        ├── execution/             # Suivi en cours d'Epic (EPIC_EXECUTION.md)
        ├── functional-specs/      # Specs fonctionnelles par Workstream
        ├── technical-specs/       # Specs techniques par Workstream
        ├── reviews/               # Croyances invalidées — écrire au moment de la découverte
        ├── learnings/             # Pratiques transférables — écrire après une review
        ├── exploration/           # Notes exploratoires — jamais mises à jour, jamais citées comme décision
        └── templates/             # Templates user-story, etc.
```

**Backend (à scaffolder) :**
```
backend/
├── entities/     # Domain — dataclasses pures, zéro dépendance externe
├── bll/          # Application — use cases + interfaces (ports)
├── ports/        # Interfaces abstraites (ICandidatRepository, IEmailService...)
├── dal/          # Infrastructure — adapters SQLAlchemy, Cloudinary, Resend
└── api/v1/       # Presentation — routers FastAPI, Pydantic DTOs
```

---

## Stack technique

Voir `SOLUTION_DESIGN.md §5` — ne pas recopier ici. En résumé :
- **Backend :** FastAPI + SQLAlchemy + PostgreSQL (Railway)
- **Frontend :** React 19 + Vite + TypeScript + FSD (Vercel)
- **Services :** Cloudinary (fichiers), Resend (emails)
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
- Classes/Entités : `PascalCase` (ex. `CandidatRepository`, `DocumentSoumis`)
- Variables/fonctions : `snake_case`
- Booléens : préfixés `is_`, `has_`, `can_` (ex. `is_valid`, `has_document`)
- Constantes : `UPPER_SNAKE_CASE`
- Interfaces (ports) : préfixées `I` (ex. `ICandidatRepository`, `IEmailService`)

**TypeScript/React (frontend) :**
- Composants : `PascalCase.tsx`
- Fichiers non-composants : `camelCase.ts`
- Variables/fonctions : `camelCase`
- Booléens : préfixés `is`, `has`, `can`
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

1. **PostgreSQL est la seule source de vérité.** Les URLs Cloudinary et les statuts email sont des effets de bord — jamais des états.

2. **L'email est non bloquant.** Une erreur Resend ne doit jamais annuler une candidature ou une validation. La référence dossier s'affiche à l'écran même si l'email échoue.

3. **`deplacement_physique`** est un champ obligatoire sur chaque candidature — c'est la métrique principale du MVP (cible : ≥ 70 % à `false`).

4. **`(candidat_id, document_requis_id)` est une contrainte UNIQUE.** Le remplacement d'un document rejeté est un upsert — jamais une insertion qui créerait un doublon.

5. **Toute action admin est auditée** — `valide_par` + `date_validation` sont immuables une fois écrits.

6. **Les fichiers sont validés côté serveur** — magic bytes (`filetype`), extension, taille ≤ 5 Mo — avant tout stockage Cloudinary.

7. **Les routes `/api/v1/admin/` sont protégées par JWT** — `get_current_admin()` à chaque endpoint, jamais seulement à la connexion.

8. **La simulation de paiement doit être visuellement claire** — le candidat ne doit pas croire qu'il paye réellement (risque de recours).

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

