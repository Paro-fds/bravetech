class AppError(Exception):
    """Base for every domain exception this service raises."""


# --- Persistence-level: raised by DAL, generic across every entity ---


class NotFoundError(AppError):
    pass


class DuplicateKeyError(AppError):
    pass


# --- Business-level: raised by BLL, specific and meaningful ---
#
# Add exceptions here as real business rules need them, e.g.
# `class DuplicateEmailError(AppError): pass`. Keep names semantic and
# business-facing, never layer-prefixed (PEP 8: suffix Error, no layer
# prefix) — see project-docs/learnings/03-backend-layered-architecture-template.md
# for why.
