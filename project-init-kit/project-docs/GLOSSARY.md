---
created: 2026-09-26T00:35:00Z
updated: 2026-09-26T00:35:00Z
---

# GLOSSARY.md — FDS Portail

**Réponses :** Que signifie ce terme ? — consulter ce document chaque fois qu'un mot est ambigu.
**Dépend de :** `PRD.md` + `PLAN.md`.

---

## Acteurs et rôles

*Qui ou quoi interagit avec ce système, dans une capacité distincte.*

| Terme | Définition |
|---|---|
| **Candidat** | Lycéen ou adulte souhaitant s'inscrire à la FDS-UEH. Accès entièrement public — aucun compte requis. S'identifie via sa **référence dossier** pour le suivi. Peut consulter les cursus, postuler, uploader des documents, suivre son dossier et remplacer un document rejeté. |
| **Administrateur (Admin)** | Agent du secrétariat FDS. Accès authentifié (email + mot de passe → JWT). Peut consulter toutes les candidatures, valider ou rejeter des documents. Toute action est auditée. En cas de conflit de besoin avec le Candidat, l'Admin est prioritaire (traçabilité > simplicité). |
| **Agent** | Sous-rôle d'Administrateur avec permissions potentiellement réduites. Identifiant de rôle : `agent` (vs `admin`). Non différencié fonctionnellement en V1 — distinction préparée pour post-MVP. |
| **Système** | Le backend FastAPI agissant de façon autonome : génération de références, déclenchement d'emails, validation des fichiers. N'est pas un acteur humain. |

> **Terme à ne pas confondre :** « utilisateur » n'est jamais utilisé seul dans ce projet — il désigne toujours un Candidat (public) ou un Administrateur (authentifié). Utiliser le terme précis selon le contexte.

---

## Composants du système

*Les éléments qui tournent ou se déploient indépendamment.*

| Terme | Définition |
|---|---|
| **FDS Portail** | Le produit dans son ensemble — comprend le frontend et le backend. À ne pas confondre avec les autres modules de l'écosystème FDS (FDS Pay, FDS Akademi, FDS SYS). |
| **Frontend** | Application React/Vite (SPA) hébergée sur Vercel. Sert les pages publiques (cursus, candidature, suivi) et le tableau de bord admin. Structure interne : Feature-Sliced Design (FSD). |
| **Backend** | API FastAPI hébergée sur Railway. Structure interne : Clean Architecture (4 couches). Expose les endpoints REST sous `/api/v1/`. Source de vérité : PostgreSQL. |
| **FDS SYS** | Système externe — System of Record des identités des administrateurs FDS. FDS Portail *consomme* ces identités mais ne les gère pas. Non livré en V1 : les comptes admin sont créés manuellement. |
| **FDS Pay** | Module externe de paiement réel (MonCash/NatCash). Non livré en V1 — FDS Portail simule le paiement. |

---

## Stockages de données

*Où l'information persiste réellement.*

| Terme | Définition |
|---|---|
| **Fichiers JSON (`cursus/`)** | **Source de vérité pour l'offre académique.** Fichiers JSON officiels décrivant les filières, matières et pièces requises par cursus (`mpc.json`, `genie-civil.json`, etc.). Données de référence statiques versionnées avec le code, sans nécessité de table SQL. |
| **PostgreSQL** | **Source de vérité des dossiers candidats.** Conteneurisé sous Docker sur VM Linux / Proxmox (ADR-006). Contient les tables transactionnelles (`candidats`, `candidatures`, `documents_soumis`, `utilisateurs`). Backup régulier. Perte = perte de dossiers. |
| **Cloudinary** | Stockage des fichiers physiques (PDF, JPG) uploadés par les candidats. Stockage secondaire — les fichiers survivent si PostgreSQL est perdu, mais les dossiers associés ne peuvent pas être reconstitués sans la base. URLs signées, accès via proxy admin. |
| **Mémoire application** | L'API FastAPI est **stateless** — aucun état de session persisté entre les requêtes. Cache en mémoire pour la lecture des fichiers JSON de cursus. |

> **Règle absolue :** Les URLs Cloudinary et les statuts d'email ne remplacent jamais les données PostgreSQL. Les informations académiques des cursus émanent directement des fichiers JSON officiels.

---

## Vocabulaire du domaine

*Termes de processus ou de contenu qu'un outsider pourrait mal interpréter.*

| Terme | Définition |
|---|---|
| **Référence dossier** | Identifiant unique d'une candidature, format `CAN-YYYY-NNNN` (ex. `CAN-2026-0089`). Générée par le backend au moment de la soumission. Sert de clé d'accès public au suivi — remplace un login pour le Candidat. |
| **Dossier** | L'ensemble des informations et documents soumis par un Candidat pour une candidature. Synonyme de "candidature" dans les conversations courantes — mais dans le code, c'est l'entité `Candidat` qui porte le dossier. |
| **Document requis** | Pièce justificative exigée par la FDS pour une candidature (ex. diplôme, pièce d'identité). Défini dans la table `documents_requis`. Référence : ce que le candidat *doit* fournir. |
| **Document soumis** | Fichier effectivement uploadé par un Candidat pour satisfaire un Document requis. Entité `DocumentSoumis` en base. Un Document soumis remplace le précédent en cas de rejet (upsert — jamais deux lignes pour le même `(candidat_id, document_requis_id)`). |
| **Statut de validation** | État d'un Document soumis. Trois valeurs possibles : `en_attente` (uploadé, pas encore traité), `valide` (approuvé par un Admin), `rejete` (refusé par un Admin). Alimente la barre de progression du suivi. |
| **Déplacement physique** | Champ booléen `deplacement_physique` sur l'entité `Candidat`. Indique si le candidat a dû se déplacer physiquement pour compléter sa candidature. Valeur cible : `false` pour ≥ 70 % des dossiers (critère de succès PRD §11). |
| **Walking Skeleton** | Implémentation minimale traversant toutes les couches du système de bout en bout : d'un `POST /api/v1/candidature` jusqu'à l'affichage de la référence à l'écran et l'envoi de l'email. Objectif de `epic-002`. |
| **Simulation de paiement** | Dans FDS Portail V1, le paiement MonCash/NatCash est simulé — aucune transaction réelle n'a lieu. Le candidat saisit une référence transactionnelle fictive, et le système la persiste comme si elle était valide. Le paiement réel est délégué à FDS Pay (hors V1). |
| **Proxy document** | Endpoint admin (`GET /api/v1/admin/proxy-document`) qui récupère un fichier Cloudinary et le sert au client après vérification du JWT. Empêche l'accès direct aux URLs Cloudinary sans authentification. |
| **Audit** | Enregistrement immuable de chaque décision admin sur un Document soumis — champs `valide_par` (ID de l'Admin) et `date_validation` (timestamp). Permet au secrétariat de justifier toute décision. |
| **Upsert** | Opération d'écriture qui crée un Document soumis s'il n'existe pas, ou le met à jour s'il existe déjà (sur la contrainte UNIQUE `(candidat_id, document_requis_id)`). Utilisé lors du remplacement d'un document rejeté — garantit qu'un candidat n'a jamais deux lignes pour le même document. |
| **Magic bytes** | Signature binaire au début d'un fichier identifiant son vrai format (ex. `%PDF-` pour les PDFs). Vérifiés côté serveur via la bibliothèque `filetype` pour empêcher l'upload de fichiers exécutables renommés en `.pdf` ou `.jpg`. |
| **Période d'inscription** | Fenêtre temporelle pendant laquelle les candidatures sont ouvertes. Correspond au pic de charge connu — aucune maintenance tolérée durant cette période. |

---

## Workstream, Epic et Milestone

*Générique — conservé tel quel.*

- **Workstream** = *quelle zone fonctionnelle*. Ne finit jamais. Peut être revisité par un Epic ultérieur. Identifiant : `WS-NN` (deux chiffres).
- **Epic** = *quand, et à quel volume à la fois*. Étape de construction séquentielle et cadrée dans le temps. Identifiant : `epic-NNN-name` (dossier à trois chiffres).
- **Milestone** = *ce qui est livré*. La représentation GitHub d'un Epic — pas un quatrième concept séparé.

**Workstreams de FDS Portail :** WS-01 (Portail public), WS-02 (Candidature), WS-03 (Suivi), WS-04 (Administration), WS-05 (Notifications) — définis dans `SOLUTION_DESIGN.md §2`.

---

## Documents du projet

*Simple pointeur.*

La liste canonique de tous les autres documents du projet : voir `PRD.md §14` — Documents associés.

---

*GLOSSARY.md — FDS Portail — Bravetech · GL-EN3-2026*
