"""Cas d'utilisation : gestion des comptes du personnel — Couche BLL.

Réservé au rôle `admin`. Aucun compte n'est jamais supprimé afin de conserver l'intégrité
de l'audit des décisions (`decisions_documents`) et du calendrier (`calendriers_admission`) :
un accès retiré passe simplement à `est_actif=False`.

Garde-fous contre le blocage du portail :
- Un administrateur ne peut ni se désactiver ni se retirer le rôle `admin` lui-même.
- Le dernier administrateur actif ne peut être ni désactivé ni rétrogradé en `agent`.
"""

import re
import uuid

from backend.entities.erreurs import (
    ActionSurSoiInterdite,
    DernierAdministrateurActif,
    InformationsInvalides,
    UtilisateurDejaExistant,
    UtilisateurIntrouvable,
)
from backend.entities.utilisateur import LONGUEUR_MIN_MOT_DE_PASSE, ROLE_ADMIN, ROLES, Utilisateur
from backend.ports.securite import IHacheurMotDePasse
from backend.ports.utilisateur_repository import IUtilisateurRepository

_RE_EMAIL = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")


def _verifier_email(email: str, erreurs: dict[str, str]) -> str:
    propre = (email or "").strip().lower()
    if not propre:
        erreurs["email"] = "Adresse email obligatoire."
    elif len(propre) > 255 or not _RE_EMAIL.fullmatch(propre):
        erreurs["email"] = "Adresse email invalide."
    return propre


def _verifier_mot_de_passe(mot_de_passe: str, erreurs: dict[str, str]) -> str:
    texte = mot_de_passe or ""
    if len(texte) < LONGUEUR_MIN_MOT_DE_PASSE:
        erreurs["mot_de_passe"] = f"Le mot de passe doit contenir au moins {LONGUEUR_MIN_MOT_DE_PASSE} caractères."
    return texte


def _verifier_role(role: str, erreurs: dict[str, str]) -> str:
    propre = (role or "").strip()
    if propre not in ROLES:
        erreurs["role"] = "Rôle invalide (choisissez « agent » ou « admin »)."
    return propre


def _obtenir_cible(utilisateurs: IUtilisateurRepository, utilisateur_id: str) -> Utilisateur:
    cible = utilisateurs.obtenir(utilisateur_id)
    if cible is None:
        raise UtilisateurIntrouvable()
    return cible


def _perd_acces_admin_actif(avant: Utilisateur, nouveau_role: str, nouvel_etat_actif: bool) -> bool:
    etait_admin_actif = avant.role == ROLE_ADMIN and avant.est_actif
    reste_admin_actif = nouveau_role == ROLE_ADMIN and nouvel_etat_actif
    return etait_admin_actif and not reste_admin_actif


class ListerUtilisateursUseCase:
    """Retourne la liste complète des comptes du personnel (actifs et désactivés)."""

    def __init__(self, utilisateurs: IUtilisateurRepository) -> None:
        self._utilisateurs = utilisateurs

    def executer(self) -> list[Utilisateur]:
        return self._utilisateurs.lister()


class CreerUtilisateurUseCase:
    """Crée un compte `agent` ou `admin` avec un mot de passe provisoire haché."""

    def __init__(self, utilisateurs: IUtilisateurRepository, hacheur: IHacheurMotDePasse) -> None:
        self._utilisateurs = utilisateurs
        self._hacheur = hacheur

    def executer(self, email: str, mot_de_passe: str, role: str) -> Utilisateur:
        erreurs: dict[str, str] = {}
        email_propre = _verifier_email(email, erreurs)
        mdp_propre = _verifier_mot_de_passe(mot_de_passe, erreurs)
        role_propre = _verifier_role(role, erreurs)
        if erreurs:
            raise InformationsInvalides(erreurs)

        if self._utilisateurs.trouver_par_email(email_propre) is not None:
            raise UtilisateurDejaExistant()

        utilisateur = Utilisateur(
            id=str(uuid.uuid4()),
            email=email_propre,
            mot_de_passe_hash=self._hacheur.hacher(mdp_propre),
            role=role_propre,
            est_actif=True,
        )
        self._utilisateurs.creer(utilisateur)
        return utilisateur


class ModifierAccesUtilisateurUseCase:
    """Change le rôle (`agent` / `admin`) et/ou l'état actif d'un compte du personnel."""

    def __init__(self, utilisateurs: IUtilisateurRepository) -> None:
        self._utilisateurs = utilisateurs

    def executer(
        self,
        cible_id: str,
        acteur: Utilisateur,
        role: str | None = None,
        est_actif: bool | None = None,
    ) -> Utilisateur:
        cible = _obtenir_cible(self._utilisateurs, cible_id)
        erreurs: dict[str, str] = {}
        nouveau_role = cible.role if role is None else _verifier_role(role, erreurs)
        if erreurs:
            raise InformationsInvalides(erreurs)
        nouvel_etat = cible.est_actif if est_actif is None else est_actif

        if _perd_acces_admin_actif(cible, nouveau_role, nouvel_etat):
            if cible.id == acteur.id:
                raise ActionSurSoiInterdite()
            if self._utilisateurs.compter_admins_actifs() <= 1:
                raise DernierAdministrateurActif()

        cible.role = nouveau_role
        cible.est_actif = nouvel_etat
        self._utilisateurs.mettre_a_jour(cible)
        return cible


class ReinitialiserMotDePasseUseCase:
    """Remplace le mot de passe d'un compte du personnel par un nouveau mot de passe provisoire."""

    def __init__(self, utilisateurs: IUtilisateurRepository, hacheur: IHacheurMotDePasse) -> None:
        self._utilisateurs = utilisateurs
        self._hacheur = hacheur

    def executer(self, cible_id: str, mot_de_passe: str) -> Utilisateur:
        erreurs: dict[str, str] = {}
        mdp_propre = _verifier_mot_de_passe(mot_de_passe, erreurs)
        if erreurs:
            raise InformationsInvalides(erreurs)

        cible = _obtenir_cible(self._utilisateurs, cible_id)
        cible.mot_de_passe_hash = self._hacheur.hacher(mdp_propre)
        self._utilisateurs.mettre_a_jour(cible)
        return cible

