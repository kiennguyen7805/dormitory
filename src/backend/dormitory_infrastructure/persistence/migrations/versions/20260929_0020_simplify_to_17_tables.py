"""Keep the 17 tables used by the educational API.

The removed tables contain features outside the selected course scope. Back up
the database before applying this migration if it contains non-demo data.
"""

from importlib.resources import files

from alembic import op


revision = "20260929_0020"
down_revision = "20260928_0019"
branch_labels = None
depends_on = None


def _install_sql(filename: str) -> None:
    statements = (
        files("dormitory_infrastructure.persistence")
        .joinpath("sql", filename)
        .read_text(encoding="utf-8")
        .split("-- NEXT STATEMENT")
    )
    for statement in statements:
        if statement.strip():
            op.execute(statement.strip())


def upgrade() -> None:
    # PostgreSQL cannot change the result columns of these functions in place.
    op.execute("DROP FUNCTION IF EXISTS public.fn_get_user(uuid)")
    op.execute("DROP FUNCTION IF EXISTS public.fn_list_users(text)")
    op.execute("DROP FUNCTION IF EXISTS public.fn_auth_user(uuid, text, text)")
    op.execute("DROP FUNCTION IF EXISTS public.fn_list_permissions()")

    _install_sql("identity.sql")
    _install_sql("identity_operations.sql")
    _install_sql("auth.sql")

    op.drop_table("role_permissions")
    op.drop_table("permissions")

    op.drop_table("notification_reads")
    op.drop_table("notification_targets")
    op.drop_table("notifications")

    op.drop_table("maintenance_events")
    op.drop_table("maintenance_plans")
    op.drop_table("maintenance_requests")

    op.drop_table("violation_evidences")
    op.drop_table("violations")
    op.drop_table("violation_types")

    op.drop_table("payments")
    op.drop_table("contract_events")
    op.drop_table("room_transfer_requests")

    op.drop_column("meter_readings", "import_batch_id")
    op.drop_column("meter_readings", "source")
    op.drop_table("utility_import_batches")
    op.drop_table("stored_files")


def downgrade() -> None:
    raise RuntimeError(
        "Migration 0020 removes out-of-scope data; restore a pre-upgrade backup to downgrade."
    )
