---
created: 2026-09-24T20:42:00Z
updated: 2026-09-30T16:04:08Z
---

# PRD.md — FDS Portail

**Réponses :** Qu'est-ce que nous construisons, pour qui, et pourquoi ?
**Dépend de :** rien — c'est le premier document à remplir.

---

## 1. Énoncé du produit

**FDS Portail** est la vitrine publique officielle de la Faculté des Sciences (FDS-UEH) et la plateforme dématérialisée d'inscription. Il permet à un candidat à l'admission de s'informer sur les cursus, de soumettre son dossier et de suivre son traitement intégralement en ligne depuis son smartphone.

Il existe parce que les informations sur les cursus circulent via des canaux informels (WhatsApp, bouche-à-oreille), et qu'un candidat hors de Port-au-Prince doit aujourd'hui obligatoirement se déplacer physiquement pour obtenir une information fiable ou déposer une candidature — créant une inégalité d'accès structurelle.

## 2. Public

**Candidat (public principal)** — lycéen, souvent hors de Port-au-Prince, smartphone Android, connexion 3G intermittente. Son accès est entièrement public : aucun compte requis pour postuler ou suivre son dossier (il utilise sa référence dossier).

**Administrateur FDS (public secondaire)** — agent du secrétariat qui traite les dossiers reçus. Son accès est authentifié (email + mot de passe, JWT). Il a priorité sur le candidat en cas de conflit de besoin (ex. traçabilité vs simplicité).

## 3. Scénario idéal de bout en bout

1. Louismy ouvre le portail sur son Android et consulte la fiche du cursus Génie Informatique (dates, prérequis, pièces requises).
2. Il clique « Postuler », saisit ses informations personnelles et répond à la question sur le déplacement physique.
3. Il simule le paiement des frais (MonCash/NatCash) — une référence transactionnelle est générée.
4. Il uploade ses pièces justificatives (PDF/JPG, max 5 Mo chacune).
5. Le système génère la référence `CAN-2026-0089` et lui envoie un email de confirmation avec un lien de suivi.
6. Louismy suit son dossier via sa référence : une barre de progression indique l'état de chaque document.
7. L'administrateur valide ou rejette un document — Louismy reçoit immédiatement un email.
8. Si un document est rejeté, Louismy le remplace depuis la page de suivi sans se déplacer.

**Ce qui doit être vrai à chaque étape :**
- Étape 1 : le portail est accessible en 3G, les fiches cursus sont à jour et lisibles sur mobile
- Étapes 2-4 : le formulaire fonctionne en plusieurs étapes sans perte de données si la connexion est coupée entre deux
- Étape 5 : l'email est envoyé de manière non bloquante — si il échoue, la référence est quand même affichée à l'écran
- Étape 6 : la barre de progression reflète l'état réel de la base, pas un état calculé côté client
- Étapes 7-8 : l'admin est authentifié, chaque décision est auditée, et le candidat peut remplacer sans créer un doublon

**Où ça se casse aujourd'hui :** à l'étape 1 (aucune source officielle fiable en ligne) et à l'étape 4 (dépôt papier uniquement, impossible à distance).

## 4. Tâches à accomplir

| Tâche | Sans le portail aujourd'hui |
|---|---|
| S'informer sur les cursus et prérequis | Chercher sur Google → site obsolète → déplacement physique pour obtenir une brochure photocopiée avec corrections à la main |
| Déposer une candidature | Déplacement physique obligatoire + remplissage de formulaire papier |
| Suivre l'avancement de son dossier | Rappeler la faculté (souvent sans réponse) ou se déplacer à nouveau |
| Remplacer un document rejeté | Nouveau déplacement physique |

La tâche critique : **le dépôt de candidature**. Si elle reste non résolue, tout le reste du produit est inutile.

## 5. Expérience produit en couches

Deux niveaux d'accès, distincts par nature de confiance :

- **Candidat (public)** — aucun compte, accès par référence dossier. Peut consulter les cursus, postuler, suivre son dossier, remplacer un document rejeté.
- **Administrateur FDS (authentifié)** — JWT, rôle `admin` ou `agent`. Peut consulter toutes les candidatures, valider/rejeter des documents.

La frontière est de **sécurité** : un candidat ne doit jamais voir le dossier d'un autre.

## 6. Ce que le produit peut faire

| Capacité | Déclencheur | Résultat réel |
|---|---|---|
| **Consulter les fiches cursus** | Candidat clique sur un cursus depuis l'accueil | Page affichant description, dates clés et liste des pièces requises |
| **Postuler** | Candidat clique « Postuler » et complète le formulaire en 3 étapes | Dossier créé en base, référence `CAN-2026-X` générée, email de confirmation envoyé |
| **Simuler le paiement** | Candidat confirme la simulation MonCash/NatCash | `statut_paiement` et `reference_paiement` enregistrés, accès à l'étape upload débloqué |
| **Uploader une pièce** | Candidat attache un fichier PDF/JPG ≤ 5 Mo | Fichier stocké sur Cloudinary, `DocumentSoumis` créé avec statut `en_attente` |
| **Suivre son dossier** | Candidat saisit sa référence sur la page de suivi | Barre de progression affichant le statut de chaque document |
| **Remplacer un document rejeté** | Candidat uploade un nouveau fichier sur un document `rejete` | Même `DocumentSoumis` mis à jour (upsert), statut repassé à `en_attente` |
| **Valider / rejeter un document** | Admin clique Valider ou Rejeter dans le tableau de bord | Statut mis à jour en base, audit enregistré (`valide_par`, `date_validation`), email déclenché |
| **Consulter les candidatures** | Admin ouvre le tableau de bord | Liste paginée des dossiers avec statuts et indicateur `deplacement_physique` |

**Capacité supposée présente mais explicitement hors périmètre V1 :** le paiement réel (MonCash/NatCash). Un candidat qui s'attendrait à payer directement depuis le portail sera redirigé vers une simulation — l'argent réel est délégué à FDS Pay.

## 7. Ce que le produit ne doit jamais faire

- Exposer le dossier d'un candidat à un autre candidat (même par URL directe)
- Accepter un fichier exécutable déguisé en PDF/JPG
- Laisser un échec d'email annuler une candidature valide (l'email est une notification, pas la source de vérité)
- Révéler des détails internes (stack trace, schéma BDD) dans les réponses d'erreur

**Pire cas d'abus plausible et réponse du système :**
- *Un acteur forge un JWT pour accéder aux dossiers admin* → signature HS256 validée à chaque requête via `get_current_admin()` ; toute requête non valide retourne 401/403 sans détail interne
- *Un candidat tente d'accéder au dossier d'un autre via sa référence* → seul le statut public est retourné par référence, aucune donnée personnelle de tiers n'est exposée
- *Upload massif de fichiers pour épuiser le stockage* → rate limiting sur `POST /api/upload` (10 req/60s par IP) + limite de taille serveur (5 Mo)
- *Upload d'un exécutable renommé en PDF* → vérification des magic bytes côté serveur via `filetype` avant tout enregistrement

## 8. Voix et persona

*Non applicable.* Le portail ne génère pas de contenu conversationnel propre. Les emails transactionnels (confirmation, validation, rejet) sont fonctionnels et factuels.

## 9. Modèle d'accès

**Candidat** : aucune inscription requise. L'accès au suivi de dossier se fait par référence unique (`CAN-2026-X`). Aucune révocation.

**Administrateur** : compte créé par la FDS (FDS SYS est le System of Record des identités internes — FDS Portail consomme cette donnée). Authentification email + mot de passe hashé bcrypt → JWT HS256 (durée 60 min). Révocation possible par suppression du compte. Toute action admin est auditée (`valide_par`, `date_validation`).

## 10. Observabilité

Première question après mise en ligne : **combien de candidatures ont été soumises, et quel pourcentage sans déplacement physique ?**

Surveillance à risque : indisponibilité pendant la période d'inscription, taux d'abandon du formulaire > 30 %, taux de rejet de documents > 20 %.

Consulté par : l'équipe produit et le secrétariat FDS, pendant la période d'inscription.

## 11. Critères de succès

- ≥ 20 candidatures soumises en ligne dans les 14 premiers jours
- ≥ 70 % des candidats répondent « Non » à la question de déplacement physique
- ≤ 30 % d'abandon du formulaire
- ≥ 80 % des documents rejetés remplacés en ligne sans déplacement

La plus petite version valide : **un candidat soumet un dossier complet et reçoit sa référence sans avoir à se déplacer**.

## 12. Critères d'échec / blocages avant mise en ligne

- Un document candidat est accessible sans authentification admin → **bloquant**
- Le formulaire est inutilisable sur mobile 360 px → **bloquant**
- Une candidature est perdue si l'email échoue → **bloquant**
- Les fichiers exécutables sont acceptés à l'upload → **bloquant**

**Différence entre « pas parfait » et « réellement bloquant » :** un mode sombre absent, une barre de progression imparfaite, ou une notification SMS manquante sont des imperfections — le portail reste utilisable. Ce qui est bloquant, c'est ce qui empêche un candidat de soumettre son dossier ou expose des données personnelles. Les quatre critères ci-dessus sont non négociables ; tout le reste est une amélioration.

## 13. Hors périmètre — V1

| Élément exclu | Pourquoi pas en V1 | Supposé inclus par un lecteur novice ? |
|---|---|---|
| Transactions monétaires réelles | Déléguées à FDS Pay (module séparé) | **Oui** — un candidat pourrait supposer qu'il paye vraiment |
| Espace étudiant complet (compte, historique) | Le suivi par référence suffit pour le MVP ; un compte complet est post-MVP | Non |
| Plateforme de cours (FDS Akademi) | Module séparé, hors périmètre Bravetech | Non |
| SSO institutionnel complet (FDS SYS) | Architecturalement préparé, pas livré en V1 | Non |
| Notifications SMS | Should Have — prévu mais non bloquant pour le MVP | Non |
| Export CSV/PDF des dossiers | Could Have — utile pour les commissions, pas critique pour le lancement | Non |
| Mode sombre | Could Have — confort, pas accessibilité de base | Non |

## 14. Documents associés

Voir `NFR.md`, `SOLUTION_DESIGN.md`, `PLAN.md`, `GLOSSARY.md`, `project-docs/execution/`, `project-docs/PROJECT_WORKFLOW.md`, `AGENTS.md`.

---

*PRD.md — FDS Portail — Bravetech · GL-EN3-2026*
