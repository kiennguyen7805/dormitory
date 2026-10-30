from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field, model_validator


class BillGenerateRequest(BaseModel):
    room_id: UUID
    period_start: date
    period_end: date
    issued_date: date
    due_date: date
    idempotency_key: str = Field(min_length=8, max_length=100)

    @model_validator(mode="after")
    def validate_dates(self):
        if self.period_end < self.period_start:
            raise ValueError("Ngày kết thúc kỳ phải từ ngày bắt đầu trở đi.")
        if self.due_date < self.issued_date:
            raise ValueError("Hạn thanh toán phải từ ngày phát hành trở đi.")
        return self


class BillItemRead(BaseModel):
    id: UUID
    item_type: str
    reference_type: str | None
    reference_id: UUID | None
    description: str
    quantity: Decimal
    unit_price: Decimal
    amount: Decimal
    calculation_snapshot: dict | None


class BillRead(BaseModel):
    id: UUID
    bill_no: str
    contract_id: UUID | None
    student_id: UUID | None
    room_id: UUID | None
    period_start: date
    period_end: date
    issued_date: date
    due_date: date
    status: str
    subtotal: Decimal
    adjustment_amount: Decimal
    total_amount: Decimal
    paid_amount: Decimal
    balance_amount: Decimal
    idempotency_key: str
    payment_method: str | None = None
    payment_reference: str | None = None
    paid_at: datetime | None = None
    items: list[BillItemRead]


class BillPaymentRequest(BaseModel):
    method: str = Field(min_length=1, max_length=30)
    reference: str | None = Field(default=None, max_length=100)
