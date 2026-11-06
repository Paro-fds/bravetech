---
created: 2026-09-08T17:38:40Z
updated: 2026-11-06T03:03:27Z
---

# FDS Portail

Vitrine publique de la Faculté des Sciences de l'Université d'État d'Haïti (FDS-UEH) et plateforme de candidature en ligne : un candidat découvre l'admission au Premier cycle MPC, dépose son dossier et le suit depuis son téléphone, sans se déplacer.

- **En production :** https://dorfilus.ueh.edu.ht (VM Proxmox de la FDS)
- **Ce qu'on construit et pour qui :** [`project-docs/PRD.md`](project-docs/PRD.md)
- **Architecture :** [`project-docs/SOLUTION_DESIGN.md`](project-docs/SOLUTION_DESIGN.md)
- **Où en est le projet, prochaine story :** [`project-docs/execution/EPIC_EXECUTION.md`](project-docs/execution/EPIC_EXECUTION.md)
- **Pour un agent :** [`AGENTS.md`](AGENTS.md)

Stack : FastAPI + SQLAlchemy + Alembic + PostgreSQL (Clean Architecture) ; React 19 + Vite + TypeScript (Feature-Sliced Design) ; Docker Compose.

## Lancer le projet en développement

Prérequis : Python 3.11+, Node 22.

```bash
git config core.hooksPath .githooks        # une fois : date `updated:` des documents

# Backend (depuis la racine) — base SQLite locale par défaut
python -m venv .venv
.venv\Scripts\activate                     # Windows ; source .venv/bin/activate ailleurs
pip install -r requirements-dev.txt
python -m backend.scripts.migrer            # crée ou met à jour la base (Alembic)
uvicorn backend.main:app --reload           # http://localhost:8000/docs

# Frontend (autre terminal) — Vite relaie /api vers le port 8000
cd frontend
npm ci
npm run dev                                 # http://localhost:5173
```

Compte du personnel (espace `/admin`) : définir `ADMIN_SEED_EMAIL` et `ADMIN_SEED_PASSWORD` (12 caractères minimum), puis `python -m backend.scripts.seed_admin`.

Sans `RESEND_API_KEY`, les emails sont écrits dans le terminal du backend au lieu d'être envoyés.

### Avec Docker (comme en production)

```bash
cp .env.example .env      # remplir au moins POSTGRES_PASSWORD et JWT_SECRET
docker compose up -d --build
docker compose exec backend python -m backend.scripts.seed_admin
```

## Vérifier avant une pull request

Les mêmes contrôles que la CI (`.github/workflows/ci.yml`), obligatoires pour fusionner sur `master` :

```bash
pytest tests/                                   # dont tests/unit/test_architecture.py
cd frontend && npx tsc -b && npm run lint && npx steiger ./src && npm test && npm run build
```

Score CRAP : `python -m coverage run --source=backend -m pytest tests/ && python -m coverage json -o coverage.json && python tools/crap.py coverage.json --seuil 30`.

## Déploiement

Chaque fusion sur `master` dont la CI est verte est déployée automatiquement sur la VM : images publiées sur GHCR, puis `deploy/deploy.sh` (copie de la base, migrations, contrôle de santé, retour arrière automatique). Détails : [`technical-specs/ws-tech-01-portail-public.md` §5.3](project-docs/technical-specs/ws-tech-01-portail-public.md).

## Organisation du dépôt

Voir la carte des dossiers dans [`AGENTS.md`](AGENTS.md). Le projet est parti du kit d'initialisation du cours ; son mode d'emploi d'origine reste dans l'historique git de ce fichier et dans [`project-docs/learnings/`](project-docs/learnings/).

---

*Bravetech · GL-EN3-2026*
