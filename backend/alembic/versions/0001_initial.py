"""Initial empty migration.

Creates no tables; it gives later migrations (KV-005 onwards) a starting point
and proves that `alembic upgrade head` works against the database.

Revision ID: 0001
Revises:
Create Date: 2026-11-23

"""

from collections.abc import Sequence

# Revision identifiers, used by Alembic.
revision: str = "0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
