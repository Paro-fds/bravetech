---
created: 2026-11-06T04:00:00Z
updated: 2026-11-06T18:04:26Z
---

# Spécification Technique — WS-04 Administration

**Réponses :** Comment l'espace du personnel est-il construit et protégé ?
**Périmètre :** consolidé à la clôture de l'Epic 3 (2026-11-06), d'après US-011 à US-013, US-015, US-028 et US-029. Comportement : [`ws-func-04-administration.md`](../functional-specs/ws-func-04-administration.md).

---

## 1. Authentification et rôles

- **`POST /api/v1/auth/token`** (JSON `email`, `password`) → `AuthentifierUtilisateurUseCase`. Même réponse 401 et même travail bcrypt pour un email inconnu, un mauvais mot de passe ou un compte inactif ; mot de passe > 72 octets refusé. Seuls les **échecs** comptent dans `limiteur_connexion` (5 par minute et par adresse, puis 429 `Retry-After: 60`).
- **Jeton** : JWT HS256 (`EmetteurJwt`, PyJWT), `DUREE_SESSION_MINUTES = 60`, algorithme imposé au décodage (`alg: none`, jeton expiré ou autre secret refusés). `JWT_SECRET` : 32 caractères minimum, **sans valeur par défaut** ; absent → 503 et message dans les journaux.
- **Protection** : `get_current_admin` (rôles `admin`, `agent`) est posé **sur le routeur** `/admin` entier ; un test parcourt le schéma OpenAPI et vérifie que toute route `/admin` refuse l'accès anonyme. `get_current_admin_complet` (rôle `admin` seul) protège `PUT /admin/calendrier`. Rôle et état actif **relus en base à chaque requête** (`ObtenirUtilisateurCourantUseCase`).
- **Seed** : `python -m backend.scripts.seed_admin` avec `ADMIN_SEED_EMAIL`, `ADMIN_SEED_PASSWORD` (≥ 12 caractères) ; idempotent ; le mot de passe n'est jamais affiché ni journalisé.
- **Frontend** : `entities/session` (store Zustand dans `sessionStorage`, `enteteAuth`, `sessionValide`) ; `AdminLayout` renvoie vers la connexion sans session valide ; toute réponse 401 ferme la session.

## 2. Routes `/api/v1/admin`

| Route | Rôle | Notes |
|---|---|---|
| `GET /moi` | admin, agent | |
| `GET /candidatures?page&limit&q&statut&deplacement_physique` | admin, agent | `ListerCandidaturesUseCase` : soumis seulement, filtres et pagination **en mémoire** (`limit` ≤ 100), recherche sans accents ; à passer en SQL au-delà de quelques milliers de dossiers |
| `GET /candidatures/export?format=csv\|pdf` | admin, agent | Déclarée **avant** `/candidatures/{reference}`. CSV `;` + BOM UTF-8 + CRLF, formules neutralisées (`=`, `+`, `-`, `@` préfixés d'une apostrophe) ; PDF reportlab (A4 paysage) ; chaque export journalisé sans donnée personnelle |
| `GET /candidatures/{reference}` | admin, agent | `ObtenirDossierAdminUseCase` ; aucune clé de stockage renvoyée |
| `GET /proxy-document/{document_id}` | admin, agent | `ObtenirContenuDocumentUseCase` ; en-têtes `X-Content-Type-Options: nosniff`, `Content-Security-Policy: sandbox`, `Cache-Control: private, no-store`. Le frontend le lit par `fetch` puis l'affiche depuis une URL locale (une balise `<img>` n'envoie pas l'en-tête d'authentification) |
| `PUT /documents/{document_id}/statut` | admin, agent | Voir §3 ; email en tâche de fond après l'enregistrement (WS-05) |
| `GET /calendrier`, `PUT /calendrier` | lecture : admin, agent ; écriture : admin | ws-tech-01 §6 |
| `GET /utilisateurs`, `POST /utilisateurs` | admin | §5 ; création : 201, 409 email déjà utilisé, 422 |
| `PATCH /utilisateurs/{id}` (`role`, `est_actif`) | admin | §5 ; 404, 409 garde-fous, 422 |
| `PUT /utilisateurs/{id}/mot-de-passe` | admin | §5 ; 404, 422 |

## 3. Décisions et audit

- `DeciderDocumentUseCase` : seule une pièce `en_attente` d'un dossier **soumis** se décide (sinon 404 ou 409) ; motif obligatoire pour un refus (5 à 500 caractères, 422 sinon), aucun motif pour une validation.
- **Audit en ajout seul** : la table `decisions_documents` (`statut`, `motif`, `decide_par` → `utilisateurs.id`, `decide_le` UTC) est écrite **dans la même transaction** que la mise à jour du document (`valide_par`, `date_validation`). L'application n'a aucune route de modification ni de suppression de cet historique.
- **Deux agents simultanés** : mise à jour conditionnelle (`WHERE statut_validation = 'en_attente'`) ; le second reçoit `DocumentDejaDecide` → 409, rien n'est écrit.
- Le remplacement par le candidat (WS-03) remet le document en attente ; l'historique garde le refus.

## 5. Gestion des accès (US-029)

- `backend/bll/gerer_utilisateurs.py` : `ListerUtilisateursUseCase`, `CreerUtilisateurUseCase` (email normalisé en minuscules, `LONGUEUR_MIN_MOT_DE_PASSE = 12`, haché par `IHacheurMotDePasse`), `ModifierAccesUtilisateurUseCase`, `ReinitialiserMotDePasseUseCase`. Toutes les routes exigent `get_current_admin_complet`.
- **Pas de suppression** : un retrait d'accès est `est_actif = False`, pour que `decisions_documents.decide_par` et `calendriers_admission.modifie_par` (clés étrangères vers `utilisateurs`) restent valides.
- **Garde-fous** (`_perd_acces_admin_actif`) : si la modification fait perdre à un admin actif son statut d'admin actif, elle est refusée quand la cible est l'auteur (`ActionSurSoiInterdite` → 409) ou quand `compter_admins_actifs() <= 1` (`DernierAdministrateurActif` → 409).
- Port `IUtilisateurRepository` étendu (`lister`, `mettre_a_jour`, `compter_admins_actifs`) ; la constante `LONGUEUR_MIN_MOT_DE_PASSE` est passée de `seed_admin.py` à l'entité `utilisateur.py`.
- Effet immédiat : rôle et état actif étant relus en base à chaque requête (§1), un compte désactivé est refusé dès sa requête suivante, sans attendre l'expiration du jeton.
- Tests : `tests/integration/test_utilisateurs_api.py`.

## 4. Frontend

`pages/admin-candidatures`, `pages/admin-dossier` (`PanneauDecision`), `pages/admin-calendrier`, `pages/admin-utilisateurs` (lien « Accès » visible du seul rôle `admin`), entité `entities/dossier-admin` (API, types, badges). Mise en page fluide (barre latérale qui passe au-dessus sur mobile, grilles `auto-fit`, tableau défilant).

---

*ws-tech-04-administration.md — FDS Portail — Bravetech · GL-EN3-2026*
