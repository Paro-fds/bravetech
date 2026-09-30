---
created: 2026-09-26T15:23:00Z
updated: 2026-09-30T16:04:08Z
workstream: WS-01
---

# Spécification Fonctionnelle — WS-01 Portail Public

**Workstream :** WS-01 Portail public  
**Statut :** ✅ Livré via Epic 1 (US-001, US-002)  
**Public cible :** Candidats, lycéens, grand public (accès sans authentification, optimisé mobile 360px et connexions intermittentes)

---

## 1. Description du comportement utilisateur

Le portail public constitue la vitrine officielle et la première étape du parcours candidat pour la Faculté des Sciences (FDS-UEH). Il permet à tout visiteur de découvrir les filières d'ingénierie et de sciences fondamentales, d'accéder au programme académique et de préparer les pièces requises pour leur dossier d'admission.

### 1.1 Page d'accueil (`/`) — Catalogue des cursus

1. **En-tête institutionnel** :
   - Présentation de la Faculté des Sciences (Université d'État d'Haïti).
   - Accroche informative et bouton d'action direct vers les cursus.
2. **Liste des cursus disponibles** :
   - Grille réactive de cartes présentant chaque département et filière officielle (Génie Civil, Génie Électromécanique, Génie Électronique, Math-Physique-Chimie / MPC, Architecture).
   - Informations résumées par carte : code de filière, titre, description succincte, durée d'études (ex. 5 ans / 10 semestres ou 1 an pour MPC), diplôme délivré (Diplôme d'Ingénieur / Certificat MPC).
   - Interaction : clic sur une carte ou sur le lien « Découvrir le programme » menant à la fiche détaillée (`/cursus/:id`).
3. **Pied de page institutionnel** :
   - Coordonnées officielles de la FDS (Rue Monseigneur Guilloux, Port-au-Prince), horaires de permanence, liens d'information.

### 1.2 Page détaillée d'un cursus (`/cursus/:id`)

1. **Fil d'ariane & En-tête** :
   - Bouton de retour vers la liste complète des cursus.
   - Badge du département, titre officiel de la formation, niveau de diplôme et statut d'admission ouvert.
2. **Présentation académique** :
   - Objectifs de la formation et débouchés professionnels.
   - Durée, nombre de semestres et volume de crédits académiques.
   - Grille semestrielle dépliante listant les unités d'enseignement et matières officielles avec leurs crédits respectifs.
3. **Pièces requises pour l'admission** :
   - Liste officielle des documents requis pour postuler (ex. Acte de naissance / Extrait d'archives, Certificat de fin d'études secondaires / Bac II, Relevé de notes officiel, Deux photos d'identité récentes, Certificat de bonne vie et mœurs, Certificat médical récent).
   - Indicateur clair d'obligation (Obligatoire / Facultatif).
4. **Passerelle vers la candidature** :
   - Appel à l'action bien visible « Déposer ma candidature » redirigeant vers le flux de candidature (`/postuler?cursus={id}`) prévu dans l'Epic 2.

---

## 2. Règles métier et contraintes fonctionnelles

1. **Accès totalement anonyme et libre** :
   - Aucune création de compte ou saisie de mot de passe n'est exigée pour consulter les fiches et pièces requises.
2. **Données officielles de référence** :
   - Les informations affichées proviennent de la source de vérité institutionnelle de la Faculté des Sciences (`cursus/*.json`).
3. **Résilience et cas d'erreur** :
   - Si un visiteur tente d'accéder à un cursus inexistant (ex. `/cursus/invalide`), une page d'erreur 404 conviviale avec un message clair et un bouton de redirection vers l'accueil est affichée.
4. **Adaptabilité mobile** :
   - L'ensemble des tableaux, listes de pièces et grilles est lisible sur écran mobile dès 360 px de largeur (smartphones Android standard en Haïti).

---

*ws-func-01-portail-public.md — FDS Portail — Bravetech · GL-EN3-2026*
