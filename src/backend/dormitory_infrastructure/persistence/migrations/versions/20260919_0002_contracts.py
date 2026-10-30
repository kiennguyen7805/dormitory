"""Add housing applications, contracts and bed assignments.

Revision ID: 20260919_0002
Revises: 20260912_0001
Create Date: 2026-09-19
"""

from alembic import op
import sqlalchemy as sa

revision = "20260919_0002"
down_revision = "20260912_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "housing_applications",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("student_id", sa.Uuid(), nullable=False),
        sa.Column("term_code", sa.String(length=30), nullable=False),
        sa.Column("preferred_room_type_id", sa.Uuid(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("rejection_reason", sa.String(length=500), nullable=True),
        sa.Column("reviewed_by_user_id", sa.Uuid(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["preferred_room_type_id"], ["room_types.id"]),
        sa.ForeignKeyConstraint(["reviewed_by_user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["student_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_housing_applications_status"),
        "housing_applications",
        ["status"],
        unique=False,
    )
    op.create_index(
        op.f("ix_housing_applications_student_id"),
        "housing_applications",
        ["student_id"],
        unique=False,
    )
    op.create_table(
        "contracts",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("contract_no", sa.String(length=50), nullable=False),
        sa.Column("student_id", sa.Uuid(), nullable=False),
        sa.Column("application_id", sa.Uuid(), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("base_rate", sa.Numeric(14, 2), nullable=False),
        sa.Column("terminated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["application_id"], ["housing_applications.id"]),
        sa.ForeignKeyConstraint(["student_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("application_id"),
        sa.UniqueConstraint("contract_no"),
    )
    op.create_index(op.f("ix_contracts_status"), "contracts", ["status"], unique=False)
    op.create_index(
        op.f("ix_contracts_student_id"), "contracts", ["student_id"], unique=False
    )
    op.create_table(
        "bed_assignments",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("contract_id", sa.Uuid(), nullable=False),
        sa.Column("bed_id", sa.Uuid(), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.ForeignKeyConstraint(["bed_id"], ["beds.id"]),
        sa.ForeignKeyConstraint(["contract_id"], ["contracts.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_bed_assignments_bed_id"), "bed_assignments", ["bed_id"], unique=False
    )
    op.create_index(
        op.f("ix_bed_assignments_contract_id"),
        "bed_assignments",
        ["contract_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_bed_assignments_status"), "bed_assignments", ["status"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_bed_assignments_status"), table_name="bed_assignments")
    op.drop_index(op.f("ix_bed_assignments_contract_id"), table_name="bed_assignments")
    op.drop_index(op.f("ix_bed_assignments_bed_id"), table_name="bed_assignments")
    op.drop_table("bed_assignments")
    op.drop_index(op.f("ix_contracts_student_id"), table_name="contracts")
    op.drop_index(op.f("ix_contracts_status"), table_name="contracts")
    op.drop_table("contracts")
    op.drop_index(
        op.f("ix_housing_applications_student_id"),
        table_name="housing_applications",
    )
    op.drop_index(
        op.f("ix_housing_applications_status"),
        table_name="housing_applications",
    )
    op.drop_table("housing_applications")
