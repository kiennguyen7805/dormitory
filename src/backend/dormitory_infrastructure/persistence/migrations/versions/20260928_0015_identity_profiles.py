"""Use PostgreSQL functions for permissions and student profiles."""

from importlib.resources import files

from alembic import op

revision = "20260928_0015"
down_revision = "20260928_0014"
branch_labels = None
depends_on = None


def upgrade() -> None:
    statements = (
        files("dormitory_infrastructure.persistence")
        .joinpath("sql", "identity_profiles.sql")
        .read_text(encoding="utf-8")
        .split("-- NEXT STATEMENT")
    )
    for statement in statements:
        op.execute(statement.strip())


def downgrade() -> None:
    op.execute(
        "DROP FUNCTION IF EXISTS public.fn_upsert_student_profile("
        "uuid, text, text, text, date, text, text, text, text, text, text)"
    )
    op.execute("DROP FUNCTION IF EXISTS public.fn_get_student_profile(uuid)")
    op.execute("DROP FUNCTION IF EXISTS public.fn_list_permissions()")
