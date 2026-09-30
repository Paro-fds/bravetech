---
created: 2026-09-10T19:30:13Z
updated: 2026-09-30T16:04:08Z
---

# `learnings/` — pratique transférable vers ton prochain projet

Un apprentissage est une **pratique transférable** : quelque chose qui vaut la peine d'être fait sur n'importe quel projet, appris en le faisant sur celui-ci. Il est écrit pour quelqu'un qui ne lira jamais cette base de code — y compris toi, dans dix-huit mois, en démarrant quelque chose d'autre.

## Dans quel dossier cela va-t-il ?

Trois destinations, une question chacune. Pose-les dans l'ordre et arrête-toi à la première réponse oui.

| Question | Destination |
|---|---|
| Est-ce du contenu que le produit enseigne ou livre lui-même ? | où que vive le contenu du produit — pas ici |
| Est-ce une correction de ce que tu croyais sur *ce* code ? | **`../reviews/`** — daté, lié à un fichier, écrit au moment de la découverte |
| S'agit-il d'une pratique utile sur un projet sans lien avec celui-ci ? | **ici** |

**Pose la deuxième question honnêtement, car la plupart des découvertes appartiennent là.** Un apprentissage qui ne peut pas survivre à l'enlèvement de tous les noms spécifiques au projet est une revue classée dans le mauvais dossier. Le test : *retire chaque nom propre à ce projet. Reste-t-il quelque chose d'intéressant à lire ?*

**Une revue est la source d'un apprentissage.** Plus tard, un passage sur `../reviews/` demande : *est-ce vrai au-delà de cette base de code ?* — et si la réponse est oui, cela devient un fichier ici pendant que **la revue reste exactement là où elle est.** Extraire n'est pas déplacer.

## Nommage

`NN-<descriptive-kebab-case>.md` : `04-trusting-a-new-tool.md`, pas `trusting_a_new_tool.md`. Le nombre enregistre **l'ordre dans lequel l'apprentissage est entré dans ce dossier**, attribué une fois et jamais réattribué — pas un ordre de lecture et pas une priorité, puisque ces fichiers sont cherché par sujet. Même convention que `reviews/`, pour la même raison. Les fichiers importés d'un autre projet sont renumérotés selon votre séquence au lieu de conserver ceux du projet d'origine, car ils ne disent rien de vrai ici.

## Structure

N'importe quelle forme qui le sert, mais ces quatre sections méritent leur place, et une est non négociable :

- **`## Context`** — ce que c'est, et pourquoi il vaut la peine de le conserver plutôt que de le redériver.
- **`## How this was learned`** — le déclencheur, puis **le chemin**, puis les pièges. **Le chemin doit montrer les mauvais chemins comme des mauvais chemins.** « J'ai essayé Y, ça a cassé parce que Z, corrigé en X » — pas lissé en « nous avons décidé X ». C'est toute la valeur ; un fichier qui ne retient que la version finale propre n'est pas un apprentissage, c'est de la documentation.
- **`## The Rule`** — le conseil réutilisable, généralisé au-delà de l'incident unique qui l'a produit.
- **`## Common mistakes`** — un tableau de corrections *réelles* qui se sont produites. Jamais des hypothèses.

Si un travail n'a vraiment eu aucun mauvais détour, écris-le en une ligne au lieu de fabriquer du drame que le travail n'a pas eu.

---

*Note de mainteneur, pour qui exporte ce kit :* les fichiers d'apprentissage d'exemple viennent du propre dossier `learnings/` du projet source et sont copiés au moment de l'export, pour qu'il n'y ait qu'une seule copie vivante au lieu de deux qui dérivent. Les règles ci-dessus sont la partie que l'étudiant doit connaître ; les exemples servent d'illustration.
