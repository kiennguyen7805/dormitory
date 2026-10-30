from uuid import UUID

from .schemas import BillGenerateRequest


class BillingService:
    def __init__(self, repository) -> None:
        self.repository = repository

    def list_bills(self, user_id: UUID, role: str, room_id: UUID | None = None):
        return self.repository.list_bills(user_id, role, room_id)

    def get_bill(self, bill_id: UUID, user_id: UUID, role: str):
        return self.repository.get_bill(bill_id, user_id, role)

    def generate(self, data: BillGenerateRequest, user_id: UUID):
        return self.repository.generate(data, user_id)

    def confirm_payment(self, bill_id: UUID, method: str, reference: str | None, user_id: UUID):
        return self.repository.confirm_payment(bill_id, method, reference, user_id)
    

