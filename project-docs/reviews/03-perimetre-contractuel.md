---
created: 2026-11-05T17:47:00Z
updated: 2026-11-05T17:47:40Z
---

# 03 — Le périmètre à livrer (ce que nous croyions sur le paiement simulé et les emails)

**Contexte :** le 2026-11-05, relecture ligne à ligne du périmètre de l'équipe dans le document de lancement du Projet 2 (Partie 3 : Must, Should, Could ; Partie 5 : « ce qui doit fonctionner »), comparé au code et à la production.

## Découvertes

| ID | Ce que nous croyions | Ce qui est vrai | Preuve | Statut |
|---|---|---|---|---|
| F1 | Le paiement simulé est complet : US-006 est livrée, ses critères d'acceptation sont cochés (succès, saisie invalide, double envoi, étape précédente manquante). | Le cours exige « le paiement qui réussit, celui qui échoue, celui qui est refusé, celui qui est relancé ». Le simulateur ne savait que **réussir** ou **refuser une saisie invalide**. Aucun refus de l'opérateur, aucun échec technique, aucune relance. Nos critères d'acceptation avaient été écrits sans relire ce passage du cours. | `backend/bll/simuler_paiement.py` avant correction : seules issues possibles, `InformationsInvalides` ou succès. | ✅ Corrigé (US-006, as-built du 2026-11-05) |
| F2 | Les emails sont livrés : US-008 (confirmation) et US-014 (validation et rejet) sont codées et testées. | Ils sont **désactivés en production** (`EMAIL_ENABLED=false`, aucune clé Resend sur la VM). Pour le correcteur, un Must Have qui ne fonctionne pas sur l'URL publique n'est pas livré. « Codé et testé » n'est pas « en production ». | `.env` de la VM, lu le 2026-11-05. | ⏳ En cours : domaine d'envoi à vérifier chez Resend, clé à poser sur la VM |
| F3 | US-027 (sauvegardes hors site) fait partie du périmètre noté. | Elle n'est dans aucune case du MoSCoW du contrat : c'est un ajout de l'équipe pour l'exploitation. Seul US-016 (SMS, Should Have) est contractuel parmi les stories ouvertes. | Document de lancement, Partie 3, Équipe 2. | ✅ Clarifié : US-016 à livrer ou à justifier au §2 du rapport |

## Résolution

| Règle | Destination |
|---|---|
| Un critère d'acceptation se relit contre le périmètre contractuel (document de lancement, Partie 3 et Partie 5), pas seulement contre la story | `PROJECT_WORKFLOW.md` (définition de fini) |
| Les issues simulées du paiement et les numéros de test | `US-006.md` (as-built) et docstring de `simuler_paiement.py` |
| Une fonctionnalité n'est livrée que si elle marche sur l'URL de production | `PROJECT_WORKFLOW.md` (définition de fini) |
