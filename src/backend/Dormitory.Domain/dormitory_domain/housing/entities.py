from dataclasses import dataclass, field
from decimal import Decimal
from uuid import UUID, uuid4

from dormitory_domain.common import BedStatus


@dataclass(slots=True)
class Building:
    code: str
    name: str
    address: str
    floors: int
    is_active: bool = True
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        self.code = self.code.strip().upper()
        self.name = self.name.strip()
        if not self.code or not self.name:
            raise ValueError("Building code and name are required")
        if self.floors < 1:
            raise ValueError("Building must have at least one floor")


@dataclass(slots=True)
class RoomType:
    name: str
    default_monthly_rate: Decimal
    is_active: bool = True
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        self.name = self.name.strip()
        if not self.name:
            raise ValueError("Room type name is required")
        if self.default_monthly_rate < 0:
            raise ValueError("Monthly rate cannot be negative")


@dataclass(slots=True)
class Room:
    building_id: UUID
    room_type_id: UUID
    code: str
    floor: int
    is_active: bool = True
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        self.code = self.code.strip().upper()
        if not self.code:
            raise ValueError("Room code is required")
        if self.floor < 1:
            raise ValueError("Room floor must be positive")


@dataclass(slots=True)
class Bed:
    room_id: UUID
    code: str
    is_active: bool = True
    is_occupied: bool = False
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        self.code = self.code.strip().upper()
        if not self.code:
            raise ValueError("Bed code is required")

    @property
    def status(self) -> BedStatus:
        if not self.is_active:
            return BedStatus.MAINTENANCE
        return BedStatus.OCCUPIED if self.is_occupied else BedStatus.AVAILABLE
