from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field, model_validator

from dormitory_domain.billing import TariffTier, validate_tariff_tiers


class UtilityRead(BaseModel):
    id: UUID
    code: str
    name: str
    unit: str
    rounding_scale: int
    is_active: bool


class MeterCreate(BaseModel):
    utility_id: UUID
    room_id: UUID
    meter_code: str = Field(min_length=1, max_length=50)
    serial_number: str | None = Field(default=None, max_length=100)
    installed_at: date | None = None
    initial_reading: Decimal = Field(default=Decimal("0"), ge=0)
    note: str | None = Field(default=None, max_length=500)


class MeterRead(BaseModel):
    id: UUID
    utility_id: UUID
    utility_code: str
    utility_name: str
    room_id: UUID
    room_label: str
    meter_code: str
    serial_number: str | None
    initial_reading: Decimal
    is_active: bool


class TariffTierInput(BaseModel):
    tier_order: int = Field(ge=1)
    from_quantity: Decimal = Field(ge=0)
    to_quantity: Decimal | None = Field(default=None, gt=0)
    unit_price: Decimal = Field(ge=0)


class UtilityTariffCreate(BaseModel):
    utility_id: UUID
    name: str = Field(min_length=1, max_length=120)
    effective_from: date
    effective_to: date | None = None
    calculation_type: str = Field(default="Tiered", pattern="^(Flat|Tiered)$")
    tiers: list[TariffTierInput] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_period_and_tiers(self):
        if self.effective_to is not None and self.effective_to < self.effective_from:
            raise ValueError("Ngày kết thúc biểu giá phải sau ngày bắt đầu.")
        validate_tariff_tiers(
            [
                TariffTier(
                    tier_order=item.tier_order,
                    from_quantity=item.from_quantity,
                    to_quantity=item.to_quantity,
                    unit_price=item.unit_price,
                )
                for item in self.tiers
            ],
            self.calculation_type,
        )
        return self


class TariffTierRead(TariffTierInput):
    id: UUID


class UtilityTariffRead(BaseModel):
    id: UUID
    utility_id: UUID
    utility_code: str
    utility_name: str
    name: str
    effective_from: date
    effective_to: date | None
    calculation_type: str
    is_active: bool
    tiers: list[TariffTierRead]


class MeterReadingCreate(BaseModel):
    meter_id: UUID
    period_start: date
    period_end: date
    previous_reading: Decimal = Field(ge=0)
    current_reading: Decimal = Field(ge=0)

    @model_validator(mode="after")
    def validate_reading(self):
        if self.period_end < self.period_start:
            raise ValueError("Ngày kết thúc kỳ phải từ ngày bắt đầu trở đi.")
        if self.current_reading < self.previous_reading:
            raise ValueError("Chỉ số hiện tại không được nhỏ hơn chỉ số trước.")
        return self


class MeterReadingRead(BaseModel):
    id: UUID
    meter_id: UUID
    meter_code: str
    utility_code: str
    period_start: date
    period_end: date
    previous_reading: Decimal
    current_reading: Decimal
    consumption: Decimal
    calculated_amount: Decimal
    tariff_id: UUID
    tariff_snapshot: dict
    recorded_at: datetime
