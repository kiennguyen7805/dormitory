from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field, model_validator


class HousingApplicationCreate(BaseModel):
    term_code: str = Field(min_length=1, max_length=30)
    room_id: UUID


class HousingApplicationReject(BaseModel):
    reason: str = Field(min_length=1, max_length=500)


class HousingApplicationRead(BaseModel):
    id: UUID
    student_id: UUID
    student_name: str
    term_code: str
    room_id: UUID | None
    room_code: str | None
    status: str
    rejection_reason: str | None
    created_at: datetime


class AssignRoomRequest(BaseModel):
    start_date: date
    end_date: date

    @model_validator(mode="after")
    def validate_period(self):
        if self.end_date <= self.start_date:
            raise ValueError("Ngày kết thúc phải sau ngày bắt đầu.")
        return self


class TerminateContractRequest(BaseModel):
    termination_date: date


class BedAssignmentRead(BaseModel):
    id: UUID
    bed_id: UUID
    building_code: str
    room_code: str
    bed_code: str
    start_date: date
    end_date: date | None
    status: str


class ContractRead(BaseModel):
    id: UUID
    contract_no: str
    student_id: UUID
    student_name: str
    application_id: UUID
    start_date: date
    end_date: date
    status: str
    base_rate: Decimal
    current_assignment: BedAssignmentRead | None
