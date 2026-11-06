---
created: 2026-11-06T04:00:00Z
updated: 2026-11-06T18:04:26Z
---

# Spécification Fonctionnelle — WS-04 Administration

**Réponses :** Que fait le personnel de la Faculté dans l'espace `/admin` ?
**Périmètre :** consolidé à la clôture de l'Epic 3 (2026-11-06) à partir d'US-011 à US-013, complété par l'export (US-015, Epic 4), le calendrier d'admission (US-028) et la gestion des accès du personnel (US-029). L'espace admin reste en français (pas de kreyòl). Implémentation : [`ws-tech-04-administration.md`](../technical-specs/ws-tech-04-administration.md).

---

## 1. Accès

- **Connexion** (`/admin/login`) : email et mot de passe. Un seul message d'erreur pour un email inconnu, un mauvais mot de passe ou un compte désactivé. Après 5 échecs en une minute, la connexion est bloquée une minute.
- **Session** : 60 minutes, sans renouvellement ; elle disparaît à la fermeture de l'onglet (poste partagé). Session expirée → retour à la connexion.
- **Deux rôles** : `admin` (tout) et `agent` (consulter et décider les pièces, consulter le calendrier). Seul un `admin` modifie le calendrier et gère les accès.
- **Comptes** : le premier admin est créé par un script au déploiement ; les suivants depuis l'écran « Accès » (§5).

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

## 5. Gestion des accès du personnel (`/admin/utilisateurs`, US-029)

Réservée au rôle `admin` (lien « Accès » de la barre latérale ; un agent n'y a pas accès).

- **Liste** de tous les comptes, actifs et désactivés, avec leur rôle.
- **Créer un compte** : email, rôle (`agent` ou `admin`), mot de passe provisoire de 12 caractères minimum, à transmettre à la personne. Un email déjà utilisé est refusé.
- **Changer le rôle** d'un compte, ou le **désactiver / réactiver**. Un compte désactivé ne peut plus se connecter, et une session déjà ouverte est refusée à la requête suivante.
- **Réinitialiser le mot de passe** : nouveau mot de passe provisoire.
- **Aucun compte n'est supprimé** : ses décisions passées et ses modifications du calendrier restent attribuées dans l'historique.
- **Garde-fous** : un administrateur ne peut ni se désactiver ni se retirer le rôle `admin` lui-même ; le dernier administrateur actif ne peut être ni désactivé ni rétrogradé. Le portail ne peut donc jamais se retrouver sans administrateur.

---

*ws-func-04-administration.md — FDS Portail — Bravetech · GL-EN3-2026*
