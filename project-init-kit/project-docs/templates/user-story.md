---
created: 2026-09-08T17:38:40Z
updated: 2026-09-11T14:49:25Z
---

# _TEMPLATE_US.md — modèle de user story

> **Rappel de vocabulaire** : une **User story** est l'unité concrète de travail à l'intérieur d'un **Epic** (étape de construction séquentielle, voir `PLAN.md`), touchant un ou plusieurs **Workstream** (zone fonctionnelle, voir `SOLUTION_DESIGN.md`). Voir aussi `GLOSSARY.md` § Workstream, Epic et Milestone.
>
> Copie ce fichier vers `epic-NNN-<name>/US-NNN.md` une fois que le premier Epic est nommé dans `PLAN.md`. La numérotation `US-NNN` est séquentielle sur **tout le projet**, jamais réinitialisée par Epic, jamais réutilisée.

```markdown
# US-NNN: [Titre court]

**Statut :** 🔲 Backlog / ✅ Fait / etc.
**Milestone :** [Nom de l'Epic]
**Dépend de :** US-XXX (optionnel — uniquement s'il existe une vraie dépendance)

---

## En tant que [rôle depuis GLOSSARY.md]
Je veux [fonctionnalité ou capacité]
Afin de [résultat]

## Contexte
[Ce qui existe déjà. Quel est l'état de la base de code. Quels fichiers/composants/
histoires précédentes cela s'appuie sur. Ce qu'il ne faut pas supposer déjà fait.]

## Critères d'acceptation
- [ ] [Spécifique et binaire]
- [ ] [...]

## Hors périmètre
- [Ce qui ne doit pas être construit dans cette histoire]

## Tâches
- [ ] [Étape de mise en œuvre concrète]
- [ ] [...]

## Définition de terminé
- [ ] [Élément spécifique vérifié à l'œil ou par test]

## Notes de mise en œuvre
[Ajouté une fois que le travail commence ou se termine — ce qui s'est réellement passé,
écarts par rapport au plan, décisions prises en cours de route.]
```

> **Questions à se poser avant d'écrire chaque section :**
>
> **En tant que / Je veux / Afin de**
> 1. Qui veut précisément cela — quel rôle nommé dans le Glossary, et pas seulement « un utilisateur » ?
> 2. Que veulent-ils pouvoir faire, en une phrase ?
> 3. Pourquoi ce résultat compte-t-il pour eux, pas seulement pour toi en tant que concepteur ?
>
> **Contexte**
> 1. Qu'est-ce qui existe déjà et sur quoi cela s'appuie ?
> 2. Que ne faut-il pas supposer explicitement déjà fait ?
>
> **Critères d'acceptation**
> 1. Quelle est la plus petite affirmation testable, sans ambiguïté, vraie ou fausse une fois le travail terminé ?
> 2. Y a-t-il un critère qui est en réalité une tâche déguisée — une étape de mise en œuvre, pas un résultat observable ?
>
> **Hors périmètre**
> 1. Qu'est-ce qui est adjacent à cette histoire et qu'un lecteur pourrait supposer inclus, mais qui ne l'est pas ?
>
> **Tâches**
> 1. Quelle est la prochaine action concrète, dans un ordre réellement exécutable de bout en bout ?
>
> **Définition de terminé**
> 1. Que la personne qui a demandé cela vérifie-t-elle réellement de ses propres yeux pour accepter le résultat ?
>
> **Notes de mise en œuvre**
> 1. Qu'est-ce qui a changé entre ce qui était prévu et ce qui a été réellement construit, et pourquoi ?
