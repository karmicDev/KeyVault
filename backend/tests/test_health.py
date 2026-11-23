"""Tests for GET /health."""

from fastapi.testclient import TestClient
from sqlalchemy import create_engine

from keyvault.config import get_settings
from keyvault.main import create_app


def test_client_uses_test_database(client: TestClient) -> None:
    assert client.app.state.engine.url.database == "keyvault_test"


def test_health_ok(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "db": "ok"}


def test_health_returns_503_when_database_is_down() -> None:
    # Nothing listens on port 1, so every connection attempt fails at once:
    # a real connection error, no mocking.
    url = get_settings().database_url().set(port=1)
    engine = create_engine(url)
    try:
        with TestClient(create_app(engine=engine)) as client:
            response = client.get("/health")
    finally:
        engine.dispose()

    assert response.status_code == 503
    assert response.json() == {"status": "error", "db": "error"}
