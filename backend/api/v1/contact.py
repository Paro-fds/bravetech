"""Router du formulaire de contact — Couche Présentation / API v1 (US-019).
"""

import os

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from backend.api.v1.candidatures import get_email_sender
from backend.api.v1.limiteur import LimiteurDebit, adresse_client
from backend.bll.contacter_secretariat import ContacterSecretariatUseCase
from backend.entities.erreurs import ContactIndisponible, EnvoiEmailEchoue, InformationsInvalides
from backend.ports.email_sender import IEmailSender
from fastapi import Request

router = APIRouter(prefix="/contact", tags=["Contact"])

# Formulaire public : 3 messages par tranche de 10 minutes et par IP, pour ne pas servir de relais à du courrier indésirable
limiteur_contact = LimiteurDebit(max_requetes=3, fenetre_secondes=600)


def get_email_secretariat() -> str:
    """Adresse qui reçoit les messages du formulaire (`CONTACT_EMAIL`, à fournir par la Faculté)."""
    return os.getenv("CONTACT_EMAIL", "")


class MessageContactRequest(BaseModel):
    nom: str = Field(max_length=200)
    email: str = Field(max_length=255)
    message: str = Field(max_length=5000)
    # Piège à robots : champ invisible pour les visiteurs, rempli par les scripts automatiques
    site_web: str | None = Field(default=None, max_length=200)


class MessageContactResponse(BaseModel):
    envoye: bool


@router.post("", response_model=MessageContactResponse, summary="Écrire au secrétariat")
def contacter_secretariat(
    payload: MessageContactRequest,
    requete: Request,
    email_sender: IEmailSender = Depends(get_email_sender),
    destinataire: str = Depends(get_email_secretariat),
):
    """Valide le message puis l'envoie au secrétariat. Un échec d'envoi renvoie 503 : le visiteur garde son texte."""
    client = adresse_client(requete)
    if limiteur_contact.est_atteint(client):
        raise HTTPException(
            status_code=429,
            detail="Trop de messages envoyés. Patientez quelques minutes puis réessayez.",
            headers={"Retry-After": "600"},
        )
    if payload.site_web:
        return MessageContactResponse(envoye=True)  # robot : on fait comme si, sans rien envoyer
    limiteur_contact.enregistrer(client)
    try:
        ContacterSecretariatUseCase(email_sender, destinataire).executer(payload.model_dump(exclude={"site_web"}))
    except InformationsInvalides as erreur:
        raise HTTPException(status_code=422, detail={"erreurs": erreur.erreurs})
    except (ContactIndisponible, EnvoiEmailEchoue):
        raise HTTPException(
            status_code=503,
            detail="Votre message n'a pas pu être envoyé. Réessayez dans quelques minutes.",
        )
    return MessageContactResponse(envoye=True)
