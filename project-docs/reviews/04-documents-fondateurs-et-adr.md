---
created: 2026-11-06T03:30:00Z
updated: 2026-11-06T03:03:27Z
---

# 04 — Les documents fondateurs suivaient-ils les décisions ? (Cloudinary, Railway, le gabarit oublié)

**Contexte :** le 2026-11-06, relecture des documents fondateurs avant la remise, avec la grille de notation du document de lancement (Partie 4 : « un document du kit encore rempli des questions du gabarit » est une pénalité ; test de reprise sur `AGENTS.md`).

## Découvertes

| ID | Ce que nous croyions | Ce qui est vrai | Preuve | Statut |
|---|---|---|---|---|
| F1 | Une ADR qui remplace une décision met le projet à jour : ADR-007 (2026-09-27) a remplacé Cloudinary par un volume local, ADR-006 et ADR-009 ont remplacé Railway et Vercel par la VM de la FDS. | Seul le registre des ADR avait changé. `AGENTS.md` (« Services : Cloudinary », fait critique 6 « avant tout stockage Cloudinary »), `NFR.md` (14 passages sur Railway, Vercel et Cloudinary, dont le plan de sauvegarde), `GLOSSARY.md`, `PRD.md` et `PROJECT_WORKFLOW.md` (`CLOUDINARY_*`, `SECRET_KEY`) décrivaient encore l'ancien choix, cinq semaines plus tard. Un agent neuf qui lit `AGENTS.md` aurait cherché un adaptateur Cloudinary. | `grep -i "cloudinary\|railway\|vercel"` sur les documents fondateurs : 56 occurrences dans six documents. | ✅ Corrigé le 2026-11-06 |
| F2 | `SOLUTION_DESIGN.md` est un document rempli. | Il contenait **deux fois** les sections 1 à 15 : la version du projet, puis le gabarit du kit avec 9 « *(À rédiger)* » et ses questions. Le second exemplaire portait pourtant du vrai contenu (déploiement §11, ADR-006 à ADR-009), ajouté au mauvais endroit au fil des stories, et la première §11 renvoyait à « la seconde section plus bas ». Les deux tableaux d'ADR donnaient deux sens différents aux numéros 001 à 003. | Lignes 13 et 262 du fichier avant correction : deux titres « ## 1. Objectif et périmètre ». | ✅ Fusionné : un seul document (273 lignes au lieu de 400), une seule table d'ADR ; les décisions 002 et 003 du second tableau deviennent ADR-010 et ADR-011 |
| F3 | La carte des composants de `SOLUTION_DESIGN.md` §4 décrit le code. | Elle décrivait le code imaginé le 2026-09-26 : `CandidatRepositorySQLAlchemy`, `CloudinaryStorageAdapter`, `IStorageService`, routes `/api/v1/upload` et `/api/v1/candidature/{ref}`, `python-jose` et `passlib`. Aucun de ces noms n'existe. | `backend/ports/`, `backend/dal/`, schéma OpenAPI de l'application. | ✅ Corrigé d'après le code (routes réelles, ports et adaptateurs réels) |
| F4 | Le `README.md` présente le projet. | C'était le mode d'emploi du kit d'initialisation (« copie project-init-kit dans ton projet »), inchangé depuis le 2026-09-30. Le cours attend « ce qu'est le projet, comment le lancer ». | `git log -- README.md` : un seul commit, `configuration`. | ✅ Réécrit |

## Pourquoi c'est arrivé

Chaque story a mis à jour le document qu'elle touchait directement (sa spec, son ADR), jamais les documents qui **citaient** l'ancien choix. Aucune étape de la définition de fini ne demandait de chercher l'ancien terme ailleurs.

## Résolution

| Règle | Destination |
|---|---|
| Une ADR qui remplace un choix (fournisseur, hébergement, bibliothèque) impose de chercher l'ancien nom dans les documents fondateurs et `AGENTS.md`, et de les corriger dans la même PR | `PROJECT_WORKFLOW.md` (définition de fini) |
| Un document du kit ne garde ni questions du gabarit ni « *(À rédiger)* » une fois rempli | `PROJECT_WORKFLOW.md` (définition de fini) |
