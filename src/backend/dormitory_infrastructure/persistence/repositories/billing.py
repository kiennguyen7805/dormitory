from uuid import UUID, uuid4

from sqlalchemy import text
from sqlalchemy.engine import Connection
from sqlalchemy.exc import IntegrityError

from dormitory_application.billing import BillGenerateRequest, BillItemRead, BillRead
from dormitory_application.common import BusinessRuleError, NotFoundError


class StoredBillingRepository:
    def __init__(self, db: Connection) -> None:
        self.db = db

    def _bill(self, row) -> BillRead:
        items = self.db.execute(text("SELECT * FROM public.fn_bill_items(:id)"),
                                {"id": row["id"]}).mappings().all()
        return BillRead(**dict(row), items=[BillItemRead(**dict(item)) for item in items])

    def _get_bill(self, bill_id: UUID):
        row = self.db.execute(text("SELECT * FROM public.fn_get_bill(:id)"),
                              {"id": bill_id}).mappings().one_or_none()
        if row is None:
            raise NotFoundError("Bill not found")
        return row

    def get_bill(self, bill_id: UUID, user_id: UUID, role: str) -> BillRead:
        row = self._get_bill(bill_id)
        if role == "Student" and not self.db.scalar(
            text("SELECT public.fn_student_can_view_bill(:bill_id, :user_id)"),
            {"bill_id": bill_id, "user_id": user_id},
        ):
            raise BusinessRuleError("OWN_DATA_ONLY", "Bạn chỉ được xem hóa đơn phòng mình ở.", 403)
        return self._bill(row)

    def list_bills(self, user_id: UUID, role: str, room_id: UUID | None = None) -> list[BillRead]:
        rows = self.db.execute(
            text("SELECT * FROM public.fn_list_room_bills(:user_id, :role, :room_id)"),
            {"user_id": user_id, "role": role, "room_id": room_id},
        ).mappings().all()
        return [self._bill(row) for row in rows]

    def generate(self, data: BillGenerateRequest, user_id: UUID) -> BillRead:
        try:
            result = self.db.scalar(
                text("SELECT public.fn_generate_room_bill(:id, :no, :room_id, :start, "
                     ":end, :issued, :due, :key, :user_id)"),
                {"id": uuid4(), "no": f"HD-{data.period_end:%Y%m}-{uuid4().hex[:8].upper()}",
                 "room_id": data.room_id, "start": data.period_start,
                 "end": data.period_end, "issued": data.issued_date,
                 "due": data.due_date, "key": data.idempotency_key,
                 "user_id": user_id},
            )
            if result == "ROOM_NOT_FOUND":
                self.db.rollback()
                raise NotFoundError("Room not found")
            errors = {
                "IDEMPOTENCY_KEY_REUSED": ("Khóa chống trùng đã dùng cho hóa đơn khác.", 409),
                "BILL_PERIOD_ALREADY_EXISTS": ("Phòng đã có hóa đơn trong kỳ này.", 409),
                "READINGS_INCOMPLETE": ("Cần đủ chỉ số điện và nước của phòng trong kỳ.", 422),
                "INVALID_PERIOD": ("Kỳ hóa đơn không hợp lệ.", 422),
            }
            if result in errors:
                self.db.rollback()
                message, status = errors[result]
                raise BusinessRuleError(result, message, status)
            self.db.commit()
        except IntegrityError as exc:
            self.db.rollback()
            raise BusinessRuleError("BILL_DATA_CONFLICT", "Hóa đơn phòng và kỳ này đã tồn tại.") from exc
        return self._bill(self._get_bill(UUID(result)))

    def confirm_payment(self, bill_id: UUID, method: str, reference: str | None,
                        user_id: UUID) -> BillRead:
        result = self.db.scalar(
            text("SELECT public.fn_confirm_room_bill_payment(:id, :method, :reference, :actor)"),
            {"id": bill_id, "method": method, "reference": reference, "actor": user_id},
        )
        if result == "BILL_NOT_FOUND":
            self.db.rollback()
            raise NotFoundError("Bill not found")
        if result != "OK":
            self.db.rollback()
            raise BusinessRuleError(result, "Hóa đơn đã thanh toán hoặc không còn hiệu lực.", 409)
        self.db.commit()
        return self._bill(self._get_bill(bill_id))
