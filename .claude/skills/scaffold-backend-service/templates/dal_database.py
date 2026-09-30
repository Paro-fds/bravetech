from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings

is_sqlite = settings.database_url.startswith("sqlite")
connect_args = {"check_same_thread": False} if is_sqlite else {}
engine = create_engine(settings.database_url, connect_args=connect_args)

# The moment a second process/service writes to the same SQLite file, WAL
# mode stops being optional — see project-docs/learnings/03-backend-layered-
# architecture-template.md's concurrency gotcha. Setting it here means it's
# never silently missing even for a service that's single-writer today but
# might not stay that way.
if is_sqlite:
    @event.listens_for(engine, "connect")
    def _enable_wal_mode(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
