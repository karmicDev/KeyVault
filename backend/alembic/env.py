"""Alembic environment: runs migrations against the KeyVault database."""

from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine

from keyvault.config import get_settings
from keyvault.db import Base

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name, disable_existing_loggers=False)

# Models register their tables on Base.metadata (from KV-005 on); autogenerate
# compares the database against it.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """`alembic upgrade head --sql`: print the SQL instead of running it."""
    url = get_settings().database_url().render_as_string(hide_password=False)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations on a live connection.

    Tests pass their own connection in `config.attributes["connection"]`
    (to migrate the test database); otherwise the settings decide.
    """
    connection = config.attributes.get("connection")
    if connection is not None:
        _run(connection)
        return

    engine = create_engine(get_settings().database_url())
    try:
        with engine.connect() as connection:
            _run(connection)
    finally:
        engine.dispose()


def _run(connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
