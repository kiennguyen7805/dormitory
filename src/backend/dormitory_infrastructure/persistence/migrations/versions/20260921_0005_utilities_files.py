"""Add utilities, metering, tariff and file metadata tables."""

from alembic import op
import sqlalchemy as sa

revision = "20260921_0005"
down_revision = "20260921_0004"
branch_labels = None
depends_on = None
NOW = sa.text("CURRENT_TIMESTAMP")


def upgrade() -> None:
    op.create_table("stored_files",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("storage_provider", sa.String(30), nullable=False),
        sa.Column("storage_key", sa.String(500), nullable=False, unique=True),
        sa.Column("original_name", sa.String(255), nullable=False),
        sa.Column("content_type", sa.String(150), nullable=False),
        sa.Column("size_bytes", sa.BigInteger(), nullable=False),
        sa.Column("checksum_sha256", sa.String(64)),
        sa.Column("uploaded_by", sa.Uuid(), sa.ForeignKey("users.id")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=NOW, nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True)),
        sa.CheckConstraint("size_bytes > 0", name="ck_stored_files_size"),
    )
    op.create_table("utilities",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("code", sa.String(30), nullable=False, unique=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("unit", sa.String(30), nullable=False),
        sa.Column("rounding_scale", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=NOW, nullable=False),
        sa.CheckConstraint("rounding_scale >= 0", name="ck_utilities_rounding"),
    )
    op.create_table("meters",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("utility_id", sa.Uuid(), sa.ForeignKey("utilities.id"), nullable=False),
        sa.Column("room_id", sa.Uuid(), sa.ForeignKey("rooms.id"), nullable=False),
        sa.Column("meter_code", sa.String(50), nullable=False, unique=True),
        sa.Column("serial_number", sa.String(100)), sa.Column("installed_at", sa.Date()),
        sa.Column("initial_reading", sa.Numeric(14, 3), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("retired_at", sa.Date()), sa.Column("note", sa.String(500)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=NOW, nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=NOW, nullable=False),
        sa.CheckConstraint("initial_reading >= 0", name="ck_meters_initial"),
    )
    op.create_index("ix_meters_room_id", "meters", ["room_id"])
    op.create_table("utility_tariffs",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("utility_id", sa.Uuid(), sa.ForeignKey("utilities.id"), nullable=False),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("effective_from", sa.Date(), nullable=False), sa.Column("effective_to", sa.Date()),
        sa.Column("calculation_type", sa.String(20), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("created_by", sa.Uuid(), sa.ForeignKey("users.id")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=NOW, nullable=False),
        sa.CheckConstraint("effective_to IS NULL OR effective_to >= effective_from", name="ck_tariffs_period"),
        sa.CheckConstraint("calculation_type IN ('Flat','Tiered')", name="ck_tariffs_type"),
    )
    op.create_index("ix_tariffs_utility", "utility_tariffs", ["utility_id", "effective_from"])
    op.create_table("tariff_tiers",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("tariff_id", sa.Uuid(), sa.ForeignKey("utility_tariffs.id"), nullable=False),
        sa.Column("tier_order", sa.Integer(), nullable=False),
        sa.Column("from_quantity", sa.Numeric(14, 3), nullable=False),
        sa.Column("to_quantity", sa.Numeric(14, 3)),
        sa.Column("unit_price", sa.Numeric(14, 2), nullable=False),
        sa.UniqueConstraint("tariff_id", "tier_order", name="uq_tariff_tiers_order"),
        sa.CheckConstraint("tier_order > 0 AND from_quantity >= 0 AND unit_price >= 0", name="ck_tariff_tiers_positive"),
        sa.CheckConstraint("to_quantity IS NULL OR to_quantity > from_quantity", name="ck_tariff_tiers_range"),
    )
    op.create_table("utility_import_batches",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("file_id", sa.Uuid(), sa.ForeignKey("stored_files.id")),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("total_rows", sa.Integer(), nullable=False), sa.Column("valid_rows", sa.Integer(), nullable=False),
        sa.Column("invalid_rows", sa.Integer(), nullable=False), sa.Column("preview_rows", sa.JSON()),
        sa.Column("created_by", sa.Uuid(), sa.ForeignKey("users.id")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=NOW, nullable=False),
        sa.Column("confirmed_at", sa.DateTime(timezone=True)),
        sa.CheckConstraint("total_rows >= 0 AND valid_rows >= 0 AND invalid_rows >= 0", name="ck_import_counts"),
    )
    op.create_table("meter_readings",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("meter_id", sa.Uuid(), sa.ForeignKey("meters.id"), nullable=False),
        sa.Column("period_start", sa.Date(), nullable=False), sa.Column("period_end", sa.Date(), nullable=False),
        sa.Column("previous_reading", sa.Numeric(14, 3), nullable=False),
        sa.Column("current_reading", sa.Numeric(14, 3), nullable=False),
        sa.Column("consumption", sa.Numeric(14, 3), nullable=False),
        sa.Column("tariff_id", sa.Uuid(), sa.ForeignKey("utility_tariffs.id"), nullable=False),
        sa.Column("tariff_snapshot", sa.JSON(), nullable=False),
        sa.Column("calculated_amount", sa.Numeric(14, 2), nullable=False),
        sa.Column("source", sa.String(20), nullable=False),
        sa.Column("import_batch_id", sa.Uuid(), sa.ForeignKey("utility_import_batches.id")),
        sa.Column("recorded_by", sa.Uuid(), sa.ForeignKey("users.id")),
        sa.Column("recorded_at", sa.DateTime(timezone=True), server_default=NOW, nullable=False),
        sa.UniqueConstraint("meter_id", "period_start", "period_end", name="uq_meter_readings_period"),
        sa.CheckConstraint("period_end >= period_start", name="ck_readings_period"),
        sa.CheckConstraint("previous_reading >= 0 AND current_reading >= previous_reading AND consumption = current_reading - previous_reading AND calculated_amount >= 0", name="ck_readings_values"),
    )
    op.create_index("ix_meter_readings_meter", "meter_readings", ["meter_id", "period_end"])


def downgrade() -> None:
    for table in ("meter_readings", "utility_import_batches", "tariff_tiers", "utility_tariffs", "meters", "utilities", "stored_files"):
        op.drop_table(table)
