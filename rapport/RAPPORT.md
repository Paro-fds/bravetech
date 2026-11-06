---
created: 2026-11-06T04:30:00Z
updated: 2026-11-06T18:35:56Z
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
| Pull Requests | https://github.com/Paro-fds/bravetech/pulls?q=is%3Apr — 30+ PR fusionnées, dont #48 (Alembic), #52 (déploiement continu), #53/#54 (test de retour arrière), #55 (steiger, CRAP), #60 (calendrier) |
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

**Ajouté en cours de route, hors plan initial :** l'Epic 4 (Histoire et Contact, interface en kreyòl, refonte visuelle d'après les maquettes, export, mode sombre, calendrier d'admission) et l'Epic 5 (Alembic, adresse réelle du visiteur derrière les proxys, CI frontend, déploiement continu). L'export, d'abord Won't Have, a été rétabli quand nous avons relu le contrat, qui le place en Could.

**Coupé ou non livré, et pourquoi :**
- **SMS réels (US-016, Should Have) : simulés, pas envoyés.** Aucun fournisseur SMS (Twilio, opérateur haïtien) n'a pu être obtenu avant le dépôt. Nous avons appliqué au SMS la règle que le contrat impose au paiement : le portail construit le SMS (≤ 160 caractères) aux mêmes moments que l'email, l'enregistre, et le personnel le lit dans « SMS (simulation) ». Un vrai fournisseur se branche derrière le port `ISmsSender` sans toucher au métier. Ce qui manque : l'adaptateur réel, et la désactivation des SMS par le candidat (critère optionnel).
- **Sauvegardes hors site (US-027).** Hors contrat, mais nécessaires à l'exploitation. Aujourd'hui, une copie de la base est faite avant chaque déploiement, sur la VM elle-même ; elle ne protège pas d'une perte de la VM. C'est écrit dans `NFR.md`.
- **Cloudinary, Vercel, Railway.** Abandonnés : fichiers sur un volume de la VM (ADR-007), tout le portail sur la VM de la FDS (ADR-006, ADR-009).

**Pourquoi le plan n'a pas été tenu à la lettre :** deux changements de fond l'ont déformé. Le 31 octobre, la Faculté nous a appris que l'admission est unique (tout candidat entre en MPC) : le modèle « une candidature par cursus » était faux (review 01, ADR-008). Et le 4 novembre, la mise en ligne sur la VM a fait apparaître des problèmes qu'aucun test local ne montrait (dépendances, schéma de base, proxys), d'où l'Epic 5.

---

## 3. Journal de la méthode

**Ce que l'historique git montre, sans arrangement :** 94 commits. Les documents fondateurs sont commités avant le code (22–30 septembre). Puis **un trou d'un mois** : un seul commit entre le 30 septembre et le 31 octobre. L'essentiel du code est écrit du 1er au 5 novembre (31 commits le 1er novembre, 35 le 5). Le rythme proposé par le cours (six semaines régulières) n'a pas été tenu.

**Ce qui a marché :**
- **Une branche et une PR par story**, avec `Issue : #N` dans le corps, et des stories empilées (`US-006` construite sur la branche d'`US-005`, etc.) pour avancer sans attendre les fusions.
- **Les notes de réalisation** (*As-built notes*) de chaque story disent ce qui a été vérifié **et ce qui ne l'a pas été** (« Non vérifié : le rendu dans un navigateur », « Non vérifié : PostgreSQL »). Plusieurs contredisent leur story (US-009 : la barre « décision finale » remplacée par « pièces validées sur 5 » ; US-013 : décision définitive au lieu de modifiable).
- **La protection de `master`** (trois contrôles obligatoires, appliqués aussi aux administrateurs) a refusé plusieurs fusions trop tôt.
- **Le test de retour arrière en production** : une version volontairement cassée (PR #53) a été déployée ; le script est revenu seul à la version précédente ; l'annulation (#54) a été redéployée.

**Ce qui a été abandonné ou adapté :**
- **Le Refine a été fait par Epic, pas par story.** Chaque Epic 2 à 5 a son `epic-NNN-refinement.md` (constats numérotés, questions, ordre de construction). En revanche, les stories des Epics 2 et 3 ont souvent été écrites et construites le même jour, sans Refine propre. Celles de l'Epic 5 l'ont été (constats `E5-1` à `E5-7` vérifiés sur la VM avant le code).
- **La clôture des Epics** : l'Epic 1 a été fermé avec ses huit étapes le 26 septembre. **Les Epics 2 et 3 n'ont été fermés que le 6 novembre**, plusieurs jours après la livraison de leurs stories : closeouts et specs WS-02 à WS-05 écrits à ce moment-là, à partir des notes de réalisation. Les issues et les Milestones n'ont été fermés que le même jour : jusque-là, toutes les issues des stories livrées étaient restées ouvertes sur le board. **Les Epics 4 et 5 sont ouverts** au dépôt (US-016 et US-027).
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

> **À rédiger par l'équipe, à la première personne.** Cette section évalue votre pilotage de l'agent : ce que vous lui avez demandé, où il s'est trompé, comment vous l'avez recadré, et ce qui a fini dans `AGENTS.md`. Matériau vérifiable à reprendre (ou à remplacer par vos propres exemples) :

**Où l'agent s'est trompé, et le recadrage :**
- Il a écrit des **adresses IP réelles** relevées dans les journaux de la VM dans des tests destinés à un dépôt public ; refusé avant la publication. → Adresses fictives (RFC 5737), et règle « Pas d'adresse réelle » dans la définition de fini (`PROJECT_WORKFLOW.md`).
- Il a laissé un **mot de passe par défaut** (`fds_secret_pass`) dans `docker-compose.yml` ; signalé par GitGuardian. → `POSTGRES_PASSWORD` obligatoire, sans défaut ; règle « Pas de secret en clair, pas même une valeur par défaut ».
- Il a cru que **les documents suivaient les décisions** et que **les stories cochées couvraient le contrat** (reviews 03 et 04).
- Il a déclaré un domaine d'envoi « vérifié » sans l'avoir vu vérifié ; corrigé dans la spec avant la fusion.
- Un formateur de code lancé sans être demandé a réécrit tout un fichier ; changement annulé et refait à la main.

**Règles de pilotage données à l'agent (dans `CLAUDE.md` et la conversation) :** demander avant d'ouvrir ou de fusionner une PR ; ne jamais fermer une issue ; ne jamais contourner la protection de `master` ; ne jamais manipuler de clé ou de mot de passe dans la conversation (les secrets vont dans le `.env` de la VM, posés par l'équipe) ; seuls les membres de l'équipe changent le statut d'une story.

**Ce qui est dans `AGENTS.md` à cause de l'agent :** *[à compléter : par exemple la carte des dossiers et les « Services » corrigés le 6 novembre, parce qu'un agent neuf aurait cherché un adaptateur Cloudinary qui n'existe pas (review 04) ; le fait critique 7 réécrit pour décrire la protection par routeur réellement en place.]*

---

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

*Captures à insérer : le board GitHub Projects, la page « Actions » (CI et déploiements verts), un extrait de `git log --oneline`, la sortie de `tools/crap.py`, la page d'accueil en production sur téléphone et sur ordinateur.*

---

## 8. Learnings

> **À rédiger par l'équipe** : ce que vous referiez, ce que vous ne referiez pas, ce qui changerait lundi prochain sur un autre sujet. Les trois apprentissages écrits dans le dépôt peuvent servir de point de départ :

- [`04`](../project-docs/learnings/04-tester-sur-le-moteur-de-production.md) — Une CI verte ne prouve rien sur un moteur qu'elle ne fait pas tourner : figer les dépendances, nommer le pilote, mettre en production tôt.
- [`05`](../project-docs/learnings/05-adopter-une-base-existante.md) — Adopter une base existante dans un outil de migrations en la comparant à la révision d'origine.
- [`06`](../project-docs/learnings/06-propager-une-decision-par-recherche.md) — Une décision qui en remplace une autre se propage par une recherche ; les critères se relisent contre le contrat.

*Pistes vraies à développer : déployer dès la semaine 2 plutôt que la semaine 6 ; ne pas laisser un mois sans commit ; lancer les contrôles du cours (steiger, CRAP) dès le premier jour.*

---

## 9. Contributions individuelles

> **À remplir par l'équipe**, nominativement. Cette table prépare les questions individuelles de soutenance.

| Membre | Ce qu'il a fait (stories, documents, déploiement, revues) | Ce qu'il peut expliquer en soutenance |
|---|---|---|
| VAILLANT Valcin *(capitaine)* | | |
| DORFILUS Skin-Paolatchi | | |
| GUERRIER Joas | | |
| LOUIS Widmaken | | |

---

*Rapport — FDS Portail — Bravetech · GL-EN3-2026*
