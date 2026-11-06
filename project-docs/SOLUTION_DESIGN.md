---
created: 2026-09-26T00:18:00Z
updated: 2026-11-06T04:11:35Z
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

FDS Portail est un **monolithe modulaire** déployé en deux images Docker coordonnées, sur une VM de la Faculté (Proxmox, ADR-006) :
- Un **frontend React/Vite** (SPA) servi par Nginx, qui relaie aussi `/api/` vers le backend.
- Un **backend FastAPI**, connecté à PostgreSQL (conteneur sur la même VM), au stockage des pièces (volume local, ADR-007) et à Resend (email).

*Corrigé le 2026-11-05 (US-026) : ce paragraphe décrivait Vercel et Railway, abandonnés au profit de la VM Proxmox (ADR-006, ADR-009).*

Le flux de bout en bout : le candidat accède au frontend via HTTPS → le frontend appelle le backend via REST JSON → le backend lit/écrit dans PostgreSQL, range les pièces sur un volume Docker de la VM (ADR-007) et délègue les emails à Resend. L'administrateur passe par le même frontend mais ses routes sont protégées par JWT.

```
Candidat / Admin
      │ HTTPS
      ▼
 [Apache UEH — TLS *.ueh.edu.ht]
      │
      ▼
 [VM Proxmox FDS — Docker Compose]
   ├── Nginx + React/Vite SPA ── /api/ ──▶ FastAPI
   ├── PostgreSQL (source de vérité)
   ├── Volume des pièces (fichiers)
   └── Resend (emails, service externe)
```

---

## 4. Carte des composants

### 4.1 Frontend (image Nginx sur la VM)
- **Framework :** React 19 + Vite + TypeScript
- **Structure :** Feature-Sliced Design (FSD) — couches `app/`, `pages/`, `features/`, `entities/`, `shared/`
- **Points d'entrée publics :** `/`, `/cursus/:id`, `/postuler`, `/suivi`, `/histoire`, `/contact`, `/suivi/:reference`, `/admin/login`, `/admin` (dossiers), `/admin/candidatures/:reference`
- **État serveur :** TanStack Query (cache, retry, invalidation)
- **État client :** Zustand (formulaire multi-étapes en cours)

### 4.2 Backend (image FastAPI sur la VM)
Organisé selon la **Clean Architecture** (`_ARCHITECTURE_EXPLAINED.md`, Partie 1) :

| Couche | Dossier | Contenu |
|---|---|---|
| Domain | `entities/` | `Candidat`, `Candidature`, `DocumentSoumis`, `DecisionDocument`, `Utilisateur`, pièces d'admission — dataclasses pures, zéro dépendance externe |
| Application | `bll/` + `ports/` | Cas d'utilisation (`EnregistrerInformationsUseCase`, `SimulerPaiementUseCase`, `TeleverserDocumentUseCase`, `SoumettreCandidatureUseCase`, `ObtenirStatutCandidatureUseCase`, `RemplacerDocumentUseCase`, `DeciderDocumentUseCase`…) + ports (`ICandidatureRepository`, `IDocumentRepository`, `IStockageFichiers`, `IEmailSender`, `IUtilisateurRepository`, `IEmetteurJeton`, `IHacheurMotDePasse`) |
| Infrastructure | `dal/` | `SqlCandidatureRepository`, `SqlDocumentRepository`, `SqlUtilisateurRepository`, `StockageLocal`, `ResendEmailSender` / `ConsoleEmailSender`, `EmetteurJwt`, `HacheurBcrypt`, `JsonCursusRepository`, migrations Alembic |
| Presentation | `api/v1/` | Routers FastAPI, Pydantic DTOs, middleware, injection de dépendances |

**Points d'entrée REST** (liste complète et à jour : `/docs`, OpenAPI généré par FastAPI) :

| Route | Accès |
|---|---|
| `GET /api/v1/cursus`, `GET /api/v1/cursus/{id}` | Public |
| `POST /api/v1/candidatures` puis, sur `/api/v1/candidatures/{id}` : `GET`, `PUT …/informations`, `PUT …/deplacement-physique`, `POST …/paiement`, `GET …/documents`, `POST …/documents/{piece}`, `POST …/soumission` | Public (identifiant du brouillon) |
| `GET /api/v1/candidatures/{reference}/statut`, `POST …/{reference}/pieces/{piece}/remplacement` | Public (référence `CAN-AAAA-NNNN`), débit limité |
| `POST /api/v1/contact`, `GET /api/v1/sante` | Public |
| `POST /api/v1/auth/token` | Public (connexion du personnel) |
| `/api/v1/admin/…` : `moi`, `candidatures` (liste, `export`, `{reference}`), `proxy-document/{id}`, `documents/{id}/statut` | JWT (admin ou agent), posé sur tout le routeur |

### 4.3 Services externes
| Service | Rôle | Interface locale |
|---|---|---|
| **PostgreSQL (conteneur sur la VM)** | Source de vérité | SQLAlchemy 2.x via `dal/`, schéma par migrations Alembic (US-023) |
| **Volume Docker `bravetech_uploads_data` (sur la VM)** | Stockage des pièces (ADR-007) | `IStockageFichiers` → `StockageLocal` ; lecture par le personnel via `proxy-document` |
| **Resend** | Email transactionnel | `IEmailSender` → `ResendEmailSender` (`ConsoleEmailSender` sans clé) |

---

## 5. Stack technique

| Partie | Technologie | Raison |
|---|---|---|
| Frontend | React 19 / Vite / TypeScript | SPA Mobile-First, typage fort, HMR rapide, écosystème FSD |
| Backend | FastAPI 0.x / Python 3.11+ | Async natif, OpenAPI auto-généré, Pydantic v2 |
| Base de données | PostgreSQL 15 | ACID, intégrité référentielle stricte, index B-Tree |
| ORM | SQLAlchemy 2.x | Requêtes paramétrées (anti-injection), migrations Alembic |
| Auth | PyJWT (JWT HS256) + bcrypt | Bibliothèques éprouvées, hachage sécurisé |
| Stockage fichiers | Volume Docker sur la VM (ADR-007) | Aucune clé externe, fichiers servis seulement par le proxy authentifié ; Cloudinary reste possible derrière le même port |
| Email | Resend (API REST) | Notifications transactionnelles non bloquantes |
| Déploiement | Docker Compose sur la VM Proxmox de la FDS (ADR-006) | Images construites par GitHub Actions, publiées sur GHCR, déployées par SSH à chaque fusion sur `master` (ADR-009, US-026) |
| Secrets | `.env` hors repo + `.gitignore` | Anti-fuite de clés |
| Tests | pytest + httpx (backend), `node --test` (frontend) ; radon + coverage pour le score CRAP | Architecture + unitaires + intégration |

**Aucun emplacement réservé dans cette stack** — tous les choix sont des décisions réelles déjà validées par l'équipe (cf. cahier des charges §11).

---

## 6. Couche de données

**Deux sources de données selon la nature de l'information :**
1. **Fichiers JSON (`cursus/*.json`) :** Catalogue académique de référence (filières, durée, programmes par niveau). Les pièces requises d'admission, identiques pour tous les candidats, sont définies côté backend et non dans ces fichiers. Données statiques institutionnelles versionnées sous Git, exploitées via `JsonCursusRepository`. Aucune table SQL pour les cursus.
2. **PostgreSQL : Source de vérité unique pour les données transactionnelles et candidates.**
   Les fichiers stockés et les statuts email ne remplacent jamais les données en base — ce sont des effets de bord, pas des états.

### Entités principales (PostgreSQL)

| Entité | Table | Clé |
|---|---|---|
| `Candidat` | `candidats` | `(email, campagne)` (UNIQUE) |
| `Candidature` | `candidatures` | `candidat_id` (UNIQUE), `reference_dossier` (UNIQUE, attribuée à la soumission) |
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
- `get_current_admin` est posé sur **tout le routeur** `/api/v1/admin` (une route ajoutée en hérite) ; rôle et état du compte relus en base à chaque requête. `get_current_admin_complet` réserve une route au rôle `admin` (calendrier d'admission).
- Deny by default : jeton absent, invalide ou expiré → 401 ; rôle insuffisant → 403.

**Rate limiting :** 5 **échecs** de connexion par minute et par adresse sur `POST /api/v1/auth/token`, puis 429 (anti brute-force). Détails : `technical-specs/ws-tech-04-administration.md`.

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

1. **Environnement d'exécution :** Le système tourne au lancement sur une machine virtuelle Linux (Debian/Ubuntu Server) hébergée sur l'hyperviseur Proxmox de la Faculté des Sciences (ADR-006). L'architecture est entièrement conteneurisée via Docker et Docker Compose :
   - `db` : Conteneur PostgreSQL 15 avec volume persistant `postgres_data` ; les pièces sont sur le volume `uploads_data`.
   - `backend` : Conteneur Python 3.11-slim exécutant FastAPI via Uvicorn.
   - `frontend` : Conteneur multi-stage (Node 22 Alpine pour le build Vite, Nginx Alpine pour servir les statiques et faire reverse-proxy vers `/api/`).
2. **Cheminement d'un changement (US-025, US-026, ADR-009) :**
   - Branche, puis pull request vers `master`. La protection de `master` exige les vérifications vertes : backend (`pytest`, dont `test_architecture.py`), frontend (`tsc -b`, lint sans avertissement, tests, `vite build`) et GitGuardian.
   - Fusion sur `master` → `.github/workflows/deploy.yml` construit les images `bravetech-backend` et `bravetech-frontend`, les publie sur GHCR (étiquette = commit), puis se connecte à la VM par SSH.
   - Sur la VM, `deploy/deploy.sh` copie la base, lance `docker-compose.prod.yml` avec ces images (les migrations Alembic passent au démarrage du backend), vérifie `/api/v1/sante` et revient à la version précédente en cas d'échec.
3. **Exposition :** l'Apache de l'UEH porte le TLS (`*.ueh.edu.ht`) et relaie vers le port du portail sur la VM. Détails techniques : `technical-specs/ws-tech-01-portail-public.md` §5.

*Corrigé le 2026-11-05 (US-026) : cette section décrivait Vercel et Railway. Le 2026-11-06, le document figurait deux fois (le gabarit du kit à la suite) : fusionné en un seul.*

---

## 12. Hypothèses

| Hypothèse | Conséquence si fausse |
|---|---|
| Le volume de candidatures reste < 500 en V1 | Pool PostgreSQL (5+10 connexions) insuffisant → augmenter les ressources de la VM |
| La VM Proxmox de la FDS et son alimentation restent disponibles | Indisponibilité pendant la période d'inscription → perte de candidatures (sauvegardes hors site : US-027) |
| Les candidats ont accès à un email valide | Le système de suivi par référence + email devient inutilisable → ajouter un canal SMS |
| Le volume des pièces sur la VM survit aux redéploiements | Pièces perdues alors que la base les référence → nom de projet Compose fixe (`bravetech`), sauvegardes hors site (US-027) |
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

*Les entrées ne sont jamais supprimées, seulement marquées remplacées, avec une date et une raison. ADR-010 et ADR-011 : décisions du 2026-09-26 qui figuraient sous les numéros 002 et 003 d'un second tableau en double ; renumérotées le 2026-11-06, à la fusion des deux tableaux.*

| # | Décision | Alternative rejetée | Raison | Statut |
|---|---|---|---|---|
| ADR-001 | Monolithe Modulaire | Microservices | Équipe < 5 personnes, MVP, complexité opérationnelle non justifiée. Les modules Clean Arch facilitent une migration future. | Accepté |
| ADR-002 | REST (Contract-First, OpenAPI) | GraphQL | CRUD classique, pas d'over-fetching problématique, OpenAPI auto-généré par FastAPI, cache HTTP natif sur GET. | Accepté |
| ADR-003 | Clean Architecture (Domain / Application / Infrastructure / Presentation) | MVC | Logique métier testable sans DB, remplacement de services externes sans impact domaine, structure explicite pour l'onboarding. | Accepté |
| ADR-004 | Cloudinary pour le stockage fichiers | S3 / MinIO auto-hébergé | Pas d'infrastructure propre à gérer, URLs signées, SDK simple. Isolé derrière un port. | Remplacé par ADR-007 (2026-09-27) : aucun adaptateur Cloudinary n'a été écrit |
| ADR-005 | Resend pour l'email transactionnel | SendGrid / SMTP propre | API REST simple, bonne délivrabilité, SDK Python. Isolé derrière `IEmailSender`. | Accepté |
| ADR-006 | Déploiement conteneurisé (Docker Compose / Proxmox) | Dépendance exclusive à un PaaS propriétaire | Hébergement souverain sur l'infrastructure Linux de la faculté des sciences via Proxmox avec portabilité immédiate | Accepté (2026-09-26) |
| ADR-007 | Stockage des pièces derrière un port `IStockageFichiers`, avec un volume local persistant par défaut ; Cloudinary reste un adaptateur optionnel | Cloudinary obligatoire (ADR-004 seul) | Autonomie sur la VM Proxmox (ADR-006) et développement sans clé d'API externe. Le port permet d'ajouter Cloudinary sans toucher au métier. Arbitrage de l'Epic 2 (Q1) ; adaptateur local livré avec US-007 (2026-11-01), adaptateur Cloudinary non écrit | Accepté (2026-09-27) |
| ADR-008 | Admission unique au MPC : la candidature ne porte ni `cursus_slug` ni filière ; les pièces requises forment une liste unique de 5 | Une candidature par cursus, avec pièces variables selon le cursus (modèle initial : `UNIQUE (email, cursus_slug, campagne)`) | Règle institutionnelle (2026-10-31) : tout candidat entre en MPC (2 ans), puis choisit sa branche (3 ans) hors du portail. Un champ cursus à la candidature serait trompeur et obligerait à le migrer. Contrainte d'unicité : `(email, campagne)`. Voir `reviews/01-admission-unique-mpc.md` | Accepté (2026-10-31) |
| ADR-009 | Déploiement continu : images construites par GitHub Actions, publiées sur GHCR (publiques), déployées par SSH avec une clé limitée à `deploy/deploy.sh` (`command=`) ; contrôle `/api/v1/sante` et retour automatique à la version précédente | Runner GitHub Actions auto-hébergé sur la VM ; Dokploy ; construction des images sur la VM | Dépôt public : un runner sur la VM exécuterait le code d'un fork (E5-4). Dokploy ajoute une couche pour un seul portail (E5-3). Construire sur la VM charge la machine de production et rend chaque version non reproductible. Images publiques : elles ne contiennent que le code déjà public, et la VM n'a aucun jeton à garder. Limite acceptée : si le port SSH est un jour fermé à Internet, GitHub ne pourra plus déployer (E5-5) | Accepté (2026-11-05) |
| ADR-010 | PostgreSQL comme source unique de vérité | NoSQL (MongoDB) | Intégrité référentielle stricte, transactions ACID pour les candidatures | Accepté (2026-09-26) |
| ADR-011 | Authentification sans état par JWT | Sessions serveur (cookies) | Compatible avec une SPA mobile, aucun état de session sur le serveur | Accepté (2026-09-26) |

---

## 15. Questions ouvertes

| Question | Bloquante ? | Qui / Quand |
|---|---|---|
| Conformité légale haïtienne sur les données personnelles (consentement, responsable légal) | Non pour le lancement technique | FDS-UEH — avant mise en production publique |
| Création des comptes agents : le premier admin est créé par `backend/scripts/seed_admin.py` (US-011, résolu pour le lancement) ; aucun écran de gestion des comptes | Non | Équipe Bravetech / FDS SYS — post-MVP |
| Test de restauration de la sauvegarde PostgreSQL de la VM (US-027) | Non (RPO/RTO documentés, test non effectué) | Équipe Bravetech — avant la période d'inscription |
| Monitoring automatique (alertes 5xx) | Non pour le MVP | Post-MVP — intégrer Uptime Robot ou équivalent |

---

*SOLUTION_DESIGN.md — FDS Portail — Bravetech · GL-EN3-2026*
