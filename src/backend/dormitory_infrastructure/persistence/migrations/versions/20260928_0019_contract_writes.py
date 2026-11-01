"""Write housing application and contract transactions in PostgreSQL."""

from importlib.resources import files

from alembic import op

revision = "20260928_0019"
down_revision = "20260928_0018"
branch_labels = None
depends_on = None


def upgrade() -> None:
    statements = (
        files("dormitory_infrastructure.persistence")
        .joinpath("sql", "contract_writes_0019.sql")
        .read_text(encoding="utf-8")
        .split("-- NEXT STATEMENT")
    )
    for statement in statements:
        op.execute(statement.strip())


def downgrade() -> None:
    for signature in (
        "fn_terminate_contract(uuid, date)",
        "fn_assign_bed(uuid, uuid, uuid, text, uuid, date, date)",
        "fn_check_bed_available(uuid, date, date)",
        "fn_review_application(uuid, uuid, text, text)",
        "fn_create_application(uuid, uuid, text, uuid)",
    ):
        op.execute(f"DROP FUNCTION IF EXISTS public.{signature}")
