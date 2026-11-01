"""Router des candidatures — Couche Présentation / API v1 (US-005).

Le candidat n'a pas de compte : son brouillon est identifié par un identifiant UUID non devinable,
conservé par son navigateur pour reprendre le formulaire après une coupure de connexion.
"""

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from backend.api.v1.limiteur import limiter_envois
from backend.api.v1.dto.candidature_dto import (
    BrouillonResponse,
    DeplacementPhysiqueRequest,
    InformationsPersonnellesRequest,
    InformationsPersonnellesResponse,
    PaiementSimuleRequest,
    PieceDossierResponse,
)
from backend.bll.definir_deplacement_physique import DefinirDeplacementPhysiqueUseCase
from backend.bll.enregistrer_informations import EnregistrerInformationsUseCase, MettreAJourInformationsUseCase
from backend.bll.obtenir_brouillon import ObtenirBrouillonUseCase
from backend.bll.simuler_paiement import SimulerPaiementUseCase
from backend.bll.televerser_document import (
    ListerPiecesDossierUseCase,
    PieceDossier,
    TeleverserDocumentUseCase,
    trouver_piece,
)
from backend.dal.candidature_repository_sql import SqlCandidatureRepository
from backend.dal.database import get_db
from backend.dal.document_repository_sql import SqlDocumentRepository
from backend.dal.stockage_local import StockageLocal, racine_uploads
from backend.entities.candidat import Candidat
from backend.entities.candidature import FRAIS_DOSSIER_HTG, Candidature
from backend.entities.erreurs import (
    CandidatureDejaExistante,
    CandidatureDejaSoumise,
    CandidatureIntrouvable,
    DocumentDejaValide,
    DocumentRequisInconnu,
    EtapePrecedenteIncomplete,
    FichierInvalide,
    FichierTropVolumineux,
    InformationsInvalides,
)
from backend.ports.candidature_repository import ICandidatureRepository
from backend.ports.document_repository import IDocumentRepository
from backend.ports.stockage_fichiers import IStockageFichiers
from backend.bll.validation_fichier import OCTETS_PAR_MO

router = APIRouter(prefix="/candidatures", tags=["Candidature"])

_MESSAGE_INTROUVABLE = "Brouillon de candidature introuvable."


def get_candidature_repository(db: Session = Depends(get_db)) -> ICandidatureRepository:
    """Fournisseur de dépendance pour le repository des candidatures (SQLAlchemy)."""
    return SqlCandidatureRepository(db)


def _reponse(candidat: Candidat, candidature: Candidature) -> BrouillonResponse:
    return BrouillonResponse(
        candidature_id=candidature.id,
        statut=candidature.statut,
        deplacement_physique=candidature.deplacement_physique,
        statut_paiement=candidature.statut_paiement,
        methode_paiement=candidature.methode_paiement,
        reference_paiement=candidature.reference_paiement,
        montant_htg=FRAIS_DOSSIER_HTG,
        informations=InformationsPersonnellesResponse.model_validate(candidat),
    )


def _vers_http(erreur: Exception) -> HTTPException:
    """Traduit une erreur métier en réponse HTTP, sans détail interne."""
    if isinstance(erreur, InformationsInvalides):
        return HTTPException(status_code=422, detail={"erreurs": erreur.erreurs})
    if isinstance(erreur, CandidatureIntrouvable):
        return HTTPException(status_code=404, detail=_MESSAGE_INTROUVABLE)
    if isinstance(erreur, CandidatureDejaExistante):
        return HTTPException(status_code=409, detail="Une candidature existe déjà pour cet email.")
    if isinstance(erreur, DocumentRequisInconnu):
        return HTTPException(status_code=404, detail="Pièce requise inconnue.")
    if isinstance(erreur, FichierTropVolumineux):
        return HTTPException(status_code=413, detail=f"Le fichier dépasse la limite de {erreur.taille_max_mo} Mo.")
    if isinstance(erreur, FichierInvalide):
        return HTTPException(status_code=422, detail={"erreurs": {"fichier": erreur.message}})
    if isinstance(erreur, DocumentDejaValide):
        return HTTPException(status_code=409, detail="Ce document a déjà été validé et ne peut plus être remplacé.")
    if isinstance(erreur, EtapePrecedenteIncomplete):
        return HTTPException(status_code=409, detail="Répondez d'abord aux étapes précédentes de la candidature.")
    if isinstance(erreur, CandidatureDejaSoumise):
        return HTTPException(status_code=409, detail="Cette candidature est déjà soumise et n'est plus modifiable.")
    raise erreur


@router.post("", response_model=BrouillonResponse, status_code=201, summary="Créer un brouillon (étape 1)")
def creer_brouillon(
    payload: InformationsPersonnellesRequest,
    repo: ICandidatureRepository = Depends(get_candidature_repository),
):
    """Valide les informations personnelles et crée le brouillon de candidature."""
    try:
        candidat, candidature = EnregistrerInformationsUseCase(repo).executer(payload.model_dump())
    except (InformationsInvalides, CandidatureDejaExistante) as erreur:
        raise _vers_http(erreur)
    return _reponse(candidat, candidature)


@router.get("/{candidature_id}", response_model=BrouillonResponse, summary="Reprendre un brouillon")
def obtenir_brouillon(
    candidature_id: str,
    repo: ICandidatureRepository = Depends(get_candidature_repository),
):
    """Retourne l'état d'un brouillon pour reprendre le formulaire."""
    try:
        candidat, candidature = ObtenirBrouillonUseCase(repo).executer(candidature_id)
    except CandidatureIntrouvable as erreur:
        raise _vers_http(erreur)
    return _reponse(candidat, candidature)


@router.put("/{candidature_id}/informations", response_model=BrouillonResponse, summary="Modifier l'étape 1")
def modifier_informations(
    candidature_id: str,
    payload: InformationsPersonnellesRequest,
    repo: ICandidatureRepository = Depends(get_candidature_repository),
):
    """Met à jour les informations personnelles d'un brouillon."""
    try:
        candidat, candidature = MettreAJourInformationsUseCase(repo).executer(candidature_id, payload.model_dump())
    except (InformationsInvalides, CandidatureIntrouvable, CandidatureDejaExistante, CandidatureDejaSoumise) as erreur:
        raise _vers_http(erreur)
    return _reponse(candidat, candidature)


@router.put(
    "/{candidature_id}/deplacement-physique",
    response_model=BrouillonResponse,
    summary="Répondre à la question sur le déplacement physique",
)
def definir_deplacement_physique(
    candidature_id: str,
    payload: DeplacementPhysiqueRequest,
    repo: ICandidatureRepository = Depends(get_candidature_repository),
):
    """Enregistre la réponse obligatoire `deplacement_physique`."""
    try:
        candidature = DefinirDeplacementPhysiqueUseCase(repo).executer(candidature_id, payload.deplacement_physique)
        candidat, candidature = ObtenirBrouillonUseCase(repo).executer(candidature.id)
    except (InformationsInvalides, CandidatureIntrouvable, CandidatureDejaSoumise) as erreur:
        raise _vers_http(erreur)
    return _reponse(candidat, candidature)


@router.post(
    "/{candidature_id}/paiement",
    response_model=BrouillonResponse,
    summary="Simuler le paiement des frais de dossier (aucun montant réel prélevé)",
)
def simuler_paiement(
    candidature_id: str,
    payload: PaiementSimuleRequest,
    repo: ICandidatureRepository = Depends(get_candidature_repository),
):
    """Enregistre un paiement SIMULÉ MonCash ou NatCash et attribue la référence `PAY-SIM-AAAA-NNNN`."""
    try:
        candidature = SimulerPaiementUseCase(repo).executer(candidature_id, payload.methode, payload.numero_telephone)
        candidat, candidature = ObtenirBrouillonUseCase(repo).executer(candidature.id)
    except (InformationsInvalides, CandidatureIntrouvable, EtapePrecedenteIncomplete, CandidatureDejaSoumise) as erreur:
        raise _vers_http(erreur)
    return _reponse(candidat, candidature)


# --- US-007 : dépôt des pièces justificatives --------------------------------------------------

def get_document_repository(db: Session = Depends(get_db)) -> IDocumentRepository:
    """Fournisseur de dépendance pour le repository des documents soumis (SQLAlchemy)."""
    return SqlDocumentRepository(db)


def get_stockage_fichiers() -> IStockageFichiers:
    """Fournisseur de dépendance pour le stockage des fichiers (volume local `UPLOAD_DIR`)."""
    return StockageLocal(racine_uploads())


def _reponse_piece(piece_dossier: PieceDossier) -> PieceDossierResponse:
    piece, document = piece_dossier.piece, piece_dossier.document
    return PieceDossierResponse(
        id=piece.id,
        nom=piece.nom,
        description=piece.description,
        format_accepte=piece.format_accepte,
        taille_max_mo=piece.taille_max_mo,
        est_obligatoire=piece.est_obligatoire,
        statut=piece_dossier.statut,
        nom_fichier=document.nom_fichier if document else None,
        taille_octets=document.taille_octets if document else None,
        motif_rejet=document.motif_rejet if document else None,
    )


@router.get(
    "/{candidature_id}/documents",
    response_model=list[PieceDossierResponse],
    summary="Lister les pièces requises et l'état de chaque dépôt",
)
def lister_pieces(
    candidature_id: str,
    repo: ICandidatureRepository = Depends(get_candidature_repository),
    documents: IDocumentRepository = Depends(get_document_repository),
):
    """Retourne les 5 pièces requises avec leur statut (manquant, en_attente, valide, rejete)."""
    try:
        pieces = ListerPiecesDossierUseCase(repo, documents).executer(candidature_id)
    except CandidatureIntrouvable as erreur:
        raise _vers_http(erreur)
    return [_reponse_piece(p) for p in pieces]


@router.post(
    "/{candidature_id}/documents/{document_requis_id}",
    response_model=PieceDossierResponse,
    summary="Téléverser (ou remplacer) une pièce justificative",
    dependencies=[Depends(limiter_envois)],
)
async def televerser_document(
    candidature_id: str,
    document_requis_id: str,
    fichier: UploadFile = File(...),
    repo: ICandidatureRepository = Depends(get_candidature_repository),
    documents: IDocumentRepository = Depends(get_document_repository),
    stockage: IStockageFichiers = Depends(get_stockage_fichiers),
):
    """Valide (taille, extension, octets d'en-tête) puis stocke le fichier ; redéposer remplace le précédent."""
    try:
        piece = trouver_piece(document_requis_id)
        # Lecture bornée : jamais plus que la limite + 1 octet en mémoire, quel que soit ce qu'envoie le client
        contenu = await fichier.read(piece.taille_max_mo * OCTETS_PAR_MO + 1)
        document = TeleverserDocumentUseCase(repo, documents, stockage).executer(
            candidature_id, document_requis_id, fichier.filename, contenu
        )
    except (
        CandidatureIntrouvable,
        CandidatureDejaSoumise,
        DocumentDejaValide,
        DocumentRequisInconnu,
        EtapePrecedenteIncomplete,
        FichierInvalide,
        FichierTropVolumineux,
    ) as erreur:
        raise _vers_http(erreur)
    return _reponse_piece(PieceDossier(piece, document))
