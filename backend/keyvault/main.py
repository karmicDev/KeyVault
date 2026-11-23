"""Application factory.

Start locally with:
    uvicorn keyvault.main:create_app --factory --reload
"""

from fastapi import FastAPI
from sqlalchemy import Engine

from keyvault import health
from keyvault.config import get_settings
from keyvault.db import create_db_engine


def create_app(engine: Engine | None = None) -> FastAPI:
    """Build the FastAPI app.

    `engine` lets tests inject their own database engine; by default it is
    created from the settings.
    """
    app = FastAPI(title="KeyVault backend")
    app.state.engine = engine or create_db_engine(get_settings())
    app.include_router(health.router)
    return app
