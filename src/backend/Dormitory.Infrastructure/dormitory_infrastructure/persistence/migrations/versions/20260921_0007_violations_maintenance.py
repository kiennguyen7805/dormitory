"""Add violations and maintenance workflows."""

from alembic import op
import sqlalchemy as sa

revision = "20260921_0007"
down_revision = "20260921_0006"
branch_labels = None
depends_on = None
NOW = sa.text("CURRENT_TIMESTAMP")


def upgrade() -> None:
    op.create_table("violation_types",
        sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("code", sa.String(30), unique=True, nullable=False),
        sa.Column("name", sa.String(150), nullable=False), sa.Column("description", sa.String(1000)),
        sa.Column("default_fine_amount", sa.Numeric(14, 2), nullable=False), sa.Column("severity", sa.String(20), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=NOW, nullable=False),
        sa.CheckConstraint("default_fine_amount >= 0", name="ck_violation_types_fine"),
    )
    op.create_table("violations",
        sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("violation_no", sa.String(50), unique=True, nullable=False),
        sa.Column("student_id", sa.Uuid(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("contract_id", sa.Uuid(), sa.ForeignKey("contracts.id")),
        sa.Column("violation_type_id", sa.Uuid(), sa.ForeignKey("violation_types.id"), nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False), sa.Column("location", sa.String(200)),
        sa.Column("description", sa.String(2000), nullable=False), sa.Column("fine_amount", sa.Numeric(14, 2), nullable=False),
        sa.Column("status", sa.String(20), nullable=False), sa.Column("recorded_by", sa.Uuid(), sa.ForeignKey("users.id")),
        sa.Column("reviewed_by", sa.Uuid(), sa.ForeignKey("users.id")), sa.Column("reviewed_at", sa.DateTime(timezone=True)),
        sa.Column("rejection_reason", sa.String(500)), sa.Column("resolution_note", sa.String(1000)),
        sa.Column("bill_item_id", sa.Uuid(), sa.ForeignKey("bill_items.id"), unique=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=NOW, nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=NOW, nullable=False),
        sa.CheckConstraint("fine_amount >= 0", name="ck_violations_fine"),
    )
    op.create_index("ix_violations_student_status", "violations", ["student_id", "status", "occurred_at"])
    op.create_table("violation_evidences",
        sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("violation_id", sa.Uuid(), sa.ForeignKey("violations.id"), nullable=False),
        sa.Column("file_id", sa.Uuid(), sa.ForeignKey("stored_files.id"), nullable=False), sa.Column("description", sa.String(300)),
        sa.Column("uploaded_by", sa.Uuid(), sa.ForeignKey("users.id")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=NOW, nullable=False),
    )
    op.create_index("ix_violation_evidences_violation", "violation_evidences", ["violation_id"])
    op.create_table("maintenance_requests",
        sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("request_no", sa.String(50), unique=True, nullable=False),
        sa.Column("requester_id", sa.Uuid(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("building_id", sa.Uuid(), sa.ForeignKey("buildings.id")), sa.Column("room_id", sa.Uuid(), sa.ForeignKey("rooms.id")),
        sa.Column("bed_id", sa.Uuid(), sa.ForeignKey("beds.id")), sa.Column("title", sa.String(200), nullable=False),
        sa.Column("description", sa.String(2000), nullable=False), sa.Column("priority", sa.String(20), nullable=False),
        sa.Column("status", sa.String(30), nullable=False), sa.Column("assigned_to", sa.Uuid(), sa.ForeignKey("users.id")),
        sa.Column("deadline", sa.DateTime(timezone=True)), sa.Column("completed_at", sa.DateTime(timezone=True)),
        sa.Column("completion_note", sa.String(1000)), sa.Column("created_at", sa.DateTime(timezone=True), server_default=NOW, nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=NOW, nullable=False),
        sa.CheckConstraint("building_id IS NOT NULL OR room_id IS NOT NULL OR bed_id IS NOT NULL", name="ck_maintenance_location"),
    )
    op.create_index("ix_maintenance_requester", "maintenance_requests", ["requester_id", "status", "created_at"])
    op.create_index("ix_maintenance_assignee", "maintenance_requests", ["assigned_to", "status", "created_at"])
    op.create_table("maintenance_events",
        sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("request_id", sa.Uuid(), sa.ForeignKey("maintenance_requests.id"), nullable=False),
        sa.Column("event_type", sa.String(30), nullable=False), sa.Column("old_status", sa.String(30)), sa.Column("new_status", sa.String(30)),
        sa.Column("comment", sa.String(2000)), sa.Column("file_id", sa.Uuid(), sa.ForeignKey("stored_files.id")),
        sa.Column("created_by", sa.Uuid(), sa.ForeignKey("users.id")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=NOW, nullable=False),
    )
    op.create_index("ix_maintenance_events_request", "maintenance_events", ["request_id", "created_at"])
    op.create_table("maintenance_plans",
        sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("code", sa.String(50), unique=True, nullable=False),
        sa.Column("title", sa.String(200), nullable=False), sa.Column("building_id", sa.Uuid(), sa.ForeignKey("buildings.id")),
        sa.Column("room_id", sa.Uuid(), sa.ForeignKey("rooms.id")), sa.Column("bed_id", sa.Uuid(), sa.ForeignKey("beds.id")),
        sa.Column("description", sa.String(2000), nullable=False), sa.Column("frequency_type", sa.String(20), nullable=False),
        sa.Column("frequency_interval", sa.Integer(), nullable=False), sa.Column("next_due_date", sa.Date(), nullable=False),
        sa.Column("assigned_to", sa.Uuid(), sa.ForeignKey("users.id")), sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=NOW, nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=NOW, nullable=False),
        sa.CheckConstraint("frequency_interval > 0", name="ck_maintenance_plan_interval"),
    )


def downgrade() -> None:
    for table in ("maintenance_plans", "maintenance_events", "maintenance_requests", "violation_evidences", "violations", "violation_types"):
        op.drop_table(table)
