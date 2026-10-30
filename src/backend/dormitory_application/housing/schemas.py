from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class BuildingBase(BaseModel):
    code: str = Field(min_length=1, max_length=20)
    name: str = Field(min_length=1, max_length=120)
    address: str = Field(default="", max_length=250)
    floors: int = Field(ge=1, le=100)
    is_active: bool = True


class BuildingCreate(BuildingBase):
    pass


class BuildingUpdate(BuildingBase):
    pass


class BuildingRead(BuildingBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID


class RoomBase(BaseModel):
    building_id: UUID
    code: str = Field(min_length=1, max_length=20)
    floor: int = Field(ge=1, le=100)
    capacity: int = Field(ge=1, le=12)
    monthly_rate: Decimal = Field(ge=0)
    gender_policy: str = Field(default="Unassigned", pattern="^(Male|Female|Mixed|Unassigned)$")
    managed_by_staff_id: UUID | None = None
    status: str = Field(default="Available", pattern="^(Available|Maintenance|Inactive)$")
    is_active: bool = True
    note: str | None = Field(default=None, max_length=500)


class RoomCreate(RoomBase):
    pass


class RoomUpdate(RoomBase):
    pass


class RoomRead(RoomBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    building_code: str


class BedBase(BaseModel):
    room_id: UUID
    code: str = Field(min_length=1, max_length=20)
    is_active: bool = True
    note: str | None = Field(default=None, max_length=300)


class BedCreate(BedBase):
    pass


class BedUpdate(BedBase):
    pass


class BedRead(BedBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    status: str


class RoomBulkGenderUpdate(BaseModel):
    gender_policy: str = Field(pattern="^(Male|Female|Mixed|Unassigned)$")
    building_id: UUID | None = None
    floor: int | None = Field(default=None, ge=1)
    room_ids: list[UUID] = Field(default_factory=list)
