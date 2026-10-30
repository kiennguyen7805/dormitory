"""Housing repository backed only by PostgreSQL functions."""

from uuid import UUID, uuid4

from sqlalchemy.engine import Connection

from dormitory_application.common import BusinessRuleError
from dormitory_application.housing.schemas import (
    BedCreate, BedRead, BedUpdate, BuildingCreate, BuildingRead, BuildingUpdate,
    RoomBulkGenderUpdate, RoomCreate, RoomRead, RoomUpdate,
)

from .housing_reads import StoredHousingReads
from .housing_writes import StoredHousingWrites


class StoredHousingRepository:
    def __init__(self, db: Connection) -> None:
        self.reads = StoredHousingReads(db)
        self.writes = StoredHousingWrites(db)

    def list_buildings(self) -> list[BuildingRead]:
        return self.reads.list_buildings()

    def get_building(self, item_id: UUID) -> BuildingRead | None:
        return self.reads.get_building(item_id)

    def create_building(self, data: BuildingCreate) -> BuildingRead:
        item_id = uuid4()
        self.writes.save("building", item_id, data, True)
        return self.reads.get_building(item_id)

    def update_building(self, item_id: UUID, data: BuildingUpdate) -> BuildingRead | None:
        return self.reads.get_building(item_id) if self.writes.save(
            "building", item_id, data, False
        ) else None

    def delete_building(self, item_id: UUID) -> bool:
        result = self.writes.deactivate("building", item_id)
        if result == -1:
            raise BusinessRuleError("HOUSING_IN_USE", "Tòa nhà đang có sinh viên nội trú.")
        return result == 1

    def list_rooms(
        self, building_id: UUID | None = None, staff_id: UUID | None = None,
    ) -> list[RoomRead]:
        return self.reads.list_rooms(building_id, staff_id)

    def create_room(self, data: RoomCreate) -> RoomRead:
        item_id = uuid4()
        self.writes.create_room(item_id, data)
        return self.reads.get_room(item_id)

    def update_room(self, item_id: UUID, data: RoomUpdate) -> RoomRead | None:
        return self.reads.get_room(item_id) if self.writes.save(
            "room", item_id, data, False
        ) else None

    def delete_room(self, item_id: UUID) -> bool:
        result = self.writes.deactivate("room", item_id)
        if result == -1:
            raise BusinessRuleError("HOUSING_IN_USE", "Phòng đang có sinh viên nội trú.")
        return result == 1

    def list_beds(
        self, room_id: UUID | None = None, staff_id: UUID | None = None,
    ) -> list[BedRead]:
        return self.reads.list_beds(room_id, staff_id)

    def create_bed(self, data: BedCreate) -> BedRead:
        item_id = uuid4()
        self.writes.save("bed", item_id, data, True)
        return self.reads.get_bed(item_id)

    def update_bed(self, item_id: UUID, data: BedUpdate) -> BedRead | None:
        return self.reads.get_bed(item_id) if self.writes.save(
            "bed", item_id, data, False
        ) else None

    def delete_bed(self, item_id: UUID) -> bool:
        result = self.writes.deactivate("bed", item_id)
        if result == -1:
            raise BusinessRuleError("HOUSING_IN_USE", "Giường đang được phân cho sinh viên.")
        return result == 1

    def bulk_update_gender(
        self, data: RoomBulkGenderUpdate, actor_id: UUID, is_admin: bool
    ) -> list[RoomRead]:
        result = self.writes.bulk_update_gender(
            data.room_ids, data.building_id, data.floor, data.gender_policy,
            actor_id, is_admin,
        )
        if result == -1:
            raise BusinessRuleError("ROOM_SCOPE_REQUIRED", "Phải chọn tòa, tầng hoặc danh sách phòng.", 422)
        if result == -2:
            raise BusinessRuleError("ROOM_SCOPE_EMPTY", "Không tìm thấy phòng phù hợp.", 404)
        if result == -3:
            raise BusinessRuleError("ROOM_SCOPE_FORBIDDEN", "Staff chỉ được cấu hình phòng mình phụ trách.", 403)
        if result == -4:
            raise BusinessRuleError(
                "ROOM_OCCUPIED_GENDER_LOCKED",
                "Không thể đổi phân khu giới tính khi phòng còn người ở.",
            )
        return self.reads.list_rooms(staff_id=None if is_admin else actor_id)
