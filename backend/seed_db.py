"""Script de peuplement initial de la base de données (Seed).

Charge les cursus officiels depuis le dossier `cursus/` dans la base relationnelle.
"""

from backend.dal.cursus_loader import charger_cursus_depuis_disque
from backend.dal.cursus_repository_sql import SQLAlchemyCursusRepository


def seed():
    print("Chargement des cursus officiels depuis cursus/...")
    cursus_liste = charger_cursus_depuis_disque()
    print(f"{len(cursus_liste)} cursus trouvés sur le disque.")

    repo = SQLAlchemyCursusRepository()
    repo.sauvegarder_tous(cursus_liste)
    print("Sauvegarde terminée avec succès en base de données !")

    for c in repo.lister_tous():
        nb_niveaux = len(c.niveaux)
        print(f"  - [{c.id}] {c.nom} ({c.duree_annees} ans, {nb_niveaux} niveaux)")


if __name__ == "__main__":
    seed()
