from pathlib import Path

from sqlalchemy import Engine, create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker

from app.core.config import Settings
from app.db.base import Base


def create_database_engine(settings: Settings) -> Engine:
    """Build an engine appropriate for the configured database URL."""
    url = make_url(settings.database_url)
    connect_args = {"check_same_thread": False} if url.drivername.startswith("sqlite") else {}
    return create_engine(settings.database_url, connect_args=connect_args)


def create_session_factory(engine: Engine) -> sessionmaker:
    return sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def initialize_database(engine: Engine) -> None:
    """Create local SQLite directories and application tables when missing."""
    url = engine.url
    if url.drivername.startswith("sqlite") and url.database and url.database != ":memory:":
        Path(url.database).parent.mkdir(parents=True, exist_ok=True)

    # Import model modules before metadata inspection.
    import app.models.item  # noqa: F401

    Base.metadata.create_all(bind=engine)
