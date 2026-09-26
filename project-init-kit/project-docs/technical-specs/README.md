---
created: 2026-09-08T17:38:40Z
updated: 2026-09-11T14:49:25Z
---

# technical-specs/

**Réponses :** Comment un Workstream livré est-il réellement construit, d'un point de vue implémentation ?

**Pas de template fixe**, même logique que `functional-specs/` — les sections sont décidées par Workstream, de manière incrémentale, une fois qu'il existe une vraie implémentation à documenter.

**Convention de nommage :** `ws-tech-NN-name.md`, même couplage que le côté fonctionnel, correspondant à l'identifiant du Workstream.

> **Questions à se poser pour décider si une section est nécessaire :**
> 1. Qu'un nouvel ingénieur doit-il savoir pour modifier cela en sécurité sans casser un invariant ?
> 2. Quel est le contrat exact de données, le schéma ou la règle de nommage, suffisamment précis pour qu'il n'y ait pas de dérive entre deux implémentations ?
> 3. Quelle décision ici était non évidente au point que quelqu'un pourrait la « corriger » plus tard vers la mauvaise chose ?
>
> **Question directrice pour tout cela : une histoire de ce Workstream est-elle réellement clôturée ? Sinon, il faut attendre.**
