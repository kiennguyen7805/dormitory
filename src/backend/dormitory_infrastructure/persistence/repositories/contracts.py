"""Contract repository backed only by PostgreSQL functions."""

from datetime import date
from uuid import UUID

from sqlalchemy.engine import Connection

from dormitory_application.common import BusinessRuleError, NotFoundError
from dormitory_application.contracts import (
    AssignRoomRequest, ContractRead, HousingApplicationCreate,
    HousingApplicationRead,
)

from .contract_reads import StoredContractReads
from .contract_writes import StoredContractWrites


class StoredContractRepository:
    def __init__(self, db: Connection) -> None:
        self.reads = StoredContractReads(db)
        self.writes = StoredContractWrites(db)

    def create_application(
        self, student_id: UUID, data: HousingApplicationCreate
    ) -> HousingApplicationRead:
        item_id = self.writes.create_application(student_id, data)
        return self.reads.get_application(item_id)

    def list_applications(
        self, user_id: UUID, role: str, status: str | None
    ) -> list[HousingApplicationRead]:
        return self.reads.list_applications(user_id, role, status)

    def review_application(
        self, application_id: UUID, reviewer_id: UUID,
        target_status: str, reason: str | None,
    ) -> HousingApplicationRead:
        self.writes.review_application(application_id, reviewer_id, target_status, reason)
        return self.reads.get_application(application_id)

    def assign_room(self, application_id: UUID, data: AssignRoomRequest) -> ContractRead:
        contract_id = self.writes.assign_room(application_id, data)
        return self._load_contract(contract_id)

    def _load_contract(self, contract_id: UUID) -> ContractRead:
        item = self.reads.get_contract(contract_id)
        if item is None:
            raise NotFoundError("Contract not found")
        return item

    def list_contracts(self, user_id: UUID, role: str) -> list[ContractRead]:
        return self.reads.list_contracts(user_id, role)

    def get_contract(self, contract_id: UUID, user_id: UUID, role: str) -> ContractRead:
        item = self._load_contract(contract_id)
        if role == "Student" and item.student_id != user_id:
            raise BusinessRuleError("OWN_DATA_ONLY", "Bạn chỉ có thể xem hợp đồng của mình.", 403)
        return item

    def get_my_contract(self, student_id: UUID) -> ContractRead | None:
        return self.reads.get_my_contract(student_id)

    def terminate(self, contract_id: UUID, termination_date: date) -> ContractRead:
        self.writes.terminate(contract_id, termination_date)
        return self._load_contract(contract_id)
