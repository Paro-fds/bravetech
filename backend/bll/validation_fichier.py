"""Validation des fichiers téléversés — Couche BLL (US-007).

Le serveur ne fait jamais confiance au client : taille, extension ET octets d'en-tête (magic bytes) sont
vérifiés avant tout stockage, pour refuser un exécutable renommé en PDF ou en JPG (PRD §7, NFR).
"""

from dataclasses import dataclass

import filetype

from backend.entities.erreurs import FichierInvalide, FichierTropVolumineux

OCTETS_PAR_MO = 1024 * 1024

# Extension -> type MIME attendu pour un contenu réellement de ce format
_MIME_PAR_EXTENSION = {
    "pdf": "application/pdf",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
}

# Libellé de format (champ `format_accepte` d'une pièce) -> extensions correspondantes
_EXTENSIONS_PAR_FORMAT = {
    "PDF": {"pdf"},
    "JPG": {"jpg", "jpeg"},
    "JPEG": {"jpg", "jpeg"},
    "PNG": {"png"},
}


@dataclass(frozen=True)
class FichierValide:
    """Résultat d'une validation réussie : extension normalisée et type MIME réel."""
    extension: str
    type_mime: str


def extensions_acceptees(format_accepte: str) -> set[str]:
    """Convertit « PDF, JPG, PNG » en ensemble d'extensions autorisées."""
    extensions: set[str] = set()
    for libelle in format_accepte.replace("/", ",").split(","):
        extensions |= _EXTENSIONS_PAR_FORMAT.get(libelle.strip().upper(), set())
    return extensions


def nettoyer_nom_fichier(nom: str | None) -> str:
    """Retourne un nom d'affichage sûr : sans chemin, sans caractères de contrôle, 255 caractères au plus."""
    base = (nom or "").replace("\\", "/").rsplit("/", 1)[-1]
    propre = "".join(c for c in base if c.isprintable()).strip()
    return propre[:255] or "document"


def valider_fichier(nom_fichier: str | None, contenu: bytes, format_accepte: str, taille_max_mo: int) -> FichierValide:
    """Valide un fichier téléversé ou lève `FichierInvalide` / `FichierTropVolumineux`."""
    if len(contenu) == 0:
        raise FichierInvalide("Le fichier est vide.")
    if len(contenu) > taille_max_mo * OCTETS_PAR_MO:
        raise FichierTropVolumineux(taille_max_mo)

    nom = nettoyer_nom_fichier(nom_fichier)
    extension = nom.rsplit(".", 1)[-1].lower() if "." in nom else ""
    if extension not in extensions_acceptees(format_accepte):
        raise FichierInvalide(f"Format non accepté. Formats acceptés : {format_accepte}.")

    # Contrôle du contenu réel, indépendamment de l'extension déclarée
    detecte = filetype.guess(contenu)
    if detecte is None or detecte.mime not in _MIME_PAR_EXTENSION.values():
        raise FichierInvalide("Le contenu du fichier n'est pas un PDF, un JPG ou un PNG valide.")
    if detecte.mime != _MIME_PAR_EXTENSION[extension]:
        raise FichierInvalide("L'extension du fichier ne correspond pas à son contenu.")

    return FichierValide(extension=extension, type_mime=detecte.mime)
