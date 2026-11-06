"""SMS simulés (US-016) : un SMS est enregistré à la soumission et à chaque décision ; le personnel les consulte."""

from tests.integration.test_admin_dossiers_api import LISTE, _environnement, _soumettre, entete  # noqa: F401
from tests.integration.test_candidatures_api import SAISIE

SMS = "/api/v1/admin/sms"


def test_la_soumission_enregistre_un_sms_au_numero_du_candidat(client, entete):  # noqa: F811
    reference = _soumettre(client, "louismy@exemple.com")
    sms = client.get(SMS, headers=entete).json()
    assert len(sms) == 1
    assert sms[0]["reference_dossier"] == reference
    assert sms[0]["destinataire"] == "+509" + SAISIE["telephone"].replace(" ", "")
    assert reference in sms[0]["texte"] and len(sms[0]["texte"]) <= 160


def test_une_decision_enregistre_un_sms(client, entete):  # noqa: F811
    reference = _soumettre(client, "louismy@exemple.com")
    piece = client.get(f"{LISTE}/{reference}", headers=entete).json()["pieces"][0]
    reponse = client.put(
        f"/api/v1/admin/documents/{piece['document_id']}/statut",
        json={"statut": "rejete", "motif": "Document illisible, merci de le renvoyer."},
        headers=entete,
    )
    assert reponse.status_code == 200
    textes = [s["texte"] for s in client.get(SMS, headers=entete).json()]
    assert len(textes) == 2 and "à remplacer" in textes[0]  # le plus récent d'abord


def test_le_journal_des_sms_est_reserve_au_personnel(client):
    assert client.get(SMS).status_code == 401
