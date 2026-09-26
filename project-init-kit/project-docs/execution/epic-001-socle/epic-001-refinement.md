---
created: 2026-09-26T13:09:00Z
updated: 2026-09-26T15:23:00Z
status: closed
---

# epic-001-refinement.md — Socle & Portail public (Historique)

> **Statut : Clos.**  
> Cet Epic a été finalisé et clos le 2026-09-26. Ce fichier conserve l'historique des arbitrages et réflexions initiales.  
> Les spécifications consolidées vivent dans [ws-func-01-portail-public.md](../../functional-specs/ws-func-01-portail-public.md) et [ws-tech-01-portail-public.md](../../technical-specs/ws-tech-01-portail-public.md). Le bilan de clôture vit dans [epic-001-closeout.md](epic-001-closeout.md).

---

## Scope initial

epic-001 livre le socle technique complet + la première page publique réelle (liste et fiche des cursus). La définition de fini de cet Epic : `GET /api/v1/cursus` retourne des données réelles, le frontend affiche au moins deux fiches cursus, `test_architecture.py` passe, et le pipeline CI/CD est vert.

**Ce que cet Epic ne couvre PAS :** formulaire de candidature, upload, auth admin, emails — tout cela est epic-002 ou epic-003.

---

## Découvertes (findings)

| ID | Constat | Statut |
|---|---|---|
| E1-1 | La structure `tests/unit/test_architecture.py` est déjà créée et fonctionnelle — à inclure dans la CI dès le scaffold | ✅ Réalisé et vérifié en CI GitHub Actions |
| E1-2 | Le skill `scaffold-backend-service` est disponible dans `.claude/skills/` — à utiliser pour générer la structure Clean Arch | ✅ Réalisé (couches entities, ports, bll, dal, api/v1) |
| E1-3 | Le skill `scaffold-frontend-app` est disponible — à utiliser pour générer la structure FSD | ✅ Réalisé (React 19 + TypeScript + Vite + Tailwind 4) |
| E1-4 | Les données de cursus doivent être réelles (en base), pas hardcodées | ✅ Réalisé via `cursus_loader.py` lisant les 5 JSON officiels de `cursus/` |

---

## Questions ouvertes & Résolutions finales

| # | Question | Décision / Résolution finale |
|---|---|---|
| Q1 | Git repository déjà créé sur GitHub ? | ✅ Oui — `Paro-fds/bravetech` actif et configuré avec GitHub Projects v2 et GitHub Actions |
| Q2 | Hébergement / Infrastructure cible ? | ✅ Résolu par ADR-006 : conteneurisation Docker / Docker Compose sur VM Linux Proxmox sur site (FDS) |
| Q3 | Seed des données cursus ? | ✅ Résolu : `cursus_loader.py` exploitant les fichiers officiels `cursus/*.json` avec persistance en tables `cursus` et `documents_requis` |
| Q4 | Accès domaine / routage ? | ✅ Résolu : Nginx en reverse proxy Docker (`frontend/nginx.conf`) distribuant la SPA et routant `/api/` vers FastAPI |

---

## Relocalisation des règles d'Epic

Toutes les règles temporaires actives pendant epic-001 ont été transférées vers leurs documents de référence pérennes lors de la clôture :

- **Règle R1 (Protection du seeding)** → Relocalisée dans [ws-tech-01-portail-public.md §4](../../technical-specs/ws-tech-01-portail-public.md#4-règles-architecturales--sécurité-relocalisées-de-epic-001-refinementmd)
- **Règle R2 (Gestion stricte des secrets / `.env`)** → Relocalisée dans [ws-tech-01-portail-public.md §4](../../technical-specs/ws-tech-01-portail-public.md#4-règles-architecturales--sécurité-relocalisées-de-epic-001-refinementmd) et `SOLUTION_DESIGN.md`
- **Règle R3 (Invariant Clean Architecture en CI)** → Relocalisée dans [ws-tech-01-portail-public.md §4](../../technical-specs/ws-tech-01-portail-public.md#4-règles-architecturales--sécurité-relocalisées-de-epic-001-refinementmd) et validée par `tests/unit/test_architecture.py`

---

*epic-001-refinement.md — FDS Portail · GL-EN3-2026 — status: closed*
