from uuid import UUID

from dormitory_application.common import NotFoundError

from .interfaces import HousingRepository
from .schemas import (
    BedCreate,
    BedRead,
    BedUpdate,
    BuildingCreate,
    BuildingRead,
    BuildingUpdate,
    RoomCreate,
    RoomRead,
    RoomUpdate,
)


class HousingService:
    def __init__(self, repository: HousingRepository) -> None:
        self.repository = repository

    def list_buildings(self) -> list[BuildingRead]:
        return self.repository.list_buildings()

    def get_building(self, item_id: UUID) -> BuildingRead:
        item = self.repository.get_building(item_id)
        if item is None:
            raise NotFoundError("Building not found")
        return item

    def create_building(self, data: BuildingCreate) -> BuildingRead:
        return self.repository.create_building(data)

    def update_building(self, item_id: UUID, data: BuildingUpdate) -> BuildingRead:
        item = self.repository.update_building(item_id, data)
        if item is None:
            raise NotFoundError("Building not found")
        return item

    def delete_building(self, item_id: UUID) -> None:
        if not self.repository.delete_building(item_id):
            raise NotFoundError("Building not found")

    def list_rooms(self, building_id: UUID | None = None, staff_id: UUID | None = None) -> list[RoomRead]:
        return self.repository.list_rooms(building_id, staff_id)

    def create_room(self, data: RoomCreate) -> RoomRead:
        return self.repository.create_room(data)

    def update_room(self, item_id: UUID, data: RoomUpdate) -> RoomRead:
        item = self.repository.update_room(item_id, data)
        if item is None:
            raise NotFoundError("Room not found")
        return item

    def delete_room(self, item_id: UUID) -> None:
        if not self.repository.delete_room(item_id):
            raise NotFoundError("Room not found")

    def list_beds(self, room_id: UUID | None = None, staff_id: UUID | None = None) -> list[BedRead]:
        return self.repository.list_beds(room_id, staff_id)

    def create_bed(self, data: BedCreate) -> BedRead:
        return self.repository.create_bed(data)

    def update_bed(self, item_id: UUID, data: BedUpdate) -> BedRead:
        item = self.repository.update_bed(item_id, data)
        if item is None:
            raise NotFoundError("Bed not found")
        return item

    def delete_bed(self, item_id: UUID) -> None:
        if not self.repository.delete_bed(item_id):
            raise NotFoundError("Bed not found")

    def bulk_update_gender(self, data, actor_id: UUID, is_admin: bool) -> list[RoomRead]:
        return self.repository.bulk_update_gender(data, actor_id, is_admin)
