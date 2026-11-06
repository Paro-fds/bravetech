---
created: 2026-09-26T15:23:00Z
updated: 2026-11-06T02:48:44Z
workstream: WS-01
---

# Spécification Fonctionnelle — WS-01 Portail Public

**Workstream :** WS-01 Portail public  
**Statut :** ✅ Livré via Epic 1 (US-001, US-002) — évolutions du 2026-10-31 (admission unique au MPC, pages Histoire et Contact, Kreyòl) marquées **À faire** ci-dessous  
**Public cible :** Candidats, lycéens, grand public (accès sans authentification, optimisé mobile 360px et connexions intermittentes)

---

## 1. Description du comportement utilisateur

Le portail public constitue la vitrine officielle et la première étape du parcours candidat pour la Faculté des Sciences (FDS-UEH). Il permet à tout visiteur de découvrir le parcours de formation, d'accéder aux programmes et de préparer les pièces requises pour son dossier d'admission.

**Modèle de formation (voir PRD §1, ADR-008).** L'admission est unique : tout candidat entre au **Premier cycle MPC** (2 ans), puis choisit sa **branche** (Génie Civil, Génie Électromécanique, Génie Électronique, Architecture ; 3 ans). Parcours total : **5 ans**. Le portail ne propose aucun choix de cursus à la candidature.

### 1.1 Page d'accueil (`/`)

1. **En-tête institutionnel** : logo FDS-UEH, nom de la Faculté, sélecteur de langue FR / KR, menu (Accueil, Cursus, Histoire, Suivre mon dossier, Contact).
2. **Bandeau d'accroche** : badge d'après le calendrier d'admission (US-028) — « Admissions ouvertes jusqu'au 30 novembre 2026 », « Admissions à partir du … », « Admissions fermées », ou « Admissions ouvertes » sans calendrier ; message « Candidatez à la Faculté des Sciences, sans vous déplacer », bouton principal **Postuler maintenant** (`/postuler`), bouton secondaire **Suivre mon dossier** (`/suivi`). Sur ordinateur, une illustration d'un téléphone affichant un dossier validé pièce par pièce.
3. **Comment ça marche** : cinq étapes (découvrir le parcours, remplir le formulaire, payer en simulation, déposer les pièces, suivre son dossier).
4. **Une admission, puis votre branche** — **À faire** (Epic 1 affichait cinq cartes de même rang) :
   - Une carte mise en avant **Premier cycle MPC** (badge « Vous candidatez ici », 2 ans) menant à sa fiche.
   - Quatre cartes **branches** (3 ans) : Génie Civil, Génie Électromécanique, Génie Électronique, Architecture. Sur ordinateur, chaque carte porte une illustration légère.
5. **Accès rapide au suivi** : champ « Référence du dossier » (ex. `CAN-2026-0089`).
6. **Bandeau institutionnel** : « Une institution historique » (fondée en 1902) avec une photo réelle de la Faculté, lien vers `/histoire`.
7. **Pied de page** : Faculté des Sciences, UEH, Delmas 33 ; liens Histoire, Contact, Suivi ; rappel que le paiement en ligne est une simulation.

### 1.2 Fiche du Premier cycle MPC (`/cursus/mpc`) — **À faire**

1. **En-tête** : retour vers l'accueil, badges « Admission unique » et « Admissions ouvertes », titre, description.
2. **Chiffres clés** : durée du MPC (2 ans), durée totale (5 ans), frais de dossier (500 HTG, simulés), date limite de dépôt et rentrée.
   **Dates clés (US-028)** : ouverture des candidatures, date limite de dépôt, concours d'admission, publication des résultats, rentrée. Elles viennent du calendrier réglé par l'administration (espace admin → Calendrier) ; une date non fixée s'affiche « À confirmer par la Faculté ». Hors période, le badge « Admissions ouvertes » disparaît et la fiche indique que les candidatures sont fermées.
3. **Votre parcours en 5 ans** : MPC (années 1 et 2, « Vous candidatez ici »), puis branche au choix (années 3 à 5) avec les quatre branches nommées.
4. **Programme du MPC** : niveaux MPC 1 et MPC 2 avec, pour chaque matière, les heures de cours et de travaux pratiques (source `cursus/mpc.json`).
5. **Après le MPC** : quatre cartes branches illustrées, avec la mention que le choix de la branche se fait après le MPC et n'est pas demandé à la candidature.
6. **Pièces à fournir** : les cinq pièces obligatoires (voir §2.2). Aucun indicateur « facultatif ».
7. **Passerelle vers la candidature** : bouton **Déposer ma candidature** → `/postuler` (sans paramètre `cursus`), avec la mention « Sans déplacement. Sans compte à créer. » Sur mobile, la barre d'action reste fixée en bas de l'écran.

### 1.3 Fiche d'une branche (`/cursus/:id`, branches uniquement) — **À faire**

1. **En-tête** : badge « Branche » et « Après le MPC », titre, description.
2. **Présentation académique** : durée (3 ans), grille par niveau listant matières, codes et volumes horaires (source `cursus/<branche>.json`).
3. **Accès** : texte expliquant que la branche se choisit à la fin du MPC.
4. **Passerelle** : bouton **Voir l'admission au MPC** → `/cursus/mpc`. Pas de liste de pièces ni de bouton de candidature propre à la branche.

> Le fichier `cursus/genie-civil.json` ne décrit que les niveaux GC1 et GC2 alors que la branche dure 3 ans : le programme de 3e année est à fournir par la Faculté.

### 1.4 Page Histoire (`/histoire`) — **À faire**

1. **Bannière** : photo réelle de la cour de la Faculté (Delmas 33), titre « Plus d'un siècle de formation scientifique et technique en Haïti ».
2. **Contenu** : la fondation (1902, École des Sciences Appliquées et ses six fondateurs), repères chronologiques (1902, 1905, 1906, 1945, 1947, 1961, 1986), évolution de l'offre, gouvernance participative depuis 1986.
3. **Conseil de direction actuel** : J.E. Etienne, Hervé et Jadin Jadotte. Les noms, prénoms et titres exacts doivent être confirmés par la Faculté avant publication. Les anciens conseils ne sont pas affichés.
4. **Emplacement photo d'archive** à fournir par la Faculté.
5. **Appel à l'action** : « Rejoignez la prochaine promotion » → `/postuler`.

Source du texte : *Histoire de la Faculté Des Sciences* (document fourni par la Faculté).

### 1.5 Page Contact et accès (`/contact`) — **À faire**

1. **Coordonnées** : adresse (Delmas 33, Haïti), téléphone, email, horaires du secrétariat (à fournir par la Faculté).
2. **Questions fréquentes** : dois-je me déplacer pour candidater ? le paiement est-il réel ? j'ai perdu ma référence de dossier.
3. **Formulaire « Nous écrire »** : nom, email, message. L'acheminement du message (email au secrétariat) reste à préciser avant de planifier la story.
4. **Photo et plan d'accès** : photo de la Faculté, plan de Delmas 33 à intégrer.

### 1.6 Langues — **À faire**

1. Le français est la langue par défaut. Un sélecteur **FR / KR** dans l'en-tête bascule l'interface en Kreyòl.
2. Les textes créoles sont rédigés ou validés par la Faculté avant publication (les maquettes contiennent une proposition non validée).
3. Les données issues de `cursus/*.json` (noms de matières) restent en français.

### 1.7 Images — **À faire**

1. Privilégier des **photos réelles** de la Faculté (droit de publication confirmé, visages floutés si nécessaire) ; à défaut, des illustrations légères.
2. Aucun visuel contenant du texte incrusté ni un nom de faculté ou un logo différents du logo officiel FDS-UEH.
3. Aucune image sur les écrans d'action (formulaire, paiement simulé, dépôt de pièces, suivi). Poids des images : voir `NFR.md` (Performance).

---

### 1.8 Période de candidature (`/postuler`, US-028)

1. **Avant l'ouverture ou après la date limite**, un nouveau candidat voit « Les candidatures sont fermées », avec la date d'ouverture à venir ou la date limite passée, et deux liens : **Suivre mon dossier** et **Voir les dates d'admission** (fiche MPC). Le formulaire ne s'affiche pas.
2. **Un brouillon déjà commencé** reste affiché ; si la date limite passe avant l'envoi, la soumission est refusée avec le message « Les candidatures sont fermées : la date limite de dépôt est passée. »
3. **Après la date limite**, le suivi d'un dossier envoyé et le remplacement d'une pièce refusée restent possibles : un candidat qui a envoyé à temps doit pouvoir corriger.
4. **Sans calendrier enregistré**, les candidatures restent ouvertes (comportement d'avant US-028).

## 2. Règles métier et contraintes fonctionnelles

1. **Accès totalement anonyme et libre** :
   - Aucune création de compte ou saisie de mot de passe n'est exigée pour consulter les fiches et pièces requises.
2. **Admission unique** :
   - La candidature vise toujours le Premier cycle MPC. Aucun champ ou paramètre « cursus » n'est collecté ni transmis (`/postuler` sans `?cursus=`).
3. **Pièces requises d'admission** (liste unique, toutes obligatoires) :
   1. Acte de naissance ou extrait d'archives.
   2. Certificat de fin d'études secondaires (Bac II).
   3. Relevé de notes officiel.
   4. Deux photos d'identité récentes.
   5. Pièce d'identité (CIN).
   - Ne sont **pas** demandés : certificat de bonne vie et mœurs, certificat médical.
   - Formats : PDF ou JPG, 5 Mo maximum par fichier.
4. **Données officielles de référence** :
   - Les programmes affichés proviennent de `cursus/*.json`. Les pièces requises sont définies côté backend, pas dans ces fichiers.
5. **Résilience et cas d'erreur** :
   - Si un visiteur tente d'accéder à un cursus inexistant (ex. `/cursus/invalide`), une page d'erreur 404 conviviale avec un message clair et un bouton de redirection vers l'accueil est affichée.
6. **Adaptabilité mobile** :
   - L'ensemble des tableaux, listes de pièces et grilles est lisible sur écran mobile dès 360 px de largeur (smartphones Android standard en Haïti).
7. **Adresse de la Faculté** :
   - L'adresse à afficher est **Delmas 33** (confirmé le 2026-10-31). L'ancienne mention « Rue Monseigneur Guilloux, Port-au-Prince » est obsolète.
8. **Durée du parcours** :
   - MPC : 2 ans ; branches : 3 ans ; total : 5 ans. Les fichiers JSON font foi pour la durée de chaque cycle (l'ancienne mention « 10 semestres » est supprimée).

---

## 3. Maquettes de référence

Maquettes de l'ensemble des écrans (mobile et bureau, côté candidat et administration) : « Maquettes FDS Portail » (page privée claude.ai, lien partagé par l'équipe produit). Elles font foi pour la structure des écrans, pas pour les textes marqués entre crochets (à fournir par la Faculté).

---

*ws-func-01-portail-public.md — FDS Portail — Bravetech · GL-EN3-2026*
