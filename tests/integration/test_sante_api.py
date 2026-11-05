"""Route de santé (US-026) : le script de déploiement revient en arrière si elle ne répond pas 200."""

from sqlalchemy.exc import OperationalError

from backend.dal.database import get_db
from backend.main import app

URL = "/api/v1/sante"


def test_la_base_repond(client):
    reponse = client.get(URL)
    assert reponse.status_code == 200
    assert reponse.json() == {"statut": "ok"}


class _SessionCassee:
    def execute(self, *_):
        raise OperationalError("SELECT 1", {}, Exception("connexion refusée par 10.0.0.9"))

    def close(self):
        pass


def test_une_base_injoignable_donne_503_sans_detail(client):
    app.dependency_overrides[get_db] = lambda: _SessionCassee()
    reponse = client.get(URL)
    assert reponse.status_code == 503
    assert "10.0.0.9" not in reponse.text
