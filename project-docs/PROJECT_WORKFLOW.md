---
created: 2026-09-26T12:35:00Z
updated: 2026-11-05T17:47:40Z
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
| **Code mergé** | PR approuvée et mergée sur `master` |
| **CI verte, backend et frontend** | Les deux jobs de `.github/workflows/ci.yml` passent (US-025) : « Architecture & Unit Tests » (`pytest tests/`, dont `test_architecture.py`) et « Frontend » (`tsc -b`, `npm run lint` où un avertissement fait échouer, `npm run lint:archi` = steiger sans erreur, `npm test`, `vite build`). Le job backend calcule aussi le **score CRAP** (`tools/crap.py`) : aucune fonction au-dessus de 30 |
| **Comportement vérifié** | Le scénario de la User Story a été testé manuellement ou couvert par un test d'intégration |
| **Conforme au contrat et en production** | Les critères d'acceptation ont été relus contre le périmètre du document de lancement (Partie 3 et Partie 5 : par exemple, paiement réussi, échoué, refusé et relancé) ; la fonctionnalité marche sur `https://dorfilus.ueh.edu.ht`, pas seulement en local (voir `reviews/03`) |
| **Pas de logique métier dans Infrastructure** | Aucun import SQLAlchemy dans `entities/`, aucun appel métier dans `dal/` |
| **Pas de secret en clair** | Aucune clé API, token ou mot de passe dans le code versionné, pas même une valeur par défaut (`${VAR:?…}` dans `docker-compose.yml`) ; GitGuardian vert |
| **Pas d'adresse réelle** | Le dépôt est public : aucune adresse IP ni port d'accès tirés de la VM ou de ses journaux. Les tests utilisent des adresses fictives (RFC 5737) |
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
