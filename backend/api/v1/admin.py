"""Routes d'administration — Couche Présentation / API v1.

Toutes les routes de ce routeur exigent un jeton valide (`get_current_admin`) : la protection est posée sur le routeur,
donc une future route ajoutée ici ne peut pas l'oublier.
"""

from urllib.parse import quote

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from pydantic import BaseModel

from backend.api.v1.candidatures import get_candidature_repository, get_document_repository, get_stockage_fichiers
from backend.api.v1.dto.admin_dto import (
    DossierAdminResponse,
    LigneCandidatureResponse,
    PageCandidaturesResponse,
    PieceAdminResponse,
    StatistiquesResponse,
)
from backend.api.v1.securite import get_current_admin
from backend.bll.consulter_candidatures import (
    LIMITE_MAX,
    ListerCandidaturesUseCase,
    ObtenirContenuDocumentUseCase,
    ObtenirDossierAdminUseCase,
)
from backend.bll.obtenir_statut_candidature import (
    STATUT_GLOBAL_ACTION_REQUISE,
    STATUT_GLOBAL_COMPLET,
    STATUT_GLOBAL_EN_EXAMEN,
)
from backend.entities.candidature import FRAIS_DOSSIER_HTG
from backend.entities.erreurs import CandidatureIntrouvable, DocumentIntrouvable
from backend.entities.pieces_admission import NOM_ADMISSION
from backend.entities.utilisateur import Utilisateur
from backend.ports.candidature_repository import ICandidatureRepository
from backend.ports.document_repository import IDocumentRepository
from backend.ports.stockage_fichiers import IStockageFichiers

router = APIRouter(prefix="/admin", tags=["Administration"], dependencies=[Depends(get_current_admin)])

_STATUTS = f"^({STATUT_GLOBAL_EN_EXAMEN}|{STATUT_GLOBAL_ACTION_REQUISE}|{STATUT_GLOBAL_COMPLET})$"


class UtilisateurCourantResponse(BaseModel):
    id: str
    email: str
    role: str


@router.get("/moi", response_model=UtilisateurCourantResponse, summary="Compte connecté")
def moi(utilisateur: Utilisateur = Depends(get_current_admin)):
    return UtilisateurCourantResponse(id=utilisateur.id, email=utilisateur.email, role=utilisateur.role)


@router.get("/candidatures", response_model=PageCandidaturesResponse, summary="Liste paginée des dossiers soumis")
def lister_candidatures(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=LIMITE_MAX),
    q: str | None = Query(None, max_length=100, description="Référence ou nom du candidat"),
    statut: str | None = Query(None, pattern=_STATUTS),
    deplacement_physique: bool | None = Query(None),
    repo: ICandidatureRepository = Depends(get_candidature_repository),
    documents: IDocumentRepository = Depends(get_document_repository),
):
    resultat = ListerCandidaturesUseCase(repo, documents).executer(page, limit, q, statut, deplacement_physique)
    return PageCandidaturesResponse(
        total=resultat.total,
        page=resultat.page,
        limit=resultat.limit,
        statistiques=StatistiquesResponse(**vars(resultat.statistiques)),
        items=[
            LigneCandidatureResponse(
                reference_dossier=l.candidature.reference_dossier,
                nom=l.candidat.nom,
                prenom=l.candidat.prenom,
                statut_paiement=l.candidature.statut_paiement,
                deplacement_physique=l.candidature.deplacement_physique,
                soumise_le=l.candidature.soumise_le,
                created_at=l.candidature.created_at,
                statut=l.statut_global,
                pieces_total=l.pieces_total,
                pieces_validees=l.pieces_validees,
                pieces_en_attente=l.pieces_en_attente,
                pieces_rejetees=l.pieces_rejetees,
            )
            for l in resultat.items
        ],
    )


@router.get("/candidatures/{reference}", response_model=DossierAdminResponse, summary="Dossier complet d'un candidat")
def obtenir_dossier(
    reference: str,
    repo: ICandidatureRepository = Depends(get_candidature_repository),
    documents: IDocumentRepository = Depends(get_document_repository),
):
    try:
        dossier = ObtenirDossierAdminUseCase(repo, documents).executer(reference)
    except CandidatureIntrouvable:
        raise HTTPException(status_code=404, detail="Dossier introuvable.")
    c, cand = dossier.candidat, dossier.candidature
    return DossierAdminResponse(
        reference_dossier=cand.reference_dossier,
        statut=dossier.statut_global,
        admission=NOM_ADMISSION,
        soumise_le=cand.soumise_le,
        nom=c.nom,
        prenom=c.prenom,
        sexe=c.sexe,
        date_naissance=c.date_naissance,
        email=c.email,
        telephone=c.telephone,
        departement=c.departement,
        commune=c.commune,
        deplacement_physique=cand.deplacement_physique,
        statut_paiement=cand.statut_paiement,
        methode_paiement=cand.methode_paiement,
        reference_paiement=cand.reference_paiement,
        montant_htg=FRAIS_DOSSIER_HTG,
        pieces=[
            PieceAdminResponse(
                id=p.piece.id,
                nom=p.piece.nom,
                statut=p.statut,
                document_id=p.document.id if p.document else None,
                nom_fichier=p.document.nom_fichier if p.document else None,
                type_mime=p.document.type_mime if p.document else None,
                taille_octets=p.document.taille_octets if p.document else None,
                depose_le=p.document.soumis_le if p.document else None,
                motif_rejet=p.document.motif_rejet if p.document else None,
                valide_par=p.document.valide_par if p.document else None,
                date_validation=p.document.date_validation if p.document else None,
            )
            for p in dossier.pieces
        ],
    )


@router.get("/proxy-document/{document_id}", summary="Contenu d'une pièce déposée (accès réservé au personnel)")
def proxy_document(
    document_id: str,
    documents: IDocumentRepository = Depends(get_document_repository),
    stockage: IStockageFichiers = Depends(get_stockage_fichiers),
):
    """Sert le fichier depuis le stockage interne ; l'URL de stockage n'est jamais exposée."""
    try:
        document, contenu = ObtenirContenuDocumentUseCase(documents, stockage).executer(document_id)
    except DocumentIntrouvable:
        raise HTTPException(status_code=404, detail="Document introuvable.")
    return Response(
        content=contenu,
        media_type=document.type_mime,
        headers={
            "Content-Disposition": f"inline; filename*=UTF-8''{quote(document.nom_fichier)}",
            # Un fichier téléversé reste une donnée : aucun script, aucune détection de type, aucun cache partagé
            "X-Content-Type-Options": "nosniff",
            "Content-Security-Policy": "sandbox; default-src 'none'; img-src 'self' data:; style-src 'unsafe-inline'",
            "Cache-Control": "private, no-store",
        },
    )
