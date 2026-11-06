---
created: 2026-11-06T04:00:00Z
updated: 2026-11-06T04:11:35Z
---

# Spécification Fonctionnelle — WS-05 Notifications

**Réponses :** Quels emails le portail envoie-t-il, à qui, et que se passe-t-il s'ils n'arrivent pas ?
**Périmètre :** consolidé à la clôture de l'Epic 3 (2026-11-06) à partir d'US-008, US-010, US-014 et US-019. Les SMS (US-016) ne sont pas livrés. Implémentation : [`ws-tech-05-notifications.md`](../technical-specs/ws-tech-05-notifications.md).

---

## 1. Les emails

| Déclencheur | Destinataire | Objet | Contenu |
|---|---|---|---|
| Dossier soumis (WS-02) | Candidat | « Confirmation de votre candidature — CAN-… » | Référence (« conservez-la »), lien « Suivre mon dossier », rappel que le paiement était une simulation |
| Pièce validée (WS-04) | Candidat | « Pièce validée — <pièce> (CAN-…) » | Lien vers le suivi |
| Pièce refusée (WS-04) | Candidat | « Pièce à remplacer — <pièce> (CAN-…) » | **Motif** du refus, bouton « Remplacer le document → » |
| Pièce remplacée (WS-03) | Candidat | « Nouvelle pièce reçue — <pièce> (CAN-…) » | Accusé de réception |
| Formulaire « Nous écrire » (`/contact`) | Secrétariat (`CONTACT_EMAIL`) | Sujet fixe | Nom, email et message du visiteur ; « Répondre » écrit au visiteur |

Un dossier de 5 pièces décidées une par une produit jusqu'à 5 emails de décision : c'est voulu (un email par décision).

## 2. Règles

- **Un email au candidat n'est jamais une condition.** Si l'envoi échoue, la candidature, la décision ou le remplacement restent enregistrés et la page répond normalement ; la référence est toujours affichée à l'écran. Les écrans disent qu'un email « est envoyé », pas qu'il « a été envoyé ».
- **Le formulaire de contact est l'exception** : là, l'email *est* l'action. S'il ne part pas (envoi en échec, ou adresse du secrétariat non configurée), le visiteur reçoit un message d'erreur clair et **garde son texte** dans la page, pour réessayer plus tard.
- **Anti-spam du contact** : 3 messages par 10 minutes depuis une même adresse ; un robot qui remplit le champ piège invisible reçoit une réponse normale, sans qu'aucun email ne parte.
- **Langue** : les emails sont en français.
- **Expéditeur en production** : `FDS Portail <noreply@fds.ctpea-prefac.me>` (domaine configuré chez Resend le 2026-11-05 ; vérification à confirmer dans le tableau de bord Resend). Le domaine de l'UEH n'a pas pu être vérifié à temps (DNS gérés par l'UEH).
- **Interrupteur** : l'administrateur système peut couper tous les envois (`EMAIL_ENABLED=false`) sans redéployer le code.

## 3. Non livré

**Notifications SMS (US-016, Should Have)** : non construites. Voir `execution/EPIC_EXECUTION.md`.

---

*ws-func-05-notifications.md — FDS Portail — Bravetech · GL-EN3-2026*
