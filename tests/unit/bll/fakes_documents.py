"""Fichiers d'exemple et dépôts factices pour tester le dépôt de pièces (US-007) sans base ni disque.
"""

from copy import deepcopy

# Contenus minimaux ayant les bons octets d'en-tête (magic bytes)
PDF = b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n1 0 obj\n<<>>\nendobj\n%%EOF"
PNG = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR" + b"\x00" * 20
JPG = b"\xff\xd8\xff\xe0\x00\x10JFIF\x00" + b"\x00" * 20
EXE = b"MZ\x90\x00\x03\x00\x00\x00" + b"\x00" * 50  # exécutable Windows


class FakeDocumentRepository:
    """Dépôt en mémoire des documents soumis (upsert sur (candidat, pièce))."""

    def __init__(self) -> None:
        self.documents = {}
        self.decisions = []

    def obtenir(self, candidat_id, document_requis_id):
        return deepcopy(self.documents.get((candidat_id, document_requis_id)))

    def lister(self, candidat_id):
        return [deepcopy(d) for (c, _), d in self.documents.items() if c == candidat_id]

    def obtenir_par_id(self, document_id):
        return next((deepcopy(d) for d in self.documents.values() if d.id == document_id), None)

    def lister_par_candidats(self, candidat_ids):
        return {identifiant: self.lister(identifiant) for identifiant in candidat_ids}

    def enregistrer_decision(self, document, decision):
        from backend.entities.document_soumis import STATUT_EN_ATTENTE
        from backend.entities.erreurs import DocumentDejaDecide

        actuel = self.documents[(document.candidat_id, document.document_requis_id)]
        if actuel.statut_validation != STATUT_EN_ATTENTE:
            raise DocumentDejaDecide()
        self.documents[(document.candidat_id, document.document_requis_id)] = deepcopy(document)
        self.decisions.append(deepcopy(decision))

    def lister_decisions(self, candidat_id):
        return [deepcopy(d) for d in self.decisions if d.candidat_id == candidat_id]

    def enregistrer(self, document):
        self.documents[(document.candidat_id, document.document_requis_id)] = deepcopy(document)


class FakeStockage:
    """Stockage de fichiers en mémoire."""

    def __init__(self) -> None:
        self.fichiers: dict[str, bytes] = {}

    def enregistrer(self, cle, contenu):
        self.fichiers[cle] = contenu

    def lire(self, cle):
        return self.fichiers.get(cle)

    def supprimer(self, cle):
        self.fichiers.pop(cle, None)
