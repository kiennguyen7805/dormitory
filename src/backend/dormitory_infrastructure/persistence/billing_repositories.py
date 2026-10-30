from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from dormitory_application.billing import BillGenerateRequest, BillItemRead, BillRead
from dormitory_application.common import BusinessRuleError, NotFoundError

from .models import (
    BedAssignmentModel,
    BedModel,
    BillItemModel,
    BillModel,
    ContractModel,
    MeterModel,
    MeterReadingModel,
    RoomModel,
    UtilityModel,
)


class SqlAlchemyBillingRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def _commit(self) -> None:
        try:
            self.db.commit()
        except IntegrityError as exc:
            self.db.rollback()
            raise BusinessRuleError(
                "BILL_DATA_CONFLICT",
                "Hóa đơn cho hợp đồng và kỳ này đã tồn tại.",
            ) from exc

    def _bill(self, item: BillModel) -> BillRead:
        rows = self.db.scalars(
            select(BillItemModel)
            .where(BillItemModel.bill_id == item.id)
            .order_by(BillItemModel.created_at, BillItemModel.item_type)
        ).all()
        return BillRead(
            id=item.id,
            bill_no=item.bill_no,
            contract_id=item.contract_id,
            student_id=item.student_id,
            period_start=item.period_start,
            period_end=item.period_end,
            issued_date=item.issued_date,
            due_date=item.due_date,
            status=item.status,
            subtotal=item.subtotal,
            adjustment_amount=item.adjustment_amount,
            total_amount=item.total_amount,
            paid_amount=item.paid_amount,
            balance_amount=item.balance_amount,
            idempotency_key=item.idempotency_key,
            items=[
                BillItemRead(
                    id=row.id,
                    item_type=row.item_type,
                    reference_type=row.reference_type,
                    reference_id=row.reference_id,
                    description=row.description,
                    quantity=row.quantity,
                    unit_price=row.unit_price,
                    amount=row.amount,
                    calculation_snapshot=row.calculation_snapshot,
                )
                for row in rows
            ],
        )

    def list_bills(
        self,
        user_id: UUID,
        role: str,
        contract_id: UUID | None = None,
    ) -> list[BillRead]:
        statement = select(BillModel).order_by(BillModel.issued_date.desc(), BillModel.bill_no.desc())
        if role == "Student":
            statement = statement.where(BillModel.student_id == user_id)
        if contract_id:
            statement = statement.where(BillModel.contract_id == contract_id)
        return [self._bill(item) for item in self.db.scalars(statement).all()]

    def generate(self, data: BillGenerateRequest, user_id: UUID) -> BillRead:
        existing_by_key = self.db.scalar(
            select(BillModel).where(BillModel.idempotency_key == data.idempotency_key)
        )
        if existing_by_key:
            if (
                existing_by_key.contract_id != data.contract_id
                or existing_by_key.period_start != data.period_start
                or existing_by_key.period_end != data.period_end
            ):
                raise BusinessRuleError(
                    "IDEMPOTENCY_KEY_REUSED",
                    "Khóa chống trùng đã được dùng cho một yêu cầu khác.",
                )
            return self._bill(existing_by_key)

        contract = self.db.get(ContractModel, data.contract_id)
        if contract is None:
            raise NotFoundError("Contract not found")
        if data.period_end < contract.start_date or data.period_start > contract.end_date:
            raise BusinessRuleError(
                "BILL_PERIOD_OUTSIDE_CONTRACT",
                "Kỳ hóa đơn nằm ngoài thời hạn hợp đồng.",
                422,
            )
        duplicate_period = self.db.scalar(
            select(BillModel.id).where(
                BillModel.contract_id == data.contract_id,
                BillModel.period_start == data.period_start,
                BillModel.period_end == data.period_end,
                BillModel.status != "Void",
            ).limit(1)
        )
        if duplicate_period:
            raise BusinessRuleError(
                "BILL_PERIOD_ALREADY_EXISTS",
                "Hợp đồng đã có hóa đơn trong kỳ này.",
            )

        room_ids = self.db.scalars(
            select(RoomModel.id)
            .join(BedModel, BedModel.room_id == RoomModel.id)
            .join(BedAssignmentModel, BedAssignmentModel.bed_id == BedModel.id)
            .where(
                BedAssignmentModel.contract_id == contract.id,
                BedAssignmentModel.start_date <= data.period_end,
                or_(
                    BedAssignmentModel.end_date.is_(None),
                    BedAssignmentModel.end_date >= data.period_start,
                ),
            )
            .distinct()
        ).all()
        if not room_ids:
            raise BusinessRuleError(
                "BILL_ROOM_NOT_FOUND",
                "Không tìm thấy phòng của hợp đồng trong kỳ hóa đơn.",
            )

        bill = BillModel(
            bill_no=f"HD-{data.period_end:%Y%m}-{uuid4().hex[:8].upper()}",
            contract_id=contract.id,
            student_id=contract.student_id,
            period_start=data.period_start,
            period_end=data.period_end,
            issued_date=data.issued_date,
            due_date=data.due_date,
            status="Issued",
            subtotal=Decimal("0"),
            adjustment_amount=Decimal("0"),
            total_amount=Decimal("0"),
            paid_amount=Decimal("0"),
            balance_amount=Decimal("0"),
            idempotency_key=data.idempotency_key,
            issued_by=user_id,
        )
        self.db.add(bill)
        self.db.flush()

        housing_item = BillItemModel(
            bill_id=bill.id,
            item_type="Housing",
            reference_type="Contract",
            reference_id=contract.id,
            description=f"Phí phòng kỳ {data.period_start:%d/%m/%Y} - {data.period_end:%d/%m/%Y}",
            quantity=Decimal("1"),
            unit_price=contract.base_rate,
            amount=contract.base_rate,
            calculation_snapshot={
                "contract_no": contract.contract_no,
                "base_rate": str(contract.base_rate),
            },
        )
        self.db.add(housing_item)
        subtotal = Decimal(contract.base_rate)

        reading_rows = self.db.execute(
            select(MeterReadingModel, MeterModel, UtilityModel)
            .join(MeterModel, MeterModel.id == MeterReadingModel.meter_id)
            .join(UtilityModel, UtilityModel.id == MeterModel.utility_id)
            .where(
                MeterModel.room_id.in_(room_ids),
                MeterReadingModel.period_start == data.period_start,
                MeterReadingModel.period_end == data.period_end,
            )
            .order_by(UtilityModel.code, MeterModel.meter_code)
        ).all()
        for reading, meter, utility in reading_rows:
            average_price = (
                reading.calculated_amount / reading.consumption
                if reading.consumption
                else Decimal("0")
            )
            self.db.add(
                BillItemModel(
                    bill_id=bill.id,
                    item_type=utility.code.title(),
                    reference_type="MeterReading",
                    reference_id=reading.id,
                    description=f"{utility.name} - công tơ {meter.meter_code}",
                    quantity=reading.consumption,
                    unit_price=average_price.quantize(Decimal("0.01")),
                    amount=reading.calculated_amount,
                    calculation_snapshot={
                        "meter_code": meter.meter_code,
                        "previous_reading": str(reading.previous_reading),
                        "current_reading": str(reading.current_reading),
                        "tariff": reading.tariff_snapshot,
                    },
                )
            )
            subtotal += reading.calculated_amount

        bill.subtotal = subtotal
        bill.total_amount = subtotal
        bill.balance_amount = subtotal
        self._commit()
        return self._bill(bill)
