"""Seed and readiness database operations through stored functions."""

from importlib.resources import files

from alembic import op

revision = "20261004_0022"
down_revision = "20261004_0021"
branch_labels = None
depends_on = None


def upgrade() -> None:
    statements = (
        files("dormitory_infrastructure.persistence")
        .joinpath("sql", "seed_functions.sql")
        .read_text(encoding="utf-8")
        .split("-- NEXT STATEMENT")
    )
    for statement in statements:
        if statement.strip():
            op.execute(statement.strip())


def downgrade() -> None:
    for signature in (
        "fn_db_ready()",
        "fn_seed_utility(uuid, text, text, text, integer)",
        "fn_seed_student_profile(uuid, text)",
        "fn_seed_user(uuid, text, text, text, text)",
        "fn_seed_role(uuid, text)",
    ):
        op.execute(f"DROP FUNCTION IF EXISTS public.{signature}")
