---
created: 2026-09-08T17:38:40Z
updated: 2026-09-30T16:04:08Z
---

> **Premier apprentissage :** 2026-08-11 18:23:37
> **Dernière mise à jour :** 2026-08-13 18:10:19

## Contexte

Ce fichier est la version extractible et réutilisable d'une taxonomie documentaire qui a émergé après deux sessions complètes de restructuration, d'audit et de nettoyage des références croisées sur un vrai produit multi-service. Il existe pour qu'un *nouveau* projet n'ait pas à redériver cette structure à partir de zéro. Ce fichier est le « quoi », prêt à copier ; le projet dont il a été extrait a sa propre histoire plus longue du *pourquoi* chaque document a mérité sa portée.

Une deuxième annexe, [`02-document-section-reflection-questions.md`](02-document-section-reflection-questions.md), décompose chaque document du tableau ci-dessous en ses sections réelles et donne 3 à 5 questions de réflexion par section — à utiliser lors du démarrage effectif d'un nouveau projet et du remplissage de ces documents, pas simplement pour apprendre la forme.

## Comment cela a été appris

**Déclencheur :** Après un passage d'audit complet fichier par fichier sur un projet en cours, le propriétaire a demandé à « consigner la carte finale » afin que la même structure puisse être reconstruite pour un futur projet « plus ou moins » à partir de ce modèle plutôt qu'à partir de mémoire.

**Déclencheur de l'addendum :** Une demande a suivi pour couvrir aussi la couche *en dessous* de `CLAUDE.md` que le passage original n'avait pas touchée : la distinction entre `CLAUDE.md` et le standard ouvert `AGENTS.md`, comment fonctionnent les fichiers `CLAUDE.md` imbriqués/par dossier, et une représentation complète de ce qui peut vivre dans `.claude/` (règles, compétences, commandes, agents, workflows, hooks, MCP, plugins, worktrees) — parce que le plan était de réutiliser cette structure documentaire exacte pour un second projet plus petit, et que la couche d'extension devait être documentée dès le départ plutôt que redécouverte. Recherché dans la documentation officielle Claude Code du moment plutôt qu'assumé, puisque cette couche change fréquemment entre les versions. Une demande ultérieure dans la même session a intégré directement l'arborescence physique du projet dans ce fichier, de sorte que les règles de convention de nommage déjà présentes en prose se retrouvent à côté d'un vrai exemple concret au lieu de rester abstraites — puis a demandé que cette arborescence soit anonymisée : nom du projet généralisé en `<project-root>/`, noms des Épiques/stories réduits à leur pattern `epic-NNN-<name>`/`US-NNN`, et chaque dossier spécifique à *ce que* ce projet particulier construit (dossiers de service, sa couche de données) supprimé, de sorte que ce qui reste est la forme minimale et vraiment générique de la couche documentation plutôt qu'un instantané d'un produit.

**Le chemin :** La structure ci-dessous n'est pas celle avec laquelle le projet source a commencé. Elle a traversé un vrai renommage Phase→Épique, deux réorganisations de dossiers, une séparation PRD/NFR, un démêlage Workstream-vs-Épique, une restructuration du suivi d'exécution (un `EPIC_EXECUTION.md` plat, des `functional-specs/` et `technical-specs/` séparés, des dossiers Épique et Workstream avec zéros de bourrage), et un audit final de cohérence fichier par fichier qui a détecté une vraie dérive : des tableaux dupliqués, des références croisées de numéros de section périmées, un vocabulaire de statut incohérent, des balises de persona non concordantes, et un document (`GLOSSARY.md`) qui affirmait que son propre tableau était canonique ailleurs tout en contenant une copie complète deux lignes plus bas.

**À avoir en tête :** chacun de ces documents a mérité sa portée à la dure, en ayant d'abord la mauvaise portée et en se faisant prendre à chevaucher autre chose. Copier la *forme* ci-dessous dans un nouveau projet dès le premier jour, c'est bien. Copier du contenu dans le mauvais document, ou ignorer la vérification « est-ce que ça dit déjà ça » avant d'écrire, reproduira exactement la dérive pour laquelle ce nettoyage a été nécessaire.

## La Règle

### L'ensemble de documents, par ordre de dépendance

| # | Document | Répond à | Dépend de |
|---|---|---|---|
| 1 | `GLOSSARY.md` | Que signifie ce terme ? | Rien — à lire en premier quand un terme est ambigu |
| 2 | `PRD.md` | Que construisons-nous, pour qui, pourquoi ? | Glossaire pour le vocabulaire |
| 3 | `NFR.md` | Quel niveau de qualité doit-il atteindre ? | PRD (complémentaire, pas un sous-ensemble) |
| 4 | `SOLUTION_DESIGN.md` | Comment est-il construit ? En quels Workstreams se décompose-t-il ? | PRD + NFR |
| 5 | `PLAN.md` | Dans quel ordre, regroupés en quels Épiques ? | SOLUTION_DESIGN pour les IDs de Workstream |
| 6 | `project-docs/execution/EPIC_EXECUTION.md` | Quel est le statut de chaque story, en ce moment ? | PLAN pour les noms d'Épiques |
| 7 | `project-docs/functional-specs/`, `project-docs/technical-specs/` | Que fait réellement un Workstream livré / comment est-il réellement construit ? | Rédigés progressivement au fur et à mesure que les stories se closent, jamais à l'avance |
| 8 | `project-docs/execution/epic-NNN-*/US-NNN.md` | Qu'est-ce qui a été spécifiquement demandé et accepté pour une unité de travail ? | Rien — l'unité atomique que tout le reste résume |
| 9 | `project-docs/PROJECT_WORKFLOW.md` | Comment le travail circule-t-il réellement dans le système, et quel document toucher quand ? | Tout ce qui précède, c'est le tissu conjonctif |
| 10 | `.claude/skills/<name>/SKILL.md` | La version exécutable du #9, pour une tâche récurrente | PROJECT_WORKFLOW (copie autonome, ne le relit pas à l'exécution) |
| 11 | `CLAUDE.md` | Que doit savoir chaque session avant de toucher quoi que ce soit ? | Tout ce qui précède — c'est le résumé *dérivé*, construit en dernier, pas en premier |

Chaque ligne répond à exactement une question. Si un contenu pouvait répondre aux questions de deux lignes, il appartient à la ligne la plus spécifique, et chaque autre ligne obtient un pointeur au lieu d'une copie.

**Délibérément absent de ce tableau : un document de stratégie de test.** Quel(s) framework(s) de test utiliser et comment les tests fonctionneront réellement n'est pas décidé à l'avance dans ce modèle — cette décision est laissée à émerger une fois qu'il y a du code réel à tester, plutôt que spéculée avant qu'une première ligne de code existe. Si un projet atteint le point où cela doit être décidé, cela atterrirait le plus naturellement comme une nouvelle ligne dans ce tableau, ou se fondrait dans la section Maintenabilité existante de `NFR.md` (qui demande déjà si une suite de tests existe et ce qu'elle couvre) — pas inventé avant qu'il y ait une première ligne de code pour laquelle écrire des tests.

### Conventions de nommage non négociables

- **Workstream** (domaine fonctionnel, non limité dans le temps) : `WS-NN`, deux chiffres avec zéro de bourrage (`WS-00`… `WS-06`). Deux chiffres car un projet ne dépassera pas réalistement 99 domaines fonctionnels — les Épiques et les stories sont un comptage différent, plus rapide, et ont leur propre bourrage.
- **Épique** (étape de construction séquentielle et limitée dans le temps, une active à la fois) : `epic-NNN-name`, dossiers à trois chiffres avec zéro de bourrage (`epic-000-...`, `epic-001-...`).
- **User story** : `US-NNN`, séquentiel sur *l'ensemble du projet*, jamais remis à zéro par Épique, jamais réutilisé.
- **Fichiers spec fonctionnelle/technique** : `ws-func-NN-name.md` / `ws-tech-NN-name.md`, correspondant exactement à l'identifiant à deux chiffres du Workstream.
- **Dossiers de service** (dès qu'un projet se divise en plusieurs services backend/frontend) : `<acteur>-<service>` (ex. `user-backend` / `admin-backend`, ou quel que soit le découpage acteur), toujours en tirets, plat à la racine du dépôt, jamais concaténé, jamais imbriqué sous un dossier parent commun.

### L'arborescence physique des dossiers, modèle générique

Copiez cette forme telle quelle dans un nouveau projet ; seul le contenu de chaque fichier change :

```
<project-root>/
├── README.md                     <- comment un inconnu le fait tourner
├── AGENTS.md                     <- ligne 11 : résumé dérivé, construit en dernier, reste léger
├── CLAUDE.md                     <- import léger d'AGENTS.md, plus notes spécifiques à Claude Code
├── .claude/
│   ├── settings.json             <- versionné : config permissions/hooks
│   ├── settings.local.json       <- gitignored : substitutions personnelles
│   └── skills/
│       └── <skill-name>/SKILL.md <- ligne 10 : version exécutable de PROJECT_WORKFLOW.md, une tâche récurrente
├── .githooks/pre-commit          <- estampille `updated:` sur les markdown mis en stage
│
├── project-docs/                 <- CHAQUE document sur la construction du projet
│   ├── PRD.md                    <- ligne 2 : quoi, pour qui, pourquoi
│   ├── NFR.md                    <- ligne 3 : le niveau de qualité, complémentaire au PRD et non un sous-ensemble
│   ├── SOLUTION_DESIGN.md        <- ligne 4 : architecture, Workstreams (WS-NN), ADRs
│   ├── PLAN.md                   <- ligne 5 : séquencement des Épiques, indexé sur les IDs de Workstream
│   ├── GLOSSARY.md               <- ligne 1 : vocabulaire, à lire en premier quand un terme est ambigu
│   ├── PROJECT_WORKFLOW.md       <- ligne 9 : quel document toucher, et quand
│   ├── _ARCHITECTURE_EXPLAINED.md         <- comment le code est découpé, et pourquoi
│   ├── execution/
│   │   ├── EPIC_EXECUTION.md              <- ligne 6 : statut continu, par story
│   │   ├── epic-000-<name>/               <- dossier Épique à trois chiffres avec zéro de bourrage
│   │   └── epic-001-<name>/US-NNN.md      <- ligne 8 : séquentiel à l'échelle du projet, jamais remis à zéro par Épique
│   ├── functional-specs/ws-func-NN-*.md   <- ligne 7 : deux chiffres, correspond exactement au WS-NN du Workstream
│   ├── technical-specs/ws-tech-NN-*.md    <- ligne 7 : même couplage, côté implémentation
│   ├── reviews/NN-<name>.md      <- ce qui était cru ici et s'est avéré faux
│   ├── learnings/NN-<name>.md    <- ce fichier vit ici
│   ├── templates/user-story.md   <- copié une fois par story
│   └── exploration/              <- recherche brute, conservée telle quelle, jamais citée comme décidée
│
└── <le code source du produit>    <- frontend/, backend/, quoi que ce soit que la chose est réellement
```

**Une règle régit cette disposition : `project-docs/` contient chaque document sur la *construction* du projet, et rien qui *est* le produit.** La racine ne garde que ce qu'une première session doit lire sans qu'on le lui dise.

**Et sans point au début.** Un dossier avec point est un contrat avec l'outillage signifiant *géré par la machine* : `ls` l'omet, l'Explorateur le cache, et la plupart des outils de recherche le sautent sans option — donc les documents derrière l'un sont invisibles à toute vérification de fraîcheur qui fonctionne par grep. `.claude/` est avec point parce que rien ne le recherche et que chaque agent reçoit littéralement ce chemin. Ces documents sont pour un humain.

Où vivent le code source du projet et les dossiers de service (frontend, backend, une couche de données, quel que soit ce que le produit est réellement) est délibérément hors de portée pour ce modèle — c'est spécifique au produit, pas une partie de la forme de documentation réutilisable. Ce fichier standardise la couche documentation assise au-dessus du code ; **`project-docs/_ARCHITECTURE_EXPLAINED.md` est son pendant pour le code lui-même**, et la propre carte des dossiers `AGENTS.md` du projet enregistre la disposition réelle et concrète.

### Les trois axes de suivi de construction, délibérément séparés

- **Workstream** = *quel domaine*. Ne se complète pas. Peut être revisité par un Épique ultérieur.
- **Épique** = *quand, combien à la fois*. Que le projet gère les Épiques séquentiellement (l'un terminé avant que le suivant commence) ou permette une certaine parallélisation est une contrainte spécifique au projet — énoncer-la explicitement, ce n'est pas une propriété universelle d'« Épique ».
- **Milestone** = *ce qui est livré*. La représentation native GitHub d'un Épique, pas un quatrième concept.

### Quel document mettre à jour, et quand (la partie qui prévient la dérive)

Le tableau complet vit dans `project-docs/PROJECT_WORKFLOW.md` § Quel document mettre à jour, et quand — copiez ce tableau mot pour mot dans le `PROJECT_WORKFLOW.md` d'un nouveau projet, puis ajustez uniquement les noms de documents. La version en une ligne : **le détail d'une story est continu, le détail d'un Épique est par Épique, les décisions produit sont par décision, les décisions d'architecture obtiennent une entrée ADR sur place, tout le reste ne se met à jour que quand le fait qu'il énonce change réellement.** Ne jamais mettre à jour selon un calendrier, jamais de façon spéculative.

### Les Architecture Decision Records vivent dans le document de conception de solution

Pas un fichier séparé, pas un dossier séparé. Un seul tableau, à la fin de `SOLUTION_DESIGN.md`, les entrées ne sont jamais supprimées, seulement marquées `Deprecated` avec une date et une raison. Cela maintient « architecture actuelle » et « pourquoi ce n'est pas l'autre chose » dans le même document, là où quelqu'un a réellement besoin des deux en même temps.

### `CLAUDE.md` est construit en dernier, et reste léger

Chaque autre document ci-dessus est une source ; `CLAUDE.md` est le résumé dérivé, toujours chargé. Concrètement : une carte des dossiers, un pointeur vers la stack technique (pas un tableau de stack technique recopié), les contraintes de confidentialité/comportementales propres à ce projet, un ordre de lecture pour la première session (chemin de reprise rapide + chemin d'orientation complète), et une section de pointeurs qui nomme quel document est canonique pour quoi, sans jamais incorporer le contenu de ce document. Visez moins de ~300 lignes. Pour chaque ligne, le test est : supprimer ceci causerait-il une mauvaise action ? Si non, supprimez-le ou transformez-le en pointeur.

### `CLAUDE.md` vs `AGENTS.md`

`AGENTS.md` est un standard ouvert et agnostique aux outils (géré par la Linux Foundation, des dizaines de milliers de dépôts fin 2025) : markdown simple, pas de champs requis, lu nativement par Codex, Cursor, Copilot, Gemini CLI, Aider, Windsurf, et 20+ autres outils. **Claude Code ne lit pas `AGENTS.md` nativement.** Si un dépôt a besoin des deux (plusieurs outils IA en jeu), le pattern supporté est un `CLAUDE.md` léger qui l'importe et ajoute des instructions spécifiques à Claude en dessous :

```markdown
@AGENTS.md

## Claude Code
Utiliser le mode plan pour les modifications dans src/billing/.
```

Un lien symbolique (`ln -s AGENTS.md CLAUDE.md`) fonctionne aussi s'il n'y a rien de spécifique à Claude à ajouter, mais nécessite des droits administrateur sur Windows, donc l'import `@` est le défaut le plus portable.

**Quand utiliser lequel :** un projet mono-outil (seul Claude Code touche le dépôt) n'a besoin que de `CLAUDE.md` — ajouter `AGENTS.md` en plus est une pure duplication sans que rien ne le lise de la même façon. `AGENTS.md` gagne sa place dès qu'un second outil de codage IA rejoint le projet ; à ce moment, il devient la source de vérité partagée et `CLAUDE.md` se réduit à un import plus un court addendum spécifique à Claude.

### `CLAUDE.md` imbriqués et `.claude/rules/`

Deux mécanismes différents pour délimiter les instructions en dessous de la racine du projet, tous deux réels et tous deux utiles à connaître avant de se rabattre sur « tout va dans le `CLAUDE.md` racine » :

- **`CLAUDE.md` imbriqué** (ou `CLAUDE.local.md`) : un `CLAUDE.md` dans un sous-répertoire du répertoire de travail est découvert automatiquement mais chargé **à la demande**, seulement quand Claude lit réellement un fichier dans cette sous-arborescence — pas au lancement de session. Les fichiers `CLAUDE.md` ancêtres (remontant depuis le répertoire courant jusqu'à la racine du système de fichiers) se chargent en entier au lancement à la place, ordonnés racine en premier afin que le fichier le plus spécifique soit lu en dernier. Utilisez ceci pour une sous-arborescence avec un contexte vraiment différent — un dossier de service avec ses propres détails spécifiques à Python qui sont non pertinents en travaillant sur un frontend sans rapport, par exemple.
- **`.claude/rules/*.md`** : le mécanisme frère, délimité par glob de fichiers au lieu de par répertoire. Une règle avec frontmatter `paths:` (ex. `src/api/**/*.ts`) ne se charge que quand Claude lit un fichier correspondant ; une règle sans `paths:` se charge au lancement, même priorité que `.claude/CLAUDE.md`. Préférez ceci quand le découpage est par *type de fichier ou convention* traversant l'ensemble de l'arborescence (ex. « conventions de test », « règles de conception API ») plutôt que par *répertoire*.

Recommandation officielle : sortir du `CLAUDE.md` racine dès qu'il approche ~200 lignes — les longs fichiers se chargent encore en entier mais réduisent l'adhérence aux instructions.

### Le dossier `.claude/`

Tout ce que Claude Code lit qui est spécifique à un projet :

```
.claude/
├── settings.json         versionné   — permissions, hooks, modèle, env, statusLine
├── settings.local.json   gitignored  — substitutions personnelles, même schéma que ci-dessus
├── CLAUDE.md              versionné   — alternative au CLAUDE.md racine, même effet
├── rules/*.md             versionné   — instructions délimitées par sujet, paths: optionnel
├── skills/<name>/SKILL.md versionné   — procédures exécutables pour les tâches récurrentes
├── commands/<name>.md     versionné   — /commande ancienne en fichier unique ; les skills la remplacent
├── agents/<name>.md       versionné   — « sous-agents » : contexte isolé, accès propre aux outils
├── workflows/<name>.js    versionné   — scripts d'orchestration multi-sous-agents
├── output-styles/         versionné   — seulement si l'équipe partage un style personnalisé
└── agent-memory/<agent>/  écrit par Claude — seulement pour les sous-agents avec mémoire
```

Plus deux éléments qui vivent à la racine du projet, pas dans `.claude/` : `.mcp.json` (versionné, serveurs MCP partagés par l'équipe auxquels Claude Code lui-même se connecte) et `CLAUDE.local.md` (gitignored, notes personnelles de projet, frère d'un `settings.local.json` gitignored).

**Collision de nommage à signaler dans tout projet qui définit son propre vocabulaire de domaine « agent »** : `.claude/agents/` est un mécanisme distinct de la plateforme Claude Code (« sous-agents » — un assistant à fenêtre de contexte isolée auquel Claude délègue, ex. un sous-agent de révision de code). Si le propre produit d'un projet a déjà un concept d'« Agent » (un agent IA visible par l'utilisateur, par exemple), dites-le explicitement en conversation et dans le fichier lui-même, car « l'agent » serait sinon un terme surchargé.

### Points d'extension avancés, documentés mais pas toujours adoptés

Quatre éléments supplémentaires de l'écosystème `.claude/`, réels et actuels, pas nécessairement nécessaires pour chaque projet. Documenter la décision de ne pas en adopter un, quand c'est le choix, en fait une décision plutôt qu'une lacune :

| Mécanisme | Ce que c'est | Où il vit | À adopter quand... |
|---|---|---|---|
| **Hooks** | Commandes shell déterministes que Claude Code exécute lors d'événements du cycle de vie (`PreToolUse` peut bloquer complètement un appel d'outil, `PostToolUse` s'exécute après qu'un appel réussit, `SessionStart` se déclenche au lancement/reprise/compactage). Contrairement à `CLAUDE.md`, ceux-ci sont appliqués indépendamment de ce que Claude décide — les règles de paramètres sont appliquées par le client, pas par le jugement de Claude. | Clé `hooks` dans `settings.json` (portée projet, utilisateur ou locale) — pas un dossier séparé | Une règle `CLAUDE.md` continue d'être décrite mais pas suivie de façon fiable (ex. « toujours exécuter le linter avant de committer ») — c'est le signal pour la promouvoir d'instruction consultative à un hook `PreToolUse`/`PostToolUse` appliqué plutôt que d'écrire la phrase une troisième fois |
| **MCP (`.mcp.json`)** | La *propre* config de Claude Code pour se connecter lui-même, en tant qu'outil de codage, à des serveurs MCP externes (GitHub, une base de données, un outil de design) pendant une session. **Collision de nommage à signaler explicitement** : ceci n'a aucun rapport avec une propre architecture de produit MCP-server planifiée d'un projet, le cas échéant — ce seraient des services que le projet construit dans son produit, pas quelque chose que Claude Code le CLI lit pour s'étendre | `.mcp.json` à la racine du projet, versionné, partagé par l'équipe | L'équipe veut que Claude Code lui-même (pas le produit) lise depuis un système externe mi-session — ex. interroger un gestionnaire de tickets en direct au lieu de coller du texte de ticket dans le chat |
| **Plugins** | Un bundle autonome et distribuable de skills + agents + hooks + serveurs MCP (+ serveurs LSP), soit installé depuis une marketplace, soit auto-découvert sans étape d'installation via un manifeste `.claude-plugin/plugin.json` | Un répertoire de plugin, installé au niveau utilisateur ou projet | **La réponse directe à la réutilisation de la structure d'un projet dans un projet frère sans dérive de copier-coller** : une fois qu'une skill ou un ensemble de règles est destiné à être partagé et rester synchronisé entre les dépôts plutôt que dupliqué à la main, emballez-le en un plugin et activez-le dans les deux, au lieu de maintenir deux copies indépendantes |
| **Worktrees** | Checkouts git parallèles isolés (`--worktree`/`-w`, `.claude/worktrees/<name>/`, `.worktreeinclude` pour copier les fichiers gitignored comme `.env` dans chacun, sous-agent `isolation: worktree`) afin que plusieurs sessions éditent sans collision | `.claude/worktrees/` (ajouter à `.gitignore`), `.worktreeinclude` à la racine du projet | Utile dès qu'un modèle de travail de projet permet plusieurs sessions parallèles. **Non applicable** si le modèle de travail déclaré d'un projet est explicitement séquentiel — un agent, une story à la fois, pas de travail parallèle — les worktrees existent spécifiquement pour exécuter des sessions isolées parallèles, le contraire de cette contrainte |

### Ordre de lecture pour une session fraîche

**Reprise rapide :** `project-docs/execution/EPIC_EXECUTION.md`, puis `PLAN.md` § Étapes immédiates suivantes, puis — si un Épique est ouvert — le `epic-NNN-refinement.md` de cet Épique, que `EPIC_EXECUTION.md` nomme.

**La passation est dans les fichiers versionnés, pas dans une note de passation séparée.** Une version antérieure de ce modèle envoyait une session de reprise vers des fichiers scratch gitignored. Les documents suivis battent les notes scratch pour la raison pour laquelle le contrôle de version existe : ils sont révisés, ils sont partagés, et ils ne peuvent pas silencieusement être la copie périmée.

**Orientation complète :** `PRD.md` → `NFR.md` → `SOLUTION_DESIGN.md` → `PLAN.md` → `project-docs/execution/EPIC_EXECUTION.md` → `project-docs/functional-specs/` + `project-docs/technical-specs/` → `project-docs/PROJECT_WORKFLOW.md` + la skill pertinente. `GLOSSARY.md` est une référence permanente en dehors de cette séquence, consultée à la demande.

## Tableau des erreurs courantes

| Erreur | Pourquoi ça arrive | La correction |
|---|---|---|
| Réénoncer un tableau dans un second document « pour commodité » | Semble utile sur le moment | Un emplacement canonique par fait, toujours. Toute autre mention est un pointeur, même si ça signifie un clic supplémentaire |
| Renuméroter une section et s'arrêter une fois que les en-têtes semblent corrects | La correction évidente (les en-têtes) est visible ; les références croisées ne le sont pas | Après toute renumérotation, grep *tout le dépôt* pour les patterns `Section N` / `§N`, pas seulement le fichier modifié, et pas seulement les fichiers qui semblent des « candidats évidents » |
| Inventer une nouvelle convention de formatage au lieu de trouver celle déjà en usage | Plus rapide que de chercher | Grep pour voir comment le même genre de chose est déjà écrit ailleurs avant de formater quelque chose de nouveau |
| Traiter une question réflexive « qu'en pensez-vous » comme une instruction à exécuter | Empressement à être utile | Si le message est formulé comme une question, répondre à la question en premier. Attendre un feu vert explicite avant d'écrire quoi que ce soit |
| Ajouter une dimension de statut/progression à un document censé être intemporel (ex. un glossaire) | Le statut semble du contexte utile | Une définition répond à « qu'est-ce que c'est », pas à « est-ce que c'est construit ». Garder un champ `Statut` séparé et explicite si réellement nécessaire, ne jamais enfouir le statut de livraison dans la prose de définition |
| Laisser le texte propre d'un document non mis à jour après avoir déplacé ce qu'il décrit | Le déplacement lui-même semble être toute la tâche | Si un document dit « la version canonique de X est ici », et que X se déplace, cette phrase doit se déplacer ou être réécrite aussi, c'est une partie du contenu, pas accessoire |
| Supposer qu'un outil agentique lit `AGENTS.md` automatiquement parce qu'il existe dans le dépôt | Les deux fichiers semblent interchangeables et décrivent tous deux « des instructions pour les agents IA » | Claude Code lit uniquement `CLAUDE.md`. Un `AGENTS.md` sans rien qui l'importe via `@AGENTS.md` est invisible pour Claude Code quelle que soit sa complétude |
| Reconstruire manuellement le même ensemble de skills/hooks/règles réutilisables une seconde fois dans un projet frère au lieu de l'empaqueter une fois | Copier-coller un dossier est plus rapide sur le moment que mettre en place un plugin | Une fois qu'un élément de `.claude/` est destiné à être partagé entre dépôts, emballez-le en plugin afin que les deux projets lisent une seule source au lieu de dériver silencieusement |

### Sources

Recherché dans la documentation officielle Claude Code (tout sous `code.claude.com`, vers lequel `docs.anthropic.com/en/docs/claude-code/*` redirige maintenant) :

- [How Claude remembers your project](https://code.claude.com/docs/en/memory) — hiérarchie et ordre de chargement de `CLAUDE.md`, interop `AGENTS.md`, `.claude/rules/`
- [Explore the `.claude` directory](https://code.claude.com/docs/en/claude-directory) — référence complète des fichiers/dossiers `.claude/` au niveau projet et utilisateur
- [Plugins reference](https://code.claude.com/docs/en/plugins-reference) — composants de plugin, portées d'installation, plugins skills-directory (manifest uniquement)
- [Automate actions with hooks](https://code.claude.com/docs/en/hooks-guide) — événements du cycle de vie des hooks, application vs. guidance `CLAUDE.md`, cas d'usage exemples
- [Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp) — portée projet `.mcp.json` vs. portée locale/utilisateur `~/.claude.json`
- [Run parallel sessions with worktrees](https://code.claude.com/docs/en/worktrees) — `--worktree`, `.worktreeinclude`, sous-agent `isolation: worktree`
- [AGENTS.md](https://agents.md/) — la page de spécification du standard ouvert
