"""Calendrier d'admission (US-028) : période de candidature à l'heure d'Haïti, ordre des dates, audit."""

from datetime import date, datetime, timezone

import pytest

from backend.bll.calendrier_admission import (
    ConsulterCalendrierUseCase,
    ControlerPeriodeUseCase,
    ModifierCalendrierUseCase,
    jour_haiti,
)
from backend.entities.calendrier_admission import (
    PERIODE_A_VENIR,
    PERIODE_FERMEE,
    PERIODE_NON_DEFINIE,
    PERIODE_OUVERTE,
    CalendrierAdmission,
)
from backend.entities.erreurs import CandidaturesFermees, InformationsInvalides
from backend.entities.utilisateur import ROLE_ADMIN, Utilisateur
from backend.ports.calendrier_repository import ICalendrierRepository

ADMIN = Utilisateur("u-admin", "admin@fds.ht", "hash", ROLE_ADMIN)


class FakeCalendrierRepository(ICalendrierRepository):
    def __init__(self) -> None:
        self.versions: list[CalendrierAdmission] = []

    def obtenir_en_vigueur(self) -> CalendrierAdmission | None:
        return self.versions[-1] if self.versions else None

    def ajouter(self, calendrier: CalendrierAdmission) -> None:
        self.versions.append(calendrier)


def _horloge(annee, mois, jour, heure=12, minute=0):
    return lambda: datetime(annee, mois, jour, heure, minute, tzinfo=timezone.utc)


def _depot(ouverture=date(2026, 11, 1), limite=date(2026, 11, 30), **autres) -> FakeCalendrierRepository:
    depot = FakeCalendrierRepository()
    ModifierCalendrierUseCase(depot).executer({"date_ouverture": ouverture, "date_limite": limite, **autres}, ADMIN)
    return depot


def _etat(depot, horloge) -> str:
    return ConsulterCalendrierUseCase(depot, horloge).executer()[1]


def test_sans_calendrier_les_candidatures_restent_ouvertes():
    depot = FakeCalendrierRepository()
    assert _etat(depot, _horloge(2026, 11, 6)) == PERIODE_NON_DEFINIE
    ControlerPeriodeUseCase(depot, _horloge(2026, 11, 6)).executer()  # ne lève pas


@pytest.mark.parametrize("horloge, attendu", [
    (_horloge(2026, 10, 31), PERIODE_A_VENIR),
    (_horloge(2026, 11, 1, 5, 0), PERIODE_OUVERTE),  # 0 h à Port-au-Prince (UTC-5 en novembre)
    (_horloge(2026, 11, 15), PERIODE_OUVERTE),
    (_horloge(2026, 12, 1, 4, 59), PERIODE_OUVERTE),  # 23 h 59 le 30 novembre à Port-au-Prince
    (_horloge(2026, 12, 1, 5, 0), PERIODE_FERMEE),
])
def test_la_periode_suit_l_heure_d_haiti(horloge, attendu):
    assert _etat(_depot(), horloge) == attendu


def test_le_jour_d_haiti_differe_du_jour_utc_le_soir():
    assert jour_haiti(datetime(2026, 11, 7, 2, 0, tzinfo=timezone.utc)) == date(2026, 11, 6)


@pytest.mark.parametrize("horloge", [_horloge(2026, 10, 31), _horloge(2026, 12, 2)])
def test_hors_periode_le_controle_refuse(horloge):
    depot = _depot()
    with pytest.raises(CandidaturesFermees) as erreur:
        ControlerPeriodeUseCase(depot, horloge).executer()
    assert erreur.value.calendrier.date_limite == date(2026, 11, 30)


def test_ouverture_et_date_limite_sont_obligatoires():
    with pytest.raises(InformationsInvalides) as erreur:
        ModifierCalendrierUseCase(FakeCalendrierRepository()).executer({}, ADMIN)
    assert set(erreur.value.erreurs) == {"date_ouverture", "date_limite"}


@pytest.mark.parametrize("dates, champ", [
    ({"date_ouverture": date(2026, 12, 1), "date_limite": date(2026, 11, 30)}, "date_limite"),
    ({"date_ouverture": date(2026, 11, 1), "date_limite": date(2026, 11, 30), "date_concours": date(2026, 11, 29)}, "date_concours"),
    # Le concours n'est pas encore fixé : les résultats se comparent à la date limite
    ({"date_ouverture": date(2026, 11, 1), "date_limite": date(2026, 11, 30), "date_resultats": date(2026, 11, 2)}, "date_resultats"),
    ({"date_ouverture": date(2026, 11, 1), "date_limite": date(2026, 11, 30), "date_rentree": date(2026, 10, 1)}, "date_rentree"),
])
def test_les_dates_doivent_se_suivre(dates, champ):
    with pytest.raises(InformationsInvalides) as erreur:
        ModifierCalendrierUseCase(FakeCalendrierRepository()).executer(dates, ADMIN)
    assert list(erreur.value.erreurs) == [champ]


def test_chaque_modification_est_une_nouvelle_version_avec_son_auteur():
    depot = _depot()
    ModifierCalendrierUseCase(depot, _horloge(2026, 11, 6)).executer(
        {"date_ouverture": date(2026, 11, 1), "date_limite": date(2026, 12, 15), "date_concours": date(2027, 1, 10)}, ADMIN
    )
    assert len(depot.versions) == 2
    assert depot.versions[0].date_limite == date(2026, 11, 30)  # l'ancienne version n'est pas réécrite
    en_vigueur = depot.obtenir_en_vigueur()
    assert (en_vigueur.date_limite, en_vigueur.date_concours) == (date(2026, 12, 15), date(2027, 1, 10))
    assert en_vigueur.modifie_par == ADMIN.id
    assert en_vigueur.modifie_le == datetime(2026, 11, 6, 12, 0, tzinfo=timezone.utc)
