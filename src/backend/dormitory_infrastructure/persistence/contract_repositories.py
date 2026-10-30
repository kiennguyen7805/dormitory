from datetime import UTC, date, datetime
from uuid import UUID, uuid4

from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from dormitory_application.common import BusinessRuleError, NotFoundError
from dormitory_application.contracts import (
    AssignBedRequest,
    BedAssignmentRead,
    ContractRead,
    HousingApplicationCreate,
    HousingApplicationRead,
    TransferBedRequest,
)

from .models import (
    BedAssignmentModel,
    BedModel,
    ContractModel,
    HousingApplicationModel,
    RoomModel,
)


class SqlAlchemyContractRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def _commit(self) -> None:
        try:
            self.db.commit()
        except IntegrityError as exc:
            self.db.rollback()
            raise BusinessRuleError(
                "CONTRACT_DATA_CONFLICT",
                "Dữ liệu hợp đồng hoặc phân giường bị trùng.",
            ) from exc

    @staticmethod
    def _application(item: HousingApplicationModel) -> HousingApplicationRead:
        return HousingApplicationRead(
            id=item.id,
            student_id=item.student_id,
            student_name=item.student.full_name,
            term_code=item.term_code,
            preferred_room_type_id=item.preferred_room_type_id,
            preferred_room_type_name=item.preferred_room_type.name,
            status=item.status,
            rejection_reason=item.rejection_reason,
            created_at=item.created_at,
        )

    @staticmethod
    def _assignment(item: BedAssignmentModel) -> BedAssignmentRead:
        return BedAssignmentRead(
            id=item.id,
            bed_id=item.bed_id,
            building_code=item.bed.room.building.code,
            room_code=item.bed.room.code,
            bed_code=item.bed.code,
            start_date=item.start_date,
            end_date=item.end_date,
            status=item.status,
        )

    @classmethod
    def _contract(cls, item: ContractModel) -> ContractRead:
        current = next((x for x in item.assignments if x.status == "Active"), None)
        return ContractRead(
            id=item.id,
            contract_no=item.contract_no,
            student_id=item.student_id,
            student_name=item.student.full_name,
            application_id=item.application_id,
            start_date=item.start_date,
            end_date=item.end_date,
            status=item.status,
            base_rate=item.base_rate,
            current_assignment=cls._assignment(current) if current else None,
        )

    @staticmethod
    def _application_statement():
        return select(HousingApplicationModel).options(
            selectinload(HousingApplicationModel.student),
            selectinload(HousingApplicationModel.preferred_room_type),
        )

    @staticmethod
    def _contract_statement():
        assignment_path = (
            selectinload(ContractModel.assignments)
            .selectinload(BedAssignmentModel.bed)
            .selectinload(BedModel.room)
            .selectinload(RoomModel.building)
        )
        return select(ContractModel).options(
            selectinload(ContractModel.student),
            assignment_path,
        )

    def create_application(
        self, student_id: UUID, data: HousingApplicationCreate
    ) -> HousingApplicationRead:
        duplicate = self.db.scalar(
            select(HousingApplicationModel).where(
                HousingApplicationModel.student_id == student_id,
                HousingApplicationModel.term_code == data.term_code.strip(),
                HousingApplicationModel.status.in_(["Submitted", "Approved"]),
            )
        )
        if duplicate:
            raise BusinessRuleError(
                "APPLICATION_ALREADY_EXISTS",
                "Bạn đã có đăng ký đang xử lý cho học kỳ này.",
            )
        item = HousingApplicationModel(
            student_id=student_id,
            term_code=data.term_code.strip().upper(),
            preferred_room_type_id=data.preferred_room_type_id,
            status="Submitted",
        )
        self.db.add(item)
        self._commit()
        item = self.db.scalar(self._application_statement().where(HousingApplicationModel.id == item.id))
        return self._application(item)

    def list_applications(
        self, user_id: UUID, role: str, status: str | None
    ) -> list[HousingApplicationRead]:
        statement = self._application_statement().order_by(HousingApplicationModel.created_at.desc())
        if role == "Student":
            statement = statement.where(HousingApplicationModel.student_id == user_id)
        if status:
            statement = statement.where(HousingApplicationModel.status == status)
        return [self._application(x) for x in self.db.scalars(statement).all()]

    def review_application(
        self,
        application_id: UUID,
        reviewer_id: UUID,
        target_status: str,
        reason: str | None,
    ) -> HousingApplicationRead:
        item = self.db.scalar(
            self._application_statement()
            .where(HousingApplicationModel.id == application_id)
            .with_for_update()
        )
        if item is None:
            raise NotFoundError("Housing application not found")
        if item.status != "Submitted":
            raise BusinessRuleError(
                "APPLICATION_INVALID_STATE",
                "Chỉ đăng ký đang chờ mới có thể được duyệt hoặc từ chối.",
            )
        if target_status == "Rejected" and not reason:
            raise BusinessRuleError(
                "REJECTION_REASON_REQUIRED",
                "Phải nhập lý do từ chối.",
                422,
            )
        item.status = target_status
        item.rejection_reason = reason
        item.reviewed_by_user_id = reviewer_id
        item.reviewed_at = datetime.now(UTC)
        self._commit()
        return self._application(item)

    def _lock_available_bed(self, bed_id: UUID, start_date: date, end_date: date) -> BedModel:
        bed = self.db.scalar(select(BedModel).where(BedModel.id == bed_id).with_for_update())
        if bed is None:
            raise NotFoundError("Bed not found")
        if not bed.is_active or not bed.room.is_active:
            raise BusinessRuleError("BED_NOT_AVAILABLE", "Giường đang bảo trì hoặc phòng đã ngừng hoạt động.")
        overlap = self.db.scalar(
            select(BedAssignmentModel.id).where(
                BedAssignmentModel.bed_id == bed_id,
                BedAssignmentModel.start_date <= end_date,
                or_(
                    BedAssignmentModel.end_date.is_(None),
                    BedAssignmentModel.end_date >= start_date,
                ),
            ).limit(1)
        )
        if overlap:
            raise BusinessRuleError(
                "BED_ASSIGNMENT_CONFLICT",
                "Giường đã được phân trong khoảng thời gian này.",
            )
        return bed

    def assign_bed(self, application_id: UUID, data: AssignBedRequest) -> ContractRead:
        application = self.db.scalar(
            self._application_statement()
            .where(HousingApplicationModel.id == application_id)
            .with_for_update()
        )
        if application is None:
            raise NotFoundError("Housing application not found")
        if application.status != "Approved":
            raise BusinessRuleError(
                "APPLICATION_NOT_APPROVED",
                "Đăng ký phải được duyệt trước khi phân giường.",
            )
        if application.contract is not None:
            raise BusinessRuleError(
                "CONTRACT_ALREADY_EXISTS",
                "Đăng ký này đã có hợp đồng.",
            )
        bed = self._lock_available_bed(data.bed_id, data.start_date, data.end_date)
        contract = ContractModel(
            contract_no=f"HD-{data.start_date:%Y%m%d}-{uuid4().hex[:8].upper()}",
            student_id=application.student_id,
            application_id=application.id,
            start_date=data.start_date,
            end_date=data.end_date,
            status="Active",
            base_rate=bed.room.room_type.default_monthly_rate,
        )
        self.db.add(contract)
        self.db.flush()
        self.db.add(
            BedAssignmentModel(
                contract_id=contract.id,
                bed_id=bed.id,
                start_date=data.start_date,
                status="Active",
            )
        )
        self._commit()
        return self._load_contract(contract.id)

    def _load_contract(self, contract_id: UUID) -> ContractRead:
        item = self.db.scalar(self._contract_statement().where(ContractModel.id == contract_id))
        if item is None:
            raise NotFoundError("Contract not found")
        return self._contract(item)

    def list_contracts(self, user_id: UUID, role: str) -> list[ContractRead]:
        statement = self._contract_statement().order_by(ContractModel.start_date.desc())
        if role == "Student":
            statement = statement.where(ContractModel.student_id == user_id)
        return [self._contract(x) for x in self.db.scalars(statement).all()]

    def get_contract(self, contract_id: UUID, user_id: UUID, role: str) -> ContractRead:
        item = self.db.scalar(self._contract_statement().where(ContractModel.id == contract_id))
        if item is None:
            raise NotFoundError("Contract not found")
        if role == "Student" and item.student_id != user_id:
            raise BusinessRuleError("OWN_DATA_ONLY", "Bạn chỉ có thể xem hợp đồng của mình.", 403)
        return self._contract(item)

    def get_my_contract(self, student_id: UUID) -> ContractRead | None:
        item = self.db.scalar(
            self._contract_statement()
            .where(ContractModel.student_id == student_id)
            .order_by(ContractModel.start_date.desc())
            .limit(1)
        )
        return self._contract(item) if item else None

    def assignment_history(
        self, contract_id: UUID, user_id: UUID, role: str
    ) -> list[BedAssignmentRead]:
        contract = self.db.get(ContractModel, contract_id)
        if contract is None:
            raise NotFoundError("Contract not found")
        if role == "Student" and contract.student_id != user_id:
            raise BusinessRuleError("OWN_DATA_ONLY", "Bạn chỉ có thể xem lịch sử của mình.", 403)
        statement = (
            select(BedAssignmentModel)
            .options(
                selectinload(BedAssignmentModel.bed)
                .selectinload(BedModel.room)
                .selectinload(RoomModel.building)
            )
            .where(BedAssignmentModel.contract_id == contract_id)
            .order_by(BedAssignmentModel.start_date)
        )
        return [self._assignment(x) for x in self.db.scalars(statement).all()]

    def transfer(self, contract_id: UUID, data: TransferBedRequest) -> ContractRead:
        contract = self.db.scalar(
            select(ContractModel).where(ContractModel.id == contract_id).with_for_update()
        )
        if contract is None:
            raise NotFoundError("Contract not found")
        if contract.status != "Active":
            raise BusinessRuleError("CONTRACT_NOT_ACTIVE", "Hợp đồng không còn hiệu lực.")
        current = self.db.scalar(
            select(BedAssignmentModel).where(
                BedAssignmentModel.contract_id == contract.id,
                BedAssignmentModel.status == "Active",
            ).with_for_update()
        )
        if current is None:
            raise BusinessRuleError("ACTIVE_ASSIGNMENT_NOT_FOUND", "Không tìm thấy giường hiện tại.")
        if data.transfer_date <= current.start_date or data.transfer_date > contract.end_date:
            raise BusinessRuleError("TRANSFER_DATE_INVALID", "Ngày chuyển giường không hợp lệ.", 422)
        if current.bed_id == data.bed_id:
            raise BusinessRuleError("SAME_BED_TRANSFER", "Giường mới phải khác giường hiện tại.")
        self._lock_available_bed(data.bed_id, data.transfer_date, contract.end_date)
        current.status = "Ended"
        current.end_date = data.transfer_date
        self.db.add(
            BedAssignmentModel(
                contract_id=contract.id,
                bed_id=data.bed_id,
                start_date=data.transfer_date,
                status="Active",
            )
        )
        self._commit()
        return self._load_contract(contract.id)

    def terminate(self, contract_id: UUID, termination_date: date) -> ContractRead:
        contract = self.db.scalar(
            select(ContractModel).where(ContractModel.id == contract_id).with_for_update()
        )
        if contract is None:
            raise NotFoundError("Contract not found")
        if contract.status != "Active":
            raise BusinessRuleError("CONTRACT_NOT_ACTIVE", "Hợp đồng không còn hiệu lực.")
        current = self.db.scalar(
            select(BedAssignmentModel).where(
                BedAssignmentModel.contract_id == contract.id,
                BedAssignmentModel.status == "Active",
            ).with_for_update()
        )
        if current is None:
            raise BusinessRuleError("ACTIVE_ASSIGNMENT_NOT_FOUND", "Không tìm thấy giường hiện tại.")
        if termination_date < current.start_date or termination_date > contract.end_date:
            raise BusinessRuleError("TERMINATION_DATE_INVALID", "Ngày chấm dứt không hợp lệ.", 422)
        current.status = "Ended"
        current.end_date = termination_date
        contract.status = "Terminated"
        contract.terminated_at = datetime.now(UTC)
        self._commit()
        return self._load_contract(contract.id)
