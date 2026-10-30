"""Read student lists and details through PostgreSQL functions."""

from importlib.resources import files

from alembic import op

revision = "20260928_0014"
down_revision = "20260928_0013"
branch_labels = None
depends_on = None


def upgrade() -> None:
    statements = (
        files("dormitory_infrastructure.persistence")
        .joinpath("sql", "students.sql")
        .read_text(encoding="utf-8")
        .split("-- NEXT STATEMENT")
    )
    for statement in statements:
        op.execute(statement.strip())


def downgrade() -> None:
    op.execute("DROP FUNCTION IF EXISTS public.fn_get_student(uuid)")
    op.execute("DROP FUNCTION IF EXISTS public.fn_list_students(integer, integer)")
    op.execute("DROP FUNCTION IF EXISTS public.fn_count_students()")
