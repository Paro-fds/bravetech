"""Port de persistance des candidatures — Couche Ports.

Contrat abstrait que tout adaptateur de données (DAL) doit respecter.
"""

from abc import ABC, abstractmethod

from backend.entities.candidat import Candidat
from backend.entities.candidature import Candidature


class ICandidatureRepository(ABC):
    """Interface abstraite d'accès aux candidats et à leurs candidatures."""

    @abstractmethod
    def creer(self, candidat: Candidat, candidature: Candidature) -> None:
        """Persiste un nouveau candidat et sa candidature.

        Lève `CandidatureDejaExistante` si le couple (email, campagne) existe déjà.
        """

    @abstractmethod
    def obtenir_candidature(self, candidature_id: str) -> Candidature | None:
        """Retourne une candidature par son identifiant, ou None."""

    @abstractmethod
    def obtenir_candidat(self, candidat_id: str) -> Candidat | None:
        """Retourne un candidat par son identifiant, ou None."""

    @abstractmethod
    def trouver_candidat_par_email_campagne(self, email: str, campagne: int) -> Candidat | None:
        """Retourne le candidat d'une campagne pour un email donné, ou None."""

    @abstractmethod
    def trouver_par_reference(self, reference: str) -> tuple[Candidat, Candidature] | None:
        """Retourne le candidat et la candidature portant cette référence de dossier `CAN-AAAA-NNNN`, ou None."""

    @abstractmethod
    def lister_soumises(self) -> list[tuple[Candidat, Candidature]]:
        """Retourne tous les dossiers soumis (candidat, candidature), du plus ancien au plus récent."""

    @abstractmethod
    def reference_paiement_existe(self, reference: str) -> bool:
        """Indique si une référence de paiement simulé est déjà attribuée."""

    @abstractmethod
    def prochain_numero_reference(self, campagne: int) -> int:
        """Retourne le prochain numéro séquentiel de référence de dossier pour la campagne (1 si aucun)."""

    @abstractmethod
    def enregistrer_candidat(self, candidat: Candidat) -> None:
        """Met à jour un candidat existant.

        Lève `CandidatureDejaExistante` si le nouvel email entre en conflit sur la campagne.
        """

    @abstractmethod
    def enregistrer_candidature(self, candidature: Candidature) -> None:
        """Met à jour une candidature existante.

        Lève `ReferenceDejaAttribuee` si une référence unique entre en conflit.
        """
