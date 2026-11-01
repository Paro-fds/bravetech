"""Stockage de fichiers sur volume local — Couche DAL (adaptateur de IStockageFichiers).

Les fichiers vivent sous un volume persistant (Docker sur la VM Proxmox, ADR-006). L'adaptateur Cloudinary
reste une option future : le port permet d'en changer sans toucher au métier.
"""

import os
import re
from pathlib import Path

from backend.ports.stockage_fichiers import IStockageFichiers

RACINE_UPLOADS_PAR_DEFAUT = Path(__file__).resolve().parents[2] / "uploads"

# Clés générées côté serveur (`<candidature>/<piece>-<uuid>.<ext>`) : on refuse tout autre caractère
_CLE_VALIDE = re.compile(r"[A-Za-z0-9_\-]+(?:/[A-Za-z0-9_\-.]+)*")


def racine_uploads() -> Path:
    """Dossier racine des fichiers téléversés (variable d'environnement `UPLOAD_DIR`)."""
    return Path(os.getenv("UPLOAD_DIR", str(RACINE_UPLOADS_PAR_DEFAUT)))


class StockageLocal(IStockageFichiers):
    """Enregistre les fichiers dans un dossier local, en refusant toute sortie de ce dossier."""

    def __init__(self, racine: Path) -> None:
        self._racine = racine.resolve()

    def _chemin(self, cle: str) -> Path:
        if not _CLE_VALIDE.fullmatch(cle) or ".." in cle:
            raise ValueError("Clé de stockage invalide.")
        chemin = (self._racine / cle).resolve()
        if self._racine not in chemin.parents:
            raise ValueError("Clé de stockage hors du dossier autorisé.")
        return chemin

    def enregistrer(self, cle: str, contenu: bytes) -> None:
        chemin = self._chemin(cle)
        chemin.parent.mkdir(parents=True, exist_ok=True)
        chemin.write_bytes(contenu)

    def lire(self, cle: str) -> bytes | None:
        chemin = self._chemin(cle)
        return chemin.read_bytes() if chemin.is_file() else None

    def supprimer(self, cle: str) -> None:
        chemin = self._chemin(cle)
        if chemin.is_file():
            chemin.unlink()
