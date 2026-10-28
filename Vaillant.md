---
created: 2026-10-28T14:18:55Z
updated: 2026-10-28T14:18:55Z
---

# Répartition du travail — Vaillant

## Mission

Prendre en charge le téléversement des pièces justificatives, puis les fondations de l'espace administratif et son export. Les fonctionnalités d'administration doivent être protégées et leurs documents accessibles uniquement via un accès autorisé.

## User stories attribuées

| Story | Travail à réaliser | Dépendances |
|---|---|---|
| **US-007 — Téléversement sécurisé** | Créer le port `IFileStorage` et le stockage local (Cloudinary optionnel si configuré); contrôler côté serveur l'extension, la taille maximale de 5 Mo et les magic bytes; réaliser l'interface d'upload et les tests. | US-005, US-006 |
| **US-011 — Authentification admin** | Créer les utilisateurs et l'authentification bcrypt/JWT HS256 (expiration 60 min), les rôles `admin` et `agent`, la protection des routes, le rate limiting de 5 tentatives par minute, la page de connexion et le script de seed sécurisé par variable d'environnement. | Socle Epic 1; à intégrer après le parcours candidat de l'Epic 2 |
| **US-012 — Dashboard administratif** | Ajouter les endpoints protégés de liste paginée et de consultation détaillée des candidatures, le proxy sécurisé des documents et les écrans de dashboard/détail. Afficher notamment le statut des pièces et `deplacement_physique`. | US-011, US-008 |
| **US-015 — Export CSV/PDF** *(Could Have, après le MVP)* | Ajouter l'export protégé par JWT, avec filtre de statut et boutons sur le dashboard. Utiliser `csv` pour le CSV et convenir avec l'équipe du choix de bibliothèque PDF avant son intégration. | US-012 et Epic 3 terminé |

## Ordre et coordination

1. Réaliser US-007 après que Joas a livré US-005 et US-006; prévenir Joas quand l'upload et son contrat API sont prêts pour US-008.
2. Commencer US-011 après l'achèvement de l'Epic 2, conformément au séquencement du projet.
3. Réaliser US-012 après US-011 et la disponibilité des candidatures enregistrées en US-008.
4. US-015 est optionnelle pour le lancement et vient après le dashboard et l'Epic 3.

## Livrables attendus

- Fonctionnalités frontend et backend des stories attribuées, avec contrats API documentés si nécessaire.
- Tests de validation des fichiers, d'accès autorisé/non autorisé, de pagination et d'export.
- Pull request par story ou groupe cohérent de stories, intégrée après revue.
- Mise à jour du suivi des stories lorsque leur statut change.

## Règles à respecter

- Valider les fichiers **côté serveur** : magic bytes, extension autorisée et taille maximale de 5 Mo avant tout stockage.
- Utiliser un stockage local persistant par défaut; Cloudinary reste un adaptateur optionnel.
- Protéger chaque route `/api/v1/admin/` avec une vérification JWT et de rôle, pas uniquement la page de connexion.
- Ne jamais exposer directement les URLs de stockage des documents; passer par le proxy admin protégé.
- Ne pas versionner de secrets, de clés JWT ou de mots de passe.
- Garder la logique métier dans `bll/`, les entités indépendantes des frameworks et les accès techniques dans `dal/`.
- Une story n'est terminée que lorsque ses tests passent, le build frontend passe si concerné, et la pull request est approuvée et fusionnée.

