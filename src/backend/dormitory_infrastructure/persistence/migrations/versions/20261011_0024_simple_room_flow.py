"""Room application and one electricity/water bill per room and period."""

from importlib.resources import files

from alembic import op
import sqlalchemy as sa

revision = "20261011_0024"
down_revision = "20261011_0023"
branch_labels = None
depends_on = None


def _install(filename: str) -> None:
    sql = files("dormitory_infrastructure.persistence").joinpath("sql", filename).read_text(encoding="utf-8")
    for statement in sql.split("-- NEXT STATEMENT"):
        if statement.strip():
            op.execute(statement.strip())


def upgrade() -> None:
    op.add_column("housing_applications", sa.Column("requested_room_id", sa.Uuid(), sa.ForeignKey("rooms.id")))
    op.add_column("bills", sa.Column("room_id", sa.Uuid(), sa.ForeignKey("rooms.id")))
    op.add_column("bills", sa.Column("payment_method", sa.String(30)))
    op.add_column("bills", sa.Column("payment_reference", sa.String(100)))
    op.add_column("bills", sa.Column("paid_at", sa.DateTime(timezone=True)))
    op.add_column("bills", sa.Column("payment_recorded_by", sa.Uuid(), sa.ForeignKey("users.id")))
    op.alter_column("bills", "contract_id", nullable=True)
    op.alter_column("bills", "student_id", nullable=True)
    op.create_index("uq_nonvoid_room_bill_period", "bills", ["room_id", "period_start", "period_end"],
                    unique=True, postgresql_where=sa.text("room_id IS NOT NULL AND status <> 'Void'"))
    op.execute("DROP FUNCTION IF EXISTS public.fn_get_room(uuid)")
    op.execute("DROP FUNCTION IF EXISTS public.fn_list_rooms(uuid, uuid)")
    op.execute("DROP FUNCTION IF EXISTS public.fn_get_application(uuid)")
    op.execute("DROP FUNCTION IF EXISTS public.fn_list_applications(uuid, text, text)")
    op.execute("DROP FUNCTION IF EXISTS public.fn_create_application(uuid, uuid, text, uuid)")
    op.execute("DROP FUNCTION IF EXISTS public.fn_assign_bed(uuid, uuid, uuid, text, uuid, date, date)")
    op.execute("DROP FUNCTION IF EXISTS public.fn_generate_bill(uuid, text, uuid, date, date, date, date, text, uuid)")
    _install("room_billing.sql")


def downgrade() -> None:
    raise RuntimeError("The simplified room workflow migration is forward only")
