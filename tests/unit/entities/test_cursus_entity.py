"""Tests unitaires pour l'entité Cursus (Couche Domain).
"""

from backend.entities.cursus import Cursus, Matiere


def test_creation_cursus():
    cursus = Cursus(
        id="mpc",
        nom="MPC",
        duree_annees=2,
        description_courte="Tronc commun",
        description_longue="Description longue",
        date_ouverture_inscription="2026-08-01",
        date_fermeture_inscription="2026-10-31",
        est_ouvert=True,
    )
    assert cursus.id == "mpc"
    assert cursus.duree_annees == 2
    assert cursus.est_ouvert is True
    assert isinstance(cursus.niveaux, dict)


def test_creation_matiere():
    matiere = Matiere(
        item=1,
        titre="Analyse",
        code="AN01",
        heures=60,
    )
    assert matiere.item == 1
    assert matiere.titre == "Analyse"
    assert matiere.code == "AN01"
