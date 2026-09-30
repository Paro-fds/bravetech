---
created: 2026-09-08T17:38:40Z
updated: 2026-09-30T16:04:08Z
---

> **Premier apprentissage :** 2026-08-13 18:04:50
> **Dernière mise à jour :** 2026-08-13 18:10:19

## Contexte

Annexe à `01-documentation-structure-template.md` : ce fichier enseigne la forme (quel document répond à quelle question, dans quel ordre, disposé physiquement comment) ; le présent fichier décompose chacun de ces documents en ses sections réelles et donne 3 à 5 questions de réflexion par section, pour quiconque démarre un nouveau projet — seul ou en y réfléchissant avec un agent — avant ou pendant la rédaction de cette section.

L'usage prévu : une personne démarrant un nouveau projet lit les questions d'une section, y réfléchit ou les passe en revue avec un agent, et arrive à la session avec suffisamment de clarté pour bien remplir cette section, au lieu de fixer un modèle vide ou de demander à un agent d'en inventer le contenu. Les questions sont l'échafaudage ; les réponses doivent être celles de la personne.

`.claude/skills/*/SKILL.md` est délibérément exclu : une skill est une procédure (comment une tâche récurrente est exécutée), pas quelque chose dans lequel on se réfléchit pour en trouver le contenu.

Également délibérément absent : les questions de réflexion pour un document de stratégie de test, parce qu'un tel document n'existe pas dans le tableau du fichier `01` à décomposer — quel(s) framework(s) de test utiliser et comment les tests fonctionneront réellement est laissé à émerger une fois qu'il y a du code réel à tester, pas décidé de façon spéculative à l'avance. Voir la note correspondante dans `01-documentation-structure-template.md` pour savoir où cette décision atterrirait si un projet atteint le point où elle doit être consignée.

## Comment cela a été appris

**Déclencheur :** Après que le fichier `01` a eu une arborescence physique générique, la couche suivante vers le bas a été demandée : pour chaque document dans le tableau de dépendances du fichier `01`, lister ses sections réelles, trier chacune en « générique — réutiliser telle quelle » vs. « spécifique à ce projet — voici la version généralisée », et attacher 3 à 5 questions de réflexion par section. Un soin particulier a été demandé pour `PRD.md` spécifiquement, puisqu'il tend à avoir le plus de sections qui n'ont de sens que pour un type particulier de produit.

**Le chemin :** Les en-têtes de section réels de chaque document vivant d'un projet en cours ont été extraits (`GLOSSARY.md`, `PRD.md`, `NFR.md`, `SOLUTION_DESIGN.md`, `PLAN.md`, `project-docs/execution/EPIC_EXECUTION.md`, `project-docs/functional-specs/`, `project-docs/technical-specs/`, une story `US-NNN.md`, `project-docs/PROJECT_WORKFLOW.md`, `CLAUDE.md`) plutôt que reconstruits de mémoire, car une liste de sections périmée ici serait pire que pas de liste.

**À avoir en tête :**
- Deux documents ne correspondent pas du tout à la forme « liste de sections fixes » et sont traités différemment ci-dessous plutôt que forcés dans celle-ci : `project-docs/execution/EPIC_EXECUTION.md` est un suivi dérivé, pas rédigé via réflexion — il se remplit automatiquement au fur et à mesure que les Épiques de `PLAN.md` avancent. `project-docs/functional-specs/` et `project-docs/technical-specs/` n'ont pas de modèle fixe — leurs propres stubs README le confirment — les sections sont décidées par Workstream selon ce qui doit réellement être documenté une fois que le comportement/l'implémentation réel existe, créées progressivement, jamais à l'avance.
- Certaines sections sont genuinement conditionnelles, pas seulement « généralisables » — la section Voix et Persona de `PRD.md`, par exemple, ne s'applique que si le produit a un composant conversationnel ou de voix de marque du tout. Marquer une section « N/A, passer » est lui-même une catégorie utile, distincte de « générique, garder » et « spécifique, généraliser ».
- `NFR.md` n'a presque pas eu besoin de généralisation — ISO 25010 est déjà un modèle de qualité agnostique au projet. Cette asymétrie (NFR change à peine, PRD change beaucoup) vaut elle-même la peine d'être remarquée : plus un document décrit *ce qu'est ce produit spécifique*, moins ses sections exactes sont portables ; plus il décrit *un niveau de qualité ou un processus*, plus il est portable.

## La Règle

Chaque entrée ci-dessous : le document, son objectif (du tableau du fichier `01`), ses sections marquées **Générique** (réutiliser l'en-tête tel quel), **Généraliser** (un en-tête trop spécifique à un produit — une version réutilisable est donnée), ou **Conditionnel** (inclure uniquement si cela s'applique à votre produit du tout) — suivies de questions de réflexion par section générique/généralisée.

---

### 1. `GLOSSARY.md` — que signifie ce terme ?

Les en-têtes de catégorie d'un glossaire sont façonnés par le produit qu'il décrit — ne copiez pas les *noms* de catégorie d'un produit à un autre, copiez le pattern sous-jacent :

| Catégorie (généralisée) | Exemple d'instanciation |
|---|---|
| **Acteurs et rôles** — qui ou quoi interagit avec le système dans une capacité distincte | Agents, profils de visiteurs, modes de fonctionnement |
| **Composants système** — les pièces exécutées ou déployées indépendamment | Frontends, services backend |
| **Entrepôts de données** — où l'information persiste réellement | Bases de données, caches, stockages de fichiers |
| **Vocabulaire du domaine** — termes de processus/contenu qu'un outsider mal interpréterait | Types de contenu, processus, termes d'auth/accès |
| **Workstream, Épique et Milestone** — Générique, réutiliser verbatim | idem |
| **Documents du Projet** — Générique, pattern uniquement avec pointeurs | idem |

**Acteurs et rôles**
1. Qui ou quoi touche ce système, et chacun a-t-il besoin de capacités, accès ou niveaux de confiance différents ?
2. Y a-t-il un mot (comme « utilisateur » ou « agent ») qui pourrait signifier deux choses différentes selon le contexte ici ? Doit-il être scindé en deux termes ?
3. Y a-t-il des modes ou intentions distincts dans lesquels le même acteur peut se trouver, qui méritent d'être nommés séparément ?

**Composants système**
1. Quels sont les composants exécutés ou déployés indépendamment de ce système ?
2. Deux composants ont-ils des noms similaires qui pourraient être confondus ? Qu'est-ce qui distingue chacun en une phrase ?
3. Y a-t-il une distinction naturelle qui mérite d'être nommée comme catégorie (public vs. privé, toujours actif vs. à la demande) ?

**Entrepôts de données**
1. Où l'information persiste-t-elle réellement, et combien d'entrepôts distincts y a-t-il ?
2. Un entrepôt contient-il plus d'un type de données qui devrait être nommé séparément ?
3. Quel entrepôt, s'il était perdu, serait le plus dommageable ?

**Vocabulaire du domaine**
1. Quels noms ou noms de processus récurrents un outsider mal interpréterait-il sans définition ?
2. Quels termes sont constamment utilisés dans les conversations sur ce projet mais ne sont pas évidents à partir du seul mot ?
3. Y a-t-il un terme emprunté à un domaine plus large (ex. « épique », « token ») qui signifie quelque chose de plus précis ici ?

**Workstream, Épique et Milestone**
1. Ce projet a-t-il genuinement besoin des trois axes — domaine fonctionnel / étape séquentielle limitée dans le temps / point de livraison — ou est-il assez petit pour que deux s'effondrent en un ?
2. Quels sont les vrais Workstreams (domaines fonctionnels) de ce projet, indépendamment de l'ordre dans lequel chacun sera travaillé ?

**Documents du Projet**
1. Quel document unique est la carte canonique de chaque autre document, pour que ceci reste un pointeur et jamais une deuxième copie ?

---

### 2. `PRD.md` — que construisons-nous, pour qui, pourquoi ?

La section qui mérite le plus d'être repensée par projet. Un produit d'agent conversationnel, une application de suivi de données et un tableau de bord CRUD ont besoin de sous-ensembles différents — généraliser ou marquer conditionnel en conséquence :

| Section | Traitement |
|---|---|
| 1. Énoncé du Produit | Générique |
| 2. Audience | Générique |
| 3. Scénario Idéal de Bout en Bout | Générique |
| 4. Jobs to Be Done | Générique |
| 5. Expérience Produit en Couches | Générique (autant de niveaux d'accès/capacité qu'il en existe réellement — peut être un, peut être plusieurs) |
| 6. Ce que le Produit Peut Faire | Générique |
| 7. Ce que le Produit Ne Doit Jamais Faire | Générique — précieux pour tout produit avec des composants automatisés ou de données sensibles |
| 8. Voix et Persona | **Conditionnel** — seulement s'il y a un composant conversationnel ou de voix de marque ; à omettre entièrement sinon |
| 9. Modèle d'Accès | Générique |
| 10. Observabilité | Générique |
| 11. Critères de Succès | Générique |
| 12. Critères d'Échec / Bloquants au Lancement | Générique |
| 13. Hors Périmètre — V1 | Générique |
| 14. Documents Liés | Générique |

**Énoncé du Produit**
1. En une ou deux phrases, que fait réellement ce produit, et pour qui est-il ?
2. Quel problème réel résout-il ? Résout-il plus d'un problème distinct pour plus d'une audience distincte ?
3. Pourquoi cela doit-il exister maintenant, pour cette personne, plutôt que d'être résolu d'une autre façon ?

**Audience**
1. Qui utilisera ou rencontrera réellement ceci, dans chaque capacité distincte, pas seulement l'utilisateur « principal » ?
2. Y a-t-il une philosophie derrière qui obtient l'accès et qui ne l'obtient pas ?
3. Quelle audience compte le plus si leurs besoins entrent en conflit avec ceux d'une autre audience ?

**Scénario Idéal de Bout en Bout**
1. Parcourez, étape par étape, la meilleure expérience possible qu'une vraie personne vit, du premier contact au résultat voulu.
2. Qu'est-ce qui doit être vrai à chaque étape pour que ce scénario se produise réellement ?
3. Où dans ce parcours l'expérience s'effondrerait-elle aujourd'hui si rien d'autre n'était construit ?

**Jobs to Be Done**
1. Qu'est-ce que l'utilisateur essaie d'accomplir, indépendamment de toute fonctionnalité que vous pourriez construire ?
2. Pour chaque job, que fait l'utilisateur aujourd'hui sans ce produit ?
3. Quel job, s'il reste non résolu, rend tout le produit inutile ?

**Expérience Produit en Couches**
1. Ce produit a-t-il plus d'un niveau d'accès ou de capacité ? Combien, concrètement ?
2. Que peut voir ou faire chaque niveau que le niveau en dessous ne peut pas ?
3. Une limite de niveau ici concerne-t-elle la confiance et la sécurité, ou simplement la richesse des fonctionnalités ?

**Ce que le Produit Peut Faire**
1. Listez les capacités concrètes qu'un utilisateur peut invoquer, une par ligne, en verbes simples.
2. Pour chaque capacité, qu'est-ce qui la déclenche, et quel est le résultat réel ?
3. Y a-t-il une capacité que tout le monde supposera existante qui n'est pas réellement prévue ? Vaut la peine de l'énoncer explicitement hors périmètre maintenant.

**Ce que le Produit Ne Doit Jamais Faire**
1. Qu'est-ce qui serait activement nuisible, embarrassant ou dangereux si ce produit le faisait, même une fois ?
2. Y a-t-il des sujets, des données ou des actions qui doivent toujours être redirigés vers un humain plutôt que traités automatiquement ?
3. Quel est le pire abus plausible, et ce document dit-il ce qui se passe quand quelqu'un l'essaie ?

**Voix et Persona** *(à omettre si non applicable)*
1. Ce produit « parle-t-il » directement à quelqu'un — chat, notifications, copie générée ? Si non, cette section ne s'applique pas.
2. Si oui, quelle voix est-ce : celle d'une entreprise, d'un persona, du fondateur lui-même ?
3. Quel ton semblerait faux pour ce produit même s'il est factuellement exact ?

**Modèle d'Accès**
1. Comment quelqu'un passe-t-il de « pas d'accès » à « a accès » ? Qui l'approuve, le cas échéant ?
2. Qu'est-ce qui est stocké sur qui a accès, et qui peut le révoquer ?
3. Y a-t-il une différence entre « connecté » et « suffisamment fiable pour tout voir » ?

**Observabilité**
1. Une fois que c'est en ligne, quelle est la première question à laquelle vous voudrez répondre sur la façon dont c'est réellement utilisé ?
2. Qu'auriez-vous besoin de remarquer rapidement si quelque chose commençait à mal tourner ?
3. Qui consulte ces données, et à quelle fréquence ?

**Critères de Succès**
1. Comment saurez-vous, concrètement, que ce produit fonctionne comme prévu ?
2. Le succès est-il mesuré par l'utilisation, par un résultat pour l'utilisateur, ou par votre propre jugement ?
3. Quelle est la version minimale du « succès » qui rendrait quand même cela valable d'avoir livré ?

**Critères d'Échec / Bloquants au Lancement**
1. Qu'est-ce qui doit être vrai avant que cela soit autorisé à aller en production, de façon non négociable ?
2. Qu'est-ce qui vous ferait redescendre cela après le lancement ?
3. Y a-t-il une différence ici entre « pas encore parfait » et « vraiment bloquant » ?

**Hors Périmètre — V1**
1. Qu'est-ce que vous ne construisez délibérément pas encore, bien que ce soit lié ?
2. Que diriez-vous à quelqu'un qui demande « pourquoi est-ce que ça ne fait pas X » pour chaque élément exclu ?
3. Quelque chose d'exclu ici est-il susceptible d'être supposé inclus par un premier lecteur ?

**Documents Liés**
1. De quels autres documents un nouveau lecteur a-t-il besoin, et dans quel ordre ?
2. Y a-t-il une carte canonique unique de chaque document du projet, ou cette liste risque-t-elle de devenir une deuxième copie qui dérive ?

---

### 3. `NFR.md` — quel niveau de qualité doit-il atteindre ?

Tout Générique — ISO 25010 est un modèle de qualité agnostique au projet. La seule modification par projet est quel régime réglementaire s'applique réellement dans Conformité/Légal.

**Performance**
1. Quel temps de réponse semblerait cassé à un vrai utilisateur ?
2. Y a-t-il un moment de pic de charge connu (un lancement, une heure spécifique) ?
3. Qu'est-ce qui est réellement mesuré — chargement de page, latence API, autre chose ?

**Fiabilité / Disponibilité**
1. Que signifie « en panne » pour ce produit, précisément ?
2. Un temps d'arrêt est-il acceptable, et quand ?
3. Quel est le plan si une dépendance dont il dépend tombe en panne ?

**Scalabilité**
1. Que se passe-t-il si l'utilisation augmente de 10x du jour au lendemain ?
2. Quelle ressource s'épuise en premier ?
3. La scalabilité est-elle un risque réel à court terme ici, ou une hypothèse pour V1 ?

**Sécurité**
1. Quelle est la chose la plus sensible que ce système détient ?
2. Qui ne doit jamais pouvoir y accéder ?
3. Quel est le scénario de violation dans le pire cas, et est-il surmontable ?

**Utilisabilité / Accessibilité**
1. Qui pourrait avoir du mal à utiliser ceci tel que conçu — appareil, langue, capacité ?
2. Y a-t-il un standard d'accessibilité minimum ciblé ?
3. Quelle est la tâche la plus simple qu'un premier utilisateur doit pouvoir accomplir sans aide ?

**Compatibilité**
1. Sur quels environnements (navigateurs, appareils, OS) cela doit-il réellement fonctionner ?
2. Y a-t-il un environnement explicitement non supporté ?
3. Doit-il interopérer avec un système existant ?

**Conformité / Légal**
1. Quelle réglementation s'applique à ces données ou à cette audience ?
2. Quel consentement ou divulgation est légalement requis avant de collecter des données ?
3. Qui est responsable si quelque chose tourne mal ?

**Maintenabilité**
1. Quelle est la facilité pour une personne future, y compris vous-même futur, de modifier ceci en toute sécurité ?
2. Quel est le plan pour maintenir la documentation synchronisée avec le code ?
3. Y a-t-il une suite de tests, et que couvre-t-elle réellement ?

**Portabilité**
1. Cela pourrait-il passer à un hôte ou fournisseur différent sans réécriture complète ?
2. Y a-t-il quelque chose codé en dur pour un fournisseur qui ne devrait pas l'être ?

**Observabilité / Monitoring**
1. Sur quoi voudriez-vous être alerté immédiatement si cela tombait en panne ?
2. Qu'est-ce qui est consigné aujourd'hui par rapport à ce qui devrait l'être ?
3. Qui surveille réellement ceci ?

**Reprise après Sinistre / Sauvegarde**
1. Quel est le pire scénario de perte de données, et comment vous en remettriez-vous ?
2. À quelle fréquence les données sont-elles sauvegardées, et la restauration a-t-elle jamais été réellement testée ?
3. Quelle est la quantité acceptable de perte de données (RPO) et de temps d'arrêt (RTO) ?

**Risques et Atténuations**
1. Qu'est-ce qui est le plus susceptible de mal tourner avant que cela ne soit livré ?
2. Pour chaque risque, quel est le plan s'il se produit quand même ?
3. Quel risque, s'il se réalise, serait le plus difficile à surmonter ?

**Dépendances**
1. De quels services externes, bibliothèques ou personnes cela dépend-il pour fonctionner ?
2. Que se passe-t-il si l'un devient indisponible ou change son API ?
3. Y a-t-il un point unique de défaillance parmi ceux-ci ?

---

### 4. `SOLUTION_DESIGN.md` — comment est-il construit, et en quels Workstreams se décompose-t-il ?

| Section | Traitement |
|---|---|
| 1. Objectif et Périmètre | Générique |
| 2. Workstreams | Générique — la définition canonique de l'ID de Workstream |
| 3. Vue d'Ensemble du Système | Générique |
| 4. Carte des Composants (services/ports, diagramme, liste d'outils) | Pattern générique ; les contenus spécifiques sont toujours propres au produit |
| 5. Stack Technique | Générique |
| 6. Couche de Données | Pattern générique ; le découpage des entrepôts spécifiques est propre au produit |
| 7. Flux d'Authentification et d'Autorisation | **Conditionnel** — seulement si le produit a un contrôle d'accès du tout |
| 8. Architecture Temps Réel / Interactive | **Conditionnel** — seulement s'il y a une couche live ou streaming |
| 9-10. Boucle de Mise à Jour ou de Feedback Automatisée | **Conditionnel** — seulement si le contenu/comportement se met à jour automatiquement plutôt que par édition manuelle |
| 11. Vue d'Ensemble du Déploiement | Générique |
| 12. Hypothèses | Générique |
| 13. Hors Périmètre | Générique |
| 14. Architecture Decision Records | Générique — réutiliser le pattern de tableau ADR verbatim |
| 15. Questions Ouvertes | Générique |

**Objectif et Périmètre**
1. De quoi ce document est-il responsable de décider qu'aucun autre document ne décide ?
2. Qu'est-ce qui est explicitement hors de l'autorité de ce document (ex. les décisions produit appartiennent au PRD) ?

**Workstreams**
1. Quels sont les domaines fonctionnels indépendants de ce système, indépendamment de l'ordre de construction ?
2. Deux Workstreams pourraient-ils jamais être travaillés par des personnes différentes en même temps sans se marcher dessus ?
3. Y a-t-il un Workstream caché dans un autre qui mérite son propre ID ?

**Vue d'Ensemble du Système**
1. En quelques phrases, comment les pièces majeures s'assemblent-elles de bout en bout ?
2. Quel est le diagramme ou flux unique qui expliquerait ceci le plus rapidement à un nouvel ingénieur ?

**Carte des Composants**
1. Quels sont les composants réels exécutables/déployables, et que possède chacun ?
2. Quels ports, URLs ou points d'entrée chacun expose-t-il ?
3. Y a-t-il un composant ici qui est vraiment deux composants prétendant en être un ?

**Stack Technique**
1. Quelle est la stack pour chaque partie majeure du système, et pourquoi ce choix spécifiquement ?
2. Y a-t-il un élément de la stack qui est un placeholder/approximation plutôt qu'une vraie décision encore ?

**Couche de Données**
1. Où chaque type de données vit-il réellement, et sous quelle forme ?
2. Quel entrepôt est la source de vérité si deux entrepôts pouvaient être en désaccord ?
3. Quel est le schéma ou contrat, suffisamment précis pour que deux implémentations ne dérivent pas ?

**Flux d'Authentification et d'Autorisation** *(à omettre s'il n'y a pas de contrôle d'accès)*
1. Étape par étape, comment quelqu'un passe-t-il d'anonyme à authentifié à autorisé pour une action spécifique ?
2. Qu'est-ce qui est émis (un token, une session, une clé), et qu'est-ce que cela prouve réellement ?

**Architecture Temps Réel / Interactive** *(à omettre si rien n'est live/streaming)*
1. Qu'est-ce qui doit se produire en temps réel par rapport à ce qui peut être requête/réponse ?
2. Quel est le plan de secours si le canal temps réel se coupe en milieu d'interaction ?

**Boucle de Mise à Jour ou de Feedback Automatisée** *(à omettre si le contenu ne change que par édition manuelle)*
1. Est-ce que quelque chose à propos de ce système se met à jour lui-même en fonction de l'utilisation ou de nouvelles données ? Qu'est-ce qui le déclenche ?
2. Qui révise un changement automatisé avant qu'il ne soit mis en production, le cas échéant ?
3. Quelle est la pire chose qu'une boucle de mise à jour automatisée pourrait faire si laissée sans surveillance ?

**Vue d'Ensemble du Déploiement**
1. Où cela s'exécute-t-il réellement aujourd'hui, et où s'exécutera-t-il au lancement ?
2. Quel est le chemin d'un changement local vers son entrée en vigueur ?
3. Y a-t-il une étape CI/CD, et qu'est-ce qu'elle contrôle réellement ?

**Hypothèses**
1. Qu'est-ce que cette conception suppose être vrai et qui n'a pas encore été réellement vérifié ?
2. Quelle hypothèse, si elle s'avère fausse, forcerait une reconception plutôt qu'un patch ?

**Hors Périmètre**
1. Qu'est-ce qui est architecturalement exclu de cette version, et pourquoi ?
2. Y a-t-il quelque chose d'exclu ici qu'un Workstream ultérieur devra revisiter ?

**Architecture Decision Records**
1. Qu'est-ce qui a été décidé et aurait pu aller dans l'autre sens de façon plausible ?
2. Pourquoi l'autre option a-t-elle été rejetée, suffisamment précisément pour que quelqu'un ne la propose pas à nouveau sans le savoir ?
3. Cette décision est-elle encore d'actualité, ou a-t-elle besoin d'une entrée `Deprecated` avec une raison ?

**Questions Ouvertes**
1. Qu'est-ce qui est genuinement non résolu en ce moment qui ne devrait pas bloquer le démarrage, mais ne devrait pas non plus être oublié ?
2. Qui ou quoi résoudrait chaque question ouverte, et quand ?

---

### 5. `PLAN.md` — dans quel ordre, regroupés en quels Épiques ?

Toutes les sections Génériques (patterns de séquencement/priorisation, pas de contenu propre au produit).

**Vue d'Ensemble des Épiques**
1. Dans quel ordre les domaines fonctionnels seront-ils réellement travaillés, et pourquoi cet ordre ?
2. Un Épique est-il bloqué par la fin d'un autre ?
3. Deux Épiques peuvent-ils genuinement s'exécuter en parallèle, ou le séquentiel est-il vraiment requis ici — et pourquoi ?

**Jobs to Be Done — Référence**
1. Chaque Job to Be Done correspond-il à exactement un Épique, ou un job s'étend-il sur plusieurs ?
2. Cette table est-elle encore juste un pointeur vers les vraies définitions JTD du PRD, ou le contenu a-t-il commencé à y être dupliqué ?

**Priorisation MoSCoW**
1. Pour chaque Job to Be Done, qu'est-ce qui est vraiment Must-have par rapport à Should/Could/Won't pour V1 ?
2. Quel est le coût d'avoir tort sur quelque chose marqué Must-have qui s'avère ne pas être nécessaire ?
3. Quelque chose marqué Won't-have est-il susceptible d'être demandé de toute façon — vaut-il la peine de l'énoncer explicitement plutôt que de le supprimer silencieusement ?

**Sections de détail par Épique**
1. Que livre cet Épique que le précédent ne livrait pas ?
2. Quel(s) Workstream(s) touche-t-il principalement ?
3. Quel est l'objectif en une phrase qu'une partie prenante pourrait répéter correctement ?

**Étapes Immédiates Suivantes**
1. Quelle est la toute prochaine action concrète, pas une reformulation de toute la feuille de route ?
2. Cette section est-elle susceptible de devenir périmée rapidement — le statut au jour le jour devrait-il vivre dans un suivi dédié à la place ?

---

### 6. `project-docs/execution/EPIC_EXECUTION.md` — quel est le statut de chaque story, en ce moment ?

Pas rédigé via réflexion — c'est un suivi dérivé, rempli automatiquement au fur et à mesure que les Épiques de `PLAN.md` avancent et que les stories se closent. Pas de contenu à brainstormer ; seulement une vérification de processus :

1. Ce tableau est-il encore vrai en ce moment, ou le statut d'une story a-t-il changé sans que ce fichier soit mis à jour ?
2. Chaque Épique dans `PLAN.md` a-t-il une section correspondante ici, dans le même ordre ?

---

### 7. `project-docs/functional-specs/` et `project-docs/technical-specs/` — que fait réellement un Workstream livré / comment est-il réellement construit ?

Aucun modèle de section fixe n'existe pour l'un ou l'autre — confirmé par le stub README de chaque dossier. Les sections sont décidées par Workstream, progressivement, une fois que le comportement ou l'implémentation réel existe à documenter ; les écrire à l'avance serait de la spéculation. Utilisez ces questions pour décider *si une section est nécessaire du tout*, pas pour remplir une liste fixe :

**Spec fonctionnelle (comportement)**
1. Qu'est-ce qu'un utilisateur ou un système appelant observe maintenant qu'il ne pouvait pas observer avant que ce Workstream existe ?
2. Quels sont les cas limites ou conditions de refus que quelqu'un construisant à partir de ceci doit connaître ?
3. Y a-t-il une règle ici qui n'est pas évidente en lisant le code — une règle métier, une frontière de confidentialité, une exigence d'ordre ?

**Spec technique (implémentation)**
1. Que devrait savoir un nouvel ingénieur pour modifier ceci en toute sécurité sans casser un invariant ?
2. Quel est le contrat de données exact, le schéma ou la règle de nommage, suffisamment précis pour que deux implémentations ne dérivent pas l'une de l'autre ?
3. Quelle décision ici était suffisamment non évidente pour que quelqu'un pourrait la « corriger » en la rétablissant à la mauvaise chose plus tard ?

**Question directrice pour les deux :** une story de ce Workstream a-t-elle réellement été close ? Si non, il n'y a rien de réel à documenter — attendre.

---

### 8. `project-docs/execution/epic-NNN-*/US-NNN.md` — qu'est-ce qui a été spécifiquement demandé et accepté pour une unité de travail ?

Déjà entièrement générique (le format de user story partagé) — le seul lien par projet est que le « rôle » doit être un vrai rôle de *votre* Glossaire, pas celui d'un projet exemple.

**En tant que / Je veux / Afin que**
1. Qui veut spécifiquement ceci — quel rôle nommé du Glossaire, pas juste « un utilisateur » ?
2. Que veulent-ils pouvoir faire, en une phrase ?
3. Pourquoi ce résultat compte-t-il pour eux, pas seulement pour vous en tant que constructeur ?

**Contexte**
1. Qu'est-ce qui existe déjà sur quoi cela s'appuie ?
2. Qu'est-ce qui ne devrait explicitement *pas* être supposé comme déjà fait ?

**Critères d'acceptation**
1. Quel est le plus petit énoncé testable qui est sans ambiguïté vrai ou faux une fois ceci fait ?
2. Y a-t-il un CA ici qui est en réalité une Tâche déguisée — une étape d'implémentation, pas un résultat observable ?

**Hors périmètre**
1. Qu'est-ce qui est adjacent à cette story qu'un lecteur pourrait supposer inclus, mais qui ne l'est pas ?

**Tâches**
1. Quelle est la prochaine action concrète, dans un ordre qui pourrait réellement être suivi du début à la fin ?

**Définition de Terminé**
1. Que vérifie la personne qui a demandé ceci, de ses propres yeux, pour l'accepter ?

**Notes telles que construites**
1. Qu'est-ce qui a changé entre ce qui était prévu et ce qui a réellement été construit, et pourquoi ?

---

### 9. `project-docs/PROJECT_WORKFLOW.md` — comment le travail circule-t-il réellement, et quel document toucher quand ?

| Section | Traitement |
|---|---|
| Quel document mettre à jour, et quand | Générique — le tableau du tissu conjonctif |
| Suivi du Travail | Pattern générique, conditionnel à l'outil réellement utilisé |
| Format de User Story | Générique — pointeur vers le modèle partagé, voir §8 ci-dessus |
| Définition de Terminé | Générique |
| Référence Vocabulaire | Générique |
| Étapes de Bootstrap du Suivi | Pattern générique |

**Quel document mettre à jour, et quand**
1. Pour chaque document, quel événement du monde réel devrait déclencher sa mise à jour ?
2. Un document est-il mis à jour selon un calendrier au lieu de quand le fait sous-jacent change réellement — signe qu'il est le mauvais propriétaire de ce fait ?

**Suivi du Travail**
1. Quel outil suivra réellement le travail — un tableau, une feuille de calcul, juste des tickets ?
2. Quels sont les états par lesquels le travail passe, et qui les fait avancer ?
3. Des champs personnalisés sont-ils vraiment nécessaires, ou la propre ligne Statut du format de story le couvre-t-elle déjà ?

**Définition de Terminé (niveau projet)**
1. Quel est le niveau universel que chaque story doit atteindre avant Terminé, indépendamment du propre DoD checklist de cette story ?

**Référence Vocabulaire**
1. Chaque terme utilisé dans les specs est-il traçable à une entrée du Glossaire ?

**Étapes de bootstrap du suivi**
1. Quelles sont les étapes de configuration uniques que quelqu'un démarrant ceci depuis zéro doit faire, dans l'ordre, avant que la première story puisse être créée ?

---

### 10. `CLAUDE.md` — que doit savoir chaque session avant de toucher quoi que ce soit ?

Tout Générique — c'est ce que la propre section « CLAUDE.md est construit en dernier » du fichier `01` enseigne déjà ; ces questions sont la façon de le remplir réellement.

**Ce qu'est ce projet**
1. En 2-3 phrases, qu'est-ce que c'est et pour qui est-ce ?
2. Quel est le fait architectural unique qu'une session fraîche doit absolument savoir avant de toucher un fichier ?

**Carte des dossiers**
1. Quels sont les dossiers de premier niveau, et quelle est la raison en une ligne pour laquelle chacun existe ?
2. Y a-t-il une convention de nommage qui doit être énoncée explicitement pour ne jamais être devinée ?

**Stack technique**
1. Quelle est la stack par partie majeure du système ?
2. Où les détails canoniques sont-ils déjà documentés, pour que cette section reste un pointeur plutôt qu'une reformulation ?

**Conventions**
1. Quelle est une erreur qui s'est déjà produite une fois, que cette section existe spécifiquement pour prévenir ?
2. Quelle règle de nommage ou de formatage un nouveau contributeur se tromperait sans qu'on le lui dise directement ? Pour chaque langage/couche réellement utilisé : quelle est la règle de casse pour les fichiers, classes/composants, variables/fonctions, booléens et constantes — énoncer explicitement, ne pas laisser à inférer du premier fichier qui a accidentellement établi un précédent ? (Voir la propre section « Conventions de nommage » d'`AGENTS.md` dans ce kit pour la forme que cela devrait prendre.)
3. Y a-t-il une convention de nommage des dossiers de service/module (une fois que le projet a plus d'une pièce exécutée indépendamment), et est-elle énoncée ici plutôt que laissée implicite ?

**Contraintes de confidentialité**
1. Qu'est-ce qui ne doit jamais être révélé, dit ou inventé, et que doit-il se passer à la place quand quelqu'un le demande quand même ?
2. Y a-t-il quelque chose autorisé à l'utilisation qui était auparavant restreint — le tableau est-il réellement à jour ?

**Checklist de première session**
1. Quel est le chemin le plus rapide pour être utile à quelqu'un qui connaît déjà ce projet, par rapport à quelqu'un qui commence ?
2. Dans quel ordre les documents principaux doivent-ils être lus ?

**Pointeurs**
1. Pour la poignée de choses qui reviennent constamment en milieu de session, quel document unique est canonique pour chacune ?

## Tableau des erreurs courantes

| Erreur | Pourquoi ça arrive | La correction |
|---|---|---|
| Copier les en-têtes de section exacts d'un document dans un nouveau projet au lieu du pattern sous-jacent | L'en-tête existe déjà, semble sûr à réutiliser verbatim | Demandez « générique, généraliser ou conditionnel ? » pour chaque en-tête avant de le réutiliser — voir l'entrée PRD ci-dessus pour ce que ça donne fait correctement |
| Imposer une liste de sections fixe sur un type de document qui est censé être incrémental (specs fonctionnelles/techniques) | La cohérence semble devoir s'appliquer partout | Certains documents sont délibérément façonnés par ce qui est réel encore, pas par un modèle — écrire des sections avant qu'une story se close est de la spéculation, pas de la documentation |
| Répondre à ces questions de réflexion de façon générique au lieu des spécificités réelles du projet | Plus rapide d'écrire quelque chose de plausible que d'y réfléchir vraiment | Les questions sont l'échafaudage, pas le contenu — une réponse qui conviendrait à n'importe quel projet n'a pas réellement répondu à la question |
| Traiter une section Conditionnelle comme obligatoire parce qu'elle est dans la liste | La liste semble complète, donc omettre quelque chose qu'elle contient semble une omission | « Passer si non applicable » est lui-même la bonne réponse pour une section Conditionnelle sur un projet où elle ne s'applique pas — ne forcez pas de contenu dedans |
