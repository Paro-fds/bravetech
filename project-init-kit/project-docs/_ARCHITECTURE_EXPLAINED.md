---
created: 2026-09-16T19:40:29Z
updated: 2026-09-16T20:11:50Z
---

# Architecture, expliquée

**Réponses :** comment le code est-il divisé, pourquoi de cette manière, et quels fichiers chaque module est-il autorisé à importer ?
**Lisez ceci :** une fois, avant d'écrire le premier fichier source de l'un ou l'autre côté. Ensuite, gardez-le ouvert pendant que vous écrivez les dix suivants.

C'est le document du kit qui vous donne des réponses au lieu de questions.
Tout le reste sous `project-docs/` vous demande de réfléchir — `PRD.md` demande ce que vous construisez, `SOLUTION_DESIGN.md` demande comment.
Ce fichier dit : *voici une structure qui fonctionne, voici pourquoi elle fonctionne, et voici ce qu'elle coûte.*

**Tu peux remplacer n'importe quoi.** Ce que tu ne peux pas faire, c'est laisser cela implicite.
Une architecture que personne n'a écrite n'est pas une architecture plus simple ; c'est le même nombre de décisions, prises une fois chacun par la personne qui a touché le fichier en premier, et jamais écrites à l'endroit où la personne suivante peut les trouver.

---

## Partie 0 — L'idée unique

La majeure partie de ce qui suit est une conséquence d'une seule règle.
Robert C. Martin l'appelle la **Dependency Rule**, et la formule en une phrase :

> Les dépendances du code source ne doivent pointer qu'à l'intérieur.
> Rien dans un cercle interne ne peut connaître quoi que ce soit sur quelque chose dans un cercle externe.

Alistair Cockburn est arrivé au même endroit par une voie différente, et son cadrage est celui qui fait cliquer :

> L'asymétrie à exploiter n'est pas celle entre les côtés *gauche* et *droit* de l'application, mais entre *l'intérieur* et *l'extérieur*.

Son point est que l'interface utilisateur et la base de données sont **le même type de chose** : toutes deux sont externes, toutes deux sont remplaçables, et toutes deux tenteront de se répandre dans vos règles métier si vous les laissez faire.
Un framework web et un driver Postgres ne sont pas opposés — ce sont deux adaptateurs sur deux ports de la même machine.

### Ce que cette règle vous apporte

- **Vous pouvez tester le milieu sans démarrer quoi que ce soit.** Pas de serveur, pas de base de données, pas de navigateur. Si vos règles métier ont besoin d'un Postgres en cours d'exécution pour être exercées, elles ne sont pas isolées de Postgres.
- **Vous pouvez remplacer une frontière.** Remplacer SQLite par Postgres, ou REST par un consommateur de file, touche une seule couche.
- **Un bug a une adresse.** Quand le résultat est faux, vous pouvez demander *quelle couche est autorisée à savoir cela ?* et aller là.

### Le test qui compte vraiment

Ne mesurez pas votre architecture par son diagramme de dossiers. Mesurez-la par cette question :

> **Prenez n'importe quel fichier au hasard. Pouvez-vous dire, sans regarder, exactement quels dossiers il est autorisé à importer ?**

Si oui, vous avez une architecture. S'il dépend du fichier, vous avez uniquement une disposition de dossiers.

### Et une règle que personne ne vérifie est une préférence

C'est la partie que la plupart des projets ignorent, et c'est celle qui décide si la structure survit au contact d'une date butoir.

**Les deux moitiés de ce kit appliquent leur règle de dépendance avec une machine.**
Le backend le fait avec un test qui analyse chaque import et fait échouer le build (`tests/unit/test_architecture.py`).
Le frontend le fait avec un linter d'architecture (Steiger).
Aucun des deux ne compte sur la mémoire de quelqu'un.

La première fois qu'une personne importe directement le modèle ORM dans un route handler « juste pour économiser une étape de conversion », la frontière est partie — et elle partira silencieusement, parce que tout fonctionne encore. Dix routes plus tard, c'est irrécupérable. Un contrôle est ce qui transforme cela d'un jugement de goût en build rouge.

---

## Partie 1 — Le backend : quatre couches, une seule direction

```
entities  ←  dal  ←  bll  ←  api
   ↑                          ↑
   └──────── core/ ───────────┘   (config, logging, exceptions: disponibles pour tous)
```

Les flèches signifient **« est importé par »**. Les dépendances vont de droite à gauche, et jamais de gauche à droite.

**Cette forme a un nom — Clean Architecture — et la Partie 2 explique d'où elle vient.** Lisez la Partie 1 pour savoir ce que fait chaque dossier, puis la Partie 2 pour comprendre pourquoi la règle pointe dans cette direction.

Si vous voulez la version en un paragraphe : **les choses qui changent lentement vont au centre, les choses qui changent vite vont à la périphérie, et rien au centre n'est autorisé à nommer quoi que ce soit à la périphérie.**

### `entities/` — objets métier simples

Les choses dont votre produit parle : un `User`, un `Order`, un `Invoice`.

- Un dataclass, ou un modèle Pydantic utilisé comme type de domaine. Rien de plus.
- **Aucune import de framework. Aucune classe de base ORM. Aucune connaissance de l'existence d'une base de données.**
- C'est ce que toutes les autres couches partagent et utilisent.

Si `entities/` importe SQLAlchemy, le cercle le plus interne dépend maintenant du plus externe, et tous les avantages ci-dessus disparaissent d'un coup.

### `dal/` — la couche d'accès aux données

**La seule couche de l'ensemble du codebase autorisée à importer l'ORM.**

- Elle fait la correspondance entre la représentation de persistance (une classe mappée SQLAlchemy) et une entité simple.
- Ses fonctions **prennent des entités et renvoient des entités** — jamais une ligne mappée.
- Gardez la classe mappée privée au module : nommez-la `_UserRow`, pour que personne ne soit tenté de l'utiliser en dehors.

C'est le pattern Repository, et son but a un nom : **persistence ignorance**. Le reste de l'application ne sait pas *comment* une chose est stockée, seulement qu'elle peut être obtenue et enregistrée.

### `bll/` — la couche de logique métier

Chaque règle, chaque validation, chaque orchestrations qui implique plus d'un appel `dal/`.

- Prend des entités en entrée, renvoie des entités. **Jamais un DTO. Jamais un type ORM.**
- C'est ici que *« est-ce autorisé ? »* est décidé — pas dans la route, et pas dans le DAL.
- Si vous vous demandez où placer une logique et que la réponse est « eh bien, la route a déjà les données », la réponse est quand même ici.

### `api/` — la frontière

Entrée de requête, sortie de réponse. Rien d'autre.

- Convertissez le corps de requête entrant (un DTO) en ce dont le BLL a besoin.
- Appelez le BLL.
- Convertissez l'entité renvoyée par le BLL en un DTO de réponse.
- **Aucune règle métier.** Une route qui contient un `if` sur votre domaine a volé le travail du BLL.

### Les DTO vivent à la périphérie et nulle part ailleurs

Un **DTO** (Data Transfer Object) est la forme d'un corps de requête ou d'une réponse. C'est votre **contrat de transport** — la promesse que vous faites à quiconque vous appelle.

Il est délibérément autorisé à différer de votre entité : noms de champs différents, sous-ensemble de champs, champ calculé, relation aplatie. Cette liberté *est le point*. Votre modèle interne doit pouvoir changer sans casser chaque client.

**Un DTO ne doit jamais atteindre le BLL ou le DAL.** Le moment où la logique métier branche sur un champ optionnel d'un DTO, votre format de transport devient votre modèle de domaine, et vous ne pouvez plus modifier l'un sans l'autre.

### Pourquoi `api/v1/`, et ce que `v1` promet réellement

Le scaffold place les routes sous `app/api/v1/`, avec les DTO dans `app/api/v1/dto/`. Ce n'est pas un décor.

**Un numéro de version est une promesse qu'un client écrit aujourd'hui continuera de fonctionner demain.** Une fois qu'autre chose consomme votre API — un frontend que vous possédez aussi, une appli mobile, une autre équipe — vous ne contrôlez plus quand les appelants mettent à jour. Le versionnement donne un endroit pour mettre un changement qui autrement les casserait : `v2` apparaît, `v1` continue de fonctionner, les clients migrent à leur propre rythme.

Ce qui compte comme cassant, et donc exige une nouvelle version : supprimer un champ, renommer un champ, restreindre un type, rendre un champ optionnel obligatoire, changer le sens d'un code statut. Ce qui ne l'est pas : **ajouter** un champ optionnel, ajouter un endpoint, ajouter une valeur d'énumération que les clients sont censés ignorer si inconnue.

**La raison structurelle pour laquelle cela vit dans le nom du dossier** : parce que `dto/` se trouve *à l'intérieur* de `v1/`, un DTO v2 est un fichier différent plutôt qu'une modification d'un fichier partagé. Deux versions peuvent diverger sans qu'il y ait un seul `if version == 1` quelque part dans votre code. C'est ce qui empêche le versionnement de pourrir en pile de conditions.

**Commence par `v1` même seul.** Cela coûte un dossier aujourd'hui. Ajouter le versionnement à une API qui n'en a jamais eu coûte une migration de chaque appelant que tu ne connaissais pas.

### Exceptions : un seul fichier plat, des noms métier, mappés en un seul endroit

- Gardez les classes d'exception dans **un seul fichier plat** (`core/exceptions.py`) — pas divisées par couche, pas par fonctionnalité.
- Nommez-les selon **ce qui a échoué en termes métier** : `InvalidCredentialsError`, `DuplicateEmailError`. Jamais `DalNotFoundError`. Un appelant ne devrait pas avoir à connaître la couche qui a cassé pour comprendre ce qui s'est mal passé.
- Mappez chaque exception vers un statut HTTP dans **un seul endroit exact** (`core/exception_handlers.py`). Aucun autre fichier ne décide d'un code de statut à partir d'un type d'exception — sinon la même erreur obtient deux réponses différentes dans deux routes différentes, et personne ne s'en aperçoit pendant des mois.
- Une exception couvrant plusieurs causes est souvent *correcte* : un seul `InvalidCredentialsError` pour à la fois « mauvais mot de passe » et « token expiré » est délibéré, parce qu'un appelant capable de les distinguer peut enumérer votre vérification d'authentification.

### Application des règles

Écrivez le test avant d'en avoir besoin :

```python
# tests/unit/test_architecture.py — parcourt chaque import dans app/ et vérifie la direction
FORBIDDEN = {
    "entities": ("dal", "bll", "api", "sqlalchemy", "fastapi"),
    "dal":      ("bll", "api"),
    "bll":      ("api", "sqlalchemy"),
}
```

Parsez les imports de chaque module avec `ast`, recherchez sa couche à partir de son chemin, faites échouer le build sur toute collision.
C'est environ quarante lignes et c'est la différence entre une architecture et une intention.

La raison complète de cette couche, y compris le compromis de partager un DAL entre deux services, se trouve dans `project-docs/learnings/03-backend-layered-architecture-template.md`. Le *comment* — les dossiers, le boilerplate, les commandes — relève du skill `scaffold-backend-service`.

---

## Partie 2 — Comment on l'appelle : Clean Architecture

**La structure de la Partie 1 a un nom, et ce nom est Clean Architecture.**
Utilise-le. C'est ce que tu dois écrire dans `SOLUTION_DESIGN.md`, ce que tu dois dire dans une revue, et ce que tu dois chercher quand tu veux lire davantage.

### Une idée, quatre noms, vingt ans

La même architecture a été conçue indépendamment plusieurs fois, et chaque arrivée lui a donné un nom différent. Ce ne sont pas des approches concurrentes, et tu n'as pas à choisir entre elles :

| Année | Nom | Qui | Ce qu'il a ajouté |
|---|---|---|---|
| 2005 | **Hexagonal Architecture**, plus tard **Ports & Adapters** | Alistair Cockburn | l'idée que l'UI et la base de données sont le même type de chose — toutes deux externes |
| 2008 | **Onion Architecture** | Jeffrey Palermo | l'image concentrique, et l'argument du *churn* : les technologies d'accès aux données changent tous les quelques ans, donc elles ne doivent pas être au centre |
| 2012 | **Clean Architecture** | Robert C. Martin | la consolidation, et la Dependency Rule comme une seule phrase citable |

Le cadrage de Palermo est celui qu'il faut garder, parce qu'il explique *pourquoi* la règle pointe dans cette direction : **mets les choses qui changent lentement au centre, et les choses qui changent vite à la périphérie.** Tes règles métier survivent à votre base de données, votre framework web et probablement votre langage. Structure le code pour que cela soit possible.

C'est aussi pour cela que `entities/` est au centre. Pas parce que c'est important au sens abstrait — parce que c'est la partie que tu veux le moins réécrire quand tout le reste autour est remplacé.

### La chose qui la rend fonctionnelle, et que le diagramme ne peut pas montrer

**L'inversion de dépendance.** C'est le mécanisme, et c'est la partie que la plupart des gens ratent lorsqu'ils copient le diagramme de dossiers.

Voici le problème qu'elle résout. Au **runtime**, le flux de contrôle va *vers l'extérieur* : le BLL a besoin d'un utilisateur, donc le DAL exécute une requête, donc le driver de base de données ouvre une socket. C'est inévitable — la logique métier a vraiment besoin de la base de données.

Mais si le BLL *importe* le DAL pour faire cela, la dépendance pointe vers l'extérieur et la règle est cassée. Donc on les sépare :

- La couche **interne** déclare ce dont elle a besoin, via une interface qu'elle possède : `UserRepository`, avec un `find_by_email` qui prend et renvoie des entités.
- La couche **externe** l'implémente : `DalUser` satisfait cette interface en utilisant SQLAlchemy.
- Quelque chose à la toute périphérie — la **composition root**, souvent là où votre application démarre — lui donne l'implémentation concrète.

Le BLL nomme maintenant une interface qu'il possède et ne nomme plus SQLAlchemy. Le contrôle s'écoule toujours vers l'extérieur au runtime ; la dépendance source pointe vers l'intérieur. **La dépendance au moment de la compilation et la direction d'appel au runtime sont des choses différentes, et inverser l'une sans l'autre est tout le tour de magie.**

En Python, c'est plus léger qu'il n'y paraît : l'interface peut être un `Protocol`, ou dans un petit projet simplement un paramètre de constructeur typé et donné au démarrage. L'important est que le BLL ne fasse pas `import` depuis `dal/`, et qu'un test puisse lui donner un faux.

**Le test qui dit si tu l'as réellement fait :** peux-tu tester unitaire `bll/` sans base de données en cours d'exécution ? Si oui, tu as inversé la dépendance. Si tu as dû démarrer SQLite pour tester une règle métier, tu as dessiné le diagramme mais pas construit l'architecture.

### L'objection du modèle anémique, et que faire à ce sujet

Une critique mérite d'être abordée de front, parce qu'elle est juste.

Tes `entities/` sont des dataclasses — des données sans comportement — et toute la logique vit dans `bll/`. Martin Fowler a nommé cela le **anemic domain model** et le considère comme un anti-pattern :

> Il n'y a presque aucun comportement sur ces objets, ce qui les réduit à de simples sacs de getters et setters.

Et la charge qui pique :

> Ils supportent tous les coûts d'un modèle de domaine, sans produire aucun des bénéfices.

**Deux réponses honnêtes. Sache laquelle tu donnes.**

1. **Pour la plupart des applications, ce compromis est acceptable, et il faut le prendre consciemment.** Si tes règles sont surtout validation, autorisation et orchestration sur plusieurs choses stockées, elles n'appartiennent vraiment pas à un seul objet, et un modèle riche achète une cérémonie plutôt que de la clarté. C'est le cas courant, et le choisir délibérément n'est pas la même chose que dériver vers cela.

2. **Quand le comportement appartient clairement à une entité, mets-le sur l'entité.** Rien dans cette architecture ne l'interdit — une méthode qui n'utilise que les champs propres de l'objet n'importe rien et ne casse aucune règle. `order.total()`, `invoice.is_overdue()`, `booking.overlaps(other)` appartiennent à l'objet. Les déplacer vers un service est la manière dont un modèle devient anémique : pas par design, mais un confort à la fois.

**Règle de bon sens : si la logique n'a besoin que des données propres à cet objet, elle va sur l'objet. Si elle a besoin de la base de données, d'une autre entité ou du monde extérieur, elle va dans `bll/`.**

### Note sur le Domain-Driven Design, pour ne pas les confondre

Tu rencontreras le DDD dans presque tout ce qui est écrit sur Clean Architecture, donc il vaut la peine d'ajouter une courte section pour les distinguer.

**Ce n'est pas le Domain-Driven Design, et tu ne dois pas l'appeler ainsi.**

Le DDD est une discipline différente, sur *comment on arrive à un modèle* via des conversations avec des experts du domaine. Son centre de gravité est stratégique — bounded contexts, subdomains, context mapping — et rien de tout cela n'est ici. Ce que cette architecture partage avec le DDD sont deux de ses plus petits patterns tactiques : le **repository** (ton `dal/`) et la **persistence ignorance** (tes `entities/`). Partager deux patterns avec une discipline ne fait pas de toi un praticien de cette discipline.

Evans lui-même a dit qu'il **avait trop mis l'accent sur ces blocs tactiques**, et que la moitié stratégique est la partie qui compte et que les gens ignorent. Donc un codebase qui adopte des repositories et se dit DDD a adopté précisément la moitié que son auteur pense surpondérée. Dis « Clean Architecture », ce qui est exact, et laisse le DDD signifier ce qu'il signifie.

**Cherche le vrai DDD quand les règles métier sont le vrai défi** — assurance, logistique, finance, facturation de santé — quand des experts du domaine s'affrontent sur ce qu'un mot veut dire et que différentes zones du business ont besoin de modèles différents du même nom. Pour une application CRUD avec un modèle de permissions, il produit des dossiers en forme DDD sans aucun des bénéfices du DDD.

**Une idée du DDD vaut quand même le détour, et tu l'as déjà.** `GLOSSARY.md` — la règle selon laquelle les mots utilisés par les experts du domaine, les mots de tes conversations et les identifiants de ton code source doivent former **un seul vocabulaire** — est le *Ubiquitous Language* du DDD, et c'est probablement l'idée la plus précieuse du livre. Le kit l'applique structurellement : le glossaire est écrit avant le code, les termes de chaque histoire doivent correspondre à une entrée, et `check-project-docs` recherche les mots que tu as retirés. Continue à faire cela. Cela coûte presque rien et c'est là que la vraie valeur du DDD se trouvait.

---

## Partie 3 — Le frontend : Feature-Sliced Design

Le frontend utilise le **Feature-Sliced Design (FSD)** : une méthodologie explicite et documentée en externe, avec sa propre spécification, son linter et son vocabulaire.

### Les couches

```
src/
  app/        providers, router, global styles, point d'entrée
  pages/      une tranche par route — compose widgets et features
  widgets/    blocs composites autonomes (un header, une sidebar, un feed)
  features/   choses qu'un utilisateur *fait* — une action avec son UI et sa logique
  entities/   noms métier — l'utilisateur, la commande, le commentaire
  shared/     ui/ api/ lib/ config/ — réutilisable, agnostique au métier
```

Tu n'as pas à utiliser les six. **Leurs noms sont fixes, cependant** — c'est ce qui rend la structure lisible pour quiconque connaît le FSD. Une petite application peut commencer avec seulement `app/`, `pages/`, `entities/` et `shared/`, puis grandir avec `features/` et `widgets/` quand elle en a besoin.

### Tranches et segments

Dans chaque couche sauf `app/` et `shared/`, le code est divisé en **tranches** nommées selon le domaine métier — `entities/user/`, `features/add-to-cart/`.

Dans chaque tranche, le code est divisé en **segments** nommés selon l'objectif technique :

| Segment | Contient |
|---|---|
| `ui/` | composants, styles, tout ce qui est visuel |
| `api/` | requêtes vers le backend, et les types de ce qui revient |
| `model/` | stores d'état, schémas, logique métier |
| `lib/` | helpers dont la tranche a besoin |
| `config/` | constantes, feature flags |

### La règle d'import, et l'API publique

Deux règles font le vrai travail.

**1. Un module ne peut importer que depuis des couches strictement inférieures.** `pages/` peut utiliser `features/` ; `features/` ne peut jamais utiliser `pages/`. Les cycles deviennent structurellement impossibles.

**2. Une tranche ne peut pas importer une tranche sœur sur sa propre couche.** `features/add-to-cart/` ne peut pas atteindre `features/checkout/`. Si deux features ont besoin de la même chose, cette chose appartient à une couche plus basse — généralement dans `entities/` ou `shared/`.

Chaque tranche expose une **API publique** via un `index.ts` à sa racine, et c'est le seul point d'entrée légal. Atteindre directement `features/checkout/ui/Button.tsx` est une violation, même depuis une couche autorisée à l'importer. L'API publique est ce qui permet de réorganiser le contenu d'une tranche sans toucher au reste.

### Application des règles

```bash
npm i -D steiger @feature-sliced/steiger-plugin
```

Configure `steiger.config.ts` et exécute-le dans la CI. Les règles qui comptent : `fsd/forbidden-imports` (imports ascendants et imports entre tranches), `fsd/no-public-api-sidestep` (contourner un `index.ts`), `fsd/no-layer-public-api`.

C'est la réponse frontend à `test_architecture.py`. Même travail, machine différente.

### Comment cela diffère du backend, dit simplement

**Les deux moitiés de ce kit n'utilisent pas le même principe de structuration, et tu dois le savoir plutôt que le découvrir plus tard.**

| | backend | frontend (FSD) |
|---|---|---|
| Règle | imports unidirectionnels | imports unidirectionnels |
| Direction | **vers l'intérieur**, vers `entities/` — le code le plus abstrait, le plus stable | **vers le bas**, vers `shared/` — le plus réutilisable, le moins spécifique au métier |
| Organisé par | couche technique | tranche métier, *puis* segment technique |
| Inversion de dépendance | oui — le point de la règle | **non**, par conception ; les imports directs descendants sont autorisés |
| Appliqué par | un test pytest | un linter (Steiger) |

Les directions sont vraiment opposées : le backend pointe vers la politique métier, le FSD pointe vers les utilitaires génériques. Le FSD a été décrit comme deux flux de développement se faisant face — le backend construit de bas en haut à partir du domaine, le frontend construit de haut en bas à partir de la page.

**Pourquoi c'est acceptable.** Les deux moitiés ont des pressions différentes. La partie difficile du backend est les règles métier qui doivent rester correctes tandis que l'infrastructure change autour, et la Dependency Rule protège exactement cela. La partie difficile du frontend est que les fonctionnalités se multiplient, les équipes travaillent en parallèle, et *« où va ce fichier ? »* est demandé vingt fois par jour. Le FSD répond directement à cette question, ce que la Dependency Rule ne fait pas.

**Ce qu'ils partagent, et c'est la chose à retenir :** chaque fichier a un ensemble déclaré de dossiers depuis lesquels il peut importer, cet ensemble est écrit, et une machine le vérifie. C'est l'idée transférable. Les noms de couche sont le dialecte local.

### La stack, et où chaque élément vit

| Préoccupation | Choix | Vit dans |
|---|---|---|
| Routage | React Router | `app/` |
| État serveur | TanStack Query | le segment `api/` d'une tranche ; hooks de query à côté des requêtes qu'ils encapsulent |
| État client | Zustand | le segment `model/` de la tranche qui le possède |
| État UI local | `useState` | à l'intérieur du composant |
| Config / providers | React Context | `app/` |

**L'état serveur et l'état client sont des choses différentes, et la distinction est la raison même pour laquelle il y a deux bibliothèques.**
Les données qui vivent sur le serveur et sont *mises en cache* dans le navigateur — une liste, un enregistrement, tout ce qui est récupéré — relèvent de TanStack Query : chargement, erreurs, retries, invalidation et refetching sont tous une seule et même préoccupation et sont résolus. Les données qui n'existent que dans le navigateur — un état d'un panneau de filtres, un formulaire multi-étapes en cours, un élément sélectionné — relèvent de Zustand.

La faute la plus courante pour un débutant est de mettre des données serveur dans un store global et d'écrire manuellement l'invalidation du cache. La seconde est de recourir à un store global pour quelque chose qu'un composant possède seul. Utilise `useState` jusqu'à ce que deux composants non liés aient besoin de la même valeur.

**Le Context est pour la configuration, pas pour un état qui change souvent.** Chaque consommateur se re-render sur chaque changement, donc un thème ou un utilisateur courant est bien, mais une valeur mise à jour en direct ne l'est pas.

### TypeScript

Le frontend est en TypeScript, et la raison est la frontière.

Le segment `api/` est l'endroit où vivent les DTO serveur. Avec les types, « un DTO ne doit pas atteindre l'UI » cesse d'être une convention et devient une erreur de compilation : déclare le type de transport dans `api/`, mappe-le vers ton propre type à la frontière, et ne exporte jamais le type de transport. C'est une garantie plus forte que n'importe quelle règle de chemin linter — et c'est la même garantie que le backend obtient avec `entities/` ne n'ayant pas d'import ORM.

Nomme les deux formes différemment et ne les laisse jamais fusionner : `UserDto` pour ce que le serveur a envoyé, `User` pour ce que ton application pense.

### Ce que `scaffold-frontend-app` pose

Le skill est dans `.claude/skills/scaffold-frontend-app/`, et voici son rôle :

1. `npm create vite@latest -- --template react-ts`, puis Tailwind.
2. Créer `src/{app,pages,widgets,features,entities,shared}`, avec `shared/{ui,api,lib,config}` et un `index.ts` dans chaque tranche créée.
3. Installer React Router, TanStack Query, Zustand ; brancher le router et le `QueryClientProvider` dans `app/`.
4. Installer et configurer `steiger` + `@feature-sliced/steiger-plugin`, et **prouver qu'il échoue sur un import ascendant volontaire** avant de déclarer le succès — un linter que personne n'a vu passer au rouge n'est qu'une affirmation, pas une garantie.
5. Configurer Vitest + Testing Library, avec des tests séparés `pure/` (pas de DOM, et un test important React échoue) et `rendered/`.
6. Créer **aucune** feature, entity ou widget — ce sont des travaux d'histoire, exactement comme le scaffold backend ne crée pas de `dal_*.py`. Il ne crée même pas ces trois dossiers vides : Steiger signale les tranches vides ou insignifiantes, donc les pré-créer vous donne un linter rouge sur un projet où vous n'avez encore écrit rien. **Une couche est créée par la première histoire qui en a besoin.**
7. Vérifier qu'il boot puis faire le rapport.

**Même condition stricte que le scaffold backend** : rien n'est scaffoldé avant accord sur le périmètre et existence des documents.

---

## Partie 4 — Conventions de nommage

Déclare-les dès qu'un langage entre dans ton projet, et étends-les à la première vraie erreur de nommage détectée — pas avant.

### Python

| Type | Convention | Exemple |
|---|---|---|
| Module | `snake_case`, préfixé par sa couche | `dal_user.py`, `bll_billing.py`, `ent_invoice.py` |
| Classe | `PascalCase`, avec le même préfixe | `DalUser`, `BllBilling`, `EntInvoice` |
| Ligne ORM privée | underscore au début | `_UserRow` |
| Fonction, variable | `snake_case` | `find_by_email` |
| Constante | `UPPER_SNAKE_CASE` | `MAX_RETRIES` |
| Booléen | préfixé par `is_` / `has_` / `can_` | `is_active`, `has_paid` |
| Dossier de package | lowercase, pas de underscores | `entities/`, `dal/`, `bll/` |

**Le préfixe de couche vaut l'ugliness.** `dal_user.py` à côté de `bll_user.py` vous dit ce qui est quoi dans un onglet, une stack trace, un résultat de recherche et une revue de code — partout où un simple `user.py` ne le ferait pas. Le coût est réel et le bénéfice est plus grand.

**Une règle dure vient avec cela :** un préfixe de couche ne doit jamais apparaître dans quelque chose qu'un utilisateur lit à l'écran. C'est un aide de navigation interne, pas du vocabulaire.

### TypeScript / React

| Type | Convention | Exemple |
|---|---|---|
| Fichier de composant | `PascalCase.tsx`, nommé d'après son export unique | `UserCard.tsx` |
| Hook | `camelCase.ts`, préfixé `use` | `useCurrentUser.ts` |
| Module pur | `camelCase.ts` | `formatDate.ts` |
| Type / interface | `PascalCase`, pas de préfixe `I` | `User`, pas `IUser` |
| Type de transport | `PascalCase` + `Dto` | `UserDto` |
| Dossier (slice, segment) | `kebab-case` | `features/add-to-cart/` |
| Constante | `UPPER_SNAKE_CASE` | `PAGE_SIZE` |
| Booléen | `is` / `has` / `can` / `should` | `isLoading`, `canEdit` |
| Gestionnaire d'événement | `handleX` où il est défini, `onX` comme prop | `onSubmit={handleSubmit}` |
| API publique | `index.ts` à la racine de chaque tranche | `features/add-to-cart/index.ts` |

Un composant par fichier, nommé comme le fichier. Un fichier exportant trois composants est trois fichiers qui n'ont pas encore été séparés.

### Horodatages, partout

**Stocke et transmet l'UTC. Toujours.** ISO-8601 avec `Z`. Convertis en heure locale dans l'UI et nulle part ailleurs.
C'est une règle à poser dès le premier jour parce que le coût de se tromper n'est pas un bug à corriger — c'est des données stockées qui sont maintenant ambiguës.

### Documents et dossiers

- `SCREAMING_SNAKE.md` pour les documents canoniques où il n'y en a qu'un seul : `PRD.md`, `PLAN.md`, `GLOSSARY.md`.
- `hyphenated-lowercase.md` pour tout ce que tu as en grand nombre, et pour chaque dossier.
- **Les dossiers dont les fichiers représentent un historique les numérotent `NN-name.md`** — `reviews/`, `learnings/`. Le nombre est l'ordre d'écriture du fichier, **assigné une fois et jamais réassigné**, parce qu'une citation dans un ancien commit doit continuer à se résoudre.
- Chaque fichier Markdown s'ouvre avec `created` et `updated` dans le frontmatter YAML, en UTC, et `updated` est estampillé par `.githooks/pre-commit` au lieu d'être maintenu à la main.

### Étendre cette section

Ajoute une ligne ici **à la première vraie erreur de nommage détectée** — un composant nommé de manière incohérente, un horodatage stocké localement, un booléen sans préfixe.
N'invente pas de règles avant que le code n'ait besoin d'elles. Une liste de conventions écrite spéculativement est une liste que personne ne croit.

---

## Partie 5 — La stack recommandée

C'est ce que les scaffolds du kit produisent. **C'est un point de départ, pas une exigence.**

### Backend

| Partie | Choix | Pourquoi précisément |
|---|---|---|
| Langage | **Python 3.12+** | typage qui est maintenant vraiment bon, et la plus grande surface de bibliothèques pour n'importe quel domaine |
| Framework | **FastAPI** | async natif, documentation OpenAPI automatique depuis vos DTO, et validation Pydantic au bon endroit |
| ORM | **SQLAlchemy 2.x**, déclaratif typé | colonnes et relations réelles, donc votre schéma est un vrai schéma plutôt qu'un blob JSON |
| Migrations | **Alembic** | le schéma changera ; la seule question est de savoir si ce changement est documenté |
| Base de données | **SQLite** au départ, **PostgreSQL** quand tu as besoin d'écrivains concurrents | SQLite demande zéro configuration et un seul fichier ; le DAL rend le changement peu coûteux |
| Dépendances | **`uv`** | un seul lockfile, assez rapide pour tourner au démarrage, installe le package editable pour que les imports fonctionnent partout |
| Validation | **Pydantic v2** | DTO qui se valident eux-mêmes à la frontière |
| Tests | **pytest** | avec `pytest-asyncio` en mode auto |

### Frontend

| Partie | Choix | Pourquoi précisément |
|---|---|---|
| Langage | **TypeScript** | c'est ce qui rend la frontière DTO exploitable plutôt qu'aspirationnelle |
| Framework | **React 19** | le plus grand écosystème, et la doc/tooling du FSD l'assume |
| Build | **Vite** | serveur dev instantané, et la chose que supposent tous les guides actuels |
| Styling | **Tailwind CSS 4** | un vocabulaire de tokens au lieu d'une bibliothèque de composants que tu finiras par combattre |
| Routage | **React Router** | la valeur par défaut ; le routing basé sur les fichiers est une décision framework, pas une librairie |
| État serveur | **TanStack Query** | cache, retries et invalidation sont un problème résolu, et les réécrire est l'erreur frontend la plus répétée |
| État client | **Zustand** | petit, non opinionné, pas de cérémonie de provider. Redux Toolkit uniquement pour une grande équipe et une grande app |
| Tests | **Vitest + Testing Library + jsdom** | même config que Vite, pas de deuxième pipeline de build |
| Lint d'architecture | **Steiger** | la règle, vérifiée |

### Ce que coûte un changement

- **Une base de données différente** — presque gratuit, si `dal/` est honnête. C'est le layering qui paie pour lui-même.
- **Un framework Python différent** — une réécriture de `api/`, rien d'autre. Là aussi, c'est le layering qui paie pour lui-même.
- **Un framework frontend différent** — le FSD est agnostique au framework ; les couches et la règle survivent. Les composants ne survivent pas.
- **Abandonner TypeScript** — la frontière `api/` redevient une convention, seulement appliquée par le linter et toi.
- **Abandonner les vérifications d'architecture** — gratuit aujourd'hui, et tu ne pourras pas dire quand cela cesse de l'être. C'est le seul élément de cette liste qu'il ne faut pas prendre.

---

## Partie 6 — Où cela se situe dans ton chemin

```
1. Copie le kit dans ton projet vide              (README.md § Install)
2. Lance le starter prompt                        STARTER_PROMPT.md
       ↓  remplit, une section à la fois, avec tes réponses :
   PRD → NFR → SOLUTION_DESIGN → PLAN → GLOSSARY → PROJECT_WORKFLOW
3. Écris AGENTS.md / CLAUDE.md                    (dérivé, en dernier)
4. Planifie le premier Epic et ses stories        skills: epic, user-story
5. Scaffold le backend                            skill: scaffold-backend-service
6. Scaffold le frontend                           skill: scaffold-frontend-app
7. Construis, une story à la fois
```

**Les étapes 5 et 6 viennent après l'étape 2, et cet ordre est la revendication centrale du kit.**
Scaffolder d'abord signifie choisir tes couches avant de connaître ton domaine, et la couche que tu choisis mal est celle que tu ne remarqueras pas pendant un mois.

Lis `project-docs/learnings/03-backend-layered-architecture-template.md` pour le raisonnement long derrière la Partie 1, et `project-docs/learnings/01-documentation-structure-template.md` pour comprendre pourquoi les documents sont ordonnés comme ils le sont.

---

## Partie 7 — Où lire plus loin

**Tout ce qui suit a été ouvert et vérifié.** Commence en haut de chaque liste ; elles sont ordonnées, pas alphabétiques.

### Clean Architecture — commence ici

**1. [The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)** — Robert C. Martin, ~10 min.
Le post original, et toujours l'énoncé complet le plus court. Si tu lis une seule chose, lis celle-ci. C'est là que vient la phrase de la Dependency Rule dans la Partie 0, et c'est aussi là que le diagramme de cercles concentriques que tout le monde redessine a été dessiné pour la première fois.

**2. [Common web application architectures](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures)** — Microsoft Learn, ~20 min.
**La meilleure explication gratuite avec de vrais diagrammes**, et celle qui fera cliquer la Partie 1. Lis *"What are layers"*, *"Traditional N-Layer architecture"* et *"Clean architecture"*, puis arrête-toi à *"Monolithic applications and containers"* — le reste est Azure et Docker dont tu n'as pas besoin.

C'est écrit en C#, et cela n'a pas d'importance : la section qui enseigne le plus est celle qui explique pourquoi la N-Layer traditionnelle met ta logique métier au-dessus de ta base de données, et comment l'inversion d'une dépendance corrige le problème. Cet argument est indépendant du langage, et leur `UI / BLL / DAL` est exactement ton `api / bll / dal`.

**3. [The Onion Architecture](https://jeffreypalermo.com/2008/07/the-onion-architecture-part-1/)** — Jeffrey Palermo, ~8 min.
Lis ceci pour la *raison*, que la Partie 2 emprunte : les technologies d'accès aux données changent tous les quelques ans, donc elles ne doivent pas être la chose sur laquelle tout le reste repose. C'est court, et l'argument est le plus clair des trois.

**4. [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/)** — Alistair Cockburn, ~15 min.
Le plus ancien des quatre noms et le plus quotable. Valeur lecture une fois pour une idée : *"l'asymétrie à exploiter n'est pas celle entre les côtés gauche et droit de l'application, mais entre l'intérieur et l'extérieur."* Une fois que l'UI et la base de données te semblent du même type de chose, le reste de ce document est évident.

### Quand tu veux aller plus loin

**[Anemic Domain Model](https://martinfowler.com/bliki/AnemicDomainModel.html)** — Martin Fowler, ~6 min.
L'objection que la Partie 2 répond. Lis-la pour décider délibérément, plutôt que d'apprendre plus tard que tu as construit un anti-pattern.

**[Explicit Architecture: how I put it all together](https://herbertograca.com/2017/11/16/explicit-architecture-01-ddd-hexagonal-onion-clean-cqrs-how-i-put-it-all-together/)** — Herberto Graça, ~17 min. **Avancé.**
Le meilleur article sur la manière dont Hexagonal, Onion et Clean se relient. **Attention, car c'est exactement la confusion que la Partie 2 met en garde** : il mélange DDD et CQRS avec eux, ce qui est légitime pour son objectif et *n'est pas* ce que tu construis. Lis-le pour les relations entre les styles d'architecture ; traite le matériel DDD et CQRS comme lecture complémentaire sur autre chose.

*Livres, si tu veux :* Clean Architecture *de Martin (2017) est la version longue du lien 1. Domain-Driven Design* de Evans *(2003) est un sujet différent — lis-le quand ton domaine est vraiment difficile, pas pour comprendre cette organisation.*

### Feature-Sliced Design — le frontend

**1. [Overview](https://feature-sliced.design/docs/get-started/overview)** — ~10 min. Couches, tranches, segments et règle d'import. Toute la méthodologie en une page.

**2. [Tutorial](https://feature-sliced.design/docs/get-started/tutorial)** — un parcours pratique pour construire un clone de Medium, en deux parties : décide d'abord la structure *sur papier*, puis écris-la. Suppose React et TypeScript. **La partie sur papier est la plus précieuse** — décider à quelle couche appartient quelque chose avant de l'écrire est la vraie compétence.

**3. [Public API](https://feature-sliced.design/docs/reference/public-api)** — ~5 min. La convention `index.ts`, et pourquoi la contourner est une violation même depuis une couche autorisée à t'importer.

**4. [Steiger](https://github.com/feature-sliced/steiger)** — le linter. Installe-le dès le premier jour, pas après que la structure s'est déjà dérivée.

### Des alternatives valables existent

**[Bulletproof React](https://github.com/alan2207/bulletproof-react/blob/master/docs/project-structure.md)** — l'alternative principale basée sur les features à FSD : moins de concepts, moins de cérémonie, une règle plus souple. Lis sa section ESLint `import/no-restricted-paths` même si tu utilises FSD — c'est le plus court exemple clair d'application d'une frontière dans les outils JavaScript.

### La documentation de la stack

[FastAPI](https://fastapi.tiangolo.com/tutorial/bigger-applications/) (*Bigger Applications* est la structure de routage que tu veux) · [SQLAlchemy 2.0 ORM](https://docs.sqlalchemy.org/en/20/orm/quickstart.html) · [Alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html) · [uv](https://docs.astral.sh/uv/) · [Pydantic](https://docs.pydantic.dev/latest/) · [Vite](https://vite.dev/guide/) · [TanStack Query](https://tanstack.com/query/latest/docs/framework/react/overview) · [Zustand](https://zustand.docs.pmnd.rs/) · [React Router](https://reactrouter.com/) · [Tailwind](https://tailwindcss.com/docs) · [Vitest](https://vitest.dev/) · [Testing Library](https://testing-library.com/docs/react-testing-library/intro/)

---

*Si un lien ci-dessus est mort au moment où tu le lis, les termes de recherche qui trouveront son remplacement sont : "clean architecture dependency rule", "onion architecture Palermo", "hexagonal architecture ports adapters", "feature-sliced design layers".*
