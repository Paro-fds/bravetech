"""Modèles ORM SQLAlchemy — Couche DAL (Data Access Layer).

Représentation relationnelle des tables dynamiques et transactionnelles en base de données.
Note : Les informations de cursus et pièces requises sont des données de référence
statiques stockées directement sous forme de fichiers JSON dans `cursus/` et ne
nécessitent pas de tables SQL (cf. JsonCursusRepository).

Les modèles de persistance (Candidat, Candidature, DocumentSoumis, Utilisateur)
seront introduits avec les Epics 2 et 3.
"""

from backend.dal.database import Base

# Placeholder pour les futures tables transactionnelles (Epic 2 & 3)
