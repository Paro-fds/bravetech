---
created: 2026-09-29T18:00:00Z
updated: 2026-09-29T18:00:00Z
status: open
---

# epic-003-refinement.md — Administration & Audit

> **Ce fichier est la source de vérité des règles en cours pour epic-003.**  
> Toute règle technique ou décision d'arbitrage produite pendant cet Epic vit ici jusqu'à sa clôture.  
> À la clôture : chaque règle sera déplacée dans le document propriétaire, et ce fichier servira d'historique.

---

## 1. Scope de l'Epic 3

L'Epic 3 implémente le **volet administration** du FDS Portail : l'authentification sécurisée des agents de la FDS, le tableau de bord de gestion des candidatures, la validation ou le rejet de chaque document soumis (avec traçabilité complète), et les notifications email déclenchées par ces décisions.

**Ce que cet Epic ne couvre PAS :**
- La candidature elle-même côté candidat (Epic 2).
- Le remplacement de document rejeté côté candidat (US-010 — Epic 2).
- Les exports et le mode sombre (Epic 4 — Could Have).
- Les paiements réels ou l'intégration FDS Pay (hors périmètre V1).

---

## 2. Découvertes (Findings)

| ID | Constat | Statut |
|---|---|---|
| E3-1 | Les entités `Candidat` et `DocumentSoumis` sont créées par l'Epic 2. L'Epic 3 les consomme en lecture/écriture via le même DAL. | ✅ Confirmé |
| E3-2 | L'authentification admin repose sur JWT HS256 + bcrypt, sans SSO institutionnel dans cette phase. La table `utilisateurs` est créée dans cet Epic. | ✅ Retenu |
| E3-3 | La traçabilité (`valide_par`, `date_validation`) est une exigence stricte du MoSCoW Must Have — chaque décision doit être auditée et immuable. | ✅ Exigence absolue |
| E3-4 | L'email de notification validation/rejet (US-014) est déclenché côté admin après update du statut — il doit être non-bloquant (échec email ≠ annulation de la décision). | ✅ Règle héritée de E2-4 |
| E3-5 | Le rate limiting anti-brute-force sur `/api/auth/token` (5 req/60s) est une exigence de sécurité Must Have (OWASP A07). | ✅ À implémenter dans cet Epic |

---

## 3. Questions ouvertes & Décisions techniques

| # | Question | Recommandation | Arbitrage |
|---|---|---|---|
| Q1 | **Durée de vie du JWT admin :** 60 min ou plus long ? | 60 min (exigence sécurité). Refresh token hors MVP — l'admin se reconnecte manuellement. | ✅ 60 min sans refresh |
| Q2 | **Pagination du dashboard :** taille par page ? | 20 dossiers par page (`?page=1&limit=20`) — évite les full table scans à volume croissant. | ✅ 20 par page |
| Q3 | **Rôles RBAC :** `admin` seul ou `admin` + `agent` ? | Deux rôles : `admin` (lecture + écriture + accès complet) et `agent` (lecture + décisions documents). | ✅ Deux rôles |
| Q4 | **Seedage du premier compte admin :** comment sans exposition de mot de passe ? | Script de seed protégé par variable d'env (`ADMIN_SEED_PASSWORD`), exécuté une seule fois au déploiement. | ✅ Script de seed env-gated |

---

## 4. Découpage des User Stories (Ordre de build)

| Ordre | Story | Titre | Dépend de |
|---|---|---|---|
| 1 | **US-011** | Authentification administrateur (JWT + RBAC) | Socle Epic 1 |
| 2 | **US-012** | Dashboard admin — liste et consultation des candidatures | US-011 |
| 3 | **US-013** | Validation ou rejet d'un document avec audit | US-012 |
| 4 | **US-014** | Notification email déclenchée par une décision admin | US-013 |
