"""Routes d'administration — Couche Présentation / API v1.

Toutes les routes de ce routeur exigent un jeton valide (`get_current_admin`) : la protection est posée sur le routeur,
donc une future route ajoutée ici ne peut pas l'oublier.
"""

import logging
from datetime import datetime, timezone
from urllib.parse import quote

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, Response
from pydantic import BaseModel

from backend.api.v1.candidatures import (
    get_candidature_repository,
    get_document_repository,
    get_email_sender,
    get_stockage_fichiers,
    get_url_base_portail,
)
from backend.api.v1.dto.admin_dto import (
    DecisionHistoriqueResponse,
    DecisionRequest,
    DossierAdminResponse,
    LigneCandidatureResponse,
    PageCandidaturesResponse,
    PieceAdminResponse,
    StatistiquesResponse,
)
from backend.api.v1.calendrier import dates_du_calendrier, get_calendrier_repository
from backend.api.v1.dto.calendrier_dto import CalendrierAdminResponse, CalendrierRequest
from backend.api.v1.securite import get_current_admin, get_current_admin_complet, get_utilisateur_repository
from backend.bll.consulter_candidatures import (
    LIMITE_MAX,
    ListerCandidaturesUseCase,
    ObtenirContenuDocumentUseCase,
    ObtenirDossierAdminUseCase,
)
from backend.bll.calendrier_admission import ConsulterCalendrierUseCase, ModifierCalendrierUseCase
from backend.bll.decider_document import DeciderDocumentUseCase
from backend.bll.exporter_candidatures import generer_csv, vers_lignes
from backend.bll.notifier_decision import NotifierDecisionUseCase
from backend.bll.televerser_document import trouver_piece
from backend.bll.obtenir_statut_candidature import (
    STATUT_GLOBAL_ACTION_REQUISE,
    STATUT_GLOBAL_COMPLET,
    STATUT_GLOBAL_EN_EXAMEN,
)
from backend.dal.export_pdf import generer_pdf
from backend.entities.candidature import FRAIS_DOSSIER_HTG
from backend.entities.document_soumis import DocumentSoumis
from backend.entities.erreurs import (
    CandidatureIntrouvable,
    DocumentDejaDecide,
    DocumentIntrouvable,
    InformationsInvalides,
)
from backend.entities.pieces_admission import NOM_ADMISSION
from backend.entities.utilisateur import Utilisateur
from backend.ports.calendrier_repository import ICalendrierRepository
from backend.ports.candidature_repository import ICandidatureRepository
from backend.ports.document_repository import IDocumentRepository
from backend.ports.email_sender import IEmailSender
from backend.ports.stockage_fichiers import IStockageFichiers
from backend.ports.utilisateur_repository import IUtilisateurRepository

_journal = logging.getLogger(__name__)

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


_LIBELLES_FILTRE_STATUT = {"en_examen": "à examiner", "action_requise": "action du candidat", "complet": "complets"}


@router.get(
    "/candidatures/export",
    summary="Exporter la liste filtrée des dossiers (CSV ou PDF)",
    response_class=Response,
    responses={200: {"content": {"text/csv": {}, "application/pdf": {}}}},
)
def exporter_candidatures(
    format: str = Query("csv", pattern="^(csv|pdf)$"),
    q: str | None = Query(None, max_length=100),
    statut: str | None = Query(None, pattern=_STATUTS),
    deplacement_physique: bool | None = Query(None),
    utilisateur: Utilisateur = Depends(get_current_admin),
    repo: ICandidatureRepository = Depends(get_candidature_repository),
    documents: IDocumentRepository = Depends(get_document_repository),
):
    """Télécharge tous les dossiers correspondant aux filtres (pas de pagination), avec les colonnes minimales.

    Sans `statut`, tous les dossiers soumis sont exportés. Ni email, ni téléphone ne sont inclus.
    """
    dossiers = ListerCandidaturesUseCase(repo, documents).filtrer(q, statut, deplacement_physique)
    maintenant = datetime.now(timezone.utc)
    # Trace de l'accès à des données personnelles en masse : qui, quoi, combien (sans aucune donnée personnelle)
    _journal.info("Export %s de %d dossier(s) par l'utilisateur %s.", format, len(dossiers), utilisateur.id)

    nom_fichier = f"candidatures-{maintenant:%Y-%m-%d}.{format}"
    if format == "csv":
        contenu, type_mime = generer_csv(dossiers), "text/csv; charset=utf-8"
    else:
        criteres = [f"statut : {_LIBELLES_FILTRE_STATUT[statut]}"] if statut else []
        if deplacement_physique is not None:
            criteres.append(f"déplacement : {'oui' if deplacement_physique else 'non'}")
        if q and q.strip():
            criteres.append(f"recherche : « {q.strip()} »")
        contenu = generer_pdf(
            "Candidatures — Premier cycle MPC", ", ".join(criteres) or "tous les dossiers soumis", vers_lignes(dossiers), maintenant
        )
        type_mime = "application/pdf"
    return Response(
        content=contenu,
        media_type=type_mime,
        headers={
            "Content-Disposition": f'attachment; filename="{nom_fichier}"',
            "Cache-Control": "private, no-store",
            "X-Content-Type-Options": "nosniff",
        },
    )


@router.get("/candidatures/{reference}", response_model=DossierAdminResponse, summary="Dossier complet d'un candidat")
def obtenir_dossier(
    reference: str,
    repo: ICandidatureRepository = Depends(get_candidature_repository),
    documents: IDocumentRepository = Depends(get_document_repository),
    utilisateurs: IUtilisateurRepository = Depends(get_utilisateur_repository),
):
    try:
        dossier = ObtenirDossierAdminUseCase(repo, documents).executer(reference)
    except CandidatureIntrouvable:
        raise HTTPException(status_code=404, detail="Dossier introuvable.")
    c, cand = dossier.candidat, dossier.candidature
    emails: dict[str, str] = {}
    for decision in dossier.decisions:
        if decision.decide_par not in emails:
            auteur = utilisateurs.obtenir(decision.decide_par)
            emails[decision.decide_par] = auteur.email if auteur else "compte supprimé"
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
        decisions=[
            DecisionHistoriqueResponse(
                piece_id=d.document_requis_id,
                piece_nom=trouver_piece(d.document_requis_id).nom,
                statut=d.statut,
                motif=d.motif,
                decide_par=emails[d.decide_par],
                decide_le=d.decide_le,
            )
            for d in dossier.decisions
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


def _piece_apres_decision(document: DocumentSoumis) -> PieceAdminResponse:
    return PieceAdminResponse(
        id=document.document_requis_id,
        nom=trouver_piece(document.document_requis_id).nom,
        statut=document.statut_validation,
        document_id=document.id,
        nom_fichier=document.nom_fichier,
        type_mime=document.type_mime,
        taille_octets=document.taille_octets,
        depose_le=document.soumis_le,
        motif_rejet=document.motif_rejet,
        valide_par=document.valide_par,
        date_validation=document.date_validation,
    )


@router.put(
    "/documents/{document_id}/statut",
    response_model=PieceAdminResponse,
    summary="Valider ou refuser une pièce (décision définitive, enregistrée avec son auteur)",
)
def decider_document(
    document_id: str,
    payload: DecisionRequest,
    taches: BackgroundTasks,
    utilisateur: Utilisateur = Depends(get_current_admin),
    repo: ICandidatureRepository = Depends(get_candidature_repository),
    documents: IDocumentRepository = Depends(get_document_repository),
    email_sender: IEmailSender = Depends(get_email_sender),
    url_base: str = Depends(get_url_base_portail),
):
    """Enregistre `valide_par` et `date_validation` ; un refus exige un motif, que le candidat verra.

    Une décision ne se modifie pas : 409 si la pièce a déjà été validée ou refusée (jusqu'à son remplacement).
    Le candidat est prévenu par email (non bloquant, voir `NotifierDecisionUseCase`).
    """
    try:
        document, decision = DeciderDocumentUseCase(repo, documents).executer(
            document_id, payload.statut, payload.motif, utilisateur
        )
    except InformationsInvalides as erreur:
        raise HTTPException(status_code=422, detail={"erreurs": erreur.erreurs})
    except DocumentIntrouvable:
        raise HTTPException(status_code=404, detail="Document introuvable.")
    except DocumentDejaDecide:
        raise HTTPException(status_code=409, detail="Cette pièce a déjà fait l'objet d'une décision, qui est définitive.")
    # L'email part APRÈS l'enregistrement, en tâche de fond : son échec ne peut ni annuler la décision ni changer la réponse
    candidat = repo.obtenir_candidat(document.candidat_id)
    candidature = repo.obtenir_par_candidat(document.candidat_id)
    if candidat is not None and candidature is not None:
        taches.add_task(NotifierDecisionUseCase(email_sender, url_base).executer, candidat, candidature, decision)
    return _piece_apres_decision(document)


# --- US-028 : calendrier d'admission ------------------------------------------------------------------

def _calendrier_admin(calendriers: ICalendrierRepository, utilisateurs: IUtilisateurRepository) -> CalendrierAdminResponse:
    calendrier, etat = ConsulterCalendrierUseCase(calendriers).executer()
    if calendrier is None:
        return CalendrierAdminResponse(etat=etat)
    auteur = utilisateurs.obtenir(calendrier.modifie_par)
    return CalendrierAdminResponse(
        etat=etat,
        modifie_par=auteur.email if auteur else None,
        modifie_le=calendrier.modifie_le,
        **dates_du_calendrier(calendrier),
    )


@router.get("/calendrier", response_model=CalendrierAdminResponse, summary="Calendrier d'admission et dernière modification")
def obtenir_calendrier_admin(
    calendriers: ICalendrierRepository = Depends(get_calendrier_repository),
    utilisateurs: IUtilisateurRepository = Depends(get_utilisateur_repository),
):
    return _calendrier_admin(calendriers, utilisateurs)


@router.put(
    "/calendrier",
    response_model=CalendrierAdminResponse,
    summary="Modifier les dates de la session (rôle admin) ; chaque modification est conservée",
)
def modifier_calendrier(
    payload: CalendrierRequest,
    utilisateur: Utilisateur = Depends(get_current_admin_complet),
    calendriers: ICalendrierRepository = Depends(get_calendrier_repository),
    utilisateurs: IUtilisateurRepository = Depends(get_utilisateur_repository),
):
    try:
        ModifierCalendrierUseCase(calendriers).executer(payload.model_dump(), utilisateur)
    except InformationsInvalides as erreur:
        raise HTTPException(status_code=422, detail={"erreurs": erreur.erreurs})
    _journal.info("Calendrier d'admission modifié par %s.", utilisateur.id)
    return _calendrier_admin(calendriers, utilisateurs)
