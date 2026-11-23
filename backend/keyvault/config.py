"""Application settings, read from environment variables and the root .env."""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

# backend/keyvault/config.py -> parents[2] is the repository root.
ROOT_ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
    """Settings for the backend.

    Values come from environment variables first, then from the root `.env`
    (the same file docker-compose uses). Names are case-insensitive, so
    `POSTGRES_USER` fills `postgres_user`.
    """

    model_config = SettingsConfigDict(env_file=ROOT_ENV_FILE, extra="ignore")

    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    def database_url(self, database: str | None = None) -> URL:
        """Build the SQLAlchemy URL; `database` overrides the database name."""
        return URL.create(
            drivername="postgresql+psycopg",
            username=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_host,
            port=self.postgres_port,
            database=database or self.postgres_db,
        )


@lru_cache
def get_settings() -> Settings:
    """Return the settings, read once per process."""
    return Settings()
