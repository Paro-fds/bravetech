---
created: 2026-09-27T12:28:00Z
updated: 2026-09-27T12:28:00Z
status: open
---

# epic-002-refinement.md — Candidature & Suivi

> **Ce fichier est la source de vérité des règles en cours pour epic-002.**  
> Toute règle technique ou décision d'arbitrage produite pendant cet Epic vit ici jusqu'à sa clôture.  
> À la clôture : chaque règle sera déplacée dans le document propriétaire, et ce fichier servira d'historique.

---

## 1. Scope de l'Epic 2

L'Epic 2 implémente le **Walking Skeleton complet côté candidat** : de la saisie des informations personnelles et la réponse à la question sur le déplacement physique, jusqu'à la simulation du paiement MonCash/NatCash, le téléversement sécurisé des pièces requises, la génération de la référence unique `CAN-2026-XXXX`, l'envoi de l'email de confirmation et la consultation de la progression sur la page de suivi.

**Ce que cet Epic ne couvre PAS :**
- L'espace d'évaluation et de validation administrative par les agents FDS (Epic 3 — WS-04).
- Le remplacement d'un document rejeté suite à notification administrative (Epic 3 — US-017).
- Les paiements monétaires réels (hors périmètre V1 — délégués à FDS Pay).

---

## 2. Découvertes (Findings)

| ID | Constat | Statut |
|---|---|---|
| E2-1 | L'offre académique et les pièces requises par cursus sont déjà disponibles via `JsonCursusRepository` sans nécessiter de tables SQL. | ✅ Confirmé (Epic 1) |
| E2-2 | Les tables relationnelles PostgreSQL sont vierges et doivent accueillir les entités candidates (`candidats`, `candidatures`, `documents_soumis`). | ✅ Prêt pour scaffold DAL |
| E2-3 | Pour respecter l'autonomie sur serveur Proxmox (ADR-006) et éviter tout blocage d'API externe en dev, le stockage de fichiers doit fonctionner en volume local persistant avec adaptateur Cloudinary optionnel. | ✅ Recommandé |
| E2-4 | L'envoi d'email doit être asynchrone et non-bloquant : un échec d'email ne doit sous aucun prétexte annuler ou bloquer une candidature valide. | ✅ Règle absolue du PRD §7 |
| E2-5 | La question `deplacement_physique` est un KPI central du PRD (§11) et doit obligatoirement être saisie et persistée. | ✅ Exigence stricte |

---

## 3. Questions ouvertes & Décisions techniques

| # | Question | Recommandation | Arbitrage proposé |
|---|---|---|---|
| Q1 | **Stockage des fichiers uploadés :** Cloudinary obligatoire ou stockage fichier sur volume Docker ? | Créer un port `IFileStorage` avec implémentation `LocalFileStorage` (volume Docker `uploads/` sur la VM Proxmox) et adaptateur `CloudinaryFileStorage` activé si clés fournies. | ✅ Hybride / Autonome (ADR-007) |
| Q2 | **Notification email sans clé API Resend :** Comment gérer le dev local ou l'absence de clé ? | Port `IEmailSender` avec `ConsoleEmailSender` (mode log/mock) si `RESEND_API_KEY` absente, et `ResendEmailSender` si configurée. | ✅ Tolérant aux pannes |
| Q3 | **Format de la référence de candidature :** Comment garantir l'unicité ? | Format `CAN-2026-XXXX` (ex: `CAN-2026-0001` ou UUID raccourci / séquence) généré côté backend lors de la validation finale. | ✅ Canonique |
| Q4 | **Contrôle de sécurité des uploads :** Comment vérifier les pièces sans exécutable ? | Vérification double : extension autorisée (`.pdf`, `.jpg`, `.jpeg`, `.png`), taille maximale (≤ 5 Mo), et vérification des magic bytes du fichier. | ✅ Sécurité stricte |

---

## 4. Découpage du lot de User Stories (Ordre de build)

Les 5 User Stories de l'Epic 2 sont ordonnées pour garantir un flux d'intégration progressif et testable :

| Ordre | Story | Titre | Dépend de | Description |
|---|---|---|---|---|
| 1 | **US-005** | Formulaire d'inscription & question `deplacement_physique` | Socle Epic 1 | Entités du domaine, tables PostgreSQL, Étape 1 du formulaire mobile (infos personnelles + question déplacement). |
| 2 | **US-006** | Simulation de paiement MonCash / NatCash | US-005 | Étape 2 du formulaire : choix opérateur, calcul des frais, validation simulée, génération `PAY-SIM-2026-XXXX`. |
| 3 | **US-007** | Téléversement sécurisé des pièces requises | US-005, US-006 | Étape 3 : upload avec jauge ≤ 5 Mo, contrôle MIME/magic bytes, stockage sécurisé des fichiers. |
| 4 | **US-008** | Finalisation de candidature & notification de confirmation | US-007 | Étape 4 : persistance finale, attribution de la référence `CAN-2026-XXXX`, email asynchrone non-bloquant. |
| 5 | **US-009** | Consultation et suivi de dossier par référence | US-008 | Page `/suivi`, consultation publique par référence `CAN-XXXX`, barre de progression et état des pièces. |

---

## 5. Règles actives pendant cet Epic

*(Ces règles seront relocalisées dans les documents pérennes à la clôture de l'Epic 2)*

- **R1 (Non-bloquage notification) :** L'échec d'envoi d'un email de confirmation ne doit jamais déclencher une exception HTTP 500 ni annuler une transaction de candidature validée.
- **R2 (Contrôle magic bytes) :** Tout fichier reçu sur l'endpoint d'upload doit être validé par ses octets d'en-tête (magic bytes) et limité strictement à 5 Mo.
- **R3 (Mesure déplacement physique) :** Le champ `deplacement_physique` (`boolean`) est obligatoire dans le contrat de soumission de dossier.
- **R4 (Étanchéité des données) :** La consultation de suivi par référence `GET /api/v1/candidatures/{ref}` ne retourne que le statut public du dossier et la liste des documents, sans exposer de données personnelles confidentielles d'autres candidats.

---

*epic-002-refinement.md — FDS Portail · GL-EN3-2026 — status: open*
