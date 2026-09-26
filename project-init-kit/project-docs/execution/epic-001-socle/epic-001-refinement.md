---
created: 2026-09-26T13:09:00Z
updated: 2026-09-26T13:09:00Z
status: open
---

# epic-001-refinement.md — Socle & Portail public

> **Ce fichier est la source de vérité des règles en cours pour epic-001.**
> Toute règle produite pendant cet Epic vit ici jusqu'à la clôture.
> À la clôture : chaque règle est déplacée dans le document propriétaire, et ce fichier devient l'historique de l'Epic.

---

## Scope

epic-001 livre le socle technique complet + la première page publique réelle (liste et fiche des cursus). La définition de fini de cet Epic : `GET /api/v1/cursus` retourne des données réelles, le frontend affiche au moins deux fiches cursus, `test_architecture.py` passe, et le pipeline CI/CD est vert.

**Ce que cet Epic ne couvre PAS :** formulaire de candidature, upload, auth admin, emails — tout cela est epic-002 ou epic-003.

---

## Découvertes (findings)

| ID | Constat | Statut |
|---|---|---|
| E1-1 | La structure `tests/unit/test_architecture.py` est déjà créée et fonctionnelle — à inclure dans la CI dès le scaffold | ✅ Confirmé |
| E1-2 | Le skill `scaffold-backend-service` est disponible dans `.claude/skills/` — à utiliser pour générer la structure Clean Arch | ✅ À utiliser |
| E1-3 | Le skill `scaffold-frontend-app` est disponible — à utiliser pour générer la structure FSD | ✅ À utiliser |
| E1-4 | Les données de cursus doivent être réelles (en base), pas hardcodées | ✅ Confirmé — table `documents_requis` et données initiales via seed |

---

## Questions ouvertes

| # | Question | Recommandation | Résolu ? |
|---|---|---|---|
| Q1 | Git repository déjà créé sur GitHub ? | — | ✅ Oui — repo existant |
| Q2 | Plan Railway choisi (Starter / Pro) ? | Starter suffit pour le MVP | ⏳ Reporté — déploiement hors scope immédiat |
| Q3 | Seed des données cursus : fichier SQL ou script Python ? | Script Python (`seed_db.py`) aligné sur la stack SQLAlchemy | ⏳ À confirmer au moment de US-001 |
| Q4 | Domaine custom sur Vercel ou `*.vercel.app` suffit pour le MVP ? | `*.vercel.app` suffit — domaine custom avant lancement public | ⏳ Reporté — déploiement hors scope immédiat |

---

## Stories — ordre de build

Le déploiement Railway + Vercel (US-004) est **reporté** — on livre d'abord le contenu en local avec CI locale. US-004 sera repris avant la fin de l'Epic pour valider le déploiement.

| Ordre | Story | Dépend de | Raison |
|---|---|---|---|
| 1 | **US-003** — Tests d'architecture en CI locale | — | Valider la structure avant d'écrire le moindre code métier |
| 2 | **US-001** — Liste des cursus (backend + frontend) | US-003 | Endpoint + page réelle, CI locale verte |
| 3 | **US-002** — Fiche détaillée d'un cursus | US-001 | S'appuie sur `/api/v1/cursus/:id` issu de US-001 |
| 4 | **US-004** — Déploiement Railway + Vercel | US-001, US-002 | Reporté — à faire après que le contenu est stable |

> **Note :** les IDs sont permanents. L'ordre d'exécution est 3 → 1 → 2 → 4.

---

## Règles actives pendant cet Epic

*(Ces règles se déplacent dans le document propriétaire à la clôture de l'Epic)*

- **R1 :** Le seed de données ne doit jamais s'exécuter en production — protégé par `if settings.ENV == "development"`.
- **R2 :** Toute variable d'environnement sensible (`DATABASE_URL`, `SECRET_KEY`) est dans `.env` (jamais commitée) et dans Railway/Vercel dashboard. Vérifier `.gitignore` avant le premier push.
- **R3 :** `test_architecture.py` doit passer même sur un projet vide — si le test échoue à vide, c'est une erreur de configuration, pas de code.

---

*epic-001-refinement.md — FDS Portail · GL-EN3-2026 — status: open*

---

## Règles actives pendant cet Epic

*(Ces règles se déplacent dans le document propriétaire à la clôture de l'Epic)*

- **R1 :** Le seed de données ne doit jamais s'exécuter en production — protégé par `if settings.ENV == "development"`.
- **R2 :** Toute variable d'environnement sensible (`DATABASE_URL`, `SECRET_KEY`) est dans `.env` (jamais commitée) et dans Railway/Vercel dashboard. Vérifier `.gitignore` avant le premier push.
- **R3 :** `test_architecture.py` doit passer même sur un projet vide (0 fichiers dans `entities/`, `bll/`, `dal/`, `api/`) — si le test échoue à vide, c'est une erreur de configuration, pas de code.

---

*epic-001-refinement.md — FDS Portail · GL-EN3-2026 — status: open*
