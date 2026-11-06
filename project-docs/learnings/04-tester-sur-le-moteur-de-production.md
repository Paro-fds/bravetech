---
created: 2026-11-06T04:13:16Z
updated: 2026-11-06T04:13:16Z
---

> **First learned:** 2026-11-04 15:45:00
> **Last updated:** 2026-11-05 23:11:55

# Une CI verte ne prouve rien sur un moteur qu'elle ne fait pas tourner

## Context

Un projet web teste souvent sur une base légère (SQLite en mémoire, en CI comme sur le poste du développeur) et tourne en production sur une autre (PostgreSQL). Tant que le code passe par un ORM, la différence paraît sans importance. Elle ne l'est pas : le **pilote** de la base, et toute la chaîne de dépendances qui le choisit, n'est jamais chargé par les tests. Ce fichier existe parce que cet écart est invisible jusqu'au premier démarrage réel, puis bloquant d'un coup.

## How this was learned

**Trigger :** premier démarrage du backend sur la machine de production (2026-11-04). Le conteneur plantait à l'import : `ModuleNotFoundError: No module named 'psycopg'`.

**The path :**
1. Les dépendances Python étaient déclarées `sqlalchemy>=2.0.0`, sans borne haute. L'image Docker construite ce jour-là a installé SQLAlchemy **2.1.8**, dont le pilote par défaut pour une URL `postgresql://` est passé de psycopg2 à psycopg 3. L'image n'avait que `psycopg2-binary`.
2. La CI était verte depuis des semaines : elle n'utilisait que SQLite, donc n'importait jamais aucun pilote PostgreSQL. Le poste de développement aussi.
3. **Premier correctif, mauvais :** un fichier `docker-compose.override.yml` non versionné sur le serveur, qui forçait `postgresql+psycopg2://`. Le portail démarrait, mais la correction n'existait que sur une machine : la prochaine personne qui reconstruisait l'image sans ce fichier retrouvait la panne.
4. **Correctif retenu :** le code réécrit lui-même toute URL `postgresql://` ou `postgres://` en `postgresql+psycopg2://` (avec un test), et **toutes** les dépendances sont figées avec `==` (celles de l'image qui tournait). Monter une version passe par une pull request, avec la CI.
5. Le même jour, un second écart du même genre est apparu : une base créée sur le serveur par une ancienne méthode, que rien en CI ne reproduisait (voir `05-adopter-une-base-existante.md`).

**Things to be aware of :**
- `>=` sans borne haute veut dire « la version du jour de la construction ». Deux images construites à une semaine d'écart ne sont pas la même application.
- Le symptôme ne ressemble pas à un problème de version : c'est un module introuvable, au démarrage, sur une machine où « rien n'a changé ».
- Un contournement posé à la main sur le serveur fait disparaître le symptôme et garde la cause. Il faut qu'il revienne dans le dépôt, ou il sera perdu.
- Ce que les tests ne chargent jamais (pilote de base, client d'un service externe, variable d'environnement de production) doit avoir au moins un test qui l'importe ou une vérification au démarrage.

## The Rule

1. **Figer toutes les dépendances** (`==`, ou un fichier de verrouillage) dans le dépôt ; la montée de version est un changement revu, pas un effet de la date de construction.
2. **Nommer explicitement ce qui choisit un comportement par défaut** (le pilote dans l'URL, l'adaptateur, la région) plutôt que d'hériter du défaut d'une bibliothèque.
3. **Lister ce que la CI n'exerce pas** (moteur de base, services externes) et le vérifier au moins une fois sur le vrai environnement avant de déclarer une story terminée ; l'écrire dans ses notes de réalisation (« Non vérifié : PostgreSQL »).
4. **Un correctif posé sur le serveur n'est pas un correctif** tant qu'il n'est pas dans le dépôt.

## Common mistakes

| Mistake | Why it happened | Fix |
|---|---|---|
| `sqlalchemy>=2.0.0` sans borne haute | Paraissait « compatible avec les futures versions » | Versions figées avec `==` dans `requirements*.txt` |
| Conclure « ça marche » d'une CI verte | La CI n'avait jamais chargé le pilote PostgreSQL | Pilote explicite dans le code, vérification sur la VM notée dans chaque story qui touche la base |
| Corriger par un fichier non versionné sur le serveur | Urgence de remettre le portail en ligne | Correction déplacée dans le code et le `docker-compose.yml` versionnés, fichier du serveur supprimé (vérifié le 2026-11-05) |
