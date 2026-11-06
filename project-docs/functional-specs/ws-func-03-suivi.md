---
created: 2026-11-06T04:00:00Z
updated: 2026-11-06T04:11:35Z
---

# Spécification Fonctionnelle — WS-03 Suivi de dossier

**Réponses :** Que voit et que peut faire un candidat une fois son dossier envoyé ?
**Périmètre :** consolidé à la clôture de l'Epic 2 (2026-11-06) à partir d'US-009 et US-010, avec la mise en page ordinateur (US-022, PR #58) et l'adresse réelle du visiteur (US-024). Implémentation : [`ws-tech-03-suivi.md`](../technical-specs/ws-tech-03-suivi.md).

---

## 1. Retrouver son dossier (`/suivi`)

- Le candidat saisit sa référence `CAN-AAAA-NNNN` (minuscules et espaces acceptés). Un format invalide est signalé avant tout appel.
- Liens directs : `/suivi/CAN-2026-0089` (écran de confirmation, emails) ; l'ancien `/suivi?ref=…` y redirige.
- Référence inconnue ou mal formée : un seul message, « Aucun dossier trouvé pour cette référence. Vérifiez les chiffres, ou contactez-nous. » Rien ne permet de savoir si une référence existe.
- « Vous avez perdu votre référence ? » : lien d'écriture à la Faculté.

## 2. Ce que montre un dossier

- **Identité minimale** : référence, prénom et **initiale** du nom (« Louismy L. »), admission MPC, date d'envoi. Jamais d'email, de téléphone, de date de naissance, de commune ni de nom de fichier : la référence suffit pour consulter, elle ne doit rien révéler d'autre.
- **Avancement** : « n pièces validées sur 5 » et un badge global :

| Badge | Quand |
|---|---|
| En examen | Aucune pièce refusée, au moins une pas encore validée |
| Action requise | Au moins une pièce refusée |
| Dossier complet | Les 5 pièces validées |

- **Chaque pièce** : statut (En examen, Validée, À remplacer), date de réception ou de validation (au jour d'Haïti), et pour un refus le **motif** écrit par le personnel.
- Le portail ne prononce **aucune admission** : il dit seulement où en sont les pièces.
- Sur ordinateur : identité et avancement à gauche, toujours visibles ; pièces à droite.

## 3. Remplacer une pièce refusée (`/suivi/<référence>/remplacer/<pièce>`)

- Accès par « Remplacer ce document » sous la pièce refusée, ou par le bouton de l'email de refus.
- Le candidat rappelle **l'email de sa candidature** et choisit le nouveau fichier : sans compte et avec des références qui se suivent, la référence seule ne prouve pas qui il est. Référence ou email faux : même refus.
- Mêmes contrôles qu'au dépôt (format, ≤ 5 Mo, contenu réel). Un fichier refusé laisse la pièce refusée et l'ancien fichier en place.
- Après l'envoi, la pièce repasse « En examen » et le personnel peut de nouveau la décider ; le refus précédent reste dans l'historique du personnel. Un accusé de réception est envoyé par email.
- Seule une pièce **refusée** se remplace ; une pièce en examen ou validée, non.
- **Après la date limite** (US-028), suivi et remplacement restent possibles : un candidat qui a envoyé à temps doit pouvoir corriger.

## 4. Limites de consultation

Pour freiner qui essaierait de deviner des références : au-delà de 20 consultations par minute depuis la même adresse, le candidat lit « Trop de recherches en peu de temps. Patientez une minute puis réessayez. » Après 5 erreurs d'email en une minute, le remplacement est bloqué une minute. Chaque visiteur a son propre compteur, même derrière les proxys de l'UEH (US-024).

---

*ws-func-03-suivi.md — FDS Portail — Bravetech · GL-EN3-2026*
