# Lancement officiel du Projet 2
**GL-EN3-2026 · Lundi 21 septembre 2026**
*Jean Fritz SAINT-PAUL · FDS-UEH*

---

> **Gardez ce document ouvert pendant les six prochaines semaines.** C'est la référence de ce qui est attendu et de ce qui est noté. Tout ce qui est dit aujourd'hui à l'oral est écrit ici.

## Plan du cours

1. **Ce qu'on vous demande** — les quatre livrables et les contraintes
2. **Livrable 1** — le cahier des charges remanié
3. **Le périmètre exact, équipe par équipe** — votre MoSCoW devient votre contrat
4. **Livrable 2** — le dépôt du projet et sa documentation
5. **Livrable 3** — l'application en production
6. **Livrable 4** — le rapport
7. **Notation** — la grille, le bonus, la formule
8. **La soutenance** — format et questions individuelles
9. **Calendrier et ressources**

---

## Partie 1 — Ce qu'on vous demande

### Le Projet 2 en une phrase

> *Repartir de votre cahier des charges du Projet 1, construire avec votre agent le package documentaire du kit, puis développer et déployer un MVP réellement utilisable en production.*

Le Projet 1 notait un **dossier de conception**. Le Projet 2 note un **produit qui tourne** — et la **méthode** avec laquelle vous l'avez construit. Ces deux moitiés comptent presque autant l'une que l'autre, et c'est le changement le plus important à comprendre aujourd'hui.

### Les quatre livrables

| # | Livrable | Forme |
|---|---|---|
| 1 | **Le cahier des charges remanié** | Document PDF ou Word, 10-15 pages |
| 2 | **Le dépôt du projet** | Dépôt Git complet : backend, frontend, et `project-docs/` |
| 3 | **L'application en production** | URL accessible, qui fonctionne |
| 4 | **Le rapport** | Document PDF, 8-12 pages — le guide de lecture des trois autres |

### Les contraintes, rappelées

| Élément | Exigence |
|---|---|
| **Périmètre fonctionnel** | **Tout votre MoSCoW du Projet 1, sauf le Won't Have** — Must + Should + Could. Le détail de votre équipe est en Partie 3 |
| **Base de données** | Simple. Rien de compliqué. |
| **Paiement** | Un simulateur est accepté — mais **tous les cas d'usage doivent fonctionner**, y compris les refus et les échecs |
| **Partie admin** | Tous les cas d'usage doivent fonctionner |
| **Architecture** | Les quatre couches du backend, Feature-Sliced Design côté frontend (cours du 17 septembre) |
| **Déploiement** | Frontend sur Vercel · API sur Render, Railway ou Fly · PostgreSQL managé (Neon, Supabase) |

### Les équipes et leurs modules — inchangés

| Équipe | Module | Persona | Pain point |
|--------|--------|---------|------------|
| **Sterno X-Core Group** | M1 — FDS Akademi | Étudiant FDS | Ne peut pas prouver les compétences qu'il déclare |
| **Bravetech** | M2 — FDS Portail | Candidat à l'inscription | Ne trouve pas d'information officielle sans se déplacer |
| **Neural Squad** | M3 — FDS Admin | Étudiant FDS | Aucune visibilité sur sa demande après dépôt |
| **Brainstorm** | M4 — FDS Pay | Étudiant FDS | Ne peut pas payer ses frais sans cash ni intermédiaire |

---

## Partie 2 — Livrable 1 : le cahier des charges remanié

Vous ne repartez pas de zéro : vous reprenez celui du Projet 1, vous le corrigez, et vous le **raccourcissez**. Le format visé est plus court que le précédent, parce qu'une partie de son contenu a maintenant un meilleur domicile dans `project-docs/`.

### Les quatorze sections, dans le nouvel ordre

| § | Section | Statut |
|---|---------|--------|
| 1 | Le problème | ✅ Fait au Projet 1 — à corriger selon les commentaires reçus |
| 2 | La solution proposée | ✅ Fait — à corriger |
| 3 | Le persona | ✅ Fait — à corriger |
| 4 | L'interview utilisateur | ✅ Fait — à corriger |
| 5 | Customer Journey Map | ✅ Fait — à corriger |
| 6 | **Job to Be Done** | 🔄 **Remonté** — vient maintenant AVANT l'hypothèse |
| 7 | L'hypothèse testable | 🔄 À reformuler, en la faisant découler du JTBD |
| 8 | Priorisation MoSCoW | ✅ Fait — à réviser avec ce que vous savez maintenant |
| 9 | Walking Skeleton | ✅ Fait — à réviser |
| 10 | **Use Cases** — le diagramme seul | 🔄 **Sans les user stories** |
| 11 | Diagrammes de séquence | ✅ Fait — à corriger |
| 12 | Modèle de données | 🔄 À reprendre : c'est le moment de rejuger vos entités |
| 13 | Architecture technique | 🔄 **Résumé seulement** |
| 14 | Choix technologiques | 🔄 Résumé seulement |

### Les quatre changements, et pourquoi

**1. Le Job to Be Done remonte avant l'hypothèse.** Au Projet 1, l'hypothèse venait en §3.4 et le JTBD en §3.5 — l'ordre était inversé. Le JTBD est ce qui *fonde* l'hypothèse : on formule une hypothèse sur ce qui change dans la vie de quelqu'un, donc il faut d'abord avoir dit ce qu'il cherche à accomplir.

**2. Plus de user stories dans ce document.** Elles vivent maintenant dans `project-docs/execution/epic-NNN-*/US-NNN.md`, écrites au fur et à mesure avec le skill `user-story`. En mettre ici en créerait une deuxième copie qui dérivera de la première dès la première semaine. Le diagramme de cas d'utilisation, lui, reste : il donne la vue d'ensemble.

**3. Plus de diagramme d'activité.** Il était déjà optionnel au Projet 1 et il ne sera pas noté.

**4. L'architecture n'est qu'un résumé.** Le détail — les Workstreams, les ADR, la stack justifiée — va dans `SOLUTION_DESIGN.md`. Ce qui reste ici : le diagramme de composants et une page qui dit quelle architecture vous adoptez. **Répéter la même décision dans deux documents, c'est garantir qu'ils finiront par se contredire.**

---

## Partie 3 — Le périmètre exact, équipe par équipe

### La règle, et c'est le point le plus important de la séance

> **Votre priorisation MoSCoW du Projet 1 devient votre contrat.**
> Vous devez livrer **le Must Have, le Should Have et le Could Have**.
> **Seul le Won't Have reste hors périmètre.**

Au Projet 1, le MoSCoW servait à définir un MVP : le Must Have suffisait. Ce n'est plus le cas. **Ce que vous avez classé Should Have et Could Have entre maintenant dans le périmètre à livrer.** Vous l'avez écrit vous-mêmes, vous l'avez jugé faisable, et vous avez six semaines et un agent.

Trois conséquences à accepter tout de suite :

1. **Vous ne pouvez plus déplacer une fonctionnalité en Won't Have pour vous alléger.** Le périmètre est figé sur la version que vous avez rendue en juin.
2. **Si votre MoSCoW était ambitieux, vous le payez maintenant** — et c'est délibéré : une priorisation est un engagement, pas une liste de souhaits.
3. **L'ordre de construction reste le vôtre.** Must d'abord, évidemment, puis Should, puis Could — c'est votre `PLAN.md` qui séquence tout ça en Epics.

> Une fonctionnalité de votre Should ou Could que vous ne livrez pas devra être **justifiée dans le §2 de votre rapport** (« prévu vs réalisé »). Une justification honnête et argumentée coûte peu. Un silence coûte beaucoup.

---

### Équipe 1 — Sterno X-Core Group · M1 FDS Akademi

**Membres** : NOEL Richardson Wisler *(capitaine)* · JEAN-BAPTISTE Olivier Stéphane · VIXAMAR Sergelie

**Le problème** : un étudiant ne peut pas prouver ni attester les compétences qu'il déclare, parce qu'aucun outil ne lui permet de les structurer avec des preuves vérifiables validées par un tiers de confiance.

**Le Job to Be Done** :
> *Quand je postule à un stage ou à un programme de master, je veux déclarer mes compétences techniques avec des preuves liées à mon travail réel et les faire valider par mes professeurs, afin de présenter un portfolio crédible et vérifiable par des recruteurs.*

**Votre périmètre à livrer :**

| Priorité | Fonctionnalités |
|---|---|
| **Must Have** | Compte étudiant (connexion) · Déclarer une compétence : nom libre + niveau (L1/L2/L3) · Attacher une preuve : lien URL ou upload de fichier (PDF, image) · Notification au professeur : validation en attente · Le professeur valide ou rejette avec commentaire · Profil public étudiant accessible par URL permanente |
| **Should Have** | Tableau de bord étudiant (en attente / validées / rejetées) · Compte professeur (inscription, connexion) · Notification e-mail à l'étudiant quand une compétence est validée ou rejetée · Explication des niveaux L1/L2/L3 dans l'interface |
| **Could Have** | Export PDF du portfolio · Plusieurs preuves par compétence · Commentaire public du professeur visible · Recherche de compétences par nom |
| ~~Won't Have~~ | *Hors périmètre* : Open Badges 3.0 · gestion des cours et devoirs · analytics par promotion · validation multi-professeurs · intégration automatique GitHub API · export de badge vérifiable externe |

---

### Équipe 2 — Bravetech · M2 FDS Portail

**Membres** : VAILLANT Valcin *(capitaine)* · DORFILUS Skin-Paolatchi · GUERRIER Joas · LOUIS Widmaken

**Le problème** : forte dépendance au déplacement physique, causée par un déficit d'information numérique fiable et centralisée — ce qui crée une inégalité d'accès pour les candidats vivant hors de Port-au-Prince.

**Le Job to Be Done** :
> *Quand je dois m'inscrire à l'université depuis ma province sans information claire, je veux pouvoir m'informer, soumettre mon dossier et payer virtuellement les frais entièrement en ligne, afin de sécuriser ma candidature à la FDS sans perdre de temps ni risquer ma sécurité dans un déplacement physique.*

**Votre périmètre à livrer :**

| Priorité | Fonctionnalités |
|---|---|
| **Must Have** | Pages de présentation des cursus et dates clés · Formulaire de candidature en ligne avec upload de pièces (PDF/JPG) · Génération d'un numéro de référence de dossier (`CAN-2026-X`) · Suivi du dossier en ligne par le candidat via sa référence · Interface sécurisée pour l'administration · Notifications automatiques par e-mail : confirmation de réception, validation d'un document, rejet d'un document avec lien pour le remplacer · Possibilité de remplacer un document rejeté depuis la page de suivi · Simulation du paiement des frais (MonCash / NatCash) |
| **Should Have** | Notifications push (SMS) en complément de l'e-mail |
| **Could Have** | Export CSV/PDF filtré de la liste des dossiers validés, pour les commissions d'admission hors ligne · Mode sombre pour l'interface administrative et le formulaire candidat |
| ~~Won't Have~~ | *Hors périmètre* : transactions monétaires réelles |

---

### Équipe 3 — Neural Squad · M3 FDS Admin

**Membres** : CHARLES Jean Guetcheen *(capitaine)* · JOSPEPH Wiycleph · PIERRE Rose Sona Ediasqua

**Le problème** : un étudiant qui dépose une demande administrative n'a aucune visibilité sur ce qui se passe après le dépôt — d'où des déplacements répétés, des relances, et des délais imprévisibles.

**Le Job to Be Done** :
> *Lorsque je dois obtenir un document administratif (relevé de notes, attestation, certificat), je veux pouvoir soumettre ma demande facilement et suivre son avancement en temps réel, afin d'éviter les déplacements répétés et l'incertitude sur l'état de mon dossier.*

**Votre périmètre à livrer :**

| Priorité | Fonctionnalités |
|---|---|
| **Must Have** | Création d'un compte étudiant et authentification · Soumission d'une demande administrative en ligne · Attribution automatique d'un numéro de ticket · Gestion du workflow des demandes (soumise, reçue, en traitement, prête, remise, rejetée) · Suivi de l'état d'avancement par l'étudiant · Interface pour les agents administratifs · Mise à jour du statut par le personnel administratif · Historique des demandes par utilisateur · Notifications de base (au minimum e-mail) |
| **Should Have** | Notifications par e-mail enrichies · Tableau de bord pour les responsables administratifs · Filtrage et recherche avancée des demandes · Gestion des délais de traitement par type de demande · Téléchargement du document final depuis la plateforme |
| **Could Have** | Statistiques avancées et rapports automatiques · Système de chat entre étudiant et administration · Évaluation de la satisfaction après traitement · Archivage avancé des demandes anciennes |
| ~~Won't Have~~ | *Hors périmètre* : paiement en ligne intégré · signature électronique des documents officiels · intégration avec des systèmes externes (Campus France…) · IA de prédiction des délais · automatisation complète de la génération de documents |

> **Note pour Neural Squad** : votre `Won't Have` exclut le paiement en ligne. La contrainte générale sur le simulateur de paiement ne s'applique donc pas à vous — votre équivalent est le **workflow complet des demandes, tous statuts compris, y compris le rejet**.

---

### Équipe 4 — Brainstorm · M4 FDS Pay

**Membres** : NICOLAS Jean Nickson *(capitaine)* · SAINT GERMAIN Pierre Michel Junior · JEAN CHARLES Carlbens Jovani Junior

**Le problème** : un étudiant n'a aucun moyen de payer ses frais à la FDS sans se déplacer avec du cash ou sans dépendre d'un intermédiaire.

**Le Job to Be Done** :
> *Quand je dois payer pour mes démarches à la faculté, je veux pouvoir le faire à distance, afin de régler mes démarches administratives et académiques à tout instant et n'importe où.*

**Votre périmètre à livrer :**

| Priorité | Fonctionnalités |
|---|---|
| **Must Have** | Authentification des étudiants · Consultation des différents types de frais (scolarité, documents administratifs et académiques) · Paiement des frais via MonCash · Vérification automatique du statut du paiement · Génération d'un reçu numérique · Téléchargement du reçu en PDF · Consultation de l'historique des paiements · Tableau de bord d'administration pour consulter les paiements |
| **Should Have** | Notification de confirmation par SMS ou e-mail après le paiement · Recherche et filtrage des paiements par étudiant ou par période · Tableau de bord avec statistiques de paiements · Intégration de NatCash |
| **Could Have** | Paiement en plusieurs fois · Tableau de bord personnalisé pour les étudiants · Notifications automatiques avant les échéances · Mode sombre · Support multilingue (français, créole, anglais) · QR Code sur le reçu numérique pour vérification rapide |
| ~~Won't Have~~ | *Hors périmètre* : IA de détection de fraudes · paiement international · virement bancaire · chatbot d'assistance · intégration complète avec le système académique · application mobile Android et iOS |

> **Note pour Brainstorm** : MonCash et NatCash sont à **simuler**. Aucune transaction monétaire réelle n'est attendue — mais tous les cas doivent être couverts : paiement réussi, échoué, refusé, relancé.

---

## Partie 4 — Livrable 2 : le dépôt du projet

### L'arborescence attendue

```text
votre-projet/
├── README.md                    <- ce qu'est le projet, comment le lancer
├── AGENTS.md                    <- les instructions persistantes (écrit en DERNIER)
├── CLAUDE.md                    <- import mince de AGENTS.md
├── project-docs/                <- TOUT document sur la construction du projet
│   ├── PRD.md  NFR.md  SOLUTION_DESIGN.md  PLAN.md  GLOSSARY.md
│   ├── PROJECT_WORKFLOW.md
│   ├── execution/EPIC_EXECUTION.md  +  epic-NNN-*/US-NNN.md
│   ├── functional-specs/  technical-specs/
│   ├── reviews/                 <- ce que vous croyiez et qui s'est révélé faux
│   ├── learnings/               <- ce qui se transfère à un autre projet
│   └── exploration/
├── backend/                     <- entities/ dal/ bll/ api/ core/ tests/
├── frontend/                    <- app/ pages/ widgets/ features/ entities/ shared/
├── .githooks/                   <- activé une fois : git config core.hooksPath .githooks
└── .claude/skills/              <- les neuf skills du kit
```

### Ce qui est regardé, et dans quel ordre

**Au premier abord — la qualité des documents fondateurs.** `PRD.md`, `NFR.md`, `SOLUTION_DESIGN.md`, `PLAN.md`. Est-ce que le produit est clairement défini ? Est-ce que la barre de qualité est chiffrée plutôt que souhaitée ? Est-ce que les Workstreams découpent réellement le produit ? Est-ce que le PLAN séquence des Epics faisables ?

**Ensuite — l'exécution.** Les Epics créés, les stories écrites, le process réellement suivi, les `reviews/` et les `learnings/`.

> **La question qui décide de cette partie de la note :** *le process a-t-il été **vécu**, ou reconstitué la veille du dépôt ?* Les deux se distinguent immédiatement à l'historique git, aux dates des fichiers, et au fait qu'une story reconstituée après coup n'a jamais d'`As-built notes` qui contredisent son plan initial.

### Le test de reprise

C'est le critère central sur `AGENTS.md` et `CLAUDE.md`, et il sera exécuté **en direct pendant votre soutenance** :

> Un agent neuf est ouvert sur votre dépôt, sans aucun contexte de conversation, et reçoit une seule question :
> **« D'après les documents de ce projet, quelle est la prochaine story à construire, et pourquoi ? »**

Si l'agent répond juste sans aide humaine, vos documents fonctionnent. S'il faut lui expliquer, ils ne fonctionnent pas — quelle que soit leur beauté.

C'est pour ça qu'`AGENTS.md` porte un ordre de lecture, des pointeurs vers les documents canoniques, et la table « où va une règle quand on en découvre une ». Ce n'est pas de la décoration : c'est ce qui rend un projet reprenable.

### Les plafonds anti-verbosité

Un document trop long n'est pas un document plus complet — c'est un document que personne ne relira, agent compris, et dont la moitié sera périmée sans que personne le voie.

| Règle | Seuil |
|---|---|
| `AGENTS.md` | **≤ 300 lignes** (règle du kit lui-même) |
| Toute ligne de `AGENTS.md` | Doit passer le test : *« est-ce que supprimer cette ligne causerait une mauvaise action ? »* Sinon : la couper, ou la transformer en pointeur |
| Un document qui paraphrase un autre | **Perd des points au lieu d'en gagner** |
| `PRD.md` | Ce qu'il faut pour décider, pas ce qu'il faut pour impressionner |

### Git et le suivi du travail

| Attendu | Comment ce sera vérifié |
|---|---|
| Un historique réel, étalé sur les six semaines | `git log` — des commits de la première semaine, pas seulement de la dernière |
| Des commits qui référencent les stories | `US-NNN` dans les messages de commit |
| Le hook installé | `git config core.hooksPath .githooks` — les dates `updated:` des markdowns doivent bouger |
| Un board de suivi | GitHub Projects (Kanban), ou Issues + Milestones |
| Les documents avant le code | `git log --reverse` : les documents fondateurs sont-ils commités **avant** le premier fichier de code ? |

---

## Partie 5 — Livrable 3 : l'application en production

### Le déploiement

| Composant | Où | Note |
|---|---|---|
| **Frontend** | Vercel | C'est ce pour quoi Vercel est fait |
| **API** | Render, Railway ou Fly | Offre gratuite suffisante pour ce projet |
| **Base de données** | PostgreSQL managé — Neon, Supabase | SQLite est impossible : pas de système de fichiers persistant |

> **Bonus : +10 points.** Une équipe qui déploie son application sur les **serveurs de la Faculté des Sciences**, avec le professeur Villa, gagne **10 points ajoutés à la note de groupe**. C'est la même mécanique que le bonus prototype du Projet 1.

### Ce qui doit fonctionner

**Le périmètre de votre équipe, tel qu'il est arrêté en Partie 3** : Must Have, Should Have et Could Have. Pas seulement le Must.

Là où il y a un paiement, le simulateur est accepté — mais **tous les cas d'usage doivent marcher** : le paiement qui réussit, celui qui échoue, celui qui est refusé, celui qui est relancé. Une démo qui ne montre que le chemin heureux ne démontre rien : **c'est le cas d'erreur qui prouve que la règle métier existe.**

Idem pour toute interface d'administration : tous les cas d'usage, pas seulement la liste qui s'affiche.

### Les contrôles automatiques attendus

| Contrôle | Commande | Ce qu'il prouve |
|---|---|---|
| Test d'architecture backend | `pytest tests/unit/test_architecture.py` | Aucune dépendance ne pointe dans le mauvais sens |
| Linter d'architecture frontend | `npx steiger src` | Aucun import vers le haut, aucune slice sœur, aucun contournement d'`index.ts` |
| Suite de tests | `pytest` / `npm test` | Ce que vous avez réellement couvert |

### CRAP — le score de qualité du code

Vous devrez mesurer votre propre code avec la métrique **CRAP** (*Change Risk Anti-Patterns*), et donner le résultat dans votre rapport. **Ce score sera recalculé à la correction.**

```
CRAP(f) = complexité(f)²  ×  (1 − couverture(f)/100)³  +  complexité(f)
```

où `complexité` est la complexité cyclomatique de la fonction (son nombre de chemins d'exécution) et `couverture` le pourcentage de cette fonction exercé par vos tests. **Le seuil de crappiness est 30** : au-dessus, une fonction est considérée à risque. Métrique proposée par Alberto Savoia et Bob Evans en 2007.

**Ce que la formule dit, en pratique :**

| Complexité | 0 % de couverture | 50 % | 100 % |
|---|---|---|---|
| 3 | 12 | 4,1 | 3 |
| 5 | **30** | 8,1 | 5 |
| 10 | 110 | 22,5 | 10 |
| 15 | 240 | 43,1 | 15 |
| 20 | 420 | 70 | 20 |

Les deux leçons à retenir :

1. **Une fonction non testée doit avoir une complexité ≤ 5 pour passer sous 30.** Au-delà, elle est à risque par construction.
2. **Une fonction de complexité 10 a besoin d'environ 42 % de couverture** pour passer le seuil — et de 100 % pour descendre à 10.

C'est exactement la pression qu'il faut contre du code généré : un agent produit volontiers une fonction longue qui marche. CRAP dit qu'une fonction longue **non testée** est un risque, indépendamment du fait qu'elle marche aujourd'hui.

> **À vous de chercher comment la calculer sur votre stack.** Elle n'est pas fournie clé en main par la plupart des outils Python. Piste : la complexité cyclomatique se mesure avec `radon`, la couverture par fonction avec `coverage.py` — la composition des deux est à faire. C'est un exercice de recherche volontaire : vous devez être capables de trouver, d'évaluer et de brancher un outil que le cours ne vous a pas donné.

---

## Partie 6 — Livrable 4 : le rapport

### Ce qu'il est, et ce qu'il n'est pas

> **Le rapport n'est pas une redite. C'est le guide de lecture de tout le reste.**

Il dit où regarder dans votre dépôt, et il raconte ce qui s'est réellement passé pendant six semaines. Il ne recopie ni le cahier des charges, ni le PRD, ni le SOLUTION_DESIGN : il y renvoie. **C'est lui que je lirai en premier, et c'est lui qui guidera tout le reste de ma correction.** C'est aussi essentiellement lui que vous présenterez en soutenance.

Format : **8 à 12 pages**, neuf sections.

### Les neuf sections

**1. Carte du livrable**
Où est quoi, en liens cliquables : le dépôt, l'URL de production, le `project-docs/`, le board, les Pull Requests. Une page maximum.

**2. Prévu vs réalisé**
Ce que votre `PLAN.md` annonçait au départ, ce que vous avez réellement livré, ce que vous avez coupé — **et pourquoi**. Un projet dont le plan initial a été tenu à la lettre en six semaines est un projet dont le plan était trop prudent, ou dont le rapport n'est pas sincère.

**3. Journal de la méthode**
Comment le cycle a été vécu. Ce qui a marché, ce que vous avez abandonné, ce que vous avez adapté. Est-ce que vous avez vraiment fait un `Refine` avant chaque story ? Est-ce que vous avez fermé vos Epics avec les huit étapes, ou est-ce que vous en avez sauté ? **Dire honnêtement que vous en avez sauté rapporte plus que prétendre le contraire** — parce que la première version est vérifiable et la seconde aussi.

**4. Trois décisions difficiles**
Trois décisions que vous avez dû prendre, chacune racontée avec l'alternative que vous avez écartée et la raison. Architecture, périmètre, ou outillage.

**5. Ce que les reviews ont révélé**
**Au moins deux croyances fausses**, avec la preuve qui les a fait tomber. Format : *voici ce qu'on croyait, voici ce qui l'a contredit, voici la version corrigée.* C'est la section la plus difficile à écrire et la plus révélatrice à lire.

**6. Le travail avec l'agent**
Où il a été bon, où il s'est trompé, comment vous l'avez recadré — et **ce qui a fini dans `AGENTS.md` à cause de ça**. Cette section est celle qui distingue ce rapport de tous les précédents du cours : **elle évalue votre capacité à piloter un agent, pas à en obtenir du code.**

**7. Les preuves**
Captures du board, extrait d'historique git, sortie des tests, score CRAP, URL de production accessible.

**8. Learnings**
Ce que vous referiez, ce que vous ne referiez pas. Si vous deviez recommencer lundi prochain avec un autre sujet, qu'est-ce qui changerait dans votre façon de travailler ?

**9. Contributions individuelles**
Table nominative : qui a fait quoi. Cette table **prépare vos questions individuelles de soutenance** — c'est à partir d'elle que je choisirai quoi demander à qui.

---

## Partie 7 — Notation

Le Projet 2 vaut **60 % de la note du cours** (le Projet 1 en valait 35 %, la participation compte pour les 5 à 10 % restants).

### La grille de la note de groupe — sur 100

| # | Composante | Poids | Ce qui est regardé |
|---|---|---|---|
| 1 | **Cahier des charges remanié** | 10 % | Cohérence de la chaîne, concision, JTBD qui fonde l'hypothèse |
| 2 | **Documents fondateurs** — PRD, NFR, SOLUTION_DESIGN, PLAN, GLOSSARY | 20 % | Justesse **et concision** : un PRD verbeux perd des points |
| 3 | **`AGENTS.md` / `CLAUDE.md` + test de reprise** | 10 % | Un agent neuf peut-il reprendre le projet sans aide ? |
| 4 | **Exécution du cycle** — Epics, stories, reviews, learnings, Git, board | 20 % | Le process a-t-il été vécu, ou reconstitué à la fin ? |
| 5 | **Qualité du code et respect de l'architecture** | 20 % | Les 4 couches, le sens des dépendances, les contrôles, CRAP |
| 6 | **Application en production** | 10 % | Déployée, accessible, et **le périmètre Must + Should + Could effectivement livré** (Partie 3) |
| 7 | **Rapport et soutenance** | 10 % | Le rapport guide-t-il vraiment ? La démo tient-elle ? |
| | **Total** | **100** | |
| | **Bonus** — déploiement sur les serveurs de la FDS | **+10 pts** | Ajoutés à la note de groupe |
| | **Pénalité** — élément manquant ou bâclé | **jusqu'à −10 pts** | Retirés de la note de groupe |

> **Remarquez la répartition** : les composantes 2, 3 et 4 pèsent **50 %** à elles trois. C'est-à-dire que **la moitié de la note porte sur la méthode et la documentation**, pas sur le code. Ce n'est pas un biais du correcteur : c'est ce que ce module enseignait.

### Les pénalités

**Tout élément attendu qui est absent, ou présent mais visiblement bâclé, coûte jusqu'à 10 points** — retirés de la note de groupe, exactement comme le bonus y est ajouté.

Cette pénalité existe parce qu'un élément bâclé est pire qu'un élément absent : il occupe la place du vrai travail et laisse croire qu'il a été fait. Quelques exemples de ce qui sera compté comme bâclé :

| Situation | Pourquoi c'est bâclé |
|---|---|
| Un document du kit encore rempli des **questions du gabarit**, sans réponses | Le fichier existe, le travail non |
| Un `GLOSSARY.md` jamais rempli | Le vocabulaire partagé est la condition de tout le reste |
| Un `reviews/` contenant **un seul fichier écrit le dernier jour** | Une review s'écrit au moment de la découverte, pas à la fin |
| Le cahier des charges **rendu inchangé** depuis juin | Il était à remanier, pas à re-soumettre |
| Une paire de specs `func`/`tech` **vide alors que l'Epic est fermé** | L'Epic n'est pas réellement fermé |
| Le §5 du rapport (croyances fausses) **vide ou manifestement inventé** | C'est la section qui prouve que vous avez travaillé sur du réel |
| Une démo qui **ne montre que le chemin heureux** | Elle ne démontre aucune règle métier |

> **La pénalité est cumulative dans la limite de 10 points au total**, pas 10 points par élément. Un dossier auquel il manque trois choses perd donc au maximum 10 points — mais il aura déjà perdu bien plus sur les composantes correspondantes de la grille.

### De la note de groupe à votre note

Même mécanique qu'au Projet 1 :

```
Note individuelle = moyenne(PRI, QI)

     PRI = Participation et Rigueur Individuelle
           (contribution réelle, visible dans l'historique git,
            dans les stories, et dans le §9 de votre rapport)
     QI  = Questions Individuelles
           (vos réponses STAR en soutenance)

FINAL = (Note groupe × 0,70) + (Note individuelle × 0,30)
```

### Exemple chiffré

```
Équipe X — note de groupe
   Cahier des charges (10%)      75  →   7,50
   Documents fondateurs (20%)    70  →  14,00
   AGENTS.md + reprise (10%)     60  →   6,00
   Exécution du cycle (20%)      80  →  16,00
   Code et architecture (20%)    72  →  14,40
   Production (10%)              85  →   8,50
   Rapport et soutenance (10%)   78  →   7,80
                                     ─────────
   Note de groupe                       74,20
   Bonus serveurs FDS                  +10,00
   Pénalité (GLOSSARY.md jamais rempli,
             reviews/ écrit le dernier jour)  −6,00
   NOTE DE GROUPE RETENUE               78,20
```

```
Membre A   PRI 85, QI 80  →  Note ind. 82,5
           FINAL = 78,2 × 0,70 + 82,5 × 0,30 = 54,74 + 24,75 = 79,49

Membre B   PRI 60, QI 55  →  Note ind. 57,5
           FINAL = 78,2 × 0,70 + 57,5 × 0,30 = 54,74 + 17,25 = 71,99
```

> La note de groupe protège un membre fort d'une mauvaise journée. La note individuelle garantit que chaque membre doit maîtriser le projet — pas seulement le capitaine.

### Les vérifications qui seront faites, et comment

Chacune prend quelques minutes et donne une réponse nette. Elles sont listées pour que rien ne vous surprenne :

| Vérification | Méthode |
|---|---|
| **Test de reprise** | Un agent neuf sur votre dépôt, une question, pas d'aide |
| **Traçabilité story → production** | Une fonctionnalité prise au hasard dans l'app, remontée jusqu'à la story qui l'a demandée |
| **Documents avant code** | `git log --reverse` |
| **Le hook est installé** | Les dates `updated:` bougent-elles au fil des commits ? |
| **Honnêteté du dossier** | Un `reviews/` vide après six semaines signifie que rien n'a été consigné. Une review dont tous les constats sont flatteurs n'a pas été écrite honnêtement |
| **Les contrôles tournent** | `pytest tests/unit/test_architecture.py` et `npx steiger` |
| **Score CRAP reproductible** | Le score du rapport est recalculé ; il doit correspondre |

---

## Partie 8 — La soutenance

### Format — 90 minutes par équipe

| Phase | Durée | Contenu |
|-------|-------|---------|
| **Présentation** | 35 min | Adossée au rapport : le problème, ce qui a été construit, comment vous avez travaillé, ce que vous avez appris |
| **Démo live** | 15 min | L'application **déployée**, en conditions réelles. Chemin nominal **et** cas d'erreur, sur tout le périmètre Must + Should + Could |
| **Questions individuelles** | 35 min garantis | 2 questions par membre, méthode STAR — soit 4 à 5 minutes par réponse, vous avez le temps de construire un STAR complet |
| **Retour à chaud** | 5 min | Premiers commentaires de l'enseignant |

> **Prévoyez un plan B pour la démo** : une vidéo de secours de 3 minutes montrant le parcours complet. Une panne de connexion pendant la soutenance ne doit pas vous coûter les 15 minutes de démo.

### Les questions individuelles — méthode STAR

| Lettre | Ce qu'on attend |
|--------|-----------------|
| **S** — Situation | Le contexte, brièvement |
| **T** — Tâche | Ce que **vous** deviez faire ou décider personnellement |
| **A** — Action | Les étapes que **vous** avez prises — pas « on a fait » |
| **R** — Résultat | Ce qui a changé, ce que vous avez appris |

**Le piège, comme au Projet 1** : répondre en « on ». La méthode STAR demande ce que **vous**, personnellement, avez fait et compris. Le §9 de votre rapport sera ouvert devant moi pendant que je pose la question.

### Exemples de questions, propres au Projet 2

> **Sur une décision d'architecture** — *« Montrez-moi une règle métier de votre BLL. Pourquoi est-elle là plutôt que dans la route ? Qu'est-ce qui se serait cassé si vous l'aviez mise dans la route ? »*

> **Sur le pilotage de l'agent** — *« Racontez-moi une fois où l'agent vous a proposé quelque chose que vous avez refusé. Comment avez-vous su que c'était faux, et qu'avez-vous fait ensuite ? »*

> **Sur une review** — *« Dans votre review numéro 2, vous écrivez que vous croyiez X. Qu'est-ce qui vous a fait découvrir que c'était faux, et qu'est-ce que ça a changé dans le code ? »*

> **Sur la documentation** — *« Si je supprime votre `AGENTS.md` et que j'ouvre un agent neuf sur le dépôt, qu'est-ce qu'il n'arrivera plus à faire ? »*

---

## Partie 9 — Calendrier et ressources

### Le calendrier

| Date | Événement |
|------|-----------|
| **Lundi 21 septembre** | ✅ Lancement officiel — aujourd'hui. Remise du `project-init-kit` |
| **Jeudi 24 septembre** | Dernier cours — séance ouverte de questions sur le projet et le kit |
| **25 septembre → 6 novembre** | Travail autonome. **Pas de cours.** |
| **Vendredi 6 novembre** | **Dépôt définitif, avant 23h59** — dans le dossier Teams dédié |
| **Mardi 10 → vendredi 13 novembre** | **Soutenances** — 90 min par équipe, ordre de passage du Projet 1 |

> Le dépôt du 6 novembre est **définitif**. L'application doit être en ligne et fonctionnelle à cette date — pas réparée la veille de la soutenance.

### Un découpage des six semaines

Ce n'est pas une obligation, c'est le rythme qui rend le projet faisable. Chaque ligne suppose la précédente terminée.

| Semaine | Dates | Objectif |
|---------|-------|----------|
| **0** | 21 – 27 sept | Relire votre cahier des charges, Installer le kit. **Remplir le `PRD.md` vous-mêmes, sans agent.** |
| **1** | 28 sept – 4 oct | `NFR` → `SOLUTION_DESIGN` → `PLAN` → `GLOSSARY` → `AGENTS.md`. Puis **seulement là**, les deux scaffolds |
| **2** | 5 – 11 oct | Epic X : refine, stories, premier incrément — **et premier déploiement, même minimal** |
| **3** | 12 – 18 oct | Epic X terminé et **fermé** (les huit étapes) avec test + CRAP validé |
| **4** | 19 – 25 oct | Epic Y : le cœur métier Tous les cas d'usage fonctionnent |
| **5** | 26 oct – 1 nov | Epic Y fermé.  avec test + CRAP validé + Deployment |
| **6** | 2 – 6 nov | Dernière vérification, Répétition de la soutenance, Deploiement et Livraison |

> **Déployez en semaine 2, pas en semaine 6.** L'erreur classique est de tout construire en local et de découvrir les problèmes de déploiement à quatre jours du rendu. Une application vide mais déployée en semaine 2 vous enlève le plus gros risque du projet.

### Les ressources — tout est déjà à vous

| Ressource | Ce qu'elle contient |
|-----------|---------------------|
| **`project-init-kit/`** | La structure, les neuf skills, `_ARCHITECTURE_EXPLAINED.md`, `STARTER_PROMPT.md` |
| **Récapitulatif du 14 septembre** | Le bilan des quatre modules, toutes les notions du cours |
| **Architecture et cycle, 17 septembre** | Les quatre couches, FSD, les parcours détaillés, le cycle complet |
| **Slides des trois séances** | Dans le dossier Teams |
| **WhatsApp** | Pour les blocages — entraidez-vous entre équipes |

### Ce que vous faites en sortant d'ici

1. **Aujourd'hui** : copier le kit dans un dépôt neuf, lancer `git init`, activer le hook, faire le premier commit.
2. **Cette semaine** : répondre aux questions du `PRD.md` **vous-mêmes**, avant d'ouvrir un agent.
3. **Jeudi 24** : venir avec vos questions — c'est la dernière séance.
4. **Semaine prochaine** : les documents restants, puis les scaffolds.

---

> *Vous avez le cahier des charges, la méthode, l'architecture, les outils et six semaines. Ce qui est évalué maintenant, ce n'est plus ce que vous savez — c'est ce que vous livrez, et la façon dont vous y êtes arrivés.*

---

*GL-EN3-2026 · Jean Fritz SAINT-PAUL · FDS-UEH · Lundi 21 septembre 2026*
