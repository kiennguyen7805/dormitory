"""Remove out-of-scope history tables and harden core indexes."""

from alembic import op
import sqlalchemy as sa

revision = "20260921_0009"
down_revision = "20260921_0008"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_table("audit_logs")
    op.drop_table("login_events")
    op.create_index("ix_rooms_scope", "rooms", ["managed_by_staff_id", "building_id", "floor"])
    op.create_index("ix_contracts_student_status_end", "contracts", ["student_id", "status", "end_date"])
    op.create_index("ix_assignments_bed_status_period", "bed_assignments", ["bed_id", "status", "start_date", "end_date"])


def downgrade() -> None:
    op.drop_index("ix_assignments_bed_status_period", table_name="bed_assignments")
    op.drop_index("ix_contracts_student_status_end", table_name="contracts")
    op.drop_index("ix_rooms_scope", table_name="rooms")
    op.create_table("login_events",
        sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("user_id", sa.Uuid(), sa.ForeignKey("users.id")),
        sa.Column("email", sa.String(254), nullable=False), sa.Column("succeeded", sa.Boolean(), nullable=False),
        sa.Column("ip_address", sa.String(64), nullable=False), sa.Column("user_agent", sa.String(500), nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )
    op.create_table("audit_logs",
        sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("actor_user_id", sa.Uuid(), sa.ForeignKey("users.id")),
        sa.Column("action", sa.String(100), nullable=False), sa.Column("entity_type", sa.String(80), nullable=False),
        sa.Column("entity_id", sa.String(64), nullable=False), sa.Column("before_data", sa.JSON()), sa.Column("after_data", sa.JSON()),
        sa.Column("correlation_id", sa.String(100)), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )
