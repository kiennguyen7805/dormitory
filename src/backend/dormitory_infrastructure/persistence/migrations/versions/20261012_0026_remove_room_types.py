"""Move room attributes onto rooms and remove the room_types table."""

from importlib.resources import files

from alembic import op
import sqlalchemy as sa


revision = "20261012_0026"
down_revision = "20261012_0025"
branch_labels = None
depends_on = None


def _install(filename: str) -> None:
    sql = (
        files("dormitory_infrastructure.persistence")
        .joinpath("sql", filename)
        .read_text(encoding="utf-8")
    )
    for statement in sql.split("-- NEXT STATEMENT"):
        if statement.strip():
            op.execute(statement.strip())


def upgrade() -> None:
    for signature in (
        "fn_list_room_types()",
        "fn_get_room_type(uuid)",
        "fn_list_rooms(uuid, uuid)",
        "fn_get_room(uuid)",
        "fn_create_simple_room(uuid, uuid, text, integer, integer, numeric)",
        "fn_create_application(uuid, uuid, text, uuid)",
        "fn_list_applications(uuid, text, text)",
        "fn_get_application(uuid)",
        "fn_assign_room(uuid, uuid, uuid, text, date, date)",
        "fn_assign_bed(uuid, uuid, uuid, text, uuid, date, date)",
    ):
        op.execute(f"DROP FUNCTION IF EXISTS public.{signature}")

    op.add_column("rooms", sa.Column("capacity", sa.Integer(), nullable=True))
    op.add_column("rooms", sa.Column("monthly_rate", sa.Numeric(14, 2), nullable=True))
    op.execute(
        """
        UPDATE rooms AS room
        SET capacity = COALESCE(
                room_type.default_capacity,
                (SELECT count(*)::integer FROM beds WHERE room_id = room.id),
                1
            ),
            monthly_rate = room_type.default_monthly_rate
        FROM room_types AS room_type
        WHERE room_type.id = room.room_type_id
        """
    )
    op.execute("UPDATE rooms SET capacity = 1 WHERE capacity IS NULL OR capacity < 1")
    op.execute("UPDATE rooms SET monthly_rate = 0 WHERE monthly_rate IS NULL")
    op.alter_column("rooms", "capacity", nullable=False)
    op.alter_column("rooms", "monthly_rate", nullable=False)
    op.create_check_constraint(
        "ck_rooms_capacity", "rooms", "capacity >= 1 AND capacity <= 12"
    )
    op.create_check_constraint(
        "ck_rooms_monthly_rate", "rooms", "monthly_rate >= 0"
    )

    op.execute(
        """
        UPDATE housing_applications AS application
        SET requested_room_id = (
            SELECT room.id
            FROM rooms AS room
            WHERE room.room_type_id = application.preferred_room_type_id
            ORDER BY room.code
            LIMIT 1
        )
        WHERE application.requested_room_id IS NULL
        """
    )

    op.execute(
        "ALTER TABLE housing_applications "
        "DROP CONSTRAINT IF EXISTS housing_applications_preferred_room_type_id_fkey"
    )
    op.drop_column("housing_applications", "preferred_room_type_id")
    op.execute(
        "ALTER TABLE rooms DROP CONSTRAINT IF EXISTS rooms_room_type_id_fkey"
    )
    op.drop_column("rooms", "room_type_id")
    op.drop_table("room_types")

    _install("housing_reads.sql")
    _install("housing_writes.sql")
    _install("contract_reads.sql")
    _install("contract_writes.sql")
    _install("simple_flow.sql")


def downgrade() -> None:
    raise RuntimeError("The room_types removal migration is forward only")
