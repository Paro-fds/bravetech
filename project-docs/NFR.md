---
created: 2026-09-25T20:42:00Z
updated: 2026-11-06T03:03:27Z
---

# NFR.md — FDS Portail

**Réponses :** Quelle barre de qualité ce produit doit-il atteindre ?
**Dépend de :** `PRD.md`.

---

## Performance

**1. Temps cassé pour un vrai utilisateur ?**
**3 secondes** sur connexion 3G simulée. Au-delà, un candidat sur réseau intermittent suppose que le site est mort et abandonne. Cette limite s'applique aux pages publiques critiques (accueil, fiche cursus, formulaire, suivi de dossier). Les pages admin n'ont pas de contrainte aussi stricte. Sur mobile, les images (photos, illustrations) restent légères (environ 100 Ko, format WebP, chargement différé) ; les pages de formulaire, de paiement simulé et de suivi n'en contiennent aucune.

**2. Moment de pic de charge connu ?**
Les **14 premiers jours de la période d'inscription** concentrent l'essentiel des candidatures (seuil de validation de l'hypothèse : ≥ 20 dossiers en 14 jours — cf. `PRD.md §11`). La charge reste modeste en volume absolu pour le MVP.

**3. Que mesure-t-on ?**
- **Frontend :** temps de chargement des pages publiques (Web Vitals : LCP, CLS). Aucun outil de mesure n'est branché en production : contrôle ponctuel depuis le navigateur.
- **Backend :** latence des endpoints critiques (`POST /api/v1/candidatures`, `POST /api/v1/candidatures/{id}/documents/{piece}`), lisible dans les journaux du conteneur (`docker compose logs backend` sur la VM).
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
| **Volume des pièces (VM)** | Dépôt refusé avec un message explicite, possibilité de réessayer. Aucun dossier n'est marqué complet sans document réellement stocké. |
| **Resend** | Email non envoyé mais non bloquant — la référence est affichée à l'écran et accessible via la page de suivi. |
| **PostgreSQL (conteneur sur la VM)** | Portail inopérant — aucun fallback en MVP. Priorité : restaurer la dernière copie (`~/sauvegardes/deploiements/`, ws-tech-01 §5.3). |
| **VM Proxmox de la FDS / Apache de l'UEH** | Portail inaccessible. Dépend de l'infrastructure de la Faculté (alimentation, réseau) : risque accepté pour l'hébergement souverain (ADR-006). |

---

## Scalabilité

**1. Que se passe-t-il si l'utilisation augmente de 10× ?**
**Phase MVP :** Scale Up (augmenter la mémoire et les processeurs de la VM Proxmox). L'API FastAPI est stateless — aucun état en mémoire entre les requêtes. **Phase post-MVP :** Scale Out (plusieurs instances FastAPI derrière un Load Balancer) ; nécessite de déplacer les sessions vers Redis.

**2. Quelle ressource s'épuise en premier ?**
Les **connexions PostgreSQL** (pool_size=5, max_overflow=10 — cf. cahier des charges §11.4). Ensuite : le processeur et le disque de la VM sur les dépôts simultanés.

**3. Risque à court terme ?**
**Faible pour le MVP.** Le volume attendu est de 20 à quelques centaines de candidatures. La pression réelle est concentrée sur les premières heures d'ouverture de la période d'inscription.

---

## Sécurité

**1. Donnée la plus sensible ?**
Les **documents personnels des candidats** (diplômes, pièces d'identité), stockés sur le volume des pièces de la VM (ADR-007), et la table `candidats` (nom, prénom, email, référence). Aucun fichier n'a d'adresse publique : le personnel les lit uniquement par le proxy authentifié (`/api/v1/admin/proxy-document/{id}`).

**2. Qui ne doit jamais y accéder ?**
- Un candidat anonyme aux dossiers des autres candidats.
- Toute requête non authentifiée aux routes `/api/v1/admin/`.
- Tout accès direct aux fichiers sans passer par le proxy.

**3. Pire violation — supportable ?**
- Fuite des pièces d'un dossier unique (jeton d'un agent volé) → **supportable** : le jeton expire après 60 minutes.
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
La **Clean Architecture** (4 couches : Domain / Application / Infrastructure / Presentation) garantit que chaque couche change indépendamment. Exemple : remplacer Resend par SendGrid ne touche que `backend/dal/email_adapters.py`, sans modifier la logique métier. Les use cases (`bll/`) sont testables sans base de données active (via mocks).

**2. Documentation synchronisée avec le code ?**
- `cahier_des_charges.md` : référence métier (maintenu manuellement à chaque décision).
- `project-docs/` : référence technique de conception.
- **Pas d'automatisation de sync en MVP** — discipline manuelle par l'équipe.

**3. Suite de tests ?**

| Niveau | Fichier | Ce qu'il couvre |
|---|---|---|
| **Architecture** | `tests/unit/test_architecture.py` | Règle de Dépendance — build rouge si une couche interne importe une couche externe |
| **Unitaire** | `tests/unit/bll/` | Cas d'utilisation sans DB (dépôts factices qui implémentent les ports, ex. `ICandidatureRepository`) |
| **Unitaire** | `tests/unit/entities/` | Règles métier pures (entités Domain) |
| **Intégration** | `tests/integration/` | Routes FastAPI avec base de données de test |

---

## Portabilité

**1. Migration vers un autre hôte sans réécriture ?**
**Oui.** Tout tient dans deux images Docker publiées sur GHCR et un `docker-compose.prod.yml` : changer de machine demande Docker, le fichier `.env` et une copie des volumes (base et pièces). Le frontend Vite produit des fichiers statiques déployables sur n'importe quel serveur web.

**2. Chose codée en dur pour un fournisseur unique ?**
Deux services propriétaires sont isolés derrière des interfaces abstraites et remplaçables sans impact sur la logique métier :
- **Stockage des pièces** → `IStockageFichiers` (`backend/dal/stockage_local.py` ; un adaptateur Cloudinary pourrait s'ajouter, ADR-007)
- **Resend** → `IEmailSender` (`backend/dal/email_adapters.py`)

---

## Observabilité / Surveillance

**1. Alertes immédiates souhaitées ?**
1. 5xx répétés sur `POST /api/v1/candidatures` (formulaire cassé).
2. 5xx répétés sur le dépôt des pièces (`POST /api/v1/candidatures/{id}/documents/{piece}`).
3. Taux d'erreur 401/403 anormalement élevé sur `/api/v1/admin/` (tentative d'intrusion ou JWT expiré en masse).

**2. Ce qui est journalisé vs ce qui devrait l'être ?**
- **Journalisé aujourd'hui :** chaque requête HTTP (méthode, chemin, code de réponse) dans les journaux d'uvicorn et de Nginx sur la VM ; envois d'emails et décisions du personnel par les journaux du backend. `GET /api/v1/sante` répond 200 si la base répond (utilisé par le déploiement).
- **Manquant en MVP :** alertes automatiques (Uptime monitoring), tracing distribué des requêtes multi-services.

**3. Qui surveille ?**
L'équipe Bravetech pendant la période d'inscription. Pas d'on-call défini ni d'escalade automatique en V1.

---

## Récupération après sinistre / Sauvegarde

**1. Pire scénario de perte de données ?**
Perte de la VM (disque, ou volumes Docker effacés) pendant la période d'inscription → base et pièces perdues ensemble, puisqu'elles sont sur la même machine. Une base perdue seule rend les pièces orphelines : les dossiers ne se reconstituent pas sans elle.

**2. Fréquence de sauvegarde / restauration testée ?**
Aujourd'hui, une copie de la base (`pg_dump`) est faite **avant chaque déploiement** et gardée sur la VM (10 dernières, ws-tech-01 §5.3). Elle ne protège pas contre la perte de la VM, et les pièces ne sont pas copiées. **Les sauvegardes quotidiennes hors site, avec une restauration testée, sont l'objet d'US-027, non livrée.**

**3. RPO / RTO acceptables ?**
- **RPO (perte de données max) :** 24h — un jour de candidatures perdues est tolérable ; une semaine ne l'est pas.
- **RTO (temps de retour max) :** 4h — le portail doit revenir opérationnel avant la fin de la journée d'inscription.

---

## Risques et atténuations

| Risque | Impact | Mitigation |
|---|---|---|
| Connexion Internet faible côté candidat | Abandon du formulaire | Interface mobile légère, fichiers ≤ 5 Mo, messages d'erreur clairs |
| Disque de la VM plein ou volume des pièces indisponible | Document non transmis | Message explicite + possibilité de réessayer ; aucun dossier marqué complet sans document |
| Resend indisponible | Candidat non notifié | Non bloquant — référence affichée à l'écran, accessible via page de suivi |
| Perte de la référence par le candidat | Impossibilité de suivre le dossier | Email de confirmation envoyé + affichage clair de la référence après soumission |
| Fichier malveillant uploadé | Corruption ou exploitation | Vérification magic bytes (`filetype`), extension, taille — rejet serveur avant stockage |
| Données personnelles exposées | Risque légal et réputationnel | Auth JWT obligatoire, proxy document admin, secrets hors dépôt Git |
| Pic de candidatures soudain | Saturation du pool PostgreSQL | Index B-Tree, connection pooling configuré, ressources de la VM augmentables |

**Risque le plus difficile à récupérer :** fuite complète de la table `candidats` — irréversible sur le plan réputationnel.

---

## Dépendances

| Service | Rôle | Risque si indisponible | Point de défaillance unique ? |
|---|---|---|---|
| **PostgreSQL (conteneur sur la VM)** | Source de vérité de toutes les données | Portail inopérant | **Oui — en MVP** |
| **Volume des pièces (VM)** | Stockage des fichiers candidats | Dépôt bloqué (réessai possible) | Oui, sur la même machine que la base |
| **Resend** | Notifications email transactionnelles | Emails silencieux (non bloquant) | Non |
| **VM Proxmox de la FDS** | Hébergement de tout le portail (ADR-006) | Portail inopérant | **Oui** |
| **Apache de l'UEH** | TLS (`*.ueh.edu.ht`) et relais vers la VM | Portail inaccessible depuis Internet | Oui (géré par l'UEH) |
| **GitHub (Actions, GHCR)** | Construction et déploiement des versions (ADR-009) | Plus de déploiement ; le portail en ligne continue | Non |

**Si une dépendance change son API :** le stockage et Resend sont isolés derrière des ports (`IStockageFichiers`, `IEmailSender`) — un changement d'API ne touche qu'un seul fichier d'adaptateur. PostgreSQL est accédé via SQLAlchemy ORM — un changement de version nécessite des migrations Alembic.

---

*NFR.md — FDS Portail — Bravetech · GL-EN3-2026*
