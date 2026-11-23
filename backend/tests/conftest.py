"""Shared pytest fixtures: a separate test database and a test client."""

from collections.abc import Iterator
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine, text

from keyvault.config import Settings, get_settings
from keyvault.main import create_app

TEST_DB_NAME = "keyvault_test"
BACKEND_DIR = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def db_engine() -> Iterator[Engine]:
    """Engine for the test database, created and migrated once per test run."""
    settings = get_settings()
    _create_database_if_missing(settings)
    engine = create_engine(settings.database_url(TEST_DB_NAME))
    _migrate(engine)
    yield engine
    engine.dispose()


@pytest.fixture
def client(db_engine: Engine) -> Iterator[TestClient]:
    """Test client for an app that talks to the test database."""
    with TestClient(create_app(engine=db_engine)) as test_client:
        yield test_client


def _create_database_if_missing(settings: Settings) -> None:
    """Create the test database next to the dev database in the same server."""
    # CREATE DATABASE cannot run inside a transaction, hence AUTOCOMMIT.
    admin = create_engine(settings.database_url(), isolation_level="AUTOCOMMIT")
    try:
        with admin.connect() as connection:
            exists = connection.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :name"),
                {"name": TEST_DB_NAME},
            ).scalar()
            if not exists:
                connection.execute(text(f'CREATE DATABASE "{TEST_DB_NAME}"'))
    finally:
        admin.dispose()


def _migrate(engine: Engine) -> None:
    """Run `alembic upgrade head` on the test database."""
    config = Config(str(BACKEND_DIR / "alembic.ini"))
    with engine.begin() as connection:
        config.attributes["connection"] = connection
        command.upgrade(config, "head")
