"""Read-side stored-function calls used by the contract repository."""

from uuid import UUID

from sqlalchemy import text
from sqlalchemy.engine import Connection

from dormitory_application.contracts import (
    BedAssignmentRead, ContractRead, HousingApplicationRead,
)


class StoredContractReads:
    def __init__(self, db: Connection) -> None:
        self.db = db

    def _rows(self, query: str, **params):
        return self.db.execute(text(query), params).mappings()

    def get_application(self, application_id: UUID) -> HousingApplicationRead | None:
        row = self._rows(
            "SELECT * FROM public.fn_get_application(:application_id)",
            application_id=application_id,
        ).first()
        return HousingApplicationRead.model_validate(dict(row)) if row else None

    def list_applications(
        self, user_id: UUID, role: str, status: str | None,
    ) -> list[HousingApplicationRead]:
        return [HousingApplicationRead.model_validate(dict(row)) for row in self._rows(
            "SELECT * FROM public.fn_list_applications(:user_id, :role, :status)",
            user_id=user_id, role=role, status=status,
        )]

    @staticmethod
    def _contract(row) -> ContractRead:
        assignment = None
        if row["assignment_id"] is not None:
            assignment = BedAssignmentRead(
                id=row["assignment_id"], bed_id=row["bed_id"],
                building_code=row["building_code"], room_code=row["room_code"],
                bed_code=row["bed_code"], start_date=row["assignment_start_date"],
                end_date=row["assignment_end_date"], status=row["assignment_status"],
            )
        return ContractRead(
            id=row["id"], contract_no=row["contract_no"],
            student_id=row["student_id"], student_name=row["student_name"],
            application_id=row["application_id"], start_date=row["start_date"],
            end_date=row["end_date"], status=row["status"],
            base_rate=row["base_rate"], current_assignment=assignment,
        )

    def list_contracts(self, user_id: UUID, role: str) -> list[ContractRead]:
        return [self._contract(row) for row in self._rows(
            "SELECT * FROM public.fn_list_contracts(:user_id, :role)",
            user_id=user_id, role=role,
        )]

    def get_contract(self, contract_id: UUID) -> ContractRead | None:
        row = self._rows(
            "SELECT * FROM public.fn_get_contract(:contract_id)",
            contract_id=contract_id,
        ).first()
        return self._contract(row) if row else None

    def get_my_contract(self, student_id: UUID) -> ContractRead | None:
        row = self._rows(
            "SELECT * FROM public.fn_list_contracts(:student_id, 'Student') LIMIT 1",
            student_id=student_id,
        ).first()
        return self._contract(row) if row else None

