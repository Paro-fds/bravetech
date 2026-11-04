---
created: 2026-11-04T15:40:00Z
updated: 2026-11-04T15:33:51Z
status: open
---

# epic-005-refinement.md — Mise en production

> **Ce fichier est la source de vérité des règles en cours pour epic-005.** Il est vidé à la clôture de l'Epic : chaque règle part dans son document propriétaire (`SOLUTION_DESIGN.md` ADR, `NFR.md`, spec tech).

---

## 1. Scope de l'Epic 5

Mettre le portail en ligne sur l'infrastructure de la FDS, de façon reproductible et sans perte de données :

- **Base de données** : migrations versionnées (Alembic) — `create_all` ne modifie jamais une table existante.
- **Sécurité derrière les proxys** : le limiteur de requêtes lit l'adresse réelle du visiteur sans qu'il puisse l'inventer.
- **CI** : vérifications du frontend (tsc, oxlint, tests, build) à chaque pull request.
- **CD** : images construites sur GitHub, publiées sur GHCR, déployées sur la VM par SSH à chaque fusion sur `master`.
- **Exploitation** : sauvegardes hors de la VM, restauration testée, procédure écrite.

**Ce que cet Epic ne couvre PAS :** la configuration de l'Apache de l'UEH et du routeur Meraki (service réseau de la faculté, voir §3), la surveillance avancée (métriques, alertes), toute nouvelle fonctionnalité.

---

## 2. Découvertes (2026-11-04)

| ID | Constat | Statut |
|---|---|---|
| E5-1 | Cible : une VM Ubuntu 26.04 sur le Proxmox de la FDS (4 vCPU, 7,3 Go RAM, 70 Go libres), administrée en SSH. Adresse et port d'administration : hors du dépôt (dépôt public), dans les secrets GitHub et la documentation privée de l'équipe. | ✅ Constaté |
| E5-2 | `dorfilus.ueh.edu.ht` : un Apache de l'UEH en amont porte le certificat `*.ueh.edu.ht` (RapidSSL, expire le 2027-02-28) et renvoie aujourd'hui vers une autre application de la VM. Le port 80 public répond par une erreur au lieu de rediriger vers HTTPS. Le HTTPS est donc assuré en amont, pas sur la VM. | ✅ Constaté (déduit des en-têtes) |
| E5-3 | Dokploy est installé sur la VM (son Traefik occupe 80/443). Pour un seul portail, il n'apporte pas assez : déploiement en **Docker Compose seul**, à côté, sur un autre port (variable `PORT` déjà prévue). Désinstaller Dokploy reste une question ouverte. | ✅ Décidé avec le Project Owner |
| E5-4 | Le dépôt GitHub est **public** : pas de runner GitHub Actions auto-hébergé sur la VM (un fork pourrait y exécuter du code). Le déploiement passe par SSH depuis GitHub, avec une clé dédiée limitée à un script (`command=`). | ✅ Décidé |
| E5-5 | Si le port SSH est un jour restreint aux adresses de la faculté, GitHub ne pourra plus s'y connecter : il faudra que la VM tire elle-même les nouvelles images. | ⚠️ Risque accepté |
| E5-6 | `backend/main.py` crée les tables avec `create_all` : aucune évolution de schéma ne s'applique sur une base existante. | ❌ Bloquant → US-023 |
| E5-7 | `adresse_client` (`backend/api/v1/limiteur.py`) prend le **premier** élément de `X-Forwarded-For`, que le visiteur peut inventer ; sans en-tête transmis par l'Apache UEH, tous les visiteurs partagent une adresse et le limiteur de suivi (20 requêtes) bloque tout le monde. | ❌ Bloquant → US-024 |
| E5-8 | `ci.yml` ne lance que les tests Python : le frontend n'est vérifié qu'à la main. | ⚠️ → US-025 |
| E5-9 | Démonstration (2026-11-04) : le dépôt est cloné sur la VM et lancé à la main (`docker compose up -d --build`, emails désactivés). Le port 8080 était déjà pris par un autre service : le portail écoute sur un autre port. Le bug du pilote PostgreSQL (US-023) est contourné par un `docker-compose.override.yml` non versionné. | ✅ En cours |

---

## 3. Dépendances externes (service réseau de la faculté)

- Apache UEH : renvoyer `dorfilus.ueh.edu.ht` vers la VM, port du portail, en transmettant `Host`, `X-Forwarded-For` et `X-Forwarded-Proto: https`.
- Apache UEH : accepter des corps de requête de **6 Mo** (pièces ≤ 5 Mo).
- Port 80 public : redirection vers `https://` au lieu de l'erreur 500.
- DNS `ueh.edu.ht` : enregistrements SPF/DKIM pour Resend (sinon aucun email n'atteint les candidats).
- Renouvellement du certificat `*.ueh.edu.ht` avant le 2027-02-28.

---

## 4. Découpage des User Stories

| Story | Titre | Dépend de |
|---|---|---|
| US-023 | Migrations de base de données avec Alembic | — |
| US-024 | Adresse réelle du visiteur derrière les proxys | — |
| US-025 | Vérifications du frontend en CI | — |
| US-026 | Déploiement continu vers la VM de la FDS | US-023, US-025 |
| US-027 | Sauvegardes hors site et procédure d'exploitation | US-026 |

**Ordre de build recommandé :** US-023 → US-024 → US-025 → US-026 → US-027.
