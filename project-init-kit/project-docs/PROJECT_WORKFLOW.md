---
created: 2026-09-26T12:35:00Z
updated: 2026-09-26T12:35:00Z
---

# PROJECT_WORKFLOW.md — FDS Portail

**Réponses :** Comment le travail circule-t-il réellement, et quel document faut-il toucher quand ?
**Dépend de :** tout ce qui précède — c'est le tissu de raccord.

---

## Quel document mettre à jour, et quand

*Générique — réutilise ce tableau tel quel.*

| Document | Granularité | Mis à jour quand |
|---|---|---|
| `project-docs/execution/EPIC_EXECUTION.md` | Par histoire | En continu — chaque fois que le statut d'une histoire change |
| `project-docs/functional-specs/`, `project-docs/technical-specs/` | Par Workstream | De façon incrémentale, au moment où une histoire est livrée |
| `project-docs/reviews/` | **Par découverte** | **Au moment où une croyance se révèle fausse** — pas à la fin du travail |
| `project-docs/PLAN.md` | Par Epic | Seulement quand un Epic commence ou se termine |
| `project-docs/PRD.md` | Par décision | Seulement quand une vraie décision produit/scope change |
| `project-docs/SOLUTION_DESIGN.md` (§ ADR) | Par décision d'architecture | Quand un vrai choix d'architecture est fait ou change |
| `project-docs/NFR.md` | Par exigence | Quand une exigence de qualité, un risque ou une dépendance apparaît ou change |
| `project-docs/GLOSSARY.md` | Par terme | Avant qu'un nouveau terme ambigu ne soit utilisé ailleurs |
| `project-docs/learnings/` | Par pratique réutilisable | Quand une revue s'avère vraie au-delà de cette base de code |
| `project-docs/PROJECT_WORKFLOW.md` | Par convention | Quand une convention de processus change |
| `CLAUDE.md` / `AGENTS.md` | Faits critiques pour la session | Quand un fait que chaque session doit connaître change |
| `project-docs/execution/epic-NNN-*/epic-NNN-refinement.md` | Par Epic | Écrit au moment du Refine, vidé dans les documents ci-dessus à la clôture de l'Epic |
| `project-docs/exploration/` | Jamais mis à jour | Écrit une fois, conservé tel quel, jamais cité comme décision |

---

## Suivi du travail (Tracker)

**Outil choisi : GitHub Issues + GitHub Projects.**

L'organisation du tracker suit la hiérarchie : Epic (Milestone GitHub) → User Story (Issue GitHub) → tâches (checklist dans l'Issue).

### États d'une User Story

| État | Label GitHub | Signification |
|---|---|---|
| `backlog` | *(pas de label)* | Définie, pas encore planifiée dans un sprint |
| `ready` | `ready` | Critères d'acceptation écrits, peut être démarrée |
| `in-progress` | `in-progress` | Un développeur travaille dessus |
| `in-review` | `in-review` | PR ouverte, en attente de review |
| `done` | *(Issue fermée)* | Définition de fini respectée, mergée sur `main` |

### Règles de création d'une Issue

- **Titre :** `US-NNN — [verbe] [objet]` (ex. `US-005 — Formulaire multi-étapes de candidature`).
- **Corps :** utiliser le template `project-docs/templates/user-story.md`.
- **Milestone :** assigner à l'Epic correspondant (`epic-001`, `epic-002`, `epic-003`).
- **Assignee :** une seule personne responsable par Issue.

---

## Format de user story

Voir [`project-docs/templates/user-story.md`](templates/user-story.md) — ne pas dupliquer ici.

---

## Définition de fini (niveau projet)

Chaque User Story doit satisfaire **tous** ces critères avant d'être marquée `done` :

| Critère | Vérification |
|---|---|
| **Code mergé** | PR approuvée et mergée sur `main` |
| **Tests verts** | `pytest tests/` passe en CI — dont `test_architecture.py` |
| **Pas de régression** | Le build Vite (`npm run build`) passe sans erreur |
| **Comportement vérifié** | Le scénario de la User Story a été testé manuellement ou couvert par un test d'intégration |
| **Pas de logique métier dans Infrastructure** | Aucun import SQLAlchemy dans `entities/`, aucun appel métier dans `dal/` |
| **Pas de secret en clair** | Aucune clé API, token ou mot de passe dans le code versionné |
| **Document mis à jour si nécessaire** | Si la story change un contrat API, un schéma de données ou une décision d'architecture → le document correspondant est mis à jour avant de fermer l'Issue |

> **Différence entre « fonctionnel » et « fini » :** une story qui fonctionne localement mais dont les tests échouent en CI n'est **pas** finie. Une story qui passe en CI mais introduit une violation de la Règle de Dépendance n'est **pas** finie — `test_architecture.py` est le gardien automatique de cette règle.

---

## Référence de vocabulaire

Chaque terme utilisé dans les spécifications, ce document et les conversations se résout dans [`GLOSSARY.md`](GLOSSARY.md).

---

## Étapes d'initialisation du tracker

À effectuer **une seule fois** par développeur après un clone du dépôt :

**1. Activer les hooks Git**
```bash
git config core.hooksPath .githooks
```
Active `.githooks/pre-commit`, qui inscrit `updated:` (UTC) sur chaque fichier Markdown indexé. Une date présente et fausse est lue comme vraie — ne pas ignorer cette étape.

**2. Installer les dépendances backend**
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

**3. Installer les dépendances frontend**
```bash
cd frontend
npm install
```

**4. Copier et remplir les variables d'environnement**
```bash
cp .env.example .env
# Remplir DATABASE_URL, CLOUDINARY_*, RESEND_API_KEY, SECRET_KEY
```

**5. Vérifier que les tests d'architecture passent**
```bash
pytest tests/unit/test_architecture.py -v
```
Si ce test est rouge sur un projet vide, c'est un problème de configuration — corriger avant d'écrire la moindre ligne de code métier.

**6. Créer les Milestones GitHub**
Dans GitHub → Issues → Milestones : créer `epic-001-socle`, `epic-002-candidature`, `epic-003-administration`.

---

*PROJECT_WORKFLOW.md — FDS Portail — Bravetech · GL-EN3-2026*


---

*PROJECT_WORKFLOW.md — FDS Portail — Bravetech · GL-EN3-2026*
