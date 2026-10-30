"""Move utility and billing persistence into PostgreSQL functions."""

from importlib.resources import files

from alembic import op

revision = "20261004_0021"
down_revision = "20260929_0020"
branch_labels = None
depends_on = None


def upgrade() -> None:
    sql_dir = files("dormitory_infrastructure.persistence").joinpath("sql")
    for filename in ("utility_functions.sql", "billing_functions.sql"):
        for statement in sql_dir.joinpath(filename).read_text(encoding="utf-8").split("-- NEXT STATEMENT"):
            if statement.strip():
                op.execute(statement.strip())


def downgrade() -> None:
    for signature in (
        "fn_generate_bill(uuid, text, uuid, date, date, date, date, text, uuid)",
        "fn_bill_items(uuid)", "fn_list_bills(uuid, text, uuid)", "fn_get_bill(uuid)",
        "fn_create_reading(uuid, uuid, date, date, numeric, numeric, numeric, uuid, json, numeric, uuid)",
        "fn_reading_context(uuid, date, date)", "fn_get_reading(uuid)",
        "fn_list_readings(uuid, date)", "fn_find_tariff(uuid, date)",
        "fn_create_tariff(uuid, uuid, text, date, date, text, uuid, jsonb)",
        "fn_tariff_tiers(uuid)", "fn_get_tariff(uuid)", "fn_list_tariffs(uuid)",
        "fn_create_meter(uuid, uuid, uuid, text, text, date, numeric, text)",
        "fn_get_meter(uuid)", "fn_list_meters(uuid)", "fn_list_utilities()",
    ):
        op.execute(f"DROP FUNCTION IF EXISTS public.{signature}")
