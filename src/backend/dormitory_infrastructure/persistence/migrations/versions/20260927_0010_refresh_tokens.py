"""Add rotating refresh-token state to users without creating a new table."""

from alembic import op
import sqlalchemy as sa

revision = "20260927_0010"
down_revision = "20260921_0009"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("refresh_token_hash", sa.String(64)))
    op.add_column("users", sa.Column("refresh_token_expires_at", sa.DateTime(timezone=True)))
    op.add_column("users", sa.Column("refresh_token_revoked_at", sa.DateTime(timezone=True)))
    op.create_index(
        "ix_users_refresh_token_hash",
        "users",
        ["refresh_token_hash"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index("ix_users_refresh_token_hash", table_name="users")
    op.drop_column("users", "refresh_token_revoked_at")
    op.drop_column("users", "refresh_token_expires_at")
    op.drop_column("users", "refresh_token_hash")
