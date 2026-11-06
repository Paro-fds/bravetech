"""Crée le premier compte administrateur (US-011).

Usage (une seule fois, au déploiement) :
    docker compose exec backend python -m backend.scripts.seed_admin

Variables d'environnement : `ADMIN_SEED_EMAIL` et `ADMIN_SEED_PASSWORD` (12 caractères minimum). Le mot de passe
n'est jamais écrit dans le dépôt ni affiché. Relancer le script ne change rien si le compte existe déjà.
"""

import os
import sys
import uuid

from backend.dal.database import SessionLocal, engine
from backend.dal.schema import mettre_a_jour_schema
from backend.dal.securite import HacheurBcrypt
from backend.dal.utilisateur_repository_sql import SqlUtilisateurRepository
from backend.entities.utilisateur import LONGUEUR_MIN_MOT_DE_PASSE, ROLE_ADMIN, Utilisateur


def creer_admin(email: str, mot_de_passe: str, depot: SqlUtilisateurRepository) -> bool:
    """Crée le compte admin ; retourne False s'il existe déjà. Lève ValueError si les valeurs sont inacceptables."""
    email = email.strip().lower()
    if "@" not in email:
        raise ValueError("ADMIN_SEED_EMAIL doit être une adresse email.")
    if len(mot_de_passe) < LONGUEUR_MIN_MOT_DE_PASSE:
        raise ValueError(f"ADMIN_SEED_PASSWORD doit contenir au moins {LONGUEUR_MIN_MOT_DE_PASSE} caractères.")
    if depot.trouver_par_email(email) is not None:
        return False
    depot.creer(Utilisateur(
        id=str(uuid.uuid4()),
        email=email,
        mot_de_passe_hash=HacheurBcrypt().hacher(mot_de_passe),
        role=ROLE_ADMIN,
    ))
    return True


def main() -> int:
    email = os.getenv("ADMIN_SEED_EMAIL", "")
    mot_de_passe = os.getenv("ADMIN_SEED_PASSWORD", "")
    if not email or not mot_de_passe:
        print("ADMIN_SEED_EMAIL et ADMIN_SEED_PASSWORD doivent être définis.", file=sys.stderr)
        return 1
    mettre_a_jour_schema(engine)  # sans effet si le conteneur a déjà migré la base
    with SessionLocal() as session:
        try:
            cree = creer_admin(email, mot_de_passe, SqlUtilisateurRepository(session))
        except ValueError as erreur:
            print(str(erreur), file=sys.stderr)
            return 1
    print("Compte administrateur créé." if cree else "Le compte administrateur existe déjà : rien à faire.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
