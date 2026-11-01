"""Contenu des emails transactionnels — Couche BLL.

Messages fonctionnels et factuels (PRD §8). Le HTML échappe toutes les valeurs saisies par le candidat.
"""

from html import escape

from backend.entities.candidat import Candidat
from backend.entities.candidature import FRAIS_DOSSIER_HTG, Candidature
from backend.entities.document_soumis import STATUT_VALIDE
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


def message_decision(
    candidat: Candidat, candidature: Candidature, nom_piece: str, statut: str, motif: str | None, url_suivi: str
) -> MessageEmail:
    """Email envoyé après la décision du personnel sur une pièce : validée, ou refusée avec son motif et le lien pour la remplacer."""
    reference = candidature.reference_dossier or ""
    if statut == STATUT_VALIDE:
        sujet = f"Pièce validée — {nom_piece} ({reference})"
        texte = (
            f"Bonjour {candidat.prenom},\n\n"
            f"Votre pièce « {nom_piece} » a été validée par la Faculté des Sciences (dossier {reference}).\n\n"
            f"Vous n'avez rien à faire pour cette pièce. Suivre mon dossier : {url_suivi}\n\n"
            f"Faculté des Sciences — Université d'État d'Haïti\n"
        )
        html = (
            f"<p>Bonjour {escape(candidat.prenom)},</p>"
            f"<p>Votre pièce <strong>{escape(nom_piece)}</strong> a été <strong>validée</strong> par la Faculté des Sciences "
            f"(dossier {escape(reference)}).</p>"
            f"<p>Vous n'avez rien à faire pour cette pièce.</p>"
            f'<p><a href="{escape(url_suivi, quote=True)}">Suivre mon dossier</a></p>'
            f"<p>Faculté des Sciences — Université d'État d'Haïti</p>"
        )
    else:
        sujet = f"Pièce à remplacer — {nom_piece} ({reference})"
        texte = (
            f"Bonjour {candidat.prenom},\n\n"
            f"Votre pièce « {nom_piece} » n'a pas pu être acceptée (dossier {reference}).\n"
            f"Motif : {motif or 'non précisé'}\n\n"
            f"Vous pouvez la remplacer sans vous déplacer : {url_suivi}\n\n"
            f"Faculté des Sciences — Université d'État d'Haïti\n"
        )
        html = (
            f"<p>Bonjour {escape(candidat.prenom)},</p>"
            f"<p>Votre pièce <strong>{escape(nom_piece)}</strong> n'a pas pu être acceptée (dossier {escape(reference)}).</p>"
            f"<p><strong>Motif :</strong> {escape(motif or 'non précisé')}</p>"
            f"<p>Vous pouvez la remplacer sans vous déplacer :</p>"
            f'<p><a href="{escape(url_suivi, quote=True)}" style="display:inline-block;padding:12px 20px;background:#01346d;'
            f'color:#ffffff;text-decoration:none;border-radius:8px;font-weight:bold">Remplacer le document →</a></p>'
            f"<p>Faculté des Sciences — Université d'État d'Haïti</p>"
        )
    return MessageEmail(destinataire=candidat.email, sujet=sujet, texte=texte, html=html)


def message_remplacement(candidat: Candidat, candidature: Candidature, nom_piece: str, url_suivi: str) -> MessageEmail:
    """Accusé de réception d'une pièce remplacée par le candidat."""
    reference = candidature.reference_dossier or ""
    sujet = f"Nouvelle pièce reçue — {nom_piece} ({reference})"
    texte = (
        f"Bonjour {candidat.prenom},\n\n"
        f"Nous avons bien reçu votre nouvelle version de « {nom_piece} » (dossier {reference}).\n"
        f"La Faculté va l'examiner et vous écrira dès qu'elle aura pris sa décision.\n\n"
        f"Suivre mon dossier : {url_suivi}\n\n"
        f"Faculté des Sciences — Université d'État d'Haïti\n"
    )
    html = (
        f"<p>Bonjour {escape(candidat.prenom)},</p>"
        f"<p>Nous avons bien reçu votre nouvelle version de <strong>{escape(nom_piece)}</strong> "
        f"(dossier {escape(reference)}).</p>"
        f"<p>La Faculté va l'examiner et vous écrira dès qu'elle aura pris sa décision.</p>"
        f'<p><a href="{escape(url_suivi, quote=True)}">Suivre mon dossier</a></p>'
        f"<p>Faculté des Sciences — Université d'État d'Haïti</p>"
    )
    return MessageEmail(destinataire=candidat.email, sujet=sujet, texte=texte, html=html)
