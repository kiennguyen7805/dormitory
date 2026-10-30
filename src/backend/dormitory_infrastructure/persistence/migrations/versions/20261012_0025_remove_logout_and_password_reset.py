"""Remove logout and administrative password-reset database functions."""

from alembic import op


revision = "20261012_0025"
down_revision = "20261011_0024"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        "DROP FUNCTION IF EXISTS public.fn_revoke_refresh_token(uuid, timestamptz)"
    )
    op.execute(
        "DROP FUNCTION IF EXISTS public.fn_reset_user_password(uuid, text, uuid)"
    )


def downgrade() -> None:
    raise RuntimeError("Removed authentication flows are not restored automatically")
