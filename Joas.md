---
created: 2026-10-28T14:18:55Z
updated: 2026-10-28T14:18:55Z
---

# Répartition du travail — Joas

## Mission

Prendre en charge le parcours candidat depuis le formulaire jusqu'à la confirmation, puis les notifications. Les fonctionnalités de candidature doivent respecter les règles métier du projet et rester utilisables sur téléphone.

## User stories attribuées

| Story | Travail à réaliser | Dépendances |
|---|---|---|
| **US-005 — Formulaire d'inscription** | Créer les entités `Candidat` et `Candidature`, leurs modèles de persistance et DTO; réaliser l'étape d'informations personnelles et de choix de cursus; rendre obligatoire et persister `deplacement_physique`; ajouter tests unitaires et d'intégration. | Catalogue des cursus (Epic 1) |
| **US-006 — Simulation de paiement** | Ajouter le choix MonCash/NatCash, le montant de 500 HTG, la validation du numéro haïtien, la référence simulée `PAY-SIM-2026-XXXX` et la persistance du statut de paiement. Afficher clairement qu'aucun argent réel n'est prélevé. | US-005 |
| **US-008 — Finalisation et confirmation** | Enregistrer le dossier complet, générer une référence unique `CAN-2026-XXXX`, afficher l'écran de confirmation et envoyer l'email de confirmation sans bloquer la candidature en cas d'échec. | US-005, US-006, US-007 |
| **US-014 — Emails après décision administrative** | Ajouter les emails de validation et de rejet, avec le motif de rejet et le lien de remplacement si nécessaire. Un échec email ne doit pas annuler la décision administrative; il doit être journalisé. | US-008 (port email), US-013 |
| **US-016 — Notifications SMS** *(Should Have, après le MVP)* | Ajouter le port SMS et les adaptateurs console et fournisseur configuré; envoyer le SMS après une décision admin, sans bloquer celle-ci; respecter la préférence de notification du candidat. | US-014 et Epic 3 terminés |

## Ordre et coordination

1. Réaliser US-005 puis US-006.
2. Coordonner US-007 avec Vaillant avant de finaliser US-008 : la soumission dépend du téléversement sécurisé.
3. Attendre la réalisation de US-013 par Widmaken avant de brancher les emails de décision (US-014).
4. Réaliser US-016 après US-014 et la clôture de l'Epic 3. Cette story est secondaire par rapport au parcours MVP.

## Livrables attendus

- Fonctionnalités frontend et backend des stories attribuées, avec contrats API documentés si nécessaire.
- Tests adaptés aux règles métier et aux erreurs; comportement vérifié sur mobile.
- Pull request par story ou groupe cohérent de stories, intégrée après revue.
- Mise à jour du suivi des stories lorsque leur statut change.

## Règles à respecter

- Garder la logique métier dans `bll/`, les entités indépendantes des frameworks et les accès techniques dans `dal/`.
- `deplacement_physique` est obligatoire et enregistré en base.
- Le paiement est une simulation visuellement explicite; ne jamais collecter de paiement réel.
- Un échec email ou SMS ne doit pas annuler une candidature ni une décision admin.
- Ne pas versionner de secrets ou de mots de passe.
- Une story n'est terminée que lorsque ses tests passent, le build frontend passe si concerné, et la pull request est approuvée et fusionnée.

