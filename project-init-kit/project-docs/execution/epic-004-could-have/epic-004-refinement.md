---
created: 2026-09-29T18:00:00Z
updated: 2026-09-29T18:00:00Z
status: open
---

# epic-004-refinement.md — Could Have & Should Have

> **Ce fichier est la source de vérité des règles en cours pour epic-004.**  
> Cet Epic regroupe les fonctionnalités classées Should Have (SMS) et Could Have (export, mode sombre) du MoSCoW. Il ne démarrera qu'une fois l'Epic 3 ✅ Done.

---

## 1. Scope de l'Epic 4

L'Epic 4 implémente les fonctionnalités de confort et d'efficacité opérationnelle qui ne bloquent pas le parcours principal mais augmentent significativement la valeur du produit :

- **Should Have** : Notifications SMS en complément de l'email
- **Could Have** : Export CSV/PDF des dossiers validés pour les commissions hors ligne
- **Could Have** : Mode sombre pour l'interface admin et le formulaire candidat

**Ce que cet Epic ne couvre PAS :**
- Toute fonctionnalité de candidature ou d'administration (Epics 2 & 3).
- Les transactions monétaires réelles (Won't Have V1).
- L'espace candidat complet ou l'historique multi-campagnes.

---

## 2. Découvertes (Findings)

| ID | Constat | Statut |
|---|---|---|
| E4-1 | Les SMS nécessitent une API tierce (ex : Vonage, Twilio, ou un opérateur haïtien local). Aucune clé n'est disponible en dev — le même pattern port/adaptateur que l'email s'applique (`ISmsProvider` avec `ConsoleSmsSender` en dev). | ✅ Pattern identique à IEmailSender |
| E4-2 | L'export CSV est faisable en Python sans dépendance externe (`csv` stdlib). L'export PDF nécessite `weasyprint` ou `reportlab` — à choisir pendant le refinement de US-015. | ⚠️ Dépendance à arbitrer |
| E4-3 | Le mode sombre est implémentable via une variable CSS `[data-theme="dark"]` sur le `<html>` sans librairie externe, avec persistance dans `localStorage`. | ✅ Autonome |

---

## 3. Découpage des User Stories

| Ordre | Story | Titre | Priorité | Dépend de |
|---|---|---|---|---|
| 1 | **US-015** | Export CSV/PDF filtré des dossiers validés | Could Have | US-012 (Dashboard admin) |
| 2 | **US-016** | Notifications SMS en complément de l'email | Should Have | US-014 (Notification email existante) |
| 3 | **US-017** | Mode sombre interface admin et formulaire candidat | Could Have | Epic 3 terminé |
