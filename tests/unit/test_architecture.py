"""
Test d'architecture — Règle de Dépendance (Clean Architecture)
===============================================================
Ce test parcourt chaque fichier Python du dossier `backend/` et vérifie
que les imports respectent la direction autorisée :

    entities  ←  dal  ←  bll  ←  api
        ↑                          ↑
        └────────── core/ ─────────┘  (disponible pour toutes les couches)

Les couches internes ne peuvent JAMAIS importer les couches externes.
Une violation ici = build rouge. Pas de mémoire, pas de convention : une machine.

Référence : project-docs/_ARCHITECTURE_EXPLAINED.md, Partie 1.
"""

import ast
from pathlib import Path

import pytest

# Racine du backend (chemin relatif depuis ce fichier → ../../backend)
BACKEND_ROOT = Path(__file__).resolve().parents[2] / "backend"

# Imports interdits par couche
# Format : { "couche_source": ("couches_interdites", ...) }
FORBIDDEN: dict[str, tuple[str, ...]] = {
    "entities": ("dal", "bll", "api", "sqlalchemy", "fastapi"),
    "dal":      ("bll", "api"),
    "bll":      ("api", "sqlalchemy"),
}


def _get_layer(filepath: Path) -> str | None:
    """Retourne la couche ('entities', 'dal', 'bll', 'api', 'core') ou None."""
    parts = filepath.relative_to(BACKEND_ROOT).parts
    if parts:
        return parts[0]
    return None


def _collect_imports(filepath: Path) -> list[str]:
    """Retourne la liste des modules importés dans un fichier Python."""
    try:
        tree = ast.parse(filepath.read_text(encoding="utf-8"))
    except SyntaxError:
        return []

    modules = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                modules.append(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                modules.append(node.module.split(".")[0])
    return modules


def _collect_violations() -> list[tuple[str, str, str]]:
    """
    Parcourt tous les fichiers Python du backend et retourne les violations.
    Retourne une liste de tuples (fichier_relatif, couche_source, import_interdit).
    """
    violations = []

    if not BACKEND_ROOT.exists():
        # Le backend n'existe pas encore — on passe silencieusement.
        return violations

    for py_file in BACKEND_ROOT.rglob("*.py"):
        layer = _get_layer(py_file)
        if layer not in FORBIDDEN:
            continue

        forbidden_targets = FORBIDDEN[layer]
        imports = _collect_imports(py_file)

        for imported in imports:
            if imported in forbidden_targets:
                relative = py_file.relative_to(BACKEND_ROOT)
                violations.append((str(relative), layer, imported))

    return violations


# --------------------------------------------------------------------------- #
#  Tests pytest
# --------------------------------------------------------------------------- #

def test_dependency_rule_not_violated() -> None:
    """
    Verifie que la Regle de Dependance est respectee dans l'ensemble du backend.

    Si ce test est rouge, un fichier importe une couche qu'il n'a pas le droit
    de connaitre. Corrigez l'import ou deplacez le code dans la bonne couche.
    """
    violations = _collect_violations()

    if violations:
        report_lines = [
            "\n\nVIOLATION DE LA REGLE DE DEPENDANCE (Clean Architecture)\n",
            "=" * 65,
        ]
        for filepath, layer, forbidden_import in violations:
            report_lines.append(
                f"  [X]  backend/{filepath}\n"
                f"       couche '{layer}' importe '{forbidden_import}' (interdit)\n"
            )
        report_lines.append(
            "\nRegle : les dependances ne pointent que vers l'interieur.\n"
            "Reference : project-docs/_ARCHITECTURE_EXPLAINED.md, Partie 1.\n"
        )
        pytest.fail("\n".join(report_lines))


def test_entities_layer_has_no_orm_models() -> None:
    """
    Garantit qu'aucun fichier de `entities/` n'utilise les classes de base ORM
    (DeclarativeBase, Base de SQLAlchemy). Les entites sont des dataclasses pures.
    """
    entities_dir = BACKEND_ROOT / "entities"
    if not entities_dir.exists():
        pytest.skip("Le dossier backend/entities/ n'existe pas encore.")

    orm_markers = ("DeclarativeBase", "declarative_base", "Base")
    offenders = []

    for py_file in entities_dir.rglob("*.py"):
        content = py_file.read_text(encoding="utf-8")
        for marker in orm_markers:
            if marker in content:
                offenders.append((py_file.relative_to(BACKEND_ROOT), marker))

    assert not offenders, (
        "\nEntites ORM detectees dans la couche Domain :\n"
        + "\n".join(f"  [X] backend/{f} — contient '{m}'" for f, m in offenders)
        + "\n\nLes entites doivent etre des dataclasses ou Pydantic models purs."
    )
