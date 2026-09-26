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
                              │   └── cursus_repository_json.py (JsonCursusRepository)
                              └── entities/
                                  ├── cursus.py
                                  ├── matiere.py
                                  └── document_requis.py
                                            │
                                            ▼
                               [Fichiers JSON Référence (cursus/*.json)]
                               ├── mpc.json
                               ├── genie-civil.json
                               ├── genie-electronique.json
                               ├── genie-electromecanique.json
                               └── architecture.json
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

## 3. Modèle de données & Source de vérité (Fichiers JSON `cursus/`)

Contrairement aux données transactionnelles (candidats, dossiers, pièces soumises gérés dans PostgreSQL à partir de l'Epic 2), l'offre académique des cursus et pièces requises constitue un **catalogue de référence statique**.

Les informations sont directement exploitées depuis les fichiers JSON officiels dans `cursus/` via `JsonCursusRepository` :
- `cursus/mpc.json` : Tronc commun Math-Physique-Chimie (durée 2 ans, semestres S1-S4).
- `cursus/genie-civil.json` : Filière Génie Civil (niveaux GC1 à GC3, semestres S5-S10).
- `cursus/genie-electronique.json` : Filière Génie Électronique (niveaux GEL1 à GEL3, semestres S5-S10).
- `cursus/genie-electromecanique.json` : Filière Génie Électromécanique (niveaux GIN1 à GIN3, semestres S5-S10).
- `cursus/architecture.json` : Filière Architecture (niveaux ARC1 à ARC3, semestres S5-S10).

**Avantages architecturaux :**
- Aucune migration de table SQL requise pour mettre à jour les descriptions ou programmes académiques.
- Versionnage direct sous Git dans le dépôt de code.
- Disponibilité immédiate et mise en cache mémoire via `JsonCursusRepository`.

---

## 4. Règles architecturales & Sécurité (Relocalisées de `epic-001-refinement.md`)

Les règles suivantes, actives durant l'Epic 1, sont désormais pérennes dans le socle technique :

1. **Règle R1 — Source de vérité Cursus en fichiers JSON** :
   - Les cursus et documents requis sont gérés sous forme de fichiers JSON locaux versionnés. Aucune table SQL n'est utilisée pour ces données statiques de référence.
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
