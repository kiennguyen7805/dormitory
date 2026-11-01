"""Write housing inventory through PostgreSQL functions."""

from importlib.resources import files

from alembic import op

revision = "20260928_0017"
down_revision = "20260928_0016"
branch_labels = None
depends_on = None


def upgrade() -> None:
    statements = (
        files("dormitory_infrastructure.persistence")
        .joinpath("sql", "housing_writes_0017.sql")
        .read_text(encoding="utf-8")
        .split("-- NEXT STATEMENT")
    )
    for statement in statements:
        op.execute(statement.strip())


def downgrade() -> None:
    op.execute(
        "DROP FUNCTION IF EXISTS public.fn_bulk_update_room_gender("
        "uuid[], uuid, integer, text, uuid, boolean)"
    )
    op.execute("DROP FUNCTION IF EXISTS public.fn_deactivate_housing(text, uuid)")
    op.execute("DROP FUNCTION IF EXISTS public.fn_save_housing(text, uuid, jsonb, boolean)")
