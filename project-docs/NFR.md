---
created: 2026-09-25T20:42:00Z
updated: 2026-09-30T16:04:08Z
---

# NFR.md — FDS Portail

**Réponses :** Quelle barre de qualité ce produit doit-il atteindre ?
**Dépend de :** `PRD.md`.

---

## Performance

**1. Temps cassé pour un vrai utilisateur ?**
**3 secondes** sur connexion 3G simulée. Au-delà, un candidat sur réseau intermittent suppose que le site est mort et abandonne. Cette limite s'applique aux pages publiques critiques (accueil, fiche cursus, formulaire, suivi de dossier). Les pages admin n'ont pas de contrainte aussi stricte.

**2. Moment de pic de charge connu ?**
Les **14 premiers jours de la période d'inscription** concentrent l'essentiel des candidatures (seuil de validation de l'hypothèse : ≥ 20 dossiers en 14 jours — cf. `PRD.md §11`). La charge reste modeste en volume absolu pour le MVP.

**3. Que mesure-t-on ?**
- **Frontend :** temps de chargement des pages publiques — mesuré via Vercel Analytics (Web Vitals : LCP, FID, CLS).
- **Backend :** latence des endpoints critiques (`POST /api/candidature`, `POST /api/upload`) — visible dans Railway logs.
- **Non mesuré en MVP :** tracing distribué, alertes automatisées.

---

## Fiabilité / Disponibilité

**1. Que signifie « en panne » ?**
Le formulaire de candidature est inaccessible : un candidat ne peut pas soumettre son dossier. Une panne du tableau de bord admin est secondaire si le formulaire public reste actif.

**2. Temps d'indisponibilité acceptable ?**
Cible : **99 % de disponibilité** hors maintenance annoncée. Une maintenance planifiée est acceptable uniquement en dehors de la période d'inscription. Pendant la période d'inscription : aucune indisponibilité non annoncée tolérée.

**3. Plan si une dépendance tombe ?**

| Dépendance | Plan si indisponible |
|---|---|
| **Cloudinary** | Message explicite à l'utilisateur, possibilité de réessayer. Aucun dossier n'est marqué complet sans document réellement stocké. |
| **Resend** | Email non envoyé mais non bloquant — la référence est affichée à l'écran et accessible via la page de suivi. |
| **Railway (PostgreSQL)** | Portail inopérant — aucun fallback en MVP. Priorité : restaurer depuis le dernier backup Railway. |
| **Vercel** | Frontend inaccessible — SLA Vercel élevé, risque faible. |

---

## Scalabilité

**1. Que se passe-t-il si l'utilisation augmente de 10× ?**
**Phase MVP :** Scale Up (augmenter la puissance de la machine Railway). L'API FastAPI est stateless — aucun état en mémoire entre les requêtes. **Phase post-MVP :** Scale Out (plusieurs instances FastAPI derrière un Load Balancer) ; nécessite de déplacer les sessions vers Redis.

**2. Quelle ressource s'épuise en premier ?**
Les **connexions PostgreSQL** (pool_size=5, max_overflow=10 — cf. cahier des charges §11.4). Ensuite : CPU Railway sur les uploads simultanés.

**3. Risque à court terme ?**
**Faible pour le MVP.** Le volume attendu est de 20 à quelques centaines de candidatures. La pression réelle est concentrée sur les premières heures d'ouverture de la période d'inscription.

---

## Sécurité

**1. Donnée la plus sensible ?**
Les **documents personnels des candidats** (diplômes, pièces d'identité) stockés sur Cloudinary, et la table `candidats` (nom, prénom, email, référence). Les URLs Cloudinary sont signées et accessibles uniquement via le proxy admin authentifié.

**2. Qui ne doit jamais y accéder ?**
- Un candidat anonyme aux dossiers des autres candidats.
- Toute requête non authentifiée aux routes `/api/admin/`.
- Tout accès direct aux URLs Cloudinary sans passer par le proxy.

**3. Pire violation — supportable ?**
- Fuite des URLs Cloudinary signées d'un dossier unique → **supportable** si les URLs sont à durée limitée.
- Fuite complète de la table `candidats` (noms, emails, documents) → **non supportable** — risque légal et réputationnel direct pour la FDS.

Mitigations : JWT HS256 validé à chaque requête, proxy admin, `filetype` (magic bytes), rate limiting, secrets hors dépôt Git (cf. cahier des charges §11.3 — OWASP Top 10).

---

## Utilisabilité / Accessibilité

**1. Qui peut avoir du mal ?**
- Candidats en zone rurale (3G lente, écran 360 px).
- Utilisateurs de lecteurs d'écran (accessibilité visuelle).
- Candidats peu familiers avec les formulaires multi-étapes en ligne.

**2. Niveau minimum d'accessibilité ?**
**WCAG 2.1 niveau AA** — labels explicites sur tous les champs, contraste ≥ 4.5:1, navigation clavier complète sur les formulaires, messages d'erreur indiquant comment corriger (cf. cahier des charges §11.5).

**3. Tâche minimale sans aide ?**
**Soumettre une candidature complète depuis un smartphone Android sans jamais se déplacer physiquement.** C'est le critère de succès central du MVP.

---

## Compatibilité

**1. Environnements supportés ?**
- **Prioritaire :** Android smartphone, Chrome mobile, connexion 3G.
- **Secondaire :** Desktop (Chrome, Firefox), pour les administrateurs FDS.

**2. Environnement explicitement non supporté ?**
Internet Explorer 11. Navigateurs sans JavaScript.

**3. Interopérabilité avec un système existant ?**
Architecturalement préparée, non livrée en V1 :
- **FDS SYS** : System of Record des identités administrateurs (SSO futur).
- **FDS Pay** : paiements réels (aujourd'hui simulés dans FDS Portail).
- **FDS Akademi** : plateforme de cours (hors périmètre).

---

## Conformité / Légal

> ⚠️ **À compléter ultérieurement.**
> Questions ouvertes : réglementation haïtienne applicable aux données personnelles des candidats, consentement explicite requis avant collecte, responsable légal désigné côté FDS-UEH.

---

## Maintenabilité

**1. Facilité de modification ?**
La **Clean Architecture** (4 couches : Domain / Application / Infrastructure / Presentation) garantit que chaque couche change indépendamment. Exemple : remplacer Resend par SendGrid ne touche que `infrastructure/email/resend_adapter.py` sans modifier la logique métier. Les use cases (`bll/`) sont testables sans base de données active (via mocks).

**2. Documentation synchronisée avec le code ?**
- `cahier_des_charges.md` : référence métier (maintenu manuellement à chaque décision).
- `project-docs/` : référence technique de conception.
- **Pas d'automatisation de sync en MVP** — discipline manuelle par l'équipe.

**3. Suite de tests ?**

| Niveau | Fichier | Ce qu'il couvre |
|---|---|---|
| **Architecture** | `tests/unit/test_architecture.py` | Règle de Dépendance — build rouge si une couche interne importe une couche externe |
| **Unitaire** | `tests/unit/bll/` | Use cases sans DB (mocks d'`ICandidatRepository`) |
| **Unitaire** | `tests/unit/entities/` | Règles métier pures (entités Domain) |
| **Intégration** | `tests/integration/` | Routes FastAPI avec base de données de test |

---

## Portabilité

**1. Migration vers un autre hôte sans réécriture ?**
**Oui.** L'API FastAPI est stateless — changer de PaaS (Railway → Fly.io / VPS) requiert uniquement de reconfigurer `DATABASE_URL` et les variables d'environnement. Le frontend Vite produit des artefacts statiques standards déployables sur n'importe quel CDN.

**2. Chose codée en dur pour un fournisseur unique ?**
Deux services propriétaires sont isolés derrière des interfaces abstraites et remplaçables sans impact sur la logique métier :
- **Cloudinary** → `IStorageService` (`infrastructure/storage/cloudinary_adapter.py`)
- **Resend** → `IEmailService` (`infrastructure/email/resend_adapter.py`)

---

## Observabilité / Surveillance

**1. Alertes immédiates souhaitées ?**
1. 5xx répétés sur `POST /api/candidature` (formulaire cassé).
2. 5xx répétés sur `POST /api/upload` (upload bloqué).
3. Taux d'erreur 401/403 anormalement élevé sur `/api/admin/` (tentative d'intrusion ou JWT expiré en masse).

**2. Ce qui est journalisé vs ce qui devrait l'être ?**
- **Journalisé aujourd'hui :** chaque requête HTTP (code de réponse, userId anonymisé) via le middleware Railway. Web Vitals via Vercel Analytics.
- **Manquant en MVP :** alertes automatiques (Uptime monitoring), tracing distribué des requêtes multi-services.

**3. Qui surveille ?**
L'équipe Bravetech pendant la période d'inscription. Pas d'on-call défini ni d'escalade automatique en V1.

---

## Récupération après sinistre / Sauvegarde

**1. Pire scénario de perte de données ?**
Perte de la table `candidats` + `documents_soumis` pendant la période d'inscription → dossiers irrecouvrables. Les fichiers physiques survivent sur Cloudinary (stockage indépendant). La mitigation principale est le backup automatique Railway PostgreSQL.

**2. Fréquence de sauvegarde / restauration testée ?**
Railway PostgreSQL propose des backups automatiques quotidiens selon le plan souscrit. **Aucune procédure de restauration n'a encore été testée (MVP)** — à planifier et documenter avant le lancement de la période d'inscription.

**3. RPO / RTO acceptables ?**
- **RPO (perte de données max) :** 24h — un jour de candidatures perdues est tolérable ; une semaine ne l'est pas.
- **RTO (temps de retour max) :** 4h — le portail doit revenir opérationnel avant la fin de la journée d'inscription.

---

## Risques et atténuations

| Risque | Impact | Mitigation |
|---|---|---|
| Connexion Internet faible côté candidat | Abandon du formulaire | Interface mobile légère, fichiers ≤ 5 Mo, messages d'erreur clairs |
| Cloudinary indisponible pendant un upload | Document non transmis | Message explicite + possibilité de réessayer ; aucun dossier marqué complet sans document |
| Resend indisponible | Candidat non notifié | Non bloquant — référence affichée à l'écran, accessible via page de suivi |
| Perte de la référence par le candidat | Impossibilité de suivre le dossier | Email de confirmation envoyé + affichage clair de la référence après soumission |
| Fichier malveillant uploadé | Corruption ou exploitation | Vérification magic bytes (`filetype`), extension, taille — rejet serveur avant stockage |
| Données personnelles exposées | Risque légal et réputationnel | Auth JWT obligatoire, proxy document admin, secrets hors dépôt Git |
| Pic de candidatures soudain | Saturation du pool PostgreSQL | Index B-Tree, connection pooling configuré, scale up Railway possible |

**Risque le plus difficile à récupérer :** fuite complète de la table `candidats` — irréversible sur le plan réputationnel.

---

## Dépendances

| Service | Rôle | Risque si indisponible | Point de défaillance unique ? |
|---|---|---|---|
| **PostgreSQL (Railway)** | Source de vérité de toutes les données | Portail inopérant | **Oui — en MVP** |
| **Cloudinary** | Stockage des fichiers candidats | Upload bloqué (réessai possible) | Non |
| **Resend** | Notifications email transactionnelles | Emails silencieux (non bloquant) | Non |
| **Vercel** | CDN et hébergement frontend | Interface inaccessible | Oui (SLA élevé, risque faible) |
| **Railway** | Hébergement backend + BDD | Portail inopérant | Oui |

**Si une dépendance change son API :** Cloudinary et Resend sont isolés derrière des interfaces (`IStorageService`, `IEmailService`) — un changement d'API ne touche qu'un seul fichier d'adapter. PostgreSQL est accédé via SQLAlchemy ORM — un changement de version nécessite des migrations Alembic.

---

*NFR.md — FDS Portail — Bravetech · GL-EN3-2026*
