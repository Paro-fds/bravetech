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


class DocumentRequisInconnu(ErreurMetier):
    """La pièce demandée ne fait pas partie des pièces requises d'admission."""


class FichierInvalide(ErreurMetier):
    """Le fichier est refusé (vide, format non accepté, contenu ne correspondant pas à son extension)."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class FichierTropVolumineux(ErreurMetier):
    """Le fichier dépasse la taille maximale autorisée."""

    def __init__(self, taille_max_mo: int) -> None:
        super().__init__(f"Le fichier dépasse la limite de {taille_max_mo} Mo.")
        self.taille_max_mo = taille_max_mo


class DocumentDejaValide(ErreurMetier):
    """Le document a déjà été validé par un administrateur : il ne peut plus être remplacé."""


class EtapePrecedenteIncomplete(ErreurMetier):
    """Une étape antérieure du tunnel de candidature n'est pas terminée."""


class CandidatureDejaSoumise(ErreurMetier):
    """La candidature est déjà soumise : ses informations ne sont plus modifiables."""
