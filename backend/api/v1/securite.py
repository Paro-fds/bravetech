"""Dépendances de sécurité de l'API — Couche Présentation (US-011).

`get_current_admin` protège toute route `/admin/` : il est appliqué au routeur entier, jamais seulement à la connexion
(AGENTS.md, fait critique 7). La session se transmet par l'en-tête `Authorization: Bearer <jeton>`.
"""

import logging

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from backend.api.v1.limiteur import LimiteurDebit
from backend.bll.authentification import ObtenirUtilisateurCourantUseCase
from backend.dal.database import get_db
from backend.dal.securite import HacheurBcrypt, SecretJwtManquant, creer_emetteur_jeton
from backend.dal.utilisateur_repository_sql import SqlUtilisateurRepository
from backend.entities.erreurs import AccesInterdit, JetonInvalide
from backend.entities.utilisateur import ROLE_ADMIN, ROLES, Utilisateur
from backend.ports.securite import IEmetteurJeton, IHacheurMotDePasse
from backend.ports.utilisateur_repository import IUtilisateurRepository

_journal = logging.getLogger(__name__)

# Anti brute-force (OWASP A07) : 5 échecs par fenêtre de 60 s et par IP
limiteur_connexion = LimiteurDebit(max_requetes=5)

_schema_bearer = HTTPBearer(auto_error=False)


def get_utilisateur_repository(db: Session = Depends(get_db)) -> IUtilisateurRepository:
    return SqlUtilisateurRepository(db)


def get_hacheur() -> IHacheurMotDePasse:
    return HacheurBcrypt()


def get_emetteur_jeton() -> IEmetteurJeton:
    try:
        return creer_emetteur_jeton()
    except SecretJwtManquant:
        _journal.error("JWT_SECRET absent ou trop court (32 caractères minimum) : connexion du personnel désactivée.")
        raise HTTPException(status_code=503, detail="Connexion du personnel indisponible.")


def _exiger(roles: tuple[str, ...]):
    def dependance(
        identifiants: HTTPAuthorizationCredentials | None = Depends(_schema_bearer),
        utilisateurs: IUtilisateurRepository = Depends(get_utilisateur_repository),
        emetteur: IEmetteurJeton = Depends(get_emetteur_jeton),
    ) -> Utilisateur:
        entete = {"WWW-Authenticate": "Bearer"}
        if identifiants is None:
            raise HTTPException(status_code=401, detail="Authentification requise.", headers=entete)
        try:
            return ObtenirUtilisateurCourantUseCase(utilisateurs, emetteur).executer(identifiants.credentials, roles)
        except JetonInvalide:
            raise HTTPException(status_code=401, detail="Session invalide ou expirée.", headers=entete)
        except AccesInterdit:
            raise HTTPException(status_code=403, detail="Droits insuffisants pour cette action.")

    return dependance


# Tout membre du personnel (admin ou agent)
get_current_admin = _exiger(ROLES)
# Réservé au rôle admin (gestion des comptes, etc.)
get_current_admin_complet = _exiger((ROLE_ADMIN,))
