"""Dépôt factice en mémoire pour tester les cas d'utilisation sans base de données.
"""

from copy import deepcopy

from backend.entities.candidat import Candidat
from backend.entities.candidature import Candidature
from backend.entities.erreurs import CandidatureDejaExistante
from backend.ports.candidature_repository import ICandidatureRepository


class FakeCandidatureRepository(ICandidatureRepository):
    def __init__(self) -> None:
        self.candidats: dict[str, Candidat] = {}
        self.candidatures: dict[str, Candidature] = {}

    def creer(self, candidat: Candidat, candidature: Candidature) -> None:
        if self.trouver_candidat_par_email_campagne(candidat.email, candidat.campagne):
            raise CandidatureDejaExistante()
        self.candidats[candidat.id] = deepcopy(candidat)
        self.candidatures[candidature.id] = deepcopy(candidature)

    def obtenir_candidature(self, candidature_id: str) -> Candidature | None:
        return deepcopy(self.candidatures.get(candidature_id))

    def obtenir_candidat(self, candidat_id: str) -> Candidat | None:
        return deepcopy(self.candidats.get(candidat_id))

    def trouver_candidat_par_email_campagne(self, email: str, campagne: int) -> Candidat | None:
        for candidat in self.candidats.values():
            if candidat.email == email and candidat.campagne == campagne:
                return deepcopy(candidat)
        return None

    def reference_paiement_existe(self, reference: str) -> bool:
        return any(c.reference_paiement == reference for c in self.candidatures.values())

    def prochain_numero_reference(self, campagne: int) -> int:
        prefixe = f"CAN-{campagne}-"
        numeros = [
            int(c.reference_dossier[len(prefixe):])
            for c in self.candidatures.values()
            if c.reference_dossier and c.reference_dossier.startswith(prefixe)
        ]
        return max(numeros, default=0) + 1

    def enregistrer_candidat(self, candidat: Candidat) -> None:
        self.candidats[candidat.id] = deepcopy(candidat)

    def enregistrer_candidature(self, candidature: Candidature) -> None:
        self.candidatures[candidature.id] = deepcopy(candidature)


def donnees_valides(**surcharges):
    """Saisie valide de l'étape 1, modifiable champ par champ."""
    from datetime import date

    donnees = {
        "nom": "Louis",
        "prenom": "Louismy",
        "date_naissance": date(2008, 5, 14),
        "sexe": "M",
        "telephone": "37 12 34 56",
        "email": "Louismy@Exemple.com",
        "departement": "Ouest",
        "commune": "Pétion-Ville",
    }
    donnees.update(surcharges)
    return donnees
