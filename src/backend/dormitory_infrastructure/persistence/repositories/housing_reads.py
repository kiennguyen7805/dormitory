"""Read housing inventory through PostgreSQL functions."""

from uuid import UUID

from sqlalchemy import text
from sqlalchemy.engine import Connection

from dormitory_application.housing.schemas import (
    BedRead, BuildingRead, RoomRead,
)


class StoredHousingReads:
    def __init__(self, db: Connection) -> None:
        self.db = db

    def _rows(self, query: str, **params):
        return self.db.execute(text(query), params).mappings()

    def list_buildings(self) -> list[BuildingRead]:
        return [BuildingRead.model_validate(dict(row)) for row in self._rows(
            "SELECT * FROM public.fn_list_buildings()"
        )]

    def get_building(self, item_id: UUID) -> BuildingRead | None:
        row = self._rows("SELECT * FROM public.fn_get_building(:item_id)", item_id=item_id).first()
        return BuildingRead.model_validate(dict(row)) if row else None

    def list_rooms(
        self, building_id: UUID | None = None, staff_id: UUID | None = None,
    ) -> list[RoomRead]:
        return [RoomRead.model_validate(dict(row)) for row in self._rows(
            "SELECT * FROM public.fn_list_rooms(:building_id, :staff_id)",
            building_id=building_id, staff_id=staff_id,
        )]

    def get_room(self, item_id: UUID) -> RoomRead | None:
        row = self._rows("SELECT * FROM public.fn_get_room(:item_id)", item_id=item_id).first()
        return RoomRead.model_validate(dict(row)) if row else None

    def list_beds(
        self, room_id: UUID | None = None, staff_id: UUID | None = None,
    ) -> list[BedRead]:
        return [BedRead.model_validate(dict(row)) for row in self._rows(
            "SELECT * FROM public.fn_list_beds(:room_id, :staff_id)",
            room_id=room_id, staff_id=staff_id,
        )]

    def get_bed(self, item_id: UUID) -> BedRead | None:
        row = self._rows("SELECT * FROM public.fn_get_bed(:item_id)", item_id=item_id).first()
        return BedRead.model_validate(dict(row)) if row else None

