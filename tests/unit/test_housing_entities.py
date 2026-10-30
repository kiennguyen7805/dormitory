from decimal import Decimal
from uuid import uuid4

import pytest

from dormitory_domain.common import BedStatus
from dormitory_domain.housing import Bed, Building, RoomType


def test_building_normalizes_code() -> None:
    building = Building(code=" a1 ", name="Khu A", address="", floors=5)
    assert building.code == "A1"


def test_building_requires_positive_floor_count() -> None:
    with pytest.raises(ValueError):
        Building(code="A", name="Khu A", address="", floors=0)


def test_room_type_rejects_negative_rate() -> None:
    with pytest.raises(ValueError):
        RoomType(name="Phòng 4", default_monthly_rate=Decimal("-1"))


def test_bed_status_is_derived() -> None:
    available = Bed(room_id=uuid4(), code="G1")
    occupied = Bed(room_id=uuid4(), code="G2", is_occupied=True)
    maintenance = Bed(room_id=uuid4(), code="G3", is_active=False, is_occupied=True)

    assert available.status is BedStatus.AVAILABLE
    assert occupied.status is BedStatus.OCCUPIED
    assert maintenance.status is BedStatus.MAINTENANCE
