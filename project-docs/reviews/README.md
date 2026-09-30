---
created: 2026-09-10T19:30:13Z
updated: 2026-09-30T16:04:08Z
---

# `reviews/` — ce que tu croyais qui s'est finalement avéré faux

**Ce dossier est vide et c'est le plus précieux de tous.** Rien n'y va au jour 1, et s'il est encore vide après ton premier Epic, quelque chose a mal tourné — pas avec le projet, mais avec la tenue des archives.

Une revue n'est ni un document de conception ni un journal des changements. Son mode est exactement un seul et unique objectif :

> voici ce que je croyais, voici la preuve que c'était faux, voici la revendication corrigée.

## Les règles qui font fonctionner cela

**Un fichier par élément de travail**, numéroté et nommé selon le sujet : `01-architecture-review.md`, `02-frontend-test-review.md`. **Le numéro correspond à l'ordre dans lequel la revue a été écrite, pas à une priorité ni à une catégorie** — ce dossier est un historique, donc l'ordre chronologique est celui dans lequel il faut le lire, et un simple `ls` le trierait par sujet, ce qui ne dit rien sur la manière dont la compréhension a évolué. Attribue le numéro une fois et ne le réattribue jamais : une revue ultérieure prend le prochain, car une citation dans un ancien message de commit doit continuer à pointer vers le même document. Pas de date dans le nom du fichier — les entrées à l'intérieur portent ces dates, tout comme le frontmatter `updated:`.

**Écrit au moment où la découverte est faite, pas à la fin du travail.** C'est toute la règle, et la raison en est arithmétique : une correction coûte presque rien à écrire tant qu'elle est fraîche, et devient presque impossible à reconstruire une semaine plus tard. Une revue écrite à la fin d'un Epic est un résumé de ce qui a été livré, ce que fait le document de clôture.

**Numérote les découvertes** — `F1`, `F2`, ou un tableau avec une colonne *status*. Une découverte résolue plus tard obtient sa résolution ajoutée, jamais une modification qui ferait croire que l'original avait raison depuis le début.

**Conserve les corrections, surtout les embarrassantes.** Une revue dont toutes les conclusions se sont révélées être *« légèrement plus subtiles que prévu »* est une revue que personne n'a écrite honnêtement. Le projet source dont ce kit est issu a un enregistrement selon lequel son propre `README.md` affirmait que deux modules étaient testés unitairement alors que ce n'était pas le cas — découvert en rencontrant un bug dans l'un d'eux — et ce paragraphe vaut plus que toute la prose de clean architecture à côté.

## Ce qui n'y vit pas : les règles

**Une découverte qui devient une règle ne doit pas rester seulement dans ce dossier**, et c'est la mauvaise décision qu'il vaut mieux prévenir que découvrir. Une revue est le *compte rendu* — ce que l'on croyait, la preuve, la correction. Quelqu'un cherchant une règle ouvre le document qui détient les règles de ce type ; personne ne pense à lire un historique pour savoir quelles sont les règles.

Donc, à la clôture du travail, chaque découverte reçoit une destination : le PRD si cela a changé ce que produit le produit, `SOLUTION_DESIGN.md` si cela a changé l'architecture, `PROJECT_WORKFLOW.md` si cela a changé la manière de travailler, la paire de spécifications du Workstream si c'est une zone spécifique, `AGENTS.md` si aucune session ne doit pouvoir l'oublier, `learnings/` si cela dépasse ce projet — et **nulle part du tout si ce n'était qu'une correction**, auquel cas la revue est déjà complète. Ton `AGENTS.md` doit porter ce tableau ; `project-init-kit/AGENTS.md` § *Where a rule lives* a la forme.

La revue reste exactement où elle est, et le nouvel emplacement de la règle peut pointer vers elle pour l'histoire complète. Rien ne pointe l'autre sens.

## Pourquoi c'est séparé de `learnings/`

| | |
|---|---|
| **une revue** | contemporaine, datée, liée à *ce* code. Écrite avant que quiconque ne sache comment l'histoire se terminera |
| **un apprentissage** | distillé, réutilisable, écrit après coup, destiné à s'appliquer à ton *prochain* projet |

**Une revue est la source d'un apprentissage.** Plus tard, un passage sur ces fichiers demande : *est-ce vrai au-delà de cette base de code ?* Quand la réponse est oui, cela devient un fichier `learnings/` — **et la revue reste exactement là où elle est.** Extraire n'est pas déplacer. Fusionner les deux dossiers perd la chose qui rend une revue enseignable : elle a été écrite depuis l'intérieur de l'erreur.

## Si tu donnes ce projet à quelqu'un

Ce dossier est la partie de ton processus qui est aussi un produit. Un lecteur apprend plus de la manière dont tu as eu tort que de l'architecture à laquelle tu es arrivé, et c'est le seul endroit qui survit.
