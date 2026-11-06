---
created: 2026-11-06T04:00:00Z
updated: 2026-11-06T04:11:35Z
---

# Spécification Fonctionnelle — WS-02 Candidature

**Réponses :** Que vit un candidat entre « Postuler » et la référence de son dossier ?
**Périmètre :** consolidé à la clôture de l'Epic 2 (2026-11-06) à partir d'US-005, US-006, US-007, US-008 et US-018, complété par les ajouts ultérieurs (paiement refusé et relancé, période de candidature US-028, mise en page ordinateur). Implémentation : [`ws-tech-02-candidature.md`](../technical-specs/ws-tech-02-candidature.md).

---

## 1. Le tunnel (`/postuler`)

Un seul parcours, sans compte, pour l'**admission unique au Premier cycle MPC** (ADR-008) : le candidat ne choisit aucun cursus. Quatre étapes, une barre de progression « Étape n sur 4 » (sur ordinateur : les quatre étapes nommées), puis un récapitulatif et la confirmation.

| Étape | Ce que le candidat fait | Ce qui le bloque |
|---|---|---|
| 1. Vos informations | Nom, prénom, date de naissance (14 à 90 ans), sexe, téléphone haïtien à 8 chiffres, email, département (10), commune | Champ invalide (message sous le champ) ; email déjà utilisé pour la campagne |
| 2. Admission et accès | Lit le parcours MPC (2 ans) puis branche (3 ans) ; répond **obligatoirement** « Avez-vous dû vous déplacer pour candidater ? » (`deplacement_physique`, mesure principale du produit) | Pas de réponse |
| 3. Frais de dossier | Choisit MonCash ou NatCash, saisit un numéro, « Simuler le paiement de 500 HTG ». Bandeau **PAIEMENT SIMULÉ** : aucun argent n'est prélevé | Étape 2 non faite |
| 4. Vos pièces | Dépose les **5 pièces** (acte de naissance, Bac II, relevé de notes, deux photos d'identité, CIN), une carte par pièce avec jauge d'envoi | Paiement non abouti ; fichier refusé (format, taille ≤ 5 Mo, contenu ne correspondant pas à l'extension) |
| Récapitulatif | Relit tout, « Confirmer et soumettre mon dossier » | Pièce ou étape manquante (la liste s'affiche) |
| Confirmation | Reçoit sa **référence `CAN-AAAA-NNNN`** en grand, avec copie en un clic, « Notez-la », et le bouton « Suivre mon dossier » | — |

## 2. Le paiement simulé

| Numéro saisi | Ce qui se passe |
|---|---|
| Se termine par `0000` | **Refusé** par l'opérateur (solde insuffisant), à chaque tentative avec ce numéro |
| Se termine par `9999` | **Échec** technique la première fois ; « Relancer le paiement » réussit |
| Autre | **Accepté** : référence `PAY-SIM-AAAA-NNNN` |

Les numéros de test sont affichés sous le champ. Un refus ou un échec ne débloque ni les pièces ni la soumission. Un double clic ne crée jamais deux paiements.

## 3. Règles

- **Reprise** : le brouillon est enregistré sur le serveur dès l'étape 1. Si la connexion coupe, le candidat rouvre `/postuler` sur le même appareil et reprend où il en était.
- **Une candidature par email et par campagne.** Un second départ avec le même email est refusé (« une candidature existe déjà ») : un brouillon ne se rouvre jamais par l'email, pour ne pas l'exposer à quiconque connaît l'adresse.
- **Remplacer une pièce avant l'envoi** : possible tant que le dossier n'est pas soumis.
- **Après la soumission, le dossier est verrouillé** : plus aucune modification par le tunnel. Une pièce refusée se remplace ensuite par le suivi (WS-03).
- **L'email de confirmation n'est pas une condition** : la référence s'affiche à l'écran même s'il n'arrive pas (WS-05). L'écran dit qu'un email « est envoyé », pas qu'il « a été envoyé ».
- **Période de candidature (US-028)** : avant l'ouverture ou après la date limite fixées par l'administration, un nouveau candidat voit « Les candidatures sont fermées » avec les dates, et ne peut ni commencer ni soumettre. Un brouillon commencé reste affiché, mais sa soumission est refusée après la date limite. Sans calendrier enregistré, le tunnel est ouvert.
- **Langues** : tout le tunnel existe en français et en kreyòl (sélecteur de l'en-tête, US-020).
- **Sur ordinateur** : le formulaire est dans une carte, avec à côté un encadré « Bon à savoir » (frais simulés, date limite, reprise, contact).

---

*ws-func-02-candidature.md — FDS Portail — Bravetech · GL-EN3-2026*
