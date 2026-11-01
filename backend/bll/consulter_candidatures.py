"""Cas d'utilisation : consultation des dossiers par le personnel — Couche BLL (US-012).

Lecture seule. Seuls les dossiers soumis sont visibles : un brouillon n'est pas encore un dossier.

Le filtrage et la pagination se font en mémoire sur l'ensemble des dossiers soumis. C'est suffisant pour le volume
attendu d'une campagne d'admission (quelques centaines à quelques milliers de dossiers) et évite de dupliquer en SQL
la règle du statut d'un dossier ; à remplacer par une requête paginée si le volume dépasse largement ce cadre.
"""

import unicodedata
from dataclasses import dataclass

from backend.bll.obtenir_statut_candidature import statut_global_depuis_comptes
from backend.bll.televerser_document import ListerPiecesDossierUseCase, PieceDossier
from backend.entities.candidat import Candidat
from backend.entities.candidature import STATUT_SOUMISE, Candidature
from backend.entities.decision_document import DecisionDocument
from backend.entities.document_soumis import STATUT_EN_ATTENTE, STATUT_REJETE, STATUT_VALIDE, DocumentSoumis
from backend.entities.erreurs import CandidatureIntrouvable, DocumentIntrouvable
from backend.entities.pieces_admission import pieces_admission
from backend.ports.candidature_repository import ICandidatureRepository
from backend.ports.document_repository import IDocumentRepository
from backend.ports.stockage_fichiers import IStockageFichiers

LIMITE_MAX = 100


@dataclass
class LigneCandidature:
    candidat: Candidat
    candidature: Candidature
    pieces_total: int
    pieces_validees: int
    pieces_en_attente: int
    pieces_rejetees: int
    statut_global: str


@dataclass
class Statistiques:
    """Indicateurs sur tous les dossiers soumis (pas seulement la page affichée)."""
    dossiers_soumis: int
    sans_deplacement: int  # dossiers avec deplacement_physique = false
    pieces_a_examiner: int
    pieces_deposees: int
    pieces_refusees: int


@dataclass
class PageCandidatures:
    total: int
    page: int
    limit: int
    items: list[LigneCandidature]
    statistiques: Statistiques


def _normaliser(texte: str) -> str:
    """Minuscules sans accents : « Éloïse » se trouve en tapant « eloise »."""
    decompose = unicodedata.normalize("NFD", texte.casefold())
    return "".join(c for c in decompose if unicodedata.category(c) != "Mn")


class ListerCandidaturesUseCase:
    def __init__(self, candidatures: ICandidatureRepository, documents: IDocumentRepository) -> None:
        self._candidatures = candidatures
        self._documents = documents

    def executer(
        self,
        page: int = 1,
        limit: int = 20,
        recherche: str | None = None,
        statut: str | None = None,
        deplacement_physique: bool | None = None,
    ) -> PageCandidatures:
        page = max(page, 1)
        limit = min(max(limit, 1), LIMITE_MAX)
        lignes = self._toutes_les_lignes()
        statistiques = Statistiques(
            dossiers_soumis=len(lignes),
            sans_deplacement=sum(1 for l in lignes if l.candidature.deplacement_physique is False),
            pieces_a_examiner=sum(l.pieces_en_attente for l in lignes),
            pieces_deposees=sum(l.pieces_en_attente + l.pieces_validees + l.pieces_rejetees for l in lignes),
            pieces_refusees=sum(l.pieces_rejetees for l in lignes),
        )

        retenues = [l for l in lignes if self._correspond(l, recherche, statut, deplacement_physique)]
        debut = (page - 1) * limit
        return PageCandidatures(
            total=len(retenues), page=page, limit=limit, items=retenues[debut:debut + limit], statistiques=statistiques
        )

    def _toutes_les_lignes(self) -> list[LigneCandidature]:
        total_pieces = len(pieces_admission())
        soumises = self._candidatures.lister_soumises()
        documents = self._documents.lister_par_candidats([candidat.id for candidat, _ in soumises])

        lignes: list[LigneCandidature] = []
        for candidat, candidature in soumises:
            statuts = [d.statut_validation for d in documents.get(candidat.id, [])]
            validees, rejetees = statuts.count(STATUT_VALIDE), statuts.count(STATUT_REJETE)
            lignes.append(LigneCandidature(
                candidat=candidat,
                candidature=candidature,
                pieces_total=total_pieces,
                pieces_validees=validees,
                pieces_en_attente=statuts.count(STATUT_EN_ATTENTE),
                pieces_rejetees=rejetees,
                statut_global=statut_global_depuis_comptes(validees, rejetees, total_pieces),
            ))
        return lignes

    def filtrer(
        self,
        recherche: str | None = None,
        statut: str | None = None,
        deplacement_physique: bool | None = None,
    ) -> list[LigneCandidature]:
        """Tous les dossiers correspondant aux critères, sans pagination (export)."""
        return [
            l for l in self._toutes_les_lignes() if self._correspond(l, recherche, statut, deplacement_physique)
        ]

    @staticmethod
    def _correspond(ligne: LigneCandidature, recherche: str | None, statut: str | None, deplacement: bool | None) -> bool:
        if statut and ligne.statut_global != statut:
            return False
        if deplacement is not None and ligne.candidature.deplacement_physique is not deplacement:
            return False
        if recherche and recherche.strip():
            requete = _normaliser(recherche.strip())
            c = ligne.candidat
            cibles = (
                _normaliser(ligne.candidature.reference_dossier or ""),
                _normaliser(f"{c.prenom} {c.nom}"),
                _normaliser(f"{c.nom} {c.prenom}"),
            )
            if not any(requete in cible for cible in cibles):
                return False
        return True


@dataclass
class DossierAdmin:
    candidat: Candidat
    candidature: Candidature
    pieces: list[PieceDossier]
    statut_global: str
    decisions: list[DecisionDocument]


class ObtenirDossierAdminUseCase:
    def __init__(self, candidatures: ICandidatureRepository, documents: IDocumentRepository) -> None:
        self._candidatures = candidatures
        self._documents = documents

    def executer(self, reference: str) -> DossierAdmin:
        trouve = self._candidatures.trouver_par_reference((reference or "").strip().upper())
        if trouve is None or trouve[1].statut != STATUT_SOUMISE:
            raise CandidatureIntrouvable()
        candidat, candidature = trouve
        pieces = ListerPiecesDossierUseCase(self._candidatures, self._documents).executer(candidature.id)
        return DossierAdmin(
            candidat=candidat,
            candidature=candidature,
            pieces=pieces,
            decisions=self._documents.lister_decisions(candidat.id),
            statut_global=statut_global_depuis_comptes(
                sum(1 for p in pieces if p.statut == STATUT_VALIDE),
                sum(1 for p in pieces if p.statut == STATUT_REJETE),
                len(pieces),
            ),
        )


class ObtenirContenuDocumentUseCase:
    """Relit un fichier déposé, pour l'afficher au personnel (jamais d'URL de stockage exposée)."""

    def __init__(self, documents: IDocumentRepository, stockage: IStockageFichiers) -> None:
        self._documents = documents
        self._stockage = stockage

    def executer(self, document_id: str) -> tuple[DocumentSoumis, bytes]:
        document = self._documents.obtenir_par_id(document_id)
        contenu = self._stockage.lire(document.cle_stockage) if document else None
        if document is None or contenu is None:
            raise DocumentIntrouvable()
        return document, contenu
