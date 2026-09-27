"""Extend core tables and add gender-aware housing workflow."""

from alembic import op
import sqlalchemy as sa

revision = "20260921_0004"
down_revision = "20260921_0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    now = sa.text("CURRENT_TIMESTAMP")
    for name, column in (
        ("roles", sa.Column("display_name", sa.String(100))),
        ("roles", sa.Column("description", sa.String(300))),
        ("roles", sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False)),
        ("roles", sa.Column("created_at", sa.DateTime(timezone=True), server_default=now, nullable=False)),
        ("roles", sa.Column("updated_at", sa.DateTime(timezone=True), server_default=now, nullable=False)),
        ("permissions", sa.Column("description", sa.String(300))),
        ("permissions", sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False)),
        ("users", sa.Column("last_password_changed_at", sa.DateTime(timezone=True))),
        ("users", sa.Column("created_at", sa.DateTime(timezone=True), server_default=now, nullable=False)),
        ("users", sa.Column("created_by", sa.Uuid(), sa.ForeignKey("users.id"))),
        ("users", sa.Column("updated_at", sa.DateTime(timezone=True), server_default=now, nullable=False)),
        ("users", sa.Column("updated_by", sa.Uuid(), sa.ForeignKey("users.id"))),
        ("student_profiles", sa.Column("gender", sa.String(20))),
        ("student_profiles", sa.Column("identity_number", sa.String(30))),
        ("buildings", sa.Column("created_at", sa.DateTime(timezone=True), server_default=now, nullable=False)),
        ("buildings", sa.Column("created_by", sa.Uuid(), sa.ForeignKey("users.id"))),
        ("buildings", sa.Column("updated_at", sa.DateTime(timezone=True), server_default=now, nullable=False)),
        ("buildings", sa.Column("updated_by", sa.Uuid(), sa.ForeignKey("users.id"))),
        ("room_types", sa.Column("default_capacity", sa.Integer())),
        ("room_types", sa.Column("description", sa.String(500))),
        ("room_types", sa.Column("created_at", sa.DateTime(timezone=True), server_default=now, nullable=False)),
        ("room_types", sa.Column("updated_at", sa.DateTime(timezone=True), server_default=now, nullable=False)),
        ("rooms", sa.Column("gender_policy", sa.String(20), server_default="Unassigned", nullable=False)),
        ("rooms", sa.Column("managed_by_staff_id", sa.Uuid(), sa.ForeignKey("users.id"))),
        ("rooms", sa.Column("status", sa.String(20), server_default="Available", nullable=False)),
        ("rooms", sa.Column("note", sa.String(500))),
        ("rooms", sa.Column("created_at", sa.DateTime(timezone=True), server_default=now, nullable=False)),
        ("rooms", sa.Column("updated_at", sa.DateTime(timezone=True), server_default=now, nullable=False)),
        ("rooms", sa.Column("updated_by", sa.Uuid(), sa.ForeignKey("users.id"))),
        ("beds", sa.Column("note", sa.String(300))),
        ("beds", sa.Column("created_at", sa.DateTime(timezone=True), server_default=now, nullable=False)),
        ("beds", sa.Column("updated_at", sa.DateTime(timezone=True), server_default=now, nullable=False)),
        ("housing_applications", sa.Column("expected_start_date", sa.Date())),
        ("housing_applications", sa.Column("expected_end_date", sa.Date())),
        ("housing_applications", sa.Column("note", sa.String(1000))),
        ("housing_applications", sa.Column("cancelled_at", sa.DateTime(timezone=True))),
        ("contracts", sa.Column("issued_at", sa.DateTime(timezone=True))),
        ("contracts", sa.Column("issued_by", sa.Uuid(), sa.ForeignKey("users.id"))),
        ("contracts", sa.Column("termination_reason", sa.String(500))),
        ("contracts", sa.Column("created_at", sa.DateTime(timezone=True), server_default=now, nullable=False)),
        ("contracts", sa.Column("updated_at", sa.DateTime(timezone=True), server_default=now, nullable=False)),
        ("bed_assignments", sa.Column("assigned_by", sa.Uuid(), sa.ForeignKey("users.id"))),
        ("bed_assignments", sa.Column("ended_by", sa.Uuid(), sa.ForeignKey("users.id"))),
        ("bed_assignments", sa.Column("end_reason", sa.String(500))),
        ("bed_assignments", sa.Column("created_at", sa.DateTime(timezone=True), server_default=now, nullable=False)),
    ):
        op.add_column(name, column)
    op.create_index("ix_rooms_managed_by_staff_id", "rooms", ["managed_by_staff_id"])
    op.create_check_constraint("ck_rooms_gender_policy", "rooms", "gender_policy IN ('Male','Female','Mixed','Unassigned')")
    op.create_check_constraint("ck_rooms_status", "rooms", "status IN ('Available','Maintenance','Inactive')")
    op.create_check_constraint("ck_applications_expected_period", "housing_applications", "expected_end_date IS NULL OR expected_start_date IS NULL OR expected_end_date >= expected_start_date")
    op.create_check_constraint("ck_contracts_period", "contracts", "end_date >= start_date")
    op.create_check_constraint("ck_contracts_base_rate", "contracts", "base_rate >= 0")
    op.create_check_constraint("ck_assignments_period", "bed_assignments", "end_date IS NULL OR end_date >= start_date")
    op.create_index("uq_active_assignment_contract", "bed_assignments", ["contract_id"], unique=True, postgresql_where=sa.text("status = 'Active'"))
    op.create_table(
        "room_transfer_requests",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("contract_id", sa.Uuid(), sa.ForeignKey("contracts.id"), nullable=False),
        sa.Column("student_id", sa.Uuid(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("current_bed_id", sa.Uuid(), sa.ForeignKey("beds.id"), nullable=False),
        sa.Column("preferred_room_type_id", sa.Uuid(), sa.ForeignKey("room_types.id")),
        sa.Column("preferred_building_id", sa.Uuid(), sa.ForeignKey("buildings.id")),
        sa.Column("requested_bed_id", sa.Uuid(), sa.ForeignKey("beds.id")),
        sa.Column("reason", sa.String(1000), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="Submitted"),
        sa.Column("reviewed_by", sa.Uuid(), sa.ForeignKey("users.id")),
        sa.Column("reviewed_at", sa.DateTime(timezone=True)),
        sa.Column("rejection_reason", sa.String(500)),
        sa.Column("assigned_bed_id", sa.Uuid(), sa.ForeignKey("beds.id")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=now, nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=now, nullable=False),
    )
    op.create_index("ix_transfer_contract", "room_transfer_requests", ["contract_id"])
    op.create_index("ix_transfer_student", "room_transfer_requests", ["student_id"])
    op.create_index("uq_submitted_transfer_contract", "room_transfer_requests", ["contract_id"], unique=True, postgresql_where=sa.text("status = 'Submitted'"))
    op.create_table(
        "contract_events",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("contract_id", sa.Uuid(), sa.ForeignKey("contracts.id"), nullable=False),
        sa.Column("event_type", sa.String(40), nullable=False),
        sa.Column("event_date", sa.Date(), nullable=False),
        sa.Column("old_status", sa.String(20)),
        sa.Column("new_status", sa.String(20), nullable=False),
        sa.Column("reason", sa.String(500)),
        sa.Column("event_data", sa.JSON()),
        sa.Column("created_by", sa.Uuid(), sa.ForeignKey("users.id")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=now, nullable=False),
    )
    op.create_index("ix_contract_events_contract", "contract_events", ["contract_id", "created_at"])


def downgrade() -> None:
    op.drop_table("contract_events")
    op.drop_table("room_transfer_requests")
    op.drop_index("uq_active_assignment_contract", table_name="bed_assignments")
    columns = {
        "bed_assignments": ["assigned_by", "ended_by", "end_reason", "created_at"],
        "contracts": ["issued_at", "issued_by", "termination_reason", "created_at", "updated_at"],
        "housing_applications": ["expected_start_date", "expected_end_date", "note", "cancelled_at"],
        "beds": ["note", "created_at", "updated_at"],
        "rooms": ["gender_policy", "managed_by_staff_id", "status", "note", "created_at", "updated_at", "updated_by"],
        "room_types": ["default_capacity", "description", "created_at", "updated_at"],
        "buildings": ["created_at", "created_by", "updated_at", "updated_by"],
        "student_profiles": ["gender", "identity_number"],
        "users": ["last_password_changed_at", "created_at", "created_by", "updated_at", "updated_by"],
        "permissions": ["description", "is_active"],
        "roles": ["display_name", "description", "is_active", "created_at", "updated_at"],
    }
    for table, names in columns.items():
        for name in names:
            op.drop_column(table, name)
