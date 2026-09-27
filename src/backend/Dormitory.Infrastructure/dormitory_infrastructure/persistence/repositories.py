from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from dormitory_application.common import BusinessRuleError, ConflictError
from dormitory_application.housing.schemas import (
    BedCreate,
    BedRead,
    BedUpdate,
    BuildingCreate,
    BuildingRead,
    BuildingUpdate,
    RoomCreate,
    RoomMatrixBed,
    RoomMatrixBuilding,
    RoomMatrixRoom,
    RoomBulkGenderUpdate,
    RoomRead,
    RoomTypeCreate,
    RoomTypeRead,
    RoomTypeUpdate,
    RoomUpdate,
)

from .models import BedAssignmentModel, BedModel, BuildingModel, RoomModel, RoomTypeModel, UserModel


class SqlAlchemyHousingRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def _commit(self) -> None:
        try:
            self.db.commit()
        except IntegrityError as exc:
            self.db.rollback()
            raise ConflictError("Duplicate code/name or referenced record is invalid") from exc

    @staticmethod
    def _building(model: BuildingModel) -> BuildingRead:
        return BuildingRead.model_validate(model)

    @staticmethod
    def _room_type(model: RoomTypeModel) -> RoomTypeRead:
        return RoomTypeRead.model_validate(model)

    @staticmethod
    def _room(model: RoomModel) -> RoomRead:
        return RoomRead(
            id=model.id,
            building_id=model.building_id,
            building_code=model.building.code,
            room_type_id=model.room_type_id,
            room_type_name=model.room_type.name,
            code=model.code,
            floor=model.floor,
            gender_policy=model.gender_policy,
            managed_by_staff_id=model.managed_by_staff_id,
            status=model.status,
            is_active=model.is_active,
            note=model.note,
        )

    @staticmethod
    def _bed(model: BedModel, occupied_bed_ids: set[UUID] | None = None) -> BedRead:
        occupied_bed_ids = occupied_bed_ids or set()
        status = (
            "Maintenance"
            if not model.is_active
            else "Occupied"
            if model.id in occupied_bed_ids
            else "Available"
        )
        return BedRead(
            id=model.id,
            room_id=model.room_id,
            code=model.code,
            is_active=model.is_active,
            note=model.note,
            status=status,
        )

    def list_buildings(self) -> list[BuildingRead]:
        return [self._building(x) for x in self.db.scalars(select(BuildingModel).order_by(BuildingModel.code)).all()]

    def get_building(self, item_id: UUID) -> BuildingRead | None:
        item = self.db.get(BuildingModel, item_id)
        return self._building(item) if item else None

    def create_building(self, data: BuildingCreate) -> BuildingRead:
        item = BuildingModel(**data.model_dump())
        item.code = item.code.strip().upper()
        self.db.add(item)
        self._commit()
        self.db.refresh(item)
        return self._building(item)

    def update_building(self, item_id: UUID, data: BuildingUpdate) -> BuildingRead | None:
        item = self.db.get(BuildingModel, item_id)
        if item is None:
            return None
        for key, value in data.model_dump().items():
            setattr(item, key, value)
        item.code = item.code.strip().upper()
        self._commit()
        self.db.refresh(item)
        return self._building(item)

    def delete_building(self, item_id: UUID) -> bool:
        item = self.db.get(BuildingModel, item_id)
        if item is None:
            return False
        occupied = self.db.scalar(
            select(BedAssignmentModel.id)
            .join(BedModel, BedModel.id == BedAssignmentModel.bed_id)
            .join(RoomModel, RoomModel.id == BedModel.room_id)
            .where(RoomModel.building_id == item_id, BedAssignmentModel.status == "Active")
            .limit(1)
        )
        if occupied:
            raise BusinessRuleError("HOUSING_IN_USE", "Tòa nhà đang có sinh viên nội trú.")
        item.is_active = False
        self._commit()
        return True

    def list_room_types(self) -> list[RoomTypeRead]:
        return [self._room_type(x) for x in self.db.scalars(select(RoomTypeModel).order_by(RoomTypeModel.name)).all()]

    def create_room_type(self, data: RoomTypeCreate) -> RoomTypeRead:
        item = RoomTypeModel(**data.model_dump())
        item.name = item.name.strip()
        self.db.add(item)
        self._commit()
        self.db.refresh(item)
        return self._room_type(item)

    def update_room_type(self, item_id: UUID, data: RoomTypeUpdate) -> RoomTypeRead | None:
        item = self.db.get(RoomTypeModel, item_id)
        if item is None:
            return None
        for key, value in data.model_dump().items():
            setattr(item, key, value)
        item.name = item.name.strip()
        self._commit()
        self.db.refresh(item)
        return self._room_type(item)

    def delete_room_type(self, item_id: UUID) -> bool:
        item = self.db.get(RoomTypeModel, item_id)
        if item is None:
            return False
        item.is_active = False
        self._commit()
        return True

    @staticmethod
    def _room_statement():
        return select(RoomModel).options(selectinload(RoomModel.building), selectinload(RoomModel.room_type))

    def list_rooms(self, building_id: UUID | None = None, staff_id: UUID | None = None) -> list[RoomRead]:
        statement = self._room_statement().order_by(RoomModel.floor, RoomModel.code)
        if building_id:
            statement = statement.where(RoomModel.building_id == building_id)
        if staff_id:
            statement = statement.where(RoomModel.managed_by_staff_id == staff_id)
        return [self._room(x) for x in self.db.scalars(statement).all()]

    def create_room(self, data: RoomCreate) -> RoomRead:
        item = RoomModel(**data.model_dump())
        item.code = item.code.strip().upper()
        self.db.add(item)
        self._commit()
        item = self.db.scalar(self._room_statement().where(RoomModel.id == item.id))
        return self._room(item)

    def update_room(self, item_id: UUID, data: RoomUpdate) -> RoomRead | None:
        item = self.db.get(RoomModel, item_id)
        if item is None:
            return None
        for key, value in data.model_dump().items():
            setattr(item, key, value)
        item.code = item.code.strip().upper()
        self._commit()
        item = self.db.scalar(self._room_statement().where(RoomModel.id == item_id))
        return self._room(item)

    def delete_room(self, item_id: UUID) -> bool:
        item = self.db.get(RoomModel, item_id)
        if item is None:
            return False
        occupied = self.db.scalar(
            select(BedAssignmentModel.id)
            .join(BedModel, BedModel.id == BedAssignmentModel.bed_id)
            .where(BedModel.room_id == item_id, BedAssignmentModel.status == "Active")
            .limit(1)
        )
        if occupied:
            raise BusinessRuleError("HOUSING_IN_USE", "Phòng đang có sinh viên nội trú.")
        item.is_active = False
        self._commit()
        return True

    def list_beds(self, room_id: UUID | None = None, staff_id: UUID | None = None) -> list[BedRead]:
        statement = select(BedModel).order_by(BedModel.code)
        if room_id:
            statement = statement.where(BedModel.room_id == room_id)
        if staff_id:
            statement = statement.join(RoomModel).where(RoomModel.managed_by_staff_id == staff_id)
        beds = self.db.scalars(statement).all()
        occupied = self._occupied_bed_ids()
        return [self._bed(x, occupied) for x in beds]

    def create_bed(self, data: BedCreate) -> BedRead:
        item = BedModel(**data.model_dump())
        item.code = item.code.strip().upper()
        self.db.add(item)
        self._commit()
        self.db.refresh(item)
        return self._bed(item)

    def update_bed(self, item_id: UUID, data: BedUpdate) -> BedRead | None:
        item = self.db.get(BedModel, item_id)
        if item is None:
            return None
        for key, value in data.model_dump().items():
            setattr(item, key, value)
        item.code = item.code.strip().upper()
        self._commit()
        self.db.refresh(item)
        return self._bed(item)

    def delete_bed(self, item_id: UUID) -> bool:
        item = self.db.get(BedModel, item_id)
        if item is None:
            return False
        occupied = self.db.scalar(
            select(BedAssignmentModel.id).where(
                BedAssignmentModel.bed_id == item_id,
                BedAssignmentModel.status == "Active",
            ).limit(1)
        )
        if occupied:
            raise BusinessRuleError("HOUSING_IN_USE", "Giường đang được phân cho sinh viên.")
        item.is_active = False
        self._commit()
        return True

    def room_matrix(self, staff_id: UUID | None = None) -> list[RoomMatrixBuilding]:
        statement = select(BuildingModel).options(
            selectinload(BuildingModel.rooms).selectinload(RoomModel.room_type),
            selectinload(BuildingModel.rooms).selectinload(RoomModel.beds),
        ).order_by(BuildingModel.code)
        buildings = self.db.scalars(statement).all()
        occupied = self._occupied_bed_ids()
        return [
            RoomMatrixBuilding(
                id=building.id,
                code=building.code,
                name=building.name,
                rooms=[
                    RoomMatrixRoom(
                        id=room.id,
                        code=room.code,
                        floor=room.floor,
                        room_type=room.room_type.name,
                        gender_policy=room.gender_policy,
                        managed_by_staff_id=room.managed_by_staff_id,
                        beds=[
                            RoomMatrixBed(
                                id=bed.id,
                                code=bed.code,
                                status=self._bed(bed, occupied).status,
                            )
                            for bed in sorted(room.beds, key=lambda x: x.code)
                        ],
                    )
                    for room in sorted(building.rooms, key=lambda x: (x.floor, x.code))
                    if staff_id is None or room.managed_by_staff_id == staff_id
                ],
            )
            for building in buildings
            if staff_id is None or any(room.managed_by_staff_id == staff_id for room in building.rooms)
        ]

    def _occupied_bed_ids(self) -> set[UUID]:
        return set(
            self.db.scalars(
                select(BedAssignmentModel.bed_id).where(
                    BedAssignmentModel.status == "Active"
                )
            ).all()
        )

    def bulk_update_gender(
        self, data: RoomBulkGenderUpdate, actor_id: UUID, is_admin: bool
    ) -> list[RoomRead]:
        statement = select(RoomModel)
        if data.room_ids:
            statement = statement.where(RoomModel.id.in_(data.room_ids))
        elif data.building_id:
            statement = statement.where(RoomModel.building_id == data.building_id)
            if data.floor is not None:
                statement = statement.where(RoomModel.floor == data.floor)
        else:
            raise BusinessRuleError("ROOM_SCOPE_REQUIRED", "Phải chọn tòa, tầng hoặc danh sách phòng.", 422)
        rooms = list(self.db.scalars(statement.with_for_update()).all())
        if not rooms:
            raise BusinessRuleError("ROOM_SCOPE_EMPTY", "Không tìm thấy phòng phù hợp.", 404)
        if not is_admin and any(room.managed_by_staff_id != actor_id for room in rooms):
            raise BusinessRuleError("ROOM_SCOPE_FORBIDDEN", "Staff chỉ được cấu hình phòng mình phụ trách.", 403)
        room_ids = [room.id for room in rooms]
        occupied = self.db.scalar(
            select(BedAssignmentModel.id).join(BedModel).where(
                BedModel.room_id.in_(room_ids), BedAssignmentModel.status == "Active"
            ).limit(1)
        )
        if occupied:
            raise BusinessRuleError(
                "ROOM_OCCUPIED_GENDER_LOCKED",
                "Không thể đổi phân khu giới tính khi phòng còn người ở.",
            )
        for room in rooms:
            room.gender_policy = data.gender_policy
            room.updated_by = actor_id
        self._commit()
        return self.list_rooms(staff_id=None if is_admin else actor_id)
