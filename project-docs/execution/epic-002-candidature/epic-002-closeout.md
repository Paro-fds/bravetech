---
created: 2026-11-06T04:30:00Z
updated: 2026-11-06T04:11:35Z
---

# Epic 002 Closeout — Candidature & Suivi

**Workstreams :** WS-02 Candidature, WS-03 Suivi de dossier (contributions à WS-05 Notifications)
**Status :** ✅ Done — closed 2026-11-06
**Goal :** Un candidat dépose son dossier complet depuis son téléphone, sans se déplacer, et suit son traitement avec sa référence.

Frozen record of what this Epic delivered. Full story-by-story detail lives in project-docs/execution/EPIC_EXECUTION.md and each story's own spec file — not duplicated here. Behavior and implementation, consolidated across all 7 stories, are extracted into:
- [`ws-func-02-candidature.md`](../../functional-specs/ws-func-02-candidature.md) / [`ws-tech-02-candidature.md`](../../technical-specs/ws-tech-02-candidature.md)
- [`ws-func-03-suivi.md`](../../functional-specs/ws-func-03-suivi.md) / [`ws-tech-03-suivi.md`](../../technical-specs/ws-tech-03-suivi.md)

## Stories Delivered

| Story | Titre | Spec |
|---|---|---|
| US-005 | Formulaire d'inscription & question `deplacement_physique` | [US-005.md](US-005.md) |
| US-006 | Simulation de paiement MonCash / NatCash | [US-006.md](US-006.md) |
| US-007 | Téléversement sécurisé des pièces requises | [US-007.md](US-007.md) |
| US-008 | Finalisation de candidature & notification de confirmation | [US-008.md](US-008.md) |
| US-009 | Consultation et suivi de dossier par référence | [US-009.md](US-009.md) |
| US-010 | Remplacement d'un document rejeté depuis la page de suivi | [US-010.md](US-010.md) |
| US-018 | Aligner le portail public sur l'admission unique au MPC | [US-018.md](US-018.md) |

All 7 stories ✅ Done (validées par le Project Owner le 2026-11-05).

## How the Epic changed shape

- **Ajoutée en cours d'Epic : US-018.** Le 2026-10-31, la Faculté a confirmé l'admission unique au MPC : le modèle « une candidature par cursus » était faux (`reviews/01-admission-unique-mpc.md`, ADR-008). US-018 a réaligné le portail public avant US-005.
- **Déplacée depuis l'Epic 3 : US-010** (remplacement d'une pièce). Le refinement la plaçait dans l'Epic 3 (« US-017 ») ; elle a été construite après US-014, car elle dépend d'une pièce refusée par le personnel. Elle est rangée ici, avec le suivi qu'elle prolonge.
- **Rouverte après livraison : US-006.** Le 2026-11-05, la relecture du contrat a montré qu'il manquait le paiement refusé, échoué et relancé (`reviews/03-perimetre-contractuel.md`, F1).
- **Le critère « Dossier soumis → En cours d'examen → Décision finale » d'US-009 a été remplacé** par « pièces validées sur 5 » : le portail ne prononce aucune admission.

## Contribution to WS-05 Notifications

US-008 a posé le mécanisme d'envoi (port `IEmailSender`, Resend ou console, envoi en tâche de fond après l'enregistrement) et l'email de confirmation ; US-010 a ajouté l'accusé de remplacement. Consolidé dans [`ws-func-05-notifications.md`](../../functional-specs/ws-func-05-notifications.md) et [`ws-tech-05-notifications.md`](../../technical-specs/ws-tech-05-notifications.md), écrits à la clôture de l'Epic 3.

## Rules moved out of `epic-002-refinement.md`

| Règle | Destination |
|---|---|
| R1 Email non bloquant | `AGENTS.md` fait critique 2 ; ws-tech-05 §2 |
| R2 Octets d'en-tête, 5 Mo | `AGENTS.md` fait critique 6 ; ws-tech-02 §3 |
| R3 `deplacement_physique` obligatoire | `AGENTS.md` fait critique 3 ; ws-func-02 §1 |
| R4 Le suivi n'expose aucune donnée personnelle | ws-func-03 §2, ws-tech-03 §2 (avec le test qui le vérifie) |
| R5 Admission unique, unicité `(email, campagne)` | ADR-008 ; `AGENTS.md` fait critique 9 ; ws-tech-02 §1 |
| R6 Liste unique de 5 pièces | ADR-008 ; `GLOSSARY.md` ; ws-tech-02 §1 |
| Q1 à Q4 (stockage, email sans clé, référence, contrôle des fichiers) | ADR-007 ; ws-tech-05 §1 ; ws-tech-02 §3 |

## Split to Unscheduled

None.

## Tracking

- **Étape 2 (réconcilier les issues) et étape 7 (fermer le Milestone) : laissées au Project Owner.** La règle de l'équipe est que seul le Project Owner ferme les issues. Au 2026-11-06, les issues #5 à #10 et #18 sont ouvertes alors que leurs stories sont Done. Pour terminer : fermer ces sept issues, puis `gh api -X PATCH repos/Paro-fds/bravetech/milestones/2 -f state=closed`.
- Étape 5 (`PRD.md`, `SOLUTION_DESIGN.md`) : relus le 2026-11-06 (voir `reviews/04-documents-fondateurs-et-adr.md`) ; rien de propre à cet Epic ne restait faux.

---

*epic-002-closeout.md — FDS Portail — Bravetech · GL-EN3-2026*
