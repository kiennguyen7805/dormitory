"""Read housing inventory through PostgreSQL functions."""

from importlib.resources import files

from alembic import op

revision = "20260928_0016"
down_revision = "20260928_0015"
branch_labels = None
depends_on = None


def upgrade() -> None:
    statements = (
        files("dormitory_infrastructure.persistence")
        .joinpath("sql", "housing_reads.sql")
        .read_text(encoding="utf-8")
        .split("-- NEXT STATEMENT")
    )
    for statement in statements:
        op.execute(statement.strip())


def downgrade() -> None:
    for signature in (
        "fn_get_bed(uuid)", "fn_list_beds(uuid, uuid)",
        "fn_get_room(uuid)", "fn_list_rooms(uuid, uuid)", "fn_get_room_type(uuid)",
        "fn_list_room_types()", "fn_get_building(uuid)", "fn_list_buildings()",
    ):
        op.execute(f"DROP FUNCTION IF EXISTS public.{signature}")
