"""Génération du PDF de l'export des dossiers — Couche DAL (US-015).

Adaptateur reportlab (pur Python, sans bibliothèque système, donc simple à installer dans l'image Docker). Les polices
PDF standard couvrent le français et le créole (é, è, à, ç, ò, œ…). Un caractère hors de ce jeu s'affiche en carré,
sans faire échouer l'export.
"""

import io
from datetime import datetime, timezone

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

MARINE = colors.HexColor("#01346d")
LIGNE = colors.HexColor("#d5dce8")
FOND_ENTETE = colors.HexColor("#e6edf6")

EN_TETES = ["Référence", "Nom", "Prénom", "Déplacement", "Statut", "Pièces validées", "Soumis le (UTC)"]
LARGEURS_CM = [3.4, 5.0, 5.0, 2.8, 4.0, 2.9, 3.8]


def _pied_de_page(canvas, document) -> None:
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawString(document.leftMargin, 1.0 * cm, "Faculté des Sciences, UEH — document confidentiel, réservé au personnel")
    canvas.drawRightString(landscape(A4)[0] - document.rightMargin, 1.0 * cm, f"Page {document.page}")
    canvas.restoreState()


def generer_pdf(titre: str, filtres: str, lignes: list[list[str]], genere_le: datetime | None = None) -> bytes:
    """PDF paysage A4 : titre, rappel des filtres, tableau (en-tête répété à chaque page), nombre de dossiers."""
    genere_le = genere_le or datetime.now(timezone.utc)
    styles = getSampleStyleSheet()
    titre_style = ParagraphStyle("titre", parent=styles["Title"], textColor=MARINE, fontSize=18, alignment=0, spaceAfter=4)
    info_style = ParagraphStyle("info", parent=styles["Normal"], fontSize=9, textColor=colors.HexColor("#475873"))
    cellule = ParagraphStyle("cellule", parent=styles["Normal"], fontSize=8.5, leading=10.5)

    def _p(texte: str) -> Paragraph:
        # Paragraph interprète un mini-HTML : on échappe la saisie des candidats
        return Paragraph(texte.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"), cellule)

    sortie = io.BytesIO()
    document = SimpleDocTemplate(
        sortie, pagesize=landscape(A4), leftMargin=1.5 * cm, rightMargin=1.5 * cm, topMargin=1.5 * cm, bottomMargin=1.8 * cm,
        title=titre, author="Faculté des Sciences, UEH",
    )
    contenu = [
        Paragraph(titre, titre_style),
        Paragraph(f"{len(lignes)} dossier{'s' if len(lignes) > 1 else ''} · {filtres} · généré le {genere_le:%d/%m/%Y à %H:%M} UTC", info_style),
        Spacer(1, 0.4 * cm),
    ]
    donnees = [[_p(e) for e in EN_TETES]] + [[_p(c) for c in ligne] for ligne in lignes]
    if not lignes:
        donnees.append([_p("Aucun dossier ne correspond à ces critères.")] + [_p("")] * (len(EN_TETES) - 1))
    tableau = Table(donnees, colWidths=[l * cm for l in LARGEURS_CM], repeatRows=1)
    tableau.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), FOND_ENTETE),
        ("TEXTCOLOR", (0, 0), (-1, 0), MARINE),
        ("GRID", (0, 0), (-1, -1), 0.4, LIGNE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafd")]),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    contenu.append(tableau)
    document.build(contenu, onFirstPage=_pied_de_page, onLaterPages=_pied_de_page)
    return sortie.getvalue()
