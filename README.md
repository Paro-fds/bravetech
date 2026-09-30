---
created: 2026-09-08T17:38:40Z
updated: 2026-09-30T16:04:08Z
---

# Kit d'initialisation du projet

Une structure de départ orientée documentation pour un nouveau projet logiciel, construite avec le **Développement piloté par les spécifications (Specification-Driven Development, SDD)** : on documente le contexte *avant* d'écrire le code, plutôt que d'improviser au milieu d'une conversation avec un agent.

> **Ce dossier est autonome.** Tout ce qu'il faut pour comprendre et utiliser cette structure est inclus ici — rien à récupérer ailleurs. Copie-le tel quel dans l'espace de travail de ton nouveau projet.

## Installe-le en quatre commandes

```bash
# depuis le répertoire vide de ton nouveau projet
cp -r /chemin/vers/project-init-kit/. .      # le ./ final est ce qui copie .claude et .githooks
git init                                     # si tu ne l'as pas déjà fait
git config core.hooksPath .githooks          # ajoute une balise `updated:` à chaque commit de markdown
rm -rf project-init-kit                      # si tu as copié le dossier au lieu de son contenu
```

**Le `/.` final est tout le secret, et le faire faux est la manière la plus courante de tout casser sans bruit.** `cp -r project-init-kit/ .` ignore les dossiers cachés sur la plupart des systèmes, ce qui fait perdre `.claude/` (toutes les compétences) et `.githooks/` (le marquage des horodatages) — et rien ne l'annonce. Sous Windows, pour copier depuis l'Explorateur, il faut d'abord activer *Afficher les fichiers cachés*.

**Vérifie que ça a fonctionné :** `ls -a` doit afficher `.claude` et `.githooks`. Dans Claude Code, `/help` doit lister les compétences ci-dessous.

Ensuite, lis `project-docs/_ARCHITECTURE_EXPLAINED.md`, puis colle `STARTER_PROMPT.md` dans ton agent.

## Pourquoi cela existe

La plupart des projets assistés par un agent dérivent parce que l'agent reçoit tout le produit dans une seule conversation, puis le redéduit à neuf reprises à chaque session. Ce kit suit l'approche opposée : un petit ensemble ordonné de documents qui donne à l'agent le bon contexte au bon moment, pour qu'une session puisse démarrer de manière productive au lieu de réexpliquer le produit à chaque fois.

Il capture aussi un vrai schéma architectural (structure backend en couches — voir `project-docs/learnings/03-backend-layered-architecture-template.md`) utile à réutiliser pour n'importe quel nouveau service backend, et non pas seulement documenté puis oublié.

## Ce qu'il y a dans ce kit

```text
project-init-kit/
├── README.md                        <- ce fichier
├── STARTER_PROMPT.md                <- le prompt à coller dans ton agent pour commencer
├── AGENTS.md / CLAUDE.md            <- construit en dernier, résumé dérivé de tout ce qui suit
├── project-docs/                    <- TOUS les documents sur la construction du projet
│   ├── _ARCHITECTURE_EXPLAINED.md   <- 0. À LIRE EN PREMIER — comment le code est divisé, et pourquoi
│   ├── PRD.md                       <- 1. remplir en premier
│   ├── NFR.md                       <- 2.
│   ├── SOLUTION_DESIGN.md           <- 3.
│   ├── PLAN.md                      <- 4.
│   ├── GLOSSARY.md                  <- 5. finalisé en dernier
│   ├── PROJECT_WORKFLOW.md          <- 6. quel document modifier et quand
│   ├── templates/user-story.md      <- copier ceci pour chaque histoire
│   ├── execution/
│   │   ├── EPIC_EXECUTION.md        <- tableau de suivi, se remplit au fur et à mesure du travail
│   │   └── epic-NNN-slug/           <- un dossier par Épic, contenant ses fichiers US-NNN.md
│   ├── functional-specs/README.md   <- pas de template fixe, rédigé une fois que le comportement réel est en place
│   ├── technical-specs/README.md    <- idem, côté implémentation
│   ├── reviews/README.md            <- ce que tu croyais vrai et qui s'est finalement révélé faux
│   ├── learnings/README.md          <- pratiques réutilisables pour ton prochain projet
│   │   └── 01-, 02-, 03-*.md        <- trois exemples concrets livrés ; les tiens commencent à 04
│   └── exploration/                 <- recherches brutes, conservées telles quelles, jamais citées comme décision finale
├── .githooks/                       <- pre-commit, ajoute `updated:` sur les markdown indexés
│                                       activer une fois : git config core.hooksPath .githooks
└── .claude/skills/                  <- compétences exécutables de Claude Code, voir ci-dessous
    ├── bootstrap-project-docs/      <- le prompt de démarrage, sous forme de compétence
    ├── user-story/                  <- créer/affiner/mettre à jour/supprimer une user story
    ├── epic/                        <- créer/affiner/fermer un Epic
    ├── get-work-status/             <- lecture seule : « où en sommes-nous »
    ├── check-project-docs/          <- vérifie les documents de fondation pour les dérives
    ├── document-learning/           <- écrit un fichier dans project-docs/learnings/ de la bonne manière
    ├── prepare-compact/             <- pousse le vrai travail de la session dans les fichiers d'histoire/suivi/revue, puis vérifie le chemin de reprise
    ├── scaffold-backend-service/    <- crée la structure et le squelette d'un nouveau service backend (+ 12 fichiers modèles)
    └── scaffold-frontend-app/       <- crée une app frontend React + TypeScript
```

## La règle unique que le layout impose

**`project-docs/` contient tous les documents sur la *construction* du projet, et rien qui *est* le produit.** La racine du dépôt ne garde que ce qu'une première session doit lire sans avoir à être guidée : `README.md`, `AGENTS.md`, `CLAUDE.md`.

Cette séparation vaut plus qu'elle n'en a l'air, et elle a été installée dans le projet source seulement après qu'une absence réelle ait causé un échec : documents de produit, documents de processus, matériel pédagogique, journaux de revue, outils et ce kit partageaient tous la même racine et un seul dossier fourre-tout sans règle sur ce qui appartenait à quoi. Une session a ensuite demandé ce que signifiait clôturer un Epic, n'a trouvé rien, et **a proposé d'inventer une procédure qui existait déjà** deux dossiers plus loin. Ce n'est pas un problème de recherche, c'est un problème structurel — et c'est le type de problème qui s'aggrave en silence, parce que tout fonctionne encore, il suffit juste de ne pas trouver l'information.

**`project-docs/` est aussi le nom utilisé par le projet source, et le conserver vaut plus qu'il n'y paraît.** Ce projet avait nommé le dossier d'après lui-même — un mot issu de sa propre langue — pour exactement la même raison que tu pourrais vouloir faire pareil : un dossier nommé d'après le projet se lit comme une signature, alors qu'un dossier nommé `docs` se lit comme quelque chose d'ignorable.

On l'a néanmoins renommé, et la raison vaut un paragraphe avant que tu décides. Un nom qu'il faut expliquer ne peut pas remplir la première mission d'un dossier, qui est de dire à un étranger ce qu'il contient. Et dès que le kit et le projet dont il est issu partagent le même nom, **tous les chemins dans tous les documents se transfèrent sans changement** — il n'y a rien à traduire, donc rien à dériver. C'était important ici : une version précédente de ce kit livrait une structure de dossiers alors que les compétences qui y étaient intégrées supposaient une autre structure, et la partie qui était fausse était exactement celle qu'un étudiant lit en premier.

Renomme-le donc si tu as une raison. Si tu le fais, cherche une fois `project-docs/` et corrige les liens — quelques dizaines, tous dans du markdown — et sache que tu prends en charge la traduction que le nom partagé supprimait.

**Pas de point en tête**, quel que soit le nom que tu choisis. `.project-docs` serait masqué par `ls`, par l'Explorateur, par la plupart des arbres d'éditeur et par de nombreux outils de recherche. `.claude/` est pointé parce qu'une machine le possède ; ces documents sont pour un humain.

## Les compétences, et à quoi elles servent

Ce sont des [compétences Claude Code](https://code.claude.com/docs/en/skills) — elles se chargent automatiquement lorsque leur description correspond à ce qui est demandé, ou peuvent être invoquées par nom. Les neuf supposent les conventions de documents et d'histoires de ce kit.

Elles ont été extraites du fonctionnement d'un vrai projet puis généralisées : vocabulaire propre au projet, précédents et conclusions retirés, et des emplacements de type `[OWNER]/[REPO]` laissés partout où elles touchent GitHub. **Ce qui reste est la procédure et sa raison d'être** — quand une compétence dit que *c'est l'étape qui échoue le plus souvent*, c'est un échec réel qu'une personne a vécu, pas une hypothèse.

| Compétence | Utilise-la pour... |
|---|---|
| `bootstrap-project-docs` | Te questionner section par section pour remplir `PRD.md` → `NFR.md` → `SOLUTION_DESIGN.md` → `PLAN.md` → `GLOSSARY.md` → `PROJECT_WORKFLOW.md`. Même rôle que `STARTER_PROMPT.md`, se charge automatiquement. |
| `user-story` | Créer une nouvelle `US-NNN.md` (+ issue GitHub), **l'affiner** avant de la construire, la mettre à jour ou la supprimer — l'unité de travail du quotidien. |
| `epic` | Créer un nouvel Epic, l'affiner avant d'écrire ses histoires, ou le clôturer (consolidation : document de clôture, paire de spécifications fonctionnelle + technique, vérification de périmé, fermeture de milestone). |
| `get-work-status` | Un aperçu lecture seule de « où on en est » : Epic actuel, dernière histoire terminée, prochaine histoire à construire, éléments non résolus de la dernière session. |
| `check-project-docs` | Auditer `PRD.md`/`NFR.md`/`SOLUTION_DESIGN.md`/`CLAUDE.md`/`GLOSSARY.md` par rapport à ce qui a réellement été construit, et repérer les termes obsolètes qui réapparaissent. Ne fait que rapporter, ne modifie jamais automatiquement. |
| `document-learning` | Écrire ou mettre à jour un fichier dans `project-docs/learnings/` de la bonne manière — en vérifiant d'abord qu'il s'agit bien d'un apprentissage et non d'une revue, et en incluant les vrais échecs plutôt que seulement le résultat propre. |
| `prepare-compact` | Pousser le vrai travail de la session dans les fichiers d'histoire/suivi/revue, puis vérifier que le chemin de reprise documenté nomme bien la prochaine action — de sorte que l'arbre validé soit bien le transfert de contexte. N'écrit aucun fichier de transfert et n'exécute pas `/compact`. |
| `scaffold-backend-service` | Poser la structure de dossier et le squelette d'un nouveau service FastAPI + SQLAlchemy, en utilisant le découpage Clean Architecture de la partie 1 de `_ARCHITECTURE_EXPLAINED.md`. Nécessite que les documents du projet existent déjà. |
| `scaffold-frontend-app` | Poser une application frontend React + TypeScript + Vite selon Feature-Sliced Design, avec Tailwind, React Router, TanStack Query, Zustand, le linter d'architecture Steiger et Vitest configurés — et le linter *prouvé* comme en échec sur une violation avant de rapporter une réussite. Même prérequis. |

**Deux des neuf génèrent du code plutôt que de la documentation** — `scaffold-backend-service` et `scaffold-frontend-app` — et les deux refusent de s'exécuter tant que les documents n'existent pas. C'est précisément le but : scaffolder d'abord signifie choisir tes couches avant de connaître ton domaine.

**Configuration unique** : `user-story` et `epic` font référence à `[OWNER]/[REPO]` et, si tu utilises un tableau GitHub Project, à `[TRACKER_PROJECT_NUMBER]`/`[Tracker Project Name]` — ouvre ces deux fichiers une fois et remplis tes vraies valeurs (ou adapte les étapes spécifiques à GitHub à ce que tu utilises comme suivi, selon `project-docs/PROJECT_WORKFLOW.md` § Work Tracking).

**Pourquoi la *documentation* a cette forme** : `project-docs/learnings/01-documentation-structure-template.md` (méthodologie complète, conventions de nommage) et son annexe `02-document-section-reflection-questions.md` (les questions de réflexion section par section, exactement les mêmes déjà intégrées dans chaque document ci-dessus).

**Pourquoi le *code* a cette forme** : `project-docs/_ARCHITECTURE_EXPLAINED.md` — **Clean Architecture** côté backend et **Feature-Sliced Design** côté frontend, la règle unique derrière chacun, les conventions de nommage, la stack recommandée pour les deux parties, et une liste de lecture vérifiée pour aller plus loin. `03-backend-layered-architecture-template.md` porte la réflexion plus longue côté backend.

Ces trois apprentissages sont livrés comme **exemples concrets de forme**, c'est pourquoi ils sont numérotés `01` à `03` et les tiens commencent à `04`.

## L'ordre dans lequel tu remplis les documents — et pas l'ordre alphabétique

```text
PRD.md                   <- ce qu'on veut, pour qui, pourquoi — LE PREMIER document, ne dépend de rien
       ↓
NFR.md                   <- quelle barre de qualité (peut avancer en parallèle avec le PRD)
       ↓
SOLUTION_DESIGN.md        <- comment c'est construit, dans quels Workstreams
       ↓
PLAN.md                   <- dans quel ordre, regroupé par quels Epics
       ↓
GLOSSARY.md               <- le vocabulaire — commence dès qu'un premier PRD existe, FINALISÉ en dernier
       ↓
project-docs/PROJECT_WORKFLOW.md  <- quel document modifier et quand
```

`_ARCHITECTURE_EXPLAINED.md` n'est pas dans cette séquence parce que **tu ne le remplis pas — tu le lis, puis tu décides.** Il contient déjà des réponses. Ce qu'il te demande, c'est d'accepter ou de remplacer chaque réponse délibérément, puis d'enregistrer ton choix dans `SOLUTION_DESIGN.md` §5, où vit le reste de ton architecture.

**Pourquoi le Glossary n'est pas en premier, malgré l'intuition** : sans savoir encore ce qu'est le produit, tu ne sais pas quel vocabulaire mérite une entrée. Le Glossary peut commencer à se remplir dès qu'une première version de PRD existe, mais il n'est finalisé qu'une fois `PLAN.md` terminé — c'est à ce moment qu'il y a assez de matière pour savoir réellement ce que le produit est. Sa section « Workstream, Epic et Milestone » est l'exception : générique, indépendante du produit, déjà remplie dès le premier jour.

`AGENTS.md` / `CLAUDE.md` et tout ce qui se trouve sous `project-docs/execution/`, `functional-specs/`, `technical-specs/` et `reviews/` **ne sont pas remplis maintenant** : `AGENTS.md`/`CLAUDE.md` sont le résumé *dérivé* de tout le reste, construit en dernier ; le reste se remplit une fois qu'il y a un vrai travail à consigner, pas avant.

## Essaie le PRD sans agent d'abord

**Pour `PRD.md` uniquement** : avant d'ouvrir un agent, prends le temps de répondre toi-même aux questions de réflexion — sur papier, dans un brouillon ou directement dans le fichier. Ce n'est pas une formalité : c'est le but de l'exercice. Un agent peut aider à **formaliser** une réponse que tu as déjà en tête, mais si tu lui demandes de la fournir à ta place, tu rates la vraie compétence que ce document est censé développer : ta propre capacité à penser et à planifier ce que tu construis.

Une fois que le PRD est vraiment ta propre réflexion, repose davantage sur l'agent pour les documents qui suivent (`NFR.md`, `SOLUTION_DESIGN.md`, `PLAN.md`...) — cette aide est plus légitime une fois que la réflexion fondatrice est déjà faite, sur le document qui définit ce que tu construis.

## Remplir les documents avec un agent

Copie le prompt depuis **`STARTER_PROMPT.md`** dans ton agent (ça marche avec n'importe quel outil — Claude Code ou tout autre outil de codage agentique). Il guide l'agent pour poser les questions de chaque document, une section à la fois, dans le bon ordre, sans jamais inventer une réponse à ta place. Si tu utilises Claude Code, la compétence `.claude/skills/bootstrap-project-docs/SKILL.md` fait la même chose et se charge automatiquement.

**Règle à surveiller** : si l'agent commence à rédiger plusieurs documents à la fois sans te poser aucune question, arrête-le et colle à nouveau le prompt — l'objectif n'est pas la vitesse, c'est que le contenu soit vraiment le tien. Et même quand il pose des questions au lieu d'inventer, le vrai objectif est que **tu** aies déjà réfléchi à la réponse, pas que tu l'aies improvisée devant l'agent.

## Une fois les documents remplis

Passe au cycle Explorer → Planifier → Implémenter → Commit : utilise le séquençage des Epics de `PLAN.md` pour choisir le premier Epic, `project-docs/templates/user-story.md` pour écrire sa première histoire, puis construis à partir de là.

**Scaffold le code à ce moment-là, et pas avant** — `scaffold-backend-service`, puis `scaffold-frontend-app`. Créer le squelette trop tôt signifie choisir tes couches avant de connaître ton domaine, et la couche que tu choisis mal est celle que tu ne remarqueras pas pendant un mois. `project-docs/execution/EPIC_EXECUTION.md` commence à suivre le statut dès qu'il existe une première histoire ; `project-docs/functional-specs/` et `project-docs/technical-specs/` commencent une fois que la première histoire est réellement livrée.
