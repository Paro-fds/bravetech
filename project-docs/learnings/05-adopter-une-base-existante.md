---
created: 2026-11-06T04:13:16Z
updated: 2026-11-06T04:13:16Z
---

> **First learned:** 2026-11-04 18:00:00
> **Last updated:** 2026-11-05 23:11:55

# Adopter une base existante dans un outil de migrations : comparer à la révision d'origine, pas au code du jour

## Context

Beaucoup de projets commencent sans outil de migrations (tables créées par l'ORM au démarrage) et en adoptent un plus tard, alors qu'une base de production existe déjà. Il faut alors « adopter » cette base : la déclarer à une révision sans la recréer. La question qui décide de tout est **à quoi on la compare** avant de l'adopter. Ce fichier existe parce que la réponse évidente (« aux modèles du code ») est juste le jour de l'adoption, et fausse dès la migration suivante.

## How this was learned

**Trigger :** mise en place d'Alembic sur une base PostgreSQL de production créée par `create_all` (2026-11-04), puis ajout de la première table par une migration `0002` (2026-11-05).

**The path :**
1. **Première version :** si la base a des tables mais pas de table de version, la marquer à la révision `0001` (équivalent de `alembic stamp`). Aucune vérification.
2. **Premier défaut, trouvé en copiant une vieille base de développement :** elle contenait des tables d'un ancien schéma, et aurait pu manquer d'une colonne récente. Elle aurait été déclarée à jour alors qu'elle ne l'était pas. **Correction :** avant d'adopter, comparer la base aux modèles du code (autogenerate) ; refuser s'il manque une table ou une colonne, tolérer une table en trop.
3. **Second défaut, trouvé un jour plus tard en écrivant la migration `0002` :** la comparaison se faisait contre les modèles **actuels**, qui contenaient la nouvelle table. Une vraie base d'avant les migrations n'a forcément pas cette table : elle aurait été refusée. Et les tests, qui fabriquaient « une base d'avant les migrations » avec `create_all` sur les modèles actuels, produisaient une base qui **avait** la nouvelle table, si bien que `upgrade` échouait en voulant la créer. Les tests simulaient un passé qui n'a jamais existé.
4. **Correction retenue :** la comparaison ne porte que sur les tables de la révision d'origine (`TABLES_INITIALES`) ; une table absente qui appartient à une migration postérieure est tolérée, `upgrade` la crée. Les tests créent une vraie base d'avant les migrations (les seules tables d'origine). Un test vérifie que la liste `TABLES_INITIALES` correspond exactement à ce que crée la révision `0001` : sinon, la constante se mettrait à mentir à son tour.
5. Aucune production n'a été touchée : la base du serveur était déjà marquée `0001` avant l'arrivée de `0002`.

**Things to be aware of :**
- Le code du jour décrit la **tête** des migrations, pas la révision à laquelle on adopte. Les deux ne coïncident que tant qu'il n'y a qu'une migration.
- Un test qui fabrique « l'ancien état » avec le code d'aujourd'hui ne teste pas l'ancien état.
- Le défaut ne se voit qu'à la **deuxième** migration : c'est précisément quand personne ne repense à l'adoption.

## The Rule

1. **Une base adoptée se compare au schéma de la révision à laquelle on l'adopte**, figé (liste de tables, ou la migration d'origine rejouée), jamais aux modèles courants.
2. **Refuser l'adoption d'une base qui manque de quelque chose de cette révision** ; tolérer ce qui est en trop (restes d'anciens schémas).
3. **Les tests d'adoption fabriquent l'état d'origine à partir de la révision d'origine**, pas des modèles courants.
4. **Toute constante qui décrit le passé a un test qui la compare au passé réel** (ici : la révision d'origine rejouée sur une base vide).

## Common mistakes

| Mistake | Why it happened | Fix |
|---|---|---|
| Adopter sans vérifier le contenu | « La base vient de `create_all`, elle est forcément conforme » | Comparaison avant adoption, refus si une table ou une colonne manque |
| Comparer aux modèles courants | Juste le jour de l'adoption, avec une seule migration | Comparaison limitée aux tables de la révision d'origine |
| Simuler une base ancienne avec `create_all` sur les modèles courants | Le test réutilisait l'outil de création du jour | Base de test créée avec les seules tables d'origine, et test de la constante contre la migration `0001` |
