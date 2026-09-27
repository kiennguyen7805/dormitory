"""Add billing and payments with integrated receipt snapshots."""

from alembic import op
import sqlalchemy as sa

revision = "20260921_0006"
down_revision = "20260921_0005"
branch_labels = None
depends_on = None
NOW = sa.text("CURRENT_TIMESTAMP")


def upgrade() -> None:
    op.create_table("bills",
        sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("bill_no", sa.String(50), nullable=False, unique=True),
        sa.Column("contract_id", sa.Uuid(), sa.ForeignKey("contracts.id"), nullable=False),
        sa.Column("student_id", sa.Uuid(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("period_start", sa.Date(), nullable=False), sa.Column("period_end", sa.Date(), nullable=False),
        sa.Column("issued_date", sa.Date(), nullable=False), sa.Column("due_date", sa.Date(), nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("subtotal", sa.Numeric(14, 2), nullable=False), sa.Column("adjustment_amount", sa.Numeric(14, 2), nullable=False),
        sa.Column("total_amount", sa.Numeric(14, 2), nullable=False), sa.Column("paid_amount", sa.Numeric(14, 2), nullable=False),
        sa.Column("balance_amount", sa.Numeric(14, 2), nullable=False),
        sa.Column("idempotency_key", sa.String(100), nullable=False, unique=True),
        sa.Column("issued_by", sa.Uuid(), sa.ForeignKey("users.id")), sa.Column("voided_by", sa.Uuid(), sa.ForeignKey("users.id")),
        sa.Column("voided_at", sa.DateTime(timezone=True)), sa.Column("void_reason", sa.String(500)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=NOW, nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=NOW, nullable=False),
        sa.CheckConstraint("period_end >= period_start AND due_date >= issued_date", name="ck_bills_dates"),
        sa.CheckConstraint("subtotal >= 0 AND total_amount >= 0 AND paid_amount >= 0 AND paid_amount <= total_amount AND balance_amount = total_amount - paid_amount", name="ck_bills_amounts"),
    )
    op.create_index("ix_bills_contract_period", "bills", ["contract_id", "period_start", "period_end"])
    op.create_index("ix_bills_student_status_due", "bills", ["student_id", "status", "due_date"])
    op.create_index("uq_nonvoid_bill_period", "bills", ["contract_id", "period_start", "period_end"], unique=True, postgresql_where=sa.text("status <> 'Void'"))
    op.create_table("bill_items",
        sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("bill_id", sa.Uuid(), sa.ForeignKey("bills.id"), nullable=False),
        sa.Column("item_type", sa.String(30), nullable=False), sa.Column("reference_type", sa.String(50)), sa.Column("reference_id", sa.Uuid()),
        sa.Column("description", sa.String(300), nullable=False), sa.Column("quantity", sa.Numeric(14, 3), nullable=False),
        sa.Column("unit_price", sa.Numeric(14, 2), nullable=False), sa.Column("amount", sa.Numeric(14, 2), nullable=False),
        sa.Column("calculation_snapshot", sa.JSON()), sa.Column("created_at", sa.DateTime(timezone=True), server_default=NOW, nullable=False),
        sa.CheckConstraint("quantity >= 0", name="ck_bill_items_quantity"),
    )
    op.create_index("ix_bill_items_bill", "bill_items", ["bill_id"])
    op.create_index("uq_bill_item_reference", "bill_items", ["bill_id", "reference_type", "reference_id"], unique=True, postgresql_where=sa.text("reference_id IS NOT NULL"))
    op.create_table("payments",
        sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("bill_id", sa.Uuid(), sa.ForeignKey("bills.id"), nullable=False),
        sa.Column("payment_no", sa.String(50), nullable=False, unique=True), sa.Column("amount", sa.Numeric(14, 2), nullable=False),
        sa.Column("method", sa.String(30), nullable=False), sa.Column("status", sa.String(20), nullable=False),
        sa.Column("paid_at", sa.DateTime(timezone=True), nullable=False), sa.Column("proof_file_id", sa.Uuid(), sa.ForeignKey("stored_files.id")),
        sa.Column("transaction_reference", sa.String(100), unique=True), sa.Column("recorded_by", sa.Uuid(), sa.ForeignKey("users.id")),
        sa.Column("reviewed_by", sa.Uuid(), sa.ForeignKey("users.id")), sa.Column("reviewed_at", sa.DateTime(timezone=True)),
        sa.Column("rejection_reason", sa.String(500)), sa.Column("receipt_no", sa.String(50), unique=True),
        sa.Column("receipt_issued_at", sa.DateTime(timezone=True)), sa.Column("receipt_issued_by", sa.Uuid(), sa.ForeignKey("users.id")),
        sa.Column("receipt_snapshot", sa.JSON()), sa.Column("created_at", sa.DateTime(timezone=True), server_default=NOW, nullable=False),
        sa.CheckConstraint("amount > 0", name="ck_payments_amount"),
        sa.CheckConstraint("status = 'Confirmed' OR (receipt_no IS NULL AND receipt_issued_at IS NULL AND receipt_issued_by IS NULL AND receipt_snapshot IS NULL)", name="ck_payment_receipt_confirmed"),
    )
    op.create_index("ix_payments_bill_status", "payments", ["bill_id", "status", "paid_at"])


def downgrade() -> None:
    op.drop_table("payments"); op.drop_table("bill_items"); op.drop_table("bills")
