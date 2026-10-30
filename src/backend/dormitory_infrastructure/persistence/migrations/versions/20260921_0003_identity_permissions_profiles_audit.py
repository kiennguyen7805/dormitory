"""Add permissions, student profiles and audit history.

Revision ID: 20260921_0003
Revises: 20260919_0002
"""

from alembic import op
import sqlalchemy as sa

revision = "20260921_0003"
down_revision = "20260919_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "permissions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(100), nullable=False),
        sa.Column("name", sa.String(150), nullable=False),
        sa.Column("module", sa.String(50), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )
    op.create_index("ix_permissions_code", "permissions", ["code"], unique=True)
    op.create_index("ix_permissions_module", "permissions", ["module"])
    op.create_table(
        "role_permissions",
        sa.Column("role_id", sa.Uuid(), nullable=False),
        sa.Column("permission_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"]),
        sa.ForeignKeyConstraint(["permission_id"], ["permissions.id"]),
        sa.PrimaryKeyConstraint("role_id", "permission_id"),
    )
    op.create_table(
        "student_profiles",
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("student_code", sa.String(30), nullable=False),
        sa.Column("faculty", sa.String(150), server_default="", nullable=False),
        sa.Column("cohort", sa.String(30), server_default="", nullable=False),
        sa.Column("date_of_birth", sa.Date()),
        sa.Column("phone", sa.String(30), server_default="", nullable=False),
        sa.Column("address", sa.String(300), server_default="", nullable=False),
        sa.Column("emergency_contact_name", sa.String(120), server_default="", nullable=False),
        sa.Column("emergency_contact_phone", sa.String(30), server_default="", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("user_id"),
        sa.UniqueConstraint("student_code"),
    )
    op.create_index("ix_student_profiles_student_code", "student_profiles", ["student_code"], unique=True)
    op.create_table(
        "login_events",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid()),
        sa.Column("email", sa.String(254), nullable=False),
        sa.Column("succeeded", sa.Boolean(), nullable=False),
        sa.Column("ip_address", sa.String(64), server_default="", nullable=False),
        sa.Column("user_agent", sa.String(500), server_default="", nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    for column in ("user_id", "email", "succeeded", "occurred_at"):
        op.create_index(f"ix_login_events_{column}", "login_events", [column])
    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("actor_user_id", sa.Uuid()),
        sa.Column("action", sa.String(100), nullable=False),
        sa.Column("entity_type", sa.String(80), nullable=False),
        sa.Column("entity_id", sa.String(64), nullable=False),
        sa.Column("before_data", sa.JSON()),
        sa.Column("after_data", sa.JSON()),
        sa.Column("correlation_id", sa.String(100)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["actor_user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    for column in ("actor_user_id", "action", "entity_type", "entity_id", "correlation_id", "created_at"):
        op.create_index(f"ix_audit_logs_{column}", "audit_logs", [column])


def downgrade() -> None:
    op.drop_table("audit_logs")
    op.drop_table("login_events")
    op.drop_table("student_profiles")
    op.drop_table("role_permissions")
    op.drop_table("permissions")
