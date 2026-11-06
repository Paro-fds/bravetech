"""Score CRAP (Change Risk Anti-Patterns) du backend, fonction par fonction.

    CRAP(f) = complexité(f)² × (1 − couverture(f)/100)³ + complexité(f)

- complexité : complexité cyclomatique de radon (`radon.complexity.cc_visit`) ;
- couverture : part des instructions de la fonction exécutées par les tests (`coverage json`).
  Une instruction compte pour la fonction la plus intérieure qui la contient : le corps d'une fonction
  imbriquée ne compte pas pour sa fonction parente.

Usage, depuis la racine du dépôt :
    python -m coverage run --source=backend -m pytest -q
    python -m coverage json -o coverage.json
    python tools/crap.py coverage.json [--seuil 30] [--top 15]

Sort en erreur (code 1) si une fonction dépasse le seuil : utilisable en CI.
"""

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path

from radon.complexity import cc_visit
from radon.visitors import Class, Function

RACINE = Path(__file__).resolve().parents[1]


@dataclass
class Fonction:
    fichier: str
    nom: str
    debut: int
    fin: int
    complexite: int
    couverture: float = 100.0

    @property
    def crap(self) -> float:
        return self.complexite**2 * (1 - self.couverture / 100) ** 3 + self.complexite


def _fonctions(fichier: Path) -> list[Fonction]:
    """Fonctions et méthodes du fichier, imbriquées comprises (radon les range dans `closures` et `methods`)."""
    trouvees: list[Fonction] = []
    relatif = fichier.relative_to(RACINE).as_posix()

    def visiter(bloc, prefixe: str = "") -> None:
        if isinstance(bloc, Class):
            for methode in bloc.methods:
                visiter(methode, f"{prefixe}{bloc.name}.")
            return
        if isinstance(bloc, Function):
            nom = f"{prefixe}{bloc.name}"
            trouvees.append(Fonction(relatif, nom, bloc.lineno, bloc.endline, bloc.complexity))
            for imbriquee in bloc.closures:
                visiter(imbriquee, f"{nom}.")

    for bloc in cc_visit(fichier.read_text(encoding="utf-8")):
        # cc_visit renvoie aussi les méthodes à plat : on ne garde que les blocs de premier niveau
        if isinstance(bloc, Function) and bloc.is_method:
            continue
        visiter(bloc)
    return trouvees


def _couvrir(fonctions: list[Fonction], executees: set[int], manquantes: set[int]) -> None:
    for f in fonctions:
        # Instructions de la fonction, sans celles des fonctions imbriquées plus profondes
        interieures = [g for g in fonctions if g is not f and f.debut < g.debut and g.fin <= f.fin]
        def a_moi(ligne: int) -> bool:
            return f.debut <= ligne <= f.fin and not any(g.debut <= ligne <= g.fin for g in interieures)

        faites = sum(1 for ligne in executees if a_moi(ligne))
        ratees = sum(1 for ligne in manquantes if a_moi(ligne))
        total = faites + ratees
        f.couverture = 100.0 * faites / total if total else 100.0


def calculer(rapport_couverture: Path) -> list[Fonction]:
    donnees = json.loads(rapport_couverture.read_text(encoding="utf-8"))["files"]
    resultats: list[Fonction] = []
    for fichier in sorted((RACINE / "backend").rglob("*.py")):
        if "migrations" in fichier.parts or "__pycache__" in fichier.parts:
            continue
        fonctions = _fonctions(fichier)
        cle = next((k for k in donnees if Path(k).resolve() == fichier.resolve()), None)
        if cle is None:
            for f in fonctions:  # fichier jamais importé par les tests : couverture nulle
                f.couverture = 0.0
        else:
            _couvrir(fonctions, set(donnees[cle]["executed_lines"]), set(donnees[cle]["missing_lines"]))
        resultats.extend(fonctions)
    return resultats


def main() -> int:
    parametres = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parametres.add_argument("rapport", type=Path, help="Rapport JSON de coverage.py")
    parametres.add_argument("--seuil", type=float, default=30.0)
    parametres.add_argument("--top", type=int, default=15)
    args = parametres.parse_args()

    fonctions = sorted(calculer(args.rapport), key=lambda f: f.crap, reverse=True)
    au_dessus = [f for f in fonctions if f.crap > args.seuil]
    moyenne = sum(f.crap for f in fonctions) / len(fonctions)

    print(f"Fonctions analysées : {len(fonctions)}")
    print(f"CRAP moyen : {moyenne:.2f} ; maximum : {fonctions[0].crap:.2f}")
    print(f"Au-dessus du seuil {args.seuil:g} : {len(au_dessus)}")
    print()
    print(f"{'CRAP':>7}  {'CC':>3}  {'Couv.':>6}  Fonction")
    for f in fonctions[: args.top]:
        print(f"{f.crap:7.2f}  {f.complexite:3d}  {f.couverture:5.1f}%  {f.fichier}:{f.debut} {f.nom}")
    return 1 if au_dessus else 0


if __name__ == "__main__":
    sys.exit(main())
