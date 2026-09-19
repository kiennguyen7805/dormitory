from datetime import date
from uuid import UUID

from .schemas import (
    AssignBedRequest,
    BedAssignmentRead,
    ContractRead,
    HousingApplicationCreate,
    HousingApplicationRead,
    TransferBedRequest,
)


class ContractService:
    def __init__(self, repository) -> None:
        self.repository = repository

    def create_application(
        self, student_id: UUID, data: HousingApplicationCreate
    ) -> HousingApplicationRead:
        return self.repository.create_application(student_id, data)

    def list_applications(
        self, user_id: UUID, role: str, status: str | None
    ) -> list[HousingApplicationRead]:
        return self.repository.list_applications(user_id, role, status)

    def approve_application(
        self, application_id: UUID, reviewer_id: UUID
    ) -> HousingApplicationRead:
        return self.repository.review_application(
            application_id, reviewer_id, "Approved", None
        )

    def reject_application(
        self, application_id: UUID, reviewer_id: UUID, reason: str
    ) -> HousingApplicationRead:
        return self.repository.review_application(
            application_id, reviewer_id, "Rejected", reason.strip()
        )

    def assign_bed(self, application_id: UUID, data: AssignBedRequest) -> ContractRead:
        return self.repository.assign_bed(application_id, data)

    def list_contracts(self, user_id: UUID, role: str) -> list[ContractRead]:
        return self.repository.list_contracts(user_id, role)

    def get_contract(self, contract_id: UUID, user_id: UUID, role: str) -> ContractRead:
        return self.repository.get_contract(contract_id, user_id, role)

    def get_my_contract(self, student_id: UUID) -> ContractRead | None:
        return self.repository.get_my_contract(student_id)

    def assignment_history(
        self, contract_id: UUID, user_id: UUID, role: str
    ) -> list[BedAssignmentRead]:
        return self.repository.assignment_history(contract_id, user_id, role)

    def transfer(self, contract_id: UUID, data: TransferBedRequest) -> ContractRead:
        return self.repository.transfer(contract_id, data)

    def terminate(self, contract_id: UUID, termination_date: date) -> ContractRead:
        return self.repository.terminate(contract_id, termination_date)
