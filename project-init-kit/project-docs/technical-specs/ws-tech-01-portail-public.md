---
created: 2026-09-26T15:23:00Z
updated: 2026-09-26T15:23:00Z
workstream: WS-01
---

# Spécification Technique — WS-01 Portail Public

**Workstream :** WS-01 Portail public  
**Statut :** ✅ Livré via Epic 1 (US-001, US-002, US-003, US-004)  
**Couplage fonctionnel :** [ws-func-01-portail-public.md](../functional-specs/ws-func-01-portail-public.md)

---

## 1. Vue d'ensemble de l'implémentation

Le Workstream WS-01 est implémenté selon les principes de la **Clean Architecture** (backend FastAPI) et de **Feature-Sliced Design** (frontend React SPA).

```
[Navigateur / Client HTTP]
          │
          ▼
   [Nginx Proxy (Frontend:80)]
   ├── /api/  ───────────────► [FastAPI Backend:8000]
   └── / (static SPA)         ├── api/v1/endpoints/cursus.py
                              ├── bll/use_cases/
                              │   ├── lister_cursus.py
                              │   └── obtenir_cursus_detail.py
                              ├── dal/repositories/
                              │   └── sqlalchemy_cursus_repository.py
                              └── entities/
                                  ├── cursus.py
                                  ├── matiere.py
                                  └── document_requis.py
                                            │
                                            ▼
                               [PostgreSQL 15 (Port 5432)]
                               ├── table: cursus
                               └── table: documents_requis
```

---

## 2. Contrats d'API & Endpoints

### 2.1 Lister les cursus
- **Méthode** : `GET`
- **Route** : `/api/v1/cursus`
- **Paramètres** : Aucun
- **Réponse 200 OK** :
```json
[
  {
    "id": "genie-civil",
    "nom": "Génie Civil",
    "departement": "Génie",
    "description": "Formation d'ingénieurs spécialisés en conception structurale...",
    "duree_annees": 5,
    "semestres": 10,
    "credits_totaux": 160,
    "matieres_count": 52
  }
]
```

### 2.2 Consulter le détail d'un cursus
- **Méthode** : `GET`
- **Route** : `/api/v1/cursus/{id}`
- **Réponse 200 OK** :
```json
{
  "id": "genie-civil",
  "nom": "Génie Civil",
  "departement": "Génie",
  "description": "...",
  "duree_annees": 5,
  "semestres": 10,
  "credits_totaux": 160,
  "matieres": [
    {
      "code": "GC-101",
      "nom": "Mécanique des structures",
      "semestre": 1,
      "credits": 4,
      "description": "..."
    }
  ],
  "documents_requis": [
    {
      "code": "ACTE_NAISSANCE",
      "nom": "Acte de naissance ou extrait d'archives",
      "description": "Copie certifiée conforme",
      "obligatoire": true
    }
  ]
}
```
- **Réponse 404 Not Found** :
```json
{
  "detail": "Cursus non trouvé: inconnu"
}
```

---

## 3. Schéma de données (PostgreSQL)

### 3.1 Table `cursus`
- `id` : `VARCHAR(64)` PRIMARY KEY
- `nom` : `VARCHAR(255)` NOT NULL
- `departement` : `VARCHAR(128)` NOT NULL
- `description` : `TEXT` NOT NULL
- `duree_annees` : `INTEGER` NOT NULL
- `semestres` : `INTEGER` NOT NULL
- `credits_totaux` : `INTEGER` NOT NULL
- `matieres_json` : `JSONB` NOT NULL (liste sérialisée des matières du cursus)

### 3.2 Table `documents_requis`
- `id` : `SERIAL` PRIMARY KEY
- `cursus_id` : `VARCHAR(64)` REFERENCES `cursus(id)` ON DELETE CASCADE
- `code` : `VARCHAR(64)` NOT NULL
- `nom` : `VARCHAR(255)` NOT NULL
- `description` : `TEXT`
- `obligatoire` : `BOOLEAN` DEFAULT TRUE

---

## 4. Règles architecturales & Sécurité (Relocalisées de `epic-001-refinement.md`)

Les règles suivantes, actives durant l'Epic 1, sont désormais pérennes dans le socle technique :

1. **Règle R1 — Protection du Seeding en production** :
   - Le chargement initial ou la réinitialisation des cursus (`cursus_loader.py`) ne doit jamais écraser silencieusement des données de production.
   - En environnement de production, l'initialisation doit être protégée ou déclenchée explicitement via script d'administration ou migration sécurisée.
2. **Règle R2 — Gestion stricte des secrets et variables d'environnement** :
   - Tout secret (`DATABASE_URL`, identifiants de connexion, futures clés JWT) doit être déclaré dans `.env` et proscrit de tout commit Git.
   - Un fichier modèle `.env.example` sans aucun secret réel documente les variables requises.
3. **Règle R3 — Invariant des tests d'architecture** :
   - `tests/unit/test_architecture.py` applique la règle de dépendance Clean Architecture : la couche `backend/entities/` ne doit dépendre d'aucun module externe (ni `fastapi`, ni `sqlalchemy`, ni `dal`, ni `bll`, ni `api`).
   - Le test doit passer sans erreur même sur un module vide pour prévenir toute rupture de CI lors de refactorisations.

---

## 5. Déploiement et Conteneurisation (ADR-006)

Conformément à l'ADR-006 (serveur Linux sur site / Proxmox à la Faculté des Sciences) :
- **Backend Dockerfile** : Image Python 3.11-slim optimisée avec installation des dépendances et lancement par Uvicorn.
- **Frontend Dockerfile** : Multi-stage build (Node 20 Alpine pour la compilation Vite + Nginx Alpine pour servir les fichiers statiques).
- **Reverse Proxy Nginx** : Configuration `nginx.conf` routant `/api/` vers le service backend Docker et servant `index.html` pour les routes SPA côté client.
- **Orchestration Docker Compose** : `docker-compose.yml` déclarant les 3 services (`db`, `backend`, `frontend`), les réseaux internes et le volume persistant `postgres_data`.

---

*ws-tech-01-portail-public.md — FDS Portail — Bravetech · GL-EN3-2026*
