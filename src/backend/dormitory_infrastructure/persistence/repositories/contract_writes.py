"""Write-side stored-function calls and transaction result mapping."""

from datetime import date
from uuid import UUID, uuid4

from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine import Connection

from dormitory_application.common import BusinessRuleError, NotFoundError
from dormitory_application.contracts import AssignRoomRequest, HousingApplicationCreate


_ERRORS = {
    "STUDENT_ALREADY_HOUSED": ("Sinh viên đã có hợp đồng phòng còn hiệu lực.", 409),
    "APPLICATION_ALREADY_EXISTS": ("Bạn đã có đăng ký đang xử lý cho học kỳ này.", 409),
    "APPLICATION_INVALID_STATE": ("Chỉ đăng ký đang chờ mới có thể được duyệt hoặc từ chối.", 409),
    "REJECTION_REASON_REQUIRED": ("Phải nhập lý do từ chối.", 422),
    "APPLICATION_NOT_APPROVED": ("Đăng ký phải được duyệt trước khi phân giường.", 409),
    "CONTRACT_ALREADY_EXISTS": ("Đăng ký này đã có hợp đồng.", 409),
    "BED_NOT_AVAILABLE": ("Giường đang bảo trì hoặc phòng đã ngừng hoạt động.", 409),
    "BED_ASSIGNMENT_CONFLICT": ("Giường đã được phân trong khoảng thời gian này.", 409),
    "ROOM_NOT_FOUND": ("Không tìm thấy phòng.", 404),
    "ROOM_NOT_AVAILABLE": ("Phòng không còn hoạt động.", 409),
    "ROOM_FULL": ("Phòng đã đủ chỗ trong thời gian này.", 409),
    "CONTRACT_NOT_ACTIVE": ("Hợp đồng không còn hiệu lực.", 409),
    "ACTIVE_ASSIGNMENT_NOT_FOUND": ("Không tìm thấy giường hiện tại.", 409),
    "TERMINATION_DATE_INVALID": ("Ngày chấm dứt không hợp lệ.", 422),
}


class StoredContractWrites:
    def __init__(self, db: Connection) -> None:
        self.db = db

    def _execute(self, sql: str, params: dict) -> None:
        try:
            result = self.db.execute(text(sql), params).scalar_one()
            if result != "OK":
                self.db.rollback()
                if result in ("NOT_FOUND", "APPLICATION_NOT_FOUND"):
                    raise NotFoundError("Housing application not found")
                if result == "BED_NOT_FOUND":
                    raise NotFoundError("Bed not found")
                if result == "CONTRACT_NOT_FOUND":
                    raise NotFoundError("Contract not found")
                message, status = _ERRORS[result]
                raise BusinessRuleError(result, message, status)
            self.db.commit()
        except IntegrityError as exc:
            self.db.rollback()
            raise BusinessRuleError(
                "CONTRACT_DATA_CONFLICT", "Dữ liệu hợp đồng hoặc phân giường bị trùng."
            ) from exc

    def create_application(self, student_id: UUID, data: HousingApplicationCreate) -> UUID:
        item_id = uuid4()
        self._execute(
            "SELECT public.fn_create_application(:id, :student_id, :term_code, :room_id)",
            {"id": item_id, "student_id": student_id, "term_code": data.term_code,
             "room_id": data.room_id},
        )
        return item_id

    def review_application(
        self, application_id: UUID, reviewer_id: UUID, target_status: str, reason: str | None
    ) -> None:
        self._execute(
            "SELECT public.fn_review_application(:id, :reviewer_id, :status, :reason)",
            {"id": application_id, "reviewer_id": reviewer_id,
             "status": target_status, "reason": reason},
        )

    def assign_room(self, application_id: UUID, data: AssignRoomRequest) -> UUID:
        contract_id = uuid4()
        self._execute(
            "SELECT public.fn_assign_room(:application_id, :contract_id, :assignment_id, "
            ":contract_no, :start_date, :end_date)",
            {"application_id": application_id, "contract_id": contract_id,
             "assignment_id": uuid4(), "contract_no": f"HD-{data.start_date:%Y%m%d}-{uuid4().hex[:8].upper()}",
             "start_date": data.start_date, "end_date": data.end_date},
        )
        return contract_id

    def terminate(self, contract_id: UUID, termination_date: date) -> None:
        self._execute(
            "SELECT public.fn_terminate_contract(:contract_id, :termination_date)",
            {"contract_id": contract_id, "termination_date": termination_date},
        )
