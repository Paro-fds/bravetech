---
created: 2026-11-06T04:00:00Z
updated: 2026-11-06T04:11:35Z
---

# Spécification Technique — WS-03 Suivi de dossier

**Réponses :** Comment le suivi public et le remplacement d'une pièce sont-ils construits ?
**Périmètre :** consolidé à la clôture de l'Epic 2 (2026-11-06), d'après US-009, US-010 et US-024. Comportement : [`ws-func-03-suivi.md`](../functional-specs/ws-func-03-suivi.md).

---

## 1. Routes

| Route | Cas d'utilisation | Réponses |
|---|---|---|
| `GET /api/v1/candidatures/{reference}/statut` | `ObtenirStatutCandidatureUseCase` | 200 ; **404 identique** pour une référence inconnue, mal formée ou un UUID de brouillon ; 429 (`limiter_suivi`, compteur `limiteur_suivi`) |
| `POST /api/v1/candidatures/{reference}/pieces/{piece}/remplacement` (multipart : `email`, `fichier`) | `RemplacerDocumentUseCase` | 200 ; **403 identique** pour référence inconnue ou email faux ; 409 pièce non refusée ; 413, 422 ; 429 (`limiteur_identite` après 5 échecs, `limiter_envois`) |

## 2. Réponse publique (`SuiviDossierResponse`)

`reference_dossier`, `prenom`, `initiale_nom`, `soumise_le`, `statut_global` (`en_examen` | `action_requise` | `complet`), `pieces_validees`, `pieces_total`, et par pièce : `id`, `nom`, `statut` (`manquant` | `en_attente` | `valide` | `rejete`), `motif_rejet`, `depose_le`, `valide_le`, `format_accepte`, `taille_max_mo`. **Aucun autre champ du candidat** : un test d'intégration vérifie l'absence de l'email, du téléphone, de la date de naissance, de la commune et du nom de fichier. Le statut global suit la même règle que la liste du personnel (`backend/bll/obtenir_statut_candidature.py`).

## 3. Remplacement

- **Identité** : référence + email de la candidature, comparés côté serveur ; un échec compte dans `limiteur_identite` (5 par minute et par adresse, 429 ensuite même avec le bon email).
- **Upsert** : le document garde son identifiant (`UNIQUE (candidat_id, document_requis_id)`), repasse `en_attente`, perd `motif_rejet`, `valide_par` et `date_validation`. L'historique `decisions_documents` (WS-04) garde le refus.
- **Fichier** : mêmes contrôles que le dépôt (ws-tech-02 §3). Le nouveau fichier est écrit, puis la base, puis l'ancien fichier supprimé. Limite connue : deux remplacements simultanés de la même pièce peuvent laisser un fichier orphelin sur le disque (sans effet sur la base).
- **Email** : accusé « Nouvelle pièce reçue » en tâche de fond, non bloquant (`NotifierRemplacementUseCase`, WS-05).

## 4. Limiteurs et adresse du visiteur

`backend/api/v1/limiteur.py` : compteurs en mémoire du processus (un seul uvicorn en V1 ; un stockage partagé serait nécessaire avec plusieurs processus). `limiteur_suivi` : 20 par minute ; `limiteur_envois` : 10 par minute ; `limiteur_identite` : 5 échecs par minute. L'adresse vient de `X-Forwarded-For` lue depuis la droite selon `TRUSTED_PROXY_COUNT` (ws-tech-01 §5.2) : un en-tête inventé par le visiteur ne contourne pas la limite.

## 5. Frontend

`pages/suivi` : `SuiviPage` (recherche, dossier ; validation du format par `FORMAT_REFERENCE` et `normaliserReference` de `entities/candidature`) et `RemplacerPiecePage`. Dates affichées au jour d'Haïti (`formaterJour`).

---

*ws-tech-03-suivi.md — FDS Portail — Bravetech · GL-EN3-2026*
