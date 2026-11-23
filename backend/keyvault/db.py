"""Database engine and the per-request session dependency."""

from collections.abc import Iterator

from fastapi import Request
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import DeclarativeBase, Session

from keyvault.config import Settings


def create_db_engine(settings: Settings) -> Engine:
    """Create the engine. It connects lazily, on first use."""
    # pool_pre_ping checks a pooled connection before use, so a restarted
    # database does not cause errors on the first request afterwards.
    return create_engine(settings.database_url(), pool_pre_ping=True)


def get_session(request: Request) -> Iterator[Session]:
    """FastAPI dependency: one session per request, closed afterwards."""
    with Session(request.app.state.engine) as session:
        yield session


class Base(DeclarativeBase):
    """Base class for all ORM models (the first ones follow in KV-005)."""
