"""Cas d'utilisation : authentification du personnel — Couche BLL (US-011).

Aucune indication n'est donnée sur la cause d'un échec (email inconnu, mauvais mot de passe, compte désactivé) :
la même erreur est levée, et le même travail de hachage est fait, pour ne pas révéler quels comptes existent.
"""

from backend.entities.erreurs import AccesInterdit, IdentifiantsInvalides, JetonInvalide
from backend.entities.utilisateur import ROLES, Utilisateur
from backend.ports.securite import IEmetteurJeton, IHacheurMotDePasse, JetonEmis
from backend.ports.utilisateur_repository import IUtilisateurRepository


class AuthentifierUtilisateurUseCase:
    def __init__(self, utilisateurs: IUtilisateurRepository, hacheur: IHacheurMotDePasse, emetteur: IEmetteurJeton) -> None:
        self._utilisateurs = utilisateurs
        self._hacheur = hacheur
        self._emetteur = emetteur
        # Empreinte factice : on vérifie quand même un mot de passe si le compte n'existe pas (temps de réponse constant)
        self._empreinte_factice = hacheur.hacher("mot-de-passe-factice")

    def executer(self, email: str, mot_de_passe: str) -> JetonEmis:
        utilisateur = self._utilisateurs.trouver_par_email((email or "").strip().lower())
        empreinte = utilisateur.mot_de_passe_hash if utilisateur else self._empreinte_factice
        correspond = self._hacheur.verifier(mot_de_passe or "", empreinte)
        if utilisateur is None or not correspond or not utilisateur.est_actif:
            raise IdentifiantsInvalides()
        return self._emetteur.emettre(utilisateur)


class ObtenirUtilisateurCourantUseCase:
    """Retrouve l'utilisateur d'un jeton. Le compte est relu à chaque requête : un compte désactivé perd l'accès aussitôt."""

    def __init__(self, utilisateurs: IUtilisateurRepository, emetteur: IEmetteurJeton) -> None:
        self._utilisateurs = utilisateurs
        self._emetteur = emetteur

    def executer(self, jeton: str, roles_autorises: tuple[str, ...] = ROLES) -> Utilisateur:
        revendications = self._emetteur.decoder(jeton)
        utilisateur = self._utilisateurs.obtenir(revendications.utilisateur_id)
        if utilisateur is None or not utilisateur.est_actif:
            raise JetonInvalide()
        # Le rôle fait foi en base, pas dans le jeton : un changement de rôle s'applique immédiatement
        if utilisateur.role not in roles_autorises:
            raise AccesInterdit()
        return utilisateur
