---
created: 2026-11-06T04:00:00Z
updated: 2026-11-06T04:11:35Z
---

# Spécification Technique — WS-02 Candidature

**Réponses :** Comment le tunnel de candidature est-il construit ?
**Périmètre :** consolidé à la clôture de l'Epic 2 (2026-11-06), d'après les notes de réalisation d'US-005 à US-008, US-018, et des ajouts ultérieurs. Comportement : [`ws-func-02-candidature.md`](../functional-specs/ws-func-02-candidature.md).

---

## 1. Données

| Table | Contenu | Règle |
|---|---|---|
| `candidats` | Identité, `campagne` (`CAMPAGNE_COURANTE`) | `UNIQUE (email, campagne)` en base |
| `candidatures` | Une par candidat : `deplacement_physique` (`NULL` tant que non répondu), `statut_paiement` (`en_attente`, `SIMULE_PAYE`, `REFUSE`, `ECHOUE`), `methode_paiement`, `reference_paiement`, `numero_paiement`, `statut` (`brouillon` / `soumise`), `reference_dossier`, `soumise_le` | `reference_paiement` et `reference_dossier` uniques |
| `documents_soumis` | Une ligne par (candidat, pièce) | `UNIQUE (candidat_id, document_requis_id)` : remplacer = upsert |

Pièces requises : `backend/entities/pieces_admission.py` (liste unique de 5, extensions et taille par pièce), pas de table. Schéma : migrations Alembic (ws-tech-01 §5.1).

## 2. Routes (`backend/api/v1/candidatures.py`)

| Route | Cas d'utilisation | Erreurs |
|---|---|---|
| `POST /api/v1/candidatures` | `EnregistrerInformationsUseCase` | 422 champs, 409 email déjà utilisé, 403 `candidatures_fermees` |
| `GET /api/v1/candidatures/{id}` | `ObtenirBrouillonUseCase` | 404 |
| `PUT …/{id}/informations` | `MettreAJourInformationsUseCase` | 409 si soumise |
| `PUT …/{id}/deplacement-physique` | `DefinirDeplacementPhysiqueUseCase` | 422 si pas un booléen strict |
| `POST …/{id}/paiement` | `SimulerPaiementUseCase` | 409 étape 2 manquante, **402** `paiement_refuse`, **502** `paiement_echoue` |
| `GET …/{id}/documents`, `POST …/{id}/documents/{piece}` | `ListerPiecesDossierUseCase`, `TeleverserDocumentUseCase` | 409 paiement manquant ou pièce validée, 413, 422, 429 |
| `POST …/{id}/soumission` | `SoumettreCandidatureUseCase` | 409 `{message, manques}`, 403 `candidatures_fermees` |

Le brouillon est identifié par un UUID ; les erreurs métier sont traduites par `_vers_http`, sans détail interne.

## 3. Règles d'implémentation

- **Validation** : `backend/bll/validation_informations.py` (autorité), mêmes règles côté client (`features/candidature-form/lib/validation.ts`). Téléphone stocké `+509XXXXXXXX`.
- **Paiement** (`backend/bll/simuler_paiement.py`) : idempotent (la première référence est gardée) ; issue choisie par la fin du numéro (`FIN_NUMERO_REFUS = "0000"`, `FIN_NUMERO_ECHEC = "9999"`, l'échec n'arrive qu'à la première tentative) ; la tentative est enregistrée avant de lever `PaiementRefuse` / `PaiementEchoue`. Référence `PAY-SIM-AAAA-NNNN` : 4 chiffres tirés au hasard, re-tirage jusqu'à 20 fois.
- **Fichiers** (`backend/bll/validation_fichier.py`) : lecture bornée à 5 Mo + 1 octet, extension autorisée **pour la pièce**, octets d'en-tête par `filetype` qui doivent correspondre à l'extension ; le type MIME annoncé par le navigateur n'est jamais lu ; nom d'origine nettoyé. Stockage par `IStockageFichiers` → `StockageLocal` (`UPLOAD_DIR`, volume `uploads_data`), clé `<candidature>/<piece>-<uuid>.<ext>` générée par le serveur. Écriture en base échouée → fichier supprimé ; remplacement → ancien fichier supprimé après l'enregistrement du nouveau.
- **Soumission** : contrôle de complétude (déplacement, `SIMULE_PAYE`, 5 pièces), référence `CAN-AAAA-NNNN` séquentielle (`max + 1`), collision en base → nouveau numéro (5 essais) ; idempotente (même référence, pas de second email) ; l'email part en `BackgroundTasks` **après** l'enregistrement (WS-05).
- **Période** : la dépendance `exiger_periode_ouverte` est posée sur la création et la soumission (ws-tech-01 §6).
- **Débit** : 10 envois de fichiers par minute et par adresse (`limiteur_envois`, en mémoire du processus) ; adresse du visiteur : ws-tech-01 §5.2.
- **Nginx** : `client_max_body_size 6m` sur `/api/`, sinon tout fichier de plus de 1 Mo est refusé avant l'API.

## 4. Frontend

- `features/candidature-form` : un composant par étape (`StepInformations` … `StepRecapitulatif`, `EcranConfirmation`), `BarreAction` (collée en bas sur mobile, en ligne sur ordinateur), store Zustand **persisté** (`useCandidatureStore` : identifiant du brouillon, saisie, étape).
- `pages/apply/ApplyPage.tsx` : recharge le brouillon au chargement et place le candidat à l'étape que le serveur autorise (`etapeAutorisee`) ; garde-fous qui n'affichent jamais une étape sans ses préalables ; écran « candidatures fermées » d'après `GET /api/v1/calendrier`.
- Envoi des pièces par `XMLHttpRequest` pour suivre la progression.

---

*ws-tech-02-candidature.md — FDS Portail — Bravetech · GL-EN3-2026*
