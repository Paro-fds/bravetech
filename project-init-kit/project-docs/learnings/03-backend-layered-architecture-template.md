---
created: 2026-09-08T17:38:40Z
updated: 2026-09-16T19:53:40Z
---

> **Premier apprentissage :** 2026-09-08 15:30:00
> **Dernière mise à jour :** 2026-09-08 15:30:00

## Contexte

Un backend multi-service réel a traversé plusieurs cycles de critique avant que sa structuration interne ne se stabilise en quelque chose valant la peine d'être réutilisé tel quel sur le *prochain* service backend, plutôt que redérivé (en refaisant les mêmes erreurs corrigées) depuis zéro à chaque fois. Ce fichier est la version généralisée et agnostique au projet de cette structure stabilisée — extrait des notes d'apprentissage internes d'un projet et de la skill de scaffolding qui l'accompagne, afin qu'un nouveau projet puisse démarrer un service backend déjà à la forme « stabilisée » au lieu de la forme « premier essai, sur le point d'être critiqué ».

Ce fichier complète `01-documentation-structure-template.md` : ce fichier concerne la couche *documentation* au-dessus d'un projet ; le présent fichier concerne la couche *code interne* à l'intérieur d'un service backend. À utiliser une fois que `SOLUTION_DESIGN.md` §4/§6 a décidé qu'un service a besoin d'une vraie structure interne (pas un script en fichier unique), avant d'écrire la première ligne du code source de ce service.

## Comment cela a été appris

**Déclencheur :** Un second service backend dans le même projet devait partager une table de base de données avec le premier. Décider *comment* a forcé une vraie question architecturale recherchée — dupliquer le mapping d'accès aux données dans chaque service, ou extraire un package partagé — ce qui à son tour nécessitait que la structuration elle-même soit déjà suffisamment principiée pour raisonner dessus proprement. Cette pression-test est ce qui a fait émerger la plupart des règles ci-dessous ; elles n'ont pas été conçues à l'avance, elles ont été corrigées jusqu'à leur forme finale.

**Le chemin :** Le premier service backend n'a pas démarré avec cette structure — il a traversé de vrais cycles de critique qui ont détecté : une logique métier dépendant accidentellement d'un type ORM spécifique au framework au lieu d'un objet de domaine simple ; une hiérarchie d'exceptions éclatée entre les couches qui rendait flou quelle couche était autorisée à décider d'un code de statut HTTP ; et un instinct « ajouter simplement le champ au modèle » qui faisait fuiter une préoccupation de couche de persistance (une colonne de base de données) dans du code qui ne devrait jamais voir qu'un concept de domaine. Chacun de ces éléments a été corrigé une fois, puis consigné comme règle pour que la correction n'ait pas à se reproduire sur le prochain service. Quand un second service a eu besoin de la même base de données, le choix entre « dupliquer le mapping » et « partager un package » a été résolu en pesant un compromis concret (risque de dérive de schéma de la duplication vs. conflit de convention d'outillage d'un package partagé) plutôt que par défaut — voir le Journal des Décisions pour la façon dont ce cas spécifique a été raisonné.

**À avoir en tête :**
- Cette structure justifie son coût sur un service avec une vraie logique métier et plus de quelques entités. Un service utilitaire à un seul endpoint n'a pas besoin de quatre couches — n'imposez pas ceci sur quelque chose qui n'a pas la complexité pour le justifier.
- La règle de dépendance unidirectionnelle (ci-dessous) est facile à énoncer et facile à violer accidentellement la première fois qu'un raccourci « juste cette fois » semble pratique — ex. importer directement un modèle ORM dans un gestionnaire de route pour économiser une étape de conversion. Chacun de ces raccourcis, pris une fois, devient très difficile à trouver et annuler plus tard, une fois qu'une douzaine d'autres routes ont copié le même raccourci.
- Décider de dupliquer un mapping d'accès aux données ou de le partager comme package entre services est un vrai compromis non évident, pas un défaut — voir la sous-section « Partager l'accès aux données entre services » de La Règle.

## La Règle

### Les quatre couches, et la dépendance unidirectionnelle

```
Entités  ←  Couche d'Accès aux Données (DAL)  ←  Couche de Logique Métier (BLL)  ←  Couche API
```

Les dépendances pointent dans **un seul sens**, de gauche à droite n'est jamais permis :

- **Entités** — objets de domaine simples (un dataclass, un modèle Pydantic utilisé comme type de domaine, ou équivalent dans votre langage). Pas d'imports de framework, pas de classe de base ORM, pas de connaissance qu'une base de données existe du tout. C'est ce à quoi chaque autre couche pense réellement.
- **Couche d'Accès aux Données (DAL)** — la *seule* couche autorisée à importer la bibliothèque ORM/base de données. Elle fait le mapping entre la représentation de persistance du framework (ex. une classe mappée SQLAlchemy) et une Entité simple, et expose des fonctions/méthodes qui prennent et retournent uniquement des Entités — jamais le type de ligne ORM. Gardez le vrai module de classe mappée privé au module (ex. préfixez-le `_UserRow` ou équivalent) pour que rien en dehors de cette couche ne soit même tenté de l'importer directement.
- **Couche de Logique Métier (BLL)** — toutes les règles métier, la validation et l'orchestration des appels DAL. Prend des Entités en entrée, retourne des Entités en sortie — jamais un DTO, jamais un type ORM. C'est là que « cette action peut-elle se produire » est décidé, pas dans la couche API et pas dans la DAL.
- **Couche API** — gestion des requêtes/réponses uniquement. Convertit une requête entrante en ce dont la BLL a besoin, appelle la BLL, convertit le résultat Entité de la BLL en une forme de réponse (un DTO). Ne contient pas de règles métier propres.

**Pourquoi unidirectionnel, pas un raccourci « juste cette fois » :** le moment où un gestionnaire de route importe directement un modèle ORM, ou que la BLL commence à retourner une ligne de base de données, tout l'intérêt de la frontière disparaît — la couche qui était supposée être interchangeable/testable en isolation dépend maintenant silencieusement de la chose dont elle était isolée. C'est la façon la plus courante dont cette structure s'érode ; traitez toute demande d'exception comme un signal pour chercher plus dur la couche correcte, pas comme un one-off pragmatique.

### Les DTOs vivent à la périphérie, pas au milieu

Un DTO (Data Transfer Object — la forme d'un corps de requête ou d'une payload de réponse) appartient uniquement à la couche API. Il existe pour définir le *contrat réseau*, qui est autorisé à différer de la forme interne de l'Entité (noms de champs différents, un sous-ensemble de champs, un champ calculé). Ne laissez jamais un DTO fuiter dans la BLL ou la DAL — ces couches ne voient jamais que des Entités.

### Exceptions : un fichier plat, nommé sémantiquement, mappé en exactement un endroit

- Gardez les classes d'exceptions dans un fichier plat unique (ex. `core/exceptions.py`), pas éclaté par couche ou par fonctionnalité. Nommez-les pour le sens métier de l'échec (`InvalidCredentialsError`, `DuplicateEmailError`), jamais pour quelle couche les a levées (`DAL_NotFoundError`) — un appelant ne devrait pas avoir besoin de savoir quelle couche a échoué pour comprendre ce qui a mal tourné.
- Mappez chaque exception à un statut HTTP (ou réponse au niveau transport équivalente) en exactement un endroit (ex. `core/exception_handlers.py`). Aucun autre fichier ne devrait jamais décider d'un code de statut depuis un type d'exception — cette décision appartient en un seul endroit pour qu'elle ne puisse pas dériver en deux réponses différentes pour la même exception.
- C'est bien, et souvent correct, qu'une exception couvre plus d'une cause sous-jacente quand l'appelant ne devrait pas pouvoir les distinguer (ex. une exception générique unique d'« identifiants invalides » couvrant à la fois « mauvais mot de passe » et « token expiré », pour qu'un appelant ne puisse pas utiliser la spécificité de l'erreur pour énumérer quelle partie d'une vérification d'authentification a échoué).

### Partager l'accès aux données entre services

Dès que deux services indépendants ont besoin de lire/écrire le même entrepôt de données sous-jacent, il y a un vrai choix, pas un défaut :

| Option | Quand c'est juste | Le vrai coût |
|---|---|---|
| **Dupliquer le mapping d'accès aux données** dans chaque service (chaque service définit son propre modèle de couche DAL pour la table partagée) | Les services sont censés rester indépendamment déployables, chacun avec sa propre configuration de dépendances/environnement, et le schéma de la table partagée change rarement et de façon prévisible (propriété d'exactement un historique de migrations de service) | Risque de dérive de schéma si les mappings dupliqués ne sont pas maintenus synchronisés — à atténuer avec un propriétaire unique clair du schéma/migrations réel, et un commentaire de code dans chaque doublon pointant vers ce propriétaire |
| **Extraire un package partagé** (une bibliothèque partagée dont les deux services dépendent) | Les services partagent déjà une configuration de gestion des dépendances (un workspace style monorepo, un environnement virtuel/lockfile partagé), ou le schéma partagé change suffisamment souvent pour que la duplication dériverait immédiatement | Signifie généralement faire converger les deux services vers un environnement/lockfile partagé — un vrai coût si la convention de votre projet est un environnement indépendant par service |

Quel que soit le choix, consignez la décision comme une entrée ADR dans `SOLUTION_DESIGN.md` §14 — c'est exactement le type de choix qui semble arbitraire rétrospectivement si le compromis pesé n'est pas enregistré.

### Une forme de dossier minimale pour un service backend

```
<service>/
├── app/
│   ├── main.py                 <- point d'entrée de l'app / bootstrap du serveur
│   ├── core/
│   │   ├── config.py           <- chargement des paramètres/env
│   │   ├── exceptions.py       <- fichier plat, une classe par échec métier
│   │   └── exception_handlers.py  <- le seul endroit où les exceptions se mappent en statut de réponse
│   ├── entities/                <- objets de domaine simples, pas d'imports de framework
│   ├── dal/                     <- la seule couche autorisée à importer la bibliothèque ORM/BD
│   ├── bll/                     <- règles métier, prend/retourne uniquement des Entités
│   └── api/
│       └── v1/
│           └── dto/             <- formes requête/réponse, couche API uniquement
└── <manifeste de dépendances, dossier de migrations, etc. selon votre stack>
```

Un service fraîchement scaffoldé devrait avoir une infrastructure fonctionnelle (`core/`, la configuration de connexion base de données de la DAL, un routeur API vide) mais **pas** de fichier `entities/`, `dal/`, `bll/` ou `dto/` encore — ce sont de vrais travaux de fonctionnalité, ajoutés par unité de travail (par user story), pas dans le cadre du scaffolding. Les construire avant un vrai besoin produit du code mort qui doit être maintenu sans jamais être exercé.

### Un piège de concurrence à vérifier dès qu'un second writer apparaît

Si plus d'un processus/service écrira dans la même base de données légère à base de fichiers (ex. SQLite), ne supposez pas qu'un paramètre de concurrence documenté (ex. « nous utilisons le mode WAL ») est réellement en vigueur — vérifiez-le directement (interrogez le paramètre réel à l'exécution) plutôt que de faire confiance à un commentaire ou un tableau de stack. Une configuration mono-writer ne fait jamais apparaître l'écart ; il ne devient un vrai risque de correction que le moment où un second writer arrive, ce qui est exactement quand il est le plus facile de le rater parce qu'ajouter le second service ne *ressemble* pas à un changement de base de données.

### Un piège CORS à vérifier dès qu'un second frontend d'origine distincte apparaît

Si un frontend basé sur navigateur appelle ce backend depuis une origine différente (port ou domaine différent), la vérification uniquement côté backend (un client HTTP en ligne de commande) ne détectera pas une configuration CORS manquante — le preflight CORS et son application sont purement côté navigateur, invisibles à tout client non-navigateur. La seule vérification fiable est un test basé sur un vrai navigateur (un script de navigateur headless ou un clic manuel) pilotant le vrai frontend contre le vrai backend.

## Erreurs courantes

| Erreur | Pourquoi ça arrive | Correction |
|---|---|---|
| Importer la classe mappée ORM directement dans un gestionnaire de route « juste pour économiser une étape de conversion » | Semble du boilerplate inutile sur le moment | Toujours convertir vers/depuis l'Entité à la frontière DAL, même quand cela semble redondant pour un ensemble de champs trivial — le boilerplate est ce qui garde la frontière réelle |
| Laisser un nom ou une forme de champ DTO fuiter dans la propre logique de la BLL (ex. brancher sur le champ optionnel d'un DTO au lieu de celui de l'Entité) | Le DTO est déjà dans la portée dans le gestionnaire API, pratique de le passer en travers | Convertir DTO → Entité avant d'appeler dans la BLL, toujours, même pour une requête à un seul champ |
| Éclater les classes d'exceptions par couche (`DAL_NotFoundError`, `BLL_NotFoundError`) | Semble refléter proprement l'architecture | Nommer les exceptions pour le sens métier de l'échec, pas la couche — un fichier plat, un sens par classe |
| Supposer qu'un paramètre de concurrence ou CORS documenté est réellement implémenté, parce que c'est écrit dans un doc de config/architecture | La documentation décrit l'intention, et l'intention est facile à confondre avec un fait vérifié | Vérifier le comportement à l'exécution directement (interroger le paramètre réel, exécuter la vraie vérification basée sur navigateur) le moment où un second service ou une seconde origine rejoint, ne pas faire confiance au seul document |

## Journal des Décisions — Séquence des Changements

1. **Premier service backend construit** — la séparation en quatre couches (Entités/DAL/BLL/API) et la convention du fichier d'exceptions plat adoptées après que la vraie critique a détecté des violations de frontière dans un brouillon antérieur.
2. **Le second service backend avait besoin de partager une table avec le premier** — résolu via le compromis « Partager l'accès aux données entre services » ci-dessus : le mapping de couche DAL a été dupliqué plutôt qu'un package partagé extrait, spécifiquement parce que la convention du projet était un environnement de dépendances indépendant par service, et un package partagé aurait nécessité de faire converger les deux sur un seul environnement.
3. **La construction du second service a fait émerger deux vrais écarts, pas des décisions** : un paramètre de concurrence de base de données documenté mais non implémenté, et une configuration CORS manquante uniquement détectée par un vrai test basé sur navigateur après qu'une vérification en ligne de commande avait réussi proprement — les deux généralisés dans les deux sous-sections de pièges de ce fichier ci-dessus.
