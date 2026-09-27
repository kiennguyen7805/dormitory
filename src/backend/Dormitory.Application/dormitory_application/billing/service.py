from uuid import UUID

from .schemas import BillGenerateRequest


class BillingService:
    def __init__(self, repository) -> None:
        self.repository = repository

    def list_bills(self, user_id: UUID, role: str, contract_id: UUID | None = None):
        return self.repository.list_bills(user_id, role, contract_id)

    def generate(self, data: BillGenerateRequest, user_id: UUID):
        return self.repository.generate(data, user_id)
