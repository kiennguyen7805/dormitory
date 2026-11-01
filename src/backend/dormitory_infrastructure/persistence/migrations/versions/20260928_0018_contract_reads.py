"""Read housing applications and contracts through PostgreSQL functions."""

from importlib.resources import files

from alembic import op

revision = "20260928_0018"
down_revision = "20260928_0017"
branch_labels = None
depends_on = None


def upgrade() -> None:
    statements = (
        files("dormitory_infrastructure.persistence")
        .joinpath("sql", "contract_reads_0018.sql")
        .read_text(encoding="utf-8")
        .split("-- NEXT STATEMENT")
    )
    for statement in statements:
        op.execute(statement.strip())


def downgrade() -> None:
    for signature in (
        "fn_get_contract(uuid)",
        "fn_list_contracts(uuid, text)", "fn_get_application(uuid)",
        "fn_list_applications(uuid, text, text)",
    ):
        op.execute(f"DROP FUNCTION IF EXISTS public.{signature}")
