"""Use PostgreSQL functions for authentication data access."""

from importlib.resources import files

from alembic import op

revision = "20260928_0013"
down_revision = "20260928_0012"
branch_labels = None
depends_on = None


def upgrade() -> None:
    statements = (
        files("dormitory_infrastructure.persistence")
        .joinpath("sql", "auth.sql")
        .read_text(encoding="utf-8")
        .split("-- NEXT STATEMENT")
    )
    for statement in statements:
        op.execute(statement.strip())


def downgrade() -> None:
    op.execute("DROP FUNCTION IF EXISTS public.fn_revoke_refresh_token(uuid, timestamptz)")
    op.execute("DROP FUNCTION IF EXISTS public.fn_set_refresh_token(uuid, text, timestamptz)")
    op.execute("DROP FUNCTION IF EXISTS public.fn_register_student(uuid, text, text, text, text, date)")
    op.execute("DROP FUNCTION IF EXISTS public.fn_auth_user(uuid, text, text)")
