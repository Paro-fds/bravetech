"""Santé du portail — Couche Présentation / API v1 (US-026).

Interrogée par le script de déploiement après chaque mise à jour : passe par Nginx et touche PostgreSQL.
Si elle ne répond pas 200, le déploiement revient à la version précédente.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from backend.dal.database import get_db

router = APIRouter(prefix="/sante", tags=["Santé & Info"])


@router.get("", summary="Le portail et sa base répondent")
def sante(db: Session = Depends(get_db)) -> dict[str, str]:
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        # Jamais de détail de l'erreur ici : la route est publique
        raise HTTPException(status_code=503, detail="Base de données injoignable.")
    return {"statut": "ok"}
