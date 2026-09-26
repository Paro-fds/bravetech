---
created: 2026-09-26T00:18:00Z
updated: 2026-09-26T00:18:00Z
---

# SOLUTION_DESIGN.md — FDS Portail

**Réponses :** Comment ce système est-il construit ? En quels Workstreams se décompose-t-il ?
**Dépend de :** `PRD.md` + `NFR.md`.

---

## 1. Objectif et périmètre

**Ce document décide :**
- La décomposition du système en Workstreams (zones fonctionnelles indépendantes).
- L'architecture interne du backend (Clean Architecture — 4 couches).
- La stack technique retenue et les raisons de chaque choix.
- Le modèle de données canonique (source de vérité : PostgreSQL).
- Le flux d'authentification et d'autorisation.
- La stratégie de déploiement (Docker Compose sur infrastructure Proxmox Linux FDS — ADR-006).
- Les ADRs structurants.

**Hors périmètre de ce document :**
- Les décisions produit (périmètre fonctionnel, priorisation MoSCoW) → `PRD.md`.
- Les barres de qualité (performance, disponibilité, sécurité) → `NFR.md`.
- L'ordre de construction et les Epics → `PLAN.md`.
- Les user stories détaillées → `project-docs/functional-specs/`.

---

## 2. Workstreams — définition canonique `WS-NN`

Cinq zones fonctionnelles indépendantes, chacune pouvant évoluer sans bloquer les autres :

| ID | Nom | Responsabilité |
|---|---|---|
| **WS-01** | Portail public | Pages de présentation des cursus, FAQ, contacts. Lecture seule, aucune authentification. |
| **WS-02** | Candidature | Formulaire multi-étapes (infos personnelles → simulation paiement → upload → soumission). Génération de la référence `CAN-XXXX`. |
| **WS-03** | Suivi de dossier | Page de tracking par référence. Barre de progression. Remplacement d'un document rejeté. |
| **WS-04** | Administration | Tableau de bord admin (liste des dossiers, validation/rejet de documents, audit). Accès JWT uniquement. |
| **WS-05** | Notifications | Emails transactionnels (confirmation, validation, rejet) via Resend. Non bloquant pour le flux principal. |

**Indépendance :** WS-01 peut être livré seul (vitrine statique). WS-02 dépend de WS-05 pour la confirmation mais ne le bloque pas. WS-04 dépend de WS-02 (il n'y a rien à administrer sans candidatures). WS-03 dépend de WS-02 (pas de suivi sans dossier créé).

---

## 3. Vue d'ensemble du système

FDS Portail est un **monolithe modulaire** déployé en deux artefacts coordonnés :
- Un **frontend React/Vite** (SPA) hébergé sur Vercel.
- Un **backend FastAPI** hébergé sur Railway, connecté à PostgreSQL (Railway) et aux services externes Cloudinary (stockage) et Resend (email).

Le flux de bout en bout : le candidat accède au frontend via HTTPS → le frontend appelle le backend via REST JSON → le backend lit/écrit dans PostgreSQL, délègue les fichiers à Cloudinary et les emails à Resend. L'administrateur passe par le même frontend mais ses routes sont protégées par JWT.

```
Candidat / Admin
      │ HTTPS
      ▼
 [Vercel — React/Vite SPA]
      │ REST JSON
      ▼
 [Railway — FastAPI]
   ├── PostgreSQL (source de vérité)
   ├── Cloudinary (fichiers)
   └── Resend (emails)
```

---

## 4. Carte des composants

### 4.1 Frontend (Vercel)
- **Framework :** React 19 + Vite + TypeScript
- **Structure :** Feature-Sliced Design (FSD) — couches `app/`, `pages/`, `features/`, `entities/`, `shared/`
- **Points d'entrée publics :** `/`, `/cursus/:id`, `/postuler`, `/suivi`, `/contact`, `/admin/login`, `/admin/dashboard`
- **État serveur :** TanStack Query (cache, retry, invalidation)
- **État client :** Zustand (formulaire multi-étapes en cours)

### 4.2 Backend (Railway — FastAPI)
Organisé selon la **Clean Architecture** (`_ARCHITECTURE_EXPLAINED.md`, Partie 1) :

| Couche | Dossier | Contenu |
|---|---|---|
| Domain | `entities/` | `Candidat`, `DocumentSoumis`, `DocumentRequis` — dataclasses pures, zéro dépendance externe |
| Application | `bll/` + `ports/` | Use cases (`SoumettreCandidature`, `ValiderDocument`, `RemplacerDocument`, `SuivreDossier`) + interfaces abstraites (`ICandidatRepository`, `IStorageService`, `IEmailService`) |
| Infrastructure | `dal/` | `CandidatRepositorySQLAlchemy`, `CloudinaryStorageAdapter`, `ResendEmailAdapter`, `JWTAuthAdapter` |
| Presentation | `api/v1/` | Routers FastAPI, Pydantic DTOs, middleware, injection de dépendances |

**Points d'entrée REST :**

| Méthode | Route | Accès |
|---|---|---|
| `GET` | `/api/v1/cursus` | Public |
| `GET` | `/api/v1/documents-requis` | Public |
| `POST` | `/api/v1/candidature` | Public |
| `POST` | `/api/v1/upload` | Public |
| `GET` | `/api/v1/candidature/{ref}` | Public |
| `POST` | `/api/v1/auth/token` | Public |
| `GET` | `/api/v1/admin/candidatures` | JWT admin |
| `PUT` | `/api/v1/admin/documents/{id}/statut` | JWT admin |
| `GET` | `/api/v1/admin/proxy-document` | JWT admin |

### 4.3 Services externes
| Service | Rôle | Interface locale |
|---|---|---|
| **PostgreSQL (Railway)** | Source de vérité | SQLAlchemy 2.x via `dal/` |
| **Cloudinary** | Stockage fichiers | `IStorageService` → `CloudinaryStorageAdapter` |
| **Resend** | Email transactionnel | `IEmailService` → `ResendEmailAdapter` |

---

## 5. Stack technique

| Partie | Technologie | Raison |
|---|---|---|
| Frontend | React 19 / Vite / TypeScript | SPA Mobile-First, typage fort, HMR rapide, écosystème FSD |
| Backend | FastAPI 0.x / Python 3.11+ | Async natif, OpenAPI auto-généré, Pydantic v2 |
| Base de données | PostgreSQL 15 | ACID, intégrité référentielle stricte, index B-Tree |
| ORM | SQLAlchemy 2.x | Requêtes paramétrées (anti-injection), migrations Alembic |
| Auth | python-jose (JWT HS256) + passlib (bcrypt) | Lib éprouvée, hash sécurisé |
| Stockage fichiers | Cloudinary | Upload sécurisé, URL signée, sans infra propre |
| Email | Resend (API REST) | Notifications transactionnelles non bloquantes |
| Frontend deploy | Vercel | CDN global, HTTPS automatique, preview par PR |
| Backend deploy | Railway (PaaS) | CI/CD depuis GitHub, stateless, PostgreSQL intégré |
| Secrets | `.env` hors repo + `.gitignore` | Anti-fuite de clés |
| Tests | pytest + pytest-asyncio | Architecture + unitaires + intégration |

**Aucun emplacement réservé dans cette stack** — tous les choix sont des décisions réelles déjà validées par l'équipe (cf. cahier des charges §11).

---

## 6. Couche de données

**Deux sources de données selon la nature de l'information :**
1. **Fichiers JSON (`cursus/*.json`) :** Catalogue académique de référence (cursus, programmes semestriels, pièces justificatives requises). Données statiques institutionnelles versionnées sous Git, exploitées via `JsonCursusRepository`. Aucune table SQL pour les cursus.
2. **PostgreSQL : Source de vérité unique pour les données transactionnelles et candidates.**
   Les URLs Cloudinary et les statuts email ne remplacent jamais les données en base — ce sont des effets de bord, pas des états.

### Entités principales (PostgreSQL)

| Entité | Table | Clé |
|---|---|---|
| `Candidat` | `candidats` | `reference_dossier` (UNIQUE) |
| `DocumentSoumis` | `documents_soumis` | `(candidat_id, document_type)` (UNIQUE) |
| `Utilisateur` | `utilisateurs` | `email` (UNIQUE) — consommé depuis FDS SYS |

### Contrat critique
- `DocumentSoumis.statut_validation` ∈ `{en_attente, valide, rejete}` — alimente la barre de progression.
- `candidats.deplacement_physique` ∈ `{true, false, NULL}` — mesure de l'hypothèse §3.4.
- Contrainte UNIQUE `(candidat_id, document_type)` → upsert sans doublon lors d'un remplacement.
- `valide_par` + `date_validation` → audit immuable de chaque décision admin.

Schéma SQL complet : `cahier_des_charges.md §9.3`.

---

## 7. Flux d'authentification et d'autorisation

**Applicable — les routes admin sont protégées.**

**AuthN (Qui es-tu ?) :**
1. `POST /api/v1/auth/token` — email + mot de passe.
2. Le backend vérifie le hash bcrypt contre `utilisateurs.mot_de_passe_hash`.
3. Retourne un JWT HS256 (durée 60 min, payload : `sub=user_id`, `role`).

**AuthO (Qu'as-tu le droit de faire ?) :**
- RBAC — `Utilisateur.role` ∈ `{admin, agent}`.
- `get_current_admin()` est appelé à **chaque endpoint admin** — pas seulement à la connexion.
- Deny by default : toute exception dans le contrôle d'accès → 403 Forbidden.

**Rate limiting :** 5 requêtes / 60s sur `POST /api/v1/auth/token` (anti brute-force).

**Refresh tokens :** non implémentés en MVP — l'admin se reconnecte après 60 min. Prévu en post-MVP (`POST /api/v1/auth/refresh`).

---

## 8. Architecture temps réel / interactive

**Non applicable en MVP.**
Les notifications (validation, rejet) sont asynchrones par email — pas de WebSocket, pas de Server-Sent Events. Le candidat consulte son statut en interrogeant `GET /api/v1/candidature/{ref}` (polling manuel). WebSockets serait surdimensionné pour des notifications différées.

---

## 9-10. Boucle de mise à jour automatique

**Applicable — limitée à un seul cas.**
L'envoi d'email est déclenché automatiquement par deux événements métier : soumission de candidature et décision admin sur un document. Le déclencheur est synchrone dans le handler FastAPI mais l'envoi est non bloquant (une erreur Resend ne fait pas échouer la requête principale).

Pas de boucle autonome, pas de tâche planifiée, pas de risque de runaway en MVP.

---

## 11. Vue d'ensemble du déploiement

**Aujourd'hui (développement) :** local (`npm run dev` + `uvicorn --reload`), base de données SQLite ou PostgreSQL local, variables `.env`.

**Au lancement (production) :**

| Composant | Hébergement | Pipeline |
|---|---|---|
| Frontend | Vercel | Push sur `main` → build Vite → déploiement CDN automatique |
| Backend | Railway | Push sur `main` → build Docker → déploiement stateless automatique |
| Base de données | Railway PostgreSQL | Provisionnée dans le même projet Railway, backups quotidiens |

**Chemin d'un changement local jusqu'en prod :**
1. Développement en branche feature.
2. Pull Request → review → merge sur `main`.
3. GitHub Actions (ou Railway/Vercel hooks) : tests pytest (`test_architecture`, unitaires, intégration) + build.
4. Si tout est vert → déploiement automatique.

**CI/CD en MVP :** validation minimale — `pytest tests/` + build Vite. Pas de staging environment dédié en V1.

---

## 12. Hypothèses

| Hypothèse | Conséquence si fausse |
|---|---|
| Le volume de candidatures reste < 500 en V1 | Pool PostgreSQL (5+10 connexions) insuffisant → scale up Railway immédiat |
| Railway PostgreSQL est fiable à 99 % | Indisponibilité pendant la période d'inscription → perte de candidatures |
| Les candidats ont accès à un email valide | Le système de suivi par référence + email devient inutilisable → ajouter un canal SMS |
| Cloudinary maintient son API stable | `CloudinaryStorageAdapter` à réécrire → isolé derrière `IStorageService`, coût limité |
| FDS SYS fournit les comptes administrateurs avant le lancement | Besoin d'une procédure manuelle de création de compte si ce n'est pas le cas |

**Hypothèse dont la fausseté imposerait une refonte :** si le candidat a besoin d'un compte complet (pas seulement une référence), le modèle d'accès public de WS-02 et WS-03 est à repenser en profondeur.

---

## 13. Hors périmètre architectural V1

| Élément exclu | Raison | Workstream futur |
|---|---|---|
| Transactions monétaires réelles (MonCash/NatCash) | Déléguées à FDS Pay — module séparé | WS-02 (intégration Webhook) |
| SSO institutionnel complet (FDS SYS) | Architecturalement préparé, non livré | WS-04 (auth) |
| Cache Redis (Cache-Aside) | Non justifié au volume MVP | WS-01 / WS-02 |
| Refresh tokens | MVP : reconnexion après 60 min acceptable | WS-04 (auth) |
| Notifications SMS | Should Have — non bloquant pour le lancement | WS-05 |
| Microservices | Équipe < 5 personnes, domaine en MVP — les ports Clean Arch préparent cette extraction | Post-MVP |

---

## 14. Registres de décisions d'architecture (ADR)

| # | Décision | Alternative rejetée | Raison | Statut |
|---|---|---|---|---|
| ADR-001 | Monolithe Modulaire | Microservices | Équipe < 5 personnes, MVP, complexité opérationnelle non justifiée. Les modules Clean Arch facilitent une migration future. | Accepté |
| ADR-002 | REST (Contract-First, OpenAPI) | GraphQL | CRUD classique, pas d'over-fetching problématique, OpenAPI auto-généré par FastAPI, cache HTTP natif sur GET. | Accepté |
| ADR-003 | Clean Architecture (Domain / Application / Infrastructure / Presentation) | MVC | Logique métier testable sans DB, remplacement de services externes sans impact domaine, structure explicite pour l'onboarding. | Accepté |
| ADR-004 | Cloudinary pour le stockage fichiers | S3 / MinIO auto-hébergé | Pas d'infrastructure propre à gérer, URLs signées, SDK simple. Isolé derrière `IStorageService`. | Accepté |
| ADR-005 | Resend pour l'email transactionnel | SendGrid / SMTP propre | API REST simple, bonne délivrabilité, SDK Python. Isolé derrière `IEmailService`. | Accepté |

---

## 15. Questions ouvertes

| Question | Bloquante ? | Qui / Quand |
|---|---|---|
| Conformité légale haïtienne sur les données personnelles (consentement, responsable légal) | Non pour le lancement technique | FDS-UEH — avant mise en production publique |
| Procédure de création des comptes admin si FDS SYS n'est pas prêt | Oui si aucun admin n'existe au lancement | Équipe Bravetech — sprint pré-lancement |
| Test de restauration du backup Railway PostgreSQL | Non (RPO/RTO documentés, test non effectué) | Équipe Bravetech — avant la période d'inscription |
| Monitoring automatique (alertes 5xx) | Non pour le MVP | Post-MVP — intégrer Uptime Robot ou équivalent |

---

*SOLUTION_DESIGN.md — FDS Portail — Bravetech · GL-EN3-2026*


---

## 1. Objectif et périmètre

> 1. Qu'est-ce que ce document est responsable de décider sans qu'un autre document décide à sa place ?
> 2. Qu'est-ce qui est explicitement hors de sa portée (par exemple, les décisions produit appartiennent au PRD) ?

*(À rédiger)*

## 2. Workstreams — définition canonique de `WS-NN`

> **Rappel de vocabulaire (générique, indépendant du produit — voir aussi `GLOSSARY.md` § Workstream, Epic et Milestone) :**
> - **Workstream** = *quelle zone fonctionnelle*. Ne finit jamais, peut être revisité par un Epic ultérieur. Identifiant : `WS-NN` (deux chiffres).
> - **Epic** = *quand, et à quel volume à la fois*. Étape de construction séquentielle et cadrée dans le temps. Identifiant : `epic-NNN-name`.
> - **Milestone** = *ce qui est livré*. La représentation native GitHub d'un Epic, pas un concept séparé.
>
> Les Workstreams sont définis ici ; les Epics (qui regroupent les Workstreams dans le temps) sont définis ensuite dans `PLAN.md`.

> 1. Quelles sont les zones fonctionnelles indépendantes de ce système, sans tenir compte de l'ordre de construction ?
> 2. Deux Workstreams peuvent-ils être traités par des personnes différentes en même temps sans se marcher dessus ?
> 3. Un Workstream se cache-t-il dans un autre et mérite-t-il son propre identifiant ?

*(À rédiger)*

## 3. Vue d'ensemble du système

> 1. En quelques phrases, comment les éléments majeurs s'assemblent-ils de bout en bout ?
> 2. Quel est le seul diagramme ou flux qui expliquerait le plus vite ce système à un ingénieur junior ?

*(À rédiger)*

## 4. Carte des composants

> 1. Quels sont les composants réellement exécutable/déployables, et que chacun possède-t-il ?
> 2. Quels ports, URLs ou points d'entrée chaque composant expose-t-il ?
> 3. Existe-t-il un composant qui est en réalité deux composants qui se font passer pour un seul ?

*(À rédiger)*

**Avant de répondre à cette section, lis `project-docs/_ARCHITECTURE_EXPLAINED.md`.** Elle propose une structure interne stabilisée pour les deux moitiés d'un projet — un backend structuré en couches (entities / dal / bll / api, avec DTOs et versioning à la frontière) et un frontend en Feature-Sliced Design — ainsi que les conventions de nommage et une stack recommandée, chaque élément accompagné de sa raison et de son coût.

**Traite-la comme une proposition à accepter ou remplacer délibérément, pas comme un défaut à appliquer silencieusement.** Un service utilitaire à point d'entrée unique n'a pas besoin de quatre couches, et l'imposer est une erreur en soi. Quelle que soit ta décision, **consigne-la ici** — c'est précisément ce que cette section est pour, et « on a utilisé le kit » est une bonne réponse tant qu'elle est écrite.

`project-docs/learnings/03-backend-layered-architecture-template.md` contient la réflexion plus longue sur le schéma backend, y compris le compromis quand deux services ont besoin de la même table.

## 5. Stack technique

> 1. Quelle est la pile pour chaque partie majeure du système, et pourquoi ce choix précisément ?
> 2. Y a-t-il une pièce de la stack qui est un emplacement réservé/une supposition plutôt qu'une décision réelle ?

*(À rédiger)*

## 6. Couche de données

> 1. Où chaque type de donnée vit-il réellement, et sous quelle forme ?
> 2. Quel magasin est la source de vérité si deux magasins peuvent diverger ?
> 3. Quel est le schéma ou contrat, assez précisément pour éviter qu'une implémentation et une autre ne dérivent ?

*(À rédiger)*

## 7. Flux d'authentification et d'autorisation *(Conditionnelle — ignorer s'il n'y a aucun contrôle d'accès)*

> 1. Étape par étape, comment quelqu'un passe-t-il d'anonyme à authentifié puis autorisé pour une action spécifique ?
> 2. Qu'est-ce qui est émis (jeton, session, clé), et ce qu'il prouve réellement ?

*(À confirmer : applicable ou ignoré)*

## 8. Architecture temps réel / interactive *(Conditionnelle — ignorer s'il n'y a rien en direct ou en streaming)*

> 1. Qu'est-ce qui doit arriver en temps réel par rapport à ce qui peut être en requête/réponse ?
> 2. Quel est le plan de secours si le canal temps réel tombe en plein milieu d'une interaction ?

*(À confirmer : applicable ou ignoré)*

## 9-10. Boucle de mise à jour automatique ou de retour d'information *(Conditionnelle — ignorer si le contenu/comportement ne change que par modification manuelle)*

> 1. Le système met-il quelque chose à jour automatiquement selon l'usage ou de nouvelles données ? Quel est le déclencheur ?
> 2. Qui valide une modification automatisée avant qu'elle passe en ligne, si quelqu'un le fait ?
> 3. Quel est le pire effet qu'une boucle de mise à jour automatique pourrait provoquer si elle échappe au contrôle ?

*(À confirmer : applicable ou ignoré)*

## 11. Vue d'ensemble du déploiement

1. **Environnement d'exécution :** Le système tourne au lancement sur une machine virtuelle Linux (Debian/Ubuntu Server) hébergée sur l'hyperviseur Proxmox de la Faculté des Sciences (ADR-006). L'architecture est entièrement conteneurisée via Docker et Docker Compose :
   - `db` : Conteneur PostgreSQL 15 avec volume persistant `postgres_data`.
   - `backend` : Conteneur Python 3.11-slim exécutant FastAPI via Uvicorn.
   - `frontend` : Conteneur multi-stage (Node 20 Alpine pour le build Vite, Nginx Alpine pour servir les statiques et faire reverse-proxy vers `/api/`).
2. **Cheminement d'un changement :** 
   - Développement local avec tests unitaires, d'intégration et d'architecture.
   - Push sur la branche `master` / pull request → déclenchement automatique du workflow GitHub Actions (`.github/workflows/ci.yml`).
   - Déploiement sur le serveur cible via `docker compose up -d --build`.
3. **CI/CD :** Pipeline GitHub Actions validant à chaque push l'exécution intégrale des tests pytest (tests unitaires, tests d'intégration API, et tests d'architecture Clean Architecture).

## 12. Hypothèses

> 1. Sur quoi cette conception s'appuie-t-elle sans avoir été vérifiée ?
> 2. Quelle hypothèse, si elle est fausse, imposerait une refonte plutôt qu'un correctif ?

*(À rédiger)*

## 13. Hors périmètre

> 1. Qu'est-ce qui est exclu architecturalement de cette version, et pourquoi ?
> 2. Existe-t-il quelque chose d'exclu ici qu'un Workstream ultérieur devra revoir ?

*(À rédiger)*

## 14. Registres de décisions d'architecture (ADR)

*Générique — réutilise le tableau tel quel. Les entrées ne sont jamais supprimées, seulement marquées `Deprecated` avec une date et une raison.*

| # | Décision | Alternative rejetée | Raison | Statut |
|---|---|---|---|---|
| ADR-001 | Architecture modulaire découplée (Clean Arch + FSD) | Monolithe Django / Rails classique | Découplage strict des règles métier, maintenabilité et testabilité | Accepté (2026-09-26) |
| ADR-002 | PostgreSQL comme source unique de vérité | NoSQL (MongoDB) | Intégrité référentielle stricte, transactions ACID pour les candidatures | Accepté (2026-09-26) |
| ADR-003 | Authentification stateless JWT | Sessions serveur (cookies stateful) | Compatibilité SPA Mobile, scalabilité horizontale et absence d'état serveur | Accepté (2026-09-26) |
| ADR-004 | Stockage des pièces sur Cloudinary | Stockage direct sur disque serveur | URLs signées, mise à l'échelle automatique et absence de gestion de volumes disques locaux | Accepté (2026-09-26) |
| ADR-005 | Emails transactionnels via Resend | Serveur SMTP local (Postfix) | Délivrabilité garantie, API REST asynchrone sans maintenance de serveur mail | Accepté (2026-09-26) |
| ADR-006 | Déploiement conteneurisé (Docker Compose / Proxmox) | Dépendance exclusive à un PaaS propriétaire | Hébergement souverain sur l'infrastructure Linux de la faculté des sciences via Proxmox avec portabilité immédiate | Accepté (2026-09-26) |

> **Questions à se poser, pour chaque nouvelle entrée :**
> 1. Qu'a-t-on décidé qui aurait pu très bien aller dans l'autre sens ?
> 2. Pourquoi l'autre option a-t-elle été rejetée, de façon suffisamment explicite pour que quelqu'un ne la propose pas de nouveau sans le savoir ?

## 15. Questions ouvertes

> 1. Qu'est-ce qui reste réellement non résolu maintenant, sans bloquer le démarrage, mais sans être oublié non plus ?
> 2. Qui ou quoi résoudra chaque question ouverte, et quand ?

*(À rédiger au fur et à mesure)*

---

*SOLUTION_DESIGN.md — [Nom du projet] — structure de départ issue de `project-init-kit/`.*
