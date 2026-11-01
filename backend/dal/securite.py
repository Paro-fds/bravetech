"""Adaptateurs de sécurité — Couche DAL (US-011) : bcrypt pour les mots de passe, JWT HS256 pour les sessions.

Le secret JWT vient de la variable d'environnement `JWT_SECRET` (32 caractères minimum, soit 256 bits) :
jamais de valeur par défaut, pour qu'un déploiement oublié échoue au lieu de signer avec un secret connu.
"""

import os
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from backend.entities.erreurs import JetonInvalide
from backend.entities.utilisateur import DUREE_SESSION_MINUTES, Utilisateur
from backend.ports.securite import IEmetteurJeton, IHacheurMotDePasse, JetonEmis, RevendicationsJeton

LONGUEUR_MIN_SECRET = 32
_ALGORITHME = "HS256"
_OCTETS_MAX_BCRYPT = 72  # bcrypt ignore (ou refuse) tout au-delà


class SecretJwtManquant(RuntimeError):
    """`JWT_SECRET` absent ou trop court : la connexion du personnel est désactivée."""


class HacheurBcrypt(IHacheurMotDePasse):
    def hacher(self, mot_de_passe: str) -> str:
        octets = mot_de_passe.encode("utf-8")
        if len(octets) > _OCTETS_MAX_BCRYPT:
            raise ValueError(f"Mot de passe trop long ({_OCTETS_MAX_BCRYPT} octets maximum).")
        return bcrypt.hashpw(octets, bcrypt.gensalt()).decode("ascii")

    def verifier(self, mot_de_passe: str, empreinte: str) -> bool:
        octets = mot_de_passe.encode("utf-8")
        if len(octets) > _OCTETS_MAX_BCRYPT:
            return False
        try:
            return bcrypt.checkpw(octets, empreinte.encode("ascii"))
        except ValueError:
            return False  # empreinte illisible


class EmetteurJwt(IEmetteurJeton):
    def __init__(self, secret: str, duree_minutes: int = DUREE_SESSION_MINUTES) -> None:
        if len(secret) < LONGUEUR_MIN_SECRET:
            raise SecretJwtManquant()
        self._secret = secret
        self._duree = timedelta(minutes=duree_minutes)

    def emettre(self, utilisateur: Utilisateur) -> JetonEmis:
        maintenant = datetime.now(timezone.utc)
        charge = {"sub": utilisateur.id, "role": utilisateur.role, "iat": maintenant, "exp": maintenant + self._duree}
        jeton = jwt.encode(charge, self._secret, algorithm=_ALGORITHME)
        return JetonEmis(jeton=jeton, expire_dans_secondes=int(self._duree.total_seconds()))

    def decoder(self, jeton: str) -> RevendicationsJeton:
        try:
            # L'algorithme est imposé : jamais celui annoncé par le jeton (attaque « alg: none »)
            charge = jwt.decode(jeton, self._secret, algorithms=[_ALGORITHME], options={"require": ["exp", "sub"]})
        except jwt.PyJWTError as erreur:
            raise JetonInvalide() from erreur
        return RevendicationsJeton(utilisateur_id=str(charge["sub"]), role=str(charge.get("role", "")))


def creer_emetteur_jeton() -> EmetteurJwt:
    """Construit l'émetteur depuis `JWT_SECRET` ; lève `SecretJwtManquant` s'il est absent ou trop court."""
    return EmetteurJwt(os.getenv("JWT_SECRET", ""))
