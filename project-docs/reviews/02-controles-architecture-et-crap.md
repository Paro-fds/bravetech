---
created: 2026-11-05T16:50:00Z
updated: 2026-11-06T01:57:24Z
---

# 02 — Les contrôles attendus par le cours (ce que nous croyions sur notre architecture frontend et nos tests)

**Contexte :** le 2026-11-05, veille du dépôt, comparaison du document de lancement du Projet 2 (« Les contrôles automatiques attendus ») avec le dépôt. Le cours demande `npx steiger src` et un score CRAP recalculé à la correction. Aucun des deux n'était en place.

## Découvertes

| ID | Ce que nous croyions | Ce qui est vrai | Preuve | Statut |
|---|---|---|---|---|
| F1 | Le frontend respecte Feature-Sliced Design : les dossiers `app/ pages/ features/ entities/ shared/` sont en place, `tsc`, oxlint et la revue des PR passent. | **53 violations.** 46 imports contournent l'API publique d'un segment `shared` (`shared/i18n/useT` au lieu de `shared/i18n`) ; 4 segments `shared` (`api`, `config`, `i18n`, `theme`) n'ont pas d'`index.ts` ; 2 imports croisés entre entités (`dossier-admin` → `session`, `candidature`) ; 1 entité (`contact`) utilisée par une seule page. Avoir les bons dossiers ne dit rien du sens des imports, et aucun outil ne le vérifiait. | Premier lancement de `npx steiger src` (steiger 0.9, `@feature-sliced/steiger-plugin` 0.8, règles `recommended`) : « Found 53 errors ». | ✅ Corrigé : 0 erreur |
| F2 | Le backend est bien testé : 338 tests verts, et chaque story ajoute les siens. | Couverture globale à 95 %, mais le script qui crée le premier compte admin (`backend/scripts/seed_admin.py`, US-011) n'avait **aucun test** : `main` à CRAP 30,00 (complexité 5, couverture 0 %), pile au seuil ; `creer_admin` à 20,00. Ce script ne sert qu'une fois par déploiement, donc personne ne l'exécutait. | `tools/crap.py` sur le rapport de `coverage.py` : maximum 30,00. | ✅ Corrigé : 4 tests, maximum 17,00 (`valider_informations`, complexité 17, couverte à 97,8 %) |
| F3 | « Les contrôles tournent » voulait dire : la CI est verte. | La CI ne lançait ni steiger ni CRAP. Une régression sur l'un ou l'autre serait passée sans bruit, comme les avertissements d'oxlint avant US-025. | Lecture de `.github/workflows/ci.yml`. | ✅ Les deux ajoutés à la CI, avec échec au-dessus du seuil |
| F4 | Le score CRAP couvre « notre code ». | Il ne couvre que le **backend**. Le frontend n'a que 16 tests unitaires, sur des fonctions utilitaires (`node --test`) ; ses composants React ne sont pas mesurés. | Périmètre de `tools/crap.py` (`backend/`, sans les migrations). | ⚠️ Ouvert : à dire dans le rapport (§7) |

## Résolution

| Règle | Destination |
|---|---|
| Définition de fini : steiger sans erreur et aucune fonction au-dessus de 30 en CRAP, vérifiés en CI | `PROJECT_WORKFLOW.md` |
| Un segment `shared` s'importe par son `index.ts` ; une entité n'en importe une autre que par `@x` ; une slice utilisée par une seule page vit dans cette page | `technical-specs/ws-tech-01-portail-public.md §4` |
| Calcul du score (radon × coverage, fonction la plus intérieure) | Docstring de `tools/crap.py` |
