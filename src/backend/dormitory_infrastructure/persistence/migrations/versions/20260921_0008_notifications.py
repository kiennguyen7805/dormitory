"""Add notifications, targeting and read tracking."""

from alembic import op
import sqlalchemy as sa

revision = "20260921_0008"
down_revision = "20260921_0007"
branch_labels = None
depends_on = None


def upgrade() -> None:
    now = sa.text("CURRENT_TIMESTAMP")
    op.create_table("notifications",
        sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("title", sa.String(200), nullable=False),
        sa.Column("content", sa.Text(), nullable=False), sa.Column("status", sa.String(20), nullable=False),
        sa.Column("priority", sa.String(20), nullable=False), sa.Column("published_at", sa.DateTime(timezone=True)),
        sa.Column("expires_at", sa.DateTime(timezone=True)), sa.Column("created_by", sa.Uuid(), sa.ForeignKey("users.id")),
        sa.Column("published_by", sa.Uuid(), sa.ForeignKey("users.id")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=now, nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=now, nullable=False),
        sa.CheckConstraint("expires_at IS NULL OR published_at IS NULL OR expires_at > published_at", name="ck_notifications_period"),
    )
    op.create_index("ix_notifications_status_time", "notifications", ["status", "published_at", "expires_at"])
    op.create_table("notification_targets",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("notification_id", sa.Uuid(), sa.ForeignKey("notifications.id"), nullable=False),
        sa.Column("target_type", sa.String(20), nullable=False),
        sa.Column("role_id", sa.Uuid(), sa.ForeignKey("roles.id")), sa.Column("building_id", sa.Uuid(), sa.ForeignKey("buildings.id")),
        sa.Column("room_id", sa.Uuid(), sa.ForeignKey("rooms.id")), sa.Column("user_id", sa.Uuid(), sa.ForeignKey("users.id")),
        sa.CheckConstraint("""(target_type = 'All' AND role_id IS NULL AND building_id IS NULL AND room_id IS NULL AND user_id IS NULL)
            OR (target_type = 'Role' AND role_id IS NOT NULL AND building_id IS NULL AND room_id IS NULL AND user_id IS NULL)
            OR (target_type = 'Building' AND role_id IS NULL AND building_id IS NOT NULL AND room_id IS NULL AND user_id IS NULL)
            OR (target_type = 'Room' AND role_id IS NULL AND building_id IS NULL AND room_id IS NOT NULL AND user_id IS NULL)
            OR (target_type = 'User' AND role_id IS NULL AND building_id IS NULL AND room_id IS NULL AND user_id IS NOT NULL)""", name="ck_notification_target_exactly_one"),
    )
    op.create_index("ix_notification_targets_notification", "notification_targets", ["notification_id"])
    op.create_table("notification_reads",
        sa.Column("notification_id", sa.Uuid(), sa.ForeignKey("notifications.id"), primary_key=True),
        sa.Column("user_id", sa.Uuid(), sa.ForeignKey("users.id"), primary_key=True),
        sa.Column("read_at", sa.DateTime(timezone=True), server_default=now, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("notification_reads"); op.drop_table("notification_targets"); op.drop_table("notifications")
