---
created: 2026-11-01T12:00:00Z
updated: 2026-11-01T15:51:55Z
---

# 01 — Admission unique au MPC (ce que nous croyions sur le choix du cursus)

**Contexte :** relecture des maquettes frontend avec le référent métier de la Faculté, le 2026-10-31, avant le démarrage d'`US-005`.

## Découvertes

| ID | Ce que nous croyions | Ce qui est vrai | Preuve | Statut |
|---|---|---|---|---|
| F1 | Le candidat choisit un cursus (Génie Civil, Électronique, etc.) en postulant. Le modèle portait `cursus_slug` sur `Candidat`, l'unicité `(email, cursus_slug, campagne)` et une étape « choix de filière » (US-005). | L'admission est **unique** : tout candidat entre en Premier cycle MPC (2 ans) et choisit sa branche après le MPC (3 ans). Le parcours dure 5 ans. | Déclaration du référent métier lors de la revue des maquettes. Cohérent avec `cursus_loader.py`, qui exigeait déjà une « attestation MPC » pour toute filière hors MPC. | ✅ Corrigé dans les documents |
| F2 | Les pièces requises varient selon le cursus et incluent un certificat de bonne vie et mœurs et un certificat médical. | Liste unique de 5 pièces : acte de naissance, Bac II, relevé de notes, deux photos d'identité, CIN. Pas de bonne vie et mœurs ni de certificat médical. | Déclaration du référent métier. La spec `ws-func-01` listait 6 pièces dont ces deux certificats. | ✅ Corrigé dans les documents |
| F3 | Le catalogue JSON `cursus/*.json` décrit aussi les pièces requises par cursus (`GLOSSARY.md`, `SOLUTION_DESIGN.md §6`, `ws-tech-01`). | Les fichiers JSON ne contiennent que filière, durée et niveaux. Les pièces sont codées dans `backend/dal/cursus_loader.py`. | Lecture de `cursus/*.json` (clés `filiere`, `duree_annees`, `niveaux`) et du loader. | ✅ Documents corrigés, code à aligner (voir ci-dessous) |
| F4 | La durée totale était « 5 ans / 10 semestres, ou 1 an pour MPC » selon la spec fonctionnelle. | MPC 2 ans (`mpc.json`), branches 3 ans, total 5 ans. | `duree_annees` dans les fichiers JSON ; confirmation du référent métier. | ✅ Corrigé |
| F5 | L'adresse de la Faculté est « Rue Monseigneur Guilloux, Port-au-Prince ». | La Faculté est installée à Delmas 33. | Document « Histoire de la Faculté » et confirmation du référent métier. | ✅ Corrigé |

## Résolution

Chaque règle issue de ces découvertes a été déplacée dans son document propriétaire :

| Règle | Destination |
|---|---|
| Admission unique, parcours MPC + branche, 4 étapes de candidature | `PRD.md` (§1, §3, §6, §13) |
| Vocabulaire : Admission unique, MPC, Branche, Parcours en 5 ans, Pièces requises d'admission | `GLOSSARY.md` |
| Décision d'architecture : pas de `cursus_slug`, unicité `(email, campagne)`, pièces uniques | `SOLUTION_DESIGN.md §14` (ADR-008) |
| Comportement des écrans (accueil, fiche MPC, fiche branche, Histoire, Contact, langues, images) | `functional-specs/ws-func-01-portail-public.md` |
| Écart code / règle sur les pièces | `technical-specs/ws-tech-01-portail-public.md §3` |
| Règles actives pendant l'Epic 2 (R5, R6) et findings E2-6 à E2-8 | `execution/epic-002-candidature/epic-002-refinement.md` (vidé à la clôture) |
| Fait qu'aucune session ne doit oublier | `AGENTS.md` (fait critique 9) |
| Stories concernées | `US-005`, `US-007`, `US-008`, `US-009`, `US-012`, `US-015` |
| Contrainte de qualité sur les images | `NFR.md` (Performance) |

## Reste à faire côté code (hors périmètre de cette mise à jour des documents)

- `backend/dal/cursus_loader.py` : 5 pièces uniques, sans attestation MPC ni variante par cursus.
- `backend/api/v1/cursus.py` et DTO : ne plus exposer de pièces par cursus ; fiche MPC avec parcours en 5 ans.
- Frontend : accueil (carte MPC mise en avant), fiche MPC, fiches des branches sans pièces ni bouton de candidature.
