# Cahier des Charges - FDS Portail

> **Note d'Ingénierie :** Ce document est structuré selon la méthodologie d'Analyse et Conception. Chaque section découle logiquement de la précédente (du Problème jusqu'à l'Architecture), garantissant la cohérence absolue de la solution technique ("Start from Complexity and craft Certainty").

---

## §1. Le problème

La Faculté des Sciences (FDS) de l'UEH forme l'élite de l'ingénierie en Haïti. Pourtant, elle fait face à une complexité majeure dans sa relation avec les futurs étudiants :
- **Déficit d'information :** Les informations sur les cursus, les prérequis et les dates circulent via des canaux informels (WhatsApp, bouche-à-oreille). Il n'y a pas de source de vérité officielle accessible sur mobile.
- **Friction géographique :** Un candidat résidant hors de Port-au-Prince (ex: Gonaïves, Jacmel) doit obligatoirement se déplacer physiquement pour obtenir une information fiable ou déposer une fiche papier.
- **Opérations manuelles :** Le secrétariat gère des piles de dossiers physiques, générant un manque de traçabilité et une impossibilité pour le candidat de suivre l'avancement de son dossier.

## §2. La solution

Le **FDS Portail (Module 2)** est la réponse technologique à cette complexité. Il s'agit de la vitrine publique officielle de la FDS et de la plateforme dématérialisée d'inscription. La solution transforme le chaos informationnel en "Certitude" pour le candidat, qui peut désormais s'informer, postuler et suivre son dossier intégralement en ligne depuis son smartphone.

---

## §3. Argumentation (Customer Journey & Hypothèse)

### 3.1 Le persona

**Louismy, 17 ans**, élève en Terminale à Pétion-Ville. Il possède un smartphone Android avec une connexion 3G intermittente. Il souhaite s’inscrire en génie informatique à la FDS, mais ne trouve pas facilement d’informations officielles sur les dates, les modalités d’admission et les prérequis.

---

### 3.2 L'interview

Afin de valider la réalité du terrain, une interview a été menée auprès d’un profil correspondant au persona principal. La consigne d’ouverture était :

*« Racontez-moi ce que vous avez fait pour trouver des informations sur la FDS et comprendre comment postuler, depuis le moment où vous avez décidé de vous y intéresser jusqu’au moment où vous avez soumis votre candidature ou abandonné l’idée. »*

#### Q1. Première recherche

**Question :** *« Lorsque vous avez décidé de vous renseigner sur la FDS pour vous inscrire, qu’avez-vous fait en premier ? »*

> « J’ai cherché sur Google. J’ai tapé “FDS Haïti”. J’ai trouvé un ancien site web avec les cursus, mais les informations semblaient peu à jour et le site était difficile à naviguer. Le formulaire de contact ne fonctionnait pas et je n’avais pas de numéro de téléphone direct. »

#### Q2. Recherche d’alternative

**Question :** *« Qu’avez-vous fait ensuite ? »*

> « J’ai cherché à nouveau en tapant “FDS Haïti adresse”. J’ai trouvé l’adresse de la faculté avec un numéro de téléphone. J’ai appelé, mais je n’ai obtenu aucune réponse. J’ai donc compris qu’il fallait me rendre sur place. Je m’y suis rendu deux jours plus tard. »

#### Q3. Déplacement à la faculté

**Question :** *« Comment s’est passé votre déplacement à la FDS ? Qu’avez-vous ressenti ? »*

> « Aujourd’hui, chaque déplacement comporte une certaine appréhension à cause du contexte sécuritaire. Heureusement, la FDS étant actuellement située à Delmas 33, cela restait relativement accessible pour moi qui habite à Pétion-Ville. Mais j’imagine difficilement la situation des candidats venant de province. Je me demandais aussi comment une école d’ingénieurs aussi reconnue pouvait ne pas disposer d’un site moderne permettant de s’informer et de s’inscrire en ligne. »

#### Q4. Recherche d’informations sur place

**Question :** *« Une fois sur place, comment avez-vous obtenu les informations nécessaires ? »*

> « Je me suis d’abord renseigné auprès d’étudiants qui m’ont orienté vers le secrétariat. On m’a remis une brochure photocopiée avec des corrections écrites à la main. J’ai enfin obtenu des informations concrètes sur les modalités d’inscription et les matières enseignées. Cependant, le calendrier n’était pas encore disponible et l’on m’a demandé de revenir dans deux semaines ou de rappeler plus tard. »

#### Q5. Dépôt de candidature

**Question :** *« Avez-vous finalement pu vous inscrire ? Comment cela s’est-il passé ? »*

> « Oui. Je suis revenu quelques semaines plus tard pour remplir un formulaire papier. On m’a confirmé mon admissibilité, remis un numéro d’inscription et communiqué la date du concours. Il ne me restait plus qu’à attendre. »

#### Q6. Suggestions d’amélioration

**Question :** *« Qu’est-ce qui devrait changer pour améliorer cette expérience ? »*

> « Il faudrait déjà un site web à jour avec les informations sur les cursus, les prérequis, les dates et les frais. Ensuite, la possibilité de postuler en ligne permettrait d’économiser du temps et d’éviter un déplacement. »

#### Verbatims clés retenus pour justifier le MVP

> *« J’ai trouvé un ancien site web avec les cursus, mais les informations semblaient peu à jour et le site était difficile à naviguer. »*

> *« Je me demandais comment une école d’ingénieurs de renom pouvait ne pas disposer d’un site moderne avec la possibilité de faire des inscriptions en ligne. »*

---

### 3.3 Le Customer Journey

L'expérience actuelle d'un candidat est modélisée par la carte d'expérience utilisateur (Customer Journey Map) suivante :

![Customer Journey Map](livrables/figures/customer_journey_map.png)

*Figure 1 : Carte d'expérience utilisateur (Customer Journey Map) montrant la dépendance critique aux déplacements physiques et les opportunités de numérisation.*

À partir des interviews réalisées, le parcours utilisateur actuel d’un candidat à la FDS peut également être détaillé sous forme de tableau :

| Étape | Actions du candidat | Ressenti (Émotions) | Difficultés (Pain Points) | Opportunités pour le MVP | Moments de vérité |
|---|---|---|---|---|---|
| **1. Recherche d’informations** | Louismy recherche « FDS Haïti » sur Google | Perte de temps, doute | Informations dispersées, ancien site non mis à jour | **Créer un portail officiel centralisé** avec SEO optimisé | |
| **2. Tentative de contact** | Il cherche un numéro et tente d’appeler | Frustration | Absence de canal de communication fiable | **Afficher clairement les contacts** et une FAQ | |
| **3. Déplacement physique** | Il se rend à Delmas 33 | Stress, appréhension | Déplacement coûteux en temps, risques sécuritaires | **Permettre la candidature 100% en ligne** | 🚨 *Point de rupture potentiel (abandon)* |
| **4. Sur place** | Il interroge des étudiants puis le secrétariat | Soulagement temporaire | Informations papier peu professionnelles | **Digitaliser les fiches de cursus** | |
| **5. Attente administrative** | Il doit revenir plus tard pour le calendrier | Agacement | Absence de calendrier clair et accessible | **Publier les dates clés** gérées par CMS | |
| **6. Dépôt de candidature** | Il remplit un formulaire papier | Résignation | Procédure lente et manuelle | **Formulaire d'upload de documents** (Mobile-First) | 🎯 *Moment de vérité décisif (conversion)* |
| **7. Confirmation** | Il reçoit un numéro d’inscription | Soulagement | Aucun suivi numérique du dossier | **Génération de référence et suivi en ligne** | |

#### Principal problème identifié

Le principal problème observé est une **forte dépendance au déplacement physique**, causée par un **déficit d’information numérique fiable et centralisée**. Cette situation crée une inégalité d’accès, particulièrement pour les candidats vivant hors de Port-au-Prince.

---

### 3.4 L'hypothèse

| Élément                                 | Formulation                                                                                                                                                                      |
| --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Nous croyons que**                    | les lycéens, notamment ceux vivant hors de Port-au-Prince, rencontrent des difficultés importantes pour obtenir des informations fiables et soumettre leur candidature à la FDS. |
| **Ils ont besoin de**                   | consulter des informations officielles et postuler entièrement en ligne depuis un smartphone.                                                                                    |
| **Afin de**                             | réduire les déplacements physiques, économiser du temps et améliorer l’accès aux études d’ingénierie.                                                                            |
| **Nous saurons que cela fonctionne si** | au moins **20 candidatures** sont soumises en ligne durant les deux premières semaines et que **70 % des candidats** complètent le processus sans déplacement physique.          |

**Plan de mesure de l'hypothèse :**

| Indicateur | Méthode de collecte | Seuil de validation |
|---|---|---|
| Nombre de candidatures soumises | Comptage des dossiers créés en base (`candidats.reference_dossier`) | ≥ 20 dossiers en 14 jours |
| Taux de complétion sans déplacement | Question obligatoire en fin de formulaire, persistée en base : `candidats.deplacement_physique` (`false` = Non, `true` = Oui). Calcul : `COUNT(*) WHERE deplacement_physique = false / COUNT(*) WHERE deplacement_physique IS NOT NULL` | ≥ 70 % répondent "Non" (`deplacement_physique = false`) |
| Taux d'abandon du formulaire | Comparaison entre candidats ayant commencé le formulaire et dossiers soumis | ≤ 30 % d'abandon |
| Temps moyen de soumission | Horodatage début/fin du parcours de candidature | ≤ 20 minutes sur mobile |
| Taux de documents rejetés puis remplacés | Suivi des documents passés de `rejete` à `en_attente` après remplacement | ≥ 80 % des rejets corrigés en ligne |

Ces métriques permettent d'éviter une validation subjective du MVP : le succès n'est pas seulement "le site fonctionne", mais "le site réduit effectivement la dépendance au déplacement physique".

### 3.5 Le JTBD

Le "Job to be Done" résume la motivation profonde du persona lorsqu'il interagit avec le système :

> **« Quand je** dois m'inscrire à l'université depuis ma province sans information claire, **je veux** pouvoir m'informer, soumettre mon dossier et payer virtuellement les frais entièrement en ligne **afin de** sécuriser ma candidature à la FDS sans perdre de temps ni risquer ma sécurité dans un déplacement physique. **»**

---

## §4. Priorisation MoSCoW

### 🟢 Must Have (Requis pour le MVP)
- Pages de présentation des cursus (Informatique, Physique, etc.) et dates clés.
- Formulaire de candidature en ligne avec upload de pièces justificatives (PDF/JPG).
- Génération d'un numéro de référence de dossier (ex: `CAN-2026-X`).
- Suivi du dossier (tracking) en ligne par le candidat via sa référence.
- Interface sécurisée pour l'administration (changer le statut d'un document).
- **Notifications automatiques par email** au candidat :
  - Confirmation de réception après soumission (avec la référence `CAN-2026-X`).
  - Notification de validation d'un document par l'administration.
  - Notification de rejet d'un document (avec lien pour le remplacer).
- Possibilité pour le candidat de **remplacer un document rejeté** depuis la page de suivi.
- **Simulation du paiement des frais** (MonCash / NatCash) avec génération d'une référence transactionnelle pour préparer l'interconnexion future avec le module FDS Pay.
- **Mesure de l'hypothèse §3.4 :** question obligatoire « Avez-vous dû vous déplacer pour compléter cette candidature ? », enregistrée en `candidats.deplacement_physique` et consultable côté admin.

### 🟡 Should Have (Important)
- Notifications push (SMS) en complément de l'email.

### 🔴 Won't Have (Hors Scope Phase 1)
- Transactions monétaires réelles (L'argent réel est délégué au Module FDS Pay, seule l'UX et la persistance de simulation sont dans ce MVP).
- Plateforme de cours (déléguée à FDS Akademi).

---

### 4.1 Exigences non fonctionnelles du MVP

| Qualité attendue | Exigence mesurable | Justification métier |
|---|---|---|
| **Mobile-first** | Toutes les pages critiques doivent être utilisables sur écran 360 px de large | Le persona utilise principalement un smartphone Android |
| **Performance 3G** | Les pages publiques essentielles doivent charger en moins de 3 secondes sur connexion lente simulée | L'accès réseau est intermittent pour une partie des candidats |
| **Disponibilité** | Le portail doit rester accessible pendant la période d'inscription, avec une cible de 99 % hors maintenance annoncée | Une indisponibilité bloque directement les candidatures |
| **Accessibilité** | Les formulaires doivent respecter les principes WCAG 2.1 AA : labels, contraste, navigation clavier, messages d'erreur explicites | Le service est public et doit rester inclusif |
| **Sécurité des fichiers** | Aucun fichier > 5 Mo ni format hors PDF/JPG/JPEG ne doit être accepté côté serveur | Les documents contiennent des données personnelles |
| **Traçabilité** | Toute validation/rejet admin doit enregistrer l'administrateur, la date et le nouveau statut | Le secrétariat doit pouvoir justifier les décisions |
| **Résilience email** | Une erreur d'envoi email ne doit pas annuler la candidature ou la validation du document | L'email est une notification, pas la source de vérité |

---

## §5. Walking Skeleton

### Le Walking Skeleton (Le parcours minimal de bout en bout)
> Louismy ouvre le portail FDS sur son téléphone Android. Il consulte la page du cursus Ingénierie. Il clique sur "Postuler" et remplit ses informations personnelles (nom, prénom, email). **Il est ensuite redirigé vers une interface simulant le paiement des frais de dossier (MonCash/NatCash). Une fois le paiement virtuel validé, il accède à l'étape finale où il uploade une photo de son diplôme du baccalauréat et soumet sa candidature.** Le système lui affiche immédiatement son numéro de référence `CAN-2026-0089` **et lui envoie un email de confirmation** contenant ce même numéro et un lien vers la page de suivi. Plus tard, Louismy saisit cette référence dans l'espace de suivi et voit une **barre de progression** indiquant que son dossier est reçu et **"en attente de validation"**. L'administration voit le dossier apparaître dans son tableau de bord, valide ou rejette un document — **Louismy reçoit immédiatement un email** lui indiquant le statut. Si un document est rejeté, la progression affiche **"Correction requise"** et il peut remplacer le document directement depuis la page de suivi.

---

## §6. Use Cases & User Stories

### Conventions de lecture des diagrammes

Les diagrammes utilisent Mermaid afin de rester directement lisibles dans le document Markdown. Les flèches pleines représentent une action ou une dépendance directe ; les flèches annotées précisent la nature de la relation (`inclut`, `protège`, `trace`, etc.). Chaque diagramme est suivi d'une courte lecture pour expliquer son rôle dans le cahier des charges.

### 6.1 Diagramme de Cas d'Utilisation

Ce diagramme présente les interactions principales entre les deux acteurs du MVP : le **candidat**, qui utilise le portail public, et l'**administrateur FDS**, qui traite les dossiers reçus. Il permet de vérifier que chaque fonctionnalité prioritaire du MVP est reliée à un acteur et à un besoin métier.

```mermaid
flowchart LR
    Candidat(["Candidat"])
    Admin(["Admin FDS"])

    subgraph Portail["FDS Portail"]
        UC1["Consulter les cursus et dates clés"]
        UC2["Soumettre une candidature"]
        UC3["Simuler le paiement"]
        UC4["Téléverser les pièces justificatives"]
        UC5["Suivre l'état du dossier (et progression)"]
        UC6["Remplacer un document rejeté"]

        UC7["Se connecter au tableau de bord"]
        UC8["Consulter les candidatures"]
        UC9["Valider ou rejeter un document"]
        UC10["Auditer les décisions"]
    end

    Candidat --> UC1
    Candidat --> UC2
    Candidat --> UC5

    UC2 -->|inclut| UC3
    UC2 -->|inclut| UC4
    UC5 -->|si rejet| UC6

    Admin --> UC7
    Admin --> UC8
    Admin --> UC9

    UC7 -->|protège| UC8
    UC8 -->|inclut| UC9
    UC9 -->|trace| UC10
```

**Lecture du diagramme :** le candidat n'a pas besoin de compte pour postuler ; il utilise sa référence pour suivre son dossier. L'administrateur, lui, doit obligatoirement passer par l'authentification avant d'accéder aux dossiers et de prendre une décision.

### 6.2 User Stories (Backlog MVP)

- **US1 : S'informer sur les cursus et prérequis**
  - *En tant que* candidat, *je veux* consulter la description d'un cursus et la liste de ses documents requis *afin de* préparer mon dossier d'admission avant de postuler.
  - **Critères d'acceptation (Gherkin) :**
    - *Lorsque* je suis sur la page d'accueil du portail
    - *Quand* je clique sur le cursus "Génie Informatique"
    - *Alors* la page affiche la présentation du cursus, les dates clés d'admission, et la liste exacte des pièces justificatives à fournir.

- **US2 : Téléverser les fichiers**
  - *En tant que* candidat, *je veux* téléverser mes fichiers (PDF/JPG) en ligne *afin de* ne pas avoir à les apporter physiquement au secrétariat.
  - **Critères d'acceptation (Gherkin) :**
    - *Lorsque* je remplis mon formulaire de candidature
    - *Quand* j'attache un fichier PDF de moins de 5 Mo
    - *Alors* le fichier est accepté et stocké de manière sécurisée sur Cloudinary.

- **US3 : Validation par l'Admin**
  - *En tant qu'* administrateur, *je veux* modifier le statut d'un document (`valide`, `rejete`) *afin que* le candidat connaisse l'état de sa demande.
  - **Critères d'acceptation (Gherkin) :**
    - *Lorsque* je suis connecté au tableau de bord
    - *Quand* je clique sur "Rejeter" pour un document spécifique
    - *Alors* le statut du document passe à "rejete" en base de données.

- **US4 : Email de confirmation**
  - *En tant que* candidat, *je veux* recevoir un email de confirmation après soumission *afin d'* avoir une trace officielle de mon dossier.
  - **Critères d'acceptation (Gherkin) :**
    - *Lorsque* ma candidature est soumise avec succès
    - *Quand* le serveur génère la référence du dossier
    - *Alors* je reçois un email asynchrone contenant cette référence.

- **US5 : Notification de statut**
  - *En tant que* candidat, *je veux* être notifié par email lorsqu'un document est validé ou rejeté *afin de* réagir rapidement.
  - **Critères d'acceptation (Gherkin) :**
    - *Lorsque* mon dossier est en cours de traitement
    - *Quand* l'administrateur rejette un de mes documents
    - *Alors* je reçois un email m'indiquant le motif du rejet et le lien de suivi.

- **US6 : Remplacement de document**
  - *En tant que* candidat, *je veux* pouvoir remplacer un document rejeté depuis la page de suivi *afin de* corriger mon dossier sans me déplacer.
  - **Critères d'acceptation (Gherkin) :**
    - *Lorsque* je suis sur la page de suivi de mon dossier et qu'un document est rejeté
    - *Quand* j'uploade un nouveau document valide à la place
    - *Alors* le statut de ce document repasse à "en_attente" pour révision.

- **US7 : Simulation de paiement**
  - *En tant que* candidat, *je veux* simuler le paiement de mes frais via MonCash ou NatCash *afin de* finaliser mon inscription avant de téléverser mes documents.
  - **Critères d'acceptation (Gherkin) :**
    - *Lorsque* j'ai validé mes informations personnelles
    - *Quand* je confirme la simulation du paiement sur l'interface
    - *Alors* je suis autorisé à passer à l'étape finale d'upload.

- **US8 : Barre de progression**
  - *En tant que* candidat, *je veux* visualiser l'avancement de mon dossier sous forme de barre de progression *afin de* comprendre rapidement les étapes complétées et les actions restantes.
  - **Critères d'acceptation (Gherkin) :**
    - *Lorsque* je consulte le suivi de mon dossier
    - *Quand* tous mes documents sont marqués comme "valides"
    - *Alors* la barre de progression atteint 100% et indique que le dossier est complet.

- **US9 : Mesure de l'hypothèse**
  - *En tant qu'* équipe produit, *je veux* enregistrer si le candidat s'est déplacé physiquement lors de sa candidature *afin de* mesurer le taux de complétion sans déplacement.
  - **Critères d'acceptation (Gherkin) :**
    - *Lorsque* le candidat arrive à la dernière étape du formulaire
    - *Quand* il répond "Non" à la question "Avez-vous dû vous déplacer ?"
    - *Alors* la valeur "false" est sauvegardée dans le champ `deplacement_physique` en base.

### 6.3 User Stories Sécurité

Ces stories traduisent les exigences de sécurité en besoins compréhensibles par les acteurs du système. Elles complètent les user stories fonctionnelles et permettent de vérifier que la protection des données n'est pas seulement un détail technique.

- **US-S1 : Authentification de l'administrateur**
  - *En tant qu'* administrateur, *je veux* devoir m'authentifier avant d'accéder au tableau de bord *afin d'* empêcher l'accès non autorisé aux dossiers des candidats.
  - **Critères d'acceptation (Gherkin) :**
    - *Lorsque* je tente d'accéder à la route `/admin/dashboard` sans être authentifié
    - *Quand* le système intercepte ma requête
    - *Alors* le serveur retourne un code d'erreur HTTP 401 ou 403 et me redirige vers le formulaire de connexion.

- **US-S2 : Traçabilité des actions**
  - *En tant qu'* administrateur autorisé, *je veux* que mes actions de validation ou de rejet soient enregistrées avec mon identité et la date *afin d'* assurer la traçabilité des décisions.
  - **Critères d'acceptation (Gherkin) :**
    - *Lorsque* je valide ou rejette un document candidat depuis le tableau de bord
    - *Quand* la mise à jour est persistée en base de données
    - *Alors* le système enregistre automatiquement mon identifiant unique dans `valide_par` et l'horodatage de l'action dans `date_validation`.

- **US-S3 : Confidentialité des documents**
  - *En tant que* candidat, *je veux* que mes documents soient accessibles uniquement aux administrateurs autorisés *afin de* protéger mes données personnelles.
  - **Critères d'acceptation (Gherkin) :**
    - *Lorsque* l'URL d'un document candidat est requise en ligne par un utilisateur anonyme
    - *Quand* le serveur traite la requête sur l'API de proxy
    - *Alors* le serveur refuse la requête et retourne une erreur 403 Forbidden.

- **US-S4 : Protection contre les fichiers malveillants**
  - *En tant qu'* administrateur, *je veux* que la plateforme rejette les fichiers invalides ou trop volumineux *afin de* protéger l'espace de stockage de la FDS contre les uploads malveillants.
  - **Critères d'acceptation (Gherkin) :**
    - *Lorsque* j'uploade un fichier supérieur à 5 Mo ou d'un format autre que PDF/JPG/JPEG (ou un exécutable déguisé)
    - *Quand* le serveur analyse les magic bytes et la taille du fichier
    - *Alors* le serveur rejette le fichier et retourne une erreur d'upload explicite.

- **US-S5 : Limite des tentatives (Anti brute-force)**
  - *En tant qu'* administrateur, *je veux* que les tentatives de connexion échouées bloquent temporairement mon adresse IP *afin d'* empêcher un attaquant de forcer l'accès à mon compte.
  - **Critères d'acceptation (Gherkin) :**
    - *Lorsque* je saisis un mot de passe incorrect 5 fois consécutives en moins de 60 secondes
    - *Quand* je tente une 6ème connexion
    - *Alors* le système bloque temporairement mon adresse IP et retourne une erreur 429 Too Many Requests.

- **US-S6 : Isolation des secrets applicatifs**
  - *En tant qu'* administrateur, *je veux* que les secrets applicatifs soient isolés du code source *afin d'* éviter toute fuite de clés d'API ou de mots de passe sur les dépôts de code publics.
  - **Critères d'acceptation (Gherkin) :**
    - *Lorsque* l'application démarre et charge sa configuration
    - *Quand* elle requiert les clés d'API Cloudinary, Resend et JWT
    - *Alors* elle lit ces clés exclusivement depuis les variables d'environnement locales et n'expose aucun secret en dur dans le dépôt Git.

- **US-S7 : Messages d'erreur génériques**
  - *En tant que* candidat, *je veux* voir des messages d'erreur génériques lors d'un échec technique *afin de* m'assurer que mes données personnelles ne soient pas exposées par des détails système.
  - **Critères d'acceptation (Gherkin) :**
    - *Lorsque* l'application rencontre une exception inattendue lors du traitement d'une requête
    - *Quand* elle génère la réponse HTTP retournée au client
    - *Alors* elle retourne un code d'erreur standard (400, 403, 500) avec un message générique sans révéler la stack trace ou les détails internes de la base de données.

### 6.4 Matrice de traçabilité MVP

| Besoin métier | Fonctionnalité | Donnée/API concernée | Preuve attendue |
|---|---|---|---|
| Réduire le déplacement physique | Candidature en ligne + upload | `POST /api/candidature`, `POST /api/upload` | Dossier complet créé sans dépôt papier |
| Mesurer l'impact du portail | Question déplacement + persistance | `candidats.deplacement_physique`, `POST /api/candidature` | ≥ 70 % avec `deplacement_physique = false` (requête SQL ou export admin) |
| Donner une source officielle | Pages cursus + documents requis | `GET /api/documents-requis` + catalogue cursus | Informations visibles avant candidature |
| Rassurer le candidat | Référence dossier + email | `reference_dossier`, service email | Référence affichée et envoyée |
| Rendre le suivi compréhensible | Barre de progression du dossier | `statut_paiement`, `statut_validation` | Étapes affichées selon l'état réel du dossier |
| Donner de la traçabilité au secrétariat | Tableau admin + audit validation | `valide_par`, `date_validation`, `statut_validation` | Décision admin historisée |
| Corriger sans revenir sur place | Remplacement d'un document rejeté | Upsert `DocumentSoumis` | Nouveau fichier en attente de validation |
| Protéger les données personnelles | Auth admin + contrôle d'accès documents | JWT, `GET /api/admin/proxy-document` | Aucun document visible sans authentification |
| Réduire les attaques applicatives | Validation fichiers + rate limiting | `POST /api/upload`, `POST /api/auth/token` | Fichiers dangereux rejetés et brute-force limité |

---

## §7. Diagramme de séquence

### 7.1 Diagramme de Séquence (Soumission, upload et notification)

Ce diagramme précise la collaboration technique entre le frontend React, le backend FastAPI, la base de données, Cloudinary et Resend. Il montre aussi que les emails sont déclenchés par des événements métier, sans devenir la source de vérité du dossier.

```mermaid
sequenceDiagram
    participant C as Candidat (React)
    participant API as FastAPI (Backend)
    participant DB as PostgreSQL
    participant Cloud as Cloudinary
    participant Mail as Resend (Email)
    participant A as Admin FDS

    C->>API: POST /api/candidature (infos + paiement simulé + deplacement_physique)
    activate API
    API->>DB: INSERT candidat + référence dossier + deplacement_physique
    DB-->>API: Dossier créé
    API-->>C: 201 Created + reference_dossier
    deactivate API

    loop Pour chaque document requis
        C->>API: POST /api/upload (fichier + candidat_id)
        activate API
        API->>API: Vérifier extension, taille et type MIME réel
        API->>Cloud: Upload sécurisé
        Cloud-->>API: URL sécurisée
        API->>DB: INSERT/UPDATE document_soumis (statut='en_attente')
        DB-->>API: Document enregistré
        API-->>C: 201 Created + URL document
        deactivate API
    end

    API->>Mail: Envoyer email de confirmation
    Mail-->>C: Email avec référence et lien de suivi

    C->>API: GET /api/candidature/{reference}
    API->>DB: SELECT dossier + documents
    DB-->>API: Statuts du dossier
    API-->>C: Données de suivi + progression

    A->>API: PUT /api/admin/documents/{id}/statut
    activate API
    API->>DB: UPDATE statut_validation + audit
    DB-->>API: Statut mis à jour
    API->>Mail: Envoyer notification validation/rejet
    Mail-->>C: Email de statut
    API-->>A: Confirmation de mise à jour
    deactivate API
```

**Lecture du diagramme :** la confirmation du dossier et la notification de statut sont asynchrones du point de vue métier : si l'email échoue, le dossier et ses statuts restent enregistrés en base de données.

---

## §9. Modèle de données (Classes & ERD)

### Principes fondateurs : Langage Ubiquitaire et Normalisation 3NF

Le modèle de données de FDS Portail a été conçu en respectant deux principes fondamentaux de l'ingénierie logicielle :
1. **Le Langage Ubiquitaire (Domain-Driven Design) :** Les noms des entités (`Candidat`, `DocumentRequis`, `DocumentSoumis`) ne sont pas des termes techniques génériques (ex: `UserFile`, `Upload`). Ils reprennent le vocabulaire exact utilisé par le secrétariat de la FDS lors des interviews, garantissant que le code reflète parfaitement la réalité métier.
2. **Normalisation 3NF (Troisième Forme Normale) :** Afin d'éviter la redondance et les anomalies de mise à jour, nous avons séparé la notion de *ce qui est exigé* (`DocumentRequis`, géré par l'administration) de *ce qui est fourni* (`DocumentSoumis`, envoyé par le candidat). Chaque attribut ne dépend que de sa clé primaire absolue.

**Le Concept de System of Record (SoR)**

Conformément à l'architecture globale de la faculté, le module **FDS SYS** (et non FDS Portail) est le **System of Record (SoR)** de toutes les identités utilisateurs internes de la plateforme. La table `Utilisateur` présente dans notre modèle ne fait que *consommer* cette donnée pour gérer l'authentification (ex: SSO) et tracer les décisions administratives. FDS Portail n'est pas la source de vérité pour la création ou la modification des comptes administrateurs.

En revanche, l'entité `Candidat` représente une personne externe qui soumet un dossier d'admission. Dans le MVP, le candidat n'a pas de compte global. Le FDS Portail est donc le SoR exclusif des dossiers de candidature.

### 9.1 Diagramme de Classes UML

Le diagramme ci-dessous représente les entités persistantes nécessaires au MVP. Il distingue les **candidats**, qui peuvent postuler sans compte, des **utilisateurs administratifs**, qui doivent s'authentifier pour traiter les dossiers.

```mermaid
classDiagram
    class Utilisateur {
        +UUID id
        +String email
        +String mot_de_passe_hash
        +String role
        +DateTime created_at
    }
    
    class Candidat {
        +UUID id
        +String reference_dossier
        +String nom
        +String prenom
        +String email
        +String statut_paiement
        +String methode_paiement
        +String reference_paiement
        +Boolean notifications_actives
        +Boolean deplacement_physique
        +DateTime created_at
    }
    
    class DocumentRequis {
        +UUID id
        +String nom
        +String description
        +String format_accepte
        +Boolean est_obligatoire
        +DateTime mis_a_jour_le
    }
    
    class DocumentSoumis {
        +UUID id
        +UUID candidat_id
        +UUID document_requis_id
        +String fichier_url
        +String statut_validation
        +DateTime soumis_le
        +UUID valide_par
        +DateTime date_validation
    }
    
    Candidat "1" -- "N" DocumentSoumis : possède
    DocumentRequis "1" -- "N" DocumentSoumis : définit
    Utilisateur "1" -- "N" DocumentSoumis : valide
```

**Lecture du diagramme :** `DocumentSoumis` est l'entité centrale du suivi. Son `statut_validation` alimente la barre de progression côté candidat, tandis que `valide_par` et `date_validation` assurent la traçabilité côté administration.

### 9.2 Contraintes métier
- Chaque dossier possède une référence unique.
- Un candidat ne peut avoir qu'un dossier actif par campagne d'admission.
- Les formats autorisés sont PDF, JPG et JPEG.
- La taille maximale d'un fichier est fixée à 5 Mo.
- Le backend vérifie le type MIME réel avant enregistrement.
- L'admission nécessite la validation préalable d'une étape de paiement simulé (statut et référence enregistrés en BDD).
- Un document remplacé conserve le même couple logique `(candidat_id, document_requis_id)` afin d'éviter les doublons dans le dossier.
- Le statut d'un document remplacé repasse automatiquement à `en_attente`.
- Les décisions administratives doivent toujours être auditables (`valide_par`, `date_validation`).
- À chaque soumission, `deplacement_physique` est obligatoire : `false` si le candidat n'a pas eu besoin de se déplacer, `true` sinon. Ce champ alimente l'indicateur « taux de complétion sans déplacement » (§3.5). Les dossiers antérieurs à l'introduction du champ peuvent avoir `NULL` (non renseigné).
- La contrainte `UNIQUE (candidat_id, document_requis_id)` sur `documents_soumis` garantit l'upsert sans doublon lors d'un remplacement.

### 9.3 Modèle Physique (Schéma SQL PostgreSQL)

Le modèle physique ci-dessous traduit l'ERD 3NF en commandes DDL (`CREATE TABLE`), en imposant strictement l'intégrité référentielle et les règles métier au niveau de la base de données.

```sql
-- Table consommatrice du SoR externe (FDS SYS)
CREATE TABLE utilisateurs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    mot_de_passe_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'user',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE candidats (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    reference_dossier VARCHAR(20) UNIQUE NOT NULL,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    statut_paiement VARCHAR(50) DEFAULT 'en_attente',
    methode_paiement VARCHAR(50),
    reference_paiement VARCHAR(100),
    notifications_actives BOOLEAN DEFAULT TRUE,
    deplacement_physique BOOLEAN, -- Pour la mesure d'hypothèse
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE documents_requis (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nom VARCHAR(255) NOT NULL,
    description TEXT,
    format_accepte VARCHAR(100) DEFAULT 'pdf,jpg,jpeg',
    est_obligatoire BOOLEAN DEFAULT TRUE,
    mis_a_jour_le TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE documents_soumis (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    candidat_id UUID NOT NULL REFERENCES candidats(id) ON DELETE CASCADE,
    document_requis_id UUID NOT NULL REFERENCES documents_requis(id) ON DELETE CASCADE,
    fichier_url VARCHAR(500) NOT NULL,
    statut_validation VARCHAR(50) DEFAULT 'en_attente',
    soumis_le TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    valide_par UUID REFERENCES utilisateurs(id) ON DELETE SET NULL,
    date_validation TIMESTAMP WITH TIME ZONE,
    
    -- Contrainte d'unicité pour empêcher les doublons de pièces justificatives
    CONSTRAINT unique_document_par_candidat UNIQUE (candidat_id, document_requis_id)
);
```

---

---

## §10. Architecture technique

Le modèle de données et les séquences s'exécutent au sein d'une **architecture 3-tiers (Déploiement)** combinée à la **Clean Architecture (Organisation du code interne)** — deux niveaux d'abstraction complémentaires qui coexistent dans la même application. La Clean Architecture garantit que la logique métier reste **totalement indépendante** des frameworks, de la base de données et des services externes (Cloudinary, Resend).

### 10.1 Diagramme de Composants et Flux
Le diagramme de composants ci-dessous présente la structure physique et logique du système FDS Portail :

![Architecture des composants](livrables/figures/mermaid-diagram.png)

Ce diagramme montre le découpage logique du système. Le portail reste un **monolithe modulaire** : il est déployé simplement, mais ses responsabilités internes sont séparées afin de faciliter la maintenance et une éventuelle évolution future.

```mermaid
flowchart TB
    Candidat((Candidat))
    Admin((Admin FDS))

    subgraph Plateforme["Plateforme FDS - FDS Portail"]
        Front["Frontend React / Vite"]
        API["API FastAPI"]

        subgraph Modules["Modules internes du backend"]
            Auth["Auth\nJWT + RBAC"]
            Candidature["Candidature\ncréation + suivi"]
            Documents["Documents\nupload + remplacement"]
            Administration["Administration\nvalidation + audit"]
        end

        DB[(PostgreSQL\nDonnées candidats, documents et utilisateurs)]
    end

    Cloudinary[("Cloudinary\nStockage fichiers")]
    Resend[("Resend\nEmail transactionnel")]

    subgraph Futur["Phase ultérieure hors MVP"]
        Pay["FDS Pay"]
        MonCash[("API MonCash / NatCash")]
    end

    Candidat -->|HTTPS| Front
    Admin -->|HTTPS| Front
    Front -->|REST JSON| API

    API --> Auth
    API --> Candidature
    API --> Documents
    API --> Administration

    Auth -->|lecture utilisateurs| DB
    Candidature -->|lecture / écriture| DB
    Documents -->|lecture / écriture| DB
    Administration -->|lecture / écriture + audit| DB

    Documents -->|upload sécurisé| Cloudinary
    Candidature -->|confirmation| Resend
    Administration -->|notification statut| Resend

    Candidature -.->|simulation aujourd'hui| Pay
    Pay -.->|Webhook| MonCash
```

**Lecture du diagramme :** les services Cloudinary et Resend sont externes au système. PostgreSQL reste la source de vérité : les emails et les URLs de fichiers ne remplacent jamais les statuts enregistrés en base.

### 10.2 Pattern Architectural : Monolithe Modulaire + Clean Architecture

FDS Portail adopte un **Monolithe Modulaire** dont le code interne est organisé selon les principes de la **Clean Architecture** — 4 couches avec une seule règle : **les dépendances ne pointent que vers l'intérieur**.

| Couche | Contenu | Règle d'import |
|---|---|---|
| **Domain** (`entities/`) | Entités métier pures : `Candidat`, `DocumentSoumis`, `DocumentRequis` | N'importe rien d'externe (ni SQLAlchemy, ni FastAPI) |
| **Application** (`bll/` + `ports/`) | Use cases (`SoumettreCandidature`, `ValiderDocument`) et interfaces abstraites (`ICandidatRepository`, `IEmailService`) | Importe uniquement le Domain |
| **Infrastructure** (`dal/`) | Adapters concrets : `CandidatRepositorySQLAlchemy`, `CloudinaryStorageAdapter`, `ResendEmailAdapter` | Implémente les interfaces du Application layer |
| **Presentation** (`api/`) | Routers FastAPI, Pydantic DTOs, middleware, injection de dépendances | Appelle les Use Cases ; ne contient aucune logique métier |

> **Détail complet de l'architecture :** la Règle de Dépendance, le Principe d'Inversion (Ports & Adapters), la structure des répertoires cible et les tests d'architecture sont documentés dans [`project-docs/_ARCHITECTURE_EXPLAINED.md`](project-init-kit/project-docs/_ARCHITECTURE_EXPLAINED.md).

> **Note MVP :** la séparation stricte peut être simplifiée en phase initiale. La règle absolue reste : **jamais de logique métier dans la couche Infrastructure, jamais d'import ORM dans le Domain**.

> **Pourquoi pas les Microservices ?** L'équipe est < 5 personnes, le domaine est en phase MVP. Les ports bien définis par la Clean Architecture préparent une extraction future sans refactoring majeur.

> **Application automatisée :** la Règle de Dépendance est vérifiée à chaque exécution de la suite de tests — voir [`tests/unit/test_architecture.py`](tests/unit/test_architecture.py).


### 10.3 Style d'API Choisi : REST (Contract-First)
FDS Portail expose une **API REST stateless** via FastAPI :

| Méthode HTTP | Action | Exemple endpoint |
|---|---|---|
| `GET` | Lire une ressource (idempotent) | `GET /api/candidature/{ref}` |
| `POST` | Créer une ressource | `POST /api/candidature` |
| `PUT` | Remplacer (idempotent) | `PUT /api/admin/documents/{id}/statut` |
| `DELETE` | Supprimer | *(hors scope MVP)* |

**Approche Contract-First :** le contrat API (schémas Pydantic / OpenAPI auto-généré par FastAPI via `/docs`) est défini avant le développement frontend — garantissant l'alignement entre les deux équipes sans ambiguïté. Le frontend peut mocker le backend via Swagger UI pendant le développement.

> **Pourquoi REST et non GraphQL/WebSockets ?** Le portail est une application CRUD classique avec des besoins uniformes (pas d'over-fetching problématique). REST est stateless, cacheable (GET), universellement compatible, et parfaitement outillé (OpenAPI). WebSockets serait surdimensionné pour des notifications différées (email suffisant).

### 10.4 Système de notification par email (Composant technique)
Le portail intègre un service de notification transactionnel par email via **Resend** (API REST). Trois événements déclenchent automatiquement un envoi :

| Événement | Destinataire | Contenu de l'email |
|---|---|---|
| Soumission de candidature | Candidat | Confirmation HTML avec numéro de référence `CAN-XXXX` et lien vers la page de suivi |
| Document **validé** par l'admin | Candidat | Notification verte indiquant le nom du document validé |
| Document **rejeté** par l'admin | Candidat | Notification rouge avec le nom du document et un bouton **"Remplacer le document →"** |

- Les emails sont **conditionnels** : l'envoi ne se produit que si `notifications_actives = true` sur le profil du candidat.
- Le service est **non-bloquant** : une erreur d'envoi email ne fait pas échouer la requête API principale.
- L'implémentation se trouve dans `backend/services/email.py`.

---

---

## §11. Choix technologiques

> Cette section documente les décisions d'architecture selon la méthode **ATAM simplifiée** (Architecture Tradeoff Analysis Method) et fournit les choix raisonnés pour la performance, la sécurité et l'accessibilité.

### 11.1 Architectural Decision Records (ADRs)

Cette section présente les décisions d'architecture structurantes prises pour le projet FDS Portail.

#### ADR-001 : Monolithe Modulaire vs Microservices
```

Statut : Accepté

#### Contexte
FDS Portail est un MVP développé par une équipe de < 5 personnes.
Le domaine métier (admission universitaire) est en cours de définition.
Le budget DevOps est limité et les compétences en opérations distribuées sont absentes.

#### Options considérées
- Option A — Monolithe Modulaire
  + Déploiement simple (1 artefact), transactions ACID, debugging facile
  + Modules découplés → migration future possible
  - Scalabilité uniforme seulement
- Option B — Microservices
  + Scalabilité indépendante par service, isolation des pannes
  - Complexité opérationnelle élevée (tracing, latence réseau), coût infra élevé
  - Équipe de 10+ développeurs recommandée

#### Décision
Option A — Monolithe Modulaire.
L'équipe est < 5 personnes. Le domaine est en phase MVP. La douleur opérationnelle
des microservices n'est pas justifiée. Les modules bien séparés permettront
une migration progressive si nécessaire.

#### Conséquences
+ Livraison rapide, maintenabilité élevée, cohérence ACID
- Scalabilité uniforme — surveiller si le trafic devient différencié par module
```

#### ADR-002 : REST vs GraphQL
```

Statut : Accepté

#### Contexte
FDS Portail expose des données à un frontend React et potentiellement
à des systèmes tiers (FDS Pay, FDS Akademi).

#### Options considérées
- Option A — REST
  + Standard universel, cache HTTP natif (GET), stateless, OpenAPI auto-généré
  + Compatible tous clients, documentation Swagger automatique (FastAPI)
  - Over-fetching possible sur certains endpoints
- Option B — GraphQL
  + Pas d'over-fetching, flexible pour le client
  - Cache HTTP difficile, courbe d'apprentissage serveur, overkill pour CRUD simple

#### Décision
Option A — REST stateless avec FastAPI.
Le portail est un CRUD classique. Les besoins de données sont uniformes.
OpenAPI est auto-généré par FastAPI — Contract-First sans effort supplémentaire.

#### Conséquences
+ Interface standardisée, documentation /docs disponible immédiatement
- Si les besoins clients deviennent très hétérogènes → envisager GraphQL (ADR à créer)
```

#### ADR-003 : Clean Architecture vs MVC
```
Statut : Accepté

Décision : Clean Architecture (Domain / Application / Infrastructure / Presentation).
Raison   : Logique métier testable sans DB, remplacement de services externes sans impact
           sur le domaine, structure explicite pour l'onboarding.
Compromis: Légère verbosité (interfaces/ports) — acceptable car prévient le couplage
           irréversible entre logique métier et infrastructure.
Référence: project-docs/_ARCHITECTURE_EXPLAINED.md (Parties 1 & 2)
```

### 11.2 Stack Technologique & Écosystème

#### Justification de la Stack
- **Frontend :** React 19 / Vite. Navigation côté client (SPA) pour garantir une expérience fluide (Mobile-First) essentielle pour les utilisateurs en 3G (découlant du Persona).
- **Backend :** FastAPI (Python). Performance asynchrone (`async/await`) pour ne pas bloquer le serveur lors des uploads Cloudinary et des appels email. Auto-génère la documentation OpenAPI.
- **Base de données :** PostgreSQL. Garantit l'intégrité référentielle stricte (ACID) entre les Candidats et leurs Documents. Index B-Tree sur les colonnes de filtrage fréquentes (`reference_dossier`, `email`, `candidat_id`).
- **SSO (Single Sign-On) :** L'authentification des administrateurs se fait via des jetons JWT validés contre la table partagée `Utilisateurs`, liant ainsi les frontières entre FDS Portail et FDS Admin.

#### Checklist technique (GL-EN3-2026)
| Couche | Technologie | Justification |
|---|---|---|
| Frontend | React 19 / Vite / TypeScript | SPA Mobile-First, typage fort, HMR rapide |
| Backend | FastAPI 0.x / Python 3.11 | Async natif, OpenAPI auto-généré, Pydantic |
| Base de données | PostgreSQL 15 | ACID, intégrité référentielle, index B-Tree |
| ORM | SQLAlchemy 2.x | Requêtes paramétrées (anti-injection A05) |
| Auth | python-jose (JWT HS256) + passlib (bcrypt) | Lib éprouvée (anti-A07), hash sécurisé |
| Stockage fichiers | Cloudinary | Upload sécurisé, URL signée, sans infra propre |
| Email | Resend (API REST) | Notifications transactionnelles non-bloquantes |
| Déploiement Frontend | Vercel | CDN global, HTTPS automatique |
| Déploiement Backend | Railway (PaaS) | Déploiement CI/CD depuis GitHub, Stateless |
| Secrets | `.env` hors repo + `.gitignore` | Anti-A02, Anti-A04 |

#### Dépendances Backend (requirements.txt)
- `fastapi`, `uvicorn[standard]` — serveur ASGI async
- `sqlalchemy`, `psycopg2-binary` — ORM + driver PostgreSQL
- `pydantic` — validation des entrées (anti-A05)
- `python-jose[cryptography]` — JWT
- `passlib[bcrypt]` — hachage mots de passe
- `cloudinary` — upload fichiers
- `resend` — email transactionnel
- `filetype` — vérification type MIME réel (anti-upload malveillant)
- `python-multipart` — upload form-data

#### Audit de sécurité des dépendances
```bash
# À exécuter à chaque sprint
pip check
npm audit
```

---

### 11.3 Sécurité applicative & OWASP (Security by Design)

La sécurité est conçue dès l'architecture, selon les **3 principes fondateurs Security by Design** :

| Principe | Application dans FDS Portail |
|---|---|
| **Least Privilege** | Chaque endpoint vérifie que l'utilisateur connecté a le droit d'accéder à LA ressource demandée (pas seulement d'être connecté). Un candidat ne voit que son propre dossier. |
| **Defense in Depth** | Validation côté client (UX) + validation côté serveur (FastAPI) + contraintes SQL (UNIQUE, FK) + type MIME réel + pare-feu Cloudinary. |
| **Fail Secure** | En cas d'exception dans le contrôle d'accès → 403 Forbidden. Jamais d'accès accordé par défaut. |

#### OWASP Top 10 : 2025 — Mitigations appliquées

| Code | Vulnérabilité | Mitigation dans FDS Portail |
|---|---|---|
| **A01** | Broken Access Control | `get_current_admin()` vérifie le rôle sur chaque endpoint admin. Deny by default. |
| **A02** | Security Misconfiguration | Secrets dans `.env` (hors repo Git), `.env` dans `.gitignore`. Headers HTTP configurés. |
| **A03** | Supply Chain Failures | `pip check` / `npm audit` à chaque sprint. Dépendances documentées en §10.2. |
| **A04** | Cryptographic Failures | Mots de passe hashés bcrypt (`passlib`). HTTPS obligatoire. Secrets hors du code source. |
| **A05** | Injection | SQLAlchemy ORM (requêtes paramétrées — zéro concaténation SQL). Validation Pydantic. |
| **A06** | Insecure Design | Threat Modeling STRIDE appliqué (voir tableau ci-dessous). Rate limiting sur `/api/auth/token` et `/api/candidature`. |
| **A07** | Authentication Failures | JWT à durée de vie courte. Sessions invalidées à la déconnexion. Lib éprouvée (`python-jose`). |
| **A08** | Integrity Failures | JWT signé avec secret fort (256 bits min.). Pas d'état côté client sans signature. |
| **A09** | Logging Failures | Middleware de logging : chaque requête HTTP loggée avec code de réponse + userId (hors données sensibles). |
| **A10** | Exceptional Conditions | `try/catch` global sur chaque endpoint → retourne 400/403/500 sans exposer les détails internes. |

#### Threat Modeling STRIDE — Scénarios d'abus identifiés

| Menace STRIDE | Scénario d'abus | Surface d'attaque | Mitigation appliquée |
|---|---|---|---|
| **Spoofing** | Un acteur se fait passer pour un admin en forgeant un JWT | `Authorization: Bearer` header | Signature HS256 validée à chaque requête via `get_current_admin()` |
| **Tampering** | Un candidat modifie la référence dossier pour accéder à un autre dossier | `GET /api/candidature/{ref}` | Aucune donnée sensible exposée par référence seule ; seul le statut public est retourné |
| **Repudiation** | Un admin nie avoir rejeté un document | `PUT /api/admin/documents/{id}/statut` | `valide_par` + `date_validation` enregistrés et immuables en BDD |
| **Information Disclosure** | Stack trace exposée en cas d'erreur serveur | Tous les endpoints | Messages d'erreur génériques côté client, détails dans les logs serveur uniquement |
| **Denial of Service** | Soumission massive de candidatures ou d'uploads pour épuiser les ressources | `POST /api/candidature`, `POST /api/upload` | Rate limiting `rate_limiter.py` : 5 requêtes / 60s sur `/api/auth/token` ; 10 requêtes / 60s par IP sur `/api/candidature` ; pagination sur les listes admin |
| **Elevation of Privilege** | Un utilisateur non-admin tente d'accéder aux routes `/api/admin/` | Toutes les routes admin | `get_current_admin()` + `deny by default` — 403 si rôle insuffisant |

#### Mécanismes de sécurité spécifiques aux fichiers
- **Validation des fichiers uploadés :** seuls les formats PDF, JPG et JPEG sont acceptés.
- **Contrôle du type MIME réel :** le backend utilise `filetype` pour vérifier le contenu réel du fichier (magic bytes) — pas uniquement l'extension.
- **Limitation de taille :** chaque fichier est limité à **5 Mo**.
- **Stockage indirect :** les fichiers sont stockés sur Cloudinary avec URL signée — jamais exposés directement depuis le serveur applicatif.
- **Proxy sécurisé :** `GET /api/admin/proxy-document` force le `Content-Type` correct et est accessible uniquement aux admins authentifiés.

#### Authentification & Autorisation (AuthN / AuthO)

- **AuthN (« Qui es-tu ? »)** : email + mot de passe hashé bcrypt → JWT signé (`HS256`, durée 60 min).
- **AuthO (« Qu'as-tu le droit de faire ? »)** : RBAC — table `Utilisateur.role` (`admin` / `agent`). Le rôle est vérifié à **chaque endpoint** via `get_current_admin()`, pas seulement à la connexion.
- **JWT Best Practices** : `exp` et `sub` validés à chaque requête. Secret ≥ 256 bits. Jamais de données sensibles dans le payload (base64 lisible).
- **Refresh tokens** : non implémentés dans le MVP — l'admin devra se reconnecter après 60 min d'inactivité. Un endpoint `POST /api/auth/refresh` est prévu en post-MVP (voir §10.5).

### 11.4 Performance & Scalabilité

#### Stratégie de Performance
La performance est conçue dès l'architecture selon la règle 80/20 : **mesurer avant d'optimiser**.

#### Performance Frontend (MVP 3G)
Pour répondre à l'exigence d'un chargement en moins de 3 secondes sur connexion lente (cf. §4.1), les optimisations suivantes sont intégrées nativement :
- **CSS Critique Inline (Anti-FOUC) :** L'ossature stylistique de base (couleurs de fond et de police) est injectée directement dans le `<head>` pour éviter l'effet d'écran blanc ou de texte nu pendant le chargement de React.
- **Fonts non-bloquantes :** Utilisation du pattern `media="print" + onload` et préconnexion DNS pour télécharger les Google Fonts sans bloquer le rendu initial (First Contentful Paint).
- **Code Splitting (Lazy Loading) :** Le bundle JavaScript est découpé par page via `React.lazy()`. L'utilisateur ne télécharge que le code de la page qu'il visite, réduisant la charge initiale de plus de 60%.
- **CDN Global :** Les actualités et dates clés sont servies via le cache CDN de Sanity (`useCdn: true`), rapprochant la donnée de l'utilisateur haïtien.

#### Design System (The Digital Curator) & Performance UX
Afin d'assurer une cohérence visuelle parfaite et une expérience utilisateur (UX) premium, le projet implémente un Design System sur-mesure nommé **"The Digital Curator"**.
- **Approche Atomic Design :** L'interface est construite à l'aide de composants UI purs et réutilisables (`Button`, `Card`, `Input`, `Badge`) situés dans `src/components/ui/`.
- **Variables CSS centralisées :** Les couleurs (Primary `#004B87`, Secondary, Error, Surface) et typographies sont définies dans `index.css` et exposées via TailwindCSS.
- **Règle du "No-Line" :** Utilisation d'espacements (gap, padding) et de variations de teintes (Surface-low, Surface-high) plutôt que des bordures dures (`border-b`), pour un rendu moderne, épuré et lisible sur mobile.
- **Animations fluides :** Utilisation de `motion/react` pour les transitions entre les étapes du formulaire et le rendu des listes, réduisant la charge cognitive (UX).

#### Caching Backend (Niveau Applicatif)
- **Cache HTTP** : les réponses `GET` statiques retournent des headers `Cache-Control` appropriés. Implémenté sur `GET /api/documents-requis` : `Cache-Control: public, max-age=300`.
- **Stratégie Cache-Aside (post-MVP)** : les résultats fréquemment lus et rarement modifiés (liste des `DocumentRequis`, cursus) seront mis en cache via Redis avec invalidation par TTL ou événement admin. Redis n'est pas dans la stack MVP — cette évolution est documentée en §10.5.

#### Pagination des listes
Toutes les listes retournées par l'API admin supportent la pagination pour éviter les Full Table Scans à volume croissant :

| Endpoint | Paramètres | Valeur par défaut |
|---|---|---|
| `GET /api/admin/candidatures` | `?page=1&limit=20` | 20 dossiers par page |
| `GET /api/admin/documents` | `?page=1&limit=50` | 50 documents par page *(post-MVP si liste dédiée)* |

La réponse de `GET /api/admin/candidatures` inclut `total`, `page`, `limit` et `items` (chaque item expose notamment `deplacement_physique`) pour permettre la navigation côté frontend.

#### Connection Pooling (PostgreSQL)
SQLAlchemy est configuré avec un pool de connexions pour éviter la saturation de Railway en production :

```python
# backend/database.py
engine = create_engine(
    DATABASE_URL,
    pool_size=5,        # connexions permanentes maintenues
    max_overflow=10,    # connexions supplémentaires autorisées en pic
    pool_timeout=30,    # délai d'attente avant erreur (secondes)
    pool_pre_ping=True  # vérifie la connexion avant usage (évite les connexions mortes)
)
```

#### Indexation Base de Données (PostgreSQL)

| Table | Colonne indexée | Type | Justification |
|---|---|---|---|
| `candidats` | `reference_dossier` | B-Tree UNIQUE | Recherche de suivi par référence (UC4) |
| `candidats` | `email` | B-Tree UNIQUE | Déduplication à l'inscription |
| `documents_soumis` | `candidat_id` | B-Tree | JOIN fréquent pour afficher le dossier |
| `documents_soumis` | `(candidat_id, document_requis_id)` | Composite UNIQUE | Contrainte métier upsert |

> **Problème N+1 évité** : les relations SQLAlchemy utilisent `lazy='select'` par défaut — les endpoints admin chargent les documents via JOIN explicite pour éviter N+1 requêtes.

#### Scalabilité
- **Stateless** : l'API FastAPI ne maintient aucun état en mémoire entre les requêtes — compatible Scale Out (plusieurs instances derrière un Load Balancer).
- **Scale Up (Phase MVP)** : augmentation de la puissance de la machine hôte si le trafic croît.
- **Scale Out (Phase post-MVP)** : ajout d'instances FastAPI derrière Nginx / AWS ELB avec Round Robin. Prérequis : déplacer les sessions vers Redis et les fichiers vers S3/MinIO.

### 11.5 Accessibilité (WCAG 2.1 Cible Niveau AA)

Le portail cible le niveau **AA** des Web Content Accessibility Guidelines 2.1, selon les 4 principes **P.O.U.R.** :

| Principe | Exigences appliquées |
|---|---|
| **Perceptible** | Alt text sur toutes les images. Contraste ≥ 4.5:1 (texte normal). Sous-titres si vidéo. Information non transmise par la couleur seule. |
| **Opérable** | Navigation clavier complète (Tab, Enter, Espace). Focus visible (`outline` présent). Pas de limite de temps stricte sur les formulaires. |
| **Compréhensible** | Labels explicites sur tous les champs. Messages d'erreur indiquant comment corriger. `<html lang='fr'>` déclaré. Navigation prévisible. |
| **Robuste** | HTML sémantique (`header`, `nav`, `main`, `footer`). ARIA roles si nécessaire. Composants natifs HTML préférés aux custom. |


---

## §12. Validation, Risques et Limites

Cette section transforme le cahier des charges en outil de pilotage : elle précise comment prouver que le MVP est acceptable, quels risques restent ouverts et quelles limites sont assumées en phase 1.

### 12.1 Définition de terminé (Definition of Done)

Le MVP est considéré comme terminé lorsque les conditions suivantes sont satisfaites :

- Un candidat peut consulter les cursus, ouvrir le formulaire, simuler un paiement, répondre à la question sur le déplacement physique, soumettre ses informations et téléverser tous les documents requis depuis un mobile.
- Le système génère une référence unique de dossier et permet de retrouver ce dossier depuis la page de suivi.
- Un administrateur authentifié peut consulter les candidatures, ouvrir les documents et valider ou rejeter chaque document.
- Un document rejeté peut être remplacé par le candidat sans créer un second dossier.
- Les emails de confirmation, validation et rejet sont déclenchés sans bloquer les opérations principales.
- Les contrôles serveur refusent les fichiers non autorisés, les fichiers trop lourds et les accès admin non authentifiés.
- Les pages critiques sont testées sur mobile et desktop, avec navigation clavier possible sur les formulaires.

### 12.2 Plan de tests fonctionnels

| Scénario | Données d'entrée | Résultat attendu |
|---|---|---|
| Soumission complète | Nom, prénom, email valide, paiement simulé, documents PDF/JPG | Dossier créé, référence affichée, documents en `en_attente` |
| Référence invalide | `CAN-2026-0000` inexistante | Message clair : dossier introuvable |
| Upload invalide | Fichier `.exe` ou fichier > 5 Mo | Rejet serveur avec message explicite |
| Validation admin | Admin connecté, document en attente | Statut `valide`, audit enregistré, email déclenché |
| Rejet admin | Admin connecté, document en attente | Statut `rejete`, audit enregistré, email de rejet déclenché |
| Remplacement candidat | Document rejeté + nouveau PDF/JPG valide | Même document logique mis à jour, statut repassé à `en_attente` |
| Accès non autorisé | Requête admin sans JWT | Réponse 401/403, aucune donnée sensible exposée |

### 12.3 Risques identifiés et mitigations

| Risque | Impact | Mitigation prévue |
|---|---|---|
| Connexion Internet faible côté candidat | Abandon du formulaire | Interface mobile légère, messages d'erreur clairs, fichiers limités à 5 Mo |
| Échec Cloudinary pendant l'upload | Document non transmis | Message explicite, possibilité de réessayer, aucun dossier marqué complet sans document |
| Échec Resend pendant l'email | Candidat non notifié | Email non bloquant, référence affichée à l'écran et disponible via suivi |
| Perte de la référence par le candidat | Difficulté à retrouver le dossier | Email de confirmation + recommandation d'affichage clair de la référence |
| Mauvais fichier envoyé | Rejet du dossier ou retard | Validation format/taille côté serveur + remplacement en ligne après rejet |
| Données personnelles exposées | Risque légal et réputationnel | Auth admin obligatoire, URLs de documents contrôlées, secrets hors dépôt |
| Croissance du volume de candidatures | Lenteur admin et suivi | Index sur référence/email/candidat, possibilité de scale out post-MVP |

### 12.4 Limites assumées en phase 1

- Le paiement est une simulation : aucune transaction réelle n'est exécutée dans FDS Portail.
- Le candidat ne possède pas de compte complet : le suivi repose sur la référence dossier.
- Les SMS/push notifications sont hors MVP et restent en amélioration future.
- Le portail ne gère pas les cours, les notes, les inscriptions pédagogiques ou l'espace étudiant complet.
- L'interopérabilité avec FDS Pay, FDS Akademi et un SSO institutionnel complet est préparée architecturalement, mais non livrée dans cette phase.
- **Refresh tokens absents** : le JWT admin expire après 60 min sans renouvellement automatique — l'administrateur devra se reconnecter manuellement. Un endpoint `POST /api/auth/refresh` est prévu en post-MVP.
- **Cache Redis absent** : le caching applicatif repose uniquement sur les headers `Cache-Control` HTTP dans cette phase. Redis sera introduit post-MVP pour les données fréquemment lues.

### 12.5 Évolutions post-MVP

| Priorité | Évolution | Bénéfice |
|---|---|---|
| P1 | Intégration réelle avec FDS Pay | Encaisser et réconcilier automatiquement les frais |
| P1 | Découpage backend en routeurs FastAPI par domaine | Renforcer le monolithe modulaire annoncé |
| P1 | Refresh tokens (`POST /api/auth/refresh`) | Sessions admin continues sans reconnexion toutes les 60 min |
| P1 | Cache Redis (Cache-Aside sur `DocumentRequis`) | Réduire la charge BDD sur les lectures fréquentes |
| P2 | Tableau de bord statistique des candidatures | Suivre les volumes, rejets, délais et programmes demandés |
| P2 | Notifications SMS | Atteindre les candidats qui consultent rarement leur email |
| P3 | Création d'un espace candidat complet | Historique, profil, documents persistants et communications |
| P3 | Export administratif CSV/PDF | Faciliter les commissions d'admission et l'archivage |

---

## §13. Annexe — Maquettes UI/UX

Cette section présente les captures d'écran des maquettes et de l'interface utilisateur de la plateforme FDS Portail. Elle distingue les pages publiques de l'application déployée en production (https://fds-portail.vercel.app) et les écrans du flux transactionnel complet (Walking Skeleton local).

### 13.1 Pages de l'application en production (Vercel)

Les captures ci-dessous sont issues du site officiel en ligne [fds-portail.vercel.app](https://fds-portail.vercel.app) et illustrent le design épuré "The Digital Curator" conforme au Design System.

#### 1. Page d'accueil officielle & Catalogue des Cursus
La vitrine publique présente les actualités académiques et la liste des formations disponibles.
![Page d'accueil Vercel](livrables/maquettes/vercel_home.png)

#### 2. Fiche Cursus Détaillée (Exemple : Génie Électronique)
Présentation complète des débouchés, des crédits, de la durée, et des pièces justificatives obligatoires exigées.
![Détails du cursus Vercel](livrables/maquettes/vercel_program.png)

#### 3. Formulaire de Candidature en Ligne (Mobile-First)
Interface mobile-first étape par étape pour saisir les données de contact et répondre à l'indicateur de déplacement physique.
![Formulaire de candidature Vercel](livrables/maquettes/vercel_application.png)

#### 4. Suivi en Ligne du Dossier (Recherche)
Interface publique permettant au candidat de saisir sa référence dossier pour interroger la base et suivre sa progression.
![Formulaire de suivi Vercel](livrables/maquettes/vercel_tracking.png)

#### 5. Formulaire de Contact & Assistance (Aide)
FAQ dynamique et formulaire de contact pour résoudre les doutes des lycéens à distance.
![Assistance et Aide Vercel](livrables/maquettes/vercel_contact.png)

#### 6. Page de Connexion Administration (Auth JWT)
Interface d'authentification sécurisée (email/mot de passe) pour les agents administratifs de la FDS.
![Authentification administrative Vercel](livrables/maquettes/vercel_login.png)

### 13.2 Flux transactionnel et Administration (Walking Skeleton local)

Les captures suivantes illustrent le fonctionnement du flux complet de bout en bout (y compris les services tiers et la revue admin) simulé en local.

#### 7. Écran de Paiement Mobile (Simulation MonCash)
Simulation de la passerelle de paiement mobile MonCash ou NatCash pour la validation des frais de dossier.
![Simulation paiement](livrables/maquettes/mockup_3.png)

#### 8. Téléversement des Pièces Justificatives
Zone d'upload sécurisée avec validation en temps réel de la conformité du format et de la taille (< 5 Mo).
![Téléversement documents](livrables/maquettes/mockup_4.png)

#### 9. Écran de Succès et Référence Dossier CAN-2026-X
Génération automatique du code de suivi unique et confirmation d'envoi d'email transactionnel.
![Succès candidature](livrables/maquettes/mockup_5.png)

#### 10. Tableau de Bord Admin (Gestion des Dossiers)
Liste consolidée des dossiers de candidatures avec suivi du statut et mesure de l'hypothèse de déplacement physique.
![Tableau de bord admin](livrables/maquettes/mockup_8.png)

#### 11. Écran de Revue Admin (Décision)
Interface de revue permettant à l'administrateur de valider ou de rejeter chaque pièce avec motif.
![Revue de document admin](livrables/maquettes/mockup_9.png)

#### 12. Remplacement de Document Rejeté par le Candidat
En cas de rejet d'une pièce, le candidat peut téléverser une nouvelle version depuis sa page de suivi.
![Remplacement document](livrables/maquettes/mockup_10.png)
