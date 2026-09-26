"""Router des cursus — Couche Présentation / API v1.
"""

from fastapi import APIRouter, HTTPException, Depends
from backend.bll.lister_cursus import ListerCursusUseCase
from backend.bll.obtenir_cursus_detail import ObtenirCursusDetailUseCase
from backend.dal.cursus_repository_sql import SQLAlchemyCursusRepository
from backend.ports.cursus_repository import ICursusRepository
from backend.api.v1.dto.cursus_dto import CursusListItemResponse, CursusDetailResponse

router = APIRouter(prefix="/cursus", tags=["Cursus & Formations"])


def get_cursus_repository() -> ICursusRepository:
    """Fournisseur de dépendance pour le repository des cursus."""
    return SQLAlchemyCursusRepository()


@router.get("", response_model=list[CursusListItemResponse], summary="Lister les cursus disponibles")
def lister_cursus(repo: ICursusRepository = Depends(get_cursus_repository)):
    """Retourne la liste complète des cursus proposés par la Faculté des Sciences."""
    use_case = ListerCursusUseCase(repository=repo)
    resultats = use_case.executer()
    return resultats


@router.get("/{cursus_id}", response_model=CursusDetailResponse, summary="Obtenir les détails d'un cursus")
def obtenir_cursus(cursus_id: str, repo: ICursusRepository = Depends(get_cursus_repository)):
    """Retourne la fiche détaillée d'un cursus, avec les cours par niveau et les pièces justificatives requises."""
    use_case = ObtenirCursusDetailUseCase(repository=repo)
    cursus = use_case.executer(cursus_id)
    if not cursus:
        raise HTTPException(status_code=404, detail=f"Cursus '{cursus_id}' introuvable.")
    return cursus
