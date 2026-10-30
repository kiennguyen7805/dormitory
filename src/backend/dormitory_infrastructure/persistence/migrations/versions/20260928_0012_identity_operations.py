"""Move account reads and writes into PostgreSQL functions."""

from importlib.resources import files

from alembic import op

revision = "20260928_0012"
down_revision = "20260928_0011"
branch_labels = None
depends_on = None


def upgrade() -> None:
    statements = (
        files("dormitory_infrastructure.persistence")
        .joinpath("sql", "identity_operations.sql")
        .read_text(encoding="utf-8")
        .split("-- NEXT STATEMENT")
    )
    for statement in statements:
        op.execute(statement.strip())


def downgrade() -> None:
    op.execute("DROP FUNCTION IF EXISTS public.fn_reset_user_password(uuid, text, uuid)")
    op.execute("DROP FUNCTION IF EXISTS public.fn_update_user(uuid, text, text, boolean, uuid)")
    op.execute("DROP FUNCTION IF EXISTS public.fn_create_user(uuid, text, text, text, text)")
    op.execute("DROP FUNCTION IF EXISTS public.fn_get_user(uuid)")
