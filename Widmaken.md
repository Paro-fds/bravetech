---
created: 2026-10-28T14:18:55Z
updated: 2026-10-28T14:18:55Z
---

# Répartition du travail — Widmaken

## Mission

Prendre en charge le suivi public des candidatures et la boucle de traitement des documents : décision administrative auditée, correction par le candidat, puis amélioration visuelle après la stabilisation du produit.

## User stories attribuées

| Story | Travail à réaliser | Dépendances |
|---|---|---|
| **US-009 — Suivi de dossier** | Ajouter la consultation d'un dossier par référence, l'endpoint public de statut et la page `/suivi`, avec progression et état des pièces. Limiter les données personnelles affichées et gérer clairement une référence inexistante. | US-008 |
| **US-013 — Validation ou rejet avec audit** | Ajouter les actions admin de validation/rejet, le motif facultatif et la mise à jour des statuts. Enregistrer systématiquement `valide_par` et `date_validation` sans permettre leur modification hors décision auditée; mettre à jour l'interface et les tests. | US-012 |
| **US-010 — Remplacement d'un document rejeté** | Permettre le nouvel upload depuis le suivi, réutiliser l'enregistrement du document au lieu de créer un doublon, revalider le fichier côté serveur et remettre son statut à `en_attente`. | US-009 et US-013 |
| **US-017 — Mode sombre** *(Could Have, après l'Epic 3)* | Ajouter les thèmes clair/sombre par variables CSS, un bouton de bascule, la préférence système au premier chargement et la persistance du choix. Vérifier les contrastes WCAG AA sur les pages importantes. | Epic 3 terminé |

## Ordre et coordination

1. Réaliser US-009 une fois qu'US-008 fournit des dossiers consultables.
2. Attendre le dashboard protégé d'US-012 (Vaillant) avant de commencer US-013.
3. Réaliser US-010 seulement après la disponibilité du suivi et des décisions admin. Vérifier avec Joas que les emails US-014 pointent vers le bon parcours de remplacement.
4. Réaliser US-017 après la stabilisation de l'interface admin; cette story est secondaire par rapport au MVP.

## Livrables attendus

- Fonctionnalités frontend et backend des stories attribuées, avec contrats API documentés si nécessaire.
- Tests d'intégration pour le suivi, les décisions auditées et l'absence de doublons lors du remplacement.
- Vérification de la confidentialité des données publiques et des contrastes en mode sombre.
- Pull request par story ou groupe cohérent de stories, intégrée après revue.
- Mise à jour du suivi des stories lorsque leur statut change.

## Règles à respecter

- La page publique de suivi n'expose pas les données personnelles sensibles du candidat ni les données d'autres candidats.
- Toute décision admin est auditée; `valide_par` et `date_validation` doivent être persistés.
- Le remplacement d'une pièce rejetée est un upsert avec unicité `(candidat_id, document_requis_id)`; ne jamais créer un doublon.
- Tout fichier de remplacement est validé côté serveur (magic bytes, extension et taille ≤ 5 Mo).
- Garder la logique métier dans `bll/`, les entités indépendantes des frameworks et les accès techniques dans `dal/`.
- Une story n'est terminée que lorsque ses tests passent, le build frontend passe si concerné, et la pull request est approuvée et fusionnée.

