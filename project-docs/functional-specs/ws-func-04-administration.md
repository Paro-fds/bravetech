---
created: 2026-11-06T04:00:00Z
updated: 2026-11-06T04:11:35Z
---

# Spécification Fonctionnelle — WS-04 Administration

**Réponses :** Que fait le personnel de la Faculté dans l'espace `/admin` ?
**Périmètre :** consolidé à la clôture de l'Epic 3 (2026-11-06) à partir d'US-011 à US-013, complété par l'export (US-015, Epic 4) et le calendrier d'admission (US-028). L'espace admin reste en français (pas de kreyòl). Implémentation : [`ws-tech-04-administration.md`](../technical-specs/ws-tech-04-administration.md).

---

## 1. Accès

- **Connexion** (`/admin/login`) : email et mot de passe. Un seul message d'erreur pour un email inconnu, un mauvais mot de passe ou un compte désactivé. Après 5 échecs en une minute, la connexion est bloquée une minute.
- **Session** : 60 minutes, sans renouvellement ; elle disparaît à la fermeture de l'onglet (poste partagé). Session expirée → retour à la connexion.
- **Deux rôles** : `admin` (tout) et `agent` (consulter et décider les pièces, consulter le calendrier). Seul un `admin` modifie le calendrier.
- **Comptes** : le premier admin est créé par un script au déploiement ; il n'existe pas d'écran de gestion des comptes.

## 2. Liste des dossiers (`/admin`)

- **Seuls les dossiers soumis** apparaissent ; un brouillon n'est pas un dossier.
- **Indicateurs**, sur tous les dossiers soumis : nombre de dossiers ; part « sans déplacement physique » (objectif 70 %) ; pièces à examiner ; part de pièces refusées (alerte au-delà de 20 %).
- **Statut d'un dossier** : *À examiner* ; *Action du candidat* dès qu'une pièce est refusée ; *Complet* quand les 5 pièces sont validées (même règle que le suivi du candidat).
- **Recherche** par référence ou par nom, sans tenir compte des majuscules ni des accents ; **filtres** par statut et par déplacement physique ; 20 dossiers par page, du plus ancien au plus récent (ordre de traitement).
- **Export** CSV ou PDF de **tous** les dossiers correspondant aux filtres affichés, sans pagination. L'export ne contient ni email, ni téléphone, ni adresse : il circule hors de la plateforme.

## 3. Dossier d'un candidat (`/admin/candidatures/<référence>`)

- Identité complète et coordonnées (pour contacter ou vérifier), réponse au déplacement, paiement simulé.
- **Aperçu de chaque pièce** (PDF ou image) dans la page ; aucun lien direct vers un fichier.
- **Décider une pièce** :
  - « Valider cette pièce » demande une confirmation ;
  - « Refuser cette pièce… » exige un **motif** (5 à 500 caractères) : le candidat le lira ;
  - **une décision est définitive.** Une pièce refusée ne redevient décidable qu'après son remplacement par le candidat ;
  - si un collègue a décidé la même pièce juste avant, la page se met à jour et le dit ;
  - après une décision, la pièce suivante à examiner s'ouvre.
- **Historique** de toutes les décisions du dossier (qui, quand, quoi, motif), y compris celles d'avant un remplacement.
- Chaque décision envoie un email au candidat (WS-05).

## 4. Calendrier d'admission (`/admin/calendrier`, US-028)

Ouverture, date limite de dépôt, concours, résultats, rentrée. Ouverture et date limite obligatoires ; les dates doivent se suivre. La page indique l'état (« Candidatures ouvertes », « pas encore ouvertes », « fermées ») et la dernière modification (date, auteur). Le site public suit sans redéploiement. Comportement côté candidat : ws-func-01 §1.1, §1.2, §1.8 et ws-func-02 §3.

---

*ws-func-04-administration.md — FDS Portail — Bravetech · GL-EN3-2026*
