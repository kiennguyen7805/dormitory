"""Metering and tariff access through PostgreSQL stored functions."""

import json
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import text
from sqlalchemy.engine import Connection
from sqlalchemy.exc import IntegrityError

from dormitory_application.common import BusinessRuleError, NotFoundError
from dormitory_application.utilities import (
    MeterCreate, MeterRead, MeterReadingCreate, MeterReadingRead,
    TariffTierRead, UtilityRead, UtilityTariffCreate, UtilityTariffRead,
)
from dormitory_domain.billing import TariffTier, calculate_utility_charge


class StoredUtilityRepository:
    def __init__(self, db: Connection) -> None:
        self.db = db

    def _commit(self) -> None:
        self.db.commit()

    def _row(self, sql: str, **params):
        return self.db.execute(text(sql), params).mappings().first()

    def _rows(self, sql: str, **params):
        return self.db.execute(text(sql), params).mappings().all()

    def list_utilities(self) -> list[UtilityRead]:
        rows = self._rows("SELECT * FROM public.fn_list_utilities()")
        return [UtilityRead.model_validate(dict(row)) for row in rows]

    def _meter(self, meter_id: UUID) -> MeterRead | None:
        row = self._row("SELECT * FROM public.fn_get_meter(:meter_id)", meter_id=meter_id)
        return MeterRead.model_validate(dict(row)) if row else None

    def list_meters(self, room_id: UUID | None = None) -> list[MeterRead]:
        rows = self._rows("SELECT * FROM public.fn_list_meters(:room_id)", room_id=room_id)
        return [MeterRead.model_validate(dict(row)) for row in rows]

    def create_meter(self, data: MeterCreate) -> MeterRead:
        meter_id = uuid4()
        try:
            result = self.db.scalar(
                text("SELECT public.fn_create_meter(:id, :utility_id, :room_id, "
                     ":meter_code, :serial_number, :installed_at, :initial_reading, :note)"),
                {
                    "id": meter_id, "utility_id": data.utility_id, "room_id": data.room_id,
                    "meter_code": data.meter_code.strip().upper(),
                    "serial_number": data.serial_number.strip() if data.serial_number else None,
                    "installed_at": data.installed_at,
                    "initial_reading": data.initial_reading, "note": data.note,
                },
            )
            if result != "OK":
                if result in {"UTILITY_NOT_FOUND", "ROOM_NOT_FOUND"}:
                    raise NotFoundError("Utility not found" if result == "UTILITY_NOT_FOUND" else "Room not found")
                raise BusinessRuleError(result, result)
            self._commit()
        except IntegrityError as exc:
            self.db.rollback()
            raise BusinessRuleError(
                "UTILITY_DATA_CONFLICT", "Dữ liệu công tơ, biểu giá hoặc chỉ số bị trùng."
            ) from exc
        return self._meter(meter_id)

    def _tiers(self, tariff_id: UUID) -> list[TariffTierRead]:
        rows = self._rows("SELECT * FROM public.fn_tariff_tiers(:tariff_id)", tariff_id=tariff_id)
        return [TariffTierRead.model_validate(dict(row)) for row in rows]

    def _tariff(self, row) -> UtilityTariffRead:
        return UtilityTariffRead(
            id=row["id"], utility_id=row["utility_id"],
            utility_code=row["utility_code"], utility_name=row["utility_name"],
            name=row["name"], effective_from=row["effective_from"],
            effective_to=row["effective_to"], calculation_type=row["calculation_type"],
            is_active=row["is_active"], tiers=self._tiers(row["id"]),
        )

    def _tariff_row(self, tariff_id: UUID):
        return self._row("SELECT * FROM public.fn_get_tariff(:tariff_id)", tariff_id=tariff_id)

    def list_tariffs(self, utility_id: UUID | None = None) -> list[UtilityTariffRead]:
        rows = self._rows("SELECT * FROM public.fn_list_tariffs(:utility_id)", utility_id=utility_id)
        return [self._tariff(row) for row in rows]

    def create_tariff(self, data: UtilityTariffCreate, user_id: UUID) -> UtilityTariffRead:
        tariff_id = uuid4()
        try:
            result = self.db.scalar(
                text("SELECT public.fn_create_tariff(:id, :utility_id, :name, "
                     ":effective_from, :effective_to, :calculation_type, :created_by, "
                     "CAST(:tiers AS jsonb))"),
                {
                    "id": tariff_id, "utility_id": data.utility_id,
                    "name": data.name.strip(), "effective_from": data.effective_from,
                    "effective_to": data.effective_to,
                    "calculation_type": data.calculation_type, "created_by": user_id,
                    "tiers": json.dumps([
                        {"id": str(uuid4()), **{
                            key: str(value) if isinstance(value, Decimal) else value
                            for key, value in tier.model_dump().items()
                        }} for tier in data.tiers
                    ]),
                },
            )
            if result == "UTILITY_NOT_FOUND":
                raise NotFoundError("Utility not found")
            if result == "TARIFF_PERIOD_OVERLAP":
                raise BusinessRuleError(
                    result, "Khoảng hiệu lực của biểu giá bị trùng với biểu giá đang hoạt động."
                )
            if result != "OK":
                raise BusinessRuleError(result, result)
            self._commit()
        except IntegrityError as exc:
            self.db.rollback()
            raise BusinessRuleError(
                "UTILITY_DATA_CONFLICT", "Dữ liệu công tơ, biểu giá hoặc chỉ số bị trùng."
            ) from exc
        return self._tariff(self._tariff_row(tariff_id))

    def _find_tariff(self, utility_id: UUID, period_end: date):
        row = self._row("SELECT * FROM public.fn_find_tariff(:utility_id, :period_end)",
                        utility_id=utility_id, period_end=period_end)
        if row is None:
            raise BusinessRuleError(
                "TARIFF_NOT_FOUND",
                "Không có biểu giá hiệu lực tại ngày kết thúc kỳ ghi chỉ số.",
            )
        return row

    def _reading(self, reading_id: UUID) -> MeterReadingRead:
        row = self._row("SELECT * FROM public.fn_get_reading(:reading_id)",
                        reading_id=reading_id)
        return MeterReadingRead.model_validate(dict(row))

    def create_reading(self, data: MeterReadingCreate, user_id: UUID) -> MeterReadingRead:
        meter = self._row(
            "SELECT * FROM public.fn_reading_context(:meter_id, :period_start, :period_end)",
            meter_id=data.meter_id, period_start=data.period_start, period_end=data.period_end,
        )
        if meter is None or not meter["is_active"]:
            raise NotFoundError("Meter not found")
        if meter["duplicate_id"]:
            raise BusinessRuleError(
                "METER_READING_ALREADY_EXISTS", "Công tơ đã có chỉ số trong kỳ này."
            )
        expected_previous = (meter["previous_reading"] if meter["previous_reading"] is not None
                             else meter["initial_reading"])
        if data.previous_reading != expected_previous:
            raise BusinessRuleError(
                "PREVIOUS_READING_MISMATCH",
                f"Chỉ số đầu kỳ phải bằng {expected_previous}.", 422,
            )
        tariff = self._find_tariff(meter["utility_id"], data.period_end)
        tier_models = self._tiers(tariff["id"])
        tiers = [
            TariffTier(t.tier_order, t.from_quantity, t.to_quantity, t.unit_price)
            for t in tier_models
        ]
        consumption = data.current_reading - data.previous_reading
        calculation = calculate_utility_charge(consumption, tiers, tariff["calculation_type"])
        snapshot = {
            "tariff_id": str(tariff["id"]),
            "name": tariff["name"],
            "calculation_type": tariff["calculation_type"],
            "effective_from": tariff["effective_from"].isoformat(),
            "effective_to": tariff["effective_to"].isoformat() if tariff["effective_to"] else None,
            "tiers": [
                {
                    "tier_order": tier.tier_order,
                    "from_quantity": str(tier.from_quantity),
                    "to_quantity": str(tier.to_quantity) if tier.to_quantity is not None else None,
                    "unit_price": str(tier.unit_price),
                }
                for tier in tiers
            ],
            "breakdown": [
                {
                    "tier_order": charge.tier_order,
                    "billed_quantity": str(charge.billed_quantity),
                    "unit_price": str(charge.unit_price),
                    "amount": str(charge.amount),
                }
                for charge in calculation.breakdown
            ],
        }
        reading_id = uuid4()
        try:
            result = self.db.scalar(
                text("SELECT public.fn_create_reading(:id, :meter_id, :period_start, "
                     ":period_end, :previous_reading, :current_reading, :consumption, "
                     ":tariff_id, CAST(:tariff_snapshot AS json), :calculated_amount, "
                     ":recorded_by)"),
                {
                    "id": reading_id, "meter_id": data.meter_id,
                    "period_start": data.period_start, "period_end": data.period_end,
                    "previous_reading": data.previous_reading,
                    "current_reading": data.current_reading,
                    "consumption": calculation.consumption,
                    "tariff_id": tariff["id"],
                    "tariff_snapshot": json.dumps(snapshot, ensure_ascii=False),
                    "calculated_amount": calculation.total_amount,
                    "recorded_by": user_id,
                },
            )
            if result == "METER_NOT_FOUND":
                raise NotFoundError("Meter not found")
            if result == "METER_READING_ALREADY_EXISTS":
                raise BusinessRuleError(result, "Công tơ đã có chỉ số trong kỳ này.")
            if result == "PREVIOUS_READING_MISMATCH":
                raise BusinessRuleError(result, "Chỉ số đầu kỳ không khớp.", 422)
            if result == "TARIFF_NOT_FOUND":
                raise BusinessRuleError(result, "Không có biểu giá hiệu lực tại ngày kết thúc kỳ ghi chỉ số.")
            if result != "OK":
                raise BusinessRuleError(result, result)
            self._commit()
        except IntegrityError as exc:
            self.db.rollback()
            raise BusinessRuleError(
                "UTILITY_DATA_CONFLICT", "Dữ liệu công tơ, biểu giá hoặc chỉ số bị trùng."
            ) from exc
        return self._reading(reading_id)

    def list_readings(
        self, meter_id: UUID | None = None, period_start: date | None = None
    ) -> list[MeterReadingRead]:
        rows = self._rows("SELECT * FROM public.fn_list_readings(:meter_id, :period_start)",
                          meter_id=meter_id, period_start=period_start)
        return [MeterReadingRead.model_validate(dict(row)) for row in rows]
