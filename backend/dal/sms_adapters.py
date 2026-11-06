"""Adaptateur SMS simulé — Couche DAL (US-016).

Aucun SMS ne part : le message est enregistré dans `sms_simules`, et le personnel le lit dans l'espace admin
(« SMS (simulation) »). Comme les envois partent en tâche de fond, après la fermeture de la session de la requête,
l'adaptateur ouvre sa propre session à chaque écriture.
"""

import logging
import uuid
from collections.abc import Callable
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from backend.dal.models import SmsSimuleModel
from backend.entities.sms_simule import SmsSimule
from backend.ports.sms_sender import IJournalSms, ISmsSender, MessageSms

logger = logging.getLogger(__name__)


class SmsSimuleSql(ISmsSender, IJournalSms):
    def __init__(self, fabrique_session: Callable[[], Session]) -> None:
        self._fabrique_session = fabrique_session

    def envoyer(self, message: MessageSms) -> None:
        with self._fabrique_session() as session:
            session.add(
                SmsSimuleModel(
                    id=str(uuid.uuid4()),
                    destinataire=message.destinataire,
                    texte=message.texte,
                    reference_dossier=message.reference_dossier,
                    envoye_le=datetime.now(timezone.utc),
                )
            )
            session.commit()
        logger.info("[SMS simulé] dossier %s : %d caractères enregistrés.", message.reference_dossier, len(message.texte))

    def lister(self, limite: int) -> list[SmsSimule]:
        with self._fabrique_session() as session:
            lignes = session.query(SmsSimuleModel).order_by(SmsSimuleModel.envoye_le.desc()).limit(limite).all()
            return [
                SmsSimule(
                    id=l.id,
                    destinataire=l.destinataire,
                    texte=l.texte,
                    reference_dossier=l.reference_dossier,
                    envoye_le=l.envoye_le if l.envoye_le.tzinfo else l.envoye_le.replace(tzinfo=timezone.utc),
                )
                for l in lignes
            ]
