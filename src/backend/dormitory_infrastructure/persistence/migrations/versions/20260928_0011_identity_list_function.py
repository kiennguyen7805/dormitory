"""Install the PostgreSQL function used by the account-list API."""

from importlib.resources import files

from alembic import op

revision = "20260928_0011"
down_revision = "20260927_0010"
branch_labels = None
depends_on = None


def upgrade() -> None:
    statement = (
        files("dormitory_infrastructure.persistence")
        .joinpath("sql", "identity.sql")
        .read_text(encoding="utf-8")
    )
    op.execute(statement)


def downgrade() -> None:
    op.execute("DROP FUNCTION IF EXISTS public.fn_list_users(text)")
