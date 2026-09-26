---
created: 2026-09-08T17:38:40Z
updated: 2026-09-11T14:49:25Z
---

# functional-specs/

**Réponses :** Que fait réellement un Workstream livré, du point de vue du comportement ?

**Pas de template fixe.** Les sections sont décidées par Workstream, une fois qu'il existe un vrai comportement à documenter — jamais avant. Rédiger une spécification fonctionnelle avant la clôture d'une histoire de ce Workstream relève de la spéculation, pas de la documentation.

**Convention de nommage :** `ws-func-NN-name.md`, où `NN` correspond exactement à l'identifiant du Workstream dans `SOLUTION_DESIGN.md` § Workstreams.

> **Questions à se poser pour décider si une section est nécessaire (et non pour remplir une liste fixe) :**
> 1. Qu'un utilisateur ou un système appelant observe-t-il maintenant qu'il ne pouvait pas observer avant l'existence de ce Workstream ?
> 2. Quels sont les cas limites ou les conditions de refus qu'une personne qui s'appuie dessus doit connaître ?
> 3. Existe-t-il une règle ici qui n'est pas évidente à la lecture du code — règle métier, frontière de confidentialité, contrainte d'ordre ?
>
> **Question directrice pour tout cela : une histoire de ce Workstream est-elle réellement clôturée ? Sinon, il n'y a rien de réel à documenter — il faut attendre.**
