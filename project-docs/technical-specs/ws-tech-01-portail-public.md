---
created: 2026-09-26T15:23:00Z
updated: 2026-11-04T20:08:30Z
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

Contrairement aux données transactionnelles (candidats, dossiers, pièces soumises gérés dans PostgreSQL à partir de l'Epic 2), l'offre académique (filières, durée, programmes) constitue un **catalogue de référence statique**. Les **pièces requises d'admission** forment une liste unique de 5 pièces (ADR-008) définie côté backend (`backend/dal/cursus_loader.py`), et non dans les fichiers JSON.

> **Écart code / règle (2026-10-31) :** `_creer_documents_requis_par_defaut` génère aujourd'hui 4 pièces et ajoute une « attestation de validation du cycle MPC » pour les cursus hors MPC. La règle d'admission unique demande une liste unique de 5 pièces (ajout de la CIN, photos d'identité, retrait de l'attestation MPC) et la fin de la distinction par cursus. À traiter avec US-005 / US-007.

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
   - Les cursus (filières, durée, programmes) sont gérés sous forme de fichiers JSON locaux versionnés. Aucune table SQL n'est utilisée pour ces données statiques de référence. La liste des pièces requises est unique et définie côté backend (voir §3).
2. **Règle R2 — Gestion stricte des secrets et variables d'environnement** :
   - Tout secret (`DATABASE_URL`, identifiants de connexion, futures clés JWT) doit être déclaré dans `.env` et proscrit de tout commit Git.
   - Un fichier modèle `.env.example` sans aucun secret réel documente les variables requises.
3. **Règle R3 — Invariant des tests d'architecture** :
   - `tests/unit/test_architecture.py` applique la règle de dépendance Clean Architecture : la couche `backend/entities/` ne doit dépendre d'aucun module externe (ni `fastapi`, ni `sqlalchemy`, ni `dal`, ni `bll`, ni `api`).
   - Le test doit passer sans erreur même sur un module vide pour prévenir toute rupture de CI lors de refactorisations.
4. **Règle R4 — Couleurs du frontend par jetons de rôle uniquement (US-017)** :
   - Les composants n'emploient que les jetons `fds-*` définis dans `frontend/src/app/styles/index.css` (`bg-fds-surface`, `text-fds-title`, `text-fds-accent`, `border-fds-bad-line`…). Jamais de couleur codée en dur (`bg-white`, `bg-[#…]`, `text-slate-…`) : elle ne suivrait pas le mode sombre.
   - Un jeton nomme un **rôle**, pas une teinte : `fds-accent` (liens, icônes, bordures actives) devient clair en mode sombre, alors que `fds-navy` reste un aplat foncé qui porte du texte blanc. Exceptions voulues : `text-white` et `bg-white/10` sur les aplats marine, et la pastille blanche active du sélecteur de langue (`bg-white text-fds-on-light`).
   - Les illustrations SVG (cursus, bandeau d'accueil) suivent la même règle : couleurs par classes `fill-fds-*` / `stroke-fds-*`, jamais d'attribut `fill="#…"` (US-022).
   - Le mode sombre redéfinit les jetons sous `:root[data-theme='dark']`. Toute nouvelle paire texte/fond doit tenir 4,5:1 (texte) ou 3:1 (bord de champ, remplissage de barre) dans les deux thèmes.
   - Le thème est posé sur `<html data-theme>` par un court script de `index.html`, avant le premier affichage, puis par `shared/theme/useTheme.ts`. Ordre de priorité : choix mémorisé (`localStorage`, clé `fds-theme`, valeur `clair` ou `sombre`), sinon préférence du système. Les deux endroits appliquent la même règle et doivent rester alignés.

---

## 5. Déploiement et Conteneurisation (ADR-006)

Conformément à l'ADR-006 (serveur Linux sur site / Proxmox à la Faculté des Sciences) :
- **Backend Dockerfile** : Image Python 3.11-slim optimisée avec installation des dépendances et lancement par Uvicorn.
- **Frontend Dockerfile** : Multi-stage build (Node 20 Alpine pour la compilation Vite + Nginx Alpine pour servir les fichiers statiques).
- **Reverse Proxy Nginx** : Configuration `nginx.conf` routant `/api/` vers le service backend Docker et servant `index.html` pour les routes SPA côté client.
- **Orchestration Docker Compose** : `docker-compose.yml` déclarant les 3 services (`db`, `backend`, `frontend`), les réseaux internes et le volume persistant `postgres_data`.

### 5.1 Schéma de la base : migrations Alembic (US-023)

- **Le schéma n'est créé que par les migrations.** `Base.metadata.create_all` n'est plus appelé par l'application : il crée les tables manquantes mais ne modifie jamais une table existante, si bien qu'une colonne ajoutée n'arriverait jamais en production. Seuls les tests d'intégration l'utilisent encore, sur une base SQLite en mémoire.
- **Au démarrage du conteneur backend**, `python -m backend.scripts.migrer` applique `alembic upgrade head`, puis uvicorn démarre. Si une migration échoue, l'API ne démarre pas. En développement, on lance la même commande avant `uvicorn`.
- **Modifier un modèle (`backend/dal/models.py`) impose une migration** dans la même PR :
  `alembic -c backend/alembic.ini revision --autogenerate -m "description"`, depuis la racine du dépôt, puis relire le fichier produit dans `backend/dal/migrations/versions/`. Le test `tests/integration/test_migrations.py` fait échouer la CI si les modèles et la dernière migration divergent.
- **Adoption d'une base créée avant Alembic** (la base de la VM, créée par `create_all` le 2026-11-04) : `backend/dal/schema.py` la détecte (tables présentes, pas de table `alembic_version`) et la marque à la révision `0001` sans la modifier, ce qui équivaut à `alembic stamp 0001`. Les données restent intactes. L'adoption est **refusée** si une table ou une colonne des modèles manque : une base plus ancienne que `0001` ne doit pas être déclarée à jour. Une table en trop (`cursus`, `documents_requis` dans les vieilles bases de développement) est tolérée.
- **Pilote PostgreSQL : psycopg2.** SQLAlchemy 2.1 prend psycopg 3 par défaut pour `postgresql://`, qui n'est pas installé. `backend/dal/database.py` réécrit donc `postgresql://` et `postgres://` en `postgresql+psycopg2://`, quelle que soit l'URL fournie.
- **Versions Python figées** (`==`) dans `requirements.txt` et `requirements-dev.txt`. Une version sans borne haute a cassé le démarrage en production (SQLAlchemy 2.1.8 installé à la place de 2.0). Monter une version passe par une PR, avec la CI verte.

### 5.2 Adresse du visiteur derrière les proxys (US-024)

Les limites de débit (envois de pièces, consultations de dossier, connexion, contact) comptent par adresse de visiteur (`adresse_client`, `backend/api/v1/limiteur.py`). En production, la chaîne est :

```
visiteur → Apache UEH (TLS, *.ueh.edu.ht) → Nginx du conteneur frontend → FastAPI
```

- **Chaque proxy ajoute à droite de `X-Forwarded-For`** l'adresse de qui l'a contacté. FastAPI reçoit donc `[ce que le visiteur a inventé…], visiteur, Apache`. L'adresse retenue est la N-ième entrée **en partant de la droite**, N = `TRUSTED_PROXY_COUNT`. Ne jamais lire la première entrée : le visiteur la choisit, et pourrait ainsi contourner toutes les limites.
- **`TRUSTED_PROXY_COUNT`** : `0` sans proxy (uvicorn lancé directement), `1` (par défaut) avec le seul Nginx du conteneur, `2` derrière l'Apache UEH. Trop haut, un visiteur peut inventer son adresse ; trop bas, tous les visiteurs partagent l'adresse d'Apache et la limite de 20 consultations par minute bloque tout le monde.
- **Nginx** (`frontend/nginx.conf`) transmet `X-Forwarded-For $proxy_add_x_forwarded_for` : il ajoute l'adresse d'Apache sans retirer ce qui précède. À ne pas remplacer par `$remote_addr`, qui effacerait l'adresse du visiteur.
- **Apache UEH** doit transmettre `X-Forwarded-For`. `mod_proxy` le fait par défaut avec `ProxyPass`, à condition de ne pas mettre `ProxyAddHeaders Off`. Configuration attendue :
  ```
  ProxyPass        / http://<VM>:5000/
  ProxyPassReverse / http://<VM>:5000/
  LimitRequestBody 6291456
  ```
  Vérifié le 2026-11-04 dans les journaux Nginx de la VM : les requêtes passées par Apache portent bien l'adresse publique du visiteur.
- **Limite connue** : un accès direct au port de la VM, sans passer par Apache, ne traverse qu'un proxy. L'entrée la plus à gauche, ajoutée par Nginx, est alors retenue. Un visiteur du réseau local qui envoie son propre `X-Forwarded-For` sur ce port peut donc choisir son adresse. Le port n'est pas censé être joignable depuis Internet autrement que par Apache.

---

*ws-tech-01-portail-public.md — FDS Portail — Bravetech · GL-EN3-2026*
