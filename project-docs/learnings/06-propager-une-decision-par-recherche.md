---
created: 2026-11-06T04:13:16Z
updated: 2026-11-06T04:13:16Z
---

> **First learned:** 2026-11-05 17:47:00
> **Last updated:** 2026-11-05 23:11:55

# Une décision qui en remplace une autre se propage par une recherche, pas par la mémoire

## Context

Dans un projet documenté (documents fondateurs, registre de décisions, stories avec critères d'acceptation), chaque changement met à jour **le document qu'il touche**. Ceux qui **citent** l'ancienne version, eux, ne bougent pas : rien ne les signale. Ce fichier existe parce que ce mécanisme a produit, sur le même projet et à deux niveaux différents, des documents faux pendant des semaines sans que personne ne les relise, et qu'il se corrige par une habitude simple.

## How this was learned

**Trigger :** deux relectures avant la remise, le même jour (2026-11-05), avec la grille de notation sous les yeux.

**The path :**
1. **Niveau « décision d'architecture ».** Le stockage des fichiers est passé d'un service externe (Cloudinary) à un volume local le 2026-09-27, et l'hébergement d'une plateforme (Railway, Vercel) à une machine de la Faculté le 2026-09-26. Les deux changements avaient leur entrée dans le registre des décisions (ADR). Cinq à six semaines plus tard, une recherche du mot `cloudinary|railway|vercel` dans les documents fondateurs renvoyait **56 occurrences dans six documents**, dont le fichier d'instructions de l'agent (« Services : Cloudinary ») et le plan de sauvegarde. Le document d'architecture contenait même deux exemplaires de lui-même, dont un gabarit vide, parce que des stories avaient ajouté du contenu au mauvais exemplaire.
2. **Niveau « exigence ».** Une story de paiement simulé était livrée, ses critères d'acceptation cochés. Le contrat du cours, relu ligne à ligne, exigeait aussi les cas « refusé », « échoué » et « relancé ». Les critères avaient été écrits depuis le plan du projet, jamais relus contre le contrat. Même chose pour les emails : « codés et testés », mais désactivés en production.
3. Dans les deux cas, chaque document **pris isolément** semblait juste ; seule une recherche transversale (un `grep` du terme remplacé, une relecture du contrat source) a montré l'écart.
4. **Correction :** les documents ont été corrigés (en un passage, d'après le code réel), et la règle est entrée dans la définition de fini du projet.

**Things to be aware of :**
- Un registre de décisions à jour donne une fausse impression de projet à jour : il ne dit que ce qui a changé, pas où l'ancien choix est encore écrit.
- Les documents les plus lus (instructions de l'agent, README) sont les plus touchés : on les écrit tôt et on ne les rouvre plus.
- Une case cochée prouve qu'un critère est tenu, pas que le critère était le bon. La source d'un critère (contrat, besoin client) doit être relue, pas seulement le plan qui en dérive.

## The Rule

1. **Quand une décision en remplace une autre**, chercher l'ancien terme (nom du fournisseur, de la bibliothèque, de l'hébergeur) dans tous les documents de référence, et les corriger **dans le même changement**.
2. **Écrire et relire les critères d'acceptation contre la source** (contrat, cahier des charges, demande du client), pas contre le plan qui la résume ; et considérer qu'une fonctionnalité n'est livrée que si elle marche dans l'environnement réel.
3. **Mettre ces deux vérifications dans la définition de fini**, là où elles seront appliquées à chaque story, plutôt que dans une relecture de fin de projet.
4. **Un document de gabarit rempli ne garde ni ses questions ni ses « à rédiger »** : leur présence est le signe qu'on écrit au mauvais endroit.

## Common mistakes

| Mistake | Why it happened | Fix |
|---|---|---|
| ADR écrite, documents qui la contredisent laissés tels quels | Chaque story ne met à jour que le document qu'elle touche | Recherche de l'ancien terme ajoutée à la définition de fini |
| Contenu ajouté au mauvais exemplaire d'un document dupliqué | Le gabarit du kit était resté collé à la fin du document rempli | Document fusionné ; « aucune question de gabarit » dans la définition de fini |
| Critères d'acceptation cochés mais incomplets | Écrits depuis le plan, pas depuis le contrat | Critères relus contre le contrat ; « livré = fonctionne en production » dans la définition de fini |
