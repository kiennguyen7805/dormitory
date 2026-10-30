from __future__ import annotations

from datetime import UTC, date, datetime
from decimal import Decimal
from hashlib import sha256
from io import BytesIO
from uuid import UUID, uuid4

from openpyxl import Workbook, load_workbook
from sqlalchemy import and_, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from dormitory_application.common import BusinessRuleError, NotFoundError
from dormitory_application.utilities import (
    ImportConfirmRead,
    ImportPreviewRead,
    ImportPreviewRow,
    MeterCreate,
    MeterRead,
    MeterReadingCreate,
    MeterReadingRead,
    TariffTierRead,
    UtilityRead,
    UtilityTariffCreate,
    UtilityTariffRead,
)
from dormitory_domain.billing import TariffTier, calculate_utility_charge

from .models import (
    BuildingModel,
    MeterModel,
    MeterReadingModel,
    RoomModel,
    StoredFileModel,
    TariffTierModel,
    UtilityImportBatchModel,
    UtilityModel,
    UtilityTariffModel,
)


def _decimal(value: object) -> Decimal:
    if value is None or value == "":
        raise ValueError("Thiếu giá trị số.")
    return Decimal(str(value))


def _date(value: object) -> date:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if value is None or value == "":
        raise ValueError("Thiếu ngày.")
    return date.fromisoformat(str(value).strip())


class SqlAlchemyUtilityRepository:
    TEMPLATE_HEADERS = (
        "meter_code",
        "period_start",
        "period_end",
        "previous_reading",
        "current_reading",
    )

    def __init__(self, db: Session) -> None:
        self.db = db

    def _commit(self) -> None:
        try:
            self.db.commit()
        except IntegrityError as exc:
            self.db.rollback()
            raise BusinessRuleError(
                "UTILITY_DATA_CONFLICT",
                "Dữ liệu công tơ, biểu giá hoặc chỉ số bị trùng.",
            ) from exc

    def list_utilities(self) -> list[UtilityRead]:
        items = self.db.scalars(
            select(UtilityModel).where(UtilityModel.is_active.is_(True)).order_by(UtilityModel.code)
        ).all()
        return [
            UtilityRead(
                id=item.id,
                code=item.code,
                name=item.name,
                unit=item.unit,
                rounding_scale=item.rounding_scale,
                is_active=item.is_active,
            )
            for item in items
        ]

    @staticmethod
    def _meter(item: MeterModel, utility: UtilityModel, room: RoomModel, building: BuildingModel) -> MeterRead:
        return MeterRead(
            id=item.id,
            utility_id=item.utility_id,
            utility_code=utility.code,
            utility_name=utility.name,
            room_id=item.room_id,
            room_label=f"{building.code}-{room.code}",
            meter_code=item.meter_code,
            serial_number=item.serial_number,
            initial_reading=item.initial_reading,
            is_active=item.is_active,
        )

    def list_meters(self, room_id: UUID | None = None) -> list[MeterRead]:
        statement = (
            select(MeterModel, UtilityModel, RoomModel, BuildingModel)
            .join(UtilityModel, UtilityModel.id == MeterModel.utility_id)
            .join(RoomModel, RoomModel.id == MeterModel.room_id)
            .join(BuildingModel, BuildingModel.id == RoomModel.building_id)
            .order_by(BuildingModel.code, RoomModel.code, UtilityModel.code)
        )
        if room_id:
            statement = statement.where(MeterModel.room_id == room_id)
        return [self._meter(*row) for row in self.db.execute(statement).all()]

    def create_meter(self, data: MeterCreate) -> MeterRead:
        utility = self.db.get(UtilityModel, data.utility_id)
        room = self.db.get(RoomModel, data.room_id)
        if utility is None or not utility.is_active:
            raise NotFoundError("Utility not found")
        if room is None or not room.is_active:
            raise NotFoundError("Room not found")
        item = MeterModel(
            utility_id=data.utility_id,
            room_id=data.room_id,
            meter_code=data.meter_code.strip().upper(),
            serial_number=data.serial_number.strip() if data.serial_number else None,
            installed_at=data.installed_at,
            initial_reading=data.initial_reading,
            note=data.note,
        )
        self.db.add(item)
        self._commit()
        building = self.db.get(BuildingModel, room.building_id)
        return self._meter(item, utility, room, building)

    def _tiers(self, tariff_id: UUID) -> list[TariffTierModel]:
        return list(
            self.db.scalars(
                select(TariffTierModel)
                .where(TariffTierModel.tariff_id == tariff_id)
                .order_by(TariffTierModel.tier_order)
            ).all()
        )

    def _tariff(self, item: UtilityTariffModel, utility: UtilityModel) -> UtilityTariffRead:
        return UtilityTariffRead(
            id=item.id,
            utility_id=item.utility_id,
            utility_code=utility.code,
            utility_name=utility.name,
            name=item.name,
            effective_from=item.effective_from,
            effective_to=item.effective_to,
            calculation_type=item.calculation_type,
            is_active=item.is_active,
            tiers=[
                TariffTierRead(
                    id=tier.id,
                    tier_order=tier.tier_order,
                    from_quantity=tier.from_quantity,
                    to_quantity=tier.to_quantity,
                    unit_price=tier.unit_price,
                )
                for tier in self._tiers(item.id)
            ],
        )

    def list_tariffs(self, utility_id: UUID | None = None) -> list[UtilityTariffRead]:
        statement = (
            select(UtilityTariffModel, UtilityModel)
            .join(UtilityModel, UtilityModel.id == UtilityTariffModel.utility_id)
            .order_by(UtilityModel.code, UtilityTariffModel.effective_from.desc())
        )
        if utility_id:
            statement = statement.where(UtilityTariffModel.utility_id == utility_id)
        return [self._tariff(*row) for row in self.db.execute(statement).all()]

    def create_tariff(self, data: UtilityTariffCreate, user_id: UUID) -> UtilityTariffRead:
        utility = self.db.get(UtilityModel, data.utility_id)
        if utility is None or not utility.is_active:
            raise NotFoundError("Utility not found")
        overlap_statement = select(UtilityTariffModel.id).where(
            UtilityTariffModel.utility_id == data.utility_id,
            UtilityTariffModel.is_active.is_(True),
            or_(
                UtilityTariffModel.effective_to.is_(None),
                UtilityTariffModel.effective_to >= data.effective_from,
            ),
        )
        if data.effective_to is not None:
            overlap_statement = overlap_statement.where(
                UtilityTariffModel.effective_from <= data.effective_to
            )
        overlap = self.db.scalar(overlap_statement.limit(1))
        if overlap:
            raise BusinessRuleError(
                "TARIFF_PERIOD_OVERLAP",
                "Khoảng hiệu lực của biểu giá bị trùng với biểu giá đang hoạt động.",
            )
        item = UtilityTariffModel(
            utility_id=data.utility_id,
            name=data.name.strip(),
            effective_from=data.effective_from,
            effective_to=data.effective_to,
            calculation_type=data.calculation_type,
            created_by=user_id,
        )
        self.db.add(item)
        self.db.flush()
        for tier in data.tiers:
            self.db.add(
                TariffTierModel(
                    tariff_id=item.id,
                    tier_order=tier.tier_order,
                    from_quantity=tier.from_quantity,
                    to_quantity=tier.to_quantity,
                    unit_price=tier.unit_price,
                )
            )
        self._commit()
        return self._tariff(item, utility)

    def _find_tariff(self, utility_id: UUID, period_end: date) -> UtilityTariffModel:
        tariff = self.db.scalar(
            select(UtilityTariffModel)
            .where(
                UtilityTariffModel.utility_id == utility_id,
                UtilityTariffModel.is_active.is_(True),
                UtilityTariffModel.effective_from <= period_end,
                or_(
                    UtilityTariffModel.effective_to.is_(None),
                    UtilityTariffModel.effective_to >= period_end,
                ),
            )
            .order_by(UtilityTariffModel.effective_from.desc())
            .limit(1)
        )
        if tariff is None:
            raise BusinessRuleError(
                "TARIFF_NOT_FOUND",
                "Không có biểu giá hiệu lực tại ngày kết thúc kỳ ghi chỉ số.",
            )
        return tariff

    def _prepare_reading(
        self,
        data: MeterReadingCreate,
        user_id: UUID,
        source: str,
        batch_id: UUID | None = None,
    ) -> MeterReadingModel:
        meter = self.db.get(MeterModel, data.meter_id)
        if meter is None or not meter.is_active:
            raise NotFoundError("Meter not found")
        duplicate = self.db.scalar(
            select(MeterReadingModel.id).where(
                MeterReadingModel.meter_id == data.meter_id,
                MeterReadingModel.period_start == data.period_start,
                MeterReadingModel.period_end == data.period_end,
            ).limit(1)
        )
        if duplicate:
            raise BusinessRuleError(
                "METER_READING_ALREADY_EXISTS",
                "Công tơ đã có chỉ số trong kỳ này.",
            )
        previous = self.db.scalar(
            select(MeterReadingModel)
            .where(
                MeterReadingModel.meter_id == data.meter_id,
                MeterReadingModel.period_end < data.period_start,
            )
            .order_by(MeterReadingModel.period_end.desc())
            .limit(1)
        )
        expected_previous = previous.current_reading if previous else meter.initial_reading
        if data.previous_reading != expected_previous:
            raise BusinessRuleError(
                "PREVIOUS_READING_MISMATCH",
                f"Chỉ số đầu kỳ phải bằng {expected_previous}.",
                422,
            )
        tariff = self._find_tariff(meter.utility_id, data.period_end)
        tier_models = self._tiers(tariff.id)
        tiers = [
            TariffTier(t.tier_order, t.from_quantity, t.to_quantity, t.unit_price)
            for t in tier_models
        ]
        consumption = data.current_reading - data.previous_reading
        calculation = calculate_utility_charge(consumption, tiers, tariff.calculation_type)
        snapshot = {
            "tariff_id": str(tariff.id),
            "name": tariff.name,
            "calculation_type": tariff.calculation_type,
            "effective_from": tariff.effective_from.isoformat(),
            "effective_to": tariff.effective_to.isoformat() if tariff.effective_to else None,
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
        return MeterReadingModel(
            meter_id=data.meter_id,
            period_start=data.period_start,
            period_end=data.period_end,
            previous_reading=data.previous_reading,
            current_reading=data.current_reading,
            consumption=calculation.consumption,
            tariff_id=tariff.id,
            tariff_snapshot=snapshot,
            calculated_amount=calculation.total_amount,
            source=source,
            import_batch_id=batch_id,
            recorded_by=user_id,
        )

    def _reading(self, item: MeterReadingModel) -> MeterReadingRead:
        meter = self.db.get(MeterModel, item.meter_id)
        utility = self.db.get(UtilityModel, meter.utility_id)
        return MeterReadingRead(
            id=item.id,
            meter_id=item.meter_id,
            meter_code=meter.meter_code,
            utility_code=utility.code,
            period_start=item.period_start,
            period_end=item.period_end,
            previous_reading=item.previous_reading,
            current_reading=item.current_reading,
            consumption=item.consumption,
            calculated_amount=item.calculated_amount,
            source=item.source,
            tariff_id=item.tariff_id,
            tariff_snapshot=item.tariff_snapshot,
            recorded_at=item.recorded_at,
        )

    def create_reading(self, data: MeterReadingCreate, user_id: UUID) -> MeterReadingRead:
        item = self._prepare_reading(data, user_id, "Manual")
        self.db.add(item)
        self._commit()
        self.db.refresh(item)
        return self._reading(item)

    def list_readings(
        self, meter_id: UUID | None = None, period_start: date | None = None
    ) -> list[MeterReadingRead]:
        statement = select(MeterReadingModel).order_by(MeterReadingModel.recorded_at.desc())
        if meter_id:
            statement = statement.where(MeterReadingModel.meter_id == meter_id)
        if period_start:
            statement = statement.where(MeterReadingModel.period_start == period_start)
        return [self._reading(item) for item in self.db.scalars(statement).all()]

    @classmethod
    def build_template(cls) -> bytes:
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "MeterReadings"
        sheet.append(cls.TEMPLATE_HEADERS)
        sheet.append(("DIEN-A101", "2026-09-01", "2026-09-30", 0, 125))
        sheet.freeze_panes = "A2"
        widths = (22, 18, 18, 22, 20)
        for column, width in zip("ABCDE", widths, strict=True):
            sheet.column_dimensions[column].width = width
        stream = BytesIO()
        workbook.save(stream)
        return stream.getvalue()

    def _preview_row(self, row_number: int, values: tuple[object, ...]) -> ImportPreviewRow:
        errors: list[str] = []
        meter_code = str(values[0] or "").strip().upper()
        try:
            period_start = _date(values[1])
            period_end = _date(values[2])
            previous_reading = _decimal(values[3])
            current_reading = _decimal(values[4])
            meter = self.db.scalar(select(MeterModel).where(MeterModel.meter_code == meter_code))
            if meter is None:
                raise ValueError("Không tìm thấy mã công tơ.")
            payload = MeterReadingCreate(
                meter_id=meter.id,
                period_start=period_start,
                period_end=period_end,
                previous_reading=previous_reading,
                current_reading=current_reading,
            )
            candidate = self._prepare_reading(payload, uuid4(), "Excel")
            return ImportPreviewRow(
                row_number=row_number,
                meter_code=meter_code,
                period_start=period_start,
                period_end=period_end,
                previous_reading=previous_reading,
                current_reading=current_reading,
                consumption=candidate.consumption,
                calculated_amount=candidate.calculated_amount,
                valid=True,
            )
        except (ValueError, BusinessRuleError, NotFoundError) as exc:
            errors.append(str(exc))
        return ImportPreviewRow(
            row_number=row_number,
            meter_code=meter_code,
            valid=False,
            errors=errors,
        )

    def preview_import(
        self, content: bytes, filename: str, content_type: str, user_id: UUID
    ) -> ImportPreviewRead:
        try:
            workbook = load_workbook(BytesIO(content), read_only=True, data_only=True)
            sheet = workbook.active
            rows = sheet.iter_rows(values_only=True)
            headers = tuple(str(value or "").strip() for value in next(rows))
        except Exception as exc:
            raise BusinessRuleError(
                "INVALID_EXCEL_FILE", "Không thể đọc tệp Excel.", 422
            ) from exc
        if headers != self.TEMPLATE_HEADERS:
            raise BusinessRuleError(
                "INVALID_EXCEL_TEMPLATE",
                "Tiêu đề tệp Excel không đúng mẫu được cung cấp.",
                422,
            )
        preview_rows = [
            self._preview_row(index, tuple(values))
            for index, values in enumerate(rows, start=2)
            if any(value not in (None, "") for value in values)
        ]
        serialized = [row.model_dump(mode="json") for row in preview_rows]
        valid_rows = sum(1 for row in preview_rows if row.valid)
        file = StoredFileModel(
            storage_provider="DatabaseMetadata",
            storage_key=f"utility-imports/{sha256(content).hexdigest()}-{uuid4().hex}",
            original_name=filename[:255],
            content_type=(content_type or "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")[:150],
            size_bytes=len(content),
            checksum_sha256=sha256(content).hexdigest(),
            uploaded_by=user_id,
        )
        self.db.add(file)
        self.db.flush()
        batch = UtilityImportBatchModel(
            file_id=file.id,
            status="Previewed",
            total_rows=len(preview_rows),
            valid_rows=valid_rows,
            invalid_rows=len(preview_rows) - valid_rows,
            preview_rows=serialized,
            created_by=user_id,
        )
        self.db.add(batch)
        self._commit()
        return ImportPreviewRead(
            batch_id=batch.id,
            status=batch.status,
            total_rows=batch.total_rows,
            valid_rows=batch.valid_rows,
            invalid_rows=batch.invalid_rows,
            rows=preview_rows,
        )

    def confirm_import(self, batch_id: UUID, user_id: UUID) -> ImportConfirmRead:
        batch = self.db.scalar(
            select(UtilityImportBatchModel)
            .where(UtilityImportBatchModel.id == batch_id)
            .with_for_update()
        )
        if batch is None:
            raise NotFoundError("Import batch not found")
        if batch.status != "Previewed":
            raise BusinessRuleError("IMPORT_ALREADY_CONFIRMED", "Lô dữ liệu này đã được xác nhận.")
        if batch.invalid_rows:
            raise BusinessRuleError(
                "IMPORT_HAS_ERRORS",
                "Phải sửa toàn bộ dòng lỗi và tải lại trước khi xác nhận.",
            )
        created = 0
        for row in batch.preview_rows or []:
            meter = self.db.scalar(
                select(MeterModel).where(MeterModel.meter_code == row["meter_code"])
            )
            payload = MeterReadingCreate(
                meter_id=meter.id,
                period_start=_date(row["period_start"]),
                period_end=_date(row["period_end"]),
                previous_reading=_decimal(row["previous_reading"]),
                current_reading=_decimal(row["current_reading"]),
            )
            self.db.add(self._prepare_reading(payload, user_id, "Excel", batch.id))
            created += 1
        batch.status = "Confirmed"
        batch.confirmed_at = datetime.now(UTC)
        self._commit()
        return ImportConfirmRead(batch_id=batch.id, status=batch.status, created_readings=created)
