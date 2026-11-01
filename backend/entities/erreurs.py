"""Erreurs métier — Couche Domain.

Exceptions levées par les cas d'utilisation et traduites en réponses HTTP par la couche API.
Règle absolue (Clean Architecture) : aucun import de framework ni de couche externe.
"""


class ErreurMetier(Exception):
    """Classe de base des erreurs métier de FDS Portail."""


class InformationsInvalides(ErreurMetier):
    """Un ou plusieurs champs saisis sont absents ou invalides (champ -> message)."""

    def __init__(self, erreurs: dict[str, str]) -> None:
        super().__init__("Informations invalides.")
        self.erreurs = erreurs


class CandidatureIntrouvable(ErreurMetier):
    """Aucune candidature ne correspond à l'identifiant demandé."""


class CandidatureDejaExistante(ErreurMetier):
    """Une candidature existe déjà pour cet email et cette campagne (unicité (email, campagne))."""


class CandidatureDejaSoumise(ErreurMetier):
    """La candidature est déjà soumise : ses informations ne sont plus modifiables."""
