"""Contenu des emails transactionnels — Couche BLL.

Messages fonctionnels et factuels (PRD §8). Le HTML échappe toutes les valeurs saisies par le candidat.
"""

from html import escape

from backend.entities.candidat import Candidat
from backend.entities.candidature import FRAIS_DOSSIER_HTG, Candidature
from backend.ports.email_sender import MessageEmail


def message_confirmation(candidat: Candidat, candidature: Candidature, url_suivi: str) -> MessageEmail:
    """Email de confirmation de dépôt : référence officielle et lien de suivi."""
    reference = candidature.reference_dossier or ""
    sujet = f"Confirmation de votre candidature — {reference}"

    texte = (
        f"Bonjour {candidat.prenom},\n\n"
        f"La Faculté des Sciences (UEH) a bien reçu votre dossier de candidature au Premier cycle MPC.\n\n"
        f"Votre référence de dossier : {reference}\n"
        f"Conservez-la : elle vous permet de suivre votre dossier sans compte.\n\n"
        f"Suivre mon dossier : {url_suivi}\n\n"
        f"Le paiement des frais de dossier ({FRAIS_DOSSIER_HTG} HTG) était une simulation : "
        f"aucun argent n'a été prélevé.\n\n"
        f"Faculté des Sciences — Université d'État d'Haïti\n"
    )

    html = (
        f"<p>Bonjour {escape(candidat.prenom)},</p>"
        f"<p>La Faculté des Sciences (UEH) a bien reçu votre dossier de candidature au "
        f"<strong>Premier cycle MPC</strong>.</p>"
        f"<p>Votre référence de dossier : <strong>{escape(reference)}</strong><br>"
        f"Conservez-la : elle vous permet de suivre votre dossier sans compte.</p>"
        f'<p><a href="{escape(url_suivi, quote=True)}">Suivre mon dossier</a></p>'
        f"<p>Le paiement des frais de dossier ({FRAIS_DOSSIER_HTG} HTG) était une simulation : "
        f"aucun argent n'a été prélevé.</p>"
        f"<p>Faculté des Sciences — Université d'État d'Haïti</p>"
    )
    return MessageEmail(destinataire=candidat.email, sujet=sujet, texte=texte, html=html)
