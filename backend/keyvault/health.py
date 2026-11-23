"""Health endpoint: reports whether the service and its database are reachable."""

import logging
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from keyvault.db import get_session

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health")
def health(session: Annotated[Session, Depends(get_session)]) -> JSONResponse:
    """Return 200 if `SELECT 1` succeeds, otherwise 503."""
    try:
        session.execute(text("SELECT 1"))
    except SQLAlchemyError:
        logger.warning("Database health check failed", exc_info=True)
        return JSONResponse(status_code=503, content={"status": "error", "db": "error"})
    return JSONResponse(content={"status": "ok", "db": "ok"})
