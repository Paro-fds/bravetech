---
created: 2026-11-06T04:30:00Z
updated: 2026-11-06T13:53:00Z
---

# Epic 003 Closeout — Administration & Audit

**Workstreams :** WS-04 Administration, WS-05 Notifications
**Status :** ✅ Done — closed 2026-11-06
**Goal :** Le secrétariat traite les dossiers depuis une interface protégée : il consulte, valide ou refuse chaque pièce avec une trace immuable, et le candidat est prévenu.

Frozen record of what this Epic delivered. Full story-by-story detail lives in project-docs/execution/EPIC_EXECUTION.md and each story's own spec file — not duplicated here. Behavior and implementation, consolidated across all 4 stories, are extracted into:
- [`ws-func-04-administration.md`](../../functional-specs/ws-func-04-administration.md) / [`ws-tech-04-administration.md`](../../technical-specs/ws-tech-04-administration.md)
- [`ws-func-05-notifications.md`](../../functional-specs/ws-func-05-notifications.md) / [`ws-tech-05-notifications.md`](../../technical-specs/ws-tech-05-notifications.md)

## Stories Delivered

| Story | Titre | Spec |
|---|---|---|
| US-011 | Authentification de l'administrateur (JWT + RBAC) | [US-011.md](US-011.md) |
| US-012 | Dashboard admin — liste et consultation des candidatures | [US-012.md](US-012.md) |
| US-013 | Validation ou rejet d'un document avec audit | [US-013.md](US-013.md) |
| US-014 | Notification email déclenchée par une décision admin | [US-014.md](US-014.md) |

All 4 stories ✅ Done (validées par le Project Owner le 2026-11-05).

## Decisions & deviations

1. **Une décision est définitive** (US-013) : le critère « un document validé peut être re-rejeté » n'est pas appliqué, à cause du fait critique 5 (`valide_par`, `date_validation` immuables). Une pièce refusée ne redevient décidable qu'après son remplacement par le candidat.
2. **Motif obligatoire pour un refus** (5 à 500 caractères) au lieu de facultatif : le candidat ne peut pas corriger sans lui.
3. **Historique en ajout seul** (`decisions_documents`) en plus des champs d'audit du document, pour garder un refus après remplacement.
4. **Protection posée sur le routeur `/admin` entier**, vérifiée par un test sur le schéma OpenAPI, plutôt qu'endpoint par endpoint.
5. **La liste vit sur `/admin`** et non `/admin/dashboard` (redirection conservée).

## Later additions to WS-04 (other Epics)

Export CSV/PDF (US-015, Epic 4) et calendrier d'admission (US-028, Epic 4) : intégrés aux specs WS-04 ci-dessus.

## Rules moved out of `epic-003-refinement.md`

Le fichier ne contenait pas de section « règles actives » ; ses arbitrages sont partis ainsi :

| Arbitrage | Destination |
|---|---|
| Q1 JWT 60 min sans renouvellement | ws-tech-04 §1 ; `SOLUTION_DESIGN.md` §7 |
| Q2 20 dossiers par page | ws-func-04 §2 ; ws-tech-04 §2 |
| Q3 Rôles `admin` et `agent` | ws-func-04 §1 ; `GLOSSARY.md` (Agent) |
| Q4 Premier compte par script protégé par variables d'environnement | ws-tech-04 §1 ; `SOLUTION_DESIGN.md` §15 |
| E3-5 Limitation de la connexion | ws-tech-04 §1 ; `SOLUTION_DESIGN.md` §7 |

## Split to Unscheduled

None. Not built and not in this Epic: an account-management screen for agents (noted in `SOLUTION_DESIGN.md` §15).

## Tracking

- **Étape 2 (issues) et étape 7 (Milestone) : faites le 2026-11-06**, sur accord explicite du Project Owner (qui, par règle d'équipe, est seul à fermer les issues). Issues #11 à #14 fermées, chacune avec un commentaire renvoyant à la PR qui l'a livrée ; Milestone n°3 fermé, 0 issue ouverte.
- Étape 5 : `SOLUTION_DESIGN.md` §7 (« appelé à chaque endpoint », « 5 requêtes » au lieu de 5 échecs) et §15 (création des comptes admin) corrigés à cette clôture ; `PRD.md` relu, rien de faux pour cet Epic.

---

*epic-003-closeout.md — FDS Portail — Bravetech · GL-EN3-2026*
