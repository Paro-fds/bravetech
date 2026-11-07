---
created: 2026-11-06T04:30:00Z
updated: 2026-11-07T00:58:45Z
---

# Rapport — Projet 2 · Équipe 2 Bravetech · M2 FDS Portail

**Membres :** VAILLANT Valcin *(capitaine)* · DORFILUS Skin-Paolatchi · GUERRIER Joas · LOUIS Widmaken
**Cours :** Génie Logiciel EN3 — 2026 · **Dépôt :** 6 novembre 2026

> Ce rapport est un guide de lecture. Il ne recopie ni le cahier des charges, ni le PRD, ni le SOLUTION_DESIGN : il y renvoie, et raconte ce qui s'est réellement passé.

---

## 1. Carte du livrable

| Quoi | Où |
|---|---|
| Application en production | **https://dorfilus.ueh.edu.ht** — VM Proxmox de la FDS, derrière l'Apache de l'UEH (TLS `*.ueh.edu.ht`) |
| Dépôt | https://github.com/Paro-fds/bravetech (branche `master`, protégée) |
| Cahier des charges remanié (livrable 1) | [`cahier_des_charges.md`](../cahier_des_charges.md) |
| Documents fondateurs | [`PRD`](../project-docs/PRD.md) · [`NFR`](../project-docs/NFR.md) · [`SOLUTION_DESIGN`](../project-docs/SOLUTION_DESIGN.md) (ADR §14) · [`PLAN`](../project-docs/PLAN.md) · [`GLOSSARY`](../project-docs/GLOSSARY.md) · [`PROJECT_WORKFLOW`](../project-docs/PROJECT_WORKFLOW.md) |
| Instructions de l'agent | [`AGENTS.md`](../AGENTS.md) (≤ 300 lignes), [`CLAUDE.md`](../CLAUDE.md) |
| Suivi d'exécution | [`execution/EPIC_EXECUTION.md`](../project-docs/execution/EPIC_EXECUTION.md) — une page par story (`US-NNN.md`, avec notes de réalisation), un refinement et un closeout par Epic |
| Specs par Workstream | `functional-specs/ws-func-01` à `05`, `technical-specs/ws-tech-01` à `05` |
| Reviews / Learnings | [`reviews/`](../project-docs/reviews/) (01 à 04) · [`learnings/`](../project-docs/learnings/) (04 à 06 ; 01 à 03 viennent du kit) |
| Board | GitHub Projects « Bavetech_Project » : https://github.com/users/Paro-fds/projects/2 · Milestones « Epic 1 » à « Epic 5 » |
| Pull Requests | https://github.com/Paro-fds/bravetech/pulls?q=is%3Apr — 39 PR fusionnées, dont #48 (Alembic), #52 (déploiement continu), #53/#54 (test de retour arrière), #55 (steiger, CRAP), #60 (calendrier) |
| CI | `.github/workflows/ci.yml` (backend, frontend, steiger, CRAP) et `deploy.yml` (déploiement) |

**Comptes de démonstration :** fournis séparément (jamais dans le dépôt, qui est public).

---

## 2. Prévu vs réalisé

### Ce que le PLAN annonçait (30 septembre)

Trois Epics séquentiels pour le MVP : `epic-001` socle, `epic-002` candidature et suivi, `epic-003` administration. Le SMS était le seul Should Have ; **l'export CSV/PDF était classé Won't Have** ; ni Kreyòl, ni pages Histoire/Contact, ni mise en production réelle n'étaient planifiés en tant qu'Epic. Hébergement prévu : Vercel (frontend) et Railway (backend, base) ; fichiers sur Cloudinary.

### Ce qui a été livré

| Périmètre du contrat (Partie 3) | État | Où |
|---|---|---|
| Must — Pages des cursus **et dates clés** | ✅ Cursus depuis le 26/09 ; dates clés réglables par l'admin depuis le 05/11 (US-028) | ws-func-01 |
| Must — Formulaire en ligne avec dépôt des pièces | ✅ | ws-func-02 |
| Must — Référence `CAN-2026-X` | ✅ | ws-func-02 |
| Must — Suivi par référence | ✅ | ws-func-03 |
| Must — Interface d'administration sécurisée | ✅ JWT, 2 rôles, audit | ws-func-04 |
| Must — Emails (confirmation, validation, rejet avec lien) | ✅ codés le 01/11 ; **activés en production le 05/11, réception confirmée le 06/11** | ws-func-05 |
| Must — Remplacer un document rejeté | ✅ | ws-func-03 |
| Must — Simulation MonCash / NatCash, **tous les cas** | ✅ réussi le 01/11 ; refusé, échoué, relancé le 05/11 | ws-func-02 §2 |
| Should — Notifications SMS | ✅ **simulé**, comme le paiement (voir ci-dessous) | US-016, ws-func-05 §3 |
| Could — Export CSV/PDF filtré | ✅ | ws-func-04 §2 |
| Could — Mode sombre | ✅ | US-017 |
| Bonus — déploiement sur les serveurs de la FDS | ✅ déploiement continu avec retour arrière automatique | ws-tech-01 §5.3 |

**Ajouté en cours de route, hors plan initial :** l'Epic 4 (Histoire et Contact, interface en kreyòl, refonte visuelle d'après les maquettes, export, mode sombre, calendrier d'admission, gestion des accès du personnel depuis l'espace admin — US-029) et l'Epic 5 (Alembic, adresse réelle du visiteur derrière les proxys, CI frontend, déploiement continu). L'export, d'abord Won't Have, a été rétabli quand nous avons relu le contrat, qui le place en Could.

**Coupé ou non livré, et pourquoi :**
- **SMS réels (US-016, Should Have) : simulés, pas envoyés.** Aucun fournisseur SMS (Twilio, opérateur haïtien) n'a pu être obtenu avant le dépôt. Nous avons appliqué au SMS la règle que le contrat impose au paiement : le portail construit le SMS (≤ 160 caractères) aux mêmes moments que l'email, l'enregistre, et le personnel le lit dans « SMS (simulation) ». Un vrai fournisseur se branche derrière le port `ISmsSender` sans toucher au métier. Ce qui manque : l'adaptateur réel, et la désactivation des SMS par le candidat (critère optionnel).
- **Sauvegardes hors site (US-027).** Hors contrat, mais nécessaires à l'exploitation. Aujourd'hui, une copie de la base est faite avant chaque déploiement, sur la VM elle-même ; elle ne protège pas d'une perte de la VM. C'est écrit dans `NFR.md`.
- **Cloudinary, Vercel, Railway.** Abandonnés : fichiers sur un volume de la VM (ADR-007), tout le portail sur la VM de la FDS (ADR-006, ADR-009).

**Pourquoi le plan n'a pas été tenu à la lettre :** deux changements de fond l'ont déformé. Le 31 octobre, la Faculté nous a appris que l'admission est unique (tout candidat entre en MPC) : le modèle « une candidature par cursus » était faux (review 01, ADR-008). Et le 4 novembre, la mise en ligne sur la VM a fait apparaître des problèmes qu'aucun test local ne montrait (dépendances, schéma de base, proxys), d'où l'Epic 5.

---

## 3. Journal de la méthode

**Ce que l'historique git montre, sans arrangement :** 110 commits sur `master` au 6 novembre, dont 63 hors fusions de PR (extrait au §7). Les documents fondateurs sont commités avant le code (22–30 septembre). Puis **un trou d'un mois** : un seul commit entre le 30 septembre et le 31 octobre. L'essentiel du code est écrit du 1er au 5 novembre (31 commits le 1er novembre, 36 le 5). Le rythme proposé par le cours (six semaines régulières) n'a pas été tenu.

**Ce qui a marché :**
- **Une branche et une PR par story**, avec `Issue : #N` dans le corps, et des stories empilées (`US-006` construite sur la branche d'`US-005`, etc.) pour avancer sans attendre les fusions.
- **Les notes de réalisation** (*As-built notes*) de chaque story disent ce qui a été vérifié **et ce qui ne l'a pas été** (« Non vérifié : le rendu dans un navigateur », « Non vérifié : PostgreSQL »). Plusieurs contredisent leur story (US-009 : la barre « décision finale » remplacée par « pièces validées sur 5 » ; US-013 : décision définitive au lieu de modifiable).
- **La protection de `master`** (trois contrôles obligatoires, appliqués aussi aux administrateurs) a refusé plusieurs fusions trop tôt.
- **Le test de retour arrière en production** : une version volontairement cassée (PR #53) a été déployée ; le script est revenu seul à la version précédente ; l'annulation (#54) a été redéployée.

**Ce qui a été abandonné ou adapté :**
- **Le Refine a été fait par Epic, pas par story.** Chaque Epic 2 à 5 a son `epic-NNN-refinement.md` (constats numérotés, questions, ordre de construction). En revanche, les stories des Epics 2 et 3 ont souvent été écrites et construites le même jour, sans Refine propre. Celles de l'Epic 5 l'ont été (constats `E5-1` à `E5-7` vérifiés sur la VM avant le code).
- **La clôture des Epics** : l'Epic 1 a été fermé avec ses huit étapes le 26 septembre. **Les Epics 2 et 3 n'ont été fermés que le 6 novembre**, plusieurs jours après la livraison de leurs stories : closeouts et specs WS-02 à WS-05 écrits à ce moment-là, à partir des notes de réalisation. Les issues et les Milestones n'ont été fermés que le même jour : jusque-là, toutes les issues des stories livrées étaient restées ouvertes sur le board. **Les Epics 4 et 5 sont ouverts** au dépôt : US-016 et US-029 attendent la validation en production, US-027 n'est pas construite.
- **Les reviews** : les quatre ont été écrites le jour de la découverte (01 le 1er novembre ; 02, 03, 04 les 5 et 6 novembre). Il n'y en a pas pour octobre, parce qu'il ne s'est rien passé en octobre.
- **Le statut des stories** n'a été mis à jour qu'en fin de projet (le 5 novembre, 21 stories passées en Done d'un coup, après validation par le Project Owner).

---

## 4. Trois décisions difficiles

### 4.1 Stocker les pièces sur la VM plutôt que sur Cloudinary (ADR-007)

**Décidé :** un port `IStockageFichiers` dans le domaine, et un seul adaptateur écrit, sur un volume Docker de la VM. **Écarté :** Cloudinary, prévu dans le cahier des charges (ADR-004). **Pourquoi :** une clé d'API externe pour des pièces d'identité de mineurs, un service étranger de plus dont le portail dépend, et l'impossibilité de développer ou tester sans réseau. Le port garde la porte ouverte : Cloudinary s'ajouterait sans toucher au métier. **Coût accepté :** base et fichiers sont sur la même machine ; perdre la VM, c'est tout perdre, d'où US-027. **Ce que la décision a laissé derrière elle :** cinq semaines plus tard, six documents décrivaient encore Cloudinary (review 04).

### 4.2 L'admission unique : retirer le choix du cursus de la candidature (ADR-008)

**Décidé :** une seule candidature, au Premier cycle MPC, sans champ cursus ; une liste unique de 5 pièces ; unicité `(email, campagne)`. **Écarté :** le modèle initial, une candidature par cursus avec des pièces variables, déjà inscrit dans la spec, le glossaire, le loader et le formulaire prévu. **Pourquoi :** c'est la règle de la Faculté (MPC pendant 2 ans, puis choix de la branche hors du portail). Garder un champ cursus « au cas où » aurait trompé les candidats et imposé une migration plus tard. **Coût :** une story de réalignement (US-018) avant la première story de candidature, et la correction de six documents.

### 4.3 Déployer par images GHCR et SSH restreint, plutôt qu'avec un runner sur la VM (ADR-009)

**Décidé :** GitHub Actions construit les images, les publie sur GHCR, puis se connecte en SSH avec une clé qui ne peut lancer qu'un script (`command=` dans `authorized_keys`) ; le script copie la base, applique les migrations, vérifie `/api/v1/sante` pendant 90 s et revient seul à la version précédente si besoin. **Écarté :** un runner GitHub auto-hébergé sur la VM (le dépôt est public : un fork pourrait y exécuter du code), Dokploy (une couche de plus pour un seul portail), la construction des images sur la VM (charge la production, versions non reproductibles). **Coût accepté :** si l'UEH ferme un jour le port SSH à Internet, GitHub ne pourra plus déployer.

---

## 5. Ce que les reviews ont révélé

Quatre reviews, chacune écrite le jour de la découverte. Les trois plus importantes :

**1. « Le candidat choisit un cursus en postulant. »** *(review 01, 31 octobre)* — **Ce qui l'a contredit :** le référent de la Faculté, en revoyant les maquettes : l'admission est unique, au MPC, et les pièces sont 5, sans certificat médical ni de bonne vie et mœurs. Le code (`cursus_loader.py`) exigeait déjà une « attestation MPC » pour les autres cursus : l'indice était là, personne ne l'avait lu. **Version corrigée :** ADR-008, US-018, fait critique 9 d'`AGENTS.md`.

**2. « Notre frontend respecte Feature-Sliced Design, et notre backend est bien testé. »** *(review 02, 5 novembre)* — **Ce qui l'a contredit :** le premier lancement de `npx steiger src` a trouvé **53 violations** (imports qui contournent l'API publique des segments, imports croisés entre entités) ; le premier calcul du CRAP a trouvé un script **sans aucun test**, à 30,00, pile au seuil. Avoir les bons dossiers ne disait rien du sens des imports ; 338 tests verts ne disaient rien du fichier qu'aucun test n'appelait. **Version corrigée :** 0 erreur steiger, CRAP maximum 17, les deux contrôles dans la CI, avec échec au-dessus du seuil.

**3. « Le paiement simulé et les emails sont livrés. »** *(review 03, 5 novembre)* — **Ce qui l'a contredit :** la relecture ligne à ligne du contrat. Le paiement ne savait que réussir ou refuser une saisie invalide, alors que le cours exige « réussi, échoué, refusé, relancé ». Les emails étaient codés et testés… mais désactivés en production. Nos critères d'acceptation avaient été écrits depuis notre plan, jamais relus contre le contrat. **Version corrigée :** les quatre cas de paiement ; emails activés en production avec un domaine d'envoi dédié ; deux règles dans la définition de fini (« un critère se relit contre le contrat », « livré = fonctionne en production »).

*La review 04 (documents fondateurs qui décrivaient encore Cloudinary et Railway, `SOLUTION_DESIGN.md` présent deux fois dont un gabarit vide) a produit la règle « une ADR qui remplace un choix impose de chercher l'ancien nom partout ».*

---

## 6. Le travail avec l'agent

**Comment nous l'avons utilisé.** Nous avons travaillé avec Claude Code (Opus) dans VS Code, sur tout le cycle : rédaction des stories et des refinements avec les skills du kit (`user-story`, `epic`, `document-learning`), écriture du code story par story, une branche et une PR à chaque fois, puis mise à jour des specs, des reviews et des learnings. L'agent n'a jamais eu la main sur ce qui engage l'équipe : nous validions chaque PR avant fusion, et nous posions nous-mêmes les secrets sur la VM.

**Où l'agent s'est trompé, et comment nous l'avons recadré :**
- **Des adresses IP réelles dans un dépôt public.** Il a copié dans des tests des adresses relevées dans les journaux de la VM. Nous l'avons refusé avant la publication. → Adresses fictives (RFC 5737), et règle « Pas d'adresse réelle » dans la définition de fini (`PROJECT_WORKFLOW.md`).
- **Un mot de passe par défaut** (`fds_secret_pass`) laissé dans `docker-compose.yml`, signalé par GitGuardian. → `POSTGRES_PASSWORD` obligatoire, sans valeur par défaut ; règle « Pas de secret en clair, pas même une valeur par défaut ».
- **Croire que les documents suivaient les décisions**, et que les stories cochées couvraient le contrat. Il ne l'a pas vu seul : c'est notre relecture du contrat qui l'a révélé (reviews 03 et 04).
- **Affirmer sans avoir vérifié.** Il a écrit que le domaine d'envoi Resend était « vérifié » avant que nous l'ayons vu vérifié, et il a annoncé 25 issues à fermer alors que 22 seulement étaient ouvertes. Nous avons fait corriger la spec avant la fusion, et nous avons pris l'habitude de lui demander la commande qui prouve ce qu'il affirme.
- **Une action non demandée.** Un formateur de code lancé de sa propre initiative a réécrit tout un fichier. Le changement a été annulé et refait à la main.

**Les règles que nous lui avons imposées** (dans `CLAUDE.md` et dans la conversation) :
- demander avant d'ouvrir ou de fusionner une PR ;
- ne fermer une issue ou un Milestone qu'avec notre accord explicite ;
- ne jamais contourner la protection de `master` (pas de `--admin`) ;
- ne jamais manipuler de clé ou de mot de passe dans la conversation : les secrets vont dans le `.env` de la VM, et c'est nous qui les posons ;
- seuls les membres de l'équipe changent le statut d'une story.

**Ce qui est dans `AGENTS.md` à cause de l'agent.**
- **La carte des dossiers et la ligne « Services », corrigées le 6 novembre :** un agent neuf aurait cherché un adaptateur Cloudinary qui n'existe pas (review 04).
- **Le fait critique 7, réécrit pour décrire la protection réellement en place :** `get_current_admin` posé sur le routeur admin, dont toute nouvelle route hérite.
- **Le fait critique 9 (admission unique au MPC) :** il empêche un agent de réintroduire un champ « cursus » dans la candidature.

Notre constat : l'agent écrit vite du code correct et testé. Il ne sait pas ce que la Faculté veut, ni ce qui est vrai en production. Ces deux vérifications sont restées notre travail.

## 7. Les preuves

| Preuve | Valeur au 6 novembre | Comment la vérifier |
|---|---|---|
| Tests backend | **374 tests verts** (unitaires, intégration, architecture, migrations) | `pytest tests/` |
| Tests frontend | 19 tests (`node --test`, fonctions utilitaires) ; `tsc -b`, oxlint sans avertissement, build | `cd frontend && npm test` |
| Architecture | `test_architecture.py` (règle de dépendance) ; **steiger : 0 erreur** | `npx steiger ./src` |
| **Score CRAP** | **moyenne 2,56 ; maximum 17,00** (`valider_informations`, complexité 17, couverture 97,8 %) ; 0 fonction au-dessus de 30 ; 253 fonctions | Commande dans le `README.md` ; `tools/crap.py` |
| Couverture | ≈ 97 % du backend (le frontend n'est pas mesuré par le CRAP : limite assumée, review 02 F4) | `coverage report` |
| CI | 3 contrôles obligatoires pour fusionner sur `master` | Onglet « Actions » du dépôt |
| Production | https://dorfilus.ueh.edu.ht ; `GET /api/v1/sante` → `{"statut":"ok"}` | Navigateur |
| Retour arrière | PR #53 (version cassée) → retour automatique ; #54 redéployée | Journal du workflow « Déploiement » |

**Extrait de l'historique** (`git log origin/master --no-merges --date=short --format="%ad %h %s"`, au 6 novembre) :

```
# Le début : documents fondateurs et Epic 1, puis le mois creux
2026-09-22 6ebd611 initialisation
2026-09-26 510ccc1 remplissage des documents
2026-09-26 d838977 feat(ci): socle backend clean architecture et workflow ci pytes
2026-09-26 894a6ab us-001
2026-09-26 fb39305 feat(epic-001): close Epic 1 — Socle & Portail public (US-001, US-002, US-003, US-004)
2026-09-26 334a63c refactor(cursus): rely purely on JSON reference files in cursus/ without SQL tables
2026-09-27 178136f docs(epic-002): scaffold Epic 2 refinement and user stories (US-005 to US-009)
2026-09-29 f992298 docs(livrable-1): remaniement CDC + scaffold Epics 3-4 et US-010 a US-017
2026-09-30 0998ba3 configuration
2026-10-28 8a2c6f7 repartition des taches
2026-11-01 2860739 docs(admission): admission unique au MPC, 5 pieces requises, ADR-008
2026-11-01 2cb0a5d docs(stories): ajoute US-018 (alignement admission unique), US-019 (Histoire/Contact), US-020 (Kreyol)
2026-11-01 9cd69d8 feat(us-018): aligner le portail public sur l'admission unique au MPC
2026-11-01 7b9fee1 feat(us-005): backend du formulaire d'inscription et de la question deplacement_physique
…
# La fin : clôtures, mise en production, derniers ajouts
2026-11-05 231ee6b feat(postuler): mise en page bureau du tunnel de candidature et du remplacement
2026-11-05 0ae26fe docs: clôture des Epics 2 et 3, specs WS-02 à WS-05
2026-11-05 a6fb5d2 docs(learnings): trois apprentissages tirés du projet (04 à 06)
2026-11-05 3e0bf90 docs(rapport): premier jet du rapport (sections 1 à 5 et 7 ; trame des sections 6, 8, 9)
2026-11-06 865f96c docs: US-028 validée ; issues et Milestones des Epics 2 et 3 fermés
2026-11-06 1d3ad87 docs: emails confirmés en production (review 03, F2 corrigé)
2026-11-06 b9bb9bd fix: favicon de la FDS à la place de l'icône Vite
2026-11-06 c544cfd gestiond'acces
2026-11-06 ec38bcc docs(us-029): gestion des accès dans les specs WS-04, story US-029
2026-11-06 581797a feat(us-020): noms et descriptions des cursus en kreyòl
2026-11-06 06bf92b feat(us-016): notifications SMS simulées, comme le paiement
2026-11-06 f1fa3ec docs: une seule ligne « prochaine story » dans EPIC_EXECUTION
```

Commits par jour, fusions comprises : 22/09 : 1 · 26/09 : 5 · 27/09 : 1 · 29/09 : 1 · 30/09 : 1 · **28/10 : 1** · 01/11 : 31 · 02/11 : 3 · 03/11 : 2 · 04/11 : 13 · 05/11 : 36 · 06/11 : 15.

*Captures à insérer : le board GitHub Projects, la page « Actions » (CI et déploiements verts), la sortie de `tools/crap.py`, la page d'accueil en production sur téléphone et sur ordinateur.*

---

## 8. Learnings

**Ce que nous referions :**
- **Une branche, une PR et des notes de réalisation par story**, avec « vérifié » et « non vérifié ». Ces notes nous ont permis d'écrire les specs et les closeouts après coup sans rien inventer.
- **Protéger `master` par des contrôles obligatoires**, et mettre le retour arrière automatique à l'épreuve avec une version volontairement cassée (PR #53).
- **Des ports dans le domaine** pour chaque service externe (stockage, email, SMS). Simuler le SMS comme le paiement n'a demandé aucun changement du métier, et un vrai fournisseur pourra s'ajouter de la même façon.

**Ce que nous ne referions pas :**
- **Laisser un mois sans commit** (octobre), puis tout écrire en cinq jours.
- **Déployer la semaine 6.** La VM a révélé en une journée des problèmes qu'aucun test local ne montrait : dépendances sans borne haute, base créée sans Alembic, adresse du visiteur masquée par les proxys (learning [`04`](../project-docs/learnings/04-tester-sur-le-moteur-de-production.md), Epic 5).
- **Écrire les critères d'acceptation depuis notre plan** sans les relire contre le contrat : le paiement ne gérait pas l'échec, et les emails étaient désactivés en production (review 03).

**Ce qui changerait lundi prochain, sur un autre sujet :**
- Mettre en production dès la semaine 2, même une page vide, et faire tourner la CI sur le même moteur de base que la production.
- Lancer dès le premier jour les contrôles du cours (steiger, CRAP) plutôt qu'à la fin : 53 violations FSD étaient cachées (review 02).
- Quand une décision en remplace une autre, chercher l'ancien nom dans tout le dépôt le jour même (learning [`06`](../project-docs/learnings/06-propager-une-decision-par-recherche.md)).
- Faire valider le modèle métier par la Faculté avant d'écrire la première story : l'admission unique a coûté une story de réalignement et six documents à corriger (review 01).

Les apprentissages détaillés sont dans le dépôt : [`04`](../project-docs/learnings/04-tester-sur-le-moteur-de-production.md) (tester sur le moteur de production), [`05`](../project-docs/learnings/05-adopter-une-base-existante.md) (adopter une base existante dans un outil de migrations), [`06`](../project-docs/learnings/06-propager-une-decision-par-recherche.md) (propager une décision par une recherche).

## 9. Contributions individuelles

Les stories sont celles assignées à chaque membre sur le board GitHub Projects.

| Membre | Stories | Ce qu'il peut expliquer en soutenance |
|---|---|---|
| VAILLANT Valcin *(capitaine)* | US-007 (téléversement sécurisé des pièces), US-011 (authentification JWT et rôles), US-012 (tableau de bord et revue des dossiers), US-015 (export CSV et PDF filtré) | La validation des fichiers côté serveur (magic bytes, extension, 5 Mo) ; le JWT HS256 et bcrypt, les rôles `admin` et `agent` ; les filtres et l'export |
| DORFILUS Skin-Paolatchi | US-001 à US-004 (cursus, fiche, tests d'architecture en CI, premier déploiement), US-018 à US-022 (admission unique, Histoire et Contact, kreyòl, refonte visuelle), US-023 à US-027 (Alembic, adresse réelle derrière les proxys, CI frontend, déploiement continu, sauvegardes), US-028 (calendrier d'admission), US-029 (gestion des accès). **Hors dépôt :** obtention de la VM Proxmox et de l'accès UEH (sous-domaine, proxy Apache) ; DNS Namecheap et domaine d'envoi Resend ; maquettes de la refonte visuelle. **Documents :** cahier des charges, documents fondateurs, specs, reviews, learnings, rapport, avec l'agent | La Clean Architecture et `test_architecture.py` ; le déploiement GHCR, SSH restreint et retour arrière (ADR-009) ; l'adoption d'une base existante par Alembic ; le calendrier en heure d'Haïti ; le pilotage de l'agent |
| GUERRIER Joas | US-005 (formulaire et `deplacement_physique`), US-006 (simulation MonCash / NatCash), US-008 (finalisation et confirmation), US-014 (email après décision), US-016 (SMS simulés) | Les quatre cas du paiement simulé ; la référence `CAN-2026-X` ; l'email non bloquant (tâche de fond) ; les SMS de 160 caractères au plus |
| LOUIS Widmaken | US-009 (suivi par référence), US-010 (remplacement d'une pièce rejetée), US-013 (validation ou rejet audité), US-017 (mode sombre) | Le suivi sans compte ; le remplacement par upsert sur `(candidat_id, document_requis_id)` ; l'audit `valide_par` et `date_validation` ; le thème sombre |

---

*Rapport — FDS Portail — Bravetech · GL-EN3-2026*
