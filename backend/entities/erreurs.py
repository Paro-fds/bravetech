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


class DossierIncomplet(ErreurMetier):
    """Le dossier ne peut pas être soumis : des étapes ou des pièces manquent."""

    def __init__(self, manques: list[str]) -> None:
        super().__init__("Dossier incomplet.")
        self.manques = manques


class ReferenceDejaAttribuee(ErreurMetier):
    """Une référence (de dossier ou de paiement) est déjà prise : il faut en tirer une autre."""


class CandidatureDejaSoumise(ErreurMetier):
    """La candidature est déjà soumise : ses informations ne sont plus modifiables."""


class DocumentIntrouvable(ErreurMetier):
    """Aucun document soumis ne correspond à cet identifiant."""


class DocumentDejaDecide(ErreurMetier):
    """Le document a déjà fait l'objet d'une décision : elle est définitive."""


class IdentifiantsInvalides(ErreurMetier):
    """Email ou mot de passe incorrect, ou compte désactivé (jamais précisé à l'appelant)."""


class JetonInvalide(ErreurMetier):
    """Jeton de session absent, falsifié ou expiré."""


class AccesInterdit(ErreurMetier):
    """Utilisateur authentifié mais dont le rôle ne permet pas l'action."""
